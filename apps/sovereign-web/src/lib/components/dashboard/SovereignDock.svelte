<script lang="ts">
    import {
        LayoutDashboard,
        Send,
        Wallet,
        Globe,
        ShieldAlert,
        Settings,
        Activity,
        Users,
        ListChecks,
        Link2,
        UserPlus,
        Sparkles,
    } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { backOut } from "svelte/easing";

    let { activeTab, onSelect } = $props();

    const items = [
        { id: "overview", icon: LayoutDashboard, label: "Overview" },
        { id: "evolve", icon: Sparkles, label: "Evolve" },
        { id: "register", icon: UserPlus, label: "Onboard" },
        { id: "transfers", icon: Send, label: "Transfers" },
        { id: "ledger", icon: ListChecks, label: "Ledger" },
        { id: "link", icon: Link2, label: "Link" },
        { id: "council", icon: Users, label: "Council" },
        { id: "wallet", icon: Wallet, label: "Wallet" },
        { id: "market", icon: Globe, label: "Agora" },
        { id: "command", icon: ShieldAlert, label: "Command" },
        { id: "forensics", icon: Activity, label: "Forensics" },
    ];

    let hoveredId = $state<string | null>(null);
</script>

<div
    class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 px-4 py-3 glass-dock flex items-end gap-3"
    in:fly={{ y: 50, duration: 1000, easing: backOut }}
>
    {#each items as item}
        <button
            onclick={() => onSelect(item.id)}
            onmouseenter={() => (hoveredId = item.id)}
            onmouseleave={() => (hoveredId = null)}
            class="relative flex flex-col items-center group transition-all duration-300"
            style="transform: scale({hoveredId === item.id ? 1.4 : 1});"
        >
            <div
                class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300
                {activeTab === item.id
                    ? 'bg-neon-cyan text-black shadow-[0_0_20px_rgba(0,242,255,0.4)]'
                    : 'bg-white/[0.02] border border-white/10 text-white/40 hover:bg-white/5 hover:text-white/80'}"
            >
                <item.icon size={24} />
            </div>

            {#if hoveredId === item.id}
                <div
                    class="absolute -top-12 px-3 py-1.5 bg-black/80 border border-white/10 rounded-lg text-[9px] font-black uppercase tracking-widest text-white whitespace-nowrap shadow-2xl backdrop-blur-xl"
                    transition:fly={{ y: 5, duration: 200 }}
                >
                    {item.label}
                </div>
            {/if}

            {#if activeTab === item.id}
                <div
                    class="w-1.5 h-1.5 bg-neon-cyan rounded-full mt-2 shadow-[0_0_10px_#00f2ff]"
                ></div>
            {:else}
                <div class="h-1.5 mt-2"></div>
            {/if}
        </button>
    {/each}
</div>

<style>
    .glass-dock {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(60px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 2rem;
        box-shadow:
            0 40px 100px -20px rgba(0, 0, 0, 0.8),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
</style>
