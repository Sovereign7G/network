// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN TRADING ENGINE
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]: manifold state, agent-gateway
// [OUT]: tradingEngine, PerpetualOrder, PredictionMarket, SovereignCard
// [POS]: Implements 6 core sovereign financial primitives:
//        1. On-chain orderbook (CLOB) perpetual trading
//        2. Prediction markets (Outcome Trading)
//        3. Crypto-linked Sovereign Card
//        4. Fiat on/off ramp infrastructure
//        5. AI agentic commerce (agent-managed portfolios)
//        6. Native stablecoin yield (RES → Treasury-backed)
// Protocol: When updating me, sync this header + parent folder's .folder.md
// ═══════════════════════════════════════════════════════════════════════════════


// ─── TYPES: PERPETUAL TRADING (On-Chain CLOB) ────────────────────────────────

type OrderSide = 'LONG' | 'SHORT';
type OrderType = 'MARKET' | 'LIMIT' | 'STOP_LOSS' | 'TAKE_PROFIT';
type OrderStatus = 'OPEN' | 'FILLED' | 'PARTIAL' | 'CANCELLED' | 'LIQUIDATED';

interface PerpetualMarket {
    id: string;
    symbol: string;
    baseAsset: string;
    quoteAsset: string;
    markPrice: number;
    indexPrice: number;
    fundingRate: number;         // 8h funding rate
    volume24h: number;
    openInterest: number;
    maxLeverage: number;
    tickSize: number;
    minOrderSize: number;
    status: 'ACTIVE' | 'SETTLING' | 'HALTED';
}

interface PerpetualOrder {
    orderId: string;
    marketId: string;
    side: OrderSide;
    type: OrderType;
    size: number;                // In base asset
    price: number;               // Limit price (0 for market)
    leverage: number;
    margin: number;              // Required collateral
    status: OrderStatus;
    filledSize: number;
    avgFillPrice: number;
    pnl: number;                 // Unrealized P&L
    liquidationPrice: number;
    createdAt: number;
    updatedAt: number;
    reducedOnly: boolean;
    postOnly: boolean;
}

interface OrderBookLevel {
    price: number;
    size: number;
    total: number;               // Cumulative
    count: number;               // Number of orders at this level
}

interface OrderBook {
    bids: OrderBookLevel[];
    asks: OrderBookLevel[];
    spread: number;
    spreadPct: number;
    lastUpdate: number;
}

// ─── TYPES: PREDICTION MARKETS (Outcome Trading) ────────────────────────────

type OutcomeType = 'BINARY' | 'MULTI' | 'SCALAR';
type MarketResolution = 'YES' | 'NO' | 'INVALID' | 'PENDING';

interface PredictionMarket {
    marketId: string;
    question: string;
    description: string;
    category: 'CRYPTO' | 'POLITICS' | 'SPORTS' | 'TECH' | 'MACRO' | 'SOVEREIGN';
    type: OutcomeType;
    outcomes: PredictionOutcome[];
    totalVolume: number;
    totalLiquidity: number;
    createdAt: number;
    resolvesAt: number;
    resolution: MarketResolution;
    collateralAsset: string;     // Usually RES (stablecoin)
    isFullyCollateralized: boolean;
    creatorId: string;
    featured: boolean;
}

interface PredictionOutcome {
    outcomeId: string;
    label: string;
    probability: number;         // 0-1
    price: number;               // Current price (0-1)
    shares: number;              // Total shares outstanding
    volume: number;
}

interface PredictionPosition {
    positionId: string;
    marketId: string;
    outcomeId: string;
    shares: number;
    avgPrice: number;
    currentValue: number;
    pnl: number;
    createdAt: number;
}

// ─── TYPES: SOVEREIGN CARD (Crypto-linked Payment Card) ─────────────────────

type CardStatus = 'ACTIVE' | 'FROZEN' | 'PENDING_KYC' | 'EXPIRED';
type CardTier = 'STANDARD' | 'GOLD' | 'SOVEREIGN' | 'INSTITUTIONAL';

