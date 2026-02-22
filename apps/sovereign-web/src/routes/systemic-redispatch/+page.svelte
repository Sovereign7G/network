<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import SeizureDashboard from "$lib/components/dashboard/SeizureDashboard.svelte";
    import March31Countdown from "$lib/components/dashboard/March31Countdown.svelte";
    import ArithmeticVitals from "$lib/components/dashboard/ArithmeticVitals.svelte";

    let timestamp = new Date().toISOString();

    onMount(() => {
        const interval = setInterval(() => {
            timestamp = new Date().toISOString();
        }, 1000);
        return () => clearInterval(interval);
    });
</script>

<svelte:head>
    <title>Systemic Redispatch | AGE Protocol</title>
</svelte:head>

<div class="systemic-view" in:fade>
    <div class="hero">
        <div class="top-nav">
            <span class="breadcrumb">Cathedral / Intelligence Standard</span>
            <span class="live-clock">{timestamp}</span>
        </div>
        <h1>🏛️ SYSTEMIC REDISPATCH 2026</h1>
        <p class="subtitle">From Analog Collapse to Intelligence Standard</p>
    </div>

    <div class="verdict-banner">
        <div class="quote">
            "The 'Moral' system is being liquidated to pay for the 'Physical'
            reality. Trust is dead. Work is the new standard."
        </div>
        <div class="attribution">— The Architects</div>
    </div>

    <div class="dashboard-grid">
        <div class="main-column">
            <SeizureDashboard />

            <div class="pillar-grid">
                <div class="pillar-card red">
                    <h3>🔴 PILLAR I</h3>
                    <p>
                        Analog Collapse: US Debt Wall ($11T), Japan
                        Repatriation, Basis Trade Unwind ($1.4T).
                    </p>
                </div>
                <div class="pillar-card yellow">
                    <h3>🟡 PILLAR II</h3>
                    <p>
                        Geopolitical Accelerant: USS Ford Deployment, WTI Crude
                        $67, Iran Enclosure.
                    </p>
                </div>
                <div class="pillar-card green">
                    <h3>🟢 PILLAR III</h3>
                    <p>
                        Intelligence Standard: TAO (Intelligence Reserve),
                        RENDER (Compute), XMR (Privacy Lifeboat).
                    </p>
                </div>
            </div>
        </div>

        <div class="side-column">
            <March31Countdown />
            <ArithmeticVitals />

            <div class="trigger-sequence-card">
                <h4>⚡ TRIGGER SEQUENCE</h4>
                <ul class="sequence">
                    <li>Repo 3.80% Seizure</li>
                    <li class="arr">↓</li>
                    <li>Hedge Fund Liquidation</li>
                    <li class="arr">↓</li>
                    <li>Bond Market Seizure</li>
                    <li class="arr">↓</li>
                    <li class="final">Intelligence Standard Breakout</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<style>
    .systemic-view {
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        color: white;
        background: radial-gradient(
            circle at top right,
            rgba(76, 175, 80, 0.05),
            transparent 600px
        );
    }

    .hero {
        margin-bottom: 3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 2rem;
    }

    .top-nav {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
    }
    .live-clock {
        font-family: monospace;
    }

    .hero h1 {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.5rem;
    }

    .verdict-banner {
        background: rgba(255, 62, 62, 0.03);
        border: 1px solid rgba(255, 62, 62, 0.1);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 3rem;
    }

    .quote {
        font-size: 1.5rem;
        font-style: italic;
        color: #ff3e3e;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .attribution {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.3);
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 380px;
        gap: 2rem;
    }

    .main-column {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    .side-column {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .pillar-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }

    .pillar-card {
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
    }

    .pillar-card h3 {
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .pillar-card p {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        margin: 0;
        line-height: 1.5;
    }

    .pillar-card.red h3 {
        color: #ff3e3e;
    }
    .pillar-card.yellow h3 {
        color: #ffa500;
    }
    .pillar-card.green h3 {
        color: #00ffcc;
    }

    .trigger-sequence-card {
        padding: 1.5rem;
        background: rgba(13, 13, 15, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
    }

    .trigger-sequence-card h4 {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .sequence {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    .sequence li {
        font-size: 0.9rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 0.5rem;
        width: 100%;
        text-align: center;
    }
    .arr {
        background: none !important;
        color: rgba(255, 255, 255, 0.2) !important;
        padding: 0 !important;
    }
    .final {
        background: #00ffcc22 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc44;
    }

    @media (max-width: 1024px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        .side-column {
            flex-direction: row;
            flex-wrap: wrap;
        }
        .side-column > * {
            flex: 1;
            min-width: 300px;
        }
    }
</style>
