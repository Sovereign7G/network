<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    // 🔵 PILLAR IV: MARKET MECHANICS (v20.1)
    export let sofr = 3.67;
    export let yield10y = 4.07;
    export let spread = 0.38;
    export let basisTrade = 1.4; // $1.4T

    $: status = sofr >= 3.8 ? "SEIZURE" : sofr >= 3.75 ? "CRITICAL" : "STABLE";
    $: alertColor =
        status === "SEIZURE"
            ? "#ff3e3e"
            : status === "CRITICAL"
              ? "#ffa500"
              : "#00ffcc";
</script>

<div class="seizure-dashboard" in:fade>
    <div class="header">
        <h2 style="color: {alertColor}">🧮 Systemic Redispatch</h2>
        <div
            class="badge"
            style="background: {alertColor}22; color: {alertColor}"
        >
            {status} ACTIVE
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <span class="label">Repo (SOFR)</span>
            <span class="value">{sofr.toFixed(2)}%</span>
            <div class="progress-container">
                <div
                    class="progress-bar"
                    style="width: {(sofr / 3.8) *
                        100}%; background: {alertColor}"
                ></div>
                <div class="trigger-mark" style="left: 100%"></div>
            </div>
            <span class="hint">Trigger: 3.80% (13 bps away)</span>
        </div>

        <div class="metric-card">
            <span class="label">10Y-3M Spread</span>
            <span class="value">+{spread.toFixed(2)}%</span>
            <span class="hint">Un-inversion phase active</span>
        </div>

        <div class="metric-card">
            <span class="label">10Y Yield</span>
            <span class="value">{yield10y.toFixed(2)}%</span>
            <span class="hint">Resistance at 4.5%</span>
        </div>

        <div class="metric-card">
            <span class="label">Basis Trade</span>
            <span class="value">${basisTrade}T</span>
            <span class="hint">Forced liquidation imminent</span>
        </div>
    </div>

    <div class="verdict">
        <p>"Trust is dead. Work is the new standard."</p>
    </div>
</div>

<style>
    .seizure-dashboard {
        background: rgba(13, 13, 15, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
        font-family: "Inter", sans-serif;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .header h2 {
        margin: 0;
        font-size: 1.4rem;
    }

    .badge {
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.05em;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1.5rem;
    }

    .metric-card {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
    }
    .value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #fff;
    }
    .hint {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
    }

    .progress-container {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        position: relative;
        margin: 0.5rem 0;
    }

    .progress-bar {
        height: 100%;
        border-radius: 2px;
        transition: width 0.3s;
    }
    .trigger-mark {
        position: absolute;
        height: 10px;
        width: 2px;
        background: #ff3e3e;
        top: -3px;
    }

    .verdict {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        font-style: italic;
        color: rgba(255, 255, 255, 0.4);
    }
</style>
