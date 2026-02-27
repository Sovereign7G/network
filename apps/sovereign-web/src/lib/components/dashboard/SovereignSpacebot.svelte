<script lang="ts">
    import { onMount } from "svelte";
    import { fade, slide, scale, fly } from "svelte/transition";
    import { sovereignOpenCode } from "$lib/services/opencode-engine.svelte";
    import {
        LucideActivity,
        LucideBrain,
        LucideZap,
        LucideDatabase,
        LucideUsers,
        LucideSend,
        LucideLayers,
    } from "lucide-svelte";

    let intent = $state("");
    let bots = $derived(sovereignOpenCode.activeBackgroundAgents);
    let spaceMemory = $derived(sovereignOpenCode.allSpaceMemory);
    let logs = $state<string[]>([]);

    function dispatchIntent() {
        if (!intent) return;

        const currentIntent = intent;
        intent = "";

        // Spacebot dispatch logic: Always concurrent
        sovereignOpenCode.spawnBackground({
            agentRole: "spacebot",
            prompt: currentIntent,
            category: "ultrabrain",
        });

        logs = [
            `[Spacebot] Dispatching concurrent intent: ${currentIntent}`,
            ...logs,
        ].slice(0, 50);

        // Simulate multi-step spacebot execution
        setTimeout(() => {
            sovereignOpenCode.saveToSpace(`intent_${Date.now()}`, {
                query: currentIntent,
                status: "ANALYZED",
                entropy: Math.random(),
            });
            logs = [
                `[Space Intelligence] Context synthesized for "${currentIntent.slice(0, 20)}..."`,
                ...logs,
            ];
        }, 1500);
    }

    onMount(() => {
        logs = ["Spacebot Hub Active. Non-blocking concurrency engaged."];
    });
</script>

<div
    class="spacebot-container h-full flex flex-col bg-slate-950/40 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden font-mono text-xs text-slate-300"
