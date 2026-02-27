// 🧠 SOVEREIGN COMPUTATION WORKER
// Handles heavy arithmetic, sorting, and state transformations off-thread.

import type { WorkerMessage } from '../types/worker.types';

self.onmessage = (e: MessageEvent<WorkerMessage<any>>) => {
    const { type, payload, id } = e.data;

    try {
        switch (type) {
            case "STANDARDIZE_LAYOUT":
                const standardized = standardizeLayout(payload.columns);
                self.postMessage({ id, type, payload: standardized, timestamp: Date.now() });
                break;

            case "PROCESS_CAUSAL_LOG":
                const processed = processCausalLog(payload.events, payload.maxSize);
                self.postMessage({ id, type, payload: processed, timestamp: Date.now() });
                break;

            case "CALCULATE_METABOLIC_DRIFT":
                const drift = calculateMetabolicDrift(payload.state);
                self.postMessage({ id, type, payload: drift, timestamp: Date.now() });
                break;

            default:
                self.postMessage({ id, type: "ERROR", error: "Unknown task type", timestamp: Date.now() });
        }
    } catch (err: any) {
        self.postMessage({ id, type: "ERROR", error: err.message, timestamp: Date.now() });
    }
};

function standardizeLayout(columns: any[]) {
    // Flatten
    const allBlocks = columns.flatMap((c: any) => c.blocks);
    // Sort by type
    const sortedBlocks = [...allBlocks].sort((a, b) => a.type.localeCompare(b.type));

    const newCols = [
        { id: "col-alpha", blocks: [] as unknown[] },
        { id: "col-beta", blocks: [] as unknown[] },
        { id: "col-gamma", blocks: [] as unknown[] },
    ];

    sortedBlocks.forEach((block, idx) => {
        const col = newCols[idx % 3];
        if (col) col.blocks.push(block);
    });

    return newCols;
}

function processCausalLog(events: any[], maxSize: number) {
    // Sort and deduplicate if necessary, apply time-weighting
    return events
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(0, maxSize);
}

function calculateMetabolicDrift(state: any) {
    // Simulated heavy arithmetic for metabolic paths
    let result = { ...state };
    // Add logic here if needed
    return result;
}
