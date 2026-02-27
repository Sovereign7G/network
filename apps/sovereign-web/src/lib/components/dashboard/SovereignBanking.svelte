<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { api } from "$lib/services/api";

    let bonds: any[] = $state([]);
    let credit: any = $state(null);
    let isLoading = $state(true);
    let activeTab = $state("credit");

    onMount(async () => {
        try {
            const [bondsData, creditData] = await Promise.all([
                api.request("/banking/bonds"),
                api.request("/banking/credit"),
            ]);
            bonds = bondsData;
            credit = creditData;
        } catch (error) {
            console.error("Failed to load banking data", error);
        } finally {
            isLoading = false;
        }
    });

    function getStatusColor(status: string) {
        switch (status) {
            case "CORE":
                return "text-cyan-400";
            case "STABLE":
                return "text-emerald-400";
            case "VENTURE":
                return "text-amber-400";
            default:
                return "text-white/40";
        }
    }
</script>

<div class="sovereign-banking glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-center mb-6">
        <h3 class="text-xs font-black uppercase tracking-[0.3em] text-white/40">
            Sovereign Banking
        </h3>
        <div class="flex bg-white/5 p-1 rounded-lg">
            <button
                onclick={() => (activeTab = "credit")}
                class="px-3 py-1 text-[8px] font-black uppercase tracking-widest rounded-md transition-all {activeTab ===
                'credit'
                    ? 'bg-white text-black'
                    : 'text-white/40 hover:text-white'}">Credit</button
            >
            <button
                onclick={() => (activeTab = "bonds")}
                class="px-3 py-1 text-[8px] font-black uppercase tracking-widest rounded-md transition-all {activeTab ===
                'bonds'
                    ? 'bg-white text-black'
                    : 'text-white/40 hover:text-white'}">Bonds</button
            >
        </div>
    </div>

    {#if isLoading}
        <div class="flex-1 flex items-center justify-center">
            <div class="banking-loader"></div>
        </div>
    {:else if activeTab === "credit"}
        <div class="flex-1 space-y-6" in:fade>
            <div
                class="credit-card bg-gradient-to-br from-white/10 to-transparent border border-white/10 p-6 rounded-3xl relative overflow-hidden group"
            >
                <div
                    class="absolute -right-10 -top-10 w-40 h-40 bg-white/5 rounded-full blur-3xl group-hover:bg-cyan-400/5 transition-all"
                ></div>

                <div class="flex justify-between items-start relative z-10">
                    <div>
                        <span
                            class="text-[8px] font-black uppercase tracking-widest text-white/40 block mb-1"
                            >Reputation-Linked Credit</span
                        >
                        <span class="text-2xl font-black text-white"
                            >{credit.limit.toLocaleString()}
                            {credit.currency}</span
                        >
                    </div>
                    <span
                        class="text-[10px] font-black text-emerald-400 bg-emerald-400/5 px-2 py-1 rounded"
                        >{(credit.reputation_factor * 100).toFixed(0)}% Rep</span
                    >
                </div>

                <div class="mt-8 relative z-10">
                    <div
                        class="flex justify-between text-[8px] font-black uppercase text-white/20 mb-2"
                    >
                        <span>Utilization</span>
                        <span
                            >{(
                                (credit.utilization / credit.limit) *
                                100
                            ).toFixed(0)}%</span
                        >
                    </div>
                    <div class="h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div
                            class="h-full bg-cyan-400"
                            style="width: {(credit.utilization / credit.limit) *
                                100}%"
                        ></div>
                    </div>
                </div>

                <div class="mt-8 flex justify-between items-end relative z-10">
                    <div class="flex flex-col">
                        <span
                            class="text-[7px] font-black uppercase text-white/20"
                            >Next Repayment</span
                        >
                        <span class="text-[10px] font-bold text-white/60"
                            >{new Date(
                                credit.next_repayment,
                            ).toLocaleDateString()}</span
                        >
                    </div>
                    <button
                        class="px-4 py-2 bg-white text-black text-[9px] font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-all"
                        >Draw Funds</button
                    >
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="p-3 rounded-2xl bg-white/5 border border-white/5">
                    <span
                        class="text-[7px] font-black uppercase text-white/20 block mb-1"
                        >APY (Variable)</span
                    >
                    <span class="text-sm font-black text-cyan-400">4.2%</span>
                </div>
                <div class="p-3 rounded-2xl bg-white/5 border border-white/5">
                    <span
                        class="text-[7px] font-black uppercase text-white/20 block mb-1"
                        >Collateral</span
                    >
                    <span class="text-sm font-black text-white">MERITS</span>
                </div>
            </div>
        </div>
    {:else}
        <div
            class="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar"
            in:fade
        >
            {#each bonds as bond}
                <div
                    class="bond-item bg-white/5 border border-white/5 p-4 rounded-2xl group hover:border-white/20 transition-all"
                >
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <h4
                                class="text-[10px] font-black text-white group-hover:text-cyan-400 transition-colors uppercase"
                            >
                                {bond.type.replace("_", " ")}
                            </h4>
                            <span class="text-[8px] font-mono text-white/20"
                                >{bond.id}</span
                            >
                        </div>
                        <span class="text-xs font-black text-emerald-400"
                            >+{bond.yield}%</span
                        >
                    </div>
                    <div
                        class="flex justify-between items-center mt-3 pt-3 border-t border-white/5"
                    >
                        <span
                            class="text-[8px] font-black uppercase {getStatusColor(
                                bond.status,
                            )}">{bond.status}</span
                        >
                        <span class="text-[8px] text-white/20 uppercase"
                            >Matures {bond.maturation}</span
                        >
                    </div>
                </div>
            {/each}
        </div>

        <button
            class="mt-4 w-full py-3 bg-cyan-400/10 border border-cyan-400/20 rounded-xl text-[9px] font-black uppercase tracking-widest text-cyan-400 hover:bg-cyan-400 hover:text-black transition-all"
        >
            Access Primary Market
        </button>
    {/if}
</div>

<style>
    .banking-loader {
        width: 32px;
        height: 32px;
        border: 2px solid rgba(34, 211, 238, 0.1);
        border-top-color: #22d3ee;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 2px;
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
