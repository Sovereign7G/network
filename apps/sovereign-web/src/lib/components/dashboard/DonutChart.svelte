<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";

    interface DataItem {
        label: string;
        value: number;
        color: string;
    }

    interface Props {
        data: DataItem[];
        size?: number;
        strokeWidth?: number;
    }

    let { data = [], size = 200, strokeWidth = 20 }: Props = $props();

    let total = $derived(data.reduce((acc, item) => acc + item.value, 0));
    let segments = $derived(calculateSegments(data, total));

    function calculateSegments(data: DataItem[], total: number) {
        let cumulativePercent = 0;
        return data.map((item) => {
            const percent = item.value / total;
            const start = cumulativePercent;
            cumulativePercent += percent;
            return {
                ...item,
                percent,
                dashOffset: (1 - start) * (Math.PI * (size - strokeWidth)),
                dashArray: `${percent * (Math.PI * (size - strokeWidth))} ${(1 - percent) * (Math.PI * (size - strokeWidth))}`,
            };
        });
    }

    let mounted = $state(false);
    onMount(() => {
        setTimeout(() => (mounted = true), 100);
    });
</script>

<div
    class="relative flex items-center justify-center"
    style="width: {size}px; height: {size}px;"
>
    <svg viewBox="0 0 {size} {size}" class="transform -rotate-90 w-full h-full">
        <!-- Background Track -->
        <circle
            cx={size / 2}
            cy={size / 2}
            r={(size - strokeWidth) / 2}
            fill="transparent"
            stroke="rgba(255, 255, 255, 0.05)"
            stroke-width={strokeWidth}
        />

        {#if mounted}
            {#each segments as segment}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={(size - strokeWidth) / 2}
                    fill="transparent"
                    stroke={segment.color}
                    stroke-width={strokeWidth}
                    stroke-dasharray={segment.dashArray}
                    style="stroke-dashoffset: 0; transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);"
                    stroke-linecap="round"
                    in:fade={{ duration: 1000 }}
                />
            {/each}
        {/if}
    </svg>

    <!-- Center Content -->
    <div
        class="absolute inset-0 flex flex-col items-center justify-center text-center"
    >
        <span class="text-3xl font-black tracking-tighter">100%</span>
        <span
            class="text-[8px] font-black text-white/30 uppercase tracking-widest mt-1"
            >Allocation</span
        >
    </div>
</div>
