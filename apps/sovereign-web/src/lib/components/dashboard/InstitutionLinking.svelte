<script lang="ts">
    import {
        Building2,
        Link2,
        CheckCircle2,
        ChevronRight,
        Plus,
        ExternalLink,
    } from "lucide-svelte";
    import { fade, slide } from "svelte/transition";
    import { Info } from "lucide-svelte";

    let { showWisdom } = $props();

    let institutions = $state([
        {
            name: "Sovereign Node Alpha",
            id: "ryjl3-tyaaa-aaaaa-aaaba-cai",
            status: "Connected",
            balance: "12,450.00",
            icon: Building2,
            connectedAt: "2026-02-14",
        },
        {
            name: "IC Vault Matrix",
            id: "vu5yx-eh777-77774-qaaga-cai",
            status: "Connected",
            balance: "5,240.21",
            icon: Building2,
            connectedAt: "2026-02-15",
        },
    ]);

    let isConnecting = $state(false);

    function handleConnect() {
        isConnecting = true;
        setTimeout(() => {
            isConnecting = false;
        }, 2000);
    }
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <div>
            <h3
                class="text-xl font-black italic tracking-tightest text-white/90"
            >
                LINKED SOVEREIGN INSTITUTIONS
            </h3>
            <p
                class="text-[10px] mono-font text-white/30 uppercase tracking-[0.2em] mt-1"
            >
                Manage external agents and protocol shards
            </p>
        </div>
        <div class="relative">
            <button
                onclick={handleConnect}
                disabled={isConnecting}
                class="flex items-center gap-2 px-6 py-3 bg-neon-cyan/10 border border-neon-cyan/30 text-neon-cyan rounded-2xl hover:bg-neon-cyan/20 transition-all group"
            >
                {#if isConnecting}
                    <div
                        class="w-4 h-4 border-2 border-neon-cyan border-t-transparent rounded-full animate-spin"
                    ></div>
                {:else}
                    <Plus
                        size={16}
                        class="group-hover:rotate-90 transition-transform"
                    />
                {/if}
                <span class="text-[10px] font-black uppercase tracking-widest"
                    >Connect Agent</span
                >
            </button>
            {#if showWisdom && !isConnecting}
                <div
                    class="absolute -bottom-8 right-0 px-2 py-1 bg-amber-400 text-black text-[8px] font-black rounded shadow-lg whitespace-nowrap z-20"
                >
                    NOTE: Links external canisters to your Sovereign Identity.
                </div>
            {/if}
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#each institutions as inst}
            <div
                class="glass-panel p-6 border-white/5 hover:border-neon-cyan/30 transition-all group relative overflow-hidden"
            >
                <div
                    class="absolute -right-4 -top-4 opacity-5 group-hover:opacity-10 transition-opacity"
                >
                    <inst.icon size={120} />
                </div>

                <div class="flex flex-col h-full justify-between relative z-10">
                    <div class="flex justify-between items-start mb-6">
                        <div
                            class="w-12 h-12 rounded-xl bg-neon-cyan/10 flex items-center justify-center text-neon-cyan"
                        >
                            <inst.icon size={24} />
                        </div>
                        <div
                            class="flex items-center gap-2 px-2 py-1 bg-green-500/10 border border-green-500/30 rounded-lg"
                        >
                            <CheckCircle2 size={10} class="text-green-400" />
                            <span
                                class="text-[8px] font-black text-green-400 uppercase tracking-widest"
                                >{inst.status}</span
                            >
                        </div>
                    </div>

                    <div class="space-y-1">
                        <h4 class="text-lg font-black">{inst.name}</h4>
                        <p class="text-[10px] mono-font text-white/30 truncate">
                            {inst.id}
                        </p>
                    </div>

                    <div
                        class="mt-6 pt-6 border-t border-white/5 flex justify-between items-end"
                    >
                        <div>
                            <span
                                class="text-[10px] font-black text-white/30 uppercase tracking-widest block mb-1"
                                >Total Shard Balance</span
                            >
                            <span class="text-xl font-black tracking-tight"
                                >${inst.balance}</span
                            >
                        </div>
                        <button
                            class="p-2 text-white/20 hover:text-white/60 transition-colors"
                        >
                            <ExternalLink size={18} />
                        </button>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
    }
</style>
