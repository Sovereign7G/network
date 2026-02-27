<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Server,
        ShieldCheck,
        Cpu,
        HardDrive,
        Network,
    } from "lucide-svelte";

    const infrastructure = $derived(manifold.validatorState);

    function getStatusColor(status: string) {
        switch (status) {
            case "VALIDATING":
                return "text-emerald-400";
            case "SYNCING":
                return "text-amber-400";
            case "IDLE":
                return "text-white/40";
            default:
                return "text-rose-400";
        }
    }
</script>

<div
    class="flex flex-col h-full bg-slate-900/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="p-4 bg-white/5 rounded-2xl text-cyan-400">
                <Server size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Validator_Registry
                </h2>
                <button
                    class="text-[9px] font-black text-white/30 uppercase tracking-widest hover:text-rose-400 transition-colors"
                    onclick={() => manifold.decayValidatorReputation()}
                >
                    Active_Nodes: {infrastructure.activeValidators}/{infrastructure.totalNodes}
                </button>
            </div>
        </div>
        <div
            class="px-4 py-2 bg-black/40 border border-white/10 rounded-2xl text-right"
        >
            <div class="text-[7px] font-black text-white/20 uppercase mb-0.5">
                Total_Staked_AGE
            </div>
            <div class="text-xs font-black text-white">
                {(infrastructure.totalStakedAge / 1000000).toFixed(1)}M
            </div>
        </div>
    </div>

    <!-- Compute Yield HUD -->
    <div
        class="bg-gradient-to-br from-cyan-400/10 to-transparent p-6 rounded-[2.5rem] border border-cyan-400/20 relative overflow-hidden group/hud"
    >
        <div
            class="absolute -right-4 -top-4 text-cyan-400/10 rotate-12 transition-transform group-hover/hud:scale-125 duration-700"
        >
            <Cpu size={120} />
        </div>
        <div class="relative z-10 flex flex-col gap-2">
            <div class="flex items-center gap-2">
                <Cpu size={14} class="text-cyan-400" />
                <span
                    class="text-[9px] font-black text-cyan-400 uppercase tracking-widest"
                    >Aggregate_Compute_Yield</span
                >
            </div>
            <div class="flex items-center justify-between">
                <div
                    class="text-4xl font-black text-white italic tracking-tighter flex items-end gap-3"
                >
                    {infrastructure.computeYieldTflops.toFixed(1)}
                    <div class="flex flex-col mb-1">
                        <span
                            class="text-[9px] font-black text-cyan-400 not-italic"
                            >+{(infrastructure.neuralLiquidity || 0).toFixed(0)}
                            NEURAL_BOOST</span
                        >
                        <span
                            class="text-[8px] font-black text-white/20 not-italic uppercase tracking-tighter"
                            >TFLOPS_AGGREGATE</span
                        >
                    </div>
                </div>
                <button
                    class="p-4 bg-emerald-400 text-black text-[9px] font-black uppercase tracking-widest rounded-2xl hover:brightness-110 active:scale-95 transition-all shadow-lg flex items-center gap-2"
                    onclick={() => manifold.issueSyntheticMerits()}
                >
                    <ShieldCheck size={14} />
                    Issue_Merits
                </button>
            </div>
        </div>
    </div>

    <!-- Node List -->
    <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
        <h3
            class="text-[9px] font-black text-white/20 uppercase tracking-widest px-2 mb-2"
        >
            Regional_Edge_Nodes
        </h3>
        {#each infrastructure.nodes as node (node.id)}
            <div
                class="bg-white/5 border border-white/5 p-4 rounded-2xl hover:border-cyan-400/20 transition-all flex items-center justify-between group/node"
            >
                <div class="flex items-center gap-4">
                    <div
                        class="p-2 bg-black/40 rounded-xl {getStatusColor(
                            node.status,
                        )}"
                    >
                        <ShieldCheck size={16} />
                    </div>
                    <div>
                        <h4
                            class="text-[11px] font-black text-white uppercase group-hover/node:text-cyan-400 transition-colors"
                        >
                            {node.id}
                        </h4>
                        <div class="flex items-center gap-2">
                            <span class="text-[8px] font-mono text-white/20"
                                >STAKE: {(node.stake / 1000).toFixed(0)}K AGE</span
                            >
                            <span
                                class="text-[8px] font-mono text-white/20 border-l border-white/10 pl-2"
                                >UPTIME: {(node.uptime * 100).toFixed(1)}%</span
                            >
                            <span
                                class="text-[8px] font-mono {node.reputation >
                                0.8
                                    ? 'text-emerald-400/40'
                                    : 'text-rose-400/40'} border-l border-white/10 pl-2"
                                >REP: {(node.reputation * 100).toFixed(
                                    1,
                                )}%</span
                            >
                        </div>
                    </div>
                </div>
                <div class="text-right">
                    <span
                        class="text-[9px] font-black {getStatusColor(
                            node.status,
                        )} uppercase tracking-widest">{node.status}</span
                    >
                </div>
            </div>
        {/each}
    </div>

    <!-- Footnote -->
    <div
        class="mt-auto flex items-center justify-between pt-4 border-t border-white/5"
    >
        <div
            class="flex items-center gap-2 text-[8px] font-black text-white/20 uppercase"
        >
            <Network size={12} />
            <span>Planetary_Gossip_Relay (Ring 0)</span>
        </div>
        <div
            class="flex items-center gap-2 text-[8px] font-black text-white/20 uppercase"
        >
            <HardDrive size={12} />
            <span>0xED_STAKES: CONSISTENT</span>
        </div>
    </div>
</div>
