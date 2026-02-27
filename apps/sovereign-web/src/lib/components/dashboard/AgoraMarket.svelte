<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import {
        ShoppingCart,
        ShieldCheck,
        ArrowRight,
        Database,
    } from "lucide-svelte";

    // 🏛️ AGORA MARKETPLACE: The Bazaar of Sovereignty
    let activeTab = $state("absolution"); // 'absolution' | 'compute'

    const absolutionPlans = [
        {
            id: "ABS_PLAN_001",
            blocker: "Legacy VMware",
            price: 50,
            badge: "GOLD",
            escaping: "ESXi 6.7",
            impact: 0.15,
        },
        {
            id: "ABS_PLAN_042",
            blocker: "Proprietary GPU",
            price: 150,
            badge: "PLATINUM",
            escaping: "Nvidia Grid",
            impact: 0.25,
        },
        {
            id: "ABS_PLAN_077",
            blocker: "Windows Kernel",
            price: 300,
            badge: "ELITE",
            escaping: "System32",
            impact: 0.45,
        },
    ];

    const yieldOffers = [
        {
            pool: "OASIS_01",
            yield: "12% ARI",
            score: 9.5,
            price: 0.8,
            capacity: "512 TFLOPS",
            shielded: true,
        },
        {
            pool: "OASIS_02",
            yield: "18% ARI",
            score: 8.8,
            price: 1.2,
            capacity: "1.2 PFLOPS",
            shielded: true,
        },
    ];

    function purchasePlan(plan: any) {
        manifold.purchasePlan(plan.id, plan.price);
    }

    function stakeCompute(pool: any) {
        manifold.stakeCompute(pool.pool);
    }
</script>

<div
    class="flex flex-col h-full bg-black/40 rounded-3xl border border-white/10 backdrop-blur-3xl overflow-hidden shadow-2xl"
