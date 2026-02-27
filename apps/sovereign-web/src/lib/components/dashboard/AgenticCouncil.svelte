<script lang="ts">
    import {
        Users,
        Mic,
        MicOff,
        Video,
        VideoOff,

        MoreHorizontal,
        Activity,
        ShieldCheck,
        Zap,
        Layers,
    } from "lucide-svelte";
    import { fade, fly, scale } from "svelte/transition";


    type ShardParticipant = {
        id: string;
        name: string;
        status: "ACTIVE" | "SYNCING" | "IDLE";
        integrity: number;
        isSpeaking: boolean;
        color: string;
    };

    let participants = $state<ShardParticipant[]>([
        {
            id: "alpha-01",
            name: "Alpha Merit Node",
            status: "ACTIVE",
            integrity: 0.999,
            isSpeaking: true,
            color: "text-neon-cyan",
        },
        {
            id: "hub-merit",
            name: "Central Merit Hub",
            status: "ACTIVE",
            integrity: 0.998,
            isSpeaking: false,
            color: "text-amber-400",
        },
        {
            id: "vault-cx",
            name: "Sovereign Vault CX",
            status: "SYNCING",
            integrity: 0.992,
            isSpeaking: false,
            color: "text-purple-400",
        },
        {
            id: "node-7782",
            name: "Forensics Node 7782",
            status: "IDLE",
            integrity: 1.0,
            isSpeaking: false,
            color: "text-green-400",
        },
    ]);

    let activeSpeakerId = $state("alpha-01");


    // Simulate "Speaking" changes
    setInterval(() => {
        const randomIndex = Math.floor(Math.random() * participants.length);
        participants.forEach((p, i) => (p.isSpeaking = i === randomIndex));
        activeSpeakerId = participants[randomIndex].id;
    }, 5000);
</script>

