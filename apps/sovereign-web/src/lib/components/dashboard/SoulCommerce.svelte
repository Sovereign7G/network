<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { api } from "$lib/services/api";

    let campaigns: any[] = $state([]);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            campaigns = await api.request("/social/influence");
        } catch (error) {
            console.error("Failed to load influence data", error);
        } finally {
            isLoading = false;
        }
    });

    function getStatusClass(status: string) {
        switch (status) {
            case "ACTIVE":
                return "text-emerald-400 bg-emerald-400/5";
            case "PENDING_AUDIT":
                return "text-amber-400 bg-amber-400/5";
            default:
                return "text-white/20 bg-white/5";
        }
    }
</script>

<div class="soul-commerce glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-start mb-8">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Soul Commerce // Attention Flow
            </h3>
            <p class="text-[9px] text-white/20 uppercase font-bold">
                Verifiable reach & social dividends
            </p>
        </div>
        <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></div>
            <span class="text-[8px] font-black text-rose-500 uppercase"
                >Live Mesh Graph</span
            >
        </div>
    </div>

    {#if isLoading}
        <div class="flex-1 flex items-center justify-center">
            <div class="soul-loader"></div>
        </div>
    {:else}
        <div class="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
            {#each campaigns as node, i}
                <div
                    class="campaign-node bg-white/[0.02] border border-white/5 p-4 rounded-2xl group hover:border-white/10 transition-all"
                    in:fly={{ y: 20, delay: i * 100 }}
                >
                    <div class="flex justify-between items-start mb-4">
                        <div class="flex items-center gap-3">
                            <div
                                class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-lg shadow-inner"
                            >
                                👤
                            </div>
                            <div>
                                <span
                                    class="text-[10px] font-black text-white group-hover:text-cyan-400 transition-colors"
                                    >@{node.influencer}</span
                                >
                                <div class="flex items-center gap-1.5 mt-0.5">
                                    <span
                                        class="text-[8px] font-bold text-white/20 uppercase tracking-tighter"
                                        >Reach: {node.reach}</span
                                    >
                                    <span class="text-[8px] text-white/10"
                                        >•</span
                                    >
                                    <span
                                        class="text-[8px] font-bold text-cyan-400/60 lowercase italic"
                                        >{node.campaign}</span
                                    >
                                </div>
                            </div>
                        </div>
                        <span
                            class="text-[8px] font-black uppercase px-2 py-1 rounded-md {getStatusClass(
                                node.status,
                            )}">{node.status}</span
                        >
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div class="stat-box">
                            <span
                                class="text-[7px] font-black uppercase text-white/20 block mb-1"
                                >Engagement</span
                            >
                            <div class="flex items-end gap-1">
                                <span class="text-xs font-black text-white"
                                    >{(node.engagement * 100).toFixed(1)}%</span
                                >
                                <div class="flex gap-0.5 mb-1">
                                    <div
                                        class="w-0.5 h-1 bg-cyan-400/20 rounded-full"
                                    ></div>
                                    <div
                                        class="w-0.5 h-2 bg-cyan-400/40 rounded-full"
                                    ></div>
                                    <div
                                        class="w-0.5 h-3 bg-cyan-400 rounded-full"
                                    ></div>
                                </div>
                            </div>
                        </div>
                        <div class="stat-box">
                            <span
                                class="text-[7px] font-black uppercase text-white/20 block mb-1"
                                >Soul Payout</span
                            >
                            <span class="text-xs font-black text-white"
                                >{node.payout.toLocaleString()}
                                {node.currency}</span
                            >
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <button
            class="mt-6 w-full py-3 bg-white text-black text-[9px] font-black uppercase tracking-[0.2em] rounded-xl hover:bg-cyan-400 transition-all flex items-center justify-center gap-2 group"
        >
            <span>Initiate Campaign Protocol</span>
            <span class="group-hover:translate-x-1 transition-transform">→</span
            >
        </button>
    {/if}
</div>

<style>
    .soul-commerce {
        background: linear-gradient(
            135deg,
            rgba(16, 24, 39, 0.4) 0%,
            rgba(2, 6, 23, 0.4) 100%
        );
        backdrop-filter: blur(40px);
    }

    .stat-box {
        background: rgba(255, 255, 255, 0.02);
        padding: 0.75rem;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }

    .soul-loader {
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

    .custom-scrollbar::-webkit-scrollbar {
        width: 2px;
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
