<script lang="ts">
    import { fade, fly } from "svelte/transition";
    import {
        Activity,
        Users,
        ShieldCheck,
        Zap,
        AlertTriangle,
        BarChart2,
    } from "lucide-svelte";

    // 100% Type-Safe Protocol Health Interface
    interface ProtocolHealthMetrics {
        resonance: {
            current: number;
            history: Array<{ date: string; value: number }>;
            trends: "improving" | "stable" | "declining";
        };
        transactions: {
            daily: number;
            weekly: number;
            monthly: number;
            total: number;
            volume: number;
        };
        citizens: {
            dau: number;
            wau: number;
            mau: number;
            growth: number;
            retention: number;
        };
        governance: {
            proposals: number;
            turnout: number;
            delegates: number;
            participation: number;
        };
        reliability: {
            successRate: number;
            errorRate: number;
            avgLatency: number;
            p95Latency: number;
        };
    }

    // Mock data for Phase 5 implementation
    const health: ProtocolHealthMetrics = {
        resonance: {
            current: 0.998,
            history: Array.from({ length: 30 }).map((_, i) => ({
                date:
                    new Date(Date.now() - (29 - i) * 86400000)
                        .toISOString()
                        .split("T")[0] || "",
                value: 0.95 + Math.random() * 0.04,
            })),
            trends: "improving",
        },
        transactions: {
            daily: 15420,
            weekly: 105800,
            monthly: 450200,
            total: 12500000,
            volume: 85400000,
        },
        citizens: {
            dau: 4200,
            wau: 18500,
            mau: 45000,
            growth: 0.12,
            retention: 0.88,
        },
        governance: {
            proposals: 14,
            turnout: 0.45,
            delegates: 156,
            participation: 0.62,
        },
        reliability: {
            successRate: 0.9995,
            errorRate: 0.0005,
            avgLatency: 124,
            p95Latency: 280,
        },
    };

    function formatNumber(num: number) {
        return new Intl.NumberFormat("en-US").format(num);
    }

    function formatPercentage(num: number) {
        return new Intl.NumberFormat("en-US", {
            style: "percent",
            maximumFractionDigits: 1,
        }).format(num);
    }
</script>

