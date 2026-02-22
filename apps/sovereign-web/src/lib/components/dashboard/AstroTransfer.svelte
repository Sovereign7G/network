<script lang="ts">
    import {
        Send,
        ArrowRight,
        Wallet,
        ShieldCheck,
        Zap,
        X,
    } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import { AAL3Service } from "../../auth/aal3";
    import { onMount } from "svelte";

    let { onClose, showWisdom } = $props();

    const aal3 = AAL3Service.getInstance();
    let isAAL3Verified = $state(false);

    onMount(() => {
        isAAL3Verified = aal3.isVerified();
    });

    let amount = $state("");
    let destination = $state("");
    let isProcessing = $state(false);
    let step = $state(1);

    function nextStep() {
        if (step === 1 && amount && destination) {
            step = 2;
        } else if (step === 2) {
            isProcessing = true;
            setTimeout(() => {
                isProcessing = false;
                step = 3;
            }, 2500);
        }
    }
</script>

<div class="max-w-2xl mx-auto space-y-12" in:fade>
    <div class="text-center space-y-4">
        <h2 class="text-4xl font-black italic tracking-tighter uppercase">
            ASTRO TRANSFER
        </h2>
        <p
            class="text-[10px] mono-font text-white/40 uppercase tracking-[0.3em]"
        >
            Quantum-Asynchronous Value Teleportation
        </p>
    </div>

    <div class="glass-panel p-10 space-y-8 relative overflow-hidden">
        <button
            onclick={onClose}
            class="absolute top-6 right-6 p-2 text-white/20 hover:text-white/60 transition-all z-20"
        >
            <X size={24} />
        </button>
        <div class="flex justify-between items-center mb-10 px-4">
            {#each [1, 2, 3] as s}
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-black {step >=
                        s
                            ? 'bg-neon-cyan text-black'
                            : 'bg-white/5 text-white/20 border border-white/10'} transition-all"
                    >
                        {s}
                    </div>
                    {#if s < 3}
                        <div
                            class="w-16 h-0.5 {step > s
                                ? 'bg-neon-cyan'
                                : 'bg-white/5'} transition-all"
                        ></div>
                    {/if}
                </div>
            {/each}
        </div>

        <div
            class="absolute -left-20 -top-20 w-64 h-64 bg-neon-cyan/5 rounded-full blur-3xl"
        ></div>

        {#if step === 1}
            <div class="space-y-6" in:fade>
                <div class="space-y-3">
                    <span
                        class="text-[10px] font-black text-white/40 uppercase tracking-widest ml-4 block mb-3"
                        >Source Vault</span
                    >
                    <div
                        class="p-6 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-between"
                    >
                        <div class="flex items-center gap-4">
                            <div
                                class="w-10 h-10 rounded-xl bg-neon-cyan/20 flex items-center justify-center text-neon-cyan"
                            >
                                <Wallet size={20} />
                            </div>
                            <div>
                                <div class="text-sm font-black uppercase">
                                    Main Sovereign Vault
                                </div>
                                <div
                                    class="text-[10px] text-white/30 mono-font"
                                >
                                    0xFD...7782
                                </div>
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-sm font-black">$12,450.00</div>
                            <div
                                class="text-[10px] text-neon-cyan uppercase font-bold"
                            >
                                Available
                            </div>
                        </div>
                    </div>
                </div>

                <div class="space-y-3">
                    <label
                        for="destination"
                        class="text-[10px] font-black text-white/40 uppercase tracking-widest ml-4"
                        >Destination Principal</label
                    >
                    <input
                        id="destination"
                        type="text"
                        bind:value={destination}
                        placeholder="ryjl3-tyaaa-aaaaa-aaaba-cai"
                        class="w-full p-6 bg-white/5 border border-white/10 rounded-2xl text-white placeholder:text-white/10 font-bold focus:border-neon-cyan/50 focus:outline-none transition-all"
                    />
                </div>

                <div class="space-y-3">
                    <label
                        for="amount"
                        class="text-[10px] font-black text-white/40 uppercase tracking-widest ml-4"
                        >Amount (AGE)</label
                    >
                    <div class="relative">
                        <input
                            id="amount"
                            type="number"
                            bind:value={amount}
                            placeholder="0.00"
                            class="w-full p-8 bg-white/5 border border-white/10 rounded-2xl text-5xl font-black italic text-white placeholder:text-white/10 focus:border-neon-cyan/50 focus:outline-none transition-all pr-32"
                        />
                        <div
                            class="absolute right-8 top-1/2 -translate-y-1/2 text-2xl font-black text-neon-cyan opacity-40 italic"
                        >
                            AGE
                        </div>
                        {#if showWisdom && amount}
                            <div
                                class="absolute -right-4 -top-4 px-3 py-1 bg-amber-400 text-black text-[9px] font-black rounded-lg shadow-xl z-30 animate-in fade-in zoom-in"
                            >
                                FEEDBACK: Destination shard requires {(
                                    parseFloat(amount) * 0.01
                                ).toFixed(2)} AGE for causal anchoring.
                            </div>
                        {/if}
                    </div>
                    <div class="flex gap-2 ml-4">
                        {#each [10, 50, 100, "Max"] as quick}
                            <button
                                onclick={() =>
                                    (amount =
                                        quick === "Max"
                                            ? "12450"
                                            : quick.toString())}
                                class="text-[10px] font-bold text-white/30 hover:text-neon-cyan transition-colors"
                            >
                                {quick === "Max" ? "" : "+"}{quick}
                            </button>
                        {/each}
                    </div>
                </div>

                <div class="space-y-4 pt-4">
                    <div class="flex items-center justify-between px-4">
                        <span
                            class="text-[10px] font-black text-white/20 uppercase tracking-[0.2em]"
                            >Teleportation_Spec</span
                        >
                        <div class="flex items-center gap-2">
                            <input
                                type="checkbox"
                                class="w-3 h-3 accent-neon-cyan"
                                checked
                            />
                            <span
                                class="text-[8px] font-bold text-white/40 uppercase"
                                >ONE_CLICK_ANCHOR</span
                            >
                        </div>
                    </div>

                    <div
                        class="bg-black/40 border border-white/5 rounded-3xl p-6 space-y-4"
                    >
                        <div
                            class="flex justify-between items-center text-[10px] font-bold text-white/40 uppercase tracking-widest"
                        >
                            <span>Quantum_Causal_Tax</span>
                            <span class="text-white">0.02 AGE</span>
                        </div>
                        <div
                            class="flex justify-between items-center text-[10px] font-bold text-white/40 uppercase tracking-widest"
                        >
                            <span>Network_Merit_Fee</span>
                            <span class="text-white">0.05 AGE</span>
                        </div>
                        <div
                            class="pt-4 border-t border-white/5 flex justify-between items-center text-xs font-black uppercase tracking-widest"
                        >
                            <span class="text-white/60">Total_Spec_Cost</span>
                            <span class="text-neon-cyan"
                                >{(parseFloat(amount || "0") + 0.07).toFixed(2)}
                                AGE</span
                            >
                        </div>
                    </div>
                </div>

                <button
                    onclick={nextStep}
                    disabled={!amount || !destination}
                    class="w-full py-6 bg-neon-cyan text-black font-black uppercase tracking-tighter text-xl rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all shadow-[0_0_30px_rgba(0,242,255,0.2)] disabled:opacity-30 disabled:grayscale"
                >
                    INITIALIZE_TELEPORTATION_CEREMONY <ArrowRight
                        size={20}
                        class="inline ml-2"
                    />
                </button>
            </div>
        {:else if step === 2}
            <div class="space-y-8" in:fade>
                <div
                    class="text-xs font-black uppercase tracking-[0.3em] text-white/20 mb-[-1.5rem] ml-4"
                >
                    Teleportation_spec_v1.7
                </div>
                <div
                    class="p-8 bg-black/40 border border-white/[0.05] rounded-3xl space-y-6 relative overflow-hidden"
                >
                    <div class="grid grid-cols-2 gap-8 relative z-10">
                        <div class="space-y-4">
                            <div class="space-y-1">
                                <span
                                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                    >QUANTUM_VALUE</span
                                >
                                <div
                                    class="text-3xl font-black italic text-neon-cyan"
                                >
                                    {amount}
                                    <span class="text-xs opacity-40">AGE</span>
                                </div>
                            </div>
                            <div class="space-y-1">
                                <span
                                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                    >CLEARANCE_PROTOCOL</span
                                >
                                <div
                                    class="flex items-center gap-2 text-[10px] font-black uppercase {isAAL3Verified
                                        ? 'text-green-400'
                                        : 'text-amber-400'}"
                                >
                                    {#if isAAL3Verified}
                                        <ShieldCheck size={14} /> AAL3_SOVEREIGN
                                    {:else}
                                        <Zap size={14} /> GUEST_CLEARANCE
                                    {/if}
                                </div>
                            </div>
                        </div>
                        <div class="space-y-4 text-right">
                            <div class="space-y-1">
                                <span
                                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                    >DESTINATION_SHARD</span
                                >
                                <div
                                    class="text-[10px] mono-font text-white/60 truncate"
                                >
                                    {destination}
                                </div>
                            </div>
                            <div class="space-y-1">
                                <span
                                    class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                    >CAUSAL_INTEGRITY</span
                                >
                                <div
                                    class="text-sm font-black text-neon-cyan italic"
                                >
                                    99.98% <span
                                        class="text-[8px] mono-font opacity-40"
                                        >COHERENT</span
                                    >
                                </div>
                            </div>
                        </div>
                    </div>

                    <div
                        class="pt-6 border-t border-white/[0.05] flex justify-between items-center relative z-10"
                    >
                        <div class="space-y-1">
                            <span
                                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                >LATENCY_ESTIMATE</span
                            >
                            <div class="text-[10px] mono-font text-white/40">
                                14ms // QUANTUM_ERR: 0.002%
                            </div>
                        </div>
                        <div class="flex items-center gap-4">
                            <div
                                class="px-2 py-1 bg-neon-cyan/10 rounded text-[7px] font-black text-neon-cyan uppercase tracking-widest border border-neon-cyan/20"
                            >
                                READY_FOR_ANCHOR
                            </div>
                        </div>
                    </div>

                    <!-- Ambient Glow -->
                    <div
                        class="absolute -right-20 -bottom-20 w-40 h-40 bg-neon-cyan/5 rounded-full blur-3xl"
                    ></div>
                </div>

                <button
                    onclick={nextStep}
                    disabled={isProcessing}
                    class="w-full py-6 bg-neon-cyan text-black font-black uppercase tracking-tighter text-xl rounded-2xl hover:scale-[1.02] transition-all relative overflow-hidden"
                >
                    {#if isProcessing}
                        <div
                            class="absolute inset-0 bg-black/20 overflow-hidden"
                        >
                            <div
                                class="h-full bg-neon-cyan/40 animate-pulse relative"
                            >
                                <div
                                    class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent w-20 h-full animate-[scan_2s_linear_infinite]"
                                ></div>
                            </div>
                        </div>
                        <div
                            class="relative z-10 flex items-center justify-center gap-3"
                        >
                            <div
                                class="w-5 h-5 border-3 border-black border-t-transparent rounded-full animate-spin"
                            ></div>
                            CAUSAL RENDERING...
                        </div>
                    {:else}
                        CONFIRM & TELEPORT
                    {/if}
                </button>
            </div>
        {:else if step === 3}
            <div
                class="flex flex-col items-center justify-center py-12 space-y-6 text-center"
                in:fade
            >
                <div
                    class="w-24 h-24 rounded-full bg-neon-cyan/10 border border-neon-cyan/30 flex items-center justify-center text-neon-cyan animate-bounce"
                >
                    <Zap size={48} />
                </div>
                <div class="space-y-2">
                    <h3 class="text-3xl font-black italic">
                        TELEPORTATION COMPLETE
                    </h3>
                    <p class="text-white/40 text-sm">
                        Value successfully anchored in destination shard.
                    </p>
                </div>
                <div
                    class="mono-font text-[10px] text-white/20 p-4 bg-white/5 rounded-xl border border-white/5"
                >
                    TXID: 0xAGE_BEEF_8822_COFFEE_LUV
                </div>
                <button
                    onclick={() => (step = 1)}
                    class="px-10 py-4 border border-white/10 rounded-2xl font-black uppercase tracking-widest text-[10px] hover:bg-white/5 transition-all"
                >
                    START NEW TRANSFER
                </button>
            </div>
        {/if}
    </div>
</div>

<style>
    @keyframes scan {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(500%);
        }
    }

    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(60px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 2.5rem;
        box-shadow:
            0 40px 100px -20px rgba(0, 0, 0, 0.8),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
</style>
