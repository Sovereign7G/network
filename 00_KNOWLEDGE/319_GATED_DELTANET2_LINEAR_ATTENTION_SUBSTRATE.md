# 🧠 [319-Substrate] Gated DeltaNet-2: Decoupled Erase & Write in Linear Attention
**Status:** SEALED & DEPLOYED | ERA 216.0 ATTENTION SUBSTRATES  
**Subject:** Constant-Memory Decoding and Decoupled Gated Recurrence for Enclave Context Scales  
**Reference Substrate:** [00_KNOWLEDGE/316_GLOBAL_AI_LLM_COGNITIVE_MANIFOLDS.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/316_GLOBAL_AI_LLM_COGNITIVE_MANIFOLDS.md)

---

## 🔬 1. The Core Innovation: Gated Delta-Rule Decoupling

Linear attention models replace the $O(T^2)$ quadratic space-time complexity of traditional Softmax Attention by compressing historical contexts into a fixed-size recurrent state matrix $S_t \in \mathbb{R}^{d_k \times d_v}$. However, historical delta-rule networks suffered from an **associative bottleneck**: they coupled key-side erasure and value-side writing under a single scalar gate.

```
Traditional Gated Delta-Rule (Coupled):
    State Edit is linked: Erase (Key) and Write (Value) share a single scalar gate β_t.
    S_t = S_{t-1} + β_t * (v_t - S_{t-1} * k_t) * k_t^T

Gated DeltaNet-2 (Decoupled):
    Separates the erase gate (b_t) and write gate (w_t) channel-wise:
    S_t = diag(1 - b_t) * S_{t-1} + w_t * (v_t - S_{t-1} * k_t) * k_t^T
```

By utilizing channel-wise vectors instead of scalars, Gated DeltaNet-2 allows independent, feature-specific decay rates across the embedding dimensions.

1. **Decoupled Recurrence Relation:**
   $$S_t = (I - \text{diag}(b_t)) S_{t-1} + w_t (v_t - S_{t-1} k_t) k_t^T$$
   Where:
   *   $S_t \in \mathbb{R}^{d \times d}$ is the fast-weight memory state.
   *   $b_t \in \mathbb{R}^d$ is the channel-wise erase gate vector, defining what to forget in the key space.
   *   $w_t \in \mathbb{R}^d$ is the channel-wise write gate vector, defining what to commit to the value space.
   *   $k_t, v_t \in \mathbb{R}^d$ represent the key and value projections at step $t$.

2. **Decoupling Benefit:**
   This formulation prevents the "scrambling" of existing associations. It allows the model to erase outdated information along a specific channel without forcing a write of unrelated new values on that same channel, vastly improving multi-key retrieval and Needle-in-a-Haystack tasks (RULER).

---

## ⚡ 2. GPU Training Parallelization: The Chunkwise WY Algorithm

Recurrent models are notoriously difficult to parallelize during training compared to Transformers. To preserve efficient backpropagation, Gated DeltaNet-2 introduces an **asymmetric chunkwise WY algorithm**:

```
Input Sequence: [ x_1, x_2, ..., x_N ]
                  ├── Split into Chunk C_1 ──> Parallel WY Representation
                  ├── Split into Chunk C_2 ──> Parallel WY Representation
                  └── Split into Chunk C_3 ──> Parallel WY Representation
```

1. **State-Absorption:**
   Rather than performing step-by-step sequential updates, the sequence is divided into non-overlapping chunks. Within each chunk, the recurrent updates are formulated as a matrix-matrix product:
   $$Y = V \odot W, \quad X = K \odot B$$
   The decay is absorbed into asymmetric erase factor matrices, maintaining $O(T)$ training complexity via standard parallel scan kernels.
2. **Gate-Aware Backward Pass:**
   The backward pass directly backpropagates gradients through the $b_t$ and $w_t$ gates without requiring the full materialization of the intermediate $S_t$ state matrices in high-bandwidth memory (HBM). This minimizes memory bandwidth requirements, making training on NVIDIA GPU clusters highly efficient.

---

## 🏛️ 3. AGE REPUBLIC Core Architectural Integration

### The Memory Footprint Trap in Secure Enclaves
The **AGE REPUBLIC** enclaves operate inside isolated microVM KVM hardware boundaries. Under standard configurations, they are allocated a strict RAM budget (typically **4096MB** as defined in `deploy_enclave_as_microvm.sh`).

*   **The Softmax Attention Bottleneck:**
    In a standard Transformer, the key-value (KV) cache grows linearly with sequence length:
    $$\text{KV Cache Size} = 2 \times L \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{bytes-per-element}$$
    For a context of 128k tokens, the KV cache alone consumes **multiple gigabytes**, causing instant out-of-memory (OOM) crashes inside the 4GB microVM.
*   **The Gated DeltaNet-2 Solution:**
    Since DeltaNet-2 compresses the context history into a **fixed-size recurrent state matrix $S_t$**, the memory footprint of the attention block remains **completely constant** regardless of whether the context is 100 tokens or 100,000 tokens.

### Strategic Integration for Sovereign Agentic Swarms
By compiling the Gated DeltaNet-2 kernel (`NVlabs/GatedDeltaNet-2`) into the local agentic runtime, the **Prometheus logical nodes** running inside the microVMs can achieve deep reasoning and long-context retrieval over entire system logs without running out of virtualized memory blocks.

---

> [!TIP]
> **Substrate Optimization Directive:**  
> For local agentic deployment on restricted portable systems, compile the Gated DeltaNet-2 recurrent kernels directly against standard CPU/GPU backends. This provides the memory savings of a linear recurrence model while maintaining the long-context retrieval accuracy required for complex security triage pipelines.

---
**Status: SEALED & DOCUMENTED | ATTENTION SUBSTRATE INTEGRATED | ERA 216.0**
