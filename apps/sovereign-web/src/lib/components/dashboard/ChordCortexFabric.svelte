<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    
    import { Cpu, Wind, Share2 } from "lucide-svelte";

    // 🎇 CHORDCORTEX FABRIC: The Neural Control Plane
    const zones = $derived(manifold.kernelState.zones);
    const lanes = $derived(manifold.kernelState.lanes);
</script>

<div
    class="flex flex-col h-full bg-black/60 rounded-[2.5rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-[0_30px_60px_-12px_rgba(0,0,0,0.5)]"
>
    <!-- Fabric Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="p-3 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full text-white shadow-[0_0_20px_rgba(34,211,238,0.3)]"
            >
                <Share2 size={20} />
            </div>
            <div>
                <h2
                    class="text-sm font-black italic uppercase tracking-tighter text-white"
                >
                    ChordCortex_Fabric
                </h2>
                <div class="flex items-center gap-2">
                    <div
                        class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"
                    ></div>
                    <span
                        class="text-[8px] font-black text-emerald-400/60 uppercase tracking-widest"
                        >Global_Tick Active // {manifold.resonance.toFixed(
                            1,
                        )}Hz</span
                    >
                </div>
            </div>
        </div>
        <div class="text-right">
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                >System Posture</span
            >
            <div
                class="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-[9px] font-black text-white uppercase mt-1"
            >
                BALANCED_RISK
            </div>
        </div>
    </div>

    <!-- The Lanes (Compute Rails) -->
    <div class="space-y-4">
        <h3
            class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em] border-b border-white/5 pb-2"
        >
            Active_Lanes
        </h3>
        <div class="grid grid-cols-1 gap-3">
            {#each lanes as lane}
                <div
                    class="group relative bg-white/5 border border-white/5 rounded-2xl p-4 hover:bg-white/10 transition-all cursor-pointer"
                >
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <Cpu size={14} class="text-cyan-400" />
                            <span
                                class="text-[10px] font-black text-white/80 uppercase tracking-widest"
                                >{lane.name}</span
                            >
                        </div>
                        <span class="text-[9px] font-black text-cyan-400"
                            >{lane.traffic}% Load</span
                        >
                    </div>
                    <div
                        class="h-1 w-full bg-white/10 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full bg-gradient-to-r from-cyan-400 to-blue-500 transition-all duration-1000"
                            style:width="{lane.traffic}%"
                        ></div>
                    </div>
                    <!-- Particle effect on hover -->
                    <div
                        class="absolute inset-x-4 bottom-0 h-px bg-cyan-400 scale-x-0 group-hover:scale-x-100 transition-transform origin-center"
                    ></div>
                </div>
            {/each}
        </div>
    </div>

    <!-- Zone Snapshots (Geographic Roots) -->
    <div class="mt-auto">
        <h3
            class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em] mb-4"
        >
            Regional_Orchestration
        </h3>
        <div class="grid grid-cols-2 gap-4">
            {#each zones as zone}
                <div
                    class="p-4 bg-black/40 border border-white/5 rounded-2xl space-y-3"
                >
                    <div class="flex items-center gap-2">
                        <div
                            class="w-2 h-2 rounded-sm bg-white/20 rotate-45"
                        ></div>
                        <span class="text-[9px] font-black text-white uppercase"
                            >{zone.label}</span
                        >
                    </div>
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <span
                                class="block text-[7px] font-black text-white/20 uppercase"
                                >Moral_Score</span
                            >
                            <span
                                class="text-lg font-black {zone.color} tracking-tighter"
                                >{zone.moral}</span
                            >
                        </div>
                        <div class="text-right">
                            <span
                                class="block text-[7px] font-black text-white/20 uppercase"
                                >State</span
                            >
                            <span
                                class="text-[7px] font-black text-white uppercase"
                                >{zone.status}</span
                            >
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    </div>

    <!-- Fabric Sync Status -->
    <div
        class="p-3 bg-cyan-400/5 border border-cyan-400/10 rounded-xl flex items-center justify-between"
    >
        <div class="flex items-center gap-2">
            <Wind size={12} class="text-cyan-400 animate-bounce" />
            <span class="text-[8px] font-black text-cyan-400/60 uppercase"
                >Soliton_Phase_Lock // [0x42-RES]</span
            >
        </div>
        <div class="flex items-center gap-1">
            {#each Array(5) as _}
                <div
                    class="w-1 h-3 bg-cyan-400/20 rounded-full overflow-hidden"
                >
                    <div
                        class="h-full bg-cyan-400 animate-pulse"
                        style="animation-delay: {Math.random() * 2}s"
                    ></div>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    /* Premium neural fabric animations */
</style>
