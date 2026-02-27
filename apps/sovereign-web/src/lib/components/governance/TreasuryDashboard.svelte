<script lang="ts">
    import { Wallet, ArrowUpRight } from "lucide-svelte";

    const treasuryData = {
        totalValueUSD: 1450250000,
        availableUSD: 245000000,
        runwayMonths: 48,
        allocations: [
            { id: "core", name: "Core Protocol", value: 45, color: "#10b981" },
            {
                id: "grants",
                name: "Ecosystem Grants",
                value: 30,
                color: "#3b82f6",
            },
            {
                id: "reserves",
                name: "Strategic Reserves",
                value: 15,
                color: "#6366f1",
            },
            {
                id: "validators",
                name: "Validator Incentives",
                value: 10,
                color: "#f59e0b",
            },
        ],
    };

    function formatCurrency(amount: number) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            notation: "compact",
            maximumFractionDigits: 1,
        }).format(amount);
    }
</script>

<div class="treasury-card">
    <header class="card-header">
        <Wallet size={16} class="text-amber-400" />
        <h3 class="title">Treasury Dashboard</h3>
    </header>

    <div class="card-body">
        <div class="kpi-group">
            <span class="label">Total AUM</span>
            <span class="value main"
                >{formatCurrency(treasuryData.totalValueUSD)}</span
            >
            <div class="trend positive">
                <ArrowUpRight size={10} />
                <span>+4.2% (30d)</span>
            </div>
        </div>

        <div class="split-kpi">
            <div class="kpi-box">
                <span class="label">Liquid Runway</span>
                <span class="value">{treasuryData.runwayMonths} Mo</span>
            </div>
            <div class="kpi-box text-right">
                <span class="label">Available Capital</span>
                <span class="value text-emerald-400"
                    >{formatCurrency(treasuryData.availableUSD)}</span
                >
            </div>
        </div>

        <div class="allocations">
            <div class="alloc-bar">
                {#each treasuryData.allocations as alloc}
                    <div
                        class="alloc-segment"
                        style="width: {alloc.value}%; background: {alloc.color};"
                    >
                        <div class="tooltip">{alloc.name}: {alloc.value}%</div>
                    </div>
                {/each}
            </div>

            <div class="alloc-legend">
                {#each treasuryData.allocations as alloc}
                    <div class="legend-item">
                        <div
                            class="dot"
                            style="background: {alloc.color};"
                        ></div>
                        <span>{alloc.name} ({alloc.value}%)</span>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .treasury-card {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        overflow: hidden;
        font-family: "Outfit", sans-serif;
    }
    .card-header {
        padding: 1.25rem 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .title {
        font-size: 11px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
    }
    .card-body {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .kpi-group {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .label {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        letter-spacing: 0.1em;
    }
    .value.main {
        font-size: 28px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }
    .value {
        font-size: 14px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .trend {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 9px;
        font-weight: 800;
        margin-top: 0.25rem;
    }
    .trend.positive {
        color: #10b981;
    }

    .split-kpi {
        display: flex;
        justify-content: space-between;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .alloc-bar {
        height: 12px;
        display: flex;
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .alloc-segment {
        height: 100%;
        position: relative;
    }
    .alloc-segment .tooltip {
        position: absolute;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        background: black;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 8px;
        font-weight: 800;
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
    }
    .alloc-segment:hover .tooltip {
        opacity: 1;
    }

    .alloc-legend {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 9px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
    }
    .dot {
        width: 8px;
        height: 8px;
        border-radius: 2px;
    }
</style>
