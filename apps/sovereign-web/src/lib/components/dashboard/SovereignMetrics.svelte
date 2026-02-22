<script lang="ts">
    import { Shield, Vote, Flame, Zap } from "lucide-svelte";
    import { fade } from "svelte/transition";

    interface Props {
        governanceMetrics: {
            totalLiquidity: number;
            sovereignQuorum: number;
            cycleRunway: number;
            canistersActive: number;
        };
        isZenMode: boolean;
    }

    let { governanceMetrics, isZenMode }: Props = $props();
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
    <div
        class="glass-panel p-8 flex flex-col items-center text-center transition-all hover:border-[#00f2ff]/50 group {isZenMode
            ? 'bg-white border-black/5'
            : ''}"
    >
        <div
            class="p-4 rounded-2xl bg-white/5 mb-6 group-hover:scale-110 transition-transform text-white/40"
        >
            <Shield size={20} />
        </div>
        <div
            class="text-[10px] font-black {isZenMode
                ? 'text-[#3C1E1E]/40'
                : 'text-white/40'} tracking-[0.2em] mb-2 uppercase mono-font"
        >
            PROTOCOL LIQUIDITY
        </div>
        <div
            class="text-3xl font-black tracking-tighter mb-2 {isZenMode
                ? 'text-[#3C1E1E]'
                : 'text-white'}"
        >
            ${(governanceMetrics.totalLiquidity / 1e6).toFixed(0)}M
        </div>
        <div class="text-[10px] font-bold mono-font text-green-400 opacity-60">
            +12.4%
        </div>
    </div>
    <div
        class="glass-panel p-8 flex flex-col items-center text-center transition-all hover:border-[#00f2ff]/50 group {isZenMode
            ? 'bg-white border-black/5'
            : ''}"
    >
        <div
            class="p-4 rounded-2xl bg-white/5 mb-6 group-hover:scale-110 transition-transform text-white/40"
        >
            <Vote size={20} />
        </div>
        <div
            class="text-[10px] font-black {isZenMode
                ? 'text-[#3C1E1E]/40'
                : 'text-white/40'} tracking-[0.2em] mb-2 uppercase mono-font"
        >
            SOVEREIGN QUORUM
        </div>
        <div
            class="text-3xl font-black tracking-tighter mb-2 {isZenMode
                ? 'text-[#3C1E1E]'
                : 'text-white'}"
        >
            {governanceMetrics.sovereignQuorum}%
        </div>
        <div class="text-[10px] font-bold mono-font text-green-400 opacity-60">
            STABLE
        </div>
    </div>
    <div
        class="glass-panel p-8 flex flex-col items-center text-center transition-all hover:border-[#00f2ff]/50 group {isZenMode
            ? 'bg-white border-black/5'
            : ''}"
    >
        <div
            class="p-4 rounded-2xl bg-white/5 mb-6 group-hover:scale-110 transition-transform text-white/40"
        >
            <Flame size={20} />
        </div>
        <div
            class="text-[10px] font-black {isZenMode
                ? 'text-[#3C1E1E]/40'
                : 'text-white/40'} tracking-[0.2em] mb-2 uppercase mono-font"
        >
            CYCLE RUNWAY
        </div>
        <div
            class="text-3xl font-black tracking-tighter mb-2 {isZenMode
                ? 'text-[#3C1E1E]'
                : 'text-white'}"
        >
            {governanceMetrics.cycleRunway}d
        </div>
        <div
            class="text-[10px] font-bold mono-font {isZenMode
                ? 'text-[#00B900]'
                : 'neon-text'}"
        >
            PREDICTIVE
        </div>
    </div>
    <div
        class="glass-panel p-8 flex flex-col items-center text-center transition-all hover:border-[#00f2ff]/50 group {isZenMode
            ? 'bg-[#00B900]/5 border-[#00B900]/20'
            : 'border-[#00f2ff]/50 bg-[#00f2ff]/5'}"
    >
        <div
            class="p-4 rounded-2xl bg-white/5 mb-6 group-hover:scale-110 transition-transform {isZenMode
                ? 'text-[#00B900] bg-[#00B900]/10'
                : 'neon-text bg-[#00f2ff]/10'}"
        >
            <Zap size={20} />
        </div>
        <div
            class="text-[10px] font-black {isZenMode
                ? 'text-[#3C1E1E]/40'
                : 'text-white/40'} tracking-[0.2em] mb-2 uppercase mono-font"
        >
            CANDID INTERFACES
        </div>
        <div
            class="text-3xl font-black tracking-tighter mb-2 {isZenMode
                ? 'text-[#3C1E1E]'
                : 'text-white'}"
        >
            {governanceMetrics.canistersActive}
        </div>
        <div
            class="text-[10px] font-bold mono-font {isZenMode
                ? 'text-[#00B900]'
                : 'neon-text'}"
        >
            ACTIVE
        </div>
    </div>
</div>
