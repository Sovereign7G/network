<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { slide } from "svelte/transition";
    import { api } from "$lib/services/api";
    import { RefreshCw, Clock, ArrowRightLeft, CheckCircle2, AlertCircle } from "lucide-svelte";

    let settlements: any[] = $state([]);
    let isLoading = $state(true);
    let interval: any;

    async function fetchSettlements() {
        try {
            settlements = await api.request("/payments/settlements");
        } catch (error) {
            console.error("Failed to load settlements", error);
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        fetchSettlements();
        interval = setInterval(fetchSettlements, 10000);
    });

    onDestroy(() => {
        if (interval) clearInterval(interval);
    });

    function getStatusColor(status: string) {
        switch (status) {
            case "SETTLED":
                return "text-emerald-400";
            case "PENDING":
                return "text-amber-400";
            case "FAILED":
                return "text-rose-400";
            default:
                return "text-white/40";
        }
    }
</script>

<div
    class="h-full bg-zinc-900/40 rounded-[2.5rem] border border-white/5 backdrop-blur-2xl overflow-hidden p-6 flex flex-col gap-6 shadow-2xl relative"
>
    <!-- Header -->
    <div class="flex items-center justify-between px-2">
        <div class="flex items-center gap-3">
            <ArrowRightLeft size={16} class="text-amber-400" />
            <h3
                class="text-[10px] font-black uppercase tracking-[0.3em] text-white/60"
            >
                Settlement_Stream
            </h3>
        </div>
        <button
            onclick={fetchSettlements}
            class="text-white/20 hover:text-white transition-colors"
        >
            <RefreshCw size={12} class={isLoading ? "animate-spin" : ""} />
        </button>
    </div>

    <!-- Settlement List -->
    <div class="flex-1 overflow-y-auto no-scrollbar space-y-3">
        {#each settlements as tx (tx.id)}
            <div
                in:slide={{ duration: 300 }}
                class="p-4 bg-white/5 rounded-2xl border border-white/5 hover:bg-white/10 transition-all flex items-center justify-between group"
            >
                <div class="flex items-center gap-4">
                    <div
                        class="w-10 h-10 rounded-xl bg-black/40 flex items-center justify-center border border-white/5"
                    >
                        {#if tx.status === "SETTLED"}
                            <CheckCircle2
                                size={18}
                                class="text-emerald-400/60"
                            />
                        {:else if tx.status === "PENDING"}
                            <Clock
                                size={18}
                                class="text-amber-400/60 animate-pulse"
                            />
                        {:else}
                            <AlertCircle size={18} class="text-rose-400/60" />
                        {/if}
                    </div>
                    <div>
                        <div
                            class="text-[11px] font-black text-white uppercase tracking-tighter italic"
                        >
                            {tx.merchant}
                        </div>
                        <div class="flex items-center gap-2">
                            <span
                                class="text-[8px] font-mono text-white/30 uppercase"
                                >{tx.id}</span
                            >
                            <span class="text-[8px] font-mono text-white/20"
                                >•</span
                            >
                            <span
                                class="text-[8px] font-mono text-white/30 uppercase"
                                >{new Date(tx.timestamp).toLocaleTimeString(
                                    [],
                                    { hour: "2-digit", minute: "2-digit" },
                                )}</span
                            >
                        </div>
                    </div>
                </div>

                <div class="text-right">
                    <div class="flex items-center justify-end gap-1">
                        <span class="text-[12px] font-black text-white"
                            >{tx.amount.toFixed(2)}</span
                        >
                        <span
                            class="text-[9px] font-black text-white/40 uppercase"
                            >{tx.currency}</span
                        >
                    </div>
                    <div
                        class="text-[8px] font-black uppercase tracking-widest {getStatusColor(
                            tx.status,
                        )}"
                    >
                        {tx.status}
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <!-- Stats Bar -->
    <div class="grid grid-cols-2 gap-4 mt-auto pt-4 border-t border-white/5">
        <div class="flex flex-col gap-1">
            <span
                class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
                >Total_Volume_24h</span
            >
            <div class="flex items-baseline gap-1">
                <span class="text-sm font-black text-white">12,482</span>
                <span class="text-[8px] font-black text-white/40 uppercase"
                    >RES</span
                >
            </div>
        </div>
        <div class="flex flex-col gap-1 text-right">
            <span
                class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
                >Resonance_Drift</span
            >
            <div class="flex items-baseline justify-end gap-1">
                <span class="text-sm font-black text-emerald-400">+0.42%</span>
            </div>
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
</style>
