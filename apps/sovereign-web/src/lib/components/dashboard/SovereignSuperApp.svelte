<!--
  ═══════════════════════════════════════════════════════════════════════════════
  🏛️ SOVEREIGN TRADING TERMINAL (SuperApp)
  ═══════════════════════════════════════════════════════════════════════════════
  Implements 6 core sovereign financial primitives:
  1. Perpetual Trading (CLOB orderbook)
  2. Prediction Markets (Outcome Trading)
  3. Sovereign Card (crypto-linked payments)
  4. Fiat On/Off Ramp
  5. AI Agentic Commerce
  6. Treasury-backed Stablecoin Yield
  ═══════════════════════════════════════════════════════════════════════════════
-->

<script lang="ts">
//     import { onMount, onDestroy } from "svelte";
    import { slide, fade } from "svelte/transition";
    import {
        tradingEngine,
        type OrderSide,
        type OrderType,
    } from "$lib/services/sovereign-trading-engine.svelte";

    // ── TAB STATE ──
    type SuperAppTab =
        | "TRADE"
        | "PREDICT"
        | "CARD"
        | "RAMP"
        | "AGENTS"
        | "YIELD";
    let activeTab = $state<SuperAppTab>("TRADE");

    // ── TRADING STATE ──
    let selectedMarketId = $state("AGE-USD-PERP");
    let orderSide = $state<OrderSide>("LONG");
    let orderType = $state<OrderType>("MARKET");
    let orderSize = $state(100);
    let orderPrice = $state(0);
    let orderLeverage = $state(5);
    let showConfirm = $state(false);

    // ── PREDICTION STATE ──
    let predictionAmount = $state(100);

    // ── RAMP STATE ──
    let rampAmount = $state(1000);
    let rampCurrency = $state("USD");
    let rampAsset = $state("AGE");
    let rampDirection = $state<"ON_RAMP" | "OFF_RAMP">("ON_RAMP");

    // ── DERIVED ──
    const selectedMarket = $derived(
        tradingEngine.markets.find((m) => m.id === selectedMarketId)!,
    );
    const orderBook = $derived(tradingEngine.orderBook);
    const metrics = $derived(tradingEngine.engineMetrics);

    let refreshKey = $state(0);
    let refreshInterval: ReturnType<typeof setInterval> | null = null;

    onMount(() => {
        refreshInterval = setInterval(() => {
            refreshKey++;
        }, 2000);
    });
    onDestroy(() => {
        if (refreshInterval) clearInterval(refreshInterval);
    });

    // ── ACTIONS ──
    function placeOrder() {
        const price =
            orderType === "MARKET" ? 0 : orderPrice || selectedMarket.markPrice;
        tradingEngine.placeOrder(
            selectedMarketId,
            orderSide,
            orderType,
            orderSize,
            price,
            orderLeverage,
        );
        showConfirm = true;
        setTimeout(() => {
            showConfirm = false;
        }, 2000);
    }

    function buyPrediction(marketId: string, outcomeId: string) {
        tradingEngine.buyPredictionShares(
            marketId,
            outcomeId,
            predictionAmount,
        );
    }

    function formatCurrency(n: number): string {
        if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(2)}B`;
        if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
        if (n >= 1_000) return `$${(n / 1_000).toFixed(1)}K`;
        return `$${n.toFixed(2)}`;
    }

    function formatPct(n: number): string {
        return `${n >= 0 ? "+" : ""}${n.toFixed(2)}%`;
    }

    const tabConfigs: { id: SuperAppTab; label: string; icon: string }[] = [
        { id: "TRADE", label: "Trade", icon: "📊" },
        { id: "PREDICT", label: "Predict", icon: "🔮" },
        { id: "CARD", label: "Card", icon: "💳" },
        { id: "RAMP", label: "Ramp", icon: "🏦" },
        { id: "AGENTS", label: "Agents", icon: "🤖" },
        { id: "YIELD", label: "Yield", icon: "🌱" },
    ];
</script>

<!-- ═══ MAIN CONTAINER ═══ -->
<div class="superapp-terminal" data-refresh={refreshKey}>
    <!-- ═══ HEADER BAR ═══ -->
    <header class="terminal-header">
        <div class="header-brand">
            <div class="brand-icon">⚡</div>
            <div>
                <h2>Sovereign SuperApp</h2>
                <p class="brand-sub">On-chain CLOB · Sub-200ms Finality</p>
            </div>
        </div>
        <div class="header-stats">
            <div class="stat-chip">
                <span class="stat-label">24h Vol</span>
                <span class="stat-value"
                    >{formatCurrency(metrics.totalVolume24h)}</span
                >
            </div>
            <div class="stat-chip">
                <span class="stat-label">Open Interest</span>
                <span class="stat-value"
                    >{formatCurrency(metrics.totalOpenInterest)}</span
                >
            </div>
            <div class="stat-chip stat-speed">
                <span class="stat-label">Block</span>
                <span class="stat-value">{metrics.blockTime.toFixed(1)}s</span>
            </div>
            <div class="stat-chip">
                <span class="stat-label">OPS</span>
                <span class="stat-value"
                    >{(metrics.ordersPerSecond / 1000).toFixed(0)}K/s</span
                >
            </div>
        </div>
    </header>

    <!-- ═══ TAB BAR ═══ -->
    <nav class="tab-bar">
        {#each tabConfigs as tab}
            <button
                class="tab-btn"
                class:active={activeTab === tab.id}
                onclick={() => (activeTab = tab.id)}
            >
                <span class="tab-icon">{tab.icon}</span>
                <span class="tab-label">{tab.label}</span>
            </button>
        {/each}
    </nav>

    <!-- ═══ CONTENT ═══ -->
    <div class="tab-content">
        <!-- ════ TAB: TRADE ════ -->
        {#if activeTab === "TRADE"}
            <div class="trade-panel" transitionfade={{ duration: 200 }}>
                <!-- Market Selector -->
                <div class="market-selector">
                    {#each tradingEngine.markets as m}
                        <button
                            class="market-chip"
                            class:selected={selectedMarketId === m.id}
                            onclick={() => (selectedMarketId = m.id)}
                        >
                            <span class="mc-symbol">{m.symbol}</span>
                            <span class="mc-price"
                                >${m.markPrice.toLocaleString(undefined, {
                                    minimumFractionDigits: 2,
                                })}</span
                            >
                            <span
                                class="mc-funding"
                                class:positive={m.fundingRate >= 0}
                                class:negative={m.fundingRate < 0}
                            >
                                {formatPct(m.fundingRate * 100)}
                            </span>
                        </button>
                    {/each}
                </div>

                <div class="trade-grid">
                    <!-- Orderbook -->
                    <div class="orderbook-panel">
                        <h3>Order Book</h3>
                        <div class="ob-header">
                            <span>Price</span><span>Size</span><span>Total</span
                            >
                        </div>
                        <div class="ob-asks">
                            {#each orderBook.asks.slice(0, 10).reverse() as ask}
                                <div class="ob-row ask">
                                    <span class="ob-price"
                                        >{ask.price.toFixed(3)}</span
                                    >
                                    <span class="ob-size"
                                        >{ask.size.toFixed(1)}</span
                                    >
                                    <span class="ob-total"
                                        >{ask.total.toFixed(0)}</span
                                    >
                                    <div
                                        class="ob-bar ask-bar"
                                        style="width: {Math.min(
                                            100,
                                            (ask.size / 5000) * 100,
                                        )}%"
                                    ></div>
                                </div>
                            {/each}
                        </div>
                        <div class="ob-spread">
                            <span
                                >Spread: {orderBook.spread.toFixed(3)} ({orderBook.spreadPct.toFixed(
                                    3,
                                )}%)</span
                            >
                        </div>
                        <div class="ob-bids">
                            {#each orderBook.bids.slice(0, 10) as bid}
                                <div class="ob-row bid">
                                    <span class="ob-price"
                                        >{bid.price.toFixed(3)}</span
                                    >
                                    <span class="ob-size"
                                        >{bid.size.toFixed(1)}</span
                                    >
                                    <span class="ob-total"
                                        >{bid.total.toFixed(0)}</span
                                    >
                                    <div
                                        class="ob-bar bid-bar"
                                        style="width: {Math.min(
                                            100,
                                            (bid.size / 5000) * 100,
                                        )}%"
                                    ></div>
                                </div>
                            {/each}
                        </div>
                    </div>

                    <!-- Order Entry -->
                    <div class="order-entry">
                        <h3>New Order — {selectedMarket.symbol}</h3>
                        <div class="side-toggle">
                            <button
                                class="side-btn long"
                                class:active={orderSide === "LONG"}
                                onclick={() => (orderSide = "LONG")}
                                >Long</button
                            >
                            <button
                                class="side-btn short"
                                class:active={orderSide === "SHORT"}
                                onclick={() => (orderSide = "SHORT")}
                                >Short</button
                            >
                        </div>

                        <div class="type-selector">
                            {#each ["MARKET", "LIMIT", "STOP_LOSS", "TAKE_PROFIT"] as const as t}
                                <button
                                    class="type-chip"
                                    class:active={orderType === t}
                                    onclick={() => (orderType = t)}
                                    >{t.replace("_", " ")}</button
                                >
                            {/each}
                        </div>

                        <div class="order-fields">
                            <label class="field-group">
                                <span class="field-label"
                                    >Size ({selectedMarket.baseAsset})</span
                                >
                                <input
                                    type="number"
                                    bind:value={orderSize}
                                    class="field-input"
                                    step="1"
                                />
                            </label>
                            {#if orderType !== "MARKET"}
                                <label class="field-group">
                                    <span class="field-label">Price (USD)</span>
                                    <input
                                        type="number"
                                        bind:value={orderPrice}
                                        class="field-input"
                                        step="0.001"
                                        placeholder={selectedMarket.markPrice.toFixed(
                                            3,
                                        )}
                                    />
                                </label>
                            {/if}
                            <label class="field-group">
                                <span class="field-label">Leverage</span>
                                <div class="leverage-row">
                                    <input
                                        type="range"
                                        min="1"
                                        max={selectedMarket.maxLeverage}
                                        bind:value={orderLeverage}
                                        class="leverage-slider"
                                    />
                                    <span class="leverage-value"
                                        >{orderLeverage}x</span
                                    >
                                </div>
                            </label>
                        </div>

                        <div class="order-summary">
                            <div class="summary-row">
                                <span>Margin Required</span><span
                                    >{formatCurrency(
                                        (orderSize * selectedMarket.markPrice) /
                                            orderLeverage,
                                    )}</span
                                >
                            </div>
                            <div class="summary-row">
                                <span>Notional</span><span
                                    >{formatCurrency(
                                        orderSize * selectedMarket.markPrice,
                                    )}</span
                                >
                            </div>
                            <div class="summary-row">
                                <span>Est. Liq. Price</span><span
                                    >${(
                                        selectedMarket.markPrice *
                                        (orderSide === "LONG"
                                            ? 1 - 1 / orderLeverage
                                            : 1 + 1 / orderLeverage)
                                    ).toFixed(3)}</span
                                >
                            </div>
                        </div>

                        <button
                            class="execute-btn {orderSide === 'LONG'
                                ? 'execute-long'
                                : 'execute-short'}"
                            onclick={placeOrder}
                        >
                            {orderSide === "LONG" ? "🟢" : "🔴"}
                            {orderType === "MARKET"
                                ? "Market"
                                : orderType.replace("_", " ")}
                            {orderSide}
                        </button>

                        {#if showConfirm}
                            <div class="order-confirm" transition:slide>
                                ✅ Order placed successfully
                            </div>
                        {/if}
                    </div>
                </div>
            </div>

            <!-- ════ TAB: PREDICTION MARKETS ════ -->
        {:else if activeTab === "PREDICT"}
            <div class="predict-panel" transitionfade={{ duration: 200 }}>
                <div class="predict-header">
                    <h3>🔮 Outcome Trading</h3>
                    <div class="predict-stats">
                        <span class="ps"
                            >Total Volume: {formatCurrency(
                                metrics.totalPredictionVolume,
                            )}</span
                        >
                        <span class="ps"
                            >{tradingEngine.predictionMarkets.length} Markets</span
                        >
                        <span class="ps badge-fully-coll"
                            >Fully Collateralized</span
                        >
                    </div>
                </div>

                <div class="predict-grid">
                    {#each tradingEngine.predictionMarkets as market}
                        <div
                            class="predict-card"
                            class:featured={market.featured}
                        >
                            <div class="pc-category">{market.category}</div>
                            <h4 class="pc-question">{market.question}</h4>
                            <p class="pc-description">{market.description}</p>

                            <div class="pc-outcomes">
                                {#each market.outcomes as outcome}
                                    <div class="outcome-row">
                                        <div class="outcome-info">
                                            <span class="outcome-label"
                                                >{outcome.label}</span
                                            >
                                            <div class="outcome-bar-wrap">
                                                <div
                                                    class="outcome-bar"
                                                    style="width: {outcome.probability *
                                                        100}%; background: {outcome.label ===
                                                    'Yes'
                                                        ? 'var(--color-emerald)'
                                                        : 'var(--color-rose)'}"
                                                ></div>
                                            </div>
                                            <span class="outcome-pct"
                                                >{(
                                                    outcome.probability * 100
                                                ).toFixed(1)}%</span
                                            >
                                        </div>
                                        <button
                                            class="outcome-buy-btn"
                                            onclick={() =>
                                                buyPrediction(
                                                    market.marketId,
                                                    outcome.outcomeId,
                                                )}
                                        >
                                            Buy @ ${outcome.price.toFixed(2)}
                                        </button>
                                    </div>
                                {/each}
                            </div>

                            <div class="pc-footer">
                                <span
                                    >Vol: {formatCurrency(
                                        market.totalVolume,
                                    )}</span
                                >
                                <span
                                    >Liq: {formatCurrency(
                                        market.totalLiquidity,
                                    )}</span
                                >
                                <span
                                    >Resolves: {new Date(
                                        market.resolvesAt,
                                    ).toLocaleDateString()}</span
                                >
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- ════ TAB: SOVEREIGN CARD ════ -->
        {:else if activeTab === "CARD"}
            <div class="card-panel" transitionfade={{ duration: 200 }}>
                <div class="card-visual">
                    <div class="card-render">
                        <div class="card-bg"></div>
                        <div class="card-chip">🔒</div>
                        <div class="card-logo">AGE PROTOCOL</div>
                        <div class="card-number">
                            {tradingEngine.sovereignCard.maskedNumber}
                        </div>
                        <div class="card-tier">
                            {tradingEngine.sovereignCard.tier} TIER
                        </div>
                        <div class="card-network">VISA</div>
                        <div
                            class="card-status-badge"
                            class:card-active={tradingEngine.sovereignCard
                                .status === "ACTIVE"}
                            class:card-frozen={tradingEngine.sovereignCard
                                .status === "FROZEN"}
                        >
                            {tradingEngine.sovereignCard.status}
                        </div>
                    </div>
                </div>

                <div class="card-controls">
                    <div class="card-limits">
                        <div class="limit-item">
                            <span class="limit-label">Daily</span>
                            <div class="limit-bar-wrap">
                                <div
                                    class="limit-bar"
                                    style="width: {(tradingEngine.sovereignCard
                                        .dailySpent /
                                        tradingEngine.sovereignCard
                                            .dailyLimit) *
                                        100}%"
                                ></div>
                            </div>
                            <span class="limit-text"
                                >{formatCurrency(
                                    tradingEngine.sovereignCard.dailySpent,
                                )} / {formatCurrency(
                                    tradingEngine.sovereignCard.dailyLimit,
                                )}</span
                            >
                        </div>
                        <div class="limit-item">
                            <span class="limit-label">Monthly</span>
                            <div class="limit-bar-wrap">
                                <div
                                    class="limit-bar"
                                    style="width: {(tradingEngine.sovereignCard
                                        .monthlySpent /
                                        tradingEngine.sovereignCard
                                            .monthlyLimit) *
                                        100}%"
                                ></div>
                            </div>
                            <span class="limit-text"
                                >{formatCurrency(
                                    tradingEngine.sovereignCard.monthlySpent,
                                )} / {formatCurrency(
                                    tradingEngine.sovereignCard.monthlyLimit,
                                )}</span
                            >
                        </div>
                    </div>

                    <div class="card-stats-row">
                        <div class="card-stat">
                            <span>Cashback</span><span class="cs-val"
                                >{(
                                    tradingEngine.sovereignCard.cashbackRate *
                                    100
                                ).toFixed(0)}% in AGE</span
                            >
                        </div>
                        <div class="card-stat">
                            <span>Funding</span><span class="cs-val"
                                >{tradingEngine.sovereignCard
                                    .fundingAsset}</span
                            >
                        </div>
                        <div class="card-stat">
                            <span>Auto-Convert</span><span class="cs-val"
                                >{tradingEngine.sovereignCard.autoConvert
                                    ? "✅"
                                    : "❌"}</span
                            >
                        </div>
                    </div>

                    <button
                        class="freeze-btn"
                        onclick={() => tradingEngine.toggleCardFreeze()}
                    >
                        {tradingEngine.sovereignCard.status === "ACTIVE"
                            ? "❄️ Freeze Card"
                            : "🔓 Unfreeze Card"}
                    </button>
                </div>

                <div class="card-txns">
                    <h4>Recent Transactions</h4>
                    {#each tradingEngine.sovereignCard.transactions.slice(0, 6) as tx}
                        <div class="card-tx-row">
                            <div class="ctx-merchant">
                                <span class="ctx-flag"
                                    >{tx.country === "JP"
                                        ? "🇯🇵"
                                        : tx.country === "CH"
                                          ? "🇨🇭"
                                          : "🇺🇸"}</span
                                >
                                <span class="ctx-name">{tx.merchant}</span>
                            </div>
                            <div class="ctx-amount">
                                -{formatCurrency(tx.amount)}
                            </div>
                            <div class="ctx-cashback">
                                +{tx.cashbackEarned.toFixed(2)} AGE
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- ════ TAB: FIAT RAMP ════ -->
        {:else if activeTab === "RAMP"}
            <div class="ramp-panel" transitionfade={{ duration: 200 }}>
                <h3>🏦 Sovereign On/Off Ramp</h3>
                <div class="ramp-toggle">
                    <button
                        class="ramp-dir"
                        class:active={rampDirection === "ON_RAMP"}
                        onclick={() => (rampDirection = "ON_RAMP")}
                        >Buy Crypto</button
                    >
                    <button
                        class="ramp-dir"
                        class:active={rampDirection === "OFF_RAMP"}
                        onclick={() => (rampDirection = "OFF_RAMP")}
                        >Sell Crypto</button
                    >
                </div>

                <div class="ramp-form">
                    <label class="field-group">
                        <span class="field-label"
                            >{rampDirection === "ON_RAMP"
                                ? "You Pay (Fiat)"
                                : "You Sell (Crypto)"}</span
                        >
                        <div class="ramp-input-row">
                            <input
                                type="number"
                                bind:value={rampAmount}
                                class="field-input"
                            />
                            {#if rampDirection === "ON_RAMP"}
                                <select
                                    bind:value={rampCurrency}
                                    class="ramp-select"
                                >
                                    <option value="USD">USD</option>
                                    <option value="EUR">EUR</option>
                                    <option value="JPY">JPY</option>
                                    <option value="CHF">CHF</option>
                                </select>
                            {:else}
                                <select
                                    bind:value={rampAsset}
                                    class="ramp-select"
                                >
                                    <option value="AGE">AGE</option>
                                    <option value="BTC">BTC</option>
                                    <option value="ETH">ETH</option>
                                    <option value="RES">RES</option>
                                </select>
                            {/if}
                        </div>
                    </label>

                    <div class="ramp-arrow">↕</div>

                    <label class="field-group">
                        <span class="field-label"
                            >{rampDirection === "ON_RAMP"
                                ? "You Receive (Crypto)"
                                : "You Receive (Fiat)"}</span
                        >
                        <div class="ramp-input-row">
                            <input
                                type="text"
                                value={formatCurrency(
                                    rampAmount *
                                        (rampDirection === "ON_RAMP"
                                            ? 1 / 1.42
                                            : 1.42),
                                )}
                                class="field-input"
                                readonly
                            />
                            {#if rampDirection === "ON_RAMP"}
                                <select
                                    bind:value={rampAsset}
                                    class="ramp-select"
                                >
                                    <option value="AGE">AGE</option>
                                    <option value="BTC">BTC</option>
                                    <option value="ETH">ETH</option>
                                </select>
                            {:else}
                                <select
                                    bind:value={rampCurrency}
                                    class="ramp-select"
                                >
                                    <option value="USD">USD</option>
                                    <option value="EUR">EUR</option>
                                    <option value="JPY">JPY</option>
                                </select>
                            {/if}
                        </div>
                    </label>
                </div>

                <div class="ramp-methods">
                    <h4>Payment Methods</h4>
                    <div class="method-grid">
                        {#each tradingEngine.availablePaymentMethods as method}
                            <button class="method-chip"
                                >{method === "BANK_TRANSFER"
                                    ? "🏦"
                                    : method === "VISA"
                                      ? "💳"
                                      : method === "MASTERCARD"
                                        ? "💳"
                                        : method === "APPLE_PAY"
                                          ? "🍎"
                                          : "📱"}
                                {method.replace("_", " ")}</button
                            >
                        {/each}
                    </div>
                </div>

                <button
                    class="execute-btn execute-long"
                    onclick={() =>
                        tradingEngine.executeRamp(
                            tradingEngine.getRampQuote(
                                rampDirection,
                                rampAmount,
                                rampCurrency,
                                rampAsset,
                                "VISA",
                            ),
                        )}
                >
                    {rampDirection === "ON_RAMP" ? "💰 Buy" : "💸 Sell"} — Fee: 1.5%
                </button>
            </div>

            <!-- ════ TAB: AI AGENTS ════ -->
        {:else if activeTab === "AGENTS"}
            <div class="agents-panel" transitionfade={{ duration: 200 }}>
                <div class="agents-header">
                    <h3>🤖 Agentic Commerce</h3>
                    <span class="agents-count"
                        >{tradingEngine.tradingAgents.filter(
                            (a) => a.status === "ACTIVE",
                        ).length} Active / {tradingEngine.tradingAgents.length} Total</span
                    >
                </div>

                <div class="agents-grid">
                    {#each tradingEngine.tradingAgents as agent}
                        <div
                            class="agent-card"
                            class:agent-active={agent.status === "ACTIVE"}
                            class:agent-paused={agent.status === "PAUSED"}
                        >
                            <div class="agent-header-row">
                                <div>
                                    <h4 class="agent-name">{agent.name}</h4>
                                    <span class="agent-strategy"
                                        >{agent.strategy.replace(
                                            "_",
                                            " ",
                                        )}</span
                                    >
                                </div>
                                <button
                                    class="agent-toggle"
                                    onclick={() =>
                                        tradingEngine.toggleAgent(
                                            agent.agentId,
                                        )}
                                >
                                    {agent.status === "ACTIVE"
                                        ? "⏸ Pause"
                                        : "▶ Start"}
                                </button>
                            </div>

                            <div class="agent-perf">
                                <div class="perf-item">
                                    <span class="perf-label">Total P&L</span>
                                    <span
                                        class="perf-value"
                                        class:positive={agent.performance
                                            .totalPnl >= 0}
                                        class:negative={agent.performance
                                            .totalPnl < 0}
                                    >
                                        {formatCurrency(
                                            agent.performance.totalPnl,
                                        )} ({formatPct(
                                            agent.performance.totalPnlPct,
                                        )})
                                    </span>
                                </div>
                                <div class="perf-item">
                                    <span class="perf-label">Win Rate</span>
                                    <span class="perf-value"
                                        >{(
                                            agent.performance.winRate * 100
                                        ).toFixed(1)}%</span
                                    >
                                </div>
                                <div class="perf-item">
                                    <span class="perf-label">Sharpe</span>
                                    <span class="perf-value"
                                        >{agent.performance.sharpeRatio.toFixed(
                                            1,
                                        )}</span
                                    >
                                </div>
                                <div class="perf-item">
                                    <span class="perf-label">Portfolio</span>
                                    <span class="perf-value"
                                        >{formatCurrency(
                                            agent.portfolio.totalValue,
                                        )}</span
                                    >
                                </div>
                            </div>

                            <div class="agent-last-action">
                                <span class="ala-label">Last:</span>
                                <span class="ala-text">{agent.lastAction}</span>
                            </div>

                            <div class="agent-risk-row">
                                <span
                                    >Max Leverage: {agent.riskParameters
                                        .maxLeverage}x</span
                                >
                                <span
                                    >SL: {agent.riskParameters
                                        .stopLossPct}%</span
                                >
                                <span
                                    >TP: {agent.riskParameters
                                        .takeProfitPct}%</span
                                >
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- ════ TAB: YIELD ════ -->
        {:else if activeTab === "YIELD"}
            <div class="yield-panel" transitionfade={{ duration: 200 }}>
                <div class="yield-hero">
                    <div class="yield-apy">
                        <span class="apy-label">Current RES Yield</span>
                        <span class="apy-value"
                            >{tradingEngine.stablecoinYield.currentApy.toFixed(
                                1,
                            )}% APY</span
                        >
                        <span class="apy-source"
                            >Backed by {tradingEngine.stablecoinYield.source.replace(
                                "_",
                                " ",
                            )}</span
                        >
                    </div>
                </div>

                <div class="yield-details">
                    <div class="yield-stat">
                        <span class="ys-label">Total Reserves</span>
                        <span class="ys-value"
                            >{formatCurrency(
                                tradingEngine.stablecoinYield.totalReserves,
                            )}</span
                        >
                    </div>
                    <div class="yield-stat">
                        <span class="ys-label">Treasury Backing</span>
                        <span class="ys-value"
                            >{(
                                tradingEngine.stablecoinYield.treasuryBacking *
                                100
                            ).toFixed(0)}%</span
                        >
                    </div>
                    <div class="yield-stat">
                        <span class="ys-label">Reserve Ratio</span>
                        <span class="ys-value"
                            >{tradingEngine.stablecoinYield.proofOfReserves.reserveRatio.toFixed(
                                2,
                            )}x</span
                        >
                    </div>
                    <div class="yield-stat">
                        <span class="ys-label">AGE Buyback</span>
                        <span class="ys-value"
                            >{(
                                tradingEngine.stablecoinYield
                                    .buybackAllocation * 100
                            ).toFixed(0)}% of yield</span
                        >
                    </div>
                </div>

                <div class="yield-audit">
                    <div
                        class="audit-badge"
                        class:audit-verified={tradingEngine.stablecoinYield
                            .proofOfReserves.verified}
                    >
                        {tradingEngine.stablecoinYield.proofOfReserves.verified
                            ? "✅"
                            : "⚠️"}
                        Proof of Reserves: {tradingEngine.stablecoinYield
                            .proofOfReserves.verified
                            ? "VERIFIED"
                            : "PENDING"}
                    </div>
                    <span class="audit-date">
                        Last Audit: {new Date(
                            tradingEngine.stablecoinYield.proofOfReserves.lastAudit,
                        ).toLocaleDateString()}
                        by {tradingEngine.stablecoinYield.proofOfReserves
                            .auditor}
                    </span>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    /* ═══ DESIGN TOKENS ═══ */
    .superapp-terminal {
        --st-bg: rgba(8, 10, 18, 0.97);
        --st-card: rgba(16, 20, 32, 0.9);
        --st-border: rgba(80, 100, 160, 0.12);
        --st-text: #e0e4ef;
        --st-dim: #6b7590;
        --st-accent: #6366f1;
        --color-emerald: #10b981;
        --color-rose: #f43f5e;
        --color-amber: #f59e0b;
        --color-cyan: #22d3ee;
        --color-gold: #eab308;
        background: var(--st-bg);
        border: 1px solid var(--st-border);
        border-radius: 20px;
        color: var(--st-text);
        font-family: "Inter", system-ui, sans-serif;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    /* ═══ HEADER ═══ */
    .terminal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        border-bottom: 1px solid var(--st-border);
    }
    .header-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-icon {
        font-size: 28px;
        filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.5));
    }
    .terminal-header h2 {
        margin: 0;
        font-size: 17px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .brand-sub {
        margin: 0;
        font-size: 10px;
        color: var(--st-dim);
        font-weight: 600;
    }
    .header-stats {
        display: flex;
        gap: 8px;
    }
    .stat-chip {
        padding: 4px 10px;
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1px;
    }
    .stat-label {
        font-size: 8px;
        color: var(--st-dim);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        font-size: 12px;
        font-weight: 800;
        font-variant-numeric: tabular-nums;
    }
    .stat-speed .stat-value {
        color: var(--color-emerald);
    }

    /* ═══ TAB BAR ═══ */
    .tab-bar {
        display: flex;
        gap: 2px;
        padding: 4px 16px;
        border-bottom: 1px solid var(--st-border);
        background: rgba(0, 0, 0, 0.3);
    }
    .tab-btn {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 10px 8px;
        border: none;
        background: transparent;
        color: var(--st-dim);
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .tab-btn:hover {
        background: rgba(99, 102, 241, 0.08);
        color: var(--st-text);
    }
    .tab-btn.active {
        background: linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.2),
            rgba(168, 85, 247, 0.15)
        );
        color: white;
        border-bottom: 2px solid var(--st-accent);
    }
    .tab-icon {
        font-size: 14px;
    }
    .tab-label {
        font-size: 11px;
    }

    /* ═══ CONTENT ═══ */
    .tab-content {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
    }

    /* ═══ TRADE TAB ═══ */
    .market-selector {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 14px;
    }
    .market-chip {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s;
        color: var(--st-text);
        font-size: 12px;
    }
    .market-chip:hover {
        border-color: var(--st-accent);
    }
    .market-chip.selected {
        background: rgba(99, 102, 241, 0.15);
        border-color: var(--st-accent);
    }
    .mc-symbol {
        font-weight: 800;
        font-size: 12px;
    }
    .mc-price {
        font-weight: 700;
        font-variant-numeric: tabular-nums;
    }
    .mc-funding {
        font-size: 10px;
        font-weight: 700;
    }
    .mc-funding.positive {
        color: var(--color-emerald);
    }
    .mc-funding.negative {
        color: var(--color-rose);
    }

    .trade-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
    }

    /* Orderbook */
    .orderbook-panel {
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 12px;
        padding: 12px;
        overflow: hidden;
    }
    .orderbook-panel h3 {
        margin: 0 0 8px;
        font-size: 12px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .ob-header {
        display: flex;
        justify-content: space-between;
        font-size: 9px;
        color: var(--st-dim);
        font-weight: 700;
        text-transform: uppercase;
        padding: 0 4px 4px;
        border-bottom: 1px solid var(--st-border);
    }
    .ob-row {
        display: flex;
        justify-content: space-between;
        padding: 2px 4px;
        font-size: 11px;
        font-family: "JetBrains Mono", monospace;
        position: relative;
    }
    .ob-row span {
        position: relative;
        z-index: 1;
    }
    .ob-bar {
        position: absolute;
        top: 0;
        right: 0;
        height: 100%;
        opacity: 0.08;
    }
    .ask-bar {
        background: var(--color-rose);
    }
    .bid-bar {
        background: var(--color-emerald);
    }
    .ob-price {
        font-weight: 700;
    }
    .ask .ob-price {
        color: var(--color-rose);
    }
    .bid .ob-price {
        color: var(--color-emerald);
    }
    .ob-size,
    .ob-total {
        color: var(--st-dim);
        font-size: 10px;
    }
    .ob-spread {
        text-align: center;
        padding: 4px;
        font-size: 10px;
        color: var(--st-dim);
        font-weight: 700;
        border-top: 1px solid var(--st-border);
        border-bottom: 1px solid var(--st-border);
        margin: 4px 0;
    }
    .ob-asks,
    .ob-bids {
        max-height: 200px;
        overflow: hidden;
    }

    /* Order Entry */
    .order-entry {
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 12px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .order-entry h3 {
        margin: 0;
        font-size: 13px;
        font-weight: 700;
    }
    .side-toggle {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4px;
    }
    .side-btn {
        padding: 10px;
        border: none;
        border-radius: 8px;
        font-weight: 800;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
        color: white;
    }
    .side-btn.long {
        background: rgba(16, 185, 129, 0.15);
        color: var(--color-emerald);
    }
    .side-btn.long.active {
        background: var(--color-emerald);
        color: black;
    }
    .side-btn.short {
        background: rgba(244, 63, 94, 0.15);
        color: var(--color-rose);
    }
    .side-btn.short.active {
        background: var(--color-rose);
        color: white;
    }
    .type-selector {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
    }
    .type-chip {
        padding: 5px 10px;
        border: 1px solid var(--st-border);
        border-radius: 6px;
        background: transparent;
        color: var(--st-dim);
        font-size: 10px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s;
    }
    .type-chip.active {
        background: rgba(99, 102, 241, 0.2);
        color: white;
        border-color: var(--st-accent);
    }
    .order-fields {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .field-group {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .field-label {
        font-size: 10px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
    }
    .field-input {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid var(--st-border);
        border-radius: 8px;
        padding: 8px 12px;
        color: white;
        font-size: 14px;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
        outline: none;
        transition: border-color 0.2s;
    }
    .field-input:focus {
        border-color: var(--st-accent);
    }
    .leverage-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .leverage-slider {
        flex: 1;
        accent-color: var(--st-accent);
    }
    .leverage-value {
        font-size: 14px;
        font-weight: 800;
        color: var(--color-amber);
        min-width: 32px;
    }
    .order-summary {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 8px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
    }
    .summary-row {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: var(--st-dim);
    }
    .summary-row span:last-child {
        color: var(--st-text);
        font-weight: 700;
    }
    .execute-btn {
        padding: 12px;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
        letter-spacing: 0.5px;
    }
    .execute-long {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
    }
    .execute-long:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
    }
    .execute-short {
        background: linear-gradient(135deg, #e11d48, #f43f5e);
        color: white;
    }
    .execute-short:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(244, 63, 94, 0.3);
    }
    .order-confirm {
        padding: 8px;
        text-align: center;
        font-size: 12px;
        font-weight: 700;
        color: var(--color-emerald);
        background: rgba(16, 185, 129, 0.1);
        border-radius: 8px;
    }

    /* ═══ PREDICT TAB ═══ */
    .predict-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }
    .predict-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 800;
    }
    .predict-stats {
        display: flex;
        gap: 8px;
    }
    .ps {
        font-size: 10px;
        font-weight: 700;
        color: var(--st-dim);
        padding: 4px 10px;
        background: var(--st-card);
        border-radius: 8px;
        border: 1px solid var(--st-border);
    }
    .badge-fully-coll {
        color: var(--color-emerald);
        border-color: rgba(16, 185, 129, 0.3);
    }
    .predict-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .predict-card {
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 14px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        transition: border-color 0.2s;
    }
    .predict-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }
    .predict-card.featured {
        border-color: rgba(234, 179, 8, 0.3);
    }
    .pc-category {
        font-size: 9px;
        font-weight: 800;
        color: var(--color-cyan);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .pc-question {
        margin: 0;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.3;
    }
    .pc-description {
        margin: 0;
        font-size: 11px;
        color: var(--st-dim);
        line-height: 1.4;
    }
    .pc-outcomes {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .outcome-row {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .outcome-info {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .outcome-label {
        font-size: 12px;
        font-weight: 700;
        min-width: 30px;
    }
    .outcome-bar-wrap {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
        overflow: hidden;
    }
    .outcome-bar {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    .outcome-pct {
        font-size: 12px;
        font-weight: 800;
        min-width: 42px;
        text-align: right;
        font-variant-numeric: tabular-nums;
    }
    .outcome-buy-btn {
        padding: 4px 10px;
        border: 1px solid var(--st-border);
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.1);
        color: var(--st-accent);
        font-size: 10px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s;
        white-space: nowrap;
    }
    .outcome-buy-btn:hover {
        background: rgba(99, 102, 241, 0.25);
        border-color: var(--st-accent);
    }
    .pc-footer {
        display: flex;
        gap: 12px;
        font-size: 10px;
        color: var(--st-dim);
        font-weight: 600;
        border-top: 1px solid var(--st-border);
        padding-top: 8px;
    }

    /* ═══ CARD TAB ═══ */
    .card-panel {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .card-visual {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }
    .card-render {
        position: relative;
        width: 360px;
        height: 220px;
        background: linear-gradient(
            135deg,
            #1a1a2e 0%,
            #16213e 50%,
            #0f3460 100%
        );
        border-radius: 20px;
        padding: 24px;
        overflow: hidden;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 40px rgba(99, 102, 241, 0.1);
    }
    .card-bg {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 80% 20%,
            rgba(99, 102, 241, 0.15) 0%,
            transparent 50%
        );
    }
    .card-chip {
        position: absolute;
        top: 24px;
        left: 24px;
        font-size: 28px;
    }
    .card-logo {
        position: absolute;
        top: 28px;
        right: 24px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2px;
        color: rgba(255, 255, 255, 0.6);
    }
    .card-number {
        position: absolute;
        bottom: 60px;
        left: 24px;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 3px;
        font-family: "JetBrains Mono", monospace;
    }
    .card-tier {
        position: absolute;
        bottom: 28px;
        left: 24px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
        color: var(--color-gold);
    }
    .card-network {
        position: absolute;
        bottom: 24px;
        right: 24px;
        font-size: 18px;
        font-weight: 900;
        font-style: italic;
        color: rgba(255, 255, 255, 0.4);
    }
    .card-status-badge {
        position: absolute;
        top: 24px;
        left: 70px;
        font-size: 8px;
        font-weight: 900;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .card-active {
        background: rgba(16, 185, 129, 0.2);
        color: var(--color-emerald);
    }
    .card-frozen {
        background: rgba(99, 102, 241, 0.2);
        color: var(--color-cyan);
    }
    .card-controls {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .card-limits {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .limit-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .limit-label {
        font-size: 10px;
        font-weight: 700;
        color: var(--st-dim);
        min-width: 50px;
    }
    .limit-bar-wrap {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
        overflow: hidden;
    }
    .limit-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--st-accent), #a855f7);
        border-radius: 3px;
        transition: width 0.5s;
    }
    .limit-text {
        font-size: 10px;
        font-weight: 700;
        color: var(--st-dim);
        min-width: 120px;
        text-align: right;
    }
    .card-stats-row {
        display: flex;
        gap: 12px;
    }
    .card-stat {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 8px;
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 8px;
        font-size: 10px;
    }
    .card-stat span:first-child {
        color: var(--st-dim);
        font-weight: 600;
    }
    .cs-val {
        font-weight: 800;
    }
    .freeze-btn {
        padding: 10px;
        border: 1px solid var(--st-border);
        border-radius: 10px;
        background: rgba(99, 102, 241, 0.1);
        color: var(--st-text);
        font-weight: 700;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .freeze-btn:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: var(--st-accent);
    }
    .card-txns h4 {
        margin: 0 0 8px;
        font-size: 12px;
        font-weight: 700;
        color: var(--st-dim);
    }
    .card-tx-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        font-size: 12px;
    }
    .ctx-merchant {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .ctx-flag {
        font-size: 14px;
    }
    .ctx-name {
        font-weight: 600;
    }
    .ctx-amount {
        font-weight: 700;
        color: var(--color-rose);
    }
    .ctx-cashback {
        font-weight: 700;
        color: var(--color-emerald);
        font-size: 10px;
    }

    /* ═══ RAMP TAB ═══ */
    .ramp-panel {
        display: flex;
        flex-direction: column;
        gap: 14px;
    }
    .ramp-panel h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 800;
    }
    .ramp-toggle {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4px;
    }
    .ramp-dir {
        padding: 10px;
        border: 1px solid var(--st-border);
        border-radius: 8px;
        background: transparent;
        color: var(--st-dim);
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
    }
    .ramp-dir.active {
        background: rgba(99, 102, 241, 0.2);
        color: white;
        border-color: var(--st-accent);
    }
    .ramp-form {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .ramp-input-row {
        display: flex;
        gap: 8px;
    }
    .ramp-input-row .field-input {
        flex: 1;
    }
    .ramp-select {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid var(--st-border);
        border-radius: 8px;
        padding: 8px;
        color: white;
        font-weight: 700;
        min-width: 80px;
    }
    .ramp-arrow {
        text-align: center;
        font-size: 20px;
        color: var(--st-dim);
    }
    .ramp-methods h4 {
        margin: 0 0 8px;
        font-size: 11px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
    }
    .method-grid {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }
    .method-chip {
        padding: 6px 12px;
        border: 1px solid var(--st-border);
        border-radius: 8px;
        background: var(--st-card);
        color: var(--st-text);
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s;
    }
    .method-chip:hover {
        border-color: var(--st-accent);
    }

    /* ═══ AGENTS TAB ═══ */
    .agents-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }
    .agents-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 800;
    }
    .agents-count {
        font-size: 11px;
        font-weight: 700;
        color: var(--st-dim);
        padding: 4px 12px;
        background: var(--st-card);
        border-radius: 8px;
        border: 1px solid var(--st-border);
    }
    .agents-grid {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .agent-card {
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 14px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        transition: border-color 0.2s;
    }
    .agent-card.agent-active {
        border-left: 3px solid var(--color-emerald);
    }
    .agent-card.agent-paused {
        border-left: 3px solid var(--color-amber);
        opacity: 0.7;
    }
    .agent-header-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    .agent-name {
        margin: 0;
        font-size: 14px;
        font-weight: 700;
    }
    .agent-strategy {
        font-size: 10px;
        font-weight: 700;
        color: var(--color-cyan);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .agent-toggle {
        padding: 5px 12px;
        border: 1px solid var(--st-border);
        border-radius: 6px;
        background: transparent;
        color: var(--st-text);
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s;
    }
    .agent-toggle:hover {
        border-color: var(--st-accent);
        background: rgba(99, 102, 241, 0.1);
    }
    .agent-perf {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
    }
    .perf-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .perf-label {
        font-size: 9px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
    }
    .perf-value {
        font-size: 13px;
        font-weight: 800;
        font-variant-numeric: tabular-nums;
    }
    .perf-value.positive {
        color: var(--color-emerald);
    }
    .perf-value.negative {
        color: var(--color-rose);
    }
    .agent-last-action {
        font-size: 11px;
        padding: 6px 8px;
        background: rgba(0, 0, 0, 0.25);
        border-radius: 6px;
    }
    .ala-label {
        font-weight: 700;
        color: var(--st-dim);
    }
    .ala-text {
        color: var(--st-text);
    }
    .agent-risk-row {
        display: flex;
        gap: 12px;
        font-size: 10px;
        color: var(--st-dim);
        font-weight: 600;
    }

    /* ═══ YIELD TAB ═══ */
    .yield-panel {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .yield-hero {
        text-align: center;
        padding: 24px;
        background: linear-gradient(
            135deg,
            rgba(16, 185, 129, 0.1),
            rgba(99, 102, 241, 0.1)
        );
        border-radius: 16px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .apy-label {
        display: block;
        font-size: 11px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .apy-value {
        display: block;
        font-size: 36px;
        font-weight: 900;
        color: var(--color-emerald);
    }
    .apy-source {
        display: block;
        font-size: 11px;
        color: var(--st-dim);
        margin-top: 4px;
    }
    .yield-details {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    .yield-stat {
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 10px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .ys-label {
        font-size: 10px;
        font-weight: 700;
        color: var(--st-dim);
        text-transform: uppercase;
    }
    .ys-value {
        font-size: 16px;
        font-weight: 800;
    }
    .yield-audit {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 12px;
        background: var(--st-card);
        border: 1px solid var(--st-border);
        border-radius: 10px;
    }
    .audit-badge {
        font-size: 13px;
        font-weight: 700;
    }
    .audit-badge.audit-verified {
        color: var(--color-emerald);
    }
    .audit-date {
        font-size: 11px;
        color: var(--st-dim);
    }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 768px) {
        .terminal-header {
            flex-direction: column;
            gap: 8px;
        }
        .header-stats {
            flex-wrap: wrap;
        }
        .trade-grid {
            grid-template-columns: 1fr;
        }
        .predict-grid {
            grid-template-columns: 1fr;
        }
        .agent-perf {
            grid-template-columns: repeat(2, 1fr);
        }
        .yield-details {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    /* ═══ SCROLLBAR ═══ */
    .tab-content::-webkit-scrollbar {
        width: 4px;
    }
    .tab-content::-webkit-scrollbar-thumb {
        background: var(--st-accent);
        border-radius: 4px;
    }
</style>
