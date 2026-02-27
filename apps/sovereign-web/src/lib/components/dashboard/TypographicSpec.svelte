<script lang="ts">
    import { scale } from "svelte/transition";
    import { Type, Ruler, MoveHorizontal, Target } from "lucide-svelte";

    let kerningActive = $state(true);
    let opticalGuides = $state(true);

    // Symbolic metadata for the "Invisible Engineering" visualization
    const glyphSpecs = [
        { char: "S", offset: -0.02, tension: 0.95 },
        { char: "O", offset: 0.04, tension: 1.05 },
        { char: "V", offset: -0.08, tension: 0.88 },
        { char: "E", offset: 0.01, tension: 0.92 },
        { char: "R", offset: 0.03, tension: 0.98 },
        { char: "E", offset: 0.01, tension: 0.92 },
        { char: "I", offset: 0.0, tension: 1.0 },
        { char: "G", offset: 0.05, tension: 1.08 },
        { char: "N", offset: -0.02, tension: 0.94 },
    ];
</script>

<div
    class="typographic-spec-manifold bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group font-sans"
>
    <!-- Blueprint Header -->
    <header class="flex justify-between items-start z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-amber-400/10 rounded-2xl text-amber-400 border border-amber-400/20 shadow-[0_0_20px_rgba(251,191,36,0.1)]"
            >
                <Type size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Typographic_Spec_v2.1
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Invisible_Engineering // Causal_Kerning_Analyzer
                </p>
            </div>
        </div>
        <div class="flex gap-2">
            <button
                onclick={() => (kerningActive = !kerningActive)}
                class="px-3 py-1.5 rounded-full text-[8px] font-black uppercase tracking-widest border transition-all {kerningActive
                    ? 'bg-amber-400 text-black border-amber-400'
                    : 'bg-white/5 text-white/40 border-white/10'}"
            >
                KERNING_{kerningActive ? "ACTIVE" : "RAW"}
            </button>
        </div>
    </header>

    <!-- Main Visualization Area -->
    <div
        class="flex-1 flex flex-col items-center justify-center relative min-h-[200px] z-10"
    >
        <!-- Optical Baseline -->
        <div
            class="absolute w-full h-px bg-white/5 top-1/2 translate-y-[30px]"
        ></div>
        <div
            class="absolute w-full h-px bg-white/5 top-1/2 translate-y-[-50px]"
        ></div>

        <div class="flex items-center gap-0 relative">
            {#each glyphSpecs as spec, i}
                <div
                    class="relative flex flex-col items-center transition-all duration-700"
                    style:margin-left={kerningActive
                        ? `${spec.offset * 100}px`
                        : "0px"}
                >
                    <!-- Glyph Label -->
                    <span
                        class="absolute -top-12 text-[7px] font-mono text-white/20 uppercase tracking-tighter"
                    >
                        0x{spec.char.charCodeAt(0).toString(16)}
                    </span>

                    <!-- The Character -->
                    <span
                        class="text-7xl font-black text-white selection:bg-amber-400/30 transition-all duration-700"
                        style:filter={opticalGuides
                            ? "drop-shadow(0 0 1px rgba(255,255,255,0.1))"
                            : "none"}
                        style:transform={opticalGuides
                            ? `scaleX(${spec.tension})`
                            : "scale(1)"}
                    >
                        {spec.char}
                    </span>

                    <!-- Kerning Indicators -->
                    {#if kerningActive && i < glyphSpecs.length - 1}
                        <div
                            class="absolute right-0 top-1/2 translate-x-full opacity-40"
                        >
                            <div class="w-px h-8 bg-amber-400/50"></div>
                            <span
                                class="absolute -top-3 left-1 text-[6px] font-mono text-amber-400"
                            >
                                {spec.offset > 0 ? "+" : ""}{spec.offset}
                            </span>
                        </div>
                    {/if}

                    <!-- Optical Anchors -->
                    {#if opticalGuides}
                        <div
                            class="absolute -bottom-6 w-1 h-1 bg-cyan-400/40 rounded-full animate-pulse"
                        ></div>
                    {/if}
                </div>
            {/each}
        </div>

        {#if opticalGuides}
            <div
                class="absolute inset-x-0 bottom-4 flex justify-between px-12 opacity-20 transition-opacity"
            >
                <span
                    class="text-[8px] font-black text-white/50 border-l border-white/20 pl-2"
                    >ASCENDER_MAX</span
                >
                <span
                    class="text-[8px] font-black text-white/50 border-l border-white/20 pl-2"
                    >X_HEIGHT_AVG</span
                >
                <span
                    class="text-[8px] font-black text-white/50 border-l border-white/20 pl-2"
                    >DESCENDER_MIN</span
                >
            </div>
        {/if}
    </div>

    <!-- Technical Ledger -->
    <footer
        class="mt-auto grid grid-cols-3 gap-6 pt-6 border-t border-white/10 z-10"
    >
        <div class="space-y-2">
            <div class="flex items-center gap-2">
                <Ruler size={12} class="text-amber-400" />
                <span
                    class="text-[9px] font-black text-white uppercase tracking-widest"
                    >Stroke_Engine</span
                >
            </div>
            <p class="text-[8px] text-white/30 leading-relaxed italic">
                Optimizing weight ratios for high-density OLED manifolds.
            </p>
        </div>
        <div class="space-y-2">
            <div class="flex items-center gap-2">
                <MoveHorizontal size={12} class="text-cyan-400" />
                <span
                    class="text-[9px] font-black text-white uppercase tracking-widest"
                    >Optical_Lag</span
                >
            </div>
            <p class="text-[8px] text-white/30 leading-relaxed italic">
                Compensating for retinal persistence and pixel blooming.
            </p>
        </div>
        <div class="space-y-2">
            <div class="flex items-center gap-2">
                <Target size={12} class="text-emerald-400" />
                <span
                    class="text-[9px] font-black text-white uppercase tracking-widest"
                    >Friction_Audit</span
                >
            </div>
            <div class="flex items-center gap-2">
                <div class="flex-1 h-1 bg-white/5 rounded-full overflow-hidden">
                    <div
                        class="h-full bg-emerald-400 w-[94%]"
                        style="transform-origin: left;"
                        in:scale={{ duration: 1000 }}
                    ></div>
                </div>
                <span class="text-[8px] font-bold text-emerald-400">94.2%</span>
            </div>
        </div>
    </footer>

    <!-- Background Blueprint Grid -->
    <div
        class="absolute inset-0 opacity-[0.03] pointer-events-none"
        style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 40px 40px;"
    ></div>
</div>

<style>
</style>
