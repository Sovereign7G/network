<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";

    import { Shield, BarChart3, RefreshCw, AlertTriangle } from "lucide-svelte";

    const localEconomy = $derived(manifold.localEconomyState);
    const lll = $derived(manifold.lllState);

    function getStatusClass(status: string) {
        switch (status) {
            case "STABLE":
                return "text-emerald-400 border-emerald-400/20 bg-emerald-400/5";
            case "BREACH":
                return "text-rose-400 border-rose-400/20 bg-rose-400/10 animate-pulse";
            case "QUARANTINE":
                return "text-amber-400 border-amber-400/20 bg-amber-400/5";
            default:
                return "text-white/40 border-white/10";
        }
    }
</script>

<div
    class="flex flex-col h-full bg-zinc-900/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-6 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div
                class="p-4 bg-emerald-500 rounded-2xl shadow-[0_0_30px_rgba(16,185,129,0.3)] text-black"
            >
                <Shield size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Local_Economy_HUD
                </h2>
                <span
                    class="text-[9px] font-black text-emerald-400 uppercase tracking-widest"
                    >{localEconomy.zoneId}</span
                >
            </div>
        </div>
        <div
            class={`px-4 py-2 border rounded-full text-[9px] font-black uppercase tracking-widest ${getStatusClass(localEconomy.status)}`}
        >
            {localEconomy.status}
        </div>
    </div>

    <!-- 0x5C Invariants -->
    <div class="space-y-4">
        <div class="flex items-center justify-between px-2">
            <h3
                class="text-[9px] font-black text-white/20 uppercase tracking-widest"
            >
                0x5C_Invariant_Set (LCL)
            </h3>
            <span class="text-[8px] font-bold text-white/20 uppercase"
                >Locality: Radius_0</span
            >
        </div>

        <div class="grid grid-cols-1 gap-3">
            {#each localEconomy.invariants as inv}
                <div
                    class="bg-black/40 border border-white/5 p-4 rounded-3xl flex items-center justify-between group/inv"
                >
                    <div class="flex items-center gap-4">
                        <div
                            class={`w-2 h-2 rounded-full ${inv.status === "PASS" ? "bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.5)]" : "bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.5)]"}`}
                        ></div>
                        <div>
                            <div
                                class="text-[10px] font-black text-white uppercase"
                            >
                                {inv.name}
                            </div>
                            <div
                                class="text-[8px] font-bold text-white/20 uppercase"
                            >
                                Threshold: >{inv.threshold}
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div
                            class={`text-xs font-black ${inv.status === "PASS" ? "text-white" : "text-rose-400"}`}
                        >
                            {(inv.value * 100).toFixed(0)}%
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    </div>

    <!-- 0x5E Conflict Arbiter (LLL) -->
    <div
        class="bg-indigo-500/10 border border-indigo-500/20 rounded-[2rem] p-6 relative overflow-hidden group/lll"
    >
        <div
            class="absolute -right-4 -bottom-4 text-indigo-500/10 rotate-12 group-hover/lll:scale-110 transition-transform duration-700"
        >
            <RefreshCw size={80} />
        </div>

        <div class="relative z-10 space-y-3">
            <div class="flex items-center gap-2">
                <BarChart3 size={14} class="text-indigo-400" />
                <span
                    class="text-[9px] font-black text-indigo-400 uppercase tracking-widest"
                    >Conflict_Arbiter (0x5E)</span
                >
            </div>

            <div class="flex items-end justify-between">
                <div>
                    <div
                        class="text-2xl font-black text-white tracking-widest uppercase"
                    >
                        {lll.status}
                    </div>
                    <div
                        class="text-[8px] font-black text-white/40 uppercase tracking-widest"
                    >
                        Algorithm: {lll.resolutionAlgorithm}
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-xs font-black text-white">
                        {lll.avgRoundsToConvergence}
                    </div>
                    <div
                        class="text-[8px] font-black text-white/40 uppercase tracking-widest"
                    >
                        Convergence_Rounds
                    </div>
                </div>
            </div>

            <!-- Dissonance Progress Bar -->
            <div class="space-y-1">
                <div
                    class="flex justify-between text-[7px] font-black text-indigo-400/60 uppercase"
                >
                    <span>Dissonance_Level</span>
                    <span
                        >{(lll.peakDissonance * 100).toFixed(1)}%</span
                    >
                </div>
                <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                    <div
                        class="h-full bg-indigo-400 shadow-[0_0_10px_rgba(129,140,248,0.5)] transition-all duration-500"
                        style:width="{lll.peakDissonance * 100}%"
                    ></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Action Bar -->
    <div class="mt-auto flex flex-col gap-3">
        <div class="flex gap-4">
            <button
                onclick={() => manifold.runLCLBreachSimulation()}
                class="flex-1 bg-rose-500/10 border border-rose-500/20 hover:bg-rose-500 hover:text-white transition-all py-3 rounded-2xl flex items-center justify-center gap-2 group/sim"
            >
                <AlertTriangle
                    size={14}
                    class="group-hover:sim:animate-bounce"
                />
                <span class="text-[9px] font-black uppercase tracking-widest"
                    >Simulate_Breach</span
                >
            </button>
            <button
                onclick={() => manifold.rebalanceLocalEconomy()}
                class="p-4 bg-white/5 border border-white/10 hover:border-emerald-500/50 rounded-2xl text-white/40 hover:text-emerald-400 transition-colors"
            >
                <RefreshCw size={14} />
            </button>
        </div>

        <!-- Future Potential: Reality & Thermal -->
        <div class="grid grid-cols-2 gap-3 pt-2">
            <div class="bg-black/20 border border-white/5 p-3 rounded-2xl">
                <div class="text-[7px] font-black text-white/20 uppercase mb-1">
                    Reality_Integrity (0x5E)
                </div>
                <div class="flex items-center gap-2">
                    <div
                        class="flex-1 h-0.5 bg-white/5 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full bg-cyan-400 w-[98%] shadow-[0_0_5px_rgba(34,211,238,0.5)]"
                        ></div>
                    </div>
                    <span class="text-[8px] font-black text-white">0.98</span>
                </div>
            </div>
            <div class="bg-black/20 border border-white/5 p-3 rounded-2xl">
                <div class="text-[7px] font-black text-white/20 uppercase mb-1">
                    Thermal_Load (0x5C)
                </div>
                <div class="flex items-center gap-2">
                    <div
                        class="flex-1 h-0.5 bg-white/5 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full bg-amber-400 w-[42%] shadow-[0_0_5px_rgba(251,191,36,0.5)]"
                        ></div>
                    </div>
                    <span class="text-[8px] font-black text-white">42%</span>
                </div>
            </div>
        </div>
    </div>
</div>
