<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import { Layers, Eye, Move3d, Target, Activity } from "lucide-svelte";
    import { onMount } from "svelte";

    let mouseX = $state(0);
    let mouseY = $state(0);

    function handleMouseMove(e: MouseEvent) {
        if (!manifold.isSpatialMode) return;
        mouseX = (e.clientX / window.innerWidth - 0.5) * 40;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 40;
    }

    onMount(() => {
        window.addEventListener("mousemove", handleMouseMove);
        return () => window.removeEventListener("mousemove", handleMouseMove);
    });

    const anchors = [
        {
            id: "a1",
            label: "Nodes_Nagano",
            icon: Target,
            top: "15%",
            left: "10%",
        },
        {
            id: "a2",
            label: "Causal_Anchor",
            icon: Move3d,
            top: "75%",
            left: "85%",
        },
        {
            id: "a3",
            label: "Resonance_Point",
            icon: Activity,
            top: "20%",
            left: "90%",
        },
        {
            id: "a4",
            label: "Identity_Link",
            icon: Eye,
            top: "80%",
            left: "15%",
        },
    ];
</script>

{#if manifold.isSpatialMode}
    <div
        class="fixed inset-0 z-[100] pointer-events-none overflow-hidden"
        transitionfade={{ duration: 1000 }}
    >
        <!-- Volumetric Background Distortion -->
        <div class="absolute inset-0 bg-zinc-950/20 backdrop-blur-[2px]"></div>

        <!-- Eye-Tracking Glow (Focus Simulation) -->
        <div
            class="absolute w-[600px] h-[600px] bg-purple-500/10 rounded-full blur-[120px] mix-blend-screen transition-all duration-300 ease-out"
            style="left: calc({mouseX * 1.5}px + 50%); top: calc({mouseY *
                1.5}px + 50%); transform: translate(-50%, -50%);"
        ></div>

        <!-- Perspective Grid -->
        <div
            class="absolute inset-0 opacity-20 perspective-grid"
            style="transform: rotateX(60deg) translateY({mouseY *
                0.5}px) translateX({mouseX * 0.5}px);"
        ></div>

        <!-- Floating Spatial Anchors (AR HUD Elements) -->
        {#each anchors as anchor}
            <div
                class="absolute flex flex-col items-center gap-2 transition-all duration-700 ease-out"
                style="top: {anchor.top}; left: {anchor.left}; transform: translate({mouseX *
                    0.8}px, {mouseY * 0.8}px);"
            >
                <div
                    class="w-12 h-12 rounded-full bg-white/5 border border-white/10 flex items-center justify-center backdrop-blur-3xl shadow-2xl relative group"
                >
                    <div
                        class="absolute inset-0 rounded-full bg-cyan-400/20 animate-pulse"
                    ></div>
                    <anchor.icon
                        size={18}
                        class="text-cyan-400 relative z-10"
                    />
                </div>
                <span
                    class="text-[8px] font-black text-white/40 uppercase tracking-[0.3em] font-mono"
                >
                    {anchor.label}
                </span>
            </div>
        {/each}

        <!-- Spatial Interaction Hints -->
        <div
            class="absolute bottom-12 left-1/2 -translate-x-1/2 flex items-center gap-8"
        >
            <div class="flex items-center gap-3">
                <div
                    class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center"
                >
                    <span class="text-[10px] text-white/40 font-black italic"
                        >捏</span
                    >
                </div>
                <span
                    class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                    >Pinch to zoom protocol</span
                >
            </div>
            <div class="flex items-center gap-3">
                <div
                    class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center"
                >
                    <span class="text-[10px] text-white/40 font-black italic"
                        >视</span
                    >
                </div>
                <span
                    class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                    >Look to select module</span
                >
            </div>
        </div>

        <!-- System Latency Indicator -->
        <div
            class="absolute top-12 left-1/2 -translate-x-1/2 px-4 py-1.5 bg-black/40 rounded-full border border-white/5 flex items-center gap-3"
        >
            <Layers size={12} class="text-purple-400" />
            <span
                class="text-[9px] font-black text-white/60 uppercase tracking-widest"
                >Spatial_Resolution: 4K Native</span
            >
            <div class="w-1 h-3 bg-white/10 rounded-full overflow-hidden">
                <div class="h-full bg-purple-400 w-2/3"></div>
            </div>
        </div>
    </div>
{/if}

<style>
    .perspective-grid {
        background-image: linear-gradient(
                rgba(255, 255, 255, 0.05) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.05) 1px,
                transparent 1px
            );
        background-size: 100px 100px;
        z-index: -1;
    }

    /* Global spatial distortion for the underlying dashboard when active */
    :global(.dashboard-spatial-mode) {
        perspective: 2000px;
    }

    :global(.dashboard-spatial-mode .dashboard-container) {
        transform: rotateX(2deg) rotateY(var(--spatial-ry, 0deg));
        transition: transform 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
</style>
