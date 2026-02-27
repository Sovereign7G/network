<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";

    import { Wallet, Shield, Navigation2, Star, Activity } from "lucide-svelte";

    const wallet = $derived(manifold.walletState);
    const resonance = $derived(manifold.resonance);
</script>

<div
    class="flex flex-col h-full bg-gradient-to-br from-indigo-900/40 to-black/80 rounded-[3rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
>
    <!-- Visual Glow -->
    <div
        class="absolute -top-24 -right-24 w-64 h-64 bg-cyan-400/10 rounded-full blur-[100px] pointer-events-none"
    ></div>

    <!-- Top Row: Identity & Status -->
    <div class="flex justify-between items-start z-10">
        <div class="flex items-center gap-4">
            <div
                class="w-16 h-16 rounded-full bg-white/5 border border-white/10 flex items-center justify-center backdrop-blur-3xl overflow-hidden relative"
            >
                <div
                    class="absolute inset-0 bg-gradient-to-t from-cyan-400/20 to-transparent"
                ></div>
                <Wallet size={24} class="text-white relative z-10" />
            </div>
            <div>
                <h2
                    class="text-lg font-black text-white italic tracking-tighter"
                >
                    Sovereign_Identity
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="px-2 py-0.5 bg-cyan-400 text-black text-[8px] font-black uppercase rounded-md tracking-widest"
                        >{wallet.compliance}</span
                    >
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Shard-0x042</span
                    >
                </div>
            </div>
        </div>
        <div class="text-right">
            <div class="text-[8px] font-black text-white/20 uppercase mb-2">
                Manifold_Distance
            </div>
            <div class="flex items-center gap-2 justify-end">
                <Navigation2 size={12} class="rotate-45 text-emerald-400" />
                <span class="text-xs font-black text-white"
                    >{wallet.manifoldDistance.toFixed(3)}</span
                >
            </div>
        </div>
    </div>

    <!-- Main Balances -->
    <div class="space-y-6 z-10">
        <div class="space-y-1">
            <span
                class="text-[9px] font-black text-white/20 uppercase tracking-[0.3em]"
                >Moral_Credit_Supply</span
            >
            <div class="flex items-baseline gap-2">
                <span
                    class="text-5xl font-black text-white tracking-tighter tabular-nums"
                    >{wallet.moralCredits.toLocaleString()}</span
                >
                <span class="text-lg font-black text-cyan-400 uppercase"
                    >Credits</span
                >
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div
                class="p-5 bg-white/5 border border-white/5 rounded-3xl group/item hover:bg-white/10 transition-all"
            >
                <div class="flex justify-between items-center mb-2">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >System_Merits</span
                    >
                    <Star size={12} class="text-amber-400" />
                </div>
                <div class="text-2xl font-black text-white">
                    {wallet.merits}
                </div>
            </div>
            <div
                class="p-5 bg-white/5 border border-white/5 rounded-3xl group/item hover:bg-white/10 transition-all"
            >
                <div class="flex justify-between items-center mb-2">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >Rep_Multiplier</span
                    >
                    <Activity size={12} class="text-cyan-400" />
                </div>
                <div class="text-2xl font-black text-cyan-400">
                    {(wallet.reputationScore * 100).toFixed(1)}%
                </div>
            </div>
        </div>
    </div>

    <!-- Progress / Compliance -->
    <div class="space-y-4 z-10 flex-1 flex flex-col justify-end">
        <div
            class="bg-white/5 rounded-3xl p-6 border border-white/10 relative overflow-hidden"
        >
            <div
                class="absolute inset-0 bg-gradient-to-r from-cyan-400/5 to-transparent"
            ></div>
            <div class="flex justify-between items-center mb-4 relative z-10">
                <div class="flex items-center gap-2">
                    <Shield size={16} class="text-emerald-400" />
                    <span
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                        >Dissonance_Immunity</span
                    >
                </div>
                <span class="text-[10px] font-black text-emerald-400"
                    >ACTIVE</span
                >
            </div>
            <!-- Progress Bar -->
            <div
                class="h-2 w-full bg-white/5 rounded-full overflow-hidden relative z-10"
            >
                <div
                    class="h-full bg-gradient-to-r from-cyan-400 to-emerald-400 transition-all duration-1000"
                    style:width="{resonance}%"
                ></div>
            </div>
            <div
                class="mt-3 flex justify-between text-[8px] font-black text-white/20 uppercase tracking-widest relative z-10"
            >
                <span>Resonance Threshold</span>
                <span class="text-white/40">{resonance}%</span>
            </div>
        </div>

        <button
            class="w-full py-5 bg-white text-black text-[11px] font-black uppercase tracking-[0.2em] rounded-3xl hover:bg-cyan-400 hover:scale-[1.02] active:scale-95 transition-all shadow-[0_0_40px_rgba(255,255,255,0.1)]"
            onclick={() => manifold.claimDividend()}
        >
            Claim_Moral_Dividend
        </button>
    </div>
</div>