interface SovereignCard {
    cardId: string;
    maskedNumber: string;        // **** **** **** 4242
    tier: CardTier;
    status: CardStatus;
    monthlyLimit: number;
    monthlySpent: number;
    dailyLimit: number;
    dailySpent: number;
    cashbackRate: number;        // In AGE tokens
    fundingAsset: string;        // Which crypto funds the card
    autoConvert: boolean;        // Auto-convert crypto to fiat at POS
    transactions: CardTransaction[];
    issuedAt: number;
    expiresAt: number;
}

interface CardTransaction {
    txId: string;
    merchant: string;
    merchantCategory: string;
    amount: number;              // In fiat (USD)
    cryptoAmount: number;        // In funding asset
    exchangeRate: number;
    cashbackEarned: number;
    timestamp: number;
    status: 'COMPLETED' | 'PENDING' | 'DECLINED';
    country: string;
}

// ─── TYPES: FIAT ON/OFF RAMP ────────────────────────────────────────────────

type RampDirection = 'ON_RAMP' | 'OFF_RAMP';
type PaymentMethod = 'BANK_TRANSFER' | 'VISA' | 'MASTERCARD' | 'APPLE_PAY' | 'GOOGLE_PAY' | 'SEPA' | 'PIX';

interface RampQuote {
    quoteId: string;
    direction: RampDirection;
    fiatAmount: number;
    fiatCurrency: string;
    cryptoAmount: number;
    cryptoAsset: string;
    exchangeRate: number;
    fee: number;
    feePct: number;
    paymentMethod: PaymentMethod;
    expiresAt: number;
    provider: string;
}

interface RampTransaction {
    txId: string;
    direction: RampDirection;
    fiatAmount: number;
    fiatCurrency: string;
    cryptoAmount: number;
    cryptoAsset: string;
    paymentMethod: PaymentMethod;
    status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
    createdAt: number;
    completedAt: number | null;
}

// ─── TYPES: AI AGENTIC COMMERCE ──────────────────────────────────────────────

type AgentStrategy = 'MOMENTUM' | 'MEAN_REVERSION' | 'GRID' | 'DCA' | 'PREDICTION_ALPHA' | 'SOVEREIGN_YIELD';

interface TradingAgent {
    agentId: string;
    name: string;
    strategy: AgentStrategy;
    status: 'ACTIVE' | 'PAUSED' | 'LEARNING' | 'STOPPED';
    portfolio: AgentPortfolio;
    performance: AgentPerformance;
    riskParameters: AgentRiskParams;
    lastAction: string;
    lastActionTime: number;
    createdAt: number;
}

interface AgentPortfolio {
    totalValue: number;
    allocations: { asset: string; amount: number; weight: number; }[];
    activePositions: number;
    openOrders: number;
}

interface AgentPerformance {
    totalPnl: number;
    totalPnlPct: number;
    winRate: number;
    tradesExecuted: number;
    sharpeRatio: number;
    maxDrawdown: number;
    averageReturn: number;
}

interface AgentRiskParams {
    maxPositionSize: number;     // Max % of portfolio per position
    maxLeverage: number;
    stopLossPct: number;
    takeProfitPct: number;
    maxDailyLoss: number;        // USD
    cooldownAfterLoss: number;   // Seconds
}

// ─── TYPES: STABLECOIN YIELD (Treasury-Backed) ──────────────────────────────

interface StablecoinYield {
    currentApy: number;
    source: 'TREASURY_BILLS' | 'LIQUIDITY_FEES' | 'VALIDATOR_REWARDS';
    totalReserves: number;
    treasuryBacking: number;     // % backed by US Treasury / equivalent
    proofOfReserves: {
        lastAudit: number;
        auditor: string;
        verified: boolean;
        reserveRatio: number;
    };
    buybackAllocation: number;   // % of yield used for AGE buyback
}


// ═══════════════════════════════════════════════════════════════════════════════
// THE ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

function uuid(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
}

