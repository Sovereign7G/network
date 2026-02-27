<script lang="ts">
    import {
        Zap,
        SquareCode,
        Cpu,
        Binary,
        CheckCircle2,

        AlertTriangle,
        RefreshCcw,
        Sparkles,
        ArrowUpRight,
    } from "lucide-svelte";
    import { fade, fly, slide, scale } from "svelte/transition";


    type Patch = {
        id: string;
        module: string;
        agent: string;
        impact: number;
        status: "PENDING" | "DEPLOYING" | "STABLE";
        description: string;
        diffLines: number;
    };

    let patches = $state<Patch[]>([
        {
            id: "sp-9988-cx",
            module: "CAUSAL_STATE_ENGINE",
            agent: "Devin-v2",
            impact: 15.4,
            status: "PENDING",
            description:
                "Optimization of state rebalancing logic for 10ms synchronization.",
            diffLines: 142,
        },
        {
            id: "sp-9989-fx",
            module: "FORENSIC_MONITOR",
            agent: "Junie-AI",
            impact: 8.2,
            status: "PENDING",
            description:
                "Hardening of AAL3 handshake protocols against recursive dissonance.",
            diffLines: 64,
        },
    ]);

    let isGrowing = $state(false);
    let growthProgress = $state(0);

    function initiateGrowth() {
        isGrowing = true;
        const interval = setInterval(() => {
            growthProgress += 2;
            if (growthProgress >= 100) {
                clearInterval(interval);
                isGrowing = false;
                growthProgress = 0;
            }
        }, 50);
    }
</script>

