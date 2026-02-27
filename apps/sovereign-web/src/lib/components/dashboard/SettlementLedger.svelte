<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { api } from "$lib/services/api";

    let settlements: any[] = $state([]);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            settlements = await api.request("/payments/settlements");
        } catch (error) {
            console.error("Failed to load settlements", error);
        } finally {
            isLoading = false;
        }
    });

    function formatRelativeTime(ts: number) {
        const diff = Date.now() - ts;
        if (diff < 3600000) return "Recent";
        if (diff < 86400000) return "Today";
        return "Previous";
    }
</script>

<div class="settlement-ledger glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-center mb-6">
        <h3 class="text-xs font-black uppercase tracking-[0.3em] text-white/40">
            Settlement Ledger
        </h3>
        <span
            class="text-[8px] font-black uppercase text-cyan-400 bg-cyan-400/5 px-2 py-1 rounded"
            >Institutional Rail</span
        >
    </div>

    {#if isLoading}
        <div class="flex-1 flex flex-col items-center justify-center space-y-4">
            <div class="loading-bar-container">
                <div class="loading-bar-fill"></div>
            </div>
            <span
                class="text-[8px] font-black uppercase tracking-widest text-white/20"
                >Querying Ledger...</span
            >
        </div>
    {:else}
        <div class="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar">
            {#each settlements as txn (txn.id)}
                <div
                    class="txn-card bg-white/5 border border-white/5 p-4 rounded-2xl hover:bg-white/10 transition-all group"
                >
                    <div class="flex justify-between items-start mb-2">
                        <div class="flex flex-col">
                            <span
                                class="text-[10px] font-black text-white group-hover:text-cyan-400 transition-colors"
                                >{txn.merchant}</span
                            >
                            <span
                                class="text-[8px] font-mono text-white/20 uppercase"
                                >{txn.id}</span
                            >
                        </div>
                        <div class="flex flex-col items-end">
                            <span class="text-sm font-black text-white"
                                >{txn.amount} {txn.currency}</span
                            >
                            <span
                                class="text-[8px] font-black uppercase tracking-tighter {txn.status ===
                                'SETTLED'
                                    ? 'text-emerald-400'
                                    : 'text-amber-400'}"
                            >
                                {txn.status}
                            </span>
                        </div>
                    </div>
                    <div
                        class="flex justify-between items-center mt-2 pt-2 border-t border-white/5"
                    >
                        <span
                            class="text-[8px] text-white/30 uppercase tracking-widest"
                            >{formatRelativeTime(txn.timestamp)}</span
                        >
                        <div class="flex gap-1">
                            <div
                                class="w-1 h-1 rounded-full bg-cyan-400/30"
                            ></div>
                            <div
                                class="w-1 h-1 rounded-full bg-cyan-400/30"
                            ></div>
                            <div
                                class="w-1 h-1 rounded-full bg-cyan-400/30"
                            ></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <button
            class="mt-4 w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-[0.2em] text-white/40 transition-all"
        >
            Audit Full History
        </button>
    {/if}
</div>

<style>
    .loading-bar-container {
        width: 100px;
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1px;
        overflow: hidden;
    }

    .loading-bar-fill {
        height: 100%;
        width: 30%;
        background: #22d3ee;
        animation: loading-move 1s infinite linear;
    }

    @keyframes loading-move {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(333%);
        }
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 2px;
    }

    .custom-scrollbar::-webkit-scrollbar-track {
        background: transparent;
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
