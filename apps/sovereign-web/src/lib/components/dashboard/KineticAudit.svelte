<script lang="ts">
    import {
        Zap,
        Play,
        Repeat,
        Activity,
        ShieldCheck,
        ChevronRight,
        Wind,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let currentState = $state("MANIFESTING");
    let frameRate = $state(60);
    let compositorLoad = $state(4); // %

    const keyframeLogs = [
        { id: 1, stage: "0%", action: "Initialize_Scale", status: "Passed" },
        {
            id: 2,
            stage: "50%",
            action: "Chromatic_Transition",
            status: "Passed",
        },
        {
            id: 3,
            stage: "100%",
            action: "Persistence_Applied",
            status: "Passed",
        },
    ];

    onMount(() => {
        const interval = setInterval(() => {
            frameRate = Math.floor(59 + Math.random() * 2);
            compositorLoad = Math.max(
                2,
                Math.min(8, compositorLoad + (Math.random() - 0.5)),
            );
        }, 2000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="kinetic-audit-manifold bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group"
>
    <!-- CSS Internal Animation Style -->
    <style>
        @keyframes pulse-ring {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.7);
                opacity: 1;
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(168, 85, 247, 0);
                opacity: 0.5;
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(168, 85, 247, 0);
                opacity: 1;
            }
        }
        @keyframes flow-gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        .kinetic-pulse {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        .kinetic-gradient {
            background: linear-gradient(
                -45deg,
                #a855f7,
                #ec4899,
                #3b82f6,
                #10b981
            );
            background-size: 400% 400%;
            animation: flow-gradient 15s ease infinite;
        }
    </style>

    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-purple-500/10 rounded-2xl text-purple-400 border border-purple-500/20 shadow-[0_0_20px_rgba(168,85,247,0.1)]"
            >
                <Wind size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Kinetic_Audit_Loom
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Compositor_Sovereignty // Keyframe_Orchestration
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-3 px-4 py-2 bg-purple-400/10 border border-purple-400/20 rounded-full"
        >
            <ShieldCheck size={12} class="text-purple-400" />
            <span
                class="text-[9px] font-black text-purple-400 uppercase tracking-widest"
                >HARDWARE_ACCELERATED</span
            >
        </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 grid grid-cols-2 gap-8 z-10">
        <!-- Left: Visualization -->
        <div class="flex flex-col gap-6">
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center kinetic-gradient"
            >
                <div
                    class="absolute inset-0 bg-black/40 backdrop-blur-[2px]"
                ></div>

                <div
                    class="relative z-10 w-32 h-32 flex items-center justify-center"
                >
                    <div
                        class="absolute inset-0 rounded-full kinetic-pulse"
                    ></div>
                    <div
                        class="w-16 h-16 bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl flex items-center justify-center rotate-45 group-hover:rotate-180 transition-transform duration-[2000ms] ease-in-out"
                    >
                        <Zap
                            size={24}
                            class="text-white -rotate-45 group-hover:rotate-[-180deg] transition-transform duration-[2000ms]"
                        />
                    </div>
                </div>

                <div class="mt-6 flex gap-2 z-10">
                    <span
                        class="text-[8px] font-black text-white/60 uppercase tracking-widest bg-black/40 px-3 py-1 rounded-full border border-white/10"
                        >{currentState}</span
                    >
                </div>
            </div>

            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 flex justify-between items-center"
            >
                <div class="flex flex-col gap-1">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >Render_Frequency</span
                    >
                    <div class="flex items-baseline gap-2">
                        <span class="text-2xl font-black text-white"
                            >{frameRate}</span
                        >
                        <span
                            class="text-[10px] font-bold text-white/20 uppercase"
                            >FPS</span
                        >
                    </div>
                </div>
                <Activity size={24} class="text-purple-400 opacity-20" />
            </div>
        </div>

        <!-- Right: Metrics & Logs -->
        <div class="flex flex-col gap-6">
            <!-- Compositor Load -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <Play size={14} class="text-emerald-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Compositor_Load</span
                        >
                    </div>
                    <span class="text-xs font-mono text-emerald-400"
                        >{compositorLoad.toFixed(1)}%</span
                    >
                </div>
                <div
                    class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden"
                >
                    <div
                        class="h-full bg-emerald-400 shadow-[0_0_10px_#34d399] transition-all duration-700"
                        style:width="{compositorLoad * 10}%"
                    ></div>
                </div>
            </div>

            <!-- Keyframe Audit Feed -->
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
            >
                <div class="flex justify-between items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                        >Keyframe_Audit_Sync</span
                    >
                    <Repeat size={12} class="text-white/10" />
                </div>
                <div
                    class="space-y-3 overflow-y-auto max-h-[150px] custom-scrollbar"
                >
                    {#each keyframeLogs as log}
                        <div
                            class="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/5 hover:border-purple-500/30 transition-all hover:bg-white/10 group/log"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="text-[9px] font-black text-purple-400 w-8"
                                >
                                    {log.stage}
                                </div>
                                <div class="flex flex-col">
                                    <span
                                        class="text-[9px] font-bold text-white/80"
                                        >{log.action}</span
                                    >
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase"
                                        >Verify_Manifest</span
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
        class="absolute inset-0 opacity-[0.02] pointer-events-none"
        style="background-image: radial-gradient(circle, white 0.5px, transparent 0.5px); background-size: 40px 40px;"
    ></div>
</div>
