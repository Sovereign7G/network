<script lang="ts">
    export let value: number = 0; // 0-100
    export let size: "small" | "medium" | "large" = "medium";

    const sizes = {
        small: { width: 40, strokeWidth: 4, fontSize: "0.7rem" },
        medium: { width: 80, strokeWidth: 8, fontSize: "1rem" },
        large: { width: 120, strokeWidth: 12, fontSize: "1.5rem" },
    };

    $: radius = (sizes[size].width - sizes[size].strokeWidth) / 2;
    $: circumference = 2 * Math.PI * radius;
    $: offset = circumference - (value / 100) * circumference;
</script>

<div
    class="resonance-gauge"
    style="width: {sizes[size].width}px; height: {sizes[size].width}px"
>
    <svg width={sizes[size].width} height={sizes[size].width}>
        <!-- Background circle -->
        <circle
            cx={sizes[size].width / 2}
            cy={sizes[size].width / 2}
            r={radius}
            stroke="rgba(255, 255, 255, 0.05)"
            stroke-width={sizes[size].strokeWidth}
            fill="none"
        />
        <!-- Progress circle -->
        <circle
            cx={sizes[size].width / 2}
            cy={sizes[size].width / 2}
            r={radius}
            stroke="url(#resonance-gradient)"
            stroke-width={sizes[size].strokeWidth}
            stroke-dasharray={circumference}
            stroke-dashoffset={offset}
            stroke-linecap="round"
            fill="none"
            transform="rotate(-90 {sizes[size].width / 2} {sizes[size].width /
                2})"
            class="progress-ring"
        />

        <defs>
            <linearGradient
                id="resonance-gradient"
                x1="0%"
                y1="0%"
                x2="100%"
                y2="100%"
            >
                <stop offset="0%" stop-color="#4CAF50" />
                <stop offset="100%" stop-color="#81C784" />
            </linearGradient>
        </defs>
    </svg>

    <div class="gauge-value" style="font-size: {sizes[size].fontSize}">
        {value}%
    </div>
</div>

<style>
    .resonance-gauge {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .progress-ring {
        transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .gauge-value {
        position: absolute;
        font-weight: 700;
        color: white;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
    }
</style>
