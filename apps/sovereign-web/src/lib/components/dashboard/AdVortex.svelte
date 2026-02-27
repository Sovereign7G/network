<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { api } from "$lib/services/api";

    let ads: any[] = $state([]);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            ads = await api.request("/analytics/ads");
        } catch (error) {
            console.error("Failed to load ad data", error);
        } finally {
            isLoading = false;
        }
    });

    function getStatusColor(status: string) {
        switch (status) {
            case "SURGING":
                return "text-rose-500";
            case "OPTIMIZING":
                return "text-cyan-400";
            case "STABLE":
                return "text-emerald-400";
            default:
                return "text-white/40";
        }
    }
</script>

<div class="ad-vortex glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-start mb-8">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Ad Vortex // Cognitive Reach
            </h3>
            <p class="text-[9px] text-white/20 uppercase font-bold">
                Privacy-Preserving Attention Yield
            </p>
        </div>
        <div class="text-right">
            <span
                class="text-[8px] font-black uppercase text-white/20 block mb-1"
                >Global CTR</span
            >
            <span class="text-xs font-black text-rose-500">4.82%</span>
        </div>
    </div>

    {#if isLoading}
        <div class="flex-1 flex items-center justify-center">
            <div class="vortex-loader"></div>
        </div>
    {:else}
        <div class="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
            {#each ads as ad, i}
                <div
                    class="ad-node bg-white/[0.02] border border-white/5 p-4 rounded-2xl group hover:border-white/10 transition-all"
                    in:fly={{ y: 20, delay: i * 100 }}
                >
                    <div class="flex justify-between items-center mb-3">
                        <span
                            class="text-[10px] font-black text-white group-hover:text-cyan-400 transition-colors uppercase"
                            >{ad.client}</span
                        >
                        <span
                            class="text-[8px] font-black uppercase {getStatusColor(
                                ad.status,
                            )}">{ad.status}</span
                        >
                    </div>

                    <div class="grid grid-cols-3 gap-2">
                        <div class="stat">
                            <span
                                class="text-[7px] font-black uppercase text-white/20 block mb-0.5"
                                >Impressions</span
                            >
                            <span class="text-[10px] font-bold text-white"
                                >{(ad.impressions / 1000).toFixed(0)}k</span
                            >
                        </div>
                        <div class="stat">
                            <span
                                class="text-[7px] font-black uppercase text-white/20 block mb-0.5"
                                >Conv. Rate</span
                            >
                            <span class="text-[10px] font-bold text-cyan-400"
                                >{(ad.conversion * 100).toFixed(1)}%</span
                            >
                        </div>
                        <div class="stat">
                            <span
                                class="text-[7px] font-black uppercase text-white/20 block mb-0.5"
                                >Yield (AGE)</span
                            >
                            <span class="text-[10px] font-bold text-emerald-400"
                                >+{ad.revenue}</span
                            >
                        </div>
                    </div>

                    <div
                        class="mt-3 h-1 bg-white/5 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full bg-white/20 transition-all duration-1000"
                            style="width: {ad.conversion * 1000}%"
                        ></div>
                    </div>
                </div>
            {/each}
        </div>

        <div class="mt-6 flex gap-2">
            <button
                class="flex-1 py-3 bg-white text-black text-[9px] font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-all"
                >Launch Campaign</button
            >
            <button
                class="px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white/40 hover:text-white transition-all text-[9px] font-black uppercase tracking-widest"
                >Audit Pixels</button
            >
        </div>
    {/if}
</div>

<style>
    .ad-vortex {
        background: radial-gradient(
                circle at top right,
                rgba(244, 63, 94, 0.05) 0%,
                transparent 70%
            ),
            linear-gradient(
                135deg,
                rgba(16, 24, 39, 0.4) 0%,
                rgba(2, 6, 23, 0.4) 100%
            );
    }

    .vortex-loader {
        width: 32px;
        height: 32px;
        border: 2px solid rgba(244, 63, 94, 0.1);
        border-top-color: #f43f5e;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 2px;
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
