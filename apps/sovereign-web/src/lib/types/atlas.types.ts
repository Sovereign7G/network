export type Region = 'north-america' | 'europe' | 'asia' | 'south-america' | 'africa' | 'oceania';
export type PointStatus = 'active' | 'degraded' | 'syncing' | 'offline';

export interface AtlasPoint {
    id: string;
    label: string;
    region: Region;
    scarcity: number; // 0-100
    status: PointStatus;
    tps: number;
    coordinates: [number, number];
    health: number;
    peers: number;
    latency: number;
}

export interface AtlasState {
    points: AtlasPoint[];
    totalNodes: number;
    activeNodes: number;
    avgLatency: number;
    totalThroughput: number;
    lastUpdated: number;
}
