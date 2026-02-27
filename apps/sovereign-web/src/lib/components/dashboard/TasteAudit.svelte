<script lang="ts">
    import {
        Sparkles,
        Heart,
        PencilRuler,
        Eye,
        Zap,
        ShieldCheck,
        ChevronRight,
    } from "lucide-svelte";
    // import { fade, fly, scale } from "svelte/transition";
    import { designEngineering } from "$lib/services/design-engineering-engine.svelte";

    let tasteScore = $derived(designEngineering.tasteScore);
    let intentionalityIndex = $derived(designEngineering.moralMerits);
    let foundationIntegrity = $derived(designEngineering.foundationIntegrity);
    let eniScore = $derived(designEngineering.eniScore);

    const auditFeed = [
        {
            id: 1,
            type: "Taste",
            message: "Visceral_Rightness_Detected",
            status: "Passed",
        },
        {
            id: 2,
            type: "Polish",
            message: "Anti-Slop_Filter_Active",
            status: "Verified",
        },
        {
            id: 3,
            type: "Performance",
            message: "Human-Centric_Latency_Audit",
            status: "Passed",
        },
        {
            id: 4,
            type: "Sovereignty",
            message: "Intentionality_Checksum_Stable",
            status: "Secure",
        },
    ];
</script>

<div
    class="taste-audit-manifold bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group font-sans"
>
    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-fuchsia-500/10 rounded-2xl text-fuchsia-400 border border-fuchsia-500/20 shadow-[0_0_20px_rgba(217,70,239,0.1)]"
            >
                <Sparkles size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Taste_Audit_Loom
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Design_Engineering_v1 // Anti-Slop_Protocol
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-3 px-4 py-2 bg-fuchsia-400/10 border border-fuchsia-400/20 rounded-full"
        >
            <ShieldCheck size={12} class="text-fuchsia-400" />
            <span
                class="text-[9px] font-black text-fuchsia-400 uppercase tracking-widest"
                >INTENTIONAL_DESIGN</span
            >
        </div>
    </header>

    <!-- Metrics Grid -->
    <div class="flex-1 grid grid-cols-2 gap-8 z-10">
        <!-- Left: Taste Multiplier -->
        <div class="flex flex-col gap-6">
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center"
            >
                <div class="absolute top-4 left-6 flex items-center gap-2">
                    <Heart size={14} class="text-fuchsia-500" />
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Taste_Multiplier</span
                    >
                </div>

                <div
                    class="relative w-32 h-32 flex items-center justify-center"
                >
                    <svg class="w-full h-full -rotate-90">
                        <circle
                            cx="64"
                            cy="64"
                            r="60"
                            fill="none"
                            class="stroke-white/5"
                            stroke-width="8"
                        />
                        <circle
                            cx="64"
                            cy="64"
                            r="60"
                            fill="none"
                            class="stroke-fuchsia-500 transition-all duration-1000"
                            stroke-width="8"
                            stroke-dasharray="377"
                            stroke-dashoffset={377 * (1 - tasteScore / 100)}
                        />
                    </svg>
                    <div
                        class="absolute inset-0 flex flex-col items-center justify-center"
                    >
                        <span class="text-3xl font-black text-white"
                            >{tasteScore.toFixed(0)}</span
                        >
                        <span
                            class="text-[8px] font-black text-fuchsia-400 uppercase"
                            >QUALITY</span
                        >
                    </div>
                </div>
                <span
                    class="text-[9px] font-mono text-white/20 mt-4 tracking-[0.2em]"
                    >BY_DESIGN_ENGINEER</span
                >
            </div>

            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-2"
            >
                <div class="flex justify-between items-center">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >Intentionality_Index</span
                    >
                    <PencilRuler size={12} class="text-white/40" />
                </div>
                <div class="flex items-baseline gap-2">
                    <span class="text-2xl font-black text-white"
                        >{intentionalityIndex}%</span
                    >
                    <span class="text-[10px] font-bold text-white/20 uppercase"
                        >STABLE</span
                    >
                </div>
                <div
                    class="h-1 w-full bg-white/5 rounded-full overflow-hidden mt-2"
                >
                    <div
                        class="h-full bg-fuchsia-400"
                        style:width="{intentionalityIndex}%"
                    ></div>
                </div>
            </div>
        </div>

        <!-- Right: Retention & Audit -->
        <div class="flex flex-col gap-6">
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <ShieldCheck size={14} class="text-emerald-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Foundation_Integrity</span
                        >
                    </div>
                    <span class="text-xs font-mono text-emerald-400"
                        >{foundationIntegrity.toFixed(1)}%</span
                    >
                </div>
                <div
                    class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden"
                >
                    <div
                        class="h-full bg-emerald-400 shadow-[0_0_10px_#10b981]"
                        style:width="{foundationIntegrity}%"
                    ></div>
                </div>
                <button
                    onclick={() =>
                        designEngineering.verifyFoundation(
                            "Dashboard_Sensory_Terminal",
                        )}
                    class="w-full py-2 bg-white/5 border border-white/10 rounded-xl text-[8px] font-black uppercase text-white/40 hover:bg-white/10 hover:text-white transition-all"
                >
                    Trigger_Anti-Jump_Verification
                </button>
            </div>

            <!-- ENI Metric -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <Zap size={14} class="text-fuchsia-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Product_Mastery_ENI</span
                        >
                    </div>
                    <span class="text-xs font-mono text-fuchsia-400"
                        >{eniScore.toFixed(0)}</span
                    >
                </div>
                <div
                    class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden"
                >
                    <div
                        class="h-full bg-fuchsia-400 shadow-[0_0_10px_#d946ef]"
                        style:width="{eniScore}%"
                    ></div>
                </div>
            </div>

            <!-- Audit Loom -->
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
            >
                <div class="flex justify-between items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                        >Audit_Loom_Logs</span
                    >
                    <Eye size={12} class="text-white/10" />
                </div>
                <div
                    class="space-y-3 overflow-y-auto max-h-[150px] custom-scrollbar"
                >
                    {#each auditFeed as log}
                        <div
                            class="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/5 hover:border-fuchsia-500/30 transition-all hover:bg-white/10 group/log"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-1.5 h-1.5 rounded-full bg-fuchsia-400 animate-pulse"
                                ></div>
                                <div class="flex flex-col">
                                    <span
                                        class="text-[9px] font-bold text-white/80"
                                        >{log.message}</span
                                    >
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase"
                                        >{log.type}</span
                                    >
                                </div>
                            </div>
                            <ChevronRight
                                size={10}
                                class="text-white/10 group-hover/log:translate-x-1 transition-all"
                            />
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>

    <!-- Background Blueprint -->
    <div
        class="absolute inset-0 opacity-[0.03] pointer-events-none"
        style="background-image: radial-gradient(circle, white 0.5px, transparent 0.5px); background-size: 30px 30px;"
    ></div>
</div>
