export interface FinancialProjection {
    timestamp: number;
    value: number;
    confidence: number;
    scenario: 'bull' | 'base' | 'bear';
}

export interface YieldCurve {
    tenor: number; // days
    rate: number;
    spread: number;
    liquidity: number;
}

export interface AssetAllocation {
    asset: string;
    amount: number;
    percentage: number;
}

export interface MarketMetrics {
    totalLiquidity: number;
    tradingVolume: number;
    activeMarkets: number;
    averageSpread: number;
    volatilityIndex: number;
}

export interface PortfolioIntelligence {
    allocation: AssetAllocation[];
    riskScore: number;
    projectedYield: number;
    diversificationScore: number;
    rebalanceRecommendations: RebalanceAction[];
}

export interface RebalanceAction {
    from: string;
    to: string;
    amount: number;
    reason: string;
    urgency: 'low' | 'medium' | 'high';
}

export interface FinancialIntelligenceState {
    projections: FinancialProjection[];
    yieldCurves: YieldCurve[];
    marketMetrics: MarketMetrics;
    portfolioIntelligence: PortfolioIntelligence;
    lastUpdated: number;
}
