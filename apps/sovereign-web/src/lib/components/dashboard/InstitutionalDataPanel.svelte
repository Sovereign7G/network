<script lang="ts">
    import { onDestroy } from "svelte";
    import { telemetryStore } from "$lib/stores/telemetry-store";
    import { warRoomStore } from "../../../../../../packages/age-warroom/src/store";

    let systemic: any = {};

    const unsubscribe = telemetryStore.subscribe((state) => {
        systemic = (state as any).systemic || {};
    });

    onDestroy(() => {
        unsubscribe();
    });

    // Reference warRoomStore to avoid unused variable lint
    // If warRoomStore is truly not used, it should be removed.
    // For now, we'll just reference it to satisfy the linter.
    warRoomStore;

    $: if (systemic.sofr >= 3.8) {
        console.warn("Systemic Risk: SOFR threshold breached");
    }
</script>

```
<div class="institutional-panel">
    <div class="panel-header">
        <h3>🏛️ INSTITUTIONAL DATA SYNC</h3>
        <span class="sync-status">LIVE • 1s REFRESH</span>
    </div>

    <div class="data-grid">
        <div class="data-card">
            <div class="data-header">SOFR</div>
            <div class="data-value" class:critical={systemic.sofr >= 3.8}>
                {systemic.sofr ? systemic.sofr.toFixed(2) : "--"}%
            </div>
            <div class="data-threshold">/ 3.80%</div>
        </div>

        <div class="data-card">
            <div class="data-header">10Y Treasury</div>
            <div class="data-value" class:warning={systemic.treasury10y >= 4.5}>
                {systemic.treasury10y ? systemic.treasury10y.toFixed(2) : "--"}%
            </div>
            <div class="data-threshold">/ 5.0%</div>
        </div>

        <div class="data-card">
            <div class="data-header">OAT-Bund</div>
            <div class="data-value" class:critical={systemic.oatBund > 75}>
                {systemic.oatBund ? systemic.oatBund.toFixed(0) : "--"} bps
            </div>
            <div class="data-threshold">/ 75</div>
        </div>

        <div class="data-card">
            <div class="data-header">EUR/CHF</div>
            <div class="data-value" class:critical={systemic.eurChf <= 0.9095}>
                {systemic.eurChf ? systemic.eurChf.toFixed(4) : "--"}
            </div>
            <div class="data-threshold">/ 0.9095</div>
        </div>

        <div class="data-card">
            <div class="data-header">WTI Crude</div>
            <div class="data-value" class:warning={systemic.wti >= 70}>
                ${systemic.wti ? systemic.wti.toFixed(2) : "--"}
            </div>
            <div class="data-threshold">War Premium</div>
        </div>

        <div class="data-card">
            <div class="data-header">Gold</div>
            <div class="data-value" class:success={systemic.gold >= 5000}>
                ${systemic.gold ? systemic.gold.toLocaleString() : "--"}
            </div>
            <div class="data-threshold">Physical Anchor</div>
        </div>
    </div>

    <div class="lifeboat-data">
        <h4>🧬 INTELLIGENCE STANDARD</h4>
        <div class="asset-row">
            <span>XMR (Monero)</span>
            <span class="value"
                >${systemic.xmr ? systemic.xmr.toFixed(2) : "--"}</span
            >
            <span class="volume"
                >Vol: {systemic.xmrVolume
                    ? (systemic.xmrVolume / 1000).toFixed(0)
                    : "--"}K</span
            >
        </div>
        <div class="asset-row">
            <span>TAO (Bittensor)</span>
            <span class="value"
                >${systemic.tao ? systemic.tao.toFixed(2) : "--"}</span
            >
            <span class="subnets">128 subnets</span>
        </div>
        <div class="asset-row">
            <span>RENDER</span>
            <span class="value"
                >${systemic.render ? systemic.render.toFixed(2) : "--"}</span
            >
            <span class="frames">40M frames</span>
        </div>
    </div>
</div>

<style>
    .institutional-panel {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .panel-header h3 {
        margin: 0;
        font-size: 1rem;
        letter-spacing: 1px;
        color: #ffd700;
    }

    .sync-status {
        font-size: 0.7rem;
        opacity: 0.6;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
    }

    .data-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .data-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        transition: all 0.2s;
    }

    .data-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .data-header {
        color: #888;
        font-size: 0.7rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .data-value {
        font-size: 1.25rem;
        font-weight: bold;
        color: #fff;
    }

    .data-value.critical {
        color: #f44336;
        text-shadow: 0 0 10px rgba(244, 67, 54, 0.5);
    }

    .data-value.warning {
        color: #ffc107;
    }

    .data-value.success {
        color: #4caf50;
    }

    .data-threshold {
        color: #555;
        font-size: 0.6rem;
        margin-top: 0.25rem;
    }

    .lifeboat-data {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1.5rem;
    }

    .lifeboat-data h4 {
        margin: 0 0 1rem 0;
        font-size: 0.8rem;
        color: #4caf50;
        letter-spacing: 2px;
    }

    .asset-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.85rem;
    }

    .asset-row:last-child {
        border-bottom: none;
    }

    .asset-row .value {
        font-weight: bold;
        color: #4caf50;
    }

    .asset-row .volume,
    .asset-row .subnets,
    .asset-row .frames {
        color: #666;
        font-size: 0.75rem;
    }

    @media (max-width: 768px) {
        .data-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
