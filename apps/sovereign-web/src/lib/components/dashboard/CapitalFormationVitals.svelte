<script lang="ts">
    import { fly, fade } from "svelte/transition";

    export let metrics = {
        aetherSales: 8470,
        aetherRaised: "$12.4B",
        liquifiValue: "$47.2B",
        rwaValue: "$47.2B",
        verifiedInvestors: "1.2M",
    };
</script>

<div class="capital-vitals" in:fly={{ y: 20, duration: 500 }}>
    <div class="vitals-header">
        <h2 class="section-title">
            <span class="section-icon">🏛️</span>
            Capital Formation
        </h2>
        <span class="status-badge">CAPITAL_ACTIVE</span>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <span class="metric-label">Aether Raised</span>
            <span class="metric-value">{metrics.aetherRaised}</span>
            <span class="metric-sub">{metrics.aetherSales} Token Sales</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Liquifi Value</span>
            <span class="metric-value">{metrics.liquifiValue}</span>
            <span class="metric-sub">Cap Table Managed</span>
        </div>
        <div class="metric-card highlighted">
            <span class="metric-label">RWA Tokenized</span>
            <span class="metric-value">{metrics.rwaValue}</span>
            <span class="metric-sub">Real Estate & Infrastructure</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Verified Citizens</span>
            <span class="metric-value">{metrics.verifiedInvestors}</span>
            <span class="metric-sub">Reusable Identity</span>
        </div>
    </div>
</div>

<style>
    .capital-vitals {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .vitals-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
        color: white;
    }

    .section-icon {
        font-size: 1.5rem;
    }

    .status-badge {
        padding: 0.25rem 0.75rem;
        background: rgba(78, 205, 196, 0.2);
        color: #4ecdc4;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05rem;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
    }

    .metric-card {
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .metric-card.highlighted {
        background: rgba(147, 112, 219, 0.1);
        border-color: rgba(147, 112, 219, 0.2);
    }

    .metric-card.highlighted .metric-value {
        color: #9370db;
    }

    .metric-label {
        font-size: 0.8rem;
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4ecdc4;
    }

    .metric-sub {
        font-size: 0.75rem;
        opacity: 0.5;
    }
</style>