<div class="space-y-8" in:fade>
    <div class="flex items-center justify-between">
        <div>
            <h2 class="text-3xl font-black italic tracking-tighter uppercase">
                AGENTIC_COUNCIL
            </h2>
            <p
                class="text-[10px] mono-font text-white/40 uppercase tracking-[0.3em] mt-1"
            >
                Real-Time Shard Coordination Session
            </p>
        </div>
        <div class="flex items-center gap-3">
            <div
                class="px-4 py-2 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-2"
            >
                <div
                    class="w-2 h-2 rounded-full bg-red-500 animate-pulse"
                ></div>
                <span
                    class="text-[9px] font-black text-red-500 uppercase tracking-widest"
                    >LIVE_COMMAND</span
                >
            </div>
            <div
                class="px-4 py-2 bg-white/5 border border-white/10 rounded-xl flex items-center gap-2 text-white/60"
            >
                <Users size={14} />
                <span class="text-[9px] font-black uppercase tracking-widest"
                    >{participants.length} SHARDS</span
                >
            </div>
        </div>
    </div>

    <!-- Council Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {#each participants as shard}
            <div
                class="glass-panel p-6 relative overflow-hidden group transition-all duration-500 hover:border-white/20
                {shard.isSpeaking
                    ? 'border-neon-cyan/40 bg-neon-cyan/[0.02] ring-1 ring-neon-cyan/20'
                    : 'bg-black/40 border-white/[0.03]'}"
            >
                <div
                    class="flex justify-between items-start mb-10 relative z-10"
                >
                    <div class="flex items-center gap-3">
                        <div
                            class="w-10 h-10 rounded-2xl bg-white/5 flex items-center justify-center {shard.color}"
                        >
                            <Layers size={20} />
                        </div>
                        <div>
                            <h4
                                class="text-sm font-black uppercase tracking-tight"
                            >
                                {shard.name}
                            </h4>
                            <div class="flex items-center gap-2">
                                <span
                                    class="text-[8px] mono-font text-white/30 uppercase"
                                    >{shard.id}</span
                                >
                                <div
                                    class="w-1 h-1 rounded-full {shard.status ===
                                    'ACTIVE'
                                        ? 'bg-green-400'
                                        : 'bg-amber-400'} animate-pulse"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button
                            class="p-2 bg-white/5 rounded-lg text-white/20 hover:text-white/60 transition-colors"
                        >
                            {#if shard.isSpeaking}
                                <Mic size={14} class="text-neon-cyan" />
                            {:else}
                                <MicOff size={14} />
                            {/if}
                        </button>
                        <button
                            class="p-2 bg-white/5 rounded-lg text-white/20 hover:text-white/60 transition-colors"
                        >
                            <MoreHorizontal size={14} />
                        </button>
                    </div>
                </div>

                <!-- 3D Fragment Proxy (GSAP visualization) -->
                <div class="h-40 flex items-center justify-center relative">
                    <div
                        class="w-32 h-32 bg-black border border-white/5 rounded-full flex items-center justify-center relative overflow-hidden group-hover:scale-110 transition-transform duration-700"
                        style="box-shadow: 0 0 40px rgba(0,0,0,0.8), inset 0 0 20px rgba(255,255,255,0.05);"
                    >
                        <!-- Scan line -->
                        <div
                            class="absolute inset-0 bg-gradient-to-b from-transparent via-white/[0.02] to-transparent animate-[scan_3s_linear_infinite]"
                        ></div>

                        <!-- Pulse Ring -->
                        {#if shard.isSpeaking}
                            <div
                                class="absolute inset-2 border border-neon-cyan/20 rounded-full animate-ping"
                            ></div>
                        {/if}

                        <div
                            class="relative z-10 flex flex-col items-center gap-2"
                        >
                            <span
                                class="text-2xl font-black italic {shard.color}"
                                >{(shard.integrity * 100).toFixed(1)}%</span
                            >
                            <span
                                class="text-[7px] font-black uppercase tracking-[0.3em] text-white/20"
                                >CAUSAL_SYNC</span
                            >
                        </div>
                    </div>

                    <!-- HUD Markers -->
                    <div
                        class="absolute top-0 right-0 p-4 space-y-2 opacity-40 group-hover:opacity-100 transition-opacity"
                    >
                        <div
                            class="flex items-center gap-2 justify-end text-[8px] font-black uppercase text-neon-cyan"
                        >
                            <Zap size={10} /> LATENCY: 14MS
                        </div>
                        <div
                            class="flex items-center gap-2 justify-end text-[8px] font-black uppercase text-white/40"
                        >
                            <Activity size={10} /> DRIFT: 0.002
                        </div>
                    </div>
                </div>

                <!-- Bottom Controls -->
                <div
                    class="mt-8 flex items-center justify-between border-t border-white/[0.05] pt-6 relative z-10"
                >
                    <div class="flex -space-x-2">
                        {#each Array(3) as _}
                            <div
                                class="w-6 h-6 rounded-full bg-white/5 border-2 border-black flex items-center justify-center text-[7px] font-black uppercase"
                            >
                                AI
                            </div>
                        {/each}
                    </div>
                    <button
                        class="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-[8px] font-black uppercase tracking-widest transition-all"
                    >
                        INSPECT_SHARD_CORE
                    </button>
                </div>

                <!-- Gradient Glow -->
                <div
                    class="absolute -right-10 -bottom-10 w-32 h-32 bg-neon-cyan/5 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity"
                ></div>
            </div>
        {/each}
    </div>

    <!-- Collaborative Toolbar -->
    <div
        class="fixed bottom-32 left-1/2 -translate-x-1/2 z-40 bg-black/80 backdrop-blur-2xl px-8 py-4 rounded-3xl border border-white/10 flex items-center gap-6 shadow-2xl"
    >
        <button
            class="p-4 bg-red-500 rounded-2xl text-white shadow-lg shadow-red-500/20 active:scale-90 transition-all"
        >
            <ShieldCheck size={24} />
        </button>
        <div class="h-8 w-px bg-white/10"></div>
        <button
            class="flex flex-col items-center gap-1 text-white/40 hover:text-white transition-colors"
        >
            <Mic size={20} />
            <span class="text-[6px] font-black uppercase">MUTE_ALL</span>
        </button>
        <button
            class="flex flex-col items-center gap-1 text-white/40 hover:text-white transition-colors"
        >
            <Video size={20} />
            <span class="text-[6px] font-black uppercase">STOP_SYNC</span>
        </button>
        <button class="flex flex-col items-center gap-1 text-neon-cyan">
            <Users size={20} />
            <span class="text-[6px] font-black uppercase">MANAGE_FLEET</span>
        </button>
        <div class="h-8 w-px bg-white/10"></div>
        <button
            class="px-6 py-3 bg-neon-cyan text-black font-black uppercase tracking-tighter text-xs rounded-xl hover:scale-105 active:scale-95 transition-all"
        >
            INITIATE_COUNCIL_CONSENSUS
        </button>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(40px);
        border-radius: 2.5rem;
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
