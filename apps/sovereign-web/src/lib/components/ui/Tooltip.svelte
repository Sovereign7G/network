<script lang="ts">
//     import { fade, scale } from "svelte/transition";

    export let text: string = "";
    export let x: number = 0;
    export let y: number = 0;
    export let visible: boolean = false;
</script>

{#if visible && text}
    <div
        class="tooltip-container"
        style="left: {x}px; top: {y}px;"
        transitionscale={{ duration: 200, start: 0.95, opacity: 0 }}
    >
        <div class="tooltip-aura"></div>
        <div class="tooltip-content">
            <div class="tooltip-header">
                <span class="pulse-dot"></span>
                <span class="intelligence-label">Awareness Hub</span>
            </div>
            <p class="tooltip-text">{text}</p>
        </div>
    </div>
{/if}

<style>
    .tooltip-container {
        position: fixed;
        z-index: 10000;
        pointer-events: none;
        transform: translate(-50%, -120%);
        padding: 1px;
        border-radius: 12px;
        background: linear-gradient(
            135deg,
            rgba(76, 175, 80, 0.4),
            rgba(52, 152, 219, 0.4)
        );
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .tooltip-aura {
        position: absolute;
        inset: -5px;
        background: radial-gradient(
            circle at center,
            rgba(76, 175, 80, 0.2),
            transparent 70%
        );
        filter: blur(10px);
        z-index: -1;
        border-radius: 16px;
    }

    .tooltip-content {
        background: rgba(15, 15, 25, 0.95);
        backdrop-filter: blur(20px);
        padding: 1rem;
        border-radius: 11px;
        min-width: 200px;
        max-width: 300px;
    }

    .tooltip-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.25rem;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background: #4caf50;
        border-radius: 50%;
        box-shadow: 0 0 10px #4caf50;
        animation: pulse 2s infinite;
    }

    .intelligence-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 700;
    }

    .tooltip-text {
        margin: 0;
        font-size: 0.85rem;
        line-height: 1.4;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
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
</style>
