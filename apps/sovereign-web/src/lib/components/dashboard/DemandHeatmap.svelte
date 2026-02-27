<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { api } from "$lib/services/api";

    let demand: any = $state(null);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            demand = await api.request("/analytics/demand");
        } catch (error) {
            console.error("Failed to load demand data", error);
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="demand-heatmap glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-start mb-8">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Global Demand Heatmap
            </h3>
            <p class="text-[9px] text-white/20 uppercase font-bold">
                Predictive Consumer Resonance
            </p>
        </div>
        <div class="flex items-center gap-2">
            <span class="text-[8px] font-black text-cyan-400 uppercase"
                >Live Pulse</span
            >
            <div
                class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"
            ></div>
        </div>
    </div>

    {#if isLoading}
        <div class="flex-1 flex items-center justify-center">
            <div class="heatmap-loader"></div>
        </div>
    {:else if demand}
        <div class="flex-1 space-y-6">
            {#each demand.regions as region, i}
                <div class="region-row" in:fly={{ x: 20, delay: i * 100 }}>
                    <div class="flex justify-between items-end mb-2">
                        <span
                            class="text-[10px] font-black text-white uppercase"
                            >{region.name}</span
                        >
                        <span
                            class="text-[9px] font-bold {region.shift.startsWith(
                                '+',
                            )
                                ? 'text-emerald-400'
                                : 'text-rose-400'}">{region.shift}</span
                        >
                    </div>
                    <div
                        class="relative h-6 bg-white/5 rounded-lg overflow-hidden border border-white/5"
                    >
                        <div
                            class="absolute inset-0 bg-cyan-400/20"
                            style="width: {region.density * 100}%"
                        ></div>
                        <div
                            class="absolute inset-0 flex items-center justify-center"
                        >
                            <span
                                class="text-[8px] font-black text-white/40 uppercase"
                                >Density Index: {region.density.toFixed(
                                    2,
                                )}</span
                            >
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <div
            class="mt-8 p-4 bg-cyan-400/5 border border-cyan-400/10 rounded-2xl"
        >
            <div class="flex items-center gap-2 mb-2">
                <span class="text-[8px] font-black text-white uppercase italic"
                    >AI Recommendation //</span
                >
            </div>
            <p
                class="text-[10px] font-bold text-white/60 leading-relaxed italic"
            >
                Strategic shift detected in <span class="text-cyan-400"
                    >Mars Colony 1</span
                >. Recommend re-routing Alpha-Series inventory to captured
                anticipated surge in 48h.
            </p>
        </div>
    {/if}
</div>

<style>
    .demand-heatmap {
        background: linear-gradient(
            135deg,
            rgba(16, 24, 39, 0.4) 0%,
            rgba(2, 6, 23, 0.4) 100%
        );
    }

    .heatmap-loader {
        width: 32px;
        height: 32px;
        border: 2px solid rgba(34, 211, 238, 0.1);
        border-top-color: #22d3ee;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
