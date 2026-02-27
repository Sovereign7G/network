<script lang="ts">
    import { fade } from "svelte/transition";
    import {
        ShieldCheck,
        Search,
        Truck,
        Box,
        Activity,
        Cpu,
        Droplets,
        ArrowRight,
    } from "lucide-svelte";

    type AtomicAsset = {
        id: string;
        name: string;
        category: "HARDWARE" | "BIOLOGICAL" | "RESOURCE";
        status: "IN_TRANSIT" | "VERIFIED" | "ARRIVED" | "QUARANTINED";
        origin: string;
        destination: string;
        forensicScore: number;
        shipmentDate: string;
    };

    let assets = $state<AtomicAsset[]>([
        {
            id: "ATM-0xAF",
            name: "ChordCortex_Neurochip_v4",
            category: "HARDWARE",
            status: "IN_TRANSIT",
            origin: "Sovereign_Fab_01 (Nagano)",
            destination: "Operator_Pod_Alpha",
            forensicScore: 99.8,
            shipmentDate: "2026-02-21 14:22",
        },
        {
            id: "ATM-0xBC",
            name: "Moral_BioToken_Vial_7",
            category: "BIOLOGICAL",
            status: "ARRIVED",
            origin: "DaVinci_Lab (Zug)",
            destination: "Regional_BioVault_02",
            forensicScore: 100,
            shipmentDate: "2026-02-18 09:12",
        },
    ]);

    let activeAssetId = $state("ATM-0xAF");
    let activeAsset = $derived(assets.find((a) => a.id === activeAssetId));

    function getStatusColor(status: string) {
        switch (status) {
            case "VERIFIED":
            case "ARRIVED":
                return "text-emerald-400";
            case "IN_TRANSIT":
                return "text-cyan-400";
            case "QUARANTINED":
                return "text-rose-400";
            default:
                return "text-white/20";
        }
    }
</script>

<div
    class="h-full bg-zinc-950 rounded-[2.5rem] border border-white/5 overflow-hidden flex flex-col shadow-2xl relative"
