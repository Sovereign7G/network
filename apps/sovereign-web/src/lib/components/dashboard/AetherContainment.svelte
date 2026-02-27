<script lang="ts">
    import { Box, Zap, Layers, ShieldCheck, Activity } from "lucide-svelte";
    import { onMount } from "svelte";

    let wasmNodes = $state([
        { id: "w1", name: "Logic_Shard_01", status: "Active", health: 98 },
        { id: "w2", name: "Logic_Shard_02", status: "Active", health: 100 },
        { id: "w3", name: "Logic_Shard_03", status: "Optimizing", health: 94 },
    ]);

    let dockerNodes = $state([
        {
            id: "d1",
            name: "Institutional_Pod_A",
            status: "Stabilized",
            load: 42,
        },
        { id: "d2", name: "Institutional_Pod_B", status: "Active", load: 18 },
    ]);

    let connectionFlow = $state(true);

    onMount(() => {
        const interval = setInterval(() => {
            wasmNodes.forEach((node) => {
                if (Math.random() > 0.8)
                    node.health = Math.min(
                        100,
                        node.health + (Math.random() - 0.5) * 2,
                    );
            });
            dockerNodes.forEach((node) => {
                if (Math.random() > 0.8)
                    node.load = Math.max(
                        0,
                        Math.min(100, node.load + (Math.random() - 0.5) * 5),
                    );
            });
        }, 2000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="aether-containment-hub bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-6 h-full flex flex-col gap-6 relative overflow-hidden group"
>
    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-3 bg-indigo-500/10 rounded-2xl text-indigo-400 border border-indigo-500/20"
            >
                <Box size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.3em] text-white"
                >
                    Aether_Hydra_Hub
                </h2>
                <span
                    class="text-[8px] font-black text-white/30 uppercase italic"
                    >Better Together // Multi-Runtime Manifold</span
                >
            </div>
        </div>
        <div
            class="flex items-center gap-2 px-3 py-1 bg-emerald-400/10 border border-emerald-400/20 rounded-full"
        >
            <ShieldCheck size={10} class="text-emerald-400" />
            <span class="text-[8px] font-black text-emerald-400 uppercase"
                >Synchronized_Security</span
            >
        </div>
    </header>

    <!-- Visualizer Area -->
    <div class="flex-1 flex gap-4 min-h-[250px] relative z-10">
        <!-- Wasm Side (Aether) -->
        <div class="flex-1 flex flex-col gap-4">
            <div class="flex items-center justify-between px-2">
                <span
                    class="text-[9px] font-black text-indigo-400 uppercase tracking-widest"
                    >Wasm_Aether</span
                >
                <Zap size={10} class="text-indigo-400 animate-pulse" />
            </div>
            <div class="flex-1 space-y-3">
                {#each wasmNodes as node}
                    <div
                        class="p-4 bg-indigo-500/5 border border-indigo-500/10 rounded-2xl group/node hover:border-indigo-500/40 transition-all"
                    >
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-[10px] font-bold text-white/80"
                                >{node.name}</span
                            >
                            <span
                                class="text-[8px] font-black text-indigo-400 uppercase"
                                >{node.status}</span
                            >
                        </div>
                        <div
                            class="h-1 w-full bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="h-full bg-indigo-500 shadow-[0_0_10px_#6366f1] transition-all duration-1000"
                                style:width="{node.health}%"
                            ></div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Central Conduit -->
        <div class="w-8 flex flex-col items-center justify-center gap-2">
            <div
                class="flex-1 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent relative"
            >
                {#if connectionFlow}
                    <div
                        class="absolute top-0 left-1/2 -translate-x-1/2 w-1 h-32 bg-gradient-to-b from-transparent via-cyan-400 to-transparent animate-flow-down"
                    ></div>
                    <div
                        class="absolute bottom-0 left-1/2 -translate-x-1/2 w-1 h-32 bg-gradient-to-t from-transparent via-cyan-400 to-transparent animate-flow-up"
                    ></div>
                {/if}
            </div>
            <Activity size={14} class="text-cyan-400 animate-pulse" />
            <div
                class="flex-1 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent"
            ></div>
        </div>

        <!-- Docker Side (Vessel) -->
        <div class="flex-1 flex flex-col gap-4">
            <div class="flex items-center justify-between px-2 text-right">
                <Layers size={10} class="text-sky-400" />
                <span
                    class="text-[9px] font-black text-sky-400 uppercase tracking-widest"
                    >Docker_Vessel</span
                >
            </div>
            <div class="flex-1 space-y-3">
                {#each dockerNodes as node}
                    <div
                        class="p-4 bg-sky-500/5 border border-sky-500/10 rounded-2xl group/node hover:border-sky-500/40 transition-all"
                    >
                        <div class="flex justify-between items-center mb-2">
                            <span
                                class="text-[8px] font-black text-sky-400 uppercase"
                                >{node.status}</span
                            >
                            <span class="text-[10px] font-bold text-white/80"
                                >{node.name}</span
                            >
                        </div>
                        <div
                            class="h-1 w-full bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="h-full bg-sky-500 shadow-[0_0_10px_#0ea5e9] transition-all duration-1000"
                                style:width="{node.load}%"
                            ></div>
                        </div>
                    </div>
                {/each}
                <div
                    class="p-3 border border-dashed border-white/5 rounded-2xl flex items-center justify-center opacity-40"
                >
                    <span class="text-[8px] font-black uppercase text-white/20"
                        >Awaiting_Institutional_Scale</span
                    >
                </div>
            </div>
        </div>
    </div>

    <!-- Metrics Footer -->
    <footer
        class="mt-auto pt-4 border-t border-white/5 flex justify-between items-center z-10"
    >
        <div class="flex gap-4">
            <div class="flex flex-col">
                <span class="text-[7px] font-black text-white/20 uppercase"
                    >Runtime_Efficiency</span
                >
                <span class="text-[11px] font-black text-white"
                    >+84% Improvement</span
                >
            </div>
            <div class="flex flex-col">
                <span class="text-[7px] font-black text-white/20 uppercase"
                    >Startup_Latency</span
                >
                <span class="text-[11px] font-black text-indigo-400"
                    >12ms (Aether)</span
                >
            </div>
        </div>
        <button
            class="px-4 py-2 bg-white text-black text-[9px] font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-all"
        >
            Scale_Manifold
        </button>
    </footer>

    <!-- Background Decoration -->
    <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(99,102,241,0.05),transparent_60%)] pointer-events-none"
    ></div>
</div>

<style>
    @keyframes flow-down {
        0% {
            transform: translate(-50%, -100%);
            opacity: 0;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            transform: translate(-50%, 200%);
            opacity: 0;
        }
    }
    @keyframes flow-up {
        0% {
            transform: translate(-50%, 100%);
            opacity: 0;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            transform: translate(-50%, -200%);
            opacity: 0;
        }
    }
    .animate-flow-down {
        animation: flow-down 4s linear infinite;
    }
    .animate-flow-up {
        animation: flow-up 5s linear infinite;
    }
</style>
