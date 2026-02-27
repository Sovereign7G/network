<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { BarChart3 } from "lucide-svelte";

    import type { OrderSide } from "$lib/types";

    const bourse = $derived(manifold.spectralBourse);
    const wallet = $derived(manifold.walletState);

    let orderPrice = $state(0.5);
    let orderSize = $state(100);

    function placeOrder(side: OrderSide) {
        manifold.placeSpectralOrder(side, orderPrice, orderSize);
    }
</script>

<div
    class="flex flex-col h-full bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-2xl overflow-hidden p-6 gap-6 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="p-3 bg-white/5 rounded-2xl text-cyan-400">
                <BarChart3 size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Spectral_Bourse
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[8px] font-black {bourse.status === 'ACTIVE'
                            ? 'text-emerald-400'
                            : 'text-rose-400'} uppercase"
                    >
                        {bourse.status} // 0xAA
                    </span>
                    <div class="flex gap-0.5">
                        <div
                            class="w-1 h-3 rounded-full {bourse.status ===
                            'ACTIVE'
                                ? 'bg-emerald-400'
                                : 'bg-rose-400'}"
                        ></div>
                        <div
                            class="w-1 h-3 rounded-full {bourse.status ===
                            'ACTIVE'
                                ? 'bg-emerald-400/50'
                                : 'bg-rose-400/50'}"
                        ></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="text-right">
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-tighter"
                >Brillouin_Coupling</span
            >
            <div class="text-lg font-black text-white italic">
                {(bourse.brillouinCoupling * 100).toFixed(1)}%
            </div>
        </div>
    </div>

    <!-- Health Indicators -->
    <div class="grid grid-cols-2 gap-3">
        <div class="p-3 bg-white/5 rounded-2xl border border-white/5">
            <div class="flex justify-between items-center mb-1">
                <span
                    class="text-[7px] font-black text-white/30 uppercase tracking-widest"
                    >Fiber_Health</span
                >
                <span
                    class="text-[9px] font-black {bourse.fiberHealth > 0.9
                        ? 'text-emerald-400'
                        : 'text-rose-400'}"
                >
                    {(bourse.fiberHealth * 100).toFixed(1)}%
                </span>
            </div>
            <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div
                    class="h-full {bourse.fiberHealth > 0.9
                        ? 'bg-emerald-400'
                        : 'bg-rose-400'} transition-all"
                    style:width="{bourse.fiberHealth * 100}%"
                ></div>
            </div>
        </div>
        <div class="p-3 bg-white/5 rounded-2xl border border-white/5">
            <div class="flex justify-between items-center mb-1">
                <span
                    class="text-[7px] font-black text-white/30 uppercase tracking-widest"
                    >Fee_Tier</span
                >
                <span class="text-[9px] font-black text-cyan-400"
                    >{wallet.reputationScore > 0.9 ? "VIP" : "STD"}</span
                >
            </div>
            <div class="flex gap-1">
                {#each Array(3) as _, i}
                    <div
                        class="h-1 flex-1 {wallet.reputationScore > 0.9
                            ? 'bg-cyan-400'
                            : i === 0
                              ? 'bg-cyan-400'
                              : 'bg-white/10'} rounded-full"
                    ></div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Order Book & Bonds (Tabbed or Split) -->
    <div class="flex-1 overflow-hidden flex flex-col gap-4 font-mono">
        <div class="flex-1 flex flex-col gap-2">
            <div
                class="text-[8px] font-black text-white/20 uppercase px-2 mb-1"
            >
                Order_Book
            </div>

            <!-- Asks (Red) -->
            <div
                class="flex-1 flex flex-col-reverse justify-start overflow-hidden gap-1"
            >
                {#each bourse.asks.slice(-3) as ask}
                    <div
                        class="flex justify-between items-center px-4 py-1.5 bg-rose-400/5 rounded-lg border border-rose-400/10"
                    >
                        <span class="text-[10px] font-bold text-rose-400"
                            >{ask.price.toFixed(3)}</span
                        >
                        <span class="text-[9px] font-black text-white/40"
                            >{Math.floor(ask.size)}</span
                        >
                    </div>
                {/each}
            </div>

            <!-- Bids (Green) -->
            <div
                class="flex-1 flex flex-col justify-start overflow-hidden gap-1"
            >
                {#each bourse.bids.slice(-3) as bid}
                    <div
                        class="flex justify-between items-center px-4 py-1.5 bg-emerald-400/5 rounded-lg border border-emerald-400/10"
                    >
                        <span class="text-[10px] font-bold text-emerald-400"
                            >{bid.price.toFixed(3)}</span
                        >
                        <span class="text-[9px] font-black text-white/40"
                            >{Math.floor(bid.size)}</span
                        >
                    </div>
                {/each}
            </div>
        </div>

        <!-- Reputation Bonds -->
        <div class="flex-1 flex flex-col gap-2 border-t border-white/5 pt-4">
            <div
                class="text-[8px] font-black text-cyan-400/60 uppercase px-2 mb-1 flex justify-between"
            >
                <span>Reputation_Bonds</span>
                <span>Active: {bourse.bonds.length}</span>
            </div>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-2">
                {#each bourse.bonds as bond}
                    <div
                        class="bg-white/[0.03] border border-white/5 p-3 rounded-xl flex justify-between items-center"
                    >
                        <div>
                            <div
                                class="text-[10px] font-black text-white uppercase"
                            >
                                {bond.issuer} // {bond.id}
                            </div>
                            <div
                                class="text-[7px] font-bold text-white/20 uppercase"
                            >
                                Maturity: {bond.maturity}
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-[10px] font-black text-cyan-400">
                                +{(bond.yield * 100).toFixed(1)}% Yield
                            </div>
                            <div
                                class="text-[7px] font-bold text-white/20 uppercase"
                            >
                                Parity: {bond.parity.toFixed(2)}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Order Entry -->
    <div class="space-y-4">
        <div class="grid grid-cols-2 gap-3">
            <button
                class="py-3 bg-emerald-400 text-black text-[10px] font-black uppercase tracking-widest rounded-2xl hover:brightness-110 active:scale-95 transition-all shadow-lg"
                onclick={() => placeOrder("BUY")}
            >
                Place_Bid
            </button>
            <button
                class="py-3 bg-rose-400 text-black text-[10px] font-black uppercase tracking-widest rounded-2xl hover:brightness-110 active:scale-95 transition-all shadow-lg"
                onclick={() => placeOrder("SELL")}
            >
                Place_Ask
            </button>
        </div>
        <div
            class="flex justify-between items-center text-[8px] font-black text-white/10 uppercase tracking-widest italic"
        >
            <span>Basel IV Compliant Route</span>
            <span>Spectral Band: 0xAA</span>
        </div>
    </div>
</div>
