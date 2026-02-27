<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import { Shield, Zap, ArrowUpRight, Layers } from "lucide-svelte";

    const vault = $derived(manifold.vaultState);
    const stablecoin = $derived(manifold.stablecoinState);
    const bridge = $derived(manifold.bridgeStatus);

    let activeView = $state("vault"); // 'vault' | 'stable' | 'bridge'

    function getParityColor(parity: number) {
        const drift = Math.abs(1 - parity);
        if (drift < 0.001) return "text-emerald-400";
        if (drift < 0.01) return "text-amber-400";
        return "text-rose-400";
    }
</script>

<div
    class="flex flex-col h-full bg-zinc-900/40 rounded-[2.5rem] border border-white/5 backdrop-blur-2xl overflow-hidden p-6 gap-6 shadow-2xl relative"
>
    <!-- Header Nav -->
    <div class="flex items-center justify-between px-2">
        <div class="flex gap-4">
            {#each ["vault", "stable", "bridge"] as view}
                <button
                    onclick={() => (activeView = view)}
                    class="text-[9px] font-black uppercase tracking-[0.2em] transition-all pb-2 border-b-2 {activeView ===
                    view
                        ? 'text-white border-cyan-400'
                        : 'text-white/20 border-transparent hover:text-white/40'}"
                >
                    {view}
                </button>
            {/each}
        </div>
        <div class="flex items-center gap-2">
            <div
                class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"
            ></div>
            <span
                class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                >Live_Market_Feed</span
            >
        </div>
    </div>

    <!-- Content Area -->
    <div class="flex-1 overflow-hidden relative">
        {#if activeView === "vault"}
            <div in:fade={{ duration: 200 }} class="h-full flex flex-col gap-6">
                <!-- TVL Display -->
                <div
                    class="p-6 bg-white/5 rounded-3xl border border-white/5 relative overflow-hidden group"
                >
                    <div
                        class="absolute right-0 top-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity"
                    >
                        <Shield size={64} />
                    </div>
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-[0.3em] block mb-2"
                        >Autonomous_Vault_TVL</span
                    >
                    <div
                        class="text-4xl font-black text-white tracking-tighter italic"
                    >
                        ${(vault.totalValueLockedUsd / 1000000).toFixed(2)}M
                    </div>
                    <div class="flex items-center gap-2 mt-4">
                        <div
                            class="bg-emerald-400/10 text-emerald-400 text-[8px] font-black px-2 py-1 rounded uppercase tracking-widest"
                        >
                            Strategy: {vault.activeStrategy.replace("_", " ")}
                        </div>
                        <span
                            class="text-[8px] font-bold text-white/40 uppercase"
                            >Integrity: {(vault.integrityScore * 100).toFixed(
                                2,
                            )}%</span
                        >
                    </div>
                </div>

                <!-- Asset List -->
                <div class="flex-1 space-y-3 overflow-y-auto no-scrollbar">
                    {#each vault.assets as asset}
                        <div
                            class="flex items-center justify-between p-4 bg-black/40 rounded-2xl border border-white/5 hover:border-white/10 transition-colors"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-xs font-black"
                                >
                                    {asset.asset[0]}
                                </div>
                                <div>
                                    <div
                                        class="text-[10px] font-black text-white uppercase"
                                    >
                                        {asset.asset}
                                    </div>
                                    <div
                                        class="text-[8px] text-white/30 font-bold"
                                    >
                                        {asset.amount.toLocaleString()} Units
                                    </div>
                                </div>
                            </div>
                            <div class="text-right">
                                <div
                                    class="text-[10px] font-black text-emerald-400"
                                >
                                    +{(asset.yield * 100).toFixed(1)}% APY
                                </div>
                                <div
                                    class="text-[9px] font-bold text-white/60 italic"
                                >
                                    ${(asset.valueUsd / 1000000).toFixed(2)}M
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeView === "stable"}
            <div in:fade={{ duration: 200 }} class="h-full flex flex-col gap-6">
                <!-- Parity Display -->
                <div
                    class="p-8 bg-gradient-to-br from-cyan-400/10 to-transparent rounded-[2.5rem] border border-cyan-400/10 text-center relative overflow-hidden"
                >
                    <div
                        class="text-[8px] font-black text-cyan-400/40 uppercase tracking-[0.4em] mb-4"
                    >
                        Sovereign_Parity_Index
                    </div>
                    <div
                        class="text-6xl font-black {getParityColor(
                            stablecoin.parity,
                        )} tracking-tighter mb-2"
                    >
                        {stablecoin.parity.toFixed(4)}
                    </div>
                    <div
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                    >
                        {stablecoin.symbol}
                        <span class="text-white/20 px-2">//</span> USD
                    </div>
                </div>

                <!-- Market Data -->
                <div class="grid grid-cols-2 gap-4">
                    <div
                        class="p-4 bg-white/5 rounded-2xl border border-white/5"
                    >
                        <span
                            class="text-[8px] font-black text-white/20 uppercase block mb-1"
                            >Market_Cap</span
                        >
                        <span class="text-sm font-black text-white italic"
                            >${(stablecoin.marketCap / 1000000).toFixed(
                                1,
                            )}M</span
                        >
                    </div>
                    <div
                        class="p-4 bg-white/5 rounded-2xl border border-white/5"
                    >
                        <span
                            class="text-[8px] font-black text-white/20 uppercase block mb-1"
                            >Collateral</span
                        >
                        <span class="text-sm font-black text-emerald-400"
                            >{(stablecoin.collateralBacking * 100).toFixed(
                                0,
                            )}%</span
                        >
                    </div>
                </div>

                <!-- LP Pool Activity -->
                <div class="space-y-[2px]">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest px-2 mb-2 block"
                        >Deep_Liquidity_Pools</span
                    >
                    {#each stablecoin.stableLPs as lp}
                        <div
                            class="flex items-center justify-between p-3 bg-white/[0.02] border-y border-white/5"
                        >
                            <span
                                class="text-[9px] font-black text-white/60 uppercase"
                                >{lp.pair}</span
                            >
                            <div class="flex gap-4">
                                <div class="text-right">
                                    <div
                                        class="text-[8px] text-white/20 uppercase font-black tracking-tighter"
                                    >
                                        TVL
                                    </div>
                                    <div
                                        class="text-[10px] font-black text-white italic"
                                    >
                                        ${(lp.liquidity / 1000000).toFixed(1)}M
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div
                                        class="text-[8px] text-white/20 uppercase font-black tracking-tighter"
                                    >
                                        Vol_24h
                                    </div>
                                    <div
                                        class="text-[10px] font-black text-cyan-400 italic"
                                    >
                                        ${(lp.volume24h / 1000000).toFixed(1)}M
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeView === "bridge"}
            <div in:fade={{ duration: 200 }} class="h-full flex flex-col gap-4">
                <div class="flex items-center gap-3 mb-2">
                    <Zap size={14} class="text-amber-400" />
                    <span
                        class="text-[9px] font-black text-white uppercase tracking-widest"
                        >Cross_Chain_Consensus</span
                    >
                </div>

                <div class="space-y-3">
                    {#each bridge.activeBridges as b}
                        <div
                            class="p-4 bg-white/5 rounded-2xl border border-white/5 flex items-center justify-between group cursor-pointer hover:bg-white/10 transition-all"
                        >
                            <div class="flex items-center gap-4">
                                <div
                                    class="w-2 h-2 rounded-full {b.status ===
                                    'OPERATIONAL'
                                        ? 'bg-emerald-400'
                                        : 'bg-amber-400'}"
                                ></div>
                                <div>
                                    <div
                                        class="text-[10px] font-black text-white uppercase tracking-tighter"
                                    >
                                        {b.name}
                                    </div>
                                    <div
                                        class="text-[8px] font-bold text-white/20 uppercase tracking-widest"
                                    >
                                        LATENCY: {b.latency}
                                        <span class="px-1">//</span>
                                        TVL: {b.tvl}
                                    </div>
                                </div>
                            </div>
                            <ArrowUpRight
                                size={14}
                                class="text-white/20 group-hover:text-cyan-400 group-hover:translate-x-1 group-hover:-translate-y-1 transition-all"
                            />
                        </div>
                    {/each}
                </div>

                <!-- Discovery Prompt -->
                <div
                    class="mt-auto p-4 bg-cyan-400/5 border border-cyan-400/20 rounded-3xl"
                >
                    <p
                        class="text-[9px] font-bold text-cyan-400/80 uppercase leading-relaxed text-center italic"
                    >
                        "Consolidate institutional liquidity across shards to
                        boost systemic resonance."
                    </p>
                </div>
            </div>
        {/if}
    </div>

    <!-- Footer Stats -->
    <div
        class="mt-auto pt-4 border-t border-white/5 flex justify-between items-center text-[8px] font-black text-white/20 uppercase tracking-[0.2em]"
    >
        <div class="flex items-center gap-2">
            <Layers size={12} />
            <span>Resonance: {manifold.resonance}%</span>
        </div>
        <div class="flex items-center gap-4">
            <div class="flex items-center gap-1">
                <div class="w-1 h-1 rounded-full bg-cyan-400"></div>
                <span>Sync v{bridge.globalSyncStatus * 100}</span>
            </div>
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
    .no-scrollbar {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
