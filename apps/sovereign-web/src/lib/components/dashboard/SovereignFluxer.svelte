<script lang="ts">
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import { sovereignFluxer } from "$lib/services/fluxer-engine.svelte";
    import {
        LucideMic,
        LucideVibrate,
        LucideShieldCheck,
        LucideUsers,
        LucideSettings2,
        LucideSend,
        LucideHash,
        LucideActivity,
    } from "lucide-svelte";

    let currentMessage = $state("");
    let messages = $derived(sovereignFluxer.messages);
    let channels = $derived(sovereignFluxer.channels);

    let activeChannelId = $state("flux-core");

    function sendMessage() {
        if (!currentMessage) return;
        sovereignFluxer.broadcast(currentMessage);
        currentMessage = "";
    }

    onMount(() => {
        // Initial broadcast
        sovereignFluxer.broadcast(
            "Fluxer Manifold Synchronized. Sovereign Communication Active.",
        );
    });
</script>

<div
    class="fluxer-container h-full flex bg-slate-900/60 backdrop-blur-2xl border border-white/10 rounded-3xl overflow-hidden shadow-2xl"
>
    <!-- Sidebar: Channels & Vitals -->
    <div class="w-64 border-r border-white/5 bg-black/40 flex flex-col">
        <div
            class="p-6 border-b border-white/5 flex items-center justify-between"
        >
            <div class="flex items-center gap-2">
                <div
                    class="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-[0_0_10px_#6366f1]"
                ></div>
                <span
                    class="text-white font-bold tracking-tighter text-sm uppercase"
                    >Fluxer DaVinci</span
                >
            </div>
            <LucideSettings2
                size={14}
                class="text-slate-500 hover:text-white cursor-pointer transition-colors"
            />
        </div>

        <!-- Channels List -->
        <div class="flex-1 overflow-y-auto p-4 space-y-6">
            <div>
                <h3
                    class="text-[10px] uppercase text-slate-500 font-bold tracking-widest mb-4 px-2"
                >
                    Sovereign Channels
                </h3>
                <div class="space-y-1">
                    {#each channels as channel}
                        <button
                            onclick={() => (activeChannelId = channel.id)}
                            class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition-all group {activeChannelId ===
                            channel.id
                                ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/20'
                                : 'hover:bg-white/5 text-slate-400'}"
                        >
                            <div class="flex items-center gap-3">
                                {#if channel.type === "text"}
                                    <LucideHash size={14} class="opacity-50" />
                                {:else if channel.type === "voice"}
                                    <LucideMic size={14} class="opacity-50" />
                                {:else}
                                    <LucideVibrate
                                        size={14}
                                        class="opacity-50"
                                    />
                                {/if}
                                <span class="text-xs font-medium"
                                    >{channel.name}</span
                                >
                            </div>
                            {#if channel.activeUsers > 0}
                                <span
                                    class="text-[9px] font-mono opacity-40 group-hover:opacity-100 transition-opacity"
                                    >{channel.activeUsers}</span
                                >
                            {/if}
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Vitals HUD -->
            <div
                class="bg-indigo-500/5 border border-indigo-500/10 rounded-2xl p-4 space-y-3"
            >
                <h3
                    class="text-[10px] uppercase text-indigo-400 font-bold tracking-tighter flex items-center gap-1"
                >
                    <LucideActivity size={10} /> Comm Vitals
                </h3>
                <div class="grid grid-cols-2 gap-3">
                    <div class="space-y-1">
                        <div class="text-[9px] text-slate-500">Latency</div>
                        <div class="text-[11px] font-mono text-white">
                            12.4ms
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="text-[9px] text-slate-500">Encryption</div>
                        <div class="text-[11px] font-mono text-green-400">
                            ZK-98
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Main View: Chat & Swarms -->
    <div class="flex-1 flex flex-col relative overflow-hidden">
        <!-- Background Animation (Flux Swarm) -->
        <div
            class="absolute inset-0 pointer-events-none overflow-hidden opacity-20"
        >
            <div
                class="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 blur-[120px] rounded-full animate-pulse"
            ></div>
            <div
                class="absolute bottom-1/4 right-1/4 w-64 h-64 bg-cyan-500/10 blur-[100px] rounded-full animate-pulse [animation-delay:1.5s]"
            ></div>
        </div>

        <!-- Chat Header -->
        <div
            class="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-black/10"
        >
            <div class="flex items-center gap-4">
                <span class="text-white font-bold text-sm"
                    >#{channels.find((c: any) => c.id === activeChannelId)
                        ?.name}</span
                >
                <span class="text-[10px] text-slate-500 italic opacity-80"
                    >Synchronized via Snowflake Distribution</span
                >
            </div>
            <div class="flex items-center gap-4">
                <div
                    class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/5 text-[10px] text-slate-400"
                >
                    <LucideShieldCheck size={12} class="text-green-500" />
                    <span>End-to-End ZK Shielded</span>
                </div>
                <div
                    class="flex items-center gap-2 text-slate-500 hover:text-white transition-colors cursor-pointer"
                >
                    <LucideUsers size={16} />
                </div>
            </div>
        </div>

        <!-- Messages Feed -->
        <div class="flex-1 overflow-y-auto p-8 space-y-8 scrollbar-hide">
            {#each messages as msg (msg.id)}
                <div in:fly={{ y: 20, duration: 600 }} class="flex gap-5 group">
                    <div
                        class="w-10 h-10 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex-shrink-0 flex items-center justify-center font-bold text-white text-xs border border-white/20 shadow-lg"
                    >
                        {msg.author[0]}
                    </div>
                    <div class="flex-1 space-y-1.5 min-w-0">
                        <div class="flex items-center gap-3">
                            <span
                                class="text-white font-bold text-xs tracking-tight"
                                >{msg.author}</span
                            >
                            <span
                                class="text-[9px] font-mono text-slate-500 uppercase tracking-tighter"
                                >{msg.id.slice(-8)}</span
                            >
                            <span class="text-[9px] text-slate-600 font-mono"
                                >{new Date(
                                    msg.timestamp,
                                ).toLocaleTimeString()}</span
                            >
                        </div>
                        <p
                            class="text-[13px] leading-relaxed text-slate-300 group-hover:text-white transition-colors"
                        >
                            {msg.content}
                        </p>
                        {#if msg.signature}
                            <div
                                class="text-[8px] font-mono text-indigo-500/40 truncate hover:text-indigo-500/80 transition-colors"
                            >
                                SIG: {msg.signature}
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>

        <!-- Message Input -->
        <div class="p-8 pb-10">
            <div class="relative group">
                <input
                    type="text"
                    bind:value={currentMessage}
                    placeholder="Enter message for the DaVinci..."
                    class="w-full bg-slate-950/60 border border-white/10 rounded-2xl p-4 pr-16 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/5 transition-all text-sm text-white placeholder-slate-600 shadow-2xl"
                    onkeydown={(e: KeyboardEvent) => e.key === "Enter" && sendMessage()}
                />
                <button
                    onclick={sendMessage}
                    class="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-xl bg-indigo-500 text-white hover:bg-indigo-400 transition-colors shadow-lg active:scale-95"
                >
                    <LucideSend size={16} />
                </button>
            </div>
            <div
                class="mt-3 flex justify-between px-4 text-[9px] tracking-widest font-bold text-slate-600 uppercase"
            >
                <span>Fluxer Protocol v2.4.0</span>
                <span>Node: {sovereignFluxer.stats.encryption}</span>
            </div>
        </div>
    </div>
</div>

<style>
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
