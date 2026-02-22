<script lang="ts">
    import { fade, fly } from "svelte/transition";

    export let flowTitle: string = "Standard User Flow";
    export let steps: Array<{
        label: string;
        description: string;
        status: "COMPLETED" | "ACTIVE" | "PENDING";
    }> = [];

    // Aesthetic colors based on District
    const STATUS_COLORS = {
        COMPLETED: "#4ECDC4",
        ACTIVE: "#9370DB",
        PENDING: "rgba(255,255,255,0.2)",
    };
</script>

<div class="flow-visualizer" in:fade>
    <div class="flow-header">
        <h3>🛣️ {flowTitle}</h3>
        <span class="step-count"
            >{steps.filter((s) => s.status === "COMPLETED").length} / {steps.length}
            Steps</span
        >
    </div>

    <div class="steps-container">
        {#each steps as step, i}
            <div class="step-node" in:fly={{ x: 20, delay: i * 100 }}>
                <div
                    class="node-indicator"
                    style="background: {STATUS_COLORS[step.status]}"
                >
                    {#if step.status === "COMPLETED"}
                        <span class="check">✓</span>
                    {:else if step.status === "ACTIVE"}
                        <span class="active-dot"></span>
                    {/if}
                </div>

                <div
                    class="node-content"
                    class:active={step.status === "ACTIVE"}
                >
                    <strong>{step.label}</strong>
                    <p>{step.description}</p>
                </div>

                {#if i < steps.length - 1}
                    <div
                        class="node-path"
                        style="background: linear-gradient(to bottom, {STATUS_COLORS[
                            step.status
                        ]}, {STATUS_COLORS[steps[i + 1]?.status || 'PENDING']})"
                    ></div>
                {/if}
            </div>
        {/each}
    </div>
</div>

<style>
    .flow-visualizer {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
        color: white;
    }

    .flow-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2.5rem;
    }

    .flow-header h3 {
        margin: 0;
        font-size: 1.2rem;
        letter-spacing: 0.05em;
    }

    .step-count {
        font-size: 0.8rem;
        opacity: 0.6;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
    }

    .steps-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        position: relative;
    }

    .step-node {
        display: flex;
        gap: 1.5rem;
        position: relative;
        z-index: 1;
    }

    .node-indicator {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
    }

    .check {
        color: #1a1a1a;
        font-weight: bold;
    }

    .active-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        box-shadow: 0 0 10px white;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.5);
            opacity: 0.5;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .node-content {
        flex: 1;
        opacity: 0.6;
    }

    .node-content.active {
        opacity: 1;
    }

    .node-content strong {
        display: block;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    .node-content p {
        margin: 0;
        font-size: 0.85rem;
        opacity: 0.7;
        line-height: 1.4;
    }

    .node-path {
        position: absolute;
        left: 15px;
        top: 32px;
        width: 2px;
        height: calc(100% + 2rem - 32px);
        z-index: -1;
        opacity: 0.3;
    }
</style>
