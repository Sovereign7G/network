import { browser } from "$app/environment";

class WorkerManager {
    private worker: Worker | null = null;
    private callbacks: Map<string, (data: any) => void> = new Map();

    constructor() {
        if (browser) {
            this.init();
        }
    }

    private async init() {
        // dynamic import worker
        const ComputationWorker = (await import("./computation.worker?worker")).default;
        this.worker = new ComputationWorker();
        this.worker.onmessage = (e: MessageEvent) => {
            const { id, payload, type, error } = e.data;
            if (this.callbacks.has(id)) {
                const cb = this.callbacks.get(id)!;
                if (type === "ERROR") {
                    console.error("Worker Error:", error);
                } else {
                    cb(payload);
                }
                this.callbacks.delete(id);
            }
        };
    }

    execute(type: string, payload: unknown): Promise<unknown> {
        if (!this.worker) {
            // Fallback for SSR or if worker not yet ready
            return Promise.reject("Worker not initialized");
        }

        const id = Math.random().toString(36).substring(7);
        return new Promise((resolve) => {
            this.callbacks.set(id, resolve);
            this.worker!.postMessage({ id, type, payload });
        });
    }
}

            // @ts-ignore
const workerManager = new WorkerManager();
