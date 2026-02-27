<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import { Cpu, Zap, Lock, Activity, Network, Maximize2, Box } from "lucide-svelte";

    const hilbert = $derived(manifold.hilbertState);
    const compute = $derived(manifold.computeMarket);
    const veAge = $derived(manifold.veAgeState);

    let activeTab = $state("hilbert"); // 'hilbert' | 'compute' | 'veage'

    function getComplexityColor(c: number) {
        if (c > 0.8) return "text-cyan-400";
        if (c > 0.5) return "text-emerald-400";
        return "text-amber-400";
    }
</script>

<div
    class="flex flex-col h-full bg-zinc-950/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex gap-4">
            {#each ["hilbert", "compute", "veage"] as tab}
                <button
                    onclick={() => (activeTab = tab)}
                    class="text-[9px] font-black uppercase tracking-[0.2em] transition-all pb-2 border-b-2 {activeTab ===
                    tab
                        ? 'text-white border-cyan-400'
                        : 'text-white/20 border-transparent hover:text-white/40'}"
                >
                    {tab}
                </button>
            {/each}
        </div>
        <div
            class="flex items-center gap-2 px-4 py-1 bg-white/5 rounded-full border border-white/5"
        >
            <Activity size={12} class="text-cyan-400" />
            <span class="text-[8px] font-black text-white/60 uppercase"
                >High_Density_Plane</span
            >
        </div>
    </div>

    <!-- Content Area -->
    <div class="flex-1 overflow-hidden">
        {#if activeTab === "hilbert"}
            <div in:fade class="h-full flex flex-col gap-6">
                <!-- Hilbert Index -->
                <div
                    class="p-8 bg-gradient-to-br from-white/5 to-transparent rounded-[2.5rem] border border-white/5 text-center relative overflow-hidden group"
                >
                    <div
                        class="absolute inset-0 opacity-10 flex items-center justify-center pointer-events-none group-hover:scale-110 transition-transform duration-700"
                    >
                        <Box size={120} />
                    </div>
                    <span
                        class="text-[9px] font-black text-white/20 uppercase tracking-[0.4em] mb-4 block"
                        >Hilbert_Sovereignty_Index</span
                    >
                    <div
                        class="text-6xl font-black text-white tracking-tighter italic mb-2"
                    >
                        {hilbert.index.toFixed(4)}
                    </div>
                    <div class="flex justify-center gap-4 mt-6">
                        {#each hilbert.stabilityVector as val, i}
                            <div class="flex flex-col gap-1">
                                <div
                                    class="w-1 h-8 bg-white/5 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="bg-cyan-400 w-full"
                                        style="height: {val * 100}%"
                                    ></div>
                                </div>
                                <span
                                    class="text-[6px] font-black text-white/20"
                                    >D{i + 1}</span
                                >
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Hilbert Metrics -->
                <div class="grid grid-cols-2 gap-4">
                    <div
                        class="p-4 bg-black/40 rounded-2xl border border-white/5"
                    >
                        <span
                            class="text-[8px] font-black text-white/20 uppercase block mb-1"
                            >Dimensions</span
                        >
                        <span class="text-xl font-black text-white italic"
                            >{hilbert.dimension}D</span
                        >
                    </div>
                    <div
                        class="p-4 bg-black/40 rounded-2xl border border-white/5"
                    >
                        <span
                            class="text-[8px] font-black text-white/20 uppercase block mb-1"
                            >Complexity</span
                        >
                        <span
                            class="text-xl font-black {getComplexityColor(
                                hilbert.curveComplexity,
                            )} italic"
                            >{(hilbert.curveComplexity * 100).toFixed(1)}%</span
                        >
                    </div>
                </div>
            </div>
        {:else if activeTab === "compute"}
            <div in:fade class="h-full flex flex-col gap-6">
                <!-- GPU Market HUD -->
                <div
                    class="p-6 bg-cyan-400/5 rounded-3xl border border-cyan-400/10 flex items-center justify-between"
                >
                    <div>
                        <span
                            class="text-[8px] font-black text-cyan-400/40 uppercase tracking-widest block mb-1"
                            >Active_Compute_Nodes</span
                        >
                        <div
                            class="text-3xl font-black text-white tracking-tighter italic"
                        >
                            {compute.activeGpus.toLocaleString()}
                            <span class="text-sm text-cyan-400/60 uppercase"
                                >GPUs</span
                            >
                        </div>
                    </div>
                    <div class="text-right">
                        <span
                            class="text-[8px] font-black text-cyan-400/40 uppercase tracking-widest block mb-1"
                            >Total_Capacity</span
                        >
                        <div class="text-xl font-black text-white">
                            {(compute.totalTflops / 1000).toFixed(1)} PFLOPs
                        </div>
                    </div>
                </div>

                <!-- Workforce -->
                <div class="flex-1 space-y-3 overflow-y-auto no-scrollbar">
                    {#each compute.workloads as job}
                        <div
                            class="p-4 bg-white/5 rounded-2xl border border-white/5 flex items-center justify-between hover:bg-white/10 transition-all"
                        >
                            <div class="flex items-center gap-4">
                                <div class="p-2 bg-white/5 rounded-lg">
                                    <Cpu size={14} class="text-white/40" />
                                </div>
                                <div>
                                    <div
                                        class="text-[10px] font-black text-white uppercase"
                                    >
                                        {job.type}
                                    </div>
                                    <div
                                        class="text-[8px] text-white/30 font-bold uppercase tracking-widest"
                                    >
                                        {job.id} <span class="px-1">//</span>
                                        {job.tflops} TFLOPs
                                    </div>
                                </div>
                            </div>
                            <div class="text-right">
                                <div
                                    class="text-[10px] font-black text-amber-400"
                                >
                                    {job.reward} AGE
                                </div>
                                <div
                                    class="text-[8px] font-black text-cyan-400/60 uppercase tracking-widest"
                                >
                                    {job.status}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- Footer Stats -->
                <div class="grid grid-cols-2 gap-4 mt-auto">
                    <div
                        class="flex items-center gap-3 p-3 bg-black/40 rounded-xl border border-white/5"
                    >
                        <Activity size={12} class="text-emerald-400" />
                        <div>
                            <div
                                class="text-[7px] font-black text-white/20 uppercase"
                            >
                                Demand_Index
                            </div>
                            <div class="text-[10px] font-black text-white">
                                {(compute.demandIndex * 100).toFixed(1)}%
                            </div>
                        </div>
                    </div>
                    <div
                        class="flex items-center gap-3 p-3 bg-black/40 rounded-xl border border-white/5"
                    >
                        <Zap size={12} class="text-amber-400" />
                        <div>
                            <div
                                class="text-[7px] font-black text-white/20 uppercase"
                            >
                                Price/TFLOP
                            </div>
                            <div class="text-[10px] font-black text-white">
                                {compute.pricePerTflopAge} AGE
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {:else if activeTab === "veage"}
            <div in:fade class="h-full flex flex-col gap-6">
                <!-- veAGE Stake Display -->
                <div
                    class="p-8 bg-zinc-900 rounded-[2.5rem] border border-white/10 relative overflow-hidden"
                >
                    <div class="absolute right-0 top-0 p-8 opacity-5">
                        <Lock size={80} />
                    </div>
                    <span
                        class="text-[9px] font-black text-white/20 uppercase tracking-[0.4em] mb-2 block"
                        >Vote-Escrowed_Equity</span
                    >
                    <div
                        class="text-4xl font-black text-white tracking-tighter italic mb-4"
                    >
                        {(veAge.veAgeSupply / 1000000).toFixed(2)}M
                        <span class="text-sm text-white/40 font-black uppercase"
                            >veAGE</span
                        >
                    </div>
                    <div class="flex gap-8">
                        <div>
                            <div
                                class="text-[8px] font-black text-white/20 uppercase mb-1"
                            >
                                Total_Locked
                            </div>
                            <div class="text-sm font-black text-white">
                                {(veAge.totalLockedAge / 1000000).toFixed(1)}M
                                AGE
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[8px] font-black text-white/20 uppercase mb-1"
                            >
                                Avg_Lock
                            </div>
                            <div class="text-sm font-black text-cyan-400">
                                {veAge.averageLockTimeYears}y
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Gauge Voting -->
                <div class="space-y-4">
                    <h3
                        class="text-[9px] font-black text-white/20 uppercase tracking-widest px-2"
                    >
                        Institutional_Gauges
                    </h3>
                    <div class="space-y-3">
                        {#each veAge.gauges as gauge}
                            <div class="space-y-2">
                                <div
                                    class="flex justify-between items-center px-2"
                                >
                                    <span
                                        class="text-[10px] font-black text-white/60 uppercase tracking-wider"
                                        >{gauge.name}</span
                                    >
                                    <span
                                        class="text-[10px] font-black text-cyan-400"
                                        >{(gauge.weight * 100).toFixed(
                                            0,
                                        )}%</span
                                    >
                                </div>
                                <div
                                    class="h-1.5 bg-white/5 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="h-full bg-cyan-400/40"
                                        style="width: {gauge.weight * 100}%"
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <!-- Footer Meta -->
    <div
        class="mt-auto pt-6 border-t border-white/5 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <Maximize2 size={14} class="text-white/20" />
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest italic"
                >Multi-Dimensional Liquidity Fabric v2.4</span
            >
        </div>
        <div class="flex items-center gap-2">
            <Network size={12} class="text-emerald-400" />
            <span
                class="text-[8px] font-black text-emerald-400 uppercase tracking-widest"
                >Topology: Optimistic</span
            >
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
</style>
