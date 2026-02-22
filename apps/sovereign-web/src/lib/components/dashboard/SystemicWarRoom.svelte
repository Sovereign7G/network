<script lang="ts">
    import { onMount } from "svelte";
    import { createSonicSovereignty } from "../../../../../../packages/age-sensory/src/index";
    import { pillars } from "../../../../../../packages/age-warroom/src/pillars/pillar-tracker";
    import { SovereignMoat } from "../../../../../../packages/age-warroom/src/moat/moat-trigger";
    import { lifeboatWeights } from "../../../../../../packages/age-warroom/src/lifeboat/weights";
    import { vaultStore } from "$lib/stores/vault-store";

    let moatActive = false;
    let weights: any[] = [];

    const moat = SovereignMoat.getInstance();

    onMount(() => {
        const unsubscribe = moat.subscribe((active) => {
            moatActive = active;
        });

        const vaultUnsub = vaultStore.subscribe((v) => {
            // Use balances from vaultStore
            const holdings = {
                gold: v.balances["GOLD"] || 2000,
                xmr: v.balances["XMR"] || 3000,
                tao: v.balances["TAO"] || 2500,
                render: v.balances["RENDER"] || 2500,
            };
            weights = lifeboatWeights.calculateWeights(holdings);
        });

        return () => {
            unsubscribe();
            vaultUnsub();
        };
    });
</script>

<div class="war-room" class:emergency={moatActive}>
    <div class="header">
        <h2>🚨 SYSTEMIC WAR ROOM</h2>
        {#if moatActive}
            <div class="moat-badge">🛡️ SOVEREIGN MOAT ACTIVE</div>
        {:else}
            <div class="status-badge">🟢 MONITORING PILOT</div>
        {/if}
    </div>

    <div class="pillar-grid">
        {#each pillars as pillar}
            <div class="pillar" style="border-top: 4px solid {pillar.color}">
                <div class="pillar-header">
                    <span class="pillar-name">{pillar.name}</span>
                </div>
                <div class="metrics">
                    {#each pillar.metrics as metric}
                        <div class="metric">
                            <span class="m-name">{metric.name}</span>
                            <div class="m-data">
                                <span
                                    class="m-value"
                                    class:critical={metric.status ===
                                        "CRITICAL"}
                                    class:warning={metric.status === "WARNING"}
                                >
                                    {metric.value}{metric.unit}
                                </span>
                                <span class="m-threshold"
                                    >/{metric.threshold}{metric.unit}</span
                                >
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>

    <div class="lifeboat-section">
        <div class="lb-header">
            <h3>🧬 LIFEBOAT WEIGHTS</h3>
            <span class="intel">INTELLIGENCE STANDARD ALLOCATION</span>
        </div>

        <div class="allocation-grid">
            {#each weights as asset}
                <div class="asset-card">
                    <div class="asset-info">
                        <span class="symbol">{asset.symbol}</span>
                        <span class="name">{asset.name}</span>
                    </div>
                    <div class="bar-wrap">
                        <div class="bar-bg">
                            <div
                                class="bar-fill"
                                style="width: {asset.currentAllocation}%; background: {asset.color}"
                            ></div>
                            <div
                                class="target-line"
                                style="left: {asset.targetAllocation}%"
                            ></div>
                        </div>
                    </div>
                    <div class="asset-vals">
                        <span class="current"
                            >{asset.currentAllocation?.toFixed(1)}%</span
                        >
                        <span class="target"
                            >Target {asset.targetAllocation}%</span
                        >
                    </div>
                    {#if asset.rebalanceNeeded}
                        <div class="rebalance-alert">REBALANCE REQ</div>
                    {/if}
                </div>
            {/each}
        </div>
    </div>

    <div class="trigger-path">
        <h3>⚡ RESET TRIGGER SEQUENCE</h3>
        <div class="steps">
            <div class="step">SOFR 3.80%</div>
            <div class="arrow">→</div>
            <div class="step">Basis Trade Liquidation</div>
            <div class="arrow">→</div>
            <div class="step">Bond Moat Activation</div>
            <div class="arrow">→</div>
            <div class="step highlight">INTELLIGENCE STANDARD</div>
        </div>
    </div>
</div>

<style>
    .war-room {
        background: rgba(10, 10, 15, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .war-room.emergency {
        background: rgba(40, 10, 10, 0.9);
        border-color: #ff3e00;
        box-shadow: 0 0 40px rgba(255, 62, 0, 0.2);
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    h2 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 800;
    }

    .moat-badge {
        background: #ff3e00;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        animation: flash 1s infinite;
    }

    .status-badge {
        background: rgba(0, 255, 204, 0.1);
        color: #00ffcc;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid #00ffcc;
    }

    .pillar-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
    }

    .pillar {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border-radius: 12px;
    }

    .pillar-name {
        font-size: 0.85rem;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.7);
    }

    .metrics {
        margin-top: 1rem;
    }

    .metric {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.8rem;
    }

    .m-name {
        color: rgba(255, 255, 255, 0.5);
    }
    .m-value.critical {
        color: #ff3e00;
        font-weight: bold;
    }
    .m-value.warning {
        color: #ffcc00;
    }
    .m-threshold {
        color: rgba(255, 255, 255, 0.2);
        margin-left: 0.25rem;
    }

    .lifeboat-section {
        background: rgba(255, 255, 255, 0.02);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }

    .lb-header {
        margin-bottom: 1.5rem;
    }
    .lb-header h3 {
        margin: 0;
        font-size: 1rem;
    }
    .intel {
        font-size: 0.7rem;
        color: #00ffcc;
        opacity: 0.8;
    }

    .allocation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }

    .asset-card {
        position: relative;
    }

    .asset-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .symbol {
        font-size: 1.25rem;
    }
    .name {
        font-weight: 700;
        font-size: 0.85rem;
    }

    .bar-wrap {
        height: 8px;
        margin: 1rem 0;
    }
    .bar-bg {
        height: 100%;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        position: relative;
    }
    .bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .target-line {
        position: absolute;
        top: -4px;
        height: 16px;
        width: 2px;
        background: white;
        transform: translateX(-50%);
    }

    .asset-vals {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
    }
    .current {
        color: #00ffcc;
        font-weight: bold;
    }
    .target {
        color: rgba(255, 255, 255, 0.4);
    }

    .rebalance-alert {
        position: absolute;
        top: -0.5rem;
        right: 0;
        font-size: 0.6rem;
        background: #ffcc00;
        color: black;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }

    .trigger-path {
        text-align: center;
        padding: 1.5rem;
        border-top: 1px dashed rgba(255, 255, 255, 0.1);
    }
    .trigger-path h3 {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 1rem;
    }
    .steps {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
    }
    .step {
        font-size: 0.7rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
    }
    .step.highlight {
        background: #00ffcc;
        color: black;
        font-weight: bold;
    }
    .arrow {
        color: rgba(255, 255, 255, 0.2);
    }

    @keyframes flash {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
</style>
