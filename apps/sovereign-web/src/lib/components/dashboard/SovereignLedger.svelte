<script lang="ts">
    import {
        Search,
        Filter,
        ChevronDown,
        ArrowUpRight,
        ArrowDownLeft,
        CheckCircle2,
        Clock,
        ShieldCheck,
        Download,
    } from "lucide-svelte";
    import { fade, fly, slide } from "svelte/transition";

    type Transaction = {
        id: string;
        date: string;
        amount: number;
        currency: string;
        type: "TELEPORT" | "YIELD" | "GOVERNANCE" | "FEE_BURN";
        status: "VERIFIED" | "ANCHORING" | "CAUSAL_TRACE";
        target: string;
        description: string;
    };

    let transactions: Transaction[] = $state([
        {
            id: "tx-4492-ax",
            date: "FEB 18, 09:42",
            amount: 12500,
            currency: "AGE",
            type: "TELEPORT",
            status: "VERIFIED",
            target: "SHARD_ALPHA_01",
            description: "Teleportation to Alpha Shard",
        },
        {
            id: "tx-4493-mc",
            date: "FEB 18, 09:45",
            amount: 245.5,
            currency: "ARI",
            type: "YIELD",
            status: "VERIFIED",
            target: "VAULT_S3",
            description: "Merit Realization Dividend",
        },
        {
            id: "tx-4494-gv",
            date: "FEB 18, 09:50",
            amount: 50.0,
            currency: "AGE",
            type: "GOVERNANCE",
            status: "ANCHORING",
            target: "COUNCIL_VOTE",
            description: "Staking for Proposal #88",
        },
        {
            id: "tx-4495-fb",
            date: "FEB 18, 09:55",
            amount: 12.4,
            currency: "AGE",
            type: "FEE_BURN",
            status: "CAUSAL_TRACE",
            target: "PROTOCOL_CORE",
            description: "Standard Shard Maintenance Fee",
        },
    ]);

    let searchQuery = $state("");
    let filterType = $state("ALL");

    const statusStyles = {
        VERIFIED: "text-[#24AE7C] bg-[#24AE7C]/10 border-[#24AE7C]/20",
        ANCHORING: "text-neon-cyan bg-neon-cyan/10 border-neon-cyan/20",
        CAUSAL_TRACE: "text-amber-400 bg-amber-400/10 border-amber-400/20",
    };

    const typeIcons = {
        TELEPORT: ArrowUpRight,
        YIELD: ChevronDown,
        GOVERNANCE: ShieldCheck,
        FEE_BURN: Clock,
    };
</script>

