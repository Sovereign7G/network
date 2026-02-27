<script lang="ts">
    import { fade } from "svelte/transition";
    import { icpService } from "$lib/services/icp-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { Gavel, Send, ShieldAlert, RefreshCcw } from "lucide-svelte";

    let proposalText = $state("");
    let isSubmitting = $state(false);
    let proposals = $state<any[]>([]);
    let isLoadingProposals = $state(false);
    let icp = icpService.state;

    async function loadProposals() {
        if (!icp.isAuthenticated) return;
        isLoadingProposals = true;
        try {
            const res = await icpService.getProposals();
            proposals = res;
        } catch (e) {
            console.error("Failed to load proposals", e);
        } finally {
            isLoadingProposals = false;
        }
    }

    async function submitProposal() {
        if (!proposalText || !icp.isAuthenticated) return;
        isSubmitting = true;
        try {
            const res = await icpService.proposeCrossChainAction(proposalText);
            if ("Ok" in res) {
                manifold.recordEvent(
                    "ICP_PROPOSAL_CREATED",
                    `Proposal Manifest: ${proposalText}`,
                );
                proposalText = "";
                await loadProposals();
            }
        } catch (e) {
            console.error(e);
        } finally {
            isSubmitting = false;
        }
    }

    async function approveProposal(id: string) {
        if (!icp.isAuthenticated) return;
        try {
            const res = await icpService.approveProposal(id, true);
            if ("Ok" in res) {
                manifold.recordEvent(
                    "GOV_PROPOSAL_APPROVED",
                    `Multi-sig authorization anchored for ${id}`,
                );
                await loadProposals();
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function executeProposal(id: string) {
        if (!icp.isAuthenticated) return;
        try {
            const res = await icpService.executeProposal(id);
            if ("Ok" in res) {
                manifold.recordEvent(
                    "GOV_PROPOSAL_EXECUTED",
                    `Timelock released. Proposal ${id} manifested in law.`,
                );
                await loadProposals();
            }
        } catch (e) {
            console.error(e);
        }
    }

    $effect(() => {
        if (icp.isAuthenticated) {
            loadProposals();
            const interval = setInterval(loadProposals, 10000);
            return () => clearInterval(interval);
        }
        return () => {};
    });

    function getStatusColor(status: any) {
        if (status.Passed !== undefined) return "text-emerald-400";
        if (status.Open !== undefined) return "text-amber-400";
        if (status.Executed !== undefined) return "text-cyan-400";
        return "text-rose-400";
    }

    function getStatusLabel(status: any) {
        return Object.keys(status)[0].toUpperCase();
    }
</script>

<div class="gov-bridge-panel glass-panel p-6" in:fade>
    <div class="flex items-center gap-3 mb-6">
        <div
            class="p-2 rounded-lg bg-indigo-500/20 border border-indigo-500/40 text-indigo-400"
        >
            <Gavel size={18} />
        </div>
        <div>
            <h3
                class="text-[8px] font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Institutional Bridge
            </h3>
            <h2
                class="text-xl font-black text-white uppercase tracking-tighter"
            >
                Governance Bridge
            </h2>
        </div>
    </div>

    <div class="space-y-6">
        <!-- New Proposal -->
        <div class="space-y-3">
            <div class="flex justify-between items-center">
                <span
                    class="text-[10px] font-black uppercase tracking-widest text-white/60"
                    >Propose_Action</span
                >
                <span class="text-[7px] font-black text-white/20"
                    >AAL3_REQUIRED</span
                >
            </div>
            <textarea
                bind:value={proposalText}
                placeholder="MANIFEST A NEW INSTITUTIONAL ACTION..."
                class="w-full h-24 bg-black/40 border border-white/10 rounded-2xl p-4 text-[10px] font-mono text-indigo-300 placeholder:text-white/10 outline-none focus:border-indigo-500/50 transition-all resize-none"
            ></textarea>
            <button
                onclick={submitProposal}
                disabled={isSubmitting || !icpService.state.isAuthenticated}
                class="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] transition-all flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(79,70,229,0.3)] disabled:opacity-30 disabled:grayscale"
            >
                <Send size={14} />
                {isSubmitting
                    ? "Transmitting_Action..."
                    : "Relay to Governance Canister"}
            </button>
            {#if !icpService.state.isAuthenticated}
                <p
                    class="text-[7px] text-center text-rose-400 font-black uppercase tracking-tighter italic"
                >
                    Identity required for on-chain proposal manifest
                </p>
            {/if}
        </div>

        <!-- Active Proposals -->
        <div class="space-y-3">
            <div class="flex justify-between items-center">
                <span
                    class="text-[8px] font-black uppercase text-white/20 tracking-widest"
                    >Active_Proposals</span
                >
                {#if isLoadingProposals}
                    <RefreshCcw
                        size={10}
                        class="text-indigo-400 animate-spin"
                    />
                {/if}
            </div>
            <div class="space-y-2">
                {#if proposals.length === 0}
                    <p
                        class="text-[8px] text-white/10 italic py-4 text-center border border-white/5 rounded-2xl"
                    >
                        No active proposals in the policy engine.
                    </p>
                {/if}
                {#each proposals as prop}
                    <div
                        class="p-4 bg-white/[0.02] border border-white/5 rounded-2xl space-y-3 group"
                    >
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <span class="text-[9px] font-mono text-white/20"
                                    >{prop.id.slice(0, 6)}</span
                                >
                                <span
                                    class="text-[10px] text-white/60 font-medium group-hover:text-white transition-colors"
                                >
                                    {prop.action}
                                </span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span
                                    class="text-[8px] font-black {getStatusColor(
                                        prop.status,
                                    )} uppercase"
                                >
                                    {getStatusLabel(prop.status)}
                                </span>
                            </div>
                        </div>

                        <!-- Interaction Bar -->
                        <div class="flex gap-2 pt-2 border-t border-white/5">
                            {#if prop.status.Open !== undefined}
                                <button
                                    onclick={() => approveProposal(prop.id)}
                                    class="flex-1 py-2 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 rounded-lg text-[7px] font-black uppercase text-indigo-400 transition-all"
                                >
                                    Approve_Multisig
                                </button>
                            {:else if prop.status.Passed !== undefined}
                                <button
                                    onclick={() => executeProposal(prop.id)}
                                    class="flex-1 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 rounded-lg text-[7px] font-black uppercase text-emerald-400 transition-all"
                                >
                                    Release_Timelock
                                </button>
                            {/if}
                            <div
                                class="px-3 bg-white/5 rounded-lg flex items-center gap-2"
                            >
                                <span class="text-[7px] font-mono text-white/40"
                                    >Y:{Number(prop.votes_yes)} N:{Number(
                                        prop.votes_no,
                                    )}</span
                                >
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Logic Note -->
        <div
            class="p-3 bg-indigo-500/5 border border-indigo-500/10 rounded-xl flex gap-3"
        >
            <ShieldAlert size={16} class="text-indigo-400 shrink-0" />
            <p class="text-[8px] text-white/40 leading-relaxed font-medium">
                This bridge uses **BLS Threshold Signatures** to verify
                cross-chain commands between the EVM Registry and the ICP Policy
                Engine.
            </p>
        </div>
    </div>
</div>

<style>
    .gov-bridge-panel {
        background: linear-gradient(
            135deg,
            rgba(79, 70, 229, 0.05) 0%,
            rgba(15, 23, 42, 0.4) 100%
        );
    }
</style>
