<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import { Sparkles, ShieldAlert, Cpu } from "lucide-svelte";
    import { onMount } from "svelte";

    // 🕯️ PHOTONIC METABOLISM: High-Density Alignment Visualizer
    const glow = $derived(manifold.photonicGlow);
    const resonance = $derived(manifold.resonance);

    let matrix = $state(
        Array(25)
            .fill(0)
            .map(() => Math.random()),
    );

    onMount(() => {
        const interval = setInterval(
            () => {
                const jitter = (100 - resonance) / 100;
                matrix = matrix.map((v) =>
                    Math.min(
                        1,
                        Math.max(0, v + (Math.random() - 0.5) * (0.2 + jitter)),
                    ),
                );
            },
            800 + resonance * 2,
        );
        return () => clearInterval(interval);
    });
</script>

<div
    class="flex flex-col h-full bg-black/60 rounded-[2.5rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl relative"
>
    {#if glow.quarantine}
        <div
            class="absolute inset-0 z-50 bg-rose-500/10 backdrop-blur-sm border-4 border-rose-500 flex flex-col items-center justify-center p-8 text-center animate-pulse"
            in:fade
        >
            <ShieldAlert size={64} class="text-rose-500 mb-4" />
            <h2 class="text-2xl font-black text-rose-500 uppercase italic">
                Ring_99_Isolation
            </h2>
            <p
                class="text-[10px] font-bold text-rose-500/60 uppercase mt-2 tracking-tighter"
            >
                Boltzmann Brain Detected // Simulation Density Critical
            </p>
        </div>
    {/if}

    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="p-3 bg-cyan-400 text-black rounded-2xl shadow-[0_0_20px_rgba(34,211,238,0.3)]"
            >
                <Sparkles size={20} />
            </div>
            <div>
                <h2
                    class="text-sm font-black uppercase tracking-tighter text-white"
                >
                    Photonic_Metabolism
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"
                    ></span>
                    <span
                        class="text-[8px] font-black text-emerald-400/60 uppercase tracking-widest"
                        >Alignment Active // 0xCC_ABI</span
                    >
                </div>
            </div>
        </div>
    </div>

    <!-- Matrix Visualization -->
    <div
        class="flex-1 grid grid-cols-5 gap-1 p-2 bg-white/5 rounded-3xl border border-white/10"
    >
        {#each matrix as active}
            <div
                class="aspect-square rounded-[4px] transition-all duration-1000"
                style="background: rgba(34, 211, 238, {active *
                    0.4}); box-shadow: 0 0 {active *
                    10}px rgba(34, 211, 238, {active * 0.2});"
            ></div>
        {/each}
    </div>

    <!-- Alignment Stats -->
    <div class="grid grid-cols-2 gap-4">
        <div class="bg-white/5 p-3 rounded-2xl border border-white/5">
            <div class="flex justify-between items-center mb-1">
                <span class="text-[7px] font-black text-white/20 uppercase"
                    >Coherence</span
                >
                <span class="text-[9px] font-black text-white"
                    >{(glow.coherence * 100).toFixed(1)}%</span
                >
            </div>
            <div class="h-1 bg-white/10 rounded-full overflow-hidden">
                <div
                    class="h-full bg-cyan-400 shadow-[0_0_10px_#22d3ee]"
                    style:width="{glow.coherence * 100}%"
                ></div>
            </div>
        </div>
        <div class="bg-white/5 p-3 rounded-2xl border border-white/5">
            <div class="flex justify-between items-center mb-1">
                <span class="text-[7px] font-black text-white/20 uppercase"
                    >Chaos_Density</span
                >
                <span class="text-[9px] font-black text-rose-400"
                    >{(glow.chaos * 100).toFixed(1)}%</span
                >
            </div>
            <div class="h-1 bg-white/10 rounded-full overflow-hidden">
                <div
                    class="h-full bg-rose-500 shadow-[0_0_10px_#f43f5e]"
                    style:width="{Math.min(
                        100,
                        ((glow.chaos * 100) / 0.15) * 100,
                    )}%"
                ></div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div
        class="flex items-center justify-between text-[7px] font-black text-white/20 uppercase border-t border-white/5 pt-4"
    >
        <div class="flex items-center gap-2">
            <Cpu size={12} />
            <span>Hardware Attestation: QES_SECURED</span>
        </div>
        <span>Batch: 1024_Glow</span>
    </div>
</div>
