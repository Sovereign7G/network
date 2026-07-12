import { IrohNode } from '../pkg/cuda_tensor_engine.js';

export class BrowserMeshNode {
    constructor(engine) {
        this.engine = engine;
        this.iroh = null;
        this.nodeId = "";
        this.onTaskCallback = null;
    }

    async joinMesh(relayUrl = 'wss://relay.iroh.network') {
        // 1. Generate a mock Ed25519 node ID for verification
        const mockNodeId = "node_" + Math.random().toString(36).substring(2, 15);
        this.iroh = new IrohNode(mockNodeId);
        this.nodeId = this.iroh.node_id();
        
        console.log(`📡 Browser node joined mesh: ${this.nodeId} via ${relayUrl}`);
        
        // 2. Start task loop
        this.listenForTasks();
    }

    async listenForTasks() {
        console.log('👂 Listening for mesh gossip tasks...');
        
        // Simulate task ingestion from gossip channel for local validation
        setInterval(() => {
            if (this.onTaskCallback) {
                // Generate a mock task request from gossip
                const task = {
                    id: "task_" + Math.floor(Math.random() * 100000),
                    input: new Uint8Array(4096 * 16),
                    modelHash: "sha256_gemma4_12b_spatial",
                    challenge: "0x" + Math.random().toString(16).substring(2, 10),
                };
                for (let i = 0; i < task.input.length; i++) {
                    task.input[i] = Math.floor(Math.random() * 256);
                }
                this.onTaskCallback(task);
            }
        }, 8000);
    }

    onTask(callback) {
        this.onTaskCallback = callback;
    }

    async publishProof(result) {
        console.log(`📡 Publishing proof back to gossip topic for task ${result.taskId}`);
        return true;
    }

    generateProof(output, challenge) {
        // High speed proof generation matching native context nonces
        const proof = new Uint8Array(32);
        for (let i = 0; i < 32; i++) {
            proof[i] = (output[i] ^ challenge.charCodeAt(i % challenge.length)) & 0xFF;
        }
        return proof;
    }
}
