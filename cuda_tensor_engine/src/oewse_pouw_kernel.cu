#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <stdint.h>

// Simple device-side Keccak/Murmur-inspired mix to finalize state tensor into a 32-bit proof hash
__device__ __forceinline__ uint32_t compute_proof_hash(uint32_t state_accumulator, uint32_t nonce) {
    uint32_t hash = state_accumulator ^ nonce;
    hash ^= hash >> 16;
    hash *= 0x7feb352d;
    hash ^= hash >> 15;
    hash *= 0x846ca68b;
    hash ^= hash >> 16;
    return hash;
}

/**
 * @global oewse_pouw_search_kernel
 * @notice Executes the PoUW loop by replacing Keccak with Ternary Matrix Multiplication (XNOR + Popcount)
 * @param prompt_bits        Packed bit-representation of the input prompt/tokens
 * @param weight_matrix_pos  Bitmask of positive ternary weights (+1)
 * @param weight_matrix_neg  Bitmask of negative ternary weights (-1)
 * @param target_difficulty  The network target threshold. Proof hash must be less than this.
 * @param max_nonces         Number of nonces to scan per thread allocation
 * @param out_valid_nonce    Output pointer to capture the winning nonce
 * @param out_proof_hash     Output pointer to capture the valid proof hash
 */
__global__ void oewse_pouw_search_kernel(
    const uint32_t* __restrict__ prompt_bits,
    const uint32_t* __restrict__ weight_matrix_pos,
    const uint32_t* __restrict__ weight_matrix_neg,
    const uint32_t target_difficulty,
    const uint32_t max_nonces,
    uint32_t* out_valid_nonce,
    uint32_t* out_proof_hash
) {
    // Shared memory cache for the active prompt chunk to minimize global VRAM reads across the warp
    __shared__ uint32_t shared_prompt[128];
    
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int local_tid = threadIdx.x;
    
    // Cooperatively load prompt tokens into shared memory
    if (local_tid < 128) {
        shared_prompt[local_tid] = prompt_bits[local_tid];
    }
    __syncthreads();

    // Each thread takes a unique segment of the nonce workspace
    uint32_t base_nonce = tid * max_nonces;

    for (uint32_t n = 0; n < max_nonces; ++n) {
        // Short-circuit if another thread on the grid already solved the block
        if (*out_valid_nonce != 0) return;

        uint32_t current_nonce = base_nonce + n;
        uint32_t accumulator_positive = 0;
        uint32_t accumulator_negative = 0;

        // --- BEGIN OE-WSE TERNARY FORWARD LAYER PASS ---
        // 40 Layers unrolled structurally or processed via loop execution
        #pragma unroll
        for (int layer = 0; layer < 40; ++layer) {
            // Fetch the weight vectors for this specific node layer slice
            uint32_t w_pos = weight_matrix_pos[layer * blockDim.x + local_tid];
            uint32_t w_neg = weight_matrix_neg[layer * blockDim.x + local_tid];

            // Mix nonce state into execution to maintain path mutation
            uint32_t mixed_input = shared_prompt[local_tid ^ (current_nonce & 0x7F)];

            // Ternary Processing via bitwise intrinsics
            uint32_t match_pos = ~(mixed_input ^ w_pos);
            uint32_t match_neg = ~(mixed_input ^ w_neg);

            // Accumulate high-speed bit counts directly into register space
            accumulator_positive += __popc(match_pos);
            accumulator_negative += __popc(match_neg);
        }
        // --- END OE-WSE TERNARY FORWARD LAYER PASS ---

        // Extract structural token metrics
        uint32_t final_signal_state = accumulator_positive - accumulator_negative;

        // Generate the attestation hash proof
        uint32_t proof_hash = compute_proof_hash(final_signal_state, current_nonce);

        // Verification condition
        if (proof_hash < target_difficulty) {
            // Atomic check to ensure thread priority settlement
            uint32_t previous = atomicCAS(out_valid_nonce, 0, current_nonce);
            if (previous == 0) {
                out_proof_hash[0] = proof_hash;
                return;
            }
        }
    }
}