class SovereignTradingEngine {
    // ── PERPETUAL MARKETS ──
    markets = $state<PerpetualMarket[]>([
        {
            id: 'AGE-USD-PERP', symbol: 'AGE-USD', baseAsset: 'AGE', quoteAsset: 'USD',
            markPrice: 1.42, indexPrice: 1.41, fundingRate: 0.0012,
            volume24h: 84_500_000, openInterest: 42_000_000, maxLeverage: 50,
            tickSize: 0.001, minOrderSize: 1, status: 'ACTIVE'
        },
        {
            id: 'BTC-USD-PERP', symbol: 'BTC-USD', baseAsset: 'BTC', quoteAsset: 'USD',
            markPrice: 94_500, indexPrice: 94_480, fundingRate: 0.0008,
            volume24h: 2_100_000_000, openInterest: 850_000_000, maxLeverage: 100,
            tickSize: 0.1, minOrderSize: 0.001, status: 'ACTIVE'
        },
        {
            id: 'ETH-USD-PERP', symbol: 'ETH-USD', baseAsset: 'ETH', quoteAsset: 'USD',
            markPrice: 3_200, indexPrice: 3_198, fundingRate: 0.0005,
            volume24h: 1_400_000_000, openInterest: 520_000_000, maxLeverage: 100,
            tickSize: 0.01, minOrderSize: 0.01, status: 'ACTIVE'
        },
        {
            id: 'SOL-USD-PERP', symbol: 'SOL-USD', baseAsset: 'SOL', quoteAsset: 'USD',
            markPrice: 185.40, indexPrice: 185.20, fundingRate: 0.0015,
            volume24h: 680_000_000, openInterest: 240_000_000, maxLeverage: 50,
            tickSize: 0.01, minOrderSize: 0.1, status: 'ACTIVE'
        },
    ]);

    orderBook = $state<OrderBook>({
        bids: [], asks: [], spread: 0, spreadPct: 0, lastUpdate: Date.now()
    });

    activeOrders = $state<PerpetualOrder[]>([]);
    orderHistory = $state<PerpetualOrder[]>([]);

    // ── PREDICTION MARKETS ──
    predictionMarkets = $state<PredictionMarket[]>([
        {
            marketId: 'PM-AGE-10', question: 'Will $AGE exceed $10 by Q4 2026?',
            description: 'Resolves YES if AGE token price closes above $10 on Dec 31 2026.',
            category: 'CRYPTO', type: 'BINARY',
            outcomes: [
                { outcomeId: 'yes', label: 'Yes', probability: 0.34, price: 0.34, shares: 420_000, volume: 1_200_000 },
                { outcomeId: 'no', label: 'No', probability: 0.66, price: 0.66, shares: 820_000, volume: 2_400_000 },
            ],
            totalVolume: 3_600_000, totalLiquidity: 1_240_000,
            createdAt: Date.now() - 86400000 * 30, resolvesAt: Date.now() + 86400000 * 310,
            resolution: 'PENDING', collateralAsset: 'RES',
            isFullyCollateralized: true, creatorId: 'sovereign-dao', featured: true
        },
        {
            marketId: 'PM-BTC-150K', question: 'Will Bitcoin reach $150K in 2026?',
            description: 'Resolves YES if BTC trades above $150,000 on any major exchange in 2026.',
            category: 'CRYPTO', type: 'BINARY',
            outcomes: [
                { outcomeId: 'yes', label: 'Yes', probability: 0.52, price: 0.52, shares: 1_800_000, volume: 8_400_000 },
                { outcomeId: 'no', label: 'No', probability: 0.48, price: 0.48, shares: 1_650_000, volume: 7_700_000 },
            ],
            totalVolume: 16_100_000, totalLiquidity: 3_450_000,
            createdAt: Date.now() - 86400000 * 45, resolvesAt: Date.now() + 86400000 * 310,
            resolution: 'PENDING', collateralAsset: 'RES',
            isFullyCollateralized: true, creatorId: 'sovereign-dao', featured: true
        },
        {
            marketId: 'PM-JAPAN-CBDC', question: 'Will Japan launch a retail CBDC by Mar 2027?',
            description: 'Resolves YES if the Bank of Japan officially launches a public-accessible digital yen.',
            category: 'MACRO', type: 'BINARY',
            outcomes: [
                { outcomeId: 'yes', label: 'Yes', probability: 0.28, price: 0.28, shares: 340_000, volume: 890_000 },
                { outcomeId: 'no', label: 'No', probability: 0.72, price: 0.72, shares: 880_000, volume: 2_300_000 },
            ],
            totalVolume: 3_190_000, totalLiquidity: 1_220_000,
            createdAt: Date.now() - 86400000 * 10, resolvesAt: Date.now() + 86400000 * 400,
            resolution: 'PENDING', collateralAsset: 'RES',
            isFullyCollateralized: true, creatorId: 'sovereign-research', featured: false
        },
        {
            marketId: 'PM-SOV-MESH', question: 'Will Sovereign Mesh reach 1000 nodes by June 2026?',
            description: 'Resolves YES if the AGE Protocol Sovereign Mesh validator count exceeds 1000.',
            category: 'SOVEREIGN', type: 'BINARY',
            outcomes: [
                { outcomeId: 'yes', label: 'Yes', probability: 0.61, price: 0.61, shares: 520_000, volume: 1_450_000 },
                { outcomeId: 'no', label: 'No', probability: 0.39, price: 0.39, shares: 335_000, volume: 920_000 },
            ],
            totalVolume: 2_370_000, totalLiquidity: 855_000,
            createdAt: Date.now() - 86400000 * 5, resolvesAt: Date.now() + 86400000 * 120,
            resolution: 'PENDING', collateralAsset: 'RES',
            isFullyCollateralized: true, creatorId: 'governance-branch-v1.3', featured: true
        },
    ]);

