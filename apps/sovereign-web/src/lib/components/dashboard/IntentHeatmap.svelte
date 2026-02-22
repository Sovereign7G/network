<script lang="ts">
    import { onMount } from "svelte";
    import { HeatmapEngine } from "../../../../../../packages/age-intent/src/heatmap/HeatmapEngine";
    import { telemetryStore } from "$lib/stores/telemetry-store";

    let canvas: HTMLCanvasElement;
    let engine: HeatmapEngine;

    onMount(() => {
        if (canvas) {
            engine = new HeatmapEngine(canvas);

            const unsubscribe = telemetryStore.subscribe((data: any) => {
                // Trigger a spark for each transaction or alert
                if (data.alerts && data.alerts.length > 0) {
                    engine.addIntent(
                        Math.random() * canvas.width,
                        Math.random() * canvas.height,
                        0.8,
                    );
                }
            });

            const handleResize = () => {
                const parent = canvas.parentElement;
                if (parent) {
                    engine.resize(parent.clientWidth, parent.clientHeight);
                }
            };

            window.addEventListener("resize", handleResize);
            handleResize();

            return () => {
                window.removeEventListener("resize", handleResize);
                unsubscribe();
            };
        }
    });
</script>

<div class="heatmap-container">
    <div class="heatmap-header">
        <h3>🔥 INTENT DENSITY (THE SPARK)</h3>
        <span class="status">ZK-VERIFIED INTENTS</span>
    </div>
    <canvas bind:this={canvas} class="heatmap-canvas"></canvas>
</div>

<style>
    .heatmap-container {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        overflow: hidden;
        height: 300px;
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .heatmap-header {
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 10;
        pointer-events: none;
    }

    .heatmap-header h3 {
        margin: 0;
        font-size: 0.9rem;
        color: #ff6b6b;
        letter-spacing: 1px;
    }

    .status {
        font-size: 0.7rem;
        background: rgba(255, 107, 107, 0.1);
        color: #ff6b6b;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
    }

    .heatmap-canvas {
        flex: 1;
        width: 100%;
        height: 100%;
        background: #000;
    }
</style>
