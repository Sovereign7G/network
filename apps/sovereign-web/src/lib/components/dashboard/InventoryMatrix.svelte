<script lang="ts">
    import { fade } from "svelte/transition";

    let inventory: any[] = $state([
        {
            id: "SKU-001",
            name: "Sovereign Lens v4",
            stock: 142,
            unit: "units",
            health: "OPTIMAL",
        },
        {
            id: "SKU-882",
            name: "Bio-Liquid Core",
            stock: 850,
            unit: "liters",
            health: "STABLE",
        },
        {
            id: "SKU-404",
            name: "Mesh Shards",
            stock: 12,
            unit: "crates",
            health: "CRITICAL",
        },
        {
            id: "SKU-901",
            name: "Identity Seals",
            stock: 5000,
            unit: "sigs",
            health: "OPTIMAL",
        },
    ]);

    function getHealthColor(health: string) {
        switch (health) {
            case "OPTIMAL":
                return "text-emerald-400";
            case "STABLE":
                return "text-cyan-400";
            case "CRITICAL":
                return "text-rose-500";
            default:
                return "text-white/20";
        }
    }
</script>

<div class="inventory-matrix glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-start mb-6">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Inventory Matrix
            </h3>
            <p class="text-[9px] text-white/20 uppercase font-bold">
                Real-time resource allocation
            </p>
        </div>
        <div class="text-right">
            <span
                class="text-[8px] font-black uppercase text-white/20 block mb-1"
                >Stock Level</span
            >
            <span class="text-xs font-black text-white">6,004 Total</span>
        </div>
    </div>

    <div class="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar">
        {#each inventory as item}
            <div
                class="inventory-item bg-white/[0.02] border border-white/5 p-3 rounded-xl flex justify-between items-center group hover:bg-white/[0.05] transition-all"
            >
                <div class="flex flex-col">
                    <span
                        class="text-[10px] font-black text-white group-hover:text-cyan-400 transition-colors uppercase"
                        >{item.name}</span
                    >
                    <span class="text-[8px] font-mono text-white/20"
                        >{item.id}</span
                    >
                </div>
                <div class="flex flex-col items-end">
                    <span class="text-xs font-black text-white"
                        >{item.stock}
                        <span class="text-[8px] text-white/40">{item.unit}</span
                        ></span
                    >
                    <span
                        class="text-[8px] font-black uppercase {getHealthColor(
                            item.health,
                        )}">{item.health}</span
                    >
                </div>
            </div>
        {/each}
    </div>

    <div class="mt-4 grid grid-cols-2 gap-2">
        <button
            class="py-2 bg-white/5 border border-white/10 rounded-lg text-[8px] font-black uppercase tracking-widest text-white/40 hover:text-white transition-all"
            >Audit Warehouse</button
        >
        <button
            class="py-2 bg-white/5 border border-white/10 rounded-lg text-[8px] font-black uppercase tracking-widest text-white/40 hover:text-white transition-all"
            >Restock Flow</button
        >
    </div>
</div>

<style>
    .inventory-matrix {
        background: linear-gradient(
            135deg,
            rgba(16, 24, 39, 0.4) 0%,
            rgba(2, 6, 23, 0.4) 100%
        );
        backdrop-filter: blur(40px);
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 2px;
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
