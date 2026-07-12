use candle_core::{Device, Tensor};
use std::time::Duration;
use tonic::transport::Server;
use std::io::Write;

mod oewse_driver;
mod oewse_orchestrator;
mod oewse_worker;
mod zerosync_verifier;

use oewse_orchestrator::{
    sovereign_mesh::sovereign_mesh_orchestrator_server::SovereignMeshOrchestratorServer,
    PoolRegistry, PouwOrchestrator,
};
use oewse_orchestrator::sovereign_mesh::WorkAllocation;
use oewse_worker::MeshWorker;

fn generate_mock_spatial_model(path: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::create(path)?;
    file.write_all(b"SPAT")?; // Magic
    file.write_all(&1u32.to_le_bytes())?; // Version
    file.write_all(&40u32.to_le_bytes())?; // num_layers
    file.write_all(&256u32.to_le_bytes())?; // threads_per_block
    let weights_len = 40 * 256;
    file.write_all(&(weights_len as u32).to_le_bytes())?; // weights_len
    
    let weights_pos = vec![0u32; weights_len];
    let weights_neg = vec![0u32; weights_len];
    
    for val in weights_pos {
        file.write_all(&val.to_le_bytes())?;
    }
    for val in weights_neg {
        file.write_all(&val.to_le_bytes())?;
    }
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Generate and test loading spatial model
    let spatial_model_path = "mock_model.spatial";
    println!("📦 Creating mock spatial model at {}...", spatial_model_path);
    generate_mock_spatial_model(spatial_model_path)?;
    
    println!("📂 Verifying spatial model loader FFI context...");
    match oewse_driver::OewseGpuContext::load_spatial_model(spatial_model_path) {
        Ok(_ctx) => println!("✅ Spatial model successfully loaded and uploaded to FFI context!"),
        Err(e) => eprintln!("❌ Failed to load spatial model: {}", e),
    }

    println!("⚡ Initializing GPU/CUDA Accelerated Substrate...");
    
    // Check if CUDA device is available
    let device = if candle_core::utils::cuda_is_available() {
        println!("🟢 NVIDIA CUDA Substrate Detected. Allocating tensors on GPU...");
        Device::new_cuda(0)?
    } else {
        println!("⚠️ CUDA hardware absent. Falling back to high-fidelity CPU backend...");
        Device::Cpu
    };

    // Allocate matrices
    let x = Tensor::new(&[[1f32, 2.], [3., 4.]], &device)?;
    let w = Tensor::new(&[[5f32, 6.], [7., 8.]], &device)?;
    
    // Execute matrix multiplication (GEMM)
    println!("⚙️ Executing high-performance tensor GEMM multiplication...");
    let y = x.matmul(&w)?;
    println!("✅ Tensor calculation complete. Result Matrix:\n{}", y);

    println!("\n⛏️ Initiating gRPC Multi-Node Pool Pipeline Integration (v2)...");
    
    // 1. Launch Coordinator Server (Stratum Coordinator) in the background
    let registry = PoolRegistry::default();
    let registry_clone = registry.clone();
    let addr = "[::1]:50051".parse().unwrap();
    let orchestrator = PouwOrchestrator::new(registry.clone());

    tokio::spawn(async move {
        println!("📡 Starting Pool Coordinator v2 gRPC Server on {}...", addr);
        Server::builder()
            .add_service(SovereignMeshOrchestratorServer::new(orchestrator))
            .serve(addr)
            .await
            .unwrap();
    });

    // Wait a brief moment for the server socket to open
    tokio::time::sleep(Duration::from_millis(500)).await;

    // 2. Connect Worker Client (GPU Worker Node)
    let channel = tonic::transport::Channel::from_static("http://[::1]:50051")
        .connect()
        .await?;

    let weights_pos = vec![0u32; 40 * 256];
    let weights_neg = vec![0u32; 40 * 256];
    let worker = MeshWorker::new(channel, weights_pos, weights_neg);

    tokio::spawn(async move {
        if let Err(e) = worker.start_execution_loop(32).await {
            eprintln!("❌ Worker execution loop error: {}", e);
        }
    });

    // Wait for the worker to connect and register
    tokio::time::sleep(Duration::from_millis(500)).await;

    // 3. Simulate incoming ASIC Stochastic Activations passing through Stratum pre-selection
    println!("\n📥 Simulating ASIC Stochastic Activations passing Stratum filter...");
    let mut packed_activations = vec![0u8; 32];
    for i in 0..32 {
        packed_activations[i] = 0b00_01_10_11; // Maps to [-1, 0, 0, +1] repeating pattern
    }

    // Set up mock Bitcoin Block Header (80 bytes) and a corresponding ZeroSync chain proof
    let block_header = vec![0x02u8; 80];
    
    // Create a mock ZeroSync chain proof where the first 4 bytes match the header hash bytes
    let mut zerosync_proof = vec![0u8; 32];
    // Hash mock: block_header has 80 bytes of 0x02. Simple hash = 80 * 2 = 160 (0xA0) at indexes.
    // 160 ^ 0x00 = 160.
    zerosync_proof[0] = 0xA0; 
    
    let work = WorkAllocation {
        job_id: "bitcoin-block-840000".to_string(),
        nonce: 123456,
        zerosync_chain_proof: zerosync_proof,
        bitcoin_block_header: block_header,
        packed_ternary_activations: packed_activations,
        target_difficulty: 0x00FFFFFF,
    };

    // Distribute work to registered workers
    let dispatched = registry_clone.distribute_work(work).await;
    if dispatched {
        println!("✅ Work successfully verified via ZeroSync and dispatched through pool pipeline.");
    } else {
        println!("❌ No active workers found or ZeroSync verification failed.");
    }

    // Allow time for execution pass and async result return
    tokio::time::sleep(Duration::from_secs(1)).await;
    println!("\n🏁 Multi-Node Pool Pipeline (v2) Integration Verification Completed!");

    Ok(())
}
