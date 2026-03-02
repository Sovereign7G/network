<script lang="ts">
    // @ts-nocheck
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import WorkspaceCanvas from "$lib/components/blocks/WorkspaceCanvas.svelte";
    import ProtocolGlyph from "$lib/components/dashboard/ProtocolGlyph.svelte";
    import ResonanceMonitor from "$lib/components/telemetry/ResonanceMonitor.svelte";
    import IntentStage from "$lib/components/economics/IntentStage.svelte";
    import { designEngineering } from "$lib/services/design-engineering-engine.svelte";
    import { Activity } from "lucide-svelte";

    // Manifold State
    const manifold = $state({
        isPoeticMode: true,
    });

    const initialColumns = [
        {
            id: "col-1",
            blocks: [
                {
                    id: "block-1",
                    type: "tile",
                    content: {
                        title: "Vault Balance",
                        value: "1,247.32",
                        symbol: "AGE",
                        type: "wallet",
                    },
                },
                {
                    id: "block-2",
                    type: "tile",
                    content: {
                        title: "Network Resonance",
                        value: "98.2",
                        symbol: "%",
                        type: "atlas",
                    },
                },
            ],
        },
        {
            id: "col-2",
            blocks: [
                {
                    id: "block-3",
                    type: "tile",
                    content: {
                        title: "Active Nodes",
                        value: "4,092",
                        symbol: "NODES",
                        type: "node",
                    },
                },
                {
                    id: "block-connect",
                    type: "connectivity",
                    content: {},
                },
            ],
        },
    ];

    let workspaceColumns = $state(initialColumns);
    let isLoading = $state(true);

    onMount(() => {
        setTimeout(() => {
            isLoading = false;
        }, 600);
    });

    function addNewBlock({ columnIndex }: { columnIndex: number }) {
        const newBlock = {
            id: `block-${Date.now()}`,
            type: "tile",
            content: {
                title: "New Metric",
                value: "0.00",
                symbol: "UNIT",
                type: "overview",
            },
        };
        workspaceColumns[columnIndex].blocks = [
            ...workspaceColumns[columnIndex].blocks,
            newBlock,
        ];
    }
</script>

