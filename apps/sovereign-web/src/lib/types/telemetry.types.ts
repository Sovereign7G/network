export type TelemetryMetric =
    | 'lcp' | 'fid' | 'cls' | 'ttfb' | 'fcp'
    | 'interaction' | 'navigation' | 'resource';

export interface TelemetryPoint {
    metric: TelemetryMetric;
    value: number;
    timestamp: number;
    tags?: Record<string, string>;
}

export interface TelemetryBatch {
    id: string;
    points: TelemetryPoint[];
    sessionId: string;
    timestamp: number;
    version: string;
}