<div class="space-y-10" in:fade>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div>
            <h2 class="text-4xl font-black italic tracking-tighter uppercase">
                AUTONOMOUS_GROWTH
            </h2>
            <p
                class="text-[10px] mono-font text-white/40 uppercase tracking-[0.4em] mt-1"
            >
                Self-Evolving Substrate Orchestration
            </p>
        </div>
        <button
            onclick={initiateGrowth}
            disabled={isGrowing}
            class="px-8 py-4 bg-neon-cyan text-black font-black uppercase tracking-tighter text-sm rounded-2xl hover:scale-105 active:scale-95 disabled:opacity-20 transition-all flex items-center gap-3"
        >
            <Sparkles size={18} /> INITIALIZE_SUBSYSTEM_SPAWN
        </button>
    </div>

    <!-- Growth Visualization (Canvas Proxy) -->
    <div
        class="h-64 glass-panel relative overflow-hidden flex items-center justify-center bg-black/60 border-white/[0.03]"
    >
        <div
            class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,242,255,0.05)_0%,transparent_70%)]"
        ></div>

        {#if isGrowing}
            <div class="text-center space-y-6" in:scale>
                <div class="relative">
                    <div
                        class="w-40 h-40 border-4 border-neon-cyan/10 border-t-neon-cyan rounded-full animate-spin"
                    ></div>
                    <div
                        class="absolute inset-0 flex items-center justify-center"
                    >
                        <Binary
                            size={40}
                            class="text-neon-cyan animate-pulse"
                        />
                    </div>
                </div>
                <div>
                    <span
                        class="text-lg font-black italic tracking-widest text-[#24AE7C]"
                        >{growthProgress}%</span
                    >
                    <p
                        class="text-[8px] mono-font text-white/30 uppercase tracking-[0.3em] mt-2"
                    >
                        SCAFFOLDING_NEW_GOVERNANCE_SHARD...
                    </p>
                </div>
            </div>
        {:else}
            <div class="grid grid-cols-4 gap-4 w-full px-12 opacity-40">
                {#each Array(4) as _}
                    <div
                        class="h-32 bg-white/5 border border-white/10 rounded-2xl flex flex-col items-center justify-center gap-3"
                    >
                        <div
                            class="w-10 h-10 rounded-lg bg-white/5 animate-pulse"
                        ></div>
                        <div class="h-1 w-12 bg-white/10 rounded-full"></div>
                    </div>
                {/each}
            </div>
            <div
                class="absolute inset-0 flex flex-col items-center justify-center text-center"
            >
                <Cpu size={48} class="text-white/10 mb-4" />
                <span
                    class="text-[10px] font-black uppercase tracking-[0.4em] text-white/20"
                    >AGENTIC_SUBSTRATE_IDLE</span
                >
            </div>
        {/if}
    </div>

    <!-- Sovereign Patch Interface -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="glass-panel p-8 bg-black/40 border-white/[0.03] space-y-6">
            <div class="flex items-center gap-3">
                <SquareCode size={20} class="text-neon-cyan" />
                <h3 class="text-sm font-black uppercase tracking-widest">
                    PENDING_SOVEREIGN_PATCHES
                </h3>
            </div>

            <div class="space-y-4">
                {#each patches as patch}
                    <div
                        class="p-6 bg-white/[0.02] border border-white/5 rounded-2xl group hover:border-white/10 transition-all"
                    >
                        <div class="flex justify-between items-start mb-4">
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-8 h-8 rounded-lg bg-[#24AE7C]/10 flex items-center justify-center text-[#24AE7C]"
                                >
                                    <Zap size={14} />
                                </div>
                                <div>
                                    <span
                                        class="text-[10px] font-black uppercase tracking-tight"
                                        >{patch.id}</span
                                    >
                                    <span
                                        class="text-[7px] mono-font text-white/20 uppercase block"
                                        >{patch.module}</span
                                    >
                                </div>
                            </div>
                            <div
                                class="px-2 py-0.5 bg-amber-400/10 border border-amber-400/20 rounded text-amber-400 text-[8px] font-black uppercase"
                            >
                                IMPACT: +{patch.impact}%
                            </div>
                        </div>
                        <p
                            class="text-[10px] text-white/40 leading-relaxed mb-6"
                        >
                            {patch.description}
                        </p>
                        <div class="flex items-center justify-between">
                            <span
                                class="text-[8px] mono-font text-white/20 uppercase tracking-widest"
                                >Author: {patch.agent} (+{patch.diffLines} lines)</span
                            >
                            <button
                                class="px-4 py-2 bg-white/5 hover:bg-[#24AE7C] hover:text-black rounded-lg text-[9px] font-black uppercase tracking-widest transition-all"
                            >
                                DEPLOY_PATCH
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <div class="glass-panel p-8 bg-black/40 border-white/[0.03] space-y-6">
            <div class="flex items-center gap-3">
                <RefreshCcw size={20} class="text-amber-400" />
                <h3 class="text-sm font-black uppercase tracking-widest">
                    SUBSTRATE_FORENSIC_LOG
                </h3>
            </div>

            <div
                class="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar"
            >
                {#each Array(5) as _, i}
                    <div
                        class="flex gap-4 p-4 border-l-2 border-white/5 hover:border-neon-cyan transition-all"
                    >
                        <span
                            class="text-[8px] mono-font text-white/20 mt-1 uppercase"
                            >09:5{i}:21</span
                        >
                        <div>
                            <span
                                class="text-[9px] font-black uppercase tracking-widest text-white/80 block"
                                >AGENT_HANDSHAKE_INITIATED</span
                            >
                            <p
                                class="text-[8px] text-white/30 uppercase tracking-widest mt-1"
                            >
                                Autonomous expansion of the WealthMaturity
                                module successfully completed by
                                Council-Agent-07.
                            </p>
                        </div>
                    </div>
                {/each}
            </div>

            <button
                class="w-full py-4 border border-white/5 bg-white/[0.02] hover:bg-white/5 rounded-xl text-[9px] font-black uppercase tracking-widest text-white/40 flex items-center justify-center gap-2"
            >
                VIEW_FULL_FORENSIC_SPEC_SHEET <ArrowUpRight size={14} />
            </button>
        </div>
    </div>

    <!-- Security Alert -->
    <div
        class="p-8 bg-red-500/5 border border-red-500/20 rounded-[2.5rem] flex items-center gap-6"
    >
        <div class="p-4 bg-red-500/10 rounded-2xl text-red-500">
            <AlertTriangle size={32} />
        </div>
        <div>
            <h4
                class="text-xs font-black uppercase tracking-widest text-red-500"
            >
                AUTONOMOUS_CONSENT_WARNING
            </h4>
            <p
                class="text-[10px] text-white/30 leading-relaxed mt-1 max-w-2xl uppercase tracking-widest"
            >
                Enabling autonomous growth grants AI shards the permission to
                modify the protocol's secondary memory layers. All primary state
                changes still require explicit Citizen Consent via the Deep-Auth
                Handshake.
            </p>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    @keyframes scan {
        0% {
            transform: translateY(-100%);
        }
        100% {
            transform: translateY(100%);
        }
    }
</style>
