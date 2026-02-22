<script lang="ts">
    import {
        Lightbulb,
        ArrowRight,
        Shield,
        Zap,
        TrendingUp,
        User,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    const strategies = [
        {
            title: "Liquidity Teleportation v4",
            author: "Sophia LLL",
            tier: "AAL3 verified",
            usage: "2.4k Citizens",
            performance: "+12.4%",
            icon: Zap,
            description:
                "Automated value balancing across Shard-Alpha and Merit-Hub using quantum-asynchronous logic.",
        },
        {
            title: "Jade Monolith Hardening",
            author: "Ari Protocol",
            tier: "Institutional",
            usage: "850 nodes",
            performance: "99.9% uptime",
            icon: Shield,
            description:
                "A defensive strategy that triggers automated shard rotation upon detecting behavioral dissonance > 0.4.",
        },
        {
            title: "ARI Yield Harvest",
            author: "Foundation Agent",
            tier: "Core Support",
            usage: "5.1k Citizens",
            performance: "+8.2% APY",
            icon: TrendingUp,
            description:
                "Optimized merit extraction and ARI realization workflow for high-maturity sovereign accounts.",
        },
    ];
</script>

<div class="space-y-8">
    <div class="flex items-center justify-between">
        <div>
            <h3 class="text-2xl font-black italic tracking-tighter uppercase">
                SOVEREIGN STRATEGY FEED
            </h3>
            <p
                class="text-[10px] mono-font text-white/40 uppercase tracking-[0.3em] mt-1"
            >
                Community-Verified Agentic Workflows
            </p>
        </div>
        <button
            class="px-6 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all"
        >
            SUBMIT BLUEPRINT
        </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {#each strategies as strategy, i}
            <div
                class="glass-panel p-8 group hover:border-neon-cyan/40 transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between border-white/[0.03]"
                in:fly={{ y: 20, delay: i * 150, duration: 800 }}
            >
                <div
                    class="absolute -right-4 -top-4 opacity-[0.02] group-hover:opacity-10 transition-opacity"
                >
                    <strategy.icon size={160} />
                </div>

                <div>
                    <div class="flex justify-between items-start mb-8">
                        <div
                            class="w-14 h-14 rounded-2xl bg-white/[0.02] border border-white/5 flex items-center justify-center text-white/40 group-hover:text-neon-cyan group-hover:border-neon-cyan/30 transition-all duration-500"
                        >
                            <strategy.icon size={28} />
                        </div>
                        <div
                            class="px-2 py-1 bg-neon-cyan/10 rounded text-[7px] font-black uppercase tracking-[0.2em] text-neon-cyan border border-neon-cyan/20"
                        >
                            SPEC: {strategy.tier}
                        </div>
                    </div>

                    <h4
                        class="text-2xl font-black italic tracking-tighter mb-3 uppercase group-hover:text-neon-cyan transition-colors"
                    >
                        {strategy.title}
                    </h4>
                    <p
                        class="text-[11px] mono-font text-white/40 leading-relaxed mb-8 uppercase tracking-wider"
                    >
                        {strategy.description}
                    </p>
                </div>

                <div class="space-y-6 pt-6 border-t border-white/[0.03]">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="space-y-1">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                >Architect</span
                            >
                            <div class="text-[10px] font-bold text-white/50">
                                {strategy.author}
                            </div>
                        </div>
                        <div class="space-y-1 text-right">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                >Yield Delta</span
                            >
                            <div
                                class="text-[11px] font-black text-green-400 italic"
                            >
                                {strategy.performance}
                            </div>
                        </div>
                    </div>

                    <button
                        class="w-full py-4 bg-white/[0.02] border border-white/5 group-hover:bg-neon-cyan group-hover:text-black transition-all duration-500 rounded-xl font-black uppercase text-[9px] tracking-[0.3em] flex items-center justify-center gap-3"
                    >
                        INITIALIZE BLUEPRINT <ArrowRight size={14} />
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
    }
</style>
