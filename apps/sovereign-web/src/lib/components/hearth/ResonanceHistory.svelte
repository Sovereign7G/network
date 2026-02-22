<script lang="ts">
    import { onMount } from "svelte";

    export let data = [];

    let canvas;
    let ctx;

    onMount(() => {
        if (canvas) {
            ctx = canvas.getContext("2d");
            drawChart();

            const resizeObserver = new ResizeObserver(() => {
                drawChart();
            });
            resizeObserver.observe(canvas);

            return () => resizeObserver.disconnect();
        }
    });

    $: if (ctx) drawChart();

    function drawChart() {
        if (!data || data.length === 0) return;

        const width = canvas.width;
        const height = canvas.height;
        const padding = 20;

        ctx.clearRect(0, 0, width, height);

        // Find max value for scaling
        const maxValue = Math.max(...data.map((d) => d.value), 1);

        // Draw bars
        const barWidth = (width - 2 * padding) / data.length - 2;

        data.forEach((point, i) => {
            const x = padding + i * (barWidth + 2);
            const barHeight = (point.value / maxValue) * (height - 2 * padding);
            const y = height - padding - barHeight;

            // Draw bar
            ctx.fillStyle = "#9370DB";
            ctx.globalAlpha = 0.3 + (point.value / maxValue) * 0.7;
            ctx.fillRect(x, y, barWidth, barHeight);

            // Draw top highlight
            ctx.fillStyle = "#FF6B6B";
            ctx.globalAlpha = 0.8;
            ctx.fillRect(x, y, barWidth, 2);

            // Draw value if significant
            if (point.value > maxValue * 0.3) {
                ctx.fillStyle = "white";
                ctx.font = "8px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(point.value.toString(), x + barWidth / 2, y - 5);
            }
        });

        // Draw baseline
        ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();
    }
</script>

<div class="resonance-history">
    <canvas bind:this={canvas} width="300" height="150" class="history-canvas"
    ></canvas>

    <div class="history-footer">
        <span class="history-label">Last 30 days</span>
        <span class="history-total">
            Total: {data.reduce((sum, d) => sum + d.value, 0)}
        </span>
    </div>
</div>

<style>
    .resonance-history {
        width: 100%;
    }

    .history-canvas {
        width: 100%;
        height: auto;
        aspect-ratio: 2/1;
        margin-bottom: 0.5rem;
    }

    .history-footer {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .history-total {
        color: #9370db;
    }
</style>
