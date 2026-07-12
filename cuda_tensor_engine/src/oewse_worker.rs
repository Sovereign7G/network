use std::sync::Arc;
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{transport::Channel, Request};

pub mod sovereign_mesh {
    tonic::include_proto!("sovereign.mesh.v2");
}

use sovereign_mesh::{
    sovereign_mesh_orchestrator_client::SovereignMeshOrchestratorClient,
    WorkAllocation, SettlementReceipt,
};

pub struct MeshWorker {
    client: SovereignMeshOrchestratorClient<Channel>,
    gpu_weights_pos: Arc<Vec<u32>>,
    gpu_weights_neg: Arc<Vec<u32>>,
}

impl MeshWorker {
    pub fn new(channel: Channel, weights_pos: Vec<u32>, weights_neg: Vec<u32>) -> Self {
        Self {
            client: SovereignMeshOrchestratorClient::new(channel),
            gpu_weights_pos: Arc::new(weights_pos),
            gpu_weights_neg: Arc::new(weights_neg),
        }
    }

    pub async fn start_execution_loop(self, outbound_buffer_size: usize) -> Result<(), Box<dyn std::error::Error>> {
        let (tx, rx) = mpsc::channel::<SettlementReceipt>(outbound_buffer_size);
        let outbound_stream = ReceiverStream::new(rx);

        let response = self.client.clone().process_mesh_inference(Request::new(outbound_stream)).await?;
        let mut inbound_stream = response.into_inner();

        println!("🟢 gRPC Client: Connected to v2 pool coordinator. Ready for activations...");

        // Initialize stateful GPU/CUDA execution context and upload weights once
        let threads_per_block = 256;
        let gpu_ctx = Arc::new(super::oewse_driver::OewseGpuContext::new(threads_per_block));
        gpu_ctx.upload_weights(&self.gpu_weights_pos, &self.gpu_weights_neg);

        while let Some(request) = inbound_stream.message().await? {
            let tx_clone = tx.clone();
            let gpu_ctx_clone = Arc::clone(&gpu_ctx);

            tokio::task::spawn_blocking(move || {
                if let Some((winning_nonce, proof_hash)) = execute_cuda_pass_with_context(&request, &gpu_ctx_clone) {
                    let result = SettlementReceipt {
                        job_id: request.job_id,
                        proof_hash: proof_hash.to_le_bytes().to_vec(),
                        verified_by_laws_of_math: true,
                        // Elastos BeL2 Integration: Generate a mock transaction ID for the arbiter payout clearing
                        bel2_clearing_tx_id: format!("bel2-tx-{}", winning_nonce),
                        s7g_tokens_minted: 100, // Programmatic payout metric
                        execution_entropy: 0.18,
                        signal_change: 108,
                    };
                    if let Err(e) = tx_clone.blocking_send(result) {
                        eprintln!("❌ Failed to send result through channel: {}", e);
                    }
                }
            });
        }

        Ok(())
    }
}

fn execute_cuda_pass_with_context(req: &WorkAllocation, gpu_ctx: &super::oewse_driver::OewseGpuContext) -> Option<(u64, u32)> {
    let mut prompt_bits = [0u32; 128];
    
    let packed = &req.packed_ternary_activations;
    if packed.len() >= 32 {
        for i in 0..32 {
            let byte = packed[i];
            for pair_idx in 0..4 {
                let shift = (3 - pair_idx) * 2;
                let bit_pair = (byte >> shift) & 0x03;
                prompt_bits[(i * 4) + pair_idx] = bit_pair as u32;
            }
        }
    }

    // Call native FFI driver functions using pre-allocated GPU context
    gpu_ctx.mine_inference_proof(
        &prompt_bits,
        req.target_difficulty,
    ).map(|(nonce, hash)| (nonce as u64, hash))
}