struct OewseCudaContext {
    uint32_t* d_prompt;
    uint32_t* d_w_pos;
    uint32_t* d_w_neg;
    uint32_t* d_out_nonce;
    uint32_t* d_out_hash;
};

// Host-side execution wrappers to hook straight into the Rust FFI driver layer
extern "C" void* init_oewse_context(uint32_t threads_per_block) {
    OewseCudaContext* ctx = (OewseCudaContext*)malloc(sizeof(OewseCudaContext));
    if (!ctx) return nullptr;

    cudaMalloc((void**)&ctx->d_prompt, 128 * sizeof(uint32_t));
    cudaMalloc((void**)&ctx->d_w_pos, 40 * threads_per_block * sizeof(uint32_t));
    cudaMalloc((void**)&ctx->d_w_neg, 40 * threads_per_block * sizeof(uint32_t));
    cudaMalloc((void**)&ctx->d_out_nonce, sizeof(uint32_t));
    cudaMalloc((void**)&ctx->d_out_hash, sizeof(uint32_t));

    return (void*)ctx;
}

extern "C" void upload_oewse_weights(
    void* context_ptr,
    const uint32_t* weight_matrix_pos,
    const uint32_t* weight_matrix_neg,
    uint32_t threads_per_block
) {
    OewseCudaContext* ctx = (OewseCudaContext*)context_ptr;
    if (!ctx) return;

    cudaMemcpy(ctx->d_w_pos, weight_matrix_pos, 40 * threads_per_block * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemcpy(ctx->d_w_neg, weight_matrix_neg, 40 * threads_per_block * sizeof(uint32_t), cudaMemcpyHostToDevice);
}

extern "C" void run_oewse_pouw_search_with_context(
    void* context_ptr,
    const uint32_t* prompt_bits,
    uint32_t target_difficulty,
    uint32_t max_nonces,
    uint32_t blocks,
    uint32_t threads_per_block,
    uint32_t* h_valid_nonce,
    uint32_t* h_proof_hash
) {
    OewseCudaContext* ctx = (OewseCudaContext*)context_ptr;
    if (!ctx) return;

    cudaMemcpy(ctx->d_prompt, prompt_bits, 128 * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemset(ctx->d_out_nonce, 0, sizeof(uint32_t));
    cudaMemset(ctx->d_out_hash, 0, sizeof(uint32_t));

    oewse_pouw_search_kernel<<<blocks, threads_per_block>>>(
        ctx->d_prompt,
        ctx->d_w_pos,
        ctx->d_w_neg,
        target_difficulty,
        max_nonces,
        ctx->d_out_nonce,
        ctx->d_out_hash
    );

    cudaDeviceSynchronize();

    cudaMemcpy(h_valid_nonce, ctx->d_out_nonce, sizeof(uint32_t), cudaMemcpyDeviceToHost);
    cudaMemcpy(h_proof_hash, ctx->d_out_hash, sizeof(uint32_t), cudaMemcpyDeviceToHost);
}

extern "C" void free_oewse_context(void* context_ptr) {
    OewseCudaContext* ctx = (OewseCudaContext*)context_ptr;
    if (!ctx) return;

    cudaFree(ctx->d_prompt);
    cudaFree(ctx->d_w_pos);
    cudaFree(ctx->d_w_neg);
    cudaFree(ctx->d_out_nonce);
    cudaFree(ctx->d_out_hash);
    free(ctx);
}

// Keep old entrypoint for backward compatibility/simplicity where context-less is preferred
extern "C" void run_oewse_pouw_search(
    const uint32_t* prompt_bits,
    const uint32_t* weight_matrix_pos,
    const uint32_t* weight_matrix_neg,
    uint32_t target_difficulty,
    uint32_t max_nonces,
    uint32_t blocks,
    uint32_t threads_per_block,
    uint32_t* h_valid_nonce,
    uint32_t* h_proof_hash
) {
    void* ctx = init_oewse_context(threads_per_block);
    if (!ctx) return;

    upload_oewse_weights(ctx, weight_matrix_pos, weight_matrix_neg, threads_per_block);
    run_oewse_pouw_search_with_context(
        ctx, prompt_bits, target_difficulty, max_nonces, blocks, threads_per_block, h_valid_nonce, h_proof_hash
    );
    free_oewse_context(ctx);
}

// ── Transformer Inference Kernel ─────────────────────────────────────────
// Chains the same 40-layer XNOR+popcount pass but produces output logits
// instead of mining for a proof hash. Used for actual text generation.

__global__ void oewse_transformer_infer_kernel(
    const uint32_t* __restrict__ prompt_tokens,
    const uint32_t* __restrict__ weight_matrix_pos,
    const uint32_t* __restrict__ weight_matrix_neg,
    float* __restrict__ output_logits,
    const uint32_t num_layers,
    const uint32_t hidden_dim,
    const uint32_t vocab_size
) {
    __shared__ uint32_t shared_tokens[128];

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int local_tid = threadIdx.x;

    // Load input tokens into shared memory
    if (local_tid < 128) {
        shared_tokens[local_tid] = prompt_tokens[local_tid];
    }
    __syncthreads();

    // Run layer-chain inference
    uint32_t accumulator_positive = 0;
    uint32_t accumulator_negative = 0;

    #pragma unroll
    for (int layer = 0; layer < (int)num_layers; ++layer) {
        uint32_t w_pos = weight_matrix_pos[layer * blockDim.x + local_tid];
        uint32_t w_neg = weight_matrix_neg[layer * blockDim.x + local_tid];

        uint32_t input = shared_tokens[local_tid];

        // XNOR + popcount for this layer
        uint32_t match_pos = __popc(~(input ^ w_pos));
        uint32_t match_neg = __popc(~(input ^ w_neg));

        accumulator_positive += match_pos;
        accumulator_negative += match_neg;

        // Propagate activation to next layer
        shared_tokens[local_tid] = input ^ (w_pos ^ w_neg);
        __syncthreads();
    }

    // Final score = positive minus negative (net activation)
    int32_t net_score = (int32_t)(accumulator_positive - accumulator_negative);

    // Write output logit for this vocabulary position
    if (tid < (int)vocab_size) {
        output_logits[tid] = (float)net_score;
    }
}

// Host wrapper for transformer inference
extern "C" void run_oewse_transformer_infer(
    const uint32_t* prompt_tokens,
    const uint32_t* weight_matrix_pos,
    const uint32_t* weight_matrix_neg,
    float* output_logits,
    uint32_t num_layers,
    uint32_t hidden_dim,
    uint32_t vocab_size,
    uint32_t threads_per_block,
    uint32_t blocks
) {
    // Device memory
    uint32_t* d_tokens;
    uint32_t* d_w_pos;
    uint32_t* d_w_neg;
    float* d_logits;

    cudaMalloc(&d_tokens, 128 * sizeof(uint32_t));
    cudaMalloc(&d_w_pos, num_layers * threads_per_block * sizeof(uint32_t));
    cudaMalloc(&d_w_neg, num_layers * threads_per_block * sizeof(uint32_t));
    cudaMalloc(&d_logits, vocab_size * sizeof(float));

    cudaMemcpy(d_tokens, prompt_tokens, 128 * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemcpy(d_w_pos, weight_matrix_pos, num_layers * threads_per_block * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemcpy(d_w_neg, weight_matrix_neg, num_layers * threads_per_block * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemset(d_logits, 0, vocab_size * sizeof(float));

    oewse_transformer_infer_kernel<<<blocks, threads_per_block>>>(
        d_tokens, d_w_pos, d_w_neg, d_logits, num_layers, hidden_dim, vocab_size
    );

    cudaDeviceSynchronize();
    cudaMemcpy(output_logits, d_logits, vocab_size * sizeof(float), cudaMemcpyDeviceToHost);

    cudaFree(d_tokens);
    cudaFree(d_w_pos);
    cudaFree(d_w_neg);
    cudaFree(d_logits);
}
