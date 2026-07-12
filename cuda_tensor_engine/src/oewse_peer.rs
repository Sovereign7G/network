use std::sync::Arc;
use tokio::sync::Mutex;
use serde::{Serialize, Deserialize};

use super::oewse_driver::OewseGpuContext;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ModelInfo {
    pub name: String,
    pub tiles: u32,
    pub layers: u32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct WorkerCapabilities {
    pub node_id: String,
    pub models_loaded: Vec<ModelInfo>,
    pub max_tiles: u32,
    pub avg_latency_ms: u32,
    pub current_load: f32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct AITaskRequest {
    pub task_id: String,
    pub model_name: String,
    pub target_difficulty: u32,
    pub packed_ternary_activations: Vec<u8>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct AITaskResponse {
    pub task_id: String,
    pub node_id: String,
    pub proof_hash: Vec<u8>,
    pub winning_nonce: u64,
    pub latency_us: u64,
}

pub struct OewseP2PWorker {
    pub node_id: String,
    pub gpu_context: Arc<OewseGpuContext>,
    pub capabilities: WorkerCapabilities,
    pub gossip_topic: String,
}

impl OewseP2PWorker {
    pub fn new(
        node_id: &str,
        spat_model_path: &str,
    ) -> Result<Self, Box<dyn std::error::Error>> {
        println!("📡 Initializing Iroh network endpoint for node: {}", node_id);
        
        // Load the spatial model weight context
        let gpu_context = OewseGpuContext::load_spatial_model(spat_model_path)?;
        
        let capabilities = WorkerCapabilities {
            node_id: node_id.to_string(),
            models_loaded: vec![ModelInfo {
                name: "gemma-4-12b".to_string(),
                tiles: 4096,
                layers: 48,
            }],
            max_tiles: 4096,
            avg_latency_ms: 12,
            current_load: 0.0,
        };

        Ok(Self {
            node_id: node_id.to_string(),
            gpu_context: Arc::new(gpu_context),
            capabilities,
            gossip_topic: "sovereign-ai-mesh/tasks".to_string(),
        })
    }

    pub async fn run(&self) -> Result<(), Box<dyn std::error::Error>> {
        println!("🏛️ P2P Worker {} is active on gossip topic '{}'", self.node_id, self.gossip_topic);
        println!("📢 Broadcasting capabilities: {:?}", self.capabilities);
        
        // Simulating the P2P task execution loop
        // In full deployment, this subscribes to Iroh gossip and opens QUIC streams
        Ok(())
    }
}