    predictionPositions = $state<PredictionPosition[]>([]);

    // ── SOVEREIGN CARD ──
    sovereignCard = $state<SovereignCard>({
        cardId: 'SC-0xAGE-4242',
        maskedNumber: '**** **** **** 4242',
        tier: 'SOVEREIGN',
        status: 'ACTIVE',
        monthlyLimit: 50_000,
        monthlySpent: 12_340,
        dailyLimit: 5_000,
        dailySpent: 842,
        cashbackRate: 0.03,  // 3% in AGE
        fundingAsset: 'RES',
        autoConvert: true,
        transactions: [
            { txId: 'CTX-001', merchant: 'Shinkansen JR East', merchantCategory: 'Transport', amount: 142.50, cryptoAmount: 142.50, exchangeRate: 1.0, cashbackEarned: 4.28, timestamp: Date.now() - 3600000, status: 'COMPLETED', country: 'JP' },
            { txId: 'CTX-002', merchant: 'Lawson Nagano', merchantCategory: 'Convenience', amount: 28.40, cryptoAmount: 28.40, exchangeRate: 1.0, cashbackEarned: 0.85, timestamp: Date.now() - 7200000, status: 'COMPLETED', country: 'JP' },
            { txId: 'CTX-003', merchant: 'AWS Cloud', merchantCategory: 'Technology', amount: 1_249.00, cryptoAmount: 1_249.00, exchangeRate: 1.0, cashbackEarned: 37.47, timestamp: Date.now() - 86400000, status: 'COMPLETED', country: 'US' },
            { txId: 'CTX-004', merchant: 'Migros Zurich', merchantCategory: 'Grocery', amount: 86.20, cryptoAmount: 86.20, exchangeRate: 1.0, cashbackEarned: 2.59, timestamp: Date.now() - 172800000, status: 'COMPLETED', country: 'CH' },
        ],
        issuedAt: Date.now() - 86400000 * 90,
        expiresAt: Date.now() + 86400000 * 730,
    });

    // ── FIAT RAMP ──
    rampHistory = $state<RampTransaction[]>([]);
    availablePaymentMethods = $state<PaymentMethod[]>(['BANK_TRANSFER', 'VISA', 'MASTERCARD', 'APPLE_PAY', 'GOOGLE_PAY']);

