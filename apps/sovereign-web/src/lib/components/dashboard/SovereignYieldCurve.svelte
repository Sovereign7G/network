<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    export let primeRate = 12.4;
    export let layers = [
        {
            id: 1,
            name: "Identity/Security",
            contribution: 1.2,
            color: "#FF6B6B",
            source: "S-ID signatures",
        },
        {
            id: 4,
            name: "Physical/Finance",
            contribution: 2.8,
            color: "#4ECDC4",
            source: "Real economy",
        },
        {
            id: 7,
            name: "Global/Fintech",
            contribution: 3.1,
            color: "#45B7D1",
            source: "Network effects",
        },
        {
            id: 10,
            name: "Human/Risk",
            contribution: 2.4,
            color: "#96CEB4",
            source: "Human capital",
        },
        {
            id: 13,
            name: "Infra/Supply",
            contribution: 1.9,
            color: "#FFE194",
            source: "Physical infra",
        },
        {
            id: 16,
            name: "Apps/Nation",
            contribution: 1.0,
            color: "#B4A5D1",
            source: "Digital layer",
        },
    ];

    let selectedLayer = null;

    function selectLayer(layer) {
        selectedLayer = layer;
    }
</script>

<div class="yield-curve-container" in:fade>
    <div class="header">
        <h2 class="title">Sovereign Prime Rate: {primeRate}%</h2>
        <p class="subtitle">
            Derived from 20 layers of human effort, not central banks
        </p>
    </div>

    <!-- 19-Layer Ribbon Simulation -->
    <div class="ribbon-visual">
        <svg viewBox="0 0 1000 200" class="ribbon-svg">
            <defs>
                <linearGradient
                    id="ribbonGradient"
                    x1="0%"
                    y1="0%"
                    x2="100%"
                    y2="0%"
                >
                    <stop
                        offset="0%"
                        style="stop-color:#9370DB;stop-opacity:1"
                    />
                    <stop
                        offset="50%"
                        style="stop-color:#4ECDC4;stop-opacity:1"
                    />
                    <stop
                        offset="100%"
                        style="stop-color:#FF6B6B;stop-opacity:1"
                    />
                </linearGradient>
            </defs>
            <path
                d="M0,100 Q250,50 500,100 T1000,100"
                fill="none"
                stroke="url(#ribbonGradient)"
                stroke-width="12"
                stroke-linecap="round"
                class="main-path"
            />

            {#each layers as layer, i}
                <circle
                    cx={150 + i * 140}
                    cy={100 + Math.sin(i) * 30}
                    r={selectedLayer?.id === layer.id ? 10 : 6}
                    fill={layer.color}
                    class="node"
                    on:mouseenter={() => selectLayer(layer)}
                />
            {/each}
        </svg>
    </div>

    {#if selectedLayer}
        <div class="tooltip" transition:fade>
            <h3>Layer Group: {selectedLayer.name}</h3>
            <div class="detail">
                Contribution: <span class="highlight"
                    >+{selectedLayer.contribution}%</span
                >
            </div>
            <div class="detail">Primary Source: {selectedLayer.source}</div>
        </div>
    {/if}

    <div class="breakdown-grid">
        <div class="stat">
            <span class="label">vs US Treasury</span>
            <span class="value positive">+7.7%</span>
        </div>
        <div class="stat">
            <span class="label">Volatility (MoM)</span>
            <span class="value">0.3%</span>
        </div>
        <div class="stat">
            <span class="label">Moat Status</span>
            <span class="value sovereign">ACTIVE</span>
        </div>
    </div>
</div>

<style>
    .yield-curve-container {
        padding: 2rem;
        background: rgba(20, 20, 25, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        backdrop-filter: blur(20px);
        color: white;
    }

    .title {
        font-size: 1.8rem;
        margin: 0;
        background: linear-gradient(135deg, #00ffcc, #3399ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    .ribbon-visual {
        margin: 2rem 0;
    }

    .main-path {
        filter: drop-shadow(0 0 10px rgba(78, 205, 196, 0.5));
    }

    .node {
        cursor: pointer;
        transition: all 0.2s;
        filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.2));
    }

    .node:hover {
        r: 12;
        filter: drop-shadow(0 0 10px white);
    }

    .tooltip {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }

    .tooltip h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }

    .highlight {
        color: #00ffcc;
        font-weight: 700;
    }

    .breakdown-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stat {
        display: flex;
        flex-direction: column;
    }

    .label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
    }

    .value {
        font-size: 1.2rem;
        font-weight: 600;
        font-family: "JetBrains Mono", monospace;
    }

    .positive {
        color: #00ffcc;
    }
    .sovereign {
        color: #9370db;
        text-shadow: 0 0 10px rgba(147, 112, 219, 0.5);
    }
</style>
