<script lang="ts">
    import { fade, scale, fly } from "svelte/transition";
    import { backOut, elasticOut } from "svelte/easing";
    import { Sparkles, Shield, Vote, Zap, X } from "lucide-svelte";

    let { event = "transaction", onclose } = $props<{
        event: "transaction" | "zkproof" | "vote" | "hearth";
        onclose: () => void;
    }>();

    const configs: Record<string, any> = {
        transaction: {
            icon: Zap,
            title: "Sovereign Exchange Complete",
            subtitle: "You just moved value without a bank",
            description:
                "Every peer-to-peer transaction is an act of economic sovereignty. Your assets are now truly yours.",
            color: "text-amber-400",
            bg: "bg-amber-400/10",
            border: "border-amber-400/20",
        },
        zkproof: {
            icon: Shield,
            title: "Privacy Shield Activated",
            subtitle: "You proved without revealing",
            description:
                "Zero-Knowledge technology allows you to verify your identity while keeping the underlying data private.",
            color: "text-neon-cyan",
            bg: "bg-neon-cyan/10",
            border: "border-neon-cyan/20",
        },
        vote: {
            icon: Vote,
            title: "Voice Recorded",
            subtitle: "Your voice shaped the protocol",
            description:
                "In a fractal democracy, your participation directly influences the evolution of the network state.",
            color: "text-purple-400",
            bg: "bg-purple-400/10",
            border: "border-purple-400/20",
        },
        hearth: {
            icon: Sparkles,
            title: "Memory Forged",
            subtitle: "Your journey has begun",
            description:
                "By recording your experiences in the Heart, you turn fleeting moments into permanent resonance.",
            color: "text-emerald-400",
            bg: "bg-emerald-400/10",
            border: "border-emerald-400/20",
        },
    };

    const config = $derived(configs[event]);
    const Icon = $derived(config.icon);
</script>

<div
    class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm"
    transition:fade
>
    <div
        class="max-w-md w-full glass-panel-lux relative overflow-hidden"
        in:fly={{ y: 40, duration: 600, easing: backOut }}
    >
        <!-- Gold Particles Ambience -->
        <div
            class="absolute inset-0 pointer-events-none overflow-hidden opacity-30"
        >
            {#each Array(20) as _}
                <div
                    class="particle"
                    style="
                        left: {Math.random() * 100}%; 
                        top: {Math.random() * 100}%; 
                        animation-delay: {Math.random() * 5}s;
                        background: {config.color.includes('amber')
                        ? '#fbbf24'
                        : config.color.includes('cyan')
                          ? '#00f2ff'
                          : '#a855f7'}
                    "
                ></div>
            {/each}
        </div>

        <button
            class="absolute top-6 right-6 text-white/20 hover:text-white/60 transition-colors z-20"
            onclick={onclose}
        >
            <X size={20} />
        </button>

        <div
            class="p-10 flex flex-col items-center text-center space-y-8 relative z-10"
        >
            <div
                class="icon-orb {config.bg} {config.border} {config.color}"
                in:scale={{ delay: 300, duration: 800, easing: elasticOut }}
            >
                <Icon size={48} strokeWidth={1.5} />
            </div>

            <div class="space-y-4">
                <div class="space-y-1">
                    <span
                        class="text-[10px] font-black uppercase tracking-[0.3em] {config.color}"
                        >{config.subtitle}</span
                    >
                    <h2
                        class="text-3xl font-black italic tracking-tighter text-white"
                    >
                        {config.title}
                    </h2>
                </div>
                <p class="text-sm text-white/60 leading-relaxed">
                    {config.description}
                </p>
            </div>

            <button
                class="w-full py-4 bg-white text-black font-black uppercase text-xs tracking-widest rounded-2xl hover:scale-[1.02] active:scale-95 transition-all shadow-xl shadow-white/10"
                onclick={onclose}
            >
                CONTINUE JOURNEY
            </button>
        </div>
    </div>
</div>

<style>
    .glass-panel-lux {
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.05) 0%,
            rgba(255, 255, 255, 0.01) 100%
        );
        backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 3rem;
        box-shadow:
            0 30px 60px -12px rgba(0, 0, 0, 0.5),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }

    .icon-orb {
        width: 100px;
        height: 100px;
        border-radius: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
    }

    /* Flex fix for icon centering if not working */
    .icon-orb {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        border-radius: 50%;
        animation: float 10s infinite ease-in-out;
    }

    @keyframes float {
        0%,
        100% {
            transform: translateY(0) translateX(0) scale(1);
            opacity: 0;
        }
        20% {
            opacity: 0.8;
        }
        50% {
            transform: translateY(-100px) translateX(20px) scale(0.5);
            opacity: 0.4;
        }
        80% {
            opacity: 0.8;
        }
    }
</style>
