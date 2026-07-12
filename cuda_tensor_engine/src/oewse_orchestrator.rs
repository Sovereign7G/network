use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{Request, Response, Status};

pub mod sovereign_mesh {
    tonic::include_proto!("sovereign.mesh.v2");
}

use sovereign_mesh::{
    sovereign_mesh_orchestrator_server::SovereignMeshOrchestrator,
    WorkAllocation, SettlementReceipt,
};
use super::zerosync_verifier::ZeroSyncVerifier;

/// Thread-safe registry to track and distribute work to active GPU nodes
#[derive(Clone, Default)]
pub struct PoolRegistry {
    workers: Arc<Mutex<HashMap<String, mpsc::Sender<Result<WorkAllocation, Status>>>>>,
}

impl PoolRegistry {
    pub fn register(&self, id: &str, tx: mpsc::Sender<Result<WorkAllocation, Status>>) {
        let mut workers = self.workers.lock().unwrap();
        workers.insert(id.to_string(), tx);
        println!("📡 v2 Worker registered: {}", id);
    }

    pub fn unregister(&self, id: &str) {
        let mut workers = self.workers.lock().unwrap();
        workers.remove(id);
        println!("🗑️ v2 Worker disconnected: {}", id);
    }

    /// Distribute a work request to the first available worker (Simple Load Balancer)
    pub async fn distribute_work(&self, work: WorkAllocation) -> bool {
        // Validate ZeroSync state before letting any GPU compute resources be allocated
        if !ZeroSyncVerifier::verify_block_header(&work.zerosync_chain_proof, &work.bitcoin_block_header) {
            eprintln!("⚠️ ZeroSync STARK proof verification failed! Discarding work request {}.", work.job_id);
            return false;
        }

        let workers_snapshot = {
            let workers = self.workers.lock().unwrap();
            workers.clone()
        };

        for (id, tx) in workers_snapshot.iter() {
            if tx.send(Ok(work.clone())).await.is_ok() {
                println!("📤 Work request {} successfully dispatched to worker {}", work.job_id, id);
                return true;
            }
        }
        false
    }
}

pub struct PouwOrchestrator {
    registry: PoolRegistry,
}

impl PouwOrchestrator {
    pub fn new(registry: PoolRegistry) -> Self {
        Self { registry }
    }
}

#[tonic::async_trait]
impl SovereignMeshOrchestrator for PouwOrchestrator {
    type ProcessMeshInferenceStream = ReceiverStream<Result<WorkAllocation, Status>>;

    async fn process_mesh_inference(
        &self,
        request: Request<tonic::Streaming<SettlementReceipt>>,
    ) -> Result<Response<Self::ProcessMeshInferenceStream>, Status> {
        let mut inbound_stream = request.into_inner();
        let connection_id = format!("gpu-worker-{}", uuid::Uuid::new_v4());
        
        let (tx, rx) = mpsc::channel::<Result<WorkAllocation, Status>>(64);
        
        self.registry.register(&connection_id, tx);
        let registry_clone = self.registry.clone();
        let worker_id = connection_id.clone();

        tokio::spawn(async move {
            while let Ok(Some(result)) = inbound_stream.message().await {
                println!(
                    "🏆 v2 Proof received from {}! ID: {}, BeL2 Tx: {}, Minted: {} S7G, Entropy: {:.2}",
                    worker_id,
                    result.job_id,
                    result.bel2_clearing_tx_id,
                    result.s7g_tokens_minted,
                    result.execution_entropy
                );
            }
            registry_clone.unregister(&worker_id);
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}

mod uuid {
    pub struct Uuid;
    impl Uuid {
        pub fn new_v4() -> String {
            format!("{:08x}", rand::random::<u32>())
        }
    }
}