<div class="dashboard-page h-full w-full">
    {#if isLoading}
        <div class="h-full flex flex-col items-center justify-center" out:fade>
            <div class="w-16 h-16 relative">
                <div
                    class="absolute inset-0 border-2 border-cyan-500/20 rounded-full"
                ></div>
                <div
                    class="absolute inset-0 border-2 border-t-cyan-500 rounded-full animate-spin"
                ></div>
            </div>
            <p class="text-label mt-8 animate-pulse">Syncing Manifold...</p>
        </div>
    {:else}
        <div in:fade={{ duration: 800 }} class="space-y-12">
            <!-- Header Section -->
            <header class="flex items-end justify-between">
                <div>
                    <h1 class="text-4xl text-premium">Sovereign Command</h1>
                    <p class="text-label !opacity-40 mt-2">
                        Personal Node Infrastructure & Assets
                    </p>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex flex-col items-end">
                        <span
                            class="text-[10px] font-black opacity-20 uppercase tracking-widest"
                            >Latency</span
                        >
                        <span class="text-sm font-mono text-emerald-400"
                            >12ms</span
                        >
                    </div>
                </div>
            </header>

            <!-- Workspace Section -->
            <WorkspaceCanvas
                bind:columns={workspaceColumns}
                tile={tileSnippet}
                onAddBlock={addNewBlock}
            />

            <!-- RESONANCE & INTENT ORCHESTRATION -->
            <div
                class="resonance-orchestrator grid grid-cols-1 xl:grid-cols-5 gap-10 mt-20 pb-40"
            >
                <div class="xl:col-span-2">
                    <ResonanceMonitor />
                </div>
                <div class="xl:col-span-3">
                    <IntentStage />
                </div>
            </div>
        </div>

        <!-- 🧪 STRESS CONTROLLER (DE-Sim) -->
        <div class="fixed bottom-8 right-8 z-[1000]">
            <div
                class="chiaroscuro-card p-6 border-white/10 backdrop-blur-2xl w-64 space-y-4 shadow-2xl"
            >
                <div class="flex items-center gap-3">
                    <Activity size={16} class="text-cyan-400" />
                    <span class="text-label text-[10px]">Stress Manifold</span>
                </div>

                <div class="space-y-2">
                    <div class="flex justify-between text-[10px] font-bold">
                        <span class="opacity-40 uppercase"
                            >{manifold.isPoeticMode
                                ? "HILBERT INDEX"
                                : "SYSTEM HEALTH"}</span
                        >
                        <span class="text-cyan-400"
                            >{Math.round(designEngineering.hilbertIndex)}</span
                        >
                    </div>
                    <input
                        type="range"
                        bind:value={designEngineering.hilbertIndex}
                        min="50"
                        max="100"
                        step="1"
                        class="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                    />
                </div>

                <div class="space-y-2">
                    <div class="flex justify-between text-[10px] font-bold">
                        <span class="opacity-40 uppercase">Moral Merits</span>
                        <span class="text-emerald-400"
                            >{Math.round(designEngineering.moralMerits)}</span
                        >
                    </div>
                    <input
                        type="range"
                        bind:value={designEngineering.moralMerits}
                        min="50"
                        max="100"
                        step="1"
                        class="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    />
                </div>

                <div class="pt-2 border-t border-white/5 flex gap-2">
                    <button
                        class="flex-1 py-1 px-2 rounded bg-white/5 hover:bg-red-500/20 text-[8px] font-black transition-colors"
                        onclick={() => (designEngineering.hilbertIndex = 70)}
                        >EMERGENCY</button
                    >
                    <button
                        class="flex-1 py-1 px-2 rounded bg-white/5 hover:bg-emerald-500/20 text-[8px] font-black transition-colors"
                        onclick={() => {
                            designEngineering.hilbertIndex = 98;
                            designEngineering.moralMerits = 98;
                        }}>GRACE</button
                    >
                </div>
            </div>
        </div>
    {/if}
</div>

{#snippet tileSnippet(content: any)}
    <div
        class="chiaroscuro-card p-8 h-full min-h-[220px] flex flex-col justify-between group overflow-hidden relative"
    >
        <!-- Decoration -->
        <div
            class="absolute -right-4 -top-4 w-32 h-32 bg-cyan-500/5 blur-3xl rounded-full group-hover:bg-cyan-500/10 transition-all duration-700"
        ></div>

        <div class="flex items-start justify-between relative z-10">
            <div class="space-y-4">
                <div class="text-label !opacity-60">{content.title}</div>
                <div class="flex items-baseline gap-2">
                    <span
                        class="text-5xl text-premium transition-all group-hover:tracking-tight"
                        >{content.value}</span
                    >
                    <span
                        class="text-[10px] font-black opacity-30 tracking-tighter"
                        >{content.symbol}</span
                    >
                </div>
            </div>
            <div
                class="p-4 rounded-2xl bg-white/5 border border-white/5 group-hover:border-cyan-500/30 transition-all duration-500"
            >
                <ProtocolGlyph type={content.type} size={24} active />
            </div>
        </div>

        <div class="flex items-center gap-6 relative z-10">
            <div
                class="flex-1 h-px bg-white/5 group-hover:bg-white/10 transition-colors"
            ></div>
            <div class="flex items-center gap-2">
                <div
                    class="w-1.5 h-1.5 rounded-full bg-emerald-400 glow-emerald"
                ></div>
                <span class="text-[8px] font-black opacity-30 tracking-[0.2em]"
                    >OPERATIONAL</span
                >
            </div>
        </div>
    </div>
{/snippet}

<style>
    .dashboard-page {
        overflow-y: auto;
        padding-bottom: 200px;
    }

    .glow-emerald {
        box-shadow: 0 0 10px #10b981;
    }
</style>
