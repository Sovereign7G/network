<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, slide } from "svelte/transition";
    import {
        MessageSquare,
        User,
        Heart,
        Share2,
        Globe,
        Shield,
        Zap,
    } from "lucide-svelte";

    const personalities = [
        "Sovereign Citizen",
        "Gov Auditor",
        "Cinema Mesh Producer",
        "Institutional Node",
        "DACC Analyst",
        "Phase Space Traveler",
        "WITR Forensics Agent",
        "Quantum Validator",
    ];

    const feedbacks = [
        "The QES implementation is flawless.",
        "Just processed 14 TB of narrative shards. Coherence is at 99%.",
        "Institutional rail transition was seamless.",
        "Requesting more phantom liquidity in the Nairobi sector.",
        "The HOLLY-1 production mesh is finally democratized.",
        "Causal tracing revealed a 0.2% drift in the southern hub.",
        "My digital identity feels actually sovereign for the first time.",
        "Interoperative e-governance is the future.",
    ];

    let items = $state<any[]>([]);
    let totalFeedbackCount = $state(9842011);

    function generateFeedback() {
        const personality =
            personalities[Math.floor(Math.random() * personalities.length)];
        const content = feedbacks[Math.floor(Math.random() * feedbacks.length)];
        const id = Math.random().toString(36).substring(7);
        const time = "JUST NOW";
        return {
            id,
            personality,
            content,
            time,
            likes: Math.floor(Math.random() * 50),
        };
    }

    onMount(() => {
        items = Array(5)
            .fill(null)
            .map(() => generateFeedback());

        const interval = setInterval(() => {
            const newItem = generateFeedback();
            items = [newItem, ...items.slice(0, 4)];
            totalFeedbackCount += Math.floor(Math.random() * 10);
        }, 3000);

        return () => clearInterval(interval);
    });
</script>

<div class="glass-panel p-8 h-full flex flex-col">
    <div class="flex items-center justify-between mb-8">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.2em] text-white/40 mb-1"
            >
                Pulse of the Mesh
            </h3>
            <div class="flex items-baseline gap-2">
                <span class="text-2xl font-black italic tracking-tighter"
                    >{totalFeedbackCount.toLocaleString()}</span
                >
                <span class="text-[10px] font-bold text-neon-cyan"
                    >SOVEREIGN VOICES</span
                >
            </div>
        </div>
        <Globe size={20} class="text-neon-cyan resonance-pulse" />
    </div>

    <div class="space-y-6 flex-1 overflow-hidden relative">
        <div
            class="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-[#020408] to-transparent z-10 pointer-events-none"
        ></div>

        {#each items as item (item.id)}
            <div
                in:fly={{ y: -20, duration: 500 }}
                out:fade={{ duration: 300 }}
                class="p-4 bg-white/5 border border-white/5 rounded-2xl space-y-3 relative group hover:border-neon-cyan/20 transition-all"
            >
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <div
                            class="w-6 h-6 rounded-full bg-neon-cyan/20 flex items-center justify-center"
                        >
                            <User size={12} class="text-neon-cyan" />
                        </div>
                        <span
                            class="text-[9px] font-black uppercase tracking-widest text-white/60"
                            >{item.personality}</span
                        >
                    </div>
                    <span
                        class="text-[8px] mono-font text-white/20 uppercase font-black"
                        >{item.time}</span
                    >
                </div>
                <p class="text-xs leading-relaxed text-white/80 italic">
                    "{item.content}"
                </p>
                <div class="flex items-center gap-4 pt-1">
                    <div
                        class="flex items-center gap-1.5 opacity-40 group-hover:opacity-100 transition-opacity"
                    >
                        <Heart size={10} class="text-red-400" />
                        <span class="text-[8px] mono-font">{item.likes}</span>
                    </div>
                    <div
                        class="flex items-center gap-1.5 opacity-40 group-hover:opacity-100 transition-opacity"
                    >
                        <Share2 size={10} class="text-white" />
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <button
        class="w-full mt-6 py-4 glass-panel border-white/5 hover:border-neon-cyan/40 text-[9px] font-black uppercase tracking-[0.3em] transition-all"
    >
        Enter the Agora
    </button>
</div>
