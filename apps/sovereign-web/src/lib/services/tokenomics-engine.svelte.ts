// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN TOKENOMICS ENGINE (Ousterhout Deep Module)
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  manifold-state initial values
// [OUT]: tokenomicsEngine (singleton), TokenomicsSummary, SupplyProjection
// [POS]: Deep module encapsulating ALL tokenomics logic — supply, dividends, ARI,
//        reputation, market cap, and projection. Consumers only see the summary
//        and two action methods. Implementation complexity is fully hidden.
// ═══════════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════════

interface TokenomicsSummary {
    totalSupply: number;
    circulatingSupply: number;
    circulatingRatio: number;
    dailyDividend: number;
    ariMultiplier: number;
    marketCapUsd: number;
    reputationIndex: number;
    pricePerAge: number;
    fdvUsd: number;
    inflationRate: number;
}

interface SupplyProjection {
    months: number;
    projectedCirculating: number;
    projectedMarketCap: number;
    projectedDividend: number;
    projectedAri: number;
    confidence: number;
}

type TokenomicsHealth = 'HEALTHY' | 'WARNING' | 'CRITICAL';

// ─── CONSTANTS ──────────────────────────────────────────────────────────────

const ARI_DECAY_RATE = 0.001;
const ARI_BOOST_RATE = 0.005;
const REPUTATION_FLOOR = 100;
const REPUTATION_CEILING = 1000;
const INFLATION_TARGET = 0.02;

class TokenomicsEngine {
    private _totalSupply = $state(1_000_000_000);
    private _circulatingSupply = $state(420_000_000);
    private _dailyDividend = $state(25.5);
    private _ariMultiplier = $state(1.12);
    private _marketCapUsd = $state(1_420_000_000);
    private _reputationIndex = $state(842);
    private _epochCount = $state(0);
    private _dividendHistory: number[] = [];
    private _ariHistory: number[] = [];


    get summary(): TokenomicsSummary {
        const pricePerAge = this._circulatingSupply > 0 ? this._marketCapUsd / this._circulatingSupply : 0;
        return {
            totalSupply: this._totalSupply,
            circulatingSupply: this._circulatingSupply,
            circulatingRatio: this._circulatingSupply / this._totalSupply,
            dailyDividend: this._dailyDividend,
            ariMultiplier: this._ariMultiplier,
            marketCapUsd: this._marketCapUsd,
            reputationIndex: this._reputationIndex,
            pricePerAge,
            fdvUsd: pricePerAge * this._totalSupply,
            inflationRate: this._computeInflationRate(),
        };
    }

    get health(): TokenomicsHealth {
        const inflation = this._computeInflationRate();
        const ratio = this._circulatingSupply / this._totalSupply;
        if (inflation > 0.05 || ratio > 0.8 || this._reputationIndex < 300) return 'CRITICAL';
        if (inflation > 0.03 || ratio > 0.6 || this._reputationIndex < 500) return 'WARNING';
        return 'HEALTHY';
    }

    get epoch(): number { return this._epochCount; }

    get state() {
        return {
            ageTotalSupply: this._totalSupply,
            ageCirculating: this._circulatingSupply,
            uctDailyDividend: this._dailyDividend,
            ariMultiplier: this._ariMultiplier,
            marketCapUsd: this._marketCapUsd,
            reputationIndex: this._reputationIndex,
        };
    }

    recordDividendEpoch(amount: number): void {
        this._dailyDividend = amount;
        this._dividendHistory.push(amount);
        if (this._dividendHistory.length > 365) this._dividendHistory.shift();
        const avgDividend = this._dividendHistory.reduce((a, b) => a + b, 0) / this._dividendHistory.length;
        this._ariMultiplier = amount > avgDividend
            ? Math.min(2.0, this._ariMultiplier * (1 + ARI_BOOST_RATE))
            : Math.max(0.5, this._ariMultiplier * (1 - ARI_DECAY_RATE));
        this._ariHistory.push(this._ariMultiplier);
        if (this._ariHistory.length > 365) this._ariHistory.shift();
        this._reputationIndex = Math.min(REPUTATION_CEILING, Math.max(REPUTATION_FLOOR, Math.round(this._ariMultiplier * 750)));
        this._epochCount++;
    }


    projectSupply(months: number): SupplyProjection {
        const monthlyInflation = this._computeInflationRate() / 12;
        const projectedCirculating = this._circulatingSupply * Math.pow(1 + monthlyInflation, months);
        const first = this._ariHistory[0];
        const last = this._ariHistory[this._ariHistory.length - 1];
        const ariTrend = (this._ariHistory.length >= 2 && first !== undefined && last !== undefined)
            ? (last - first) / this._ariHistory.length
            : 0;

        const projectedAri = Math.max(0.5, Math.min(2.0, this._ariMultiplier + ariTrend * months * 30));
        return {
            months,
            projectedCirculating: Math.round(projectedCirculating),
            projectedMarketCap: Math.round(projectedCirculating * (this._marketCapUsd / this._circulatingSupply) * projectedAri),
            projectedDividend: this._dailyDividend * projectedAri,
            projectedAri,
            confidence: Math.max(0.3, 1.0 - months * 0.05),
        };
    }

    updateMarketCap(newCap: number): void { this._marketCapUsd = newCap; }
    adjustARI(multiplier: number): void { this._ariMultiplier = Math.max(0.5, Math.min(2.0, multiplier)); }
    recordDividend(amount: number): void { this._dailyDividend = amount; }

    private _computeInflationRate(): number {
        return this._totalSupply === 0 ? 0 : INFLATION_TARGET * (1 - (this._circulatingSupply / this._totalSupply)) * this._ariMultiplier;
    }

    /**
     * Called by SimulationEngine on each 3s tick.
     * Replaces the orphan setInterval — all timed state flows through the heartbeat.
     * ARI decay is scaled to maintain correct economic rate.
     */
    tick(): void {
        this._ariMultiplier = Math.max(0.5, this._ariMultiplier * (1 - ARI_DECAY_RATE / 24));
        this._marketCapUsd *= (1 + (Math.random() - 0.48) * 0.001);
    }
}

const engineInstance = new TokenomicsEngine();

export const tokenomicsEngine = engineInstance;
export const tokenomicsStore = tokenomicsEngine;
