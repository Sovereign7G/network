<script lang="ts">
    import { ArrowLeftRight, Plus, TrendingUp } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import InstitutionLinking from "./InstitutionLinking.svelte";
    import SovereignStories from "./SovereignStories.svelte";
    import SovereignWallet from "./SovereignWallet.svelte";
    import SovereignRecentActivity from "./SovereignRecentActivity.svelte";
    import { goto } from "$app/navigation";

    interface Props {
        showWisdom: boolean;
        onTabSelect: (id: string) => void;
    }

    let { showWisdom, onTabSelect }: Props = $props();
</script>

<div class="space-y-16" in:fade>
    <!-- Financial Summary Card (Horizon Wisdom) -->
    <section
        class="glass-panel p-10 bg-gradient-to-r from-neon-cyan/10 to-transparent relative overflow-hidden"
    >
        <div
            class="absolute right-0 top-0 h-full w-1/3 bg-neon-cyan/5 blur-3xl rounded-full"
        ></div>
        <div
            class="relative z-10 flex flex-col md:flex-row justify-between items-end gap-8"
        >
            <div class="space-y-4">
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white/40 flex items-center gap-2"
                >
                    Sovereign Net Worth
                    {#if showWisdom}
                        <div
                            class="px-2 py-0.5 bg-amber-400 text-black text-[8px] font-black rounded animate-bounce shadow-[0_0_10px_rgba(251,191,36,0.5)]"
                        >
                            NOTE: Real-time aggregate value across indexed
                            shards.
                        </div>
                    {/if}
                </h2>
                <div class="flex items-baseline gap-4">
                    <span
                        class="text-7xl font-black tracking-tighter italic resonance-pulse"
                        >$125,480<span class="text-neon-cyan opacity-50"
                            >.00</span
                        ></span
                    >
                    <span
                        class="text-green-400 font-bold flex items-center gap-1"
                    >
                        <TrendingUp size={16} />
                        +14.2%
                    </span>
                </div>
            </div>
            <div class="flex flex-wrap gap-4">
                <button
                    onclick={() => onTabSelect("transfers")}
                    class="px-10 py-5 bg-neon-cyan text-black font-black uppercase tracking-tighter text-lg rounded-2xl hover:scale-105 transition-all shadow-[0_0_40px_rgba(0,242,255,0.4)] flex items-center gap-3"
                >
                    <ArrowLeftRight size={20} />
                    ASTRO TRANSFER
                </button>
                <button
                    class="px-8 py-5 bg-white/5 border border-white/10 font-black uppercase tracking-tighter rounded-2xl hover:bg-white/10 transition-all flex items-center gap-3"
                >
                    <Plus size={18} />
                    DEPOSIT
                </button>
                <button
                    onclick={() => goto("/dashboard/hearth")}
                    class="px-8 py-5 bg-gradient-to-r from-plasma-purple/40 to-plasma-purple/10 border border-plasma-purple/30 font-black uppercase tracking-tighter rounded-2xl hover:bg-plasma-purple/30 transition-all flex items-center gap-3"
                >
                    🔥 HEARTH
                </button>
            </div>
        </div>
    </section>

    <InstitutionLinking {showWisdom} />

    <SovereignStories />

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
        <div class="glass-panel p-8">
            <h3 class="text-xl font-black italic mb-6">QUICK WALLET</h3>
            <SovereignWallet />
        </div>
        <div class="glass-panel p-8">
            <h3 class="text-xl font-black italic mb-6">
                RECENT PROTOCOL ACTIVITY
            </h3>
            <SovereignRecentActivity />
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