    // ── AI TRADING AGENTS ──
    tradingAgents = $state<TradingAgent[]>([
        {
            agentId: 'agent-momentum-01', name: 'Sovereign Momentum Alpha',
            strategy: 'MOMENTUM', status: 'ACTIVE',
            portfolio: { totalValue: 42_500, allocations: [{ asset: 'AGE', amount: 15000, weight: 0.35 }, { asset: 'BTC', amount: 0.15, weight: 0.40 }, { asset: 'ETH', amount: 2.5, weight: 0.25 }], activePositions: 3, openOrders: 2 },
            performance: { totalPnl: 8_420, totalPnlPct: 24.7, winRate: 0.68, tradesExecuted: 142, sharpeRatio: 2.1, maxDrawdown: -8.2, averageReturn: 1.2 },
            riskParameters: { maxPositionSize: 0.25, maxLeverage: 5, stopLossPct: 3, takeProfitPct: 8, maxDailyLoss: 500, cooldownAfterLoss: 3600 },
            lastAction: 'Opened 2x LONG AGE-USD @ $1.41', lastActionTime: Date.now() - 1800000, createdAt: Date.now() - 86400000 * 30
        },
        {
            agentId: 'agent-prediction-02', name: 'Oracle Prediction Scanner',
            strategy: 'PREDICTION_ALPHA', status: 'ACTIVE',
            portfolio: { totalValue: 18_200, allocations: [{ asset: 'RES', amount: 15000, weight: 0.82 }, { asset: 'AGE', amount: 2560, weight: 0.18 }], activePositions: 5, openOrders: 0 },
            performance: { totalPnl: 3_840, totalPnlPct: 26.8, winRate: 0.72, tradesExecuted: 38, sharpeRatio: 1.8, maxDrawdown: -4.5, averageReturn: 3.1 },
            riskParameters: { maxPositionSize: 0.15, maxLeverage: 1, stopLossPct: 10, takeProfitPct: 50, maxDailyLoss: 200, cooldownAfterLoss: 7200 },
            lastAction: 'Bought 1200 YES shares on PM-AGE-10 @ $0.33', lastActionTime: Date.now() - 7200000, createdAt: Date.now() - 86400000 * 15
        },
        {
            agentId: 'agent-yield-03', name: 'Sovereign Yield Optimizer',
            strategy: 'SOVEREIGN_YIELD', status: 'ACTIVE',
            portfolio: { totalValue: 125_000, allocations: [{ asset: 'RES', amount: 100000, weight: 0.80 }, { asset: 'AGE', amount: 17850, weight: 0.18 }, { asset: 'ETH', amount: 0.625, weight: 0.02 }], activePositions: 4, openOrders: 1 },
            performance: { totalPnl: 12_400, totalPnlPct: 11.0, winRate: 0.85, tradesExecuted: 28, sharpeRatio: 3.2, maxDrawdown: -2.1, averageReturn: 0.9 },
            riskParameters: { maxPositionSize: 0.30, maxLeverage: 1, stopLossPct: 2, takeProfitPct: 5, maxDailyLoss: 1000, cooldownAfterLoss: 1800 },
            lastAction: 'Rebalanced RES/AGE LP position (+0.3% yield)', lastActionTime: Date.now() - 900000, createdAt: Date.now() - 86400000 * 60
        },
    ]);

    // ── STABLECOIN YIELD ──
    stablecoinYield = $state<StablecoinYield>({
        currentApy: 4.8,
        source: 'TREASURY_BILLS',
        totalReserves: 25_000_000,
        treasuryBacking: 0.92,
        proofOfReserves: {
            lastAudit: Date.now() - 86400000 * 7,
            auditor: 'Sovereign Attestation Service',
            verified: true,
            reserveRatio: 1.65,
        },
        buybackAllocation: 0.30,
    });

    // ── ENGINE METRICS ──
    engineMetrics = $state({
        totalVolume24h: 0,
        totalOpenInterest: 0,
        totalPredictionVolume: 0,
        activeAgents: 0,
        blockTime: 0.2,          // Sub-second finality
        ordersPerSecond: 0,
        lastEngineUpdate: Date.now(),
    });

    private _initialized = false;

    private _ensureInit() {
        if (!this._initialized) {
            this._initialized = true;
            const firstMarket = this.markets[0];
            if (firstMarket) this._generateOrderBook(firstMarket.id);
            this._updateMetrics();
        }
    }

    // ─── PERPETUAL TRADING METHODS ───────────────────────────────────────────

