<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import {
        Coins,
        TrendingUp,
        BarChart3,
        Activity,
        ArrowUpRight,
        Layers,
        ShieldCheck,
    } from "lucide-svelte";

    const tokenomics = $derived(manifold.tokenomicsState);
</script>

<div class="tokenomics-shell">
    <!-- Institutional Header -->
    <header class="tokenomics-header">
        <div class="header-brand">
            <div class="logo-box">
                <Coins size={20} class="text-black" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Tokenomics</h2>
                <div class="flex items-center gap-2">
                    <span class="plane-label">Protocol_Asset_Plane</span>
                    <div class="plane-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry text-right">
            <span class="tel-label">MARKET_CAPITALIZATION</span>
            <div class="flex items-center gap-2 justify-end">
                <span class="tel-value italic"
                    >${(tokenomics.marketCapUsd / 1000000000).toFixed(2)}B</span
                >
                <ArrowUpRight size={12} class="text-emerald-400" />
            </div>
        </div>
    </header>

    <div class="tokenomics-body scrollbar-hide">
        <!-- Ambient Asset Aura -->
        <div class="asset-aura"></div>

        <!-- High-Assurance Metrics Grid -->
        <div class="metrics-grid">
            <section
                class="metric-card gold-tint"
                in:fly={{ y: 20, duration: 600, easing: cubicOut }}
            >
                <header class="card-header">
                    <TrendingUp size={14} class="text-amber-400" />
                    <h3>ARI_Multiplier</h3>
                </header>
                <div class="card-content">
                    <span class="value"
                        >{tokenomics.ariMultiplier.toFixed(3)}x</span
                    >
                    <p class="description">
                        Anti-Rival Incentive scaling based on Global Reputation.
                    </p>
                </div>
            </section>

            <section
                class="metric-card emerald-tint"
                in:fly={{ y: 20, delay: 100, duration: 600, easing: cubicOut }}
            >
                <header class="card-header">
                    <Activity size={14} class="text-emerald-400" />
                    <h3>Daily_UCT_Yield</h3>
                </header>
                <div class="card-content">
                    <span class="value"
                        >{tokenomics.uctDailyDividend.toFixed(1)}
                        <small>CR</small></span
                    >
                    <p class="description">
                        Residual Harmony Dividend baseline at current resonance.
                    </p>
                </div>
            </section>
        </div>

        <!-- Systemic Allocation Registry -->
        <section
            class="allocation-vessel"
            in:fade={{ delay: 300, duration: 800 }}
        >
            <header class="vessel-header">
                <Layers size={12} class="text-white/40" />
                <h3>Systemic_Allocation</h3>
            </header>

            <div class="vessel-list">
                <div class="allocation-item">
                    <div class="item-meta">
                        <div class="indicator bg-cyan-400"></div>
                        <span class="label">$AGE_Circulating</span>
                    </div>
                    <span class="value"
                        >{(tokenomics.ageCirculating / 1000000).toFixed(
                            0,
                        )}M</span
                    >
                </div>

                <div class="allocation-item">
                    <div class="item-meta">
                        <div class="indicator bg-white/40"></div>
                        <span class="label">Reputation_Index_(RI)</span>
                    </div>
                    <span class="value">{tokenomics.reputationIndex}</span>
                </div>

                <div class="allocation-item">
                    <div class="item-meta">
                        <div class="indicator bg-amber-400"></div>
                        <span class="label">Inherent_Buffer</span>
                    </div>
                    <span class="value">0xAA_ACTIVE</span>
                </div>
            </div>
        </section>
    </div>

    <!-- Assurance Footer -->
    <footer class="tokenomics-footer">
        <div class="assurance-block">
            <ShieldCheck size={14} class="text-emerald-400" />
            <span class="a-label">CONSERVATION: PASS</span>
        </div>
        <div class="audit-badge">
            <BarChart3 size={12} />
            <span>Audit_Checksum_Verified</span>
        </div>
    </footer>
</div>

<style>
    .tokenomics-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
    }

    .tokenomics-header {
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .logo-box {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(251, 191, 36, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .plane-label {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .plane-pulsar {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #fbbf24;
        box-shadow: 0 0 10px #fbbf24;
        animation: pulse 1s infinite;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.2em;
        margin-bottom: 2px;
        display: block;
    }

    .tel-value {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .tokenomics-body {
        flex: 1;
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 2.5rem;
        position: relative;
        overflow-y: auto;
    }

    .asset-aura {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at top right,
            rgba(251, 191, 36, 0.05),
            transparent 60%
        );
        pointer-events: none;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        padding: 1.75rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .metric-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .card-header h3 {
        font-size: 9px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .card-content .value {
        display: block;
        font-size: 28px;
        font-weight: 950;
        color: white;
        letter-spacing: -0.02em;
        margin-bottom: 0.75rem;
    }

    .card-content .value small {
        font-size: 14px;
        opacity: 0.4;
        font-weight: 900;
    }

    .description {
        font-size: 8px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        line-height: 1.6;
        letter-spacing: 0.05em;
    }

    .gold-tint:hover {
        border-color: rgba(251, 191, 36, 0.2);
    }
    .emerald-tint:hover {
        border-color: rgba(16, 185, 129, 0.2);
    }

    .allocation-vessel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        padding: 1.75rem;
    }

    .vessel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .vessel-header h3 {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }

    .vessel-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .allocation-item {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.03);
        padding: 1rem 1.25rem;
        border-radius: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s;
    }

    .allocation-item:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.08);
    }

    .item-meta {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .indicator {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }

    .label {
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .allocation-item .value {
        font-size: 11px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .tokenomics-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .assurance-block {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .a-label {
        font-size: 8px;
        font-weight: 950;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .audit-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
