<script lang="ts">
    import { onMount } from "svelte";

    export let data: any[] = [];
    export let color = "#9370DB";

    let canvas: HTMLCanvasElement | null = null;
    let ctx: CanvasRenderingContext2D | null = null;
    let tooltip = { show: false, x: 0, y: 0, price: 0, date: "" };

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

    $: if (ctx && data) drawChart();

    function drawChart() {
        if (!data || data.length === 0 || !ctx) return;

        const width = canvas.width;
        const height = canvas.height;
        const padding = 40;

        ctx.clearRect(0, 0, width, height);

        // Find min/max for scaling
        const prices = data.map((d) => d.price);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice || 1;

        // Draw grid
        ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
        ctx.lineWidth = 1;

        // Horizontal grid lines
        for (let i = 0; i <= 4; i++) {
            const y = padding + (i * (height - 2 * padding)) / 4;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();

            // Price labels
            const price = maxPrice - (i * priceRange) / 4;
            ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
            ctx.font = "10px sans-serif";
            ctx.fillText("$" + price.toFixed(2), 5, y - 5);
        }

        // Draw line chart
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;

        data.forEach((point, i) => {
            const x = padding + (i * (width - 2 * padding)) / (data.length - 1);
            const y =
                height -
                padding -
                ((point.price - minPrice) / priceRange) *
                    (height - 2 * padding);

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();

        // Fill area under line
        ctx.lineTo(width - padding, height - padding);
        ctx.lineTo(padding, height - padding);
        ctx.closePath();
        ctx.fillStyle = color + "20";
        ctx.fill();

        // Draw points
        data.forEach((point, i) => {
            const x = padding + (i * (width - 2 * padding)) / (data.length - 1);
            const y =
                height -
                padding -
                ((point.price - minPrice) / priceRange) *
                    (height - 2 * padding);

            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = "white";
            ctx.lineWidth = 2;
            ctx.stroke();
        });
    }


    function handleMouseMove(event) {
        if (!ctx || !data || data.length === 0) return;
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;

        const scaleY = canvas.height / rect.height;

        const mouseX = (event.clientX - rect.left) * scaleX;

        const padding = 40;
        const width = canvas.width;

        // Find closest data point
        let minDist = Infinity;
        let closestIndex = -1;


        data.forEach((point, i) => {
            const x = padding + (i * (width - 2 * padding)) / (data.length - 1);
            const dist = Math.abs(mouseX - x);
            if (dist < minDist) {
                minDist = dist;
                closestIndex = i;
            }
        });

        if (closestIndex !== -1 && minDist < 30) {
            const point = data[closestIndex];

            tooltip = {
                show: true,
                x: event.clientX,
                y: event.clientY,
                price: point.price,
                date:
                    point.date instanceof Date
                        ? point.date.toLocaleDateString()
                        : new Date(point.date).toLocaleDateString(),
            };
        } else {
            tooltip.show = false;
        }
    }

    function handleMouseLeave() {
        tooltip.show = false;
    }
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="price-chart">
    <canvas
        bind:this={canvas}
        width="600"
        height="300"
        onmousemove={handleMouseMove}
        onmouseleave={handleMouseLeave}
    ></canvas>

    {#if tooltip.show}
        <div
            class="tooltip"
            style="left: {tooltip.x}px; top: {tooltip.y - 50}px;"
        >
            <div class="tooltip-price">${tooltip.price.toFixed(2)}</div>
            <div class="tooltip-date">{tooltip.date}</div>
        </div>
    {/if}
</div>

<style>
    .price-chart {
        position: relative;
        width: 100%;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        box-sizing: border-box;
    }

    canvas {
        width: 100%;
        height: auto;
        aspect-ratio: 2/1;
        cursor: crosshair;
    }

    .tooltip {
        position: fixed;
        background: rgba(20, 20, 20, 0.95);
        border: 1px solid #9370db;
        border-radius: 0.5rem;
        padding: 0.5rem;
        pointer-events: none;
        z-index: 100;
        transform: translateX(-50%);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    }

    .tooltip-price {
        font-weight: 600;
        color: #9370db;
        font-size: 0.9rem;
    }

    .tooltip-date {
        font-size: 0.7rem;
        opacity: 0.7;
    }
</style>
