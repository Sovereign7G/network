<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    let mounted = false;
    let activeFlow: "PAYMENT" | "AGREEMENT" | "SYNDICATE" | "GRANT" = "PAYMENT";

    onMount(() => {
        mounted = true;
    });

    const FLOW_TYPES = [
        {
            id: "PAYMENT",
            label: "Transaction",
            icon: "💰",
            description: "Standard machine-to-machine exchange",
        },
        {
            id: "AGREEMENT",
            label: "Smart Contract",
            icon: "📜",
            description: "Declarative joint intent",
        },
        {
            id: "SYNDICATE",
            label: "Capital Pool",
            icon: "🏛️",
            description: "Group capital formation",
        },
        {
            id: "GRANT",
            label: "Ecosystem Grant",
            icon: "🎁",
            description: "Builder funding lifecycle",
        },
    ];

    let connectors = [
        { from: "Identity", to: "Vault", status: "ACTIVE" },
        { from: "Vault", to: "Compute", status: "READY" },
    ];
</script>

<div class="compose-workspace">
    <div class="compose-header" in:fade>
        <h1>🛠️ Compose District</h1>
        <p>Connect primitives to create emergent sovereignty.</p>
    </div>

    {#if mounted}
        <div class="compose-layout">
            <!-- Sidebar: Primitives -->
            <div class="primitives-sidebar" in:fly={{ x: -20, duration: 500 }}>
                <h2>Available Primitives</h2>
                <div class="primitive-grid">
                    {#each FLOW_TYPES as flow}
                        <button
                            class="primitive-card"
                            class:active={activeFlow === flow.id}
                            on:click={() => (activeFlow = flow.id as any)}
                        >
                            <span class="p-icon">{flow.icon}</span>
                            <div class="p-text">
                                <strong>{flow.label}</strong>
                                <p>{flow.description}</p>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Canvas: Dynamic Connectors -->
            <div class="canvas-area" in:fade={{ delay: 200 }}>
                <div class="canvas-header">
                    <h2>Visual Orchestration</h2>
                    <div class="canvas-controls">
                        <button class="ctrl-btn">Clear</button>
                        <button class="ctrl-btn primary">Deploy Intent</button>
                    </div>
                </div>

                <div class="orchestration-map">
                    <svg class="connectors-svg">
                        <defs>
                            <linearGradient
                                id="grad1"
                                x1="0%"
                                y1="0%"
                                x2="100%"
                                y2="0%"
                            >
                                <stop
                                    offset="0%"
                                    style="stop-color:#9370db;stop-opacity:1"
                                />
                                <stop
                                    offset="100%"
                                    style="stop-color:#4ECDC4;stop-opacity:1"
                                />
                            </linearGradient>
                        </defs>
                        <path
                            d="M 150 150 Q 300 150 450 150"
                            stroke="url(#grad1)"
                            stroke-width="2"
                            fill="transparent"
                            class="flow-line"
                        />
                    </svg>

                    <div class="node identity glow">
                        <span class="node-icon">🆔</span>
                        <span>Citizen ID</span>
                    </div>

                    <div class="node vault glow">
                        <span class="node-icon">💰</span>
                        <span>Asset Vault</span>
                    </div>

                    <div class="node nexus glow">
                        <span class="node-icon">⚡</span>
                        <span>Intent Executor</span>
                    </div>

                    <div class="connector-overlay">
                        {#each connectors as conn}
                            <div class="conn-tag">
                                {conn.from} → {conn.to} ({conn.status})
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .compose-workspace {
        max-width: 1400px;
        margin: 0 auto;
        color: white;
    }

    .compose-header {
        margin-bottom: 3rem;
    }

    .compose-header h1 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
    }

    .compose-header p {
        opacity: 0.7;
        font-size: 1.2rem;
    }

    .compose-layout {
        display: grid;
        grid-template-columns: 350px 1fr;
        gap: 3rem;
        min-height: 600px;
    }

    .primitives-sidebar {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
    }

    .primitive-grid {
        display: grid;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .primitive-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        color: white;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
    }

    .primitive-card:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .primitive-card.active {
        border-color: #9370db;
        background: rgba(147, 112, 219, 0.1);
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
    }

    .p-icon {
        font-size: 2rem;
    }

    .p-text p {
        margin: 0.25rem 0 0 0;
        font-size: 0.8rem;
        opacity: 0.6;
    }

    .canvas-area {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        padding: 2rem;
        display: flex;
        flex-direction: column;
    }

    .canvas-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .canvas-controls {
        display: flex;
        gap: 1rem;
    }

    .ctrl-btn {
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
    }

    .ctrl-btn.primary {
        background: #9370db;
        font-weight: 600;
    }

    .orchestration-map {
        flex: 1;
        position: relative;
        background: radial-gradient(
            circle at center,
            rgba(147, 112, 219, 0.1) 0%,
            transparent 70%
        );
        border-radius: 1rem;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-around;
    }

    .node {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(147, 112, 219, 0.3);
        border-radius: 1rem;
        width: 150px;
    }

    .node-icon {
        font-size: 3rem;
    }

    .node.glow {
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
        animation: glow-pulse 4s infinite alternate;
    }

    @keyframes glow-pulse {
        from {
            box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
        }
        to {
            box-shadow: 0 0 40px rgba(147, 112, 219, 0.4);
            border-color: rgba(147, 112, 219, 0.6);
        }
    }

    .flow-line {
        stroke-dasharray: 10;
        animation: flow 20s linear infinite;
    }

    @keyframes flow {
        from {
            stroke-dashoffset: 200;
        }
        to {
            stroke-dashoffset: 0;
        }
    }

    .connectors-svg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }

    .connector-overlay {
        position: absolute;
        bottom: 2rem;
        right: 2rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .conn-tag {
        font-size: 0.8rem;
        padding: 0.4rem 0.8rem;
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid #4ecdc4;
        border-radius: 1rem;
        color: #4ecdc4;
    }
</style>
