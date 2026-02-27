<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly } from "svelte/transition";
    import {
        Recycle,
        Zap,
        Cpu,
        Award,
        ArrowUpRight,
        ArrowDownRight,
    } from "lucide-svelte";

    // 🍱 CIRCULAR_GOVERNANCE: DABBA-style community resource loops
    const merits = $derived(manifold.walletState.merits);
    const compute = $derived(manifold.validatorState.computeYieldTflops);
    const circular = $derived(manifold.circularState);

    const resourceFlows = [
        {
            id: "FLOW-01",
            from: "Local_Solar",
            to: "DABBA_Mesh",
            amount: "14.2kW",
            trend: "up",
        },
        {
            id: "FLOW-02",
            from: "DABBA_Mesh",
            to: "Communal_LLM",
            amount: "4.2 TFlops",
            trend: "down",
        },
        {
            id: "FLOW-03",
            from: "Communal_LLM",
            to: "Local_Merit_Pool",
            amount: "120 REP",
            trend: "up",
        },
    ];
</script>

<div
    class="flex flex-col h-full bg-[#0a2e2a]/40 rounded-[2.5rem] border border-emerald-500/10 backdrop-blur-3xl overflow-hidden shadow-2xl relative group"
>
    <!-- Glowing background orbits -->
    <div
        class="absolute -top-10 -right-10 w-40 h-40 bg-emerald-500/5 rounded-full blur-[60px]"
    ></div>
    <div
        class="absolute -bottom-10 -left-10 w-40 h-40 bg-cyan-500/5 rounded-full blur-[60px]"
    ></div>

    <!-- Header -->
    <div class="p-8 pb-4">
        <div class="flex items-center gap-4 mb-4">
            <div
                class="p-3 bg-emerald-400 text-black rounded-2xl shadow-[0_0_20px_rgba(52,211,153,0.3)]"
            >
                <Recycle size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Circular_Governance
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[8px] font-black {circular.status ===
                        'CRISIS'
                            ? 'text-rose-400'
                            : 'text-emerald-400/60'} uppercase tracking-widest"
                        >{circular.ownershipModel} // {circular.status}</span
                    >
                </div>
            </div>
        </div>
    </div>

    <!-- Resource Loops -->
    <div class="flex-1 px-8 space-y-4 overflow-y-auto custom-scrollbar">
        <div class="space-y-2">
            <h3
                class="text-[8px] font-black text-white/20 uppercase tracking-widest mb-3"
            >
                Resource_Flow_Matrix
            </h3>
            {#each resourceFlows as flow}
                <div
                    class="bg-white/[0.02] border border-white/5 p-4 rounded-3xl flex items-center justify-between group/flow hover:bg-white/[0.05] transition-all"
                >
                    <div class="flex items-center gap-3">
                        <div
                            class="w-8 h-8 rounded-xl bg-emerald-500/10 flex items-center justify-center"
                        >
                            {#if flow.from.includes("Solar")}
                                <Zap size={14} class="text-amber-400" />
                            {:else if flow.from.includes("Mesh")}
                                <Cpu size={14} class="text-cyan-400" />
                            {:else}
                                <Award size={14} class="text-emerald-400" />
                            {/if}
                        </div>
                        <div>
                            <div
                                class="text-[9px] font-black text-white uppercase"
                            >
                                {flow.from} → {flow.to}
                            </div>
                            <div
                                class="text-[7px] font-bold text-white/20 uppercase"
                            >
                                Internal_Sovereignty_Rail
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center gap-1 justify-end">
                            <span class="text-[10px] font-black text-white"
                                >{flow.amount}</span
                            >
                            {#if flow.trend === "up"}
                                <ArrowUpRight
                                    size={10}
                                    class="text-emerald-400"
                                />
                            {:else}
                                <ArrowDownRight
                                    size={10}
                                    class="text-rose-400"
                                />
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Ownership Stats -->
        <div class="grid grid-cols-2 gap-4 mt-6">
            <div
                class="bg-black/40 border border-white/5 p-4 rounded-3xl"
                in:fade={{ duration: 400 }}
            >
                <span
                    class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                    >Communal_Merits</span
                >
                <div class="text-xl font-black text-emerald-400">{merits}</div>
                <div
                    class="h-1 w-full bg-white/5 rounded-full mt-2 overflow-hidden"
                >
                    <div
                        class="h-full bg-emerald-400 w-[65%]"
                        style:width="{(merits / 1000) * 100}%"
                    ></div>
                </div>
            </div>
            <div
                class="bg-black/40 border border-white/5 p-4 rounded-3xl"
                in:fly={{ y: 20, delay: 100 }}
            >
                <span
                    class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                    >Mesh_Yield</span
                >
                <div class="text-xl font-black text-cyan-400">
                    {compute.toFixed(1)}T
                </div>
                <div
                    class="h-1 w-full bg-white/5 rounded-full mt-2 overflow-hidden"
                >
                    <div
                        class="h-full bg-cyan-400 w-[99.9%] shadow-[0_0_10px_rgba(34,211,238,0.5)]"
                    ></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer Action -->
    <div class="p-8">
        <button
            class="w-full bg-emerald-500 text-black font-black text-[9px] py-4 rounded-2xl uppercase tracking-[0.2em] hover:bg-emerald-400 transition-all shadow-[0_0_30px_rgba(16,185,129,0.2)]"
        >
            Initiate_Feedback_Loop
        </button>
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
        background: rgba(16, 185, 129, 0.1);
        border-radius: 10px;
    }
</style>
