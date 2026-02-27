<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import { icpService } from "$lib/services/icp-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Layers,
        Zap,
        RefreshCcw,
        Database,
        Lock,
        Dna,
    } from "lucide-svelte";

    let isMutating = $state(false);
    let selectedShard = $state("CORE_MANIFOLD");
    let mutationStatus = $state<string | null>(null);
    let icp = icpService.state;

    // Derived permission check
    let isOverseer = $derived(
        manifold.permissionLevel === "SOVEREIGN_OVERSEER",
    );

    async function triggerMutation() {
        if (!isOverseer || !icp.isAuthenticated) return;

        isMutating = true;
        mutationStatus = "Initiating_Quantum_Drift...";

        try {
            // Snapshot current state for mutation
            const layout = JSON.stringify(manifold.kernelState);
            const activeModules = [
                "icp_console",
                "biovault",
                "resonance_cortex",
            ];

            const res = await icpService.mutateMesh(
                layout,
                "QUANTUM_DARK",
                activeModules,
            );

            if ("ok" in res) {
                mutationStatus = "Mutation_Sealed_on_Chain";
                manifold.recordEvent(
                    "SHARD_MUTATION_COMPLETE",
                    `Shard ${selectedShard} mutated and synced to Mesh Registry.`,
                );

                // Visual feedback
                manifold.visualFX.glitchActive = true;
                setTimeout(
                    () => (manifold.visualFX.glitchActive = false),
                    1500,
                );
            } else {
                mutationStatus = "Mutation_Failed: " + (res as { err?: string }).err;
            }
        } catch (e) {
            mutationStatus = "Communication_Anomaly";
        } finally {
            isMutating = false;
            setTimeout(() => (mutationStatus = null), 3000);
        }
    }

    const shards = [
        { id: "CORE_MANIFOLD", label: "Core Manifold", risk: "LOW" },
        { id: "BIO_VAULT_SHARD", label: "Bio-Vault Shard", risk: "MEDIUM" },
        { id: "GOVERNANCE_ROOT", label: "Governance Root", risk: "CRITICAL" },
    ];
</script>

<div class="shard-mutation-panel glass-panel p-6" in:fade>
    <div class="flex items-center gap-3 mb-6">
        <div
            class="p-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400"
        >
            <Layers size={18} />
        </div>
        <div>
            <h3
                class="text-[8px] font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Cosmic Engineering
            </h3>
            <h2
                class="text-xl font-black text-white uppercase tracking-tighter"
            >
                Shard Mutation
            </h2>
        </div>
    </div>

    {#if !isOverseer}
        <div class="py-12 flex flex-col items-center text-center gap-4">
            <div
                class="w-16 h-16 rounded-full bg-rose-500/5 flex items-center justify-center text-rose-500/20"
            >
                <Lock size={32} />
            </div>
            <div>
                <p
                    class="text-[10px] font-bold text-rose-400 uppercase tracking-widest"
                >
                    Overseer Required
                </p>
                <p class="text-[8px] text-white/20 mt-1 leading-relaxed">
                    Autonomous Shard Mutation requires **SOVEREIGN_OVERSEER**
                    resonance level (95%+).
                </p>
            </div>
        </div>
    {:else}
        <div class="space-y-6">
            <!-- Shard Selection -->
            <div class="grid grid-cols-1 gap-2">
                {#each shards as shard}
                    <button
                        onclick={() => (selectedShard = shard.id)}
                        class="p-3 rounded-xl border transition-all flex items-center justify-between {selectedShard ===
                        shard.id
                            ? 'bg-rose-500/10 border-rose-500/40'
                            : 'bg-white/[0.02] border-white/5 hover:border-white/10'}"
                    >
                        <div class="flex items-center gap-3">
                            <Dna
                                size={14}
                                class={selectedShard === shard.id
                                    ? "text-rose-400"
                                    : "text-white/20"}
                            />
                            <span
                                class="text-[10px] font-black uppercase {selectedShard ===
                                shard.id
                                    ? 'text-white'
                                    : 'text-white/40'}">{shard.label}</span
                            >
                        </div>
                        <span
                            class="text-[7px] font-mono {shard.risk ===
                            'CRITICAL'
                                ? 'text-rose-500'
                                : 'text-white/20'}">[{shard.risk}]</span
                        >
                    </button>
                {/each}
            </div>

            <!-- Mutation Trigger -->
            <div class="space-y-3 pt-4 border-t border-white/5">
                <div
                    class="flex justify-between items-center text-[8px] font-black uppercase tracking-widest text-white/20"
                >
                    <span>Active_Identity</span>
                    <span class="text-cyan-400"
                        >{icp.principal?.slice(0, 8)}...</span
                    >
                </div>

                <button
                    onclick={triggerMutation}
                    disabled={isMutating}
                    class="w-full py-4 bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] transition-all flex items-center justify-center gap-2 shadow-[0_0_30px_rgba(225,29,72,0.3)] disabled:opacity-50"
                >
                    {#if isMutating}
                        <RefreshCcw size={14} class="animate-spin" />
                        Transmuting_Matter...
                    {:else}
                        <Zap size={14} />
                        Trigger Shard Mutation
                    {/if}
                </button>

                {#if mutationStatus}
                    <p
                        class="text-[8px] text-center font-mono text-rose-400 animate-pulse uppercase"
                        transition:slide
                    >
                        {mutationStatus}
                    </p>
                {/if}
            </div>

            <!-- Mesh Status Footer -->
            <div
                class="p-4 bg-black/40 rounded-2xl border border-white/5 space-y-3"
            >
                <div class="flex items-center gap-2">
                    <Database size={12} class="text-emerald-400" />
                    <span
                        class="text-[8px] font-black uppercase text-emerald-400 tracking-widest"
                        >Mesh_Registry_Online</span
                    >
                </div>
                <div
                    class="grid grid-cols-2 gap-2 text-[7px] font-mono text-white/30 uppercase"
                >
                    <div>Nodes: 14</div>
                    <div class="text-right">Sync: 12ms</div>
                </div>
                <p class="text-[7px] text-white/20 italic leading-relaxed">
                    * Shard mutations are permanent and replicated across the
                    Sovereign Mesh via decentralized ICP state.
                </p>
            </div>
        </div>
    {/if}
</div>

<style>
    .shard-mutation-panel {
        background: linear-gradient(
            135deg,
            rgba(225, 29, 72, 0.05) 0%,
            rgba(15, 23, 42, 0.4) 100%
        );
    }
</style>
