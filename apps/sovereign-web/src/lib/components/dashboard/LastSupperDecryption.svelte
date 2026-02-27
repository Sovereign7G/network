<script lang="ts">
    import { DECODED_FRAGMENTS } from "$lib/registries/davinci-wisdom";
    import { fade } from "svelte/transition";
    import { Eye, Lock, Cpu } from "lucide-svelte";
    import { onMount } from "svelte";

    let scanning = $state(false);
    let selectedIndex = $state(0);
    let activeFragment = $derived(DECODED_FRAGMENTS[selectedIndex]);
    let revealProgress = $state(0);

    onMount(() => {
        const interval = setInterval(() => {
            if (!scanning) {
                selectedIndex = (selectedIndex + 1) % DECODED_FRAGMENTS.length;
            }
        }, 10000);
        return () => clearInterval(interval);
    });

    async function runDecryption() {
        scanning = true;
        revealProgress = 0;

        const duration = 2000;
        const start = Date.now();

        const tick = () => {
            const elapsed = Date.now() - start;
            revealProgress = Math.min(100, (elapsed / duration) * 100);

            if (revealProgress < 100) {
                requestAnimationFrame(tick);
            } else {
                setTimeout(() => {
                    scanning = false;
                }, 500);
            }
        };

        requestAnimationFrame(tick);
    }
</script>

<div
    class="spectral-analyzer bg-black/80 rounded-[2.5rem] border border-cyan-500/20 backdrop-blur-3xl p-6 h-full flex flex-col gap-6 relative overflow-hidden group"
>
    <!-- Grid Overlay -->
    <div
        class="absolute inset-0 bg-[linear-gradient(rgba(34,211,238,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(34,211,238,0.05)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none"
    ></div>

    <!-- Scanning Scanline -->
    {#if scanning}
        <div
            class="absolute left-0 right-0 h-1 bg-cyan-400 shadow-[0_0_15px_#22d3ee] z-10"
            style:top="{revealProgress}%"
            transition:fade
        ></div>
    {/if}

    <header class="flex justify-between items-start z-10">
        <div class="flex gap-4">
            <div
                class="p-3 bg-cyan-400/10 rounded-2xl text-cyan-400 border border-cyan-400/20"
            >
                <Eye size={20} class={scanning ? "animate-pulse" : ""} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.3em] text-white"
                >
                    Spectral_Decryption
                </h2>
                <span
                    class="text-[8px] font-black text-white/30 uppercase italic"
                    >Aether_Borealis // DaVinci_Mural_Scan</span
                >
            </div>
        </div>
        <div class="flex gap-2">
            <div
                class="w-2 h-2 rounded-full {scanning
                    ? 'bg-rose-500 animate-ping'
                    : 'bg-cyan-500'}"
            ></div>
            <span class="text-[8px] font-black text-white/40 uppercase"
                >{scanning ? "Active_Scan" : "Standby"}</span
            >
        </div>
    </header>

    <div
        class="flex-1 flex flex-col items-center justify-center relative min-h-[200px] z-10"
    >
        <!-- Speculative "Last Supper" Shape Geometry -->
        <div
            class="relative w-full aspect-video border border-white/5 rounded-2xl flex items-center justify-center overflow-hidden bg-black/40"
        >
            <!-- Symbolic "Last Supper" Layout -->
            <div class="flex gap-4 items-end pb-8">
                {#each Array(12) as _, i}
                    <div
                        class="w-3 bg-white/10 rounded-t-lg transition-all duration-700"
                        style:height="{30 + (i % 3) * 15}%"
                        class:bg-cyan-400={i === selectedIndex % 12}
                        class:opacity-100={scanning}
                        class:opacity-20={!scanning}
                    ></div>
                {/each}
            </div>
            <div
                class="absolute bottom-4 left-1/2 -translate-x-1/2 w-12 h-20 bg-cyan-400/20 rounded-t-3xl blur-md"
            ></div>
            <div
                class="absolute bottom-6 left-1/2 -translate-x-1/2 w-8 h-16 bg-white/20 rounded-t-2xl"
            ></div>

            {#if scanning}
                <div
                    class="absolute inset-0 bg-cyan-400/10 animate-pulse flex items-center justify-center"
                >
                    <span
                        class="text-[10px] font-black text-cyan-400 uppercase tracking-widest"
                        >Reconstructing_Geometry</span
                    >
                </div>
            {/if}
        </div>

        <div class="mt-8 text-center px-4 w-full">
            <span
                class="text-[7px] font-black text-cyan-400/60 uppercase tracking-widest block mb-2"
                >Decoded_Axiom // {activeFragment.focus}</span
            >
            <div class="min-h-[60px] flex items-center justify-center">
                {#if !scanning}
                    <p
                        class="text-sm font-light italic leading-relaxed text-white/80"
                        in:fade={{ delay: 200 }}
                    >
                        "{activeFragment.text}"
                    </p>
                {:else}
                    <div class="flex gap-1">
                        {#each Array(5) as _, i}
                            <div
                                class="w-1 h-3 bg-cyan-400 animate-bounce"
                                style:animation-delay="{i * 0.1}s"
                            ></div>
                        {/each}
                    </div>
                {/if}
            </div>
            <div
                class="mt-4 py-1 px-3 bg-white/5 inline-block rounded-full border border-white/10"
            >
                <span class="text-[8px] font-black text-white/40 uppercase"
                    >Origin: {activeFragment.source}</span
                >
            </div>
        </div>
    </div>

    <footer class="mt-auto pt-6 border-top border-white/5 flex gap-4 z-10">
        <button
            onclick={runDecryption}
            disabled={scanning}
            class="flex-1 py-3 bg-white text-black rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-cyan-400 transition-all flex items-center justify-center gap-2 group/btn"
        >
            <Cpu
                size={14}
                class="group-hover/btn:rotate-12 transition-transform"
            />
            Initiate_Spectral_Scan
        </button>
        <div
            class="p-3 bg-white/5 rounded-xl text-white/40 border border-white/10 hover:border-cyan-400/40 hover:text-cyan-400 cursor-help transition-all group/info"
        >
            <Lock size={14} />
            <div
                class="absolute bottom-20 right-6 w-48 bg-black p-3 rounded-xl border border-white/10 opacity-0 group-hover/info:opacity-100 transition-opacity pointer-events-none"
            >
                <h4 class="text-[8px] font-black uppercase mb-1">
                    AAL3 Security Disclosure
                </h4>
                <p class="text-[7px] leading-tight text-white/40">
                    Speculative decryption of hyperspectral patterns found in
                    institutional murals. Basel IV non-binding heuristics.
                </p>
            </div>
        </div>
    </footer>
</div>

<style>
    .spectral-analyzer::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle at center,
            rgba(34, 211, 238, 0.03) 0%,
            transparent 70%
        );
        pointer-events: none;
    }
</style>
