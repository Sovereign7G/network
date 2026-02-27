import type {
    FinancialProjection,
    YieldCurve,
    PortfolioIntelligence,
    MarketMetrics
} from './financial.types';

export interface VaultAsset {
    id: string;
    asset: string;
    amount: number;
    valueUsd: number;
    yield: number;
}

export interface StableLP {
    pair: string;
    liquidity: number;
    volume24h: number;
}

export interface MetabolicState {
    vault: {
        activeStrategy: 'GROWTH_OPTIMIZED' | 'CAPITAL_PRESERVATION' | 'RESONANCE_STABILIZED';
        totalValueLockedUsd: number;
        assets: VaultAsset[];
        lastRebalance: number;
        integrityScore: number;
    };
    stablecoin: {
        symbol: string;
        name: string;
        parity: number;
        marketCap: number;
        collateralBacking: number;
        status: 'PEGGED' | 'DRIFTING' | 'DEPEGGED';
        stableLPs: StableLP[];
    };
    ledger: {
        totalMoralSupply: number;
        transfers: { id: string; from: string; to: string; amount: number; reason: string }[];
    };
    intelligence: {
        projections: FinancialProjection[];
        yieldCurves: YieldCurve[];
        marketMetrics: MarketMetrics;
        portfolioIntelligence: PortfolioIntelligence;
        lastUpdated: number;
    };
}

export interface MetabolicEngineConfig {
    tickRate: number; // ms
    sensitivity: number;
    thresholds: {
        coherenceMin: number;
        resonanceMin: number;
        alertThreshold: number;
    };
}

export interface MetabolicMetrics {
    heartRate: number; // 0-200 BPM equivalent
    coherence: number; // 0-1
    resonance: number; // 0-100
    systemLoad: number; // 0-100
    alertLevel: 'normal' | 'elevated' | 'high' | 'critical';
    lastTick: number;
}
