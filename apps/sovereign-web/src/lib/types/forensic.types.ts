export interface YieldPoint {
    timestamp: number;
    value: number;
    source: 'protocol' | 'market' | 'oracle';
    confidence: number;
}

export interface YieldAnomaly {
    timestamp: number;
    expected: number;
    actual: number;
    deviation: number;
    severity: 'low' | 'medium' | 'high' | 'critical';
    detectedAt: number;
}

export interface YieldForecast {
    timestamp: number;
    predicted: number;
    lowerBound: number;
    upperBound: number;
    confidence: number;
}

export interface ForensicYieldComponent {
    name: string;
    contribution: number;
    source: string;
    color: string;
}

export interface ForensicYieldState {
    historicalYields: YieldPoint[];
    currentYield: number;
    projectedYield: number;
    volatility: number;
    sharpeRatio: number;
    maxDrawdown: number;
    recoveryTime: number; // days
    anomalies: YieldAnomaly[];
    total: number;
    status: 'VERIFIED' | 'AUDITING';
    components: ForensicYieldComponent[];
}