    /** Place a new perpetual order. */
    placeOrder(
        marketId: string, side: OrderSide, type: OrderType,
        size: number, price: number, leverage: number,
        options: { reduceOnly?: boolean; postOnly?: boolean } = {}
    ): PerpetualOrder | null {
        const market = this.markets.find(m => m.id === marketId);
        if (!market || market.status !== 'ACTIVE') return null;

        const effectivePrice = type === 'MARKET' ? market.markPrice : price;
        const margin = (size * effectivePrice) / leverage;
        const liquidationPrice = side === 'LONG'
            ? effectivePrice * (1 - 1 / leverage + 0.005)
            : effectivePrice * (1 + 1 / leverage - 0.005);

        const order: PerpetualOrder = {
            orderId: `ORD-${uuid().slice(0, 8).toUpperCase()}`,
            marketId, side, type, size, price: effectivePrice, leverage, margin,
            status: type === 'MARKET' ? 'FILLED' : 'OPEN',
            filledSize: type === 'MARKET' ? size : 0,
            avgFillPrice: type === 'MARKET' ? effectivePrice : 0,
            pnl: 0, liquidationPrice,
            createdAt: Date.now(), updatedAt: Date.now(),
            reducedOnly: options.reduceOnly ?? false,
            postOnly: options.postOnly ?? false,
        };

        if (type === 'MARKET') {
            this.orderHistory = [order, ...this.orderHistory].slice(0, 100);
        } else {
            this.activeOrders = [order, ...this.activeOrders];
        }

        return order;
    }

    /** Cancel an active order. */
    cancelOrder(orderId: string): boolean {
        const idx = this.activeOrders.findIndex(o => o.orderId === orderId);
        if (idx === -1) return false;
        const existing = this.activeOrders[idx];
        if (!existing) return false;
        const cancelled: PerpetualOrder = {
            orderId: existing.orderId, marketId: existing.marketId,
            side: existing.side, type: existing.type, size: existing.size,
            price: existing.price, leverage: existing.leverage, margin: existing.margin,
            filledSize: existing.filledSize, avgFillPrice: existing.avgFillPrice,
            pnl: existing.pnl, liquidationPrice: existing.liquidationPrice,
            createdAt: existing.createdAt, reducedOnly: existing.reducedOnly,
            postOnly: existing.postOnly,
            status: 'CANCELLED', updatedAt: Date.now(),
        };
        this.activeOrders.splice(idx, 1);
        this.orderHistory = [cancelled, ...this.orderHistory].slice(0, 100);
        return true;
    }

    /** Get the orderbook for a specific market. */
    getOrderBook(marketId: string): OrderBook {
        this._generateOrderBook(marketId);
        return this.orderBook;
    }

    // ─── PREDICTION MARKET METHODS ───────────────────────────────────────────

    /** Buy shares in a prediction outcome. */
    buyPredictionShares(marketId: string, outcomeId: string, amount: number): PredictionPosition | null {
        const market = this.predictionMarkets.find(m => m.marketId === marketId);
        if (!market || market.resolution !== 'PENDING') return null;

        const outcome = market.outcomes.find(o => o.outcomeId === outcomeId);
        if (!outcome) return null;

        const shares = amount / outcome.price;
        outcome.volume += amount;
        outcome.shares += shares;
        market.totalVolume += amount;

        // Recalculate probabilities
        const totalShares = market.outcomes.reduce((s, o) => s + o.shares, 0);
        market.outcomes.forEach(o => {
            o.probability = o.shares / totalShares;
            o.price = o.probability;
        });

        const position: PredictionPosition = {
            positionId: `PP-${uuid().slice(0, 8)}`,
            marketId, outcomeId,
            shares, avgPrice: outcome.price,
            currentValue: shares * outcome.price,
            pnl: 0, createdAt: Date.now(),
        };

        this.predictionPositions = [position, ...this.predictionPositions];
        return position;
    }

    /** Sell prediction shares. */
    sellPredictionShares(positionId: string, shares: number): boolean {
        const pos = this.predictionPositions.find(p => p.positionId === positionId);
        if (!pos || shares > pos.shares) return false;

        const market = this.predictionMarkets.find(m => m.marketId === pos.marketId);
        const outcome = market?.outcomes.find(o => o.outcomeId === pos.outcomeId);
        if (!outcome) return false;

        const saleValue = shares * outcome.price;
        pos.shares -= shares;
        pos.pnl += saleValue - (shares * pos.avgPrice);
        pos.currentValue = pos.shares * outcome.price;

        if (pos.shares <= 0) {
            this.predictionPositions = this.predictionPositions.filter(p => p.positionId !== positionId);
        }

        return true;
    }

    // ─── SOVEREIGN CARD METHODS ──────────────────────────────────────────────