<div class="health-shell" in:fade>
    <div class="health-aura"></div>

    <header class="health-header">
        <div class="header-brand">
            <div class="icon-vessel">
                <Activity size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Protocol_Health</h2>
                <span class="subtitle">Systemic_Analytics_Engine</span>
            </div>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            <span>System_Nominal</span>
        </div>
    </header>

    <div class="health-body scrollbar-hide">
        <!-- Resonance Stratum -->
        <section class="metric-section">
            <header class="section-top">
                <h3>Systemic Resonance</h3>
                <span class="value highlight"
                    >{formatPercentage(health.resonance.current)}</span
                >
            </header>
            <div class="mini-chart">
                {#each health.resonance.history as point}
                    <div class="bar" style:height="{point.value * 100}%">
                        <div class="tooltip">
                            {point.date}: {point.value.toFixed(3)}
                        </div>
                    </div>
                {/each}
            </div>
        </section>

        <div class="grid-layout">
            <!-- Citizenship -->
            <div class="kpi-card group" in:fly={{ y: 20, delay: 100 }}>
                <Users
                    size={14}
                    class="text-cyan-400 mb-2 opacity-50 group-hover:opacity-100 transition-opacity"
                />
                <span class="kpi-label">Active Citizens (DAU)</span>
                <span class="kpi-value"
                    >{formatNumber(health.citizens.dau)}</span
                >
                <span class="kpi-delta positive"
                    >+{formatPercentage(health.citizens.growth)} Growth</span
                >
            </div>

            <!-- Reliability -->
            <div class="kpi-card group" in:fly={{ y: 20, delay: 150 }}>
                <ShieldCheck
                    size={14}
                    class="text-emerald-400 mb-2 opacity-50 group-hover:opacity-100 transition-opacity"
                />
                <span class="kpi-label">Uptime Reliability</span>
                <span class="kpi-value"
                    >{formatPercentage(health.reliability.successRate)}</span
                >
                <span class="kpi-delta"
                    >p95 Latency: {health.reliability.p95Latency}ms</span
                >
            </div>

            <!-- Volume -->
            <div class="kpi-card group" in:fly={{ y: 20, delay: 200 }}>
                <Zap
                    size={14}
                    class="text-amber-400 mb-2 opacity-50 group-hover:opacity-100 transition-opacity"
                />
                <span class="kpi-label">Daily Volume</span>
                <span class="kpi-value"
                    >${formatNumber(health.transactions.volume)}</span
                >
                <span class="kpi-delta"
                    >{formatNumber(health.transactions.daily)} TXs</span
                >
            </div>

            <!-- Governance -->
            <div class="kpi-card group" in:fly={{ y: 20, delay: 250 }}>
                <BarChart2
                    size={14}
                    class="text-indigo-400 mb-2 opacity-50 group-hover:opacity-100 transition-opacity"
                />
                <span class="kpi-label">Voter Turnout</span>
                <span class="kpi-value"
                    >{formatPercentage(health.governance.turnout)}</span
                >
                <span class="kpi-delta"
                    >{health.governance.delegates} Active Delegates</span
                >
            </div>
        </div>

        <!-- System Alerts / Health -->
        <div class="alerts-stratum">
            <h4 class="alerts-title">Metabolic Warnings</h4>
            {#if health.reliability.errorRate > 0.001}
                <div class="alert-box error">
                    <AlertTriangle size={14} />
                    <span
                        >Error rate exceeding threshold ({formatPercentage(
                            health.reliability.errorRate,
                        )})</span
                    >
                </div>
            {:else}
                <div class="alert-box success">
                    <ShieldCheck size={14} />
                    <span
                        >Zero anomalous deviations detected across 42 shards.</span
                    >
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .health-shell {
        height: 100%;
        background: rgba(10, 5, 20, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
        position: relative;
    }

    .health-aura {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at top right,
            rgba(34, 211, 238, 0.05) 0%,
            transparent 70%
        );
        pointer-events: none;
    }

    .health-header {
        padding: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
        background: rgba(0, 0, 0, 0.2);
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .icon-vessel {
        width: 40px;
        height: 40px;
        background: linear-gradient(
            135deg,
            rgba(34, 211, 238, 0.2),
            rgba(34, 211, 238, 0.05)
        );
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.1);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .subtitle {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .status-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 100px;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
        color: #10b981;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }

    .health-body {
        padding: 2rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        flex: 1;
    }

    .metric-section {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
    }

    .section-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .section-top h3 {
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        letter-spacing: 0.1em;
    }

    .value.highlight {
        font-size: 20px;
        font-weight: 950;
        color: #22d3ee;
        font-family: "JetBrains Mono", monospace;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
    }

    .mini-chart {
        height: 60px;
        display: flex;
        align-items: flex-end;
        gap: 4px;
        padding-top: 20px;
    }

    .bar {
        flex: 1;
        background: rgba(34, 211, 238, 0.4);
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-height: 4px;
        transition: all 0.3s ease;
        position: relative;
    }

    .bar:hover {
        background: #22d3ee;
    }

    .bar .tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.8);
        padding: 4px 8px;
        font-size: 8px;
        color: white;
        border-radius: 4px;
        pointer-events: none;
        opacity: 0;
        white-space: nowrap;
        margin-bottom: 4px;
    }

    .bar:hover .tooltip {
        opacity: 1;
    }

    .grid-layout {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .kpi-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        transition: all 0.3s;
    }

    .kpi-card:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .kpi-label {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        font-size: 16px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
        margin-bottom: 0.5rem;
    }

    .kpi-delta {
        font-size: 9px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.4);
    }

    .kpi-delta.positive {
        color: #10b981;
    }

    .alerts-stratum {
        margin-top: auto;
    }

    .alerts-title {
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
    }

    .alert-box {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.25rem;
        border-radius: 16px;
        font-size: 10px;
        font-weight: 800;
    }

    .alert-box.success {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed rgba(16, 185, 129, 0.2);
        color: #10b981;
    }

    .alert-box.error {
        background: rgba(244, 63, 94, 0.05);
        border: 1px dashed rgba(244, 63, 94, 0.2);
        color: #f43f5e;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
