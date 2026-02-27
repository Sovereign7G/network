import type { FinancialIntelligenceState } from '../types/financial.types';

const mockFinancialState: FinancialIntelligenceState = {
    projections: [
        { timestamp: Date.now(), value: 1250000, confidence: 0.85, scenario: 'base' },
        { timestamp: Date.now() + 86400000, value: 1280000, confidence: 0.82, scenario: 'base' },
        { timestamp: Date.now() + 86400000 * 7, value: 1450000, confidence: 0.75, scenario: 'bull' },
        { timestamp: Date.now() + 86400000 * 30, value: 1850000, confidence: 0.68, scenario: 'bull' }
    ],
    yieldCurves: [
        { tenor: 30, rate: 5.2, spread: 0.3, liquidity: 0.95 },
        { tenor: 90, rate: 5.8, spread: 0.5, liquidity: 0.92 },
        { tenor: 180, rate: 6.4, spread: 0.7, liquidity: 0.88 },
        { tenor: 365, rate: 7.1, spread: 0.9, liquidity: 0.82 }
    ],
    marketMetrics: {
        totalLiquidity: 847000000,
        tradingVolume: 12400000,
        activeMarkets: 47,
        averageSpread: 0.18,
        volatilityIndex: 12.4
    },
    portfolioIntelligence: {
        allocation: [
            { asset: 'USDC', amount: 500000, percentage: 42 },
            { asset: 'AGE', amount: 300000, percentage: 25 },
            { asset: 'SYND', amount: 200000, percentage: 17 },
            { asset: 'BTC', amount: 100000, percentage: 8 },
            { asset: 'ETH', amount: 100000, percentage: 8 }
        ],
        riskScore: 34,
        projectedYield: 12.4,
        diversificationScore: 78,
        rebalanceRecommendations: [
            {
                from: 'USDC',
                to: 'AGE',
                amount: 50000,
                reason: 'Higher yield opportunity',
                urgency: 'medium'
            }
        ]
    },
    lastUpdated: Date.now()
};