>
    <!-- Header -->
    <div
        class="p-6 border-b border-white/5 bg-gradient-to-br from-cyan-500/10 to-transparent"
    >
        <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
                <div class="p-2 bg-cyan-400 text-black rounded-xl">
                    <ShoppingCart size={18} />
                </div>
                <div>
                    <h2
                        class="text-xs font-black uppercase tracking-widest text-white"
                    >
                        Agora_Bazaar
                    </h2>
                    <p class="text-[8px] font-bold text-cyan-400/60 uppercase">
                        Systemic_Refinement_Market
                    </p>
                </div>
            </div>
            <div class="text-right flex flex-col items-end gap-1">
                <span
                    class="text-[10px] font-black text-white/40 uppercase tracking-tighter"
                    >Market Index</span
                >
                <button
                    class="group/index relative"
                    onclick={() => manifold.simulateAgoraVolitivity()}
                >
                    <div class="text-lg font-black text-cyan-400">
                        {manifold.kernelState.agora.index.toFixed(2)}
                        <span
                            class="text-[8px] {manifold.kernelState.agora
                                .trend === 'BULLISH'
                                ? 'text-emerald-400'
                                : 'text-rose-400'}"
                            >{manifold.kernelState.agora.trend === "BULLISH"
                                ? "↑"
                                : "↓"}</span
                        >
                    </div>
                </button>
            </div>
        </div>

        <!-- Tabs -->
        <div class="flex gap-2 p-1 bg-white/5 rounded-xl border border-white/5">
            <button
                class="flex-1 py-2 text-[8px] font-black uppercase tracking-widest rounded-lg transition-all
                    {activeTab === 'absolution'
                    ? 'bg-cyan-400 text-black'
                    : 'text-white/40 hover:text-white'}"
                onclick={() => (activeTab = "absolution")}
            >
                Absolution
            </button>
            <button
                class="flex-1 py-2 text-[8px] font-black uppercase tracking-widest rounded-lg transition-all
                    {activeTab === 'compute'
                    ? 'bg-cyan-400 text-black'
                    : 'text-white/40 hover:text-white'}"
                onclick={() => (activeTab = "compute")}
            >
                Compute
            </button>
        </div>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto p-4 custom-scrollbar">
        {#if activeTab === "absolution"}
            <div class="space-y-3" transition:fade>
                {#each absolutionPlans as plan}
                    <div
                        class="group bg-white/5 border border-white/5 rounded-2xl p-4 hover:border-cyan-400/30 transition-all"
                    >
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <h4
                                    class="text-[10px] font-black text-white uppercase"
                                >
                                    {plan.blocker}
                                </h4>
                                <span
                                    class="text-[7px] font-bold text-rose-400 uppercase tracking-tighter"
                                    >Escaping {plan.escaping}</span
                                >
                            </div>
                            <div
                                class="px-2 py-1 bg-cyan-400/10 border border-cyan-400/20 rounded-md text-[7px] font-black text-cyan-400 uppercase"
                            >
                                {plan.badge} Badge
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex flex-col">
                                <span
                                    class="text-[7px] font-black text-white/20 uppercase"
                                    >Impact</span
                                >
                                <span class="text-xs font-black text-white"
                                    >+{(plan.impact * 100).toFixed(0)}% RL</span
                                >
                            </div>
                            <button
                                class="flex items-center gap-2 pl-4 pr-2 py-2 text-[9px] font-black uppercase tracking-widest rounded-xl transition-all
                                    {manifold.ownedPlans.includes(plan.id)
                                    ? 'bg-emerald-400 text-black'
                                    : manifold.ageCredits < plan.price
                                      ? 'bg-white/10 text-white/20 cursor-not-allowed'
                                      : 'bg-white text-black hover:bg-cyan-400'}"
                                onclick={() => purchasePlan(plan)}
                                disabled={manifold.ownedPlans.includes(
                                    plan.id,
                                ) || manifold.ageCredits < plan.price}
                            >
                                {manifold.ownedPlans.includes(plan.id)
                                    ? "Owned"
                                    : `${plan.price} CR`}
                                <ArrowRight size={12} />
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
        {:else}
            <div class="space-y-3" transition:fade>
                {#each yieldOffers as offer}
                    <div
                        class="bg-white/5 border border-white/5 rounded-2xl p-4"
                    >
                        <div class="flex items-center gap-3 mb-4">
                            <div
                                class="w-10 h-10 bg-black/40 rounded-xl flex items-center justify-center text-cyan-400"
                            >
                                <Database size={20} />
                            </div>
                            <div>
                                <h4
                                    class="text-[10px] font-black text-white uppercase"
                                >
                                    {offer.pool}
                                </h4>
                                <p
                                    class="text-[7px] font-bold text-white/20 uppercase tracking-tighter"
                                >
                                    {offer.capacity} // Tier {offer.score}
                                </p>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div class="p-2 bg-black/20 rounded-lg">
                                <span
                                    class="block text-[6px] font-black text-white/30 uppercase"
                                    >Yield</span
                                >
                                <span
                                    class="text-[10px] font-black text-emerald-400"
                                    >{offer.yield}</span
                                >
                            </div>
                            <div class="p-2 bg-black/20 rounded-lg">
                                <span
                                    class="block text-[6px] font-black text-white/30 uppercase"
                                    >Price / Unit</span
                                >
                                <span class="text-[10px] font-black text-white"
                                    >{offer.price} CR</span
                                >
                            </div>
                        </div>
                        <button
                            class="w-full py-2 bg-cyan-400/10 border border-cyan-400/20 text-cyan-400 text-[8px] font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 hover:text-black transition-all"
                            onclick={() => stakeCompute(offer)}
                        >
                            Stake Compute Liquidity
                        </button>
                    </div>
                {/each}
            </div>
        {/if}
    </div>

    <!-- Footer -->
    <div
        class="p-4 border-t border-white/5 flex items-center justify-between opacity-40"
    >
        <div class="flex items-center gap-2">
            <ShieldCheck size={12} />
            <span class="text-[7px] font-black uppercase">QES Secured</span>
        </div>
        <span class="text-[7px] font-black uppercase tracking-widest"
            >v1.2-Ternary</span
        >
    </div>
</div>
