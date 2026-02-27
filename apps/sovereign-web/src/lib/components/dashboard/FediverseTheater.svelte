<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { slide } from "svelte/transition";
    import {
        Share2,
        MessageSquare,
        AlertCircle,
        TrendingUp,
        User,
    } from "lucide-svelte";

    const state = $derived(manifold.fediverseState);

    function getTypeColor(type: string) {
        switch (type) {
            case "ALERT":
                return "text-rose-400";
            case "REVENUE":
                return "text-emerald-400";
            case "INFO":
                return "text-cyan-400";
            default:
                return "text-white/40";
        }
    }

    function formatTime(ts: number) {
        const diff = Date.now() - ts;
        if (diff < 60000) return "Just now";
        return `${Math.floor(diff / 60000)}m ago`;
    }
</script>

<div
    class="flex flex-col h-full bg-[#1a1c2c]/60 rounded-[2.5rem] border border-white/5 backdrop-blur-3xl overflow-hidden shadow-2xl relative group"
>
    <!-- Header -->
    <div class="p-8 pb-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div
                class="p-3 bg-indigo-500 rounded-2xl shadow-[0_0_20px_rgba(99,102,241,0.3)]"
            >
                <Share2 size={20} class="text-white" />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Fediverse_Theater
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                        >Active_Instances: {state.activeInstances}</span
                    >
                    <div
                        class="w-1 h-1 rounded-full bg-emerald-400 animate-pulse"
                    ></div>
                </div>
            </div>
        </div>
        <div class="text-right">
            <div class="text-[7px] font-black text-white/20 uppercase mb-1">
                Veto_Budget
            </div>
            <div class="flex gap-1 justify-end">
                {#each Array(5) as _, i}
                    <div
                        class="w-3 h-1 rounded-full {i < state.vetoBudget
                            ? 'bg-amber-400'
                            : 'bg-white/5'}"
                    ></div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Signal Feed -->
    <div class="flex-1 overflow-y-auto px-6 space-y-4 custom-scrollbar">
        {#each state.signals as signal (signal.id)}
            <div
                in:slide={{ duration: 400 }}
                class="bg-white/[0.02] border border-white/5 p-4 rounded-3xl hover:bg-white/[0.05] transition-all group/item"
            >
                <div class="flex items-start gap-4">
                    <div
                        class="w-10 h-10 rounded-2xl bg-black/40 border border-white/10 flex items-center justify-center shrink-0"
                    >
                        {#if signal.type === "ALERT"}
                            <AlertCircle size={18} class="text-rose-400" />
                        {:else if signal.type === "REVENUE"}
                            <TrendingUp size={18} class="text-emerald-400" />
                        {:else}
                            <User size={18} class="text-white/40" />
                        {/if}
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center justify-between mb-1">
                            <span
                                class="text-[10px] font-black text-white truncate max-w-[120px]"
                                >{signal.actor}</span
                            >
                            <span
                                class="text-[8px] font-bold text-white/20 uppercase shrink-0"
                                >{formatTime(signal.timestamp)}</span
                            >
                        </div>
                        <p
                            class="text-[11px] leading-relaxed text-white/70 italic"
                        >
                            "{signal.content}"
                        </p>
                    </div>
                </div>
                <div
                    class="mt-3 flex items-center gap-4 pt-3 border-t border-white/[0.03]"
                >
                    <div class="flex items-center gap-1">
                        <MessageSquare size={10} class="text-white/20" />
                        <span
                            class="text-[8px] font-black text-white/20 uppercase"
                            >Reply</span
                        >
                    </div>
                    <div class="flex items-center gap-1">
                        <Share2 size={10} class="text-white/20" />
                        <span
                            class="text-[8px] font-black text-white/20 uppercase"
                            >Boost</span
                        >
                    </div>
                    <div class="ml-auto">
                        <span
                            class="text-[8px] font-black {getTypeColor(
                                signal.type,
                            )} uppercase tracking-widest">{signal.type}</span
                        >
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <!-- Stats Bar -->
    <div class="p-6 pt-4 mt-auto">
        <div
            class="bg-black/40 rounded-3xl p-4 border border-white/5 flex items-center justify-between"
        >
            <div class="flex flex-col">
                <span
                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                    >Global_Reputation</span
                >
                <span class="text-xs font-black text-white text-emerald-400"
                    >{(state.globalReputation * 100).toFixed(1)}%</span
                >
            </div>
            <div class="h-8 w-px bg-white/5"></div>
            <div class="flex flex-col text-right">
                <span
                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                    >Laminar_Stability</span
                >
                <span class="text-xs font-black text-cyan-400 uppercase"
                    >Coherent</span
                >
            </div>
        </div>
    </div>
</div>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
