// ═══════════════════════════════════════════════════════════════════════════════
// 🧠 COMPUTE ENGINE (Deep Module)
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  workload-queue, gpu-telemetry
// [OUT]: submitJob(), cancelJob(), market-metrics
// [POS]: Orchestrates the Sovereign Compute Market (DePIN).
// ═══════════════════════════════════════════════════════════════════════════════


interface ComputeJob {
    id: string;
    type: 'ZK_PROVING' | 'LLM_TRAINING' | 'MARCH_31_DRILL';
    tflops: number;
    status: 'QUEUED' | 'PROCESSING' | 'COMPLETED';
    reward: number;
}

interface ComputeState {
    totalTflops: number;
    activeGpus: number;
    pricePerTflopAge: number;
    demandIndex: number;
    workloads: ComputeJob[];
}

class ComputeEngine {
    private _state = $state<ComputeState>({
        totalTflops: 14500,
        activeGpus: 4200,
        pricePerTflopAge: 0.042,
        demandIndex: 0.78,
        workloads: [
            { id: 'job-zk-nagano', type: 'ZK_PROVING', tflops: 120, status: 'PROCESSING', reward: 50 },
            { id: 'job-march-31', type: 'MARCH_31_DRILL', tflops: 500, status: 'QUEUED', reward: 210 }
        ]
    });

    get state() { return this._state; }

    submitJob(type: ComputeJob['type'], tflops: number): string {
        const id = `job-${Math.random().toString(36).slice(2, 7)}`;
        const job: ComputeJob = {
            id,
            type,
            tflops,
            status: 'QUEUED',
            reward: tflops * this._state.pricePerTflopAge
        };
        this._state.workloads.push(job);
        return id;
    }

    /**
     * Called by SimulationEngine every 5th tick (~15s).
     * Replaces orphan setInterval — job lifecycle simulation.
     */
    tick() {
        const processing = this._state.workloads.find(j => j.status === 'PROCESSING');
        if (processing) {
            processing.status = 'COMPLETED';
        }
        const queued = this._state.workloads.find(j => j.status === 'QUEUED');
        if (queued) {
            queued.status = 'PROCESSING';
        }
    }
}

const engineInstance = new ComputeEngine();
export const computeEngine = engineInstance;