    /** Process a card spending transaction. */
    processCardSpend(merchant: string, category: string, amount: number, country: string): CardTransaction | null {
        if (this.sovereignCard.status !== 'ACTIVE') return null;
        if (this.sovereignCard.dailySpent + amount > this.sovereignCard.dailyLimit) return null;
        if (this.sovereignCard.monthlySpent + amount > this.sovereignCard.monthlyLimit) return null;

        const cashback = amount * this.sovereignCard.cashbackRate;

        const tx: CardTransaction = {
            txId: `CTX-${uuid().slice(0, 6)}`,
            merchant, merchantCategory: category,
            amount, cryptoAmount: amount, exchangeRate: 1.0,
            cashbackEarned: cashback,
            timestamp: Date.now(),
            status: 'COMPLETED',
            country,
        };

        this.sovereignCard.transactions = [tx, ...this.sovereignCard.transactions].slice(0, 50);
        this.sovereignCard.dailySpent += amount;
        this.sovereignCard.monthlySpent += amount;

        return tx;
    }

    /** Toggle card freeze. */
    toggleCardFreeze() {
        this.sovereignCard.status = this.sovereignCard.status === 'ACTIVE' ? 'FROZEN' : 'ACTIVE';
    }

    // ─── FIAT RAMP METHODS ───────────────────────────────────────────────────

    /** Get a fiat on/off ramp quote. */
    getRampQuote(direction: RampDirection, fiatAmount: number, fiatCurrency: string, cryptoAsset: string, paymentMethod: PaymentMethod): RampQuote {
        const rates: Record<string, number> = { AGE: 1.42, BTC: 94500, ETH: 3200, RES: 1.0, SOL: 185 };
        const rate = rates[cryptoAsset] || 1;
        const feePct = paymentMethod === 'BANK_TRANSFER' ? 0.001 : 0.015;
        const fee = fiatAmount * feePct;

        return {
            quoteId: `RQ-${uuid().slice(0, 8)}`,
            direction, fiatAmount, fiatCurrency,
            cryptoAmount: direction === 'ON_RAMP' ? (fiatAmount - fee) / rate : fiatAmount * rate,
            cryptoAsset, exchangeRate: rate,
            fee, feePct,
            paymentMethod,
            expiresAt: Date.now() + 60000,
            provider: 'Sovereign Ramp Network',
        };
    }

    /** Execute a ramp transaction. */
    async executeRamp(quote: RampQuote): Promise<RampTransaction> {
        const tx: RampTransaction = {
            txId: `RT-${uuid().slice(0, 8)}`,
            direction: quote.direction,
            fiatAmount: quote.fiatAmount, fiatCurrency: quote.fiatCurrency,
            cryptoAmount: quote.cryptoAmount, cryptoAsset: quote.cryptoAsset,
            paymentMethod: quote.paymentMethod,
            status: 'PROCESSING', createdAt: Date.now(), completedAt: null,
        };

        this.rampHistory = [tx, ...this.rampHistory];

        // Simulate processing
        setTimeout(() => {
            const idx = this.rampHistory.findIndex(r => r.txId === tx.txId);
            if (idx !== -1) {
                const existing = this.rampHistory[idx];
                if (existing) {
                    const completed: RampTransaction = {
                        txId: existing.txId, direction: existing.direction,
                        fiatAmount: existing.fiatAmount, fiatCurrency: existing.fiatCurrency,
                        cryptoAmount: existing.cryptoAmount, cryptoAsset: existing.cryptoAsset,
                        paymentMethod: existing.paymentMethod, createdAt: existing.createdAt,
                        status: 'COMPLETED', completedAt: Date.now(),
                    };
                    this.rampHistory[idx] = completed;
                }
            }
        }, 3000);

        return tx;
    }

    // ─── AI AGENT METHODS ────────────────────────────────────────────────────

    /** Toggle an AI trading agent's status. */
    toggleAgent(agentId: string) {
        const agent = this.tradingAgents.find(a => a.agentId === agentId);
        if (!agent) return;
        agent.status = agent.status === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';
    }

    /** Adjust an agent's risk parameters. */
    updateAgentRisk(agentId: string, params: Partial<AgentRiskParams>) {
        const agent = this.tradingAgents.find(a => a.agentId === agentId);
        if (!agent) return;
        Object.assign(agent.riskParameters, params);
    }

