<script lang="ts">
    import {
        Zap,
        Database,
        Cpu,
        Activity,
        Clock,
        ShieldCheck,
        ChevronRight,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let latency = $state(0.12);
    let opsPerSec = $state(142000);
    let memoryUsage = $state(42); // MB
    let singleThreadActive = $state(true);

    const dataStructures = [
        { type: "Hash", count: 1240, color: "text-cyan-400" },
        { type: "Set", count: 850, color: "text-indigo-400" },
        { type: "Stream", count: 4200, color: "text-emerald-400" },
        { type: "Sorted_Set", count: 320, color: "text-amber-400" },
    ];

    onMount(() => {
        const interval = setInterval(() => {
            latency = Math.max(
                0.08,
                Math.min(0.25, latency + (Math.random() - 0.5) * 0.05),
            );
            opsPerSec = Math.floor(140000 + Math.random() * 5000);
            memoryUsage = Math.min(128, memoryUsage + Math.random() * 0.1);
        }, 2000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="redis-sovereignty-manifold glass-panel-chiaroscuro sfumato-depth-2 elevation-2 p-8 h-full flex flex-col gap-8 relative overflow-hidden group"
>
    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-red-500/10 rounded-2xl text-red-500 border border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.1)]"
            >
                <Database size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Redis_Sovereignty_Engine
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    In-Memory_Foundation // Atomic_Manifest_Governance
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-3 px-4 py-2 bg-emerald-400/10 border border-emerald-400/20 rounded-full"
        >
            <ShieldCheck size={12} class="text-emerald-400" />
            <span
                class="text-[9px] font-black text-emerald-400 uppercase tracking-widest"
                >ATOMIC_LOCK_ENABLED</span
            >
        </div>
    </header>

    <!-- Main Grid -->
    <div class="flex-1 grid grid-cols-2 gap-8 z-10">
        <!-- Left: Single Thread Visualizer -->
        <div class="flex flex-col gap-6">
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center"
            >
                <div class="absolute top-4 left-6 flex items-center gap-2">
                    <Cpu size={14} class="text-red-500" />
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Single_Thread_Core</span
                    >
                </div>

                <!-- Atomic Ring -->
                <div
                    class="relative w-32 h-32 flex items-center justify-center"
                >
                    <div
                        class="absolute inset-0 border-2 border-white/5 rounded-full"
                    ></div>
                    {#if singleThreadActive}
                        <div
                            class="absolute inset-0 border-2 border-red-500 rounded-full border-t-transparent animate-spin"
                            style:animation-duration="0.5s"
                        ></div>
                    {/if}
                    <Zap size={32} class="text-white animate-pulse" />
                </div>
                <span
                    class="text-[10px] font-mono text-white/60 mt-4 tracking-tighter"
                    >THREAD_ID_0x7FFF</span
                >
            </div>

            <!-- Ops/Sec Counter -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-2"
            >
                <div class="flex justify-between items-center">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >Request_Velocity</span
                    >
                    <Activity size={12} class="text-cyan-400" />
                </div>
                <div class="flex items-baseline gap-2">
                    <span class="text-2xl font-black text-white"
                        >{opsPerSec.toLocaleString()}</span
                    >
                    <span class="text-[10px] font-bold text-white/20 uppercase"
                        >OPS/SEC</span
                    >
                </div>
            </div>
        </div>

        <!-- Right: Memory & Data Structures -->
        <div class="flex flex-col gap-6">
            <!-- Memory Meter -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <Clock size={14} class="text-amber-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Latency_Audit</span
                        >
                    </div>
                    <span class="text-xs font-mono text-emerald-400"
                        >{latency.toFixed(2)}ms</span
                    >
                </div>
                <div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                    <div
                        class="h-full bg-emerald-400 shadow-[0_0_10px_#34d399] transition-all duration-700"
                        style:width="{(1 - latency / 0.25) * 100}%"
                    ></div>
                </div>
            </div>

            <!-- Data Structure Grid -->
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
            >
                <span
                    class="text-[8px] font-black text-white/20 uppercase tracking-widest block"
                    >Structural_Sovereignty</span
                >
                <div class="grid grid-cols-2 gap-4 flex-1">
                    {#each dataStructures as ds}
                        <div
                            class="p-4 bg-white/2 border border-white/5 rounded-xl hover:bg-white/5 transition-all group/ds"
                        >
                            <span
                                class="text-[7px] font-black {ds.color} uppercase block mb-1"
                                >{ds.type}</span
                            >
                            <div class="flex justify-between items-center">
                                <span class="text-lg font-black text-white"
                                    >{ds.count}</span
                                >
                                <ChevronRight
                                    size={10}
                                    class="text-white/10 group-hover/ds:translate-x-1 transition-transform"
                                />
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>

    <!-- Background Blueprint -->
    <div
        class="absolute inset-0 opacity-[0.03] pointer-events-none"
        style="background-image: radial-gradient(circle, white 0.5px, transparent 0.5px); background-size: 40px 40px"
    ></div>
</div>
