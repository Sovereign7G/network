<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, slide } from "svelte/transition";

    import {
        Activity,

        Shield,
        Zap,
        Terminal,

        Layers,
        Info,
    } from "lucide-svelte";

    type TelemetryEvent = {
        id: string;
        timestamp: string;
        action: string;
        shard: string;
        clearance: string;
        status: "COHERENT" | "SYNCING" | "CAUSAL_TRACE";
        score: number;
    };

    let events = $state<TelemetryEvent[]>([]);

    const actions = [
        "YIELD_TELEPORT",
        "ASTRO_TRANSFER",
        "MERIT_HARVEST",
        "CAUSAL_ANCHOR",
        "SHARD_ROTATION",
        "AAL3_VERIFY",
        "JADE_LOCK_SCAN",
    ];

    const shards = [
        "ALPHA-01",
        "HUB-MERIT",
        "VAULT-CX",
        "NODE-7782",
        "SHARD-BEEF",
    ];

    function generateEvent(): TelemetryEvent {
        return {
            id: Math.random().toString(36).substring(7).toUpperCase(),
            timestamp: new Date().toLocaleTimeString("en-GB", {
                hour12: false,
            }),
            action: actions[Math.floor(Math.random() * actions.length)],
            shard: shards[Math.floor(Math.random() * shards.length)],
            clearance: "AAL3_ALPHA",
            status: ["COHERENT", "SYNCING", "CAUSAL_TRACE"][
                Math.floor(Math.random() * 3)
            ] as any,
            score: 0.9 + Math.random() * 0.1,
        };
    }

    onMount(() => {
        // Initial set
        events = Array(8)
            .fill(null)
            .map(() => generateEvent());

        const interval = setInterval(() => {
            const newEvent = generateEvent();
            events = [newEvent, ...events.slice(0, 7)];
        }, 4000);

        return () => clearInterval(interval);
    });
</script>

<div
    class="glass-panel p-6 h-full flex flex-col bg-black/40 border-white/[0.03]"
>
    <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
            <div
                class="w-8 h-8 rounded-lg bg-neon-cyan/10 flex items-center justify-center text-neon-cyan"
            >
                <Terminal size={16} />
            </div>
            <div>
                <h3
                    class="text-[10px] font-black uppercase tracking-[0.3em] text-white/90"
                >
                    SOVEREIGN_TELEMETRY
                </h3>
                <p
                    class="text-[7px] mono-font text-white/30 uppercase tracking-widest mt-0.5"
                >
                    Real-Time Substrate Logs
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-2 px-2 py-1 bg-green-500/10 border border-green-500/20 rounded"
        >
            <div class="w-1 h-1 rounded-full bg-green-400 animate-pulse"></div>
            <span
                class="text-[6px] font-black text-green-400 uppercase tracking-widest text-shadow-glow"
                >LIVE_STREAM</span
            >
        </div>
    </div>

    <div class="flex-1 space-y-3 overflow-hidden">
        {#each events as event (event.id)}
            <div
                in:fly={{ x: -10, duration: 600 }}
                out:fade={{ duration: 300 }}
                class="group p-3 bg-white/[0.01] border border-white/[0.03] rounded-xl hover:bg-white/[0.05] hover:border-neon-cyan/30 transition-all flex flex-col gap-2 relative overflow-hidden backdrop-blur-md"
            >
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <div
                            class="w-1 h-1 rounded-full bg-neon-cyan animate-pulse causal-pulse"
                        ></div>
                        <span
                            class="text-[8px] mono-font font-black text-neon-cyan/80"
                            >{event.timestamp}</span
                        >
                        <span
                            class="text-[9px] font-black text-white/80 tracking-tighter uppercase"
                            >{event.action}</span
                        >
                    </div>
                    <span class="text-[7px] mono-font text-white/30"
                        >ID: {event.id}</span
                    >
                </div>

                <div
                    class="grid grid-cols-3 gap-2 py-1 border-y border-white/[0.02]"
                >
                    <div class="space-y-0.5">
                        <span
                            class="text-[6px] font-black text-white/10 uppercase tracking-tighter"
                            >Locality</span
                        >
                        <div class="text-[8px] mono-font text-white/40">
                            {event.shard}
                        </div>
                    </div>
                    <div class="space-y-0.5">
                        <span
                            class="text-[6px] font-black text-white/10 uppercase tracking-tighter"
                            >Clearance</span
                        >
                        <div class="text-[8px] mono-font text-neon-cyan/40">
                            AAL3
                        </div>
                    </div>
                    <div class="space-y-0.5 text-right">
                        <span
                            class="text-[6px] font-black text-white/10 uppercase tracking-tighter"
                            >Causal_Score</span
                        >
                        <div class="text-[8px] mono-font text-green-400/60">
                            {(event.score * 100).toFixed(1)}%
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between pt-1">
                    <div
                        class="flex items-center gap-1.5 px-1.5 py-0.5 bg-white/[0.02] border border-white/5 rounded text-[7px] font-black tracking-widest uppercase text-white/30"
                    >
                        <Layers size={8} />
                        {event.status}
                    </div>
                    <div
                        class="w-16 h-0.5 bg-white/5 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full bg-neon-cyan"
                            style="width: {event.score * 100}%"
                        ></div>
                    </div>
                </div>

                <!-- HUD Scan line -->
                <div
                    class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-neon-cyan/20 to-transparent translate-y-[-1px] group-hover:translate-y-[40px] transition-transform duration-1000"
                ></div>
            </div>
        {/each}
    </div>

    <button
        class="w-full mt-6 py-4 border border-white/[0.03] bg-white/[0.01] hover:bg-neon-cyan hover:text-black transition-all rounded-xl text-[8px] font-black uppercase tracking-[0.4em] text-white/20"
    >
        EXPAND_FORENSICS_SUBSHELL
    </button>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(40px);
        border-radius: 2rem;
    }

    @keyframes causal-pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 0 0 rgba(0, 242, 255, 0);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.5);
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        }
    }

    .causal-pulse {
        animation: causal-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
</style>
