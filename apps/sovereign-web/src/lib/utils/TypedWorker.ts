import type { WorkerMessage, WorkerMessageType } from '$lib/types';

export class TypedWorker {
    private worker: Worker;
    private handlers = new Map<string, (data: any) => void>();

    constructor(workerScript: string) {
        this.worker = new Worker(workerScript);
        this.worker.onmessage = this.handleMessage.bind(this);
    }

    private handleMessage(event: MessageEvent<WorkerMessage>) {
        const message = event.data;
        const handler = this.handlers.get(message.id);

        if (handler) {
            handler(message);
            this.handlers.delete(message.id);
        }
    }

    public postMessage<T = unknown, R = unknown>(
        type: WorkerMessageType,
        payload: T,
        transfer?: Transferable[]
    ): Promise<R> {
        const id = Math.random().toString(36).substring(7).toUpperCase();
        const message: WorkerMessage<T> = {
            id,
            type,
            payload,
            timestamp: Date.now()
        };

        return new Promise((resolve, reject) => {
            this.handlers.set(id, (response: WorkerMessage<any>) => {
                if (response.type === 'ERROR' || response.error) {
                    reject(new Error(response.error || 'Unknown worker error'));
                } else {
                    resolve(response.payload);
                }
            });

            if (transfer) {
                this.worker.postMessage(message, transfer);
            } else {
                this.worker.postMessage(message);
            }
        });
    }

    public terminate(): void {
        this.worker.terminate();
    }
}