    // ─── INTERNAL: PRICE SIMULATION ──────────────────────────────────────────

    /**
     * Called by SimulationEngine on each tick (3s).
     * Replaces orphan setInterval — all market drift flows through the heartbeat.
     */
    tick() {
        this._ensureInit();

        for (const market of this.markets) {
            const drift = (Math.random() - 0.48) * market.markPrice * 0.002;
            market.markPrice = Math.max(0.001, market.markPrice + drift);
            market.indexPrice = market.markPrice * (1 + (Math.random() - 0.5) * 0.001);
            market.fundingRate += (Math.random() - 0.5) * 0.0001;
            market.volume24h += Math.random() * 100000;
        }

        // Drift prediction markets
        for (const pm of this.predictionMarkets) {
            for (const outcome of pm.outcomes) {
                const shift = (Math.random() - 0.5) * 0.005;
                outcome.probability = Math.max(0.01, Math.min(0.99, outcome.probability + shift));
                outcome.price = outcome.probability;
            }
            // Normalize
            const totalP = pm.outcomes.reduce((s, o) => s + o.probability, 0);
            pm.outcomes.forEach(o => { o.probability /= totalP; o.price = o.probability; });
        }

        // Update agent P&L
        for (const agent of this.tradingAgents) {
            if (agent.status === 'ACTIVE') {
                const pnlDrift = (Math.random() - 0.45) * agent.portfolio.totalValue * 0.001;
                agent.performance.totalPnl += pnlDrift;
                agent.portfolio.totalValue += pnlDrift;
                agent.performance.totalPnlPct = (agent.performance.totalPnl / (agent.portfolio.totalValue - agent.performance.totalPnl)) * 100;
            }
        }

        this._updateMetrics();
        const firstMarket = this.markets[0];
        if (firstMarket) this._generateOrderBook(firstMarket.id);
    }

    private _generateOrderBook(marketId: string) {
        const market = this.markets.find(m => m.id === marketId);
        if (!market) return;

        const mid = market.markPrice;
        const bids: OrderBookLevel[] = [];
        const asks: OrderBookLevel[] = [];
        let bidCumulative = 0;
        let askCumulative = 0;

        for (let i = 0; i < 15; i++) {
            const bidPrice = mid - (i + 1) * market.tickSize * (1 + Math.random() * 2);
            const askPrice = mid + (i + 1) * market.tickSize * (1 + Math.random() * 2);
            const bidSize = Math.round((100 + Math.random() * 5000) * 10) / 10;
            const askSize = Math.round((100 + Math.random() * 5000) * 10) / 10;
            bidCumulative += bidSize;
            askCumulative += askSize;

            bids.push({ price: Math.round(bidPrice * 1000) / 1000, size: bidSize, total: bidCumulative, count: Math.floor(1 + Math.random() * 10) });
            asks.push({ price: Math.round(askPrice * 1000) / 1000, size: askSize, total: askCumulative, count: Math.floor(1 + Math.random() * 10) });
        }

        const bestBid = bids[0]?.price ?? mid;
        const bestAsk = asks[0]?.price ?? mid;

        this.orderBook = {
            bids, asks,
            spread: Math.round((bestAsk - bestBid) * 1000) / 1000,
            spreadPct: ((bestAsk - bestBid) / mid) * 100,
            lastUpdate: Date.now(),
        };
    }

    private _updateMetrics() {
        this.engineMetrics = {
            totalVolume24h: this.markets.reduce((s, m) => s + m.volume24h, 0),
            totalOpenInterest: this.markets.reduce((s, m) => s + m.openInterest, 0),
            totalPredictionVolume: this.predictionMarkets.reduce((s, m) => s + m.totalVolume, 0),
            activeAgents: this.tradingAgents.filter(a => a.status === 'ACTIVE').length,
            blockTime: 0.2 + Math.random() * 0.1,
            ordersPerSecond: 140000 + Math.floor(Math.random() * 60000),
            lastEngineUpdate: Date.now(),
        };
    }

}

// import { browser } from '$app/environment';
export const tradingEngine = new SovereignTradingEngine();
