<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";
    import { Package, Truck, ShieldCheck, MapPin } from "lucide-svelte";

    const logistics = $derived(manifold.logisticsState);

    function getStatusColor(status: string) {
        switch (status) {
            case "VERIFIED":
            case "DELIVERED":
                return "text-emerald-400";
            case "IN_TRANSIT":
            case "CURRENT":
                return "text-cyan-400";
            default:
                return "text-white/40";
        }
    }
</script>

<div
    class="inventory-matrix flex flex-col h-full bg-slate-900/40 rounded-[3rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
    in:fade
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="p-4 bg-white/5 rounded-2xl text-emerald-400">
                <Package size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Logistics_Matrix
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[9px] font-black text-white/30 uppercase tracking-widest"
                        >Mesh_Verified: {logistics.shipments.filter(

                            (s) => s.mesh_verified,
                        ).length}/{logistics.shipments.length}</span
                    >
                </div>
            </div>
        </div>
        <div
            class="px-3 py-1 bg-emerald-400/10 border border-emerald-400/20 rounded-full flex items-center gap-2"
        >
            <ShieldCheck size={12} class="text-emerald-400" />
            <span
                class="text-[8px] font-black text-emerald-400 uppercase tracking-widest"
                >QES_LINKED</span
            >
        </div>
    </div>

    <!-- Active Deliveries -->
    <div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
        {#each logistics.shipments as s (s.id)}
            <div
                class="bg-white/5 border border-white/5 p-5 rounded-[2.5rem] hover:bg-white/10 transition-all flex flex-col gap-4 relative overflow-hidden group/shipment"
            >
                <div class="flex justify-between items-start">
                    <div class="flex gap-4 items-start">
                        <div
                            class="p-3 bg-black/40 rounded-2xl {s.status ===
                            'IN_TRANSIT'
                                ? 'text-cyan-400'
                                : 'text-white/20'}"
                        >
                            <Truck size={20} />
                        </div>
                        <div>
                            <h4
                                class="text-sm font-black text-white group-hover/shipment:text-cyan-400 transition-colors"
                            >
                                {s.product}
                            </h4>
                            <div
                                class="text-[8px] font-black text-white/20 uppercase tracking-widest flex items-center gap-2"
                            >
                                <MapPin size={10} />
                                {s.route}
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    class="flex justify-between items-center mt-2 pt-4 border-t border-white/5"
                >
                    <div class="flex flex-col">
                        <span
                            class="text-[7px] font-black text-white/20 uppercase mb-1"
                            >Status</span
                        >
                        <span
                            class="text-[10px] font-black {getStatusColor(
                                s.status,
                            )} uppercase tracking-widest">{s.status}</span
                        >
                    </div>
                    <div class="flex flex-col text-right">
                        <span
                            class="text-[7px] font-black text-white/20 uppercase mb-1"
                            >Mesh_Verification</span
                        >
                        <span
                            class="text-[10px] font-black {s.mesh_verified
                                ? 'text-emerald-400'
                                : 'text-rose-400'} uppercase tracking-widest"
                        >
                            {s.mesh_verified ? "SECURE" : "PENDING"}
                        </span>
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <!-- Network Topology -->
    <div class="p-6 bg-black/40 rounded-3xl border border-white/5">
        <div class="flex justify-between items-center mb-4">
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                >Mesh_Congestion</span
            >
            <span class="text-[10px] font-black text-cyan-400">NOMINAL</span>
        </div>
        <div class="grid grid-cols-8 gap-1">
            {#each Array(24) as _, i}
                <div
                    class="h-4 rounded-sm {i % 5 === 0
                        ? 'bg-cyan-400/20'
                        : 'bg-white/5'}"
                ></div>
            {/each}
        </div>
    </div>
</div>

<style>
    .supply-chain-provenance {
        background: linear-gradient(
            135deg,
            rgba(16, 24, 39, 0.4) 0%,
            rgba(2, 6, 23, 0.4) 100%
        );
        backdrop-filter: blur(40px);
    }

    .provenance-loader {
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
</style>