>
    <!-- Header: Space Status -->
    <div
        class="p-4 border-b border-white/5 bg-white/5 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <div
                class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#22d3ee]"
            ></div>
            <span
                class="text-white font-bold tracking-widest text-[10px] uppercase"
                >Space Intelligence Hub</span
            >
        </div>
        <div class="flex gap-4">
            <div class="flex items-center gap-1 opacity-60">
                <LucideActivity size={12} class="text-cyan-400" />
                <span>{bots.length} Active Swarms</span>
            </div>
            <div class="flex items-center gap-1 opacity-60">
                <LucideDatabase size={12} class="text-purple-400" />
                <span>{spaceMemory.length} Memory Shards</span>
            </div>
        </div>
    </div>

    <!-- Main View: Split Layout -->
    <div class="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-2">
        <!-- Left: Action & Bots -->
        <div
            class="p-4 flex flex-col gap-4 border-r border-white/5 bg-slate-900/20"
        >
            <div class="relative group">
                <input
                    type="text"
                    bind:value={intent}
                    placeholder="Broadcast intent to the Space..."
                    class="w-full bg-slate-950 border border-white/10 rounded-lg p-3 pl-10 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all text-sm"
                    onkeydown={(e: KeyboardEvent) => e.key === "Enter" && dispatchIntent()}
                />
                <LucideSend
                    size={16}
                    class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-cyan-400"
                />
            </div>

            <!-- Bot Swarm -->
            <div class="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin">
                <h3
                    class="text-[10px] uppercase text-slate-500 font-bold tracking-tighter mb-2 flex items-center gap-1"
                >
                    <LucideUsers size={10} /> Active Bot Swarms
                </h3>
                {#each bots as bot (bot.taskId)}
                    <div
                        in:scale={{ duration: 400, start: 0.95 }}
                        out:fade
                        class="bg-slate-900/50 border border-white/5 p-3 rounded-lg flex gap-3 items-start relative overflow-hidden group"
                    >
                        <div
                            class="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"
                        ></div>
                        <div
                            class="p-2 rounded-md bg-cyan-500/10 text-cyan-400"
                        >
                            <LucideBrain size={16} class="animate-pulse" />
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="flex justify-between mb-1">
                                <span
                                    class="text-white font-bold text-[10px] uppercase tracking-wider"
                                    >{bot.agentRole}</span
                                >
                                <span
                                    class="text-[8px] text-cyan-400/60 font-mono tracking-tighter"
                                    >{bot.taskId}</span
                                >
                            </div>
                            <p
                                class="text-[11px] leading-relaxed line-clamp-2 italic opacity-80"
                            >
                                "{bot.prompt}"
                            </p>
                            <div
                                class="mt-2 h-1 bg-slate-800 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-cyan-500 animate-[loading_2s_ease-in-out_infinite]"
                                    style="width: 30%"
                                ></div>
                            </div>
                        </div>
                    </div>
                {:else}
                    <div
                        class="h-32 flex flex-col items-center justify-center opacity-20 grayscale"
                    >
                        <LucideActivity size={32} class="mb-2" />
                        <span class="text-[10px] uppercase"
                            >Quiescent State</span
                        >
                    </div>
                {/each}
            </div>
        </div>

        <!-- Right: Memory & Logs -->
        <div class="p-4 flex flex-col gap-4 bg-slate-950/20">
            <!-- Memory Shards (Space Intelligence) -->
            <div class="h-1/2 flex flex-col">
                <h3
                    class="text-[10px] uppercase text-purple-500 font-bold tracking-tighter mb-3 flex items-center gap-1"
                >
                    <LucideLayers size={10} /> Space Memory Shards
                </h3>
                <div
                    class="flex-1 overflow-y-auto grid grid-cols-2 gap-2 pr-2 scrollbar-thin"
                >
                    {#each spaceMemory as [key, value] (key)}
                        <div
                            in:fly={{ y: 10 }}
                            class="p-2 bg-purple-500/5 border border-purple-500/10 rounded-md hover:border-purple-500/30 transition-colors"
                        >
                            <div
                                class="text-[8px] text-purple-400 font-bold truncate mb-1"
                            >
                                {key}
                            </div>
                            <div class="text-[9px] opacity-60 truncate">
                                {typeof value === "object"
                                    ? JSON.stringify(value).slice(1, 30)
                                    : value}
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- Institutional Logs -->
            <div class="h-1/2 border-t border-white/5 pt-4 flex flex-col">
                <h3
                    class="text-[10px] uppercase text-orange-500 font-bold tracking-tighter mb-3 flex items-center gap-1"
                >
                    <LucideZap size={10} /> Concurrent Log Stream
                </h3>
                <div
                    class="flex-1 overflow-y-auto space-y-1 p-2 bg-black/40 rounded border border-white/5 font-mono text-[9px] text-slate-400 scrollbar-thin"
                >
                    {#each logs as log}
                        <div
                            transition:slide
                            class="py-0.5 border-l-2 border-slate-800 pl-2 hover:bg-white/5"
                        >
                            <span class="text-slate-600"
                                >[{new Date().toLocaleTimeString()}]</span
                            >
                            {log}
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>

    <!-- Footer: System Vitals -->
    <div
        class="px-4 py-2 bg-slate-950 border-t border-white/5 flex items-center justify-between opacity-50 text-[9px]"
    >
        <div class="flex gap-4">
            <span>UPTIME: 144H 21M</span>
            <span>LATENCY: 12MS</span>
            <span class="text-cyan-400">NON-BLOCKING: ACTIVE</span>
        </div>
        <div class="font-bold tracking-widest uppercase">
            AGE-SPACEBOT-OS v1.0.4
        </div>
    </div>
</div>

<style>
    @keyframes loading {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(300%);
        }
    }

    .scrollbar-thin::-webkit-scrollbar {
        width: 3px;
    }
    .scrollbar-thin::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
    }
</style>