>
    <!-- Header -->
    <div
        class="p-8 bg-white/[0.02] border-b border-white/5 flex items-center justify-between"
    >
        <div class="flex items-center gap-4">
            <div class="p-3 bg-emerald-500/20 rounded-2xl text-emerald-400">
                <Box size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.3em] text-white"
                >
                    Borel-Simple_Phygital
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[8px] font-black text-emerald-400 uppercase tracking-widest italic"
                    >
                        ATOMIC_LAYER: ACTIVE
                    </span>
                    <div
                        class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"
                    ></div>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-6">
            <div class="text-right">
                <p
                    class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                >
                    Global_Provenance
                </p>
                <div class="flex items-center gap-1 justify-end">
                    <ShieldCheck size={10} class="text-emerald-400" />
                    <span class="text-[10px] font-mono text-white">SECURE</span>
                </div>
            </div>
        </div>
    </div>

    <div class="flex-1 flex overflow-hidden">
        <!-- Asset List -->
        <div
            class="w-80 border-r border-white/5 bg-black/20 overflow-y-auto p-6 space-y-6"
        >
            <div class="flex items-center justify-between">
                <h3
                    class="text-[9px] font-black text-white/40 uppercase tracking-[0.2em]"
                >
                    Atomic_Inventory
                </h3>
                <Search size={14} class="text-white/20" />
            </div>
            <div class="space-y-3">
                {#each assets as asset}
                    <button
                        onclick={() => (activeAssetId = asset.id)}
                        class="w-full p-5 rounded-[2rem] border text-left transition-all group overflow-hidden relative
                            {activeAssetId === asset.id
                            ? 'bg-emerald-500/10 border-emerald-500/30 shadow-xl'
                            : 'bg-transparent border-white/5 hover:border-white/10'}"
                    >
                        <div class="flex justify-between items-start mb-4">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                >{asset.id}</span
                            >
                            <div
                                class="p-2 bg-black/40 rounded-xl {getStatusColor(
                                    asset.status,
                                )}"
                            >
                                {#if asset.category === "HARDWARE"}
                                    <Cpu size={14} />
                                {:else}
                                    <Droplets size={14} />
                                {/if}
                            </div>
                        </div>
                        <h4
                            class="text-[10px] font-black text-white uppercase leading-tight mb-4"
                        >
                            {asset.name}
                        </h4>
                        <div
                            class="flex items-center justify-between pt-4 border-t border-white/5"
                        >
                            <span
                                class="text-[8px] font-black {getStatusColor(
                                    asset.status,
                                )} uppercase tracking-widest"
                                >{asset.status}</span
                            >
                            <span class="text-[9px] font-mono text-white/40"
                                >{asset.forensicScore}% VERIFIED</span
                            >
                        </div>
                    </button>
                {/each}
            </div>
        </div>

        <!-- Asset Forensic Detail -->
        <div
            class="flex-1 p-10 flex flex-col gap-10 overflow-y-auto scrollbar-hide"
        >
            {#if activeAsset}
                <div class="space-y-10" in:fade>
                    <div class="flex justify-between items-start">
                        <div class="space-y-2">
                            <h2
                                class="text-3xl font-black italic text-white tracking-tighter uppercase"
                            >
                                {activeAsset.name}
                            </h2>
                            <div class="flex gap-4">
                                <span
                                    class="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-[8px] font-black text-white/40 uppercase tracking-widest italic"
                                    >{activeAsset.category}</span
                                >
                                <span
                                    class="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-[8px] font-black text-emerald-400 uppercase tracking-widest"
                                    >QES_LINKED</span
                                >
                            </div>
                        </div>
                        <div class="text-right">
                            <p
                                class="text-[7px] font-black text-white/20 uppercase tracking-widest mb-1"
                            >
                                Atomic_Hash
                            </p>
                            <p class="text-[11px] font-mono text-white/60">
                                0x7F...4D2E
                            </p>
                        </div>
                    </div>

                    <!-- Supply Chain Timeline -->
                    <div class="space-y-6">
                        <h3
                            class="text-[9px] font-black text-white/40 uppercase tracking-[0.3em] px-2"
                        >
                            Phygital_Provenance_Trace
                        </h3>
                        <div class="relative pl-12 space-y-8">
                            <!-- Timeline Line -->
                            <div
                                class="absolute left-[23px] top-2 bottom-2 w-[2px] bg-white/5"
                            ></div>

                            <!-- Destination -->
                            <div class="relative">
                                <div
                                    class="absolute -left-12 w-12 h-12 bg-zinc-950 flex items-center justify-center"
                                >
                                    <div
                                        class="w-3 h-3 rounded-full bg-emerald-400 shadow-[0_0_15px_rgba(52,211,153,0.5)]"
                                    ></div>
                                </div>
                                <div
                                    class="p-6 bg-white/[0.02] border border-white/5 rounded-3xl space-y-2"
                                >
                                    <p
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                    >
                                        Destination
                                    </p>
                                    <p
                                        class="text-[11px] font-black text-white uppercase"
                                    >
                                        {activeAsset.destination}
                                    </p>
                                    <div
                                        class="flex items-center gap-3 text-[8px] font-black text-emerald-400/60 uppercase"
                                    >
                                        <ShieldCheck size={10} />
                                        Audit: Borel-Simple Invariant Pass
                                    </div>
                                </div>
                            </div>

                            <!-- Mid-Point -->
                            <div class="relative opacity-60">
                                <div
                                    class="absolute -left-12 w-12 h-12 bg-zinc-950 flex items-center justify-center"
                                >
                                    <div
                                        class="w-3 h-3 rounded-full bg-cyan-400"
                                    ></div>
                                </div>
                                <div
                                    class="p-6 bg-white/[0.02] border border-white/5 rounded-3xl space-y-2"
                                >
                                    <p
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                    >
                                        In-Transit
                                    </p>
                                    <p
                                        class="text-[11px] font-black text-white uppercase"
                                    >
                                        Regional_Transit_Hub_09
                                    </p>
                                    <div
                                        class="flex items-center gap-3 text-[8px] font-black text-cyan-400/60 uppercase"
                                    >
                                        <Truck size={10} />
                                        Batch: BATCH-0x992-ALPHA
                                    </div>
                                </div>
                            </div>

                            <!-- Origin -->
                            <div class="relative opacity-40">
                                <div
                                    class="absolute -left-12 w-12 h-12 bg-zinc-950 flex items-center justify-center"
                                >
                                    <div
                                        class="w-3 h-3 rounded-full bg-white/20"
                                    ></div>
                                </div>
                                <div
                                    class="p-6 bg-white/[0.02] border border-white/5 rounded-3xl space-y-2"
                                >
                                    <p
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                    >
                                        Genesis_Origin
                                    </p>
                                    <p
                                        class="text-[11px] font-black text-white uppercase"
                                    >
                                        {activeAsset.origin}
                                    </p>
                                    <p
                                        class="text-[8px] font-black text-white/20 uppercase"
                                    >
                                        {activeAsset.shipmentDate}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Digital Twin Stats -->
                    <div
                        class="grid grid-cols-2 gap-8 pt-6 border-t border-white/5"
                    >
                        <div class="space-y-4">
                            <div
                                class="flex items-center gap-3 text-emerald-400"
                            >
                                <Activity size={16} />
                                <span
                                    class="text-[9px] font-black uppercase tracking-widest"
                                    >Inherent_Veracity</span
                                >
                            </div>
                            <div
                                class="text-3xl font-black text-white tracking-widest italic"
                            >
                                {activeAsset.forensicScore}%
                            </div>
                            <p
                                class="text-[9px] text-white/30 leading-relaxed uppercase font-black tracking-widest"
                            >
                                Physical lifecycle verified by 1,421 mesh-nodes.
                            </p>
                        </div>
                        <div class="flex items-end justify-end">
                            <button
                                class="px-8 py-4 bg-white text-black text-[10px] font-black uppercase tracking-[0.3em] rounded-2xl hover:scale-105 active:scale-95 transition-all shadow-xl flex items-center gap-2"
                            >
                                Audit_Deep_Trace
                                <ArrowRight size={14} />
                            </button>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
