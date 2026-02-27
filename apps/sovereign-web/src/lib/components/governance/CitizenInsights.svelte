<script lang="ts">
    import { Users, Eye } from "lucide-svelte";

    // Privacy-preserving demographic data
    const aggregates = {
        totalVoters: 145020,
        engagementRate: 0.65,
        regionalDistribution: [
            { region: "NA", weight: 0.35 },
            { region: "EU", weight: 0.4 },
            { region: "APAC", weight: 0.2 },
            { region: "LATAM", weight: 0.05 },
        ],
    };
</script>

<div class="insights-card">
    <header class="card-header">
        <Users size={16} class="text-cyan-400" />
        <h3 class="title">Citizen Insights</h3>
    </header>

    <div class="card-body">
        <div class="kpi-row">
            <div class="kpi-item">
                <span class="label">Total Voters</span>
                <span class="value"
                    >{aggregates.totalVoters.toLocaleString()}</span
                >
            </div>
            <div class="kpi-item text-right">
                <span class="label">Engagement</span>
                <span class="value text-emerald-400"
                    >{(aggregates.engagementRate * 100).toFixed(1)}%</span
                >
            </div>
        </div>

        <div class="regions">
            <h4 class="sub-title">Regional Distribution</h4>
            {#each aggregates.regionalDistribution as reg}
                <div class="region-bar">
                    <span class="reg-name">{reg.region}</span>
                    <div class="bar-outer">
                        <div
                            class="bar-inner"
                            style:width="{reg.weight * 100}%"
                        ></div>
                    </div>
                    <span class="reg-val">{(reg.weight * 100).toFixed(0)}%</span
                    >
                </div>
            {/each}
        </div>

        <div class="privacy-note">
            <Eye size={12} class="text-emerald-400" />
            <span
                >Differential Privacy Enabled. Individual actors cannot be
                deanonymized.</span
            >
        </div>
    </div>
</div>

<style>
    .insights-card {
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
    .kpi-row {
        display: flex;
        justify-content: space-between;
    }
    .label {
        font-size: 7px;
        font-weight: 800;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        display: block;
        margin-bottom: 0.25rem;
    }
    .value {
        font-size: 18px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }
    .sub-title {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .region-bar {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .reg-name {
        width: 32px;
        font-size: 9px;
        font-weight: 800;
        color: white;
    }
    .bar-outer {
        flex: 1;
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .bar-inner {
        height: 100%;
        background: #22d3ee;
    }
    .reg-val {
        width: 32px;
        font-size: 9px;
        text-align: right;
        color: rgba(255, 255, 255, 0.4);
        font-family: "JetBrains Mono";
    }

    .privacy-note {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        background: rgba(16, 185, 129, 0.05);
        border-radius: 8px;
        font-size: 8px;
        color: #10b981;
        text-transform: uppercase;
        font-weight: 800;
    }
</style>