<div class="space-y-6" in:fade>
    <!-- Header/Search -->
    <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-black/40 backdrop-blur-3xl p-8 rounded-[2.5rem] border border-white/[0.03]"
    >
        <div>
            <h2 class="text-3xl font-black italic tracking-tighter uppercase">
                SOVEREIGN_LEDGER
            </h2>
            <p
                class="text-[10px] mono-font text-white/40 uppercase tracking-[0.3em] mt-1"
            >
                High-Fidelity Causal Transaction Feed
            </p>
        </div>

        <div class="flex items-center gap-4">
            <div class="relative">
                <Search
                    size={14}
                    class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20"
                />
                <input
                    type="text"
                    placeholder="SEARCH_CAUSAL_ID..."
                    bind:value={searchQuery}
                    class="bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 text-[10px] font-black uppercase tracking-widest focus:outline-none focus:border-neon-cyan/40 transition-all w-64"
                />
            </div>
            <button
                class="p-4 bg-white/5 border border-white/10 rounded-xl text-white/40 hover:text-white transition-all"
            >
                <Filter size={16} />
            </button>
            <button
                class="flex items-center gap-2 px-6 py-3 bg-neon-cyan text-black font-black uppercase tracking-tighter text-[10px] rounded-xl hover:scale-105 active:scale-95 transition-all"
            >
                <Download size={14} /> EXPORT_SPEC_SHEET
            </button>
        </div>
    </div>

    <!-- Transaction List -->
    <div class="glass-panel overflow-hidden bg-black/40 border-white/[0.03]">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="border-b border-white/[0.05]">
                    <th
                        class="px-8 py-5 text-[8px] font-black uppercase tracking-[0.3em] text-white/20"
                        >TIMESTAMP</th
                    >
                    <th
                        class="px-8 py-5 text-[8px] font-black uppercase tracking-[0.3em] text-white/20"
                        >DESTINATION_SHARD</th
                    >
                    <th
                        class="px-8 py-5 text-[8px] font-black uppercase tracking-[0.3em] text-white/20"
                        >VALUE_SPEC</th
                    >
                    <th
                        class="px-8 py-5 text-[8px] font-black uppercase tracking-[0.3em] text-white/20"
                        >STATUS</th
                    >
                    <th
                        class="px-8 py-5 text-[8px] font-black uppercase tracking-[0.3em] text-white/20"
                        >ACTION</th
                    >
                </tr>
            </thead>
            <tbody>
                {#each transactions as tx}
                    {@const Icon = typeIcons[tx.type]}
                    <tr
                        class="group hover:bg-white/[0.02] transition-all border-b border-white/[0.02] last:border-0 cursor-pointer"
                    >
                        <td class="px-8 py-6">
                            <div class="flex flex-col">
                                <span
                                    class="text-[10px] font-black uppercase tracking-widest text-white/80"
                                    >{tx.date}</span
                                >
                                <span
                                    class="text-[7px] mono-font text-white/20 uppercase tracking-widest mt-1"
                                    >{tx.id}</span
                                >
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            <div class="flex items-center gap-3">
                                <div
                                    class="p-2 bg-white/5 rounded-lg text-white/40 group-hover:text-neon-cyan transition-colors"
                                >
                                    <Icon size={12} />
                                </div>
                                <div class="flex flex-col">
                                    <span
                                        class="text-[10px] font-black uppercase tracking-tight text-white/90"
                                        >{tx.description}</span
                                    >
                                    <span
                                        class="text-[7px] mono-font text-white/20 uppercase mt-0.5"
                                        >{tx.target}</span
                                    >
                                </div>
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            <div class="flex items-baseline gap-1.5">
                                <span
                                    class="text-sm font-black italic text-white"
                                    >{tx.amount.toLocaleString()}</span
                                >
                                <span
                                    class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                                    >{tx.currency}</span
                                >
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            <div
                                class="inline-flex items-center gap-2 px-3 py-1 rounded-full border text-[8px] font-black uppercase tracking-widest {statusStyles[
                                    tx.status
                                ]}"
                            >
                                <div
                                    class="w-1 h-1 rounded-full bg-current animate-pulse"
                                ></div>
                                {tx.status}
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            <button
                                class="px-4 py-2 border border-white/10 rounded-lg text-[8px] font-black uppercase tracking-widest text-white/40 hover:text-white hover:border-white/20 transition-all"
                            >
                                VIEW_CAUSAL_TRACE
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <!-- Pagination/Status -->
    <div
        class="flex items-center justify-between px-8 py-4 bg-white/[0.01] border border-white/[0.05] rounded-2xl"
    >
        <div class="flex items-center gap-3">
            <div
                class="w-2 h-2 rounded-full bg-[#24AE7C] animate-pulse shadow-[0_0_10px_#24AE7C/50]"
            ></div>
            <span
                class="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]"
                >NODE_SYNCHRONIZED_UTC_SESSION</span
            >
        </div>
        <div class="flex items-center gap-2">
            <button
                class="p-2 text-white/40 hover:text-white transition-all disabled:opacity-20"
                disabled
            >
                <ChevronDown size={16} class="rotate-90" />
            </button>
            <span class="text-[9px] font-black text-white px-2"
                >PAGE_01_OF_01</span
            >
            <button
                class="p-2 text-white/40 hover:text-white transition-all disabled:opacity-20"
                disabled
            >
                <ChevronDown size={16} class="-rotate-90" />
            </button>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
