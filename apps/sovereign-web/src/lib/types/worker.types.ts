export type WorkerMessageType =
    | 'compute:start'
    | 'compute:progress'
    | 'compute:complete'
    | 'compute:error'
    | 'STANDARDIZE_LAYOUT'
    | 'PROCESS_CAUSAL_LOG'
    | 'CALCULATE_METABOLIC_DRIFT'
    | 'ERROR';

export interface WorkerMessage<T = unknown> {
    id: string;
    type: WorkerMessageType;
    payload: T;
    timestamp: number;
    error?: string;
}

export interface ComputeStartPayload {
    taskId: string;
    data: unknown;
    priority: 'low' | 'medium' | 'high';
}

export interface ComputeProgressPayload {
    taskId: string;
    progress: number;
    eta?: number;
}

export interface ComputeCompletePayload<T = unknown> {
    taskId: string;
    result: T;
    duration: number;
}

export interface ComputeErrorPayload {
    taskId: string;
    error: string;
    stack?: string;
}
