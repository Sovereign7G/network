<script lang="ts">
    import { onMount } from "svelte";

    export let allocation = {
        liquid: 60,
        staked: 25,
        vested: 15,
    };

    let canvas;
    let ctx;

    const COLORS = {
        liquid: "#4ECDC4",
        staked: "#9370DB",
        vested: "#FFD700",
    };

    onMount(() => {
        if (canvas) {
            ctx = canvas.getContext("2d");
            drawChart();
        }
    });

    $: if (ctx && allocation) drawChart();

    function drawChart() {
        if (!ctx) return;
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.35;

        ctx.clearRect(0, 0, width, height);

        // Draw donut chart
        let startAngle = 0;
        const total = Object.values(allocation).reduce((a, b) => a + b, 0);

        if (total === 0) return;

        Object.entries(allocation).forEach(([key, value]) => {
            const sliceAngle = (value / total) * Math.PI * 2;
            const endAngle = startAngle + sliceAngle;

            // Draw slice
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.closePath();
            ctx.fillStyle = COLORS[key] || "#999";
            ctx.fill();

            // Draw inner circle for donut hole
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius * 0.6, 0, Math.PI * 2);
            ctx.fillStyle = "#1a1a1a"; // closer to background color
            ctx.fill();

            startAngle = endAngle;
        });

        // Draw center text
        ctx.font = "bold 16px sans-serif";
        ctx.fillStyle = "white";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("Allocation", centerX, centerY - 10);
        ctx.font = "12px sans-serif";
        ctx.fillStyle = "#9370DB";
        ctx.fillText("by type", centerX, centerY + 10);
    }
</script>

<div class="allocation-chart">
    <canvas bind:this={canvas} width="300" height="300" class="chart-canvas"
    ></canvas>

    <div class="allocation-legend">
        {#each Object.entries(allocation) as [key, value]}
            <div class="legend-item">
                <span
                    class="legend-color"
                    style="background: {COLORS[key] || '#999'};"
                ></span>
                <span class="legend-label"
                    >{key.charAt(0).toUpperCase() + key.slice(1)}</span
                >
                <span class="legend-value">{value}%</span>
            </div>
        {/each}
    </div>
</div>

<style>
    .allocation-chart {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
    }

    .chart-canvas {
        width: 100%;
        max-width: 300px;
        height: auto;
        aspect-ratio: 1;
    }

    .allocation-legend {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        justify-content: center;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .legend-color {
        width: 1rem;
        height: 1rem;
        border-radius: 0.25rem;
    }

    .legend-label {
        opacity: 0.8;
    }

    .legend-value {
        font-weight: 600;
        color: #9370db;
    }
</style>
