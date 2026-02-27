<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { Activity, Moon, Footprints, Info } from "lucide-svelte";
    import { api } from "$lib/services/api";

    let vitals: any = $state(null);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            vitals = await api.request("/somatic/vitals");
        } catch (error) {
            console.error("Failed to load somatic vitals", error);
        } finally {
            isLoading = false;
        }
    });

    function getEnergyColor(level: string) {
        switch (level) {
            case "HIGH":
                return "#10B981";
            case "MODERATE":
                return "#34D399";
            case "LOW":
                return "#F59E0B";
            default:
                return "#EF4444";
        }
    }
</script>

<div
    class="somatic-rhythm glass-panel p-6 h-full flex flex-col relative overflow-hidden"
    in:fade
>
    <!-- Background Resonance Aura -->
    {#if vitals}
        <div
            class="absolute top-0 right-0 w-64 h-64 blur-[100px] opacity-10 pointer-events-none transition-colors duration-1000"
            style="background: {getEnergyColor(vitals.energy.level)};"
        ></div>
    {/if}

    <div class="flex justify-between items-start mb-8 relative z-10">
        <div>
            <h3
                class="text-[10px] font-black uppercase tracking-[0.4em] text-white/30 mb-1"
            >
                Somatic_Manifold
            </h3>
            <p class="text-xs font-bold text-white/60">
                Bio-Metric Resonance Loop
            </p>
        </div>
        {#if vitals}
            <div class="flex flex-col items-end">
                <span
                    class="status-pill text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full border border-white/5 bg-white/5 transition-all duration-500"
                    style="color: {getEnergyColor(
                        vitals.energy.level,
                    )}; border-color: {getEnergyColor(vitals.energy.level)}20;"
                >
                    <Activity size={10} class="inline-block mr-1" />
                    {vitals.energy.level}
                </span>
            </div>
        {/if}
    </div>

    {#if isLoading}
        <div class="flex-1 flex flex-col items-center justify-center gap-4">
            <div class="premium-loader"></div>
            <span
                class="text-[10px] font-black text-white/20 uppercase tracking-[0.2em] animate-pulse"
                >Synchronizing_Vitals</span
            >
        </div>
    {:else if vitals}
        <div
            class="flex-1 flex flex-col items-center justify-center relative py-4"
        >
            <!-- Advanced SVG Rhythms -->
            <div class="relative group">
                <svg
                    viewBox="0 0 240 240"
                    class="w-56 h-56 transition-transform duration-700 group-hover:scale-105"
                >
                    <defs>
                        <linearGradient
                            id="energyGradient"
                            x1="0%"
                            y1="0%"
                            x2="100%"
                            y2="100%"
                        >
                            <stop
                                offset="0%"
                                stop-color={getEnergyColor(vitals.energy.level)}
                            />
                            <stop offset="100%" stop-color="#3b82f6" />
                        </linearGradient>
                        <filter id="glow">
                            <feGaussianBlur
                                stdDeviation="4"
                                result="coloredBlur"
                            />
                            <feMerge>
                                <feMergeNode in="coloredBlur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    <!-- Structural Rings -->
                    <circle
                        cx="120"
                        cy="120"
                        r="100"
                        fill="none"
                        stroke="rgba(255,255,255,0.02)"
                        stroke-width="1"
                    />
                    <circle
                        cx="120"
                        cy="120"
                        r="80"
                        fill="none"
                        stroke="rgba(255,255,255,0.03)"
                        stroke-width="1"
                        stroke-dasharray="4 8"
                    />

                    <!-- Movement Progress (Outer) -->
                    <circle
                        cx="120"
                        cy="120"
                        r="90"
                        fill="none"
                        stroke="rgba(255,255,255,0.05)"
                        stroke-width="12"
                        stroke-linecap="round"
                    />
                    <circle
                        cx="120"
                        cy="120"
                        r="90"
                        fill="none"
                        stroke="url(#energyGradient)"
                        stroke-width="12"
                        stroke-dasharray="565.48"
                        stroke-dashoffset={565.48 *
                            (1 -
                                Math.min(
                                    vitals.movement.steps /
                                        vitals.movement.goal,
                                    1,
                                ))}
                        stroke-linecap="round"
                        style="filter: url(#glow);"
                        class="transition-all duration-[2000ms] ease-out"
                    />

                    <!-- Energy Flow (Inner) -->
                    <circle
                        cx="120"
                        cy="120"
                        r="70"
                        fill="none"
                        stroke="rgba(255,255,255,0.1)"
                        stroke-width="2"
                        stroke-dasharray="2 6"
                    />
                    <circle
                        cx="120"
                        cy="120"
                        r="70"
                        fill="none"
                        stroke={getEnergyColor(vitals.energy.level)}
                        stroke-width="6"
                        stroke-dasharray="439.8"
                        stroke-dashoffset={439.8 *
                            (1 - vitals.energy.score / 100)}
                        stroke-linecap="round"
                        class="transition-all duration-[1500ms] ease-out"
                    />

                    <!-- Core Pulse -->
                    <circle
                        cx="120"
                        cy="120"
                        r="12"
                        fill={getEnergyColor(vitals.energy.level)}
                        class="pulse-core shadow-lg"
                    />
                </svg>

                <!-- Center Readout -->
                <div
                    class="absolute inset-0 flex flex-col items-center justify-center text-center"
                >
                    <div
                        class="flex items-baseline gap-1"
                        in:fly={{ y: 10, duration: 800 }}
                    >
                        <span
                            class="text-4xl font-black text-white tracking-tighter"
                        >
                            {vitals.energy.score}
                        </span>
                        <span class="text-[10px] font-bold text-white/40"
                            >%</span
                        >
                    </div>
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-[0.3em]"
                        >Resonance</span
                    >
                </div>
            </div>
        </div>

        <!-- Metric Grid -->
        <div class="grid grid-cols-2 gap-4 mt-6">
            <div
                class="metric-card group p-4 rounded-3xl bg-white/5 border border-white/5 hover:bg-white/[0.08] hover:border-white/10 transition-all duration-300"
            >
                <div class="flex items-center gap-2 mb-3">
                    <div class="p-2 rounded-xl bg-cyan-400/10 text-cyan-400">
                        <Footprints size={14} />
                    </div>
                    <span
                        class="text-[9px] font-black text-white/30 uppercase tracking-widest"
                        >Movement</span
                    >
                </div>
                <div class="flex flex-col">
                    <span class="text-xl font-black text-white"
                        >{vitals.movement.steps.toLocaleString()}</span
                    >
                    <div class="flex items-center gap-1.5 mt-1">
                        <div
                            class="h-1 flex-1 bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="h-full bg-cyan-400/40"
                                style="width: {Math.min(
                                    (vitals.movement.steps /
                                        vitals.movement.goal) *
                                        100,
                                    100,
                                )}%"
                            ></div>
                        </div>
                        <span class="text-[8px] font-bold text-white/20 italic"
                            >TARGET</span
                        >
                    </div>
                </div>
            </div>

            <div
                class="metric-card group p-4 rounded-3xl bg-white/5 border border-white/5 hover:bg-white/[0.08] hover:border-white/10 transition-all duration-300"
            >
                <div class="flex items-center gap-2 mb-3">
                    <div
                        class="p-2 rounded-xl bg-purple-400/10 text-purple-400"
                    >
                        <Moon size={14} />
                    </div>
                    <span
                        class="text-[9px] font-black text-white/30 uppercase tracking-widest"
                        >Rest</span
                    >
                </div>
                <div class="flex flex-col">
                    <span class="text-xl font-black text-white"
                        >{vitals.sleep.duration}</span
                    >
                    <div class="flex items-center gap-1 mt-1">
                        <span
                            class="text-[8px] font-bold text-purple-400/60 uppercase"
                            >{vitals.sleep.quality}</span
                        >
                        <div class="w-1 h-1 rounded-full bg-white/20"></div>
                        <span class="text-[8px] font-bold text-white/20 italic"
                            >EFFICIENCY 94%</span
                        >
                    </div>
                </div>
            </div>
        </div>

        <button
            class="mt-6 w-full py-3 rounded-2xl bg-white/5 border border-white/5 text-[9px] font-black text-white/40 uppercase tracking-[0.2em] hover:bg-white/10 hover:text-white/80 transition-all flex items-center justify-center gap-2"
        >
            <Info size={12} />
            View_Full_Diagnostic
        </button>
    {/if}
</div>

<style>
    .premium-loader {
        width: 40px;
        height: 40px;
        border: 2px solid rgba(255, 255, 255, 0.05);
        border-top-color: rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .pulse-core {
        animation: core-glow 2s ease-in-out infinite;
    }

    @keyframes core-glow {
        0%,
        100% {
            transform: scale(1);
            opacity: 0.8;
            filter: blur(2px);
        }
        50% {
            transform: scale(1.3);
            opacity: 0.4;
            filter: blur(8px);
        }
    }

    .somatic-rhythm {
        font-family: "Outfit", sans-serif;
    }

    .metric-card {
        cursor: pointer;
    }
</style>
