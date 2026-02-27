<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly } from "svelte/transition";
    import { Orbit, Radio, Target } from "lucide-svelte";

    // 🌀 SINGULARITY ENGINE: Omega Point Convergence Control
    const state = $derived(manifold.singularityState);
    const circular = $derived(manifold.circularState);
</script>

<div
    class="flex flex-col h-full bg-black/90 rounded-[3rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
>
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div
                class="p-4 bg-white/5 rounded-full text-white shadow-[0_0_30px_rgba(255,255,255,0.05)] group-hover:bg-white/10 transition-all animate-spin-slow"
            >
                <Orbit size={24} />
            </div>
            <div>
                <h2
                    class="text-base font-black uppercase tracking-tighter text-white"
                >
                    Singularity_Engine
                </h2>
                <div class="flex items-center gap-2" in:fly={{ y: -5 }}>
                    <span
                        class="w-2 h-2 rounded-full {state.status ===
                        'CONVERGING'
                            ? 'bg-emerald-400 animate-pulse'
                            : 'bg-white animate-ping'}"
                    ></span>
                    <span
                        class="text-[9px] font-black {state.status ===
                        'CONVERGING'
                            ? 'text-emerald-400/60'
                            : 'text-white/60'} uppercase tracking-widest"
                        >{state.status} // ABI_0xFD</span
                    >
                </div>
            </div>
        </div>
    </div>

    <div
        class="flex-1 relative flex items-center justify-center {state.status ===
        'HORIZON_LOCK'
            ? 'horizon-locked'
            : ''} {circular.status === 'CRISIS' ? 'crisis-shake' : ''}"
    >
        {#if state.status === "HORIZON_LOCK"}
            <div
                class="absolute inset-0 bg-white mix-blend-difference animate-pulse opacity-50"
            ></div>
            <div class="void-glitch"></div>
        {/if}

        {#if circular.status === "CRISIS"}
            <div
                class="absolute inset-0 bg-rose-500/10 animate-pulse z-20"
            ></div>
            <div
                class="absolute inset-0 pointer-events-none overflow-hidden opacity-30 z-30 flex items-center"
            >
                <div
                    class="text-[10px] font-black text-rose-500 whitespace-nowrap animate-marquee w-max flex gap-4"
                >
                    <span
                        >0x5C_BREACH_DETECTED // LOCALITY_ISOLATION_INIT //
                        DABBA_CRISIS //</span
                    >
                    <span
                        >0x5C_BREACH_DETECTED // LOCALITY_ISOLATION_INIT //
                        DABBA_CRISIS //</span
                    >
                    <span
                        >0x5C_BREACH_DETECTED // LOCALITY_ISOLATION_INIT //
                        DABBA_CRISIS //</span
                    >
                    <span
                        >0x5C_BREACH_DETECTED // LOCALITY_ISOLATION_INIT //
                        DABBA_CRISIS //</span
                    >
                </div>
            </div>
        {/if}

        <div
            class="absolute inset-0 bg-radial-gradient from-white/10 to-transparent opacity-20"
        ></div>

        <!-- Convergence Ring -->
        <div class="relative w-40 h-40 flex items-center justify-center">
            <div
                class="absolute inset-0 border-2 {state.status ===
                'HORIZON_LOCK'
                    ? 'border-amber-400'
                    : 'border-white/10'} rounded-full transition-all duration-1000"
                style:transform="scale({1 + state.convergence})"
            ></div>
            <div
                class="absolute inset-4 border {state.status === 'HORIZON_LOCK'
                    ? 'border-amber-400/50'
                    : 'border-white/5'} rounded-full transition-all duration-700"
                style:transform="scale({1 - state.convergence * 0.5})"
            ></div>

            <!-- Central Singularity -->
            <div
                class="w-12 h-12 {state.status === 'HORIZON_LOCK'
                    ? 'bg-amber-400 scale-[2.5]'
                    : 'bg-white'} rounded-full shadow-[0_0_50px_rgba(255,255,255,0.2)] flex items-center justify-center overflow-hidden transition-all duration-1000"
            >
                <div
                    class="w-full h-full {state.status === 'HORIZON_LOCK'
                        ? 'bg-black'
                        : 'bg-black'} transition-all duration-1000"
                    style:transform="scale({state.convergence})"
                ></div>
            </div>
        </div>
    </div>

    <!-- Convergence Control -->
    <div class="space-y-4">
        <div class="flex justify-between items-end mb-2">
            <div class="space-y-1">
                <span class="text-[8px] font-black text-white/20 uppercase"
                    >Convergence_Index</span
                >
                <span
                    class="block text-2xl font-black {state.status ===
                    'HORIZON_LOCK'
                        ? 'text-amber-400'
                        : 'text-white'} italic tracking-tighter"
                    >{(state.convergence * 100).toFixed(2)}%</span
                >
            </div>
            {#if state.status !== "HORIZON_LOCK"}
                <button
                    class="px-4 py-2 bg-white text-black text-[10px] font-black uppercase rounded-xl hover:scale-105 transition-all active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]"
                    onclick={() => manifold.boostConvergence()}
                >
                    Boost_Alpha
                </button>
            {:else}
                <div
                    class="px-4 py-2 bg-amber-400/10 border border-amber-400/50 text-amber-400 text-[10px] font-black uppercase rounded-xl animate-pulse"
                >
                    CAUSAL_LOCKED
                </div>
            {/if}
        </div>

        <div class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
            <div
                class="h-full {state.status === 'HORIZON_LOCK'
                    ? 'bg-amber-400'
                    : 'bg-white'} shadow-[0_0_20px_rgba(255,255,255,0.8)] transition-all duration-1000"
                style:width="{state.convergence * 100}%"
            ></div>
        </div>
    </div>

    <div class="flex items-center justify-between pt-6 border-t border-white/5">
        <div class="flex items-center gap-2">
            <Target size={14} class="text-white/40" />
            <span class="text-[8px] font-black text-white/20 uppercase"
                >Horizon_Lock: {state.horizonId}</span
            >
        </div>
        <div class="flex items-center gap-1">
            <Radio size={12} class="text-emerald-400 animate-pulse" />
            <span
                class="text-[8px] font-black text-emerald-400 uppercase tracking-widest"
                >QES_LINK</span
            >
        </div>
    </div>
</div>

<style>
    .animate-spin-slow {
        animation: spin 10s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    .horizon-locked {
        background: radial-gradient(
            circle at center,
            rgba(251, 191, 36, 0.1) 0%,
            transparent 70%
        );
    }
    .void-glitch {
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(251, 191, 36, 0.05) 0px,
            transparent 1px
        );
        pointer-events: none;
    }
    @keyframes guard-scan {
        from {
            background-position: 0 0;
        }
        to {
            background-position: 0 100%;
        }
    }
    .crisis-shake {
        animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        transform: translate3d(0, 0, 0);
        backface-visibility: hidden;
        perspective: 1000px;
    }
    @keyframes shake {
        10%,
        90% {
            transform: translate3d(-1px, 0, 0);
        }
        20%,
        80% {
            transform: translate3d(2px, 0, 0);
        }
        30%,
        50%,
        70% {
            transform: translate3d(-4px, 0, 0);
        }
        40%,
        60% {
            transform: translate3d(4px, 0, 0);
        }
    }
    .animate-marquee {
        animation: marquee 5s linear infinite;
    }
    @keyframes marquee {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50%);
        }
    }
</style>
