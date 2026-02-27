<script lang="ts">
    import { fade, fly } from "svelte/transition";

    let {
        yieldData = {
            total: 12.4,
            components: [
                {
                    layer: 1,
                    name: "Identity",
                    contribution: 0.4,
                    source: "S-ID signatures",
                    color: "#FF6B6B",
                },
                {
                    layer: 4,
                    name: "Brazil",
                    contribution: 1.2,
                    source: "age://pay volume",
                    color: "#4ECDC4",
                },
                {
                    id: 5,
                    name: "Finance",
                    contribution: 1.8,
                    source: "Credit pools",
                    color: "#45B7D1",
                },
                {
                    id: 13,
                    name: "Infra",
                    contribution: 0.4,
                    source: "S-Node rewards",
                    color: "#B565A7",
                },
                {
                    id: 13,
                    name: "ICP Work",
                    contribution: 1.1,
                    source: "Cycles / Node Uptime",
                    color: "#F15A24",
                },
                {
                    id: 15,
                    name: "Supply",
                    contribution: 1.3,
                    source: "Invoice tokens",
                    color: "#DD4124",
                },
                {
                    id: 20,
                    name: "Bond",
                    contribution: 0.1,
                    source: "Parity spread",
                    color: "#9B2335",
                },
            ],
        },
    } = $props();

    let selectedLayer = $state<any>(null);

    function unfold(component: any) {
        selectedLayer = component;
    }
</script>

<div class="glass-bond" in:fade>
    <div class="header">
        <h2>Glass Bond Explorer</h2>
        <p>Mathematical certainty for every basis point.</p>
    </div>

    <button
        class="summary-card"
        onclick={() => (selectedLayer = null)}
        onkeydown={(e) => e.key === "Enter" && (selectedLayer = null)}
        aria-label="Reset layer selection"
    >
        <div class="yield-display">
            <span class="total">{yieldData.total}%</span>
            <span class="label">Total sAGE Yield</span>
        </div>
        <div class="trace-hint">Click a layer to unfold the truth</div>
    </button>

    <div class="layer-grid">
        {#each yieldData.components as component}
            <button
                class="layer-card"
                style="--layer-color: {component.color}"
                onclick={() => unfold(component)}
                onkeydown={(e) => e.key === "Enter" && unfold(component)}
                aria-label="Select {component.name} layer"
                aria-expanded={selectedLayer === component}
            >
                <div class="card-top">
                    <span class="name">{component.name}</span>
                    <span class="val">+{component.contribution}%</span>
                </div>
                <div class="source">{component.source}</div>

                {#if selectedLayer === component}
                    <div class="detail" in:fly={{ y: 20 }}>
                        <div class="row">
                            <span>Proof</span>
                            <span class="mon">0x8f3a...b2c5</span>
                        </div>
                        <div class="row">
                            <span>Audit</span>
                            <span class="mon">CONTINUOUS</span>
                        </div>
                    </div>
                {/if}
            </button>
        {/each}
    </div>
</div>

<style>
    .glass-bond {
        background: rgba(10, 10, 15, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
    }

    .header h2 {
        margin: 0;
        font-size: 1.4rem;
    }
    .header p {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }

    .summary-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        cursor: pointer;
        color: white;
        font-family: inherit;
    }

    .total {
        display: block;
        font-size: 3.5rem;
        font-weight: 800;
        color: #00ffcc;
    }

    .label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
    }

    .layer-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .layer-card {
        width: 100%;
        text-align: left;
        background: rgba(255, 255, 255, 0.05);
        border: none;
        border-left: 4px solid var(--layer-color);
        padding: 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
        color: white;
        font-family: inherit;
    }

    .layer-card:hover {
        transform: scale(1.02);
    }

    .card-top {
        display: flex;
        justify-content: space-between;
        font-weight: 600;
    }
    .val {
        color: var(--layer-color);
    }
    .source {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 0.25rem;
    }

    .detail {
        margin-top: 1rem;
        padding-top: 0.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 0.75rem;
    }

    .row {
        display: flex;
        justify-content: space-between;
        margin-top: 0.25rem;
    }
    .mon {
        font-family: monospace;
        color: #00ffcc;
    }
</style>
