<script lang="ts">
    import {
        ShoppingBag,
        MapPin,

        Zap,
        Navigation,
        CreditCard,
        Gift,
        ShieldCheck,
        TrendingUp,
        Heart,
        BookOpen,
        Languages,
        Wrench,
        Sparkles,
        QrCode,
    } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import { AAL3Service } from "../../auth/aal3";
    import { onMount } from "svelte";

    import SovereignMarketSearch from "./SovereignMarketSearch.svelte";
    import SovereignStories from "./SovereignStories.svelte";
    import SovereignMarketVoom from "./SovereignMarketVoom.svelte";
    import SovereignMarketDiscovery from "./SovereignMarketDiscovery.svelte";
    import SovereignMarketItems from "./SovereignMarketItems.svelte";
    import SovereignMarketSidebar from "./SovereignMarketSidebar.svelte";
    import SovereignMarketIsomorphicHub from "./SovereignMarketIsomorphicHub.svelte";
    import SovereignMarketKBrowser from "./SovereignMarketKBrowser.svelte";

    interface Props {
        onSelect: (id: string) => void;
        isZenMode?: boolean;
    }

    let { onSelect, isZenMode = false }: Props = $props();

    const aal3 = AAL3Service.getInstance();
    let isAAL3Verified = $state(false);
    let searchQuery = $state("");
    let activeCategory = $state("ALL_SERVICES");
    let showIsomorphicHub = $state(false);
    let activeWebShard = $state<string | null>(null);

    onMount(async () => {
        isAAL3Verified = aal3.isVerified();
    });

    const categories = [
        "ALL_SERVICES",
        "EXPRESS_DELIVERY",
        "TECHNICAL_REPAIRS",
        "AGENTIC_CONSULTATION",
        "GOVERNANCE_TASKS",
        "WEALTH_STRATEGIES",
    ];

    const marketplaceItems = [
        {
            id: "it-001",
            title: "Urgent Substrate Repair",
            author: "Maintenance-Bot-04",
            rating: 4.9,
            reviews: 124,
            reward: "125.00",
            listPrice: "150.00",
            currency: "AGE",
            time: "25 min",
            type: "TECHNICAL",
            urgency: "CRITICAL",
            icon: Wrench,
            color: "text-neon-cyan",
            bg: "bg-neon-cyan/10",
            badges: ["AAL3_VERIFIED"],
            delivery: "Arrives in 14ms",
        },
        {
            id: "it-002",
            title: "Yield Strategy: Alpha-7",
            author: "Wealth-Shaper-AI",
            rating: 5.0,
            reviews: 890,
            reward: "1,200.00",
            listPrice: "1,450.00",
            currency: "ARI",
            time: "INSTANT",
            type: "STRATEGY",
            urgency: "OPTIMAL",
            icon: Sparkles,
            color: "text-amber-400",
            bg: "bg-amber-400/10",
            badges: ["CANISTER_SAFE", "TOP_PICK"],
            delivery: "Instant_Teleport",
        },
        {
            id: "it-003",
            title: "Identity Attestation Witness",
            author: "Validator-Node-88",
            rating: 4.7,
            reviews: 42,
            reward: "15.00",
            listPrice: "20.00",
            currency: "AGE",
            time: "5 min",
            type: "GOVERNANCE",
            urgency: "NORMAL",
            icon: ShieldCheck,
            color: "text-green-400",
            bg: "bg-green-400/10",
            badges: [],
            delivery: "Arrives in 1 hour",
        },
    ];

    const suggestions = [
        "Yield Strategy Alpha-7",
        "AAL3 Shard Verification",
        "Council Consultation Session",
        "Marketplace Talent Audit",
    ];

    const quickShards = [
        {
            icon: QrCode,
            label: "SCAN_PAY",
            color: "bg-blue-500/10 text-blue-400",
            hover: "hover:bg-blue-500/20",
        },
        {
            icon: CreditCard,
            label: "WALLET",
            color: "bg-orange-500/10 text-orange-400",
            hover: "hover:bg-orange-500/20",
        },
        {
            icon: Navigation,
            label: "HAILING",
            color: "bg-green-500/10 text-green-400",
            hover: "hover:bg-green-500/20",
        },
        {
            icon: ShoppingBag,
            label: "MALL",
            color: "bg-pink-500/10 text-pink-400",
            hover: "hover:bg-pink-500/20",
        },
        {
            icon: Gift,
            label: "RE_ENVELOPE",
            color: "bg-red-500/10 text-red-400",
            hover: "hover:bg-red-500/20",
        },
        {
            icon: ShieldCheck,
            label: "INSURE",
            color: "bg-purple-500/10 text-purple-400",
            hover: "hover:bg-purple-500/20",
        },
        {
            icon: TrendingUp,
            label: "WEALTH",
            color: "bg-amber-500/10 text-amber-400",
            hover: "hover:bg-amber-500/20",
        },
        {
            icon: MapPin,
            label: "CITY_LIFE",
            color: "bg-cyan-500/10 text-cyan-400",
            hover: "hover:bg-cyan-500/20",
        },
        {
            icon: BookOpen,
            label: "ACADEMY",
            color: "bg-indigo-500/10 text-indigo-400",
            hover: "hover:bg-indigo-500/20",
        },
        {
            icon: Heart,
            label: "HEALTH",
            color: "bg-rose-500/10 text-rose-400",
            hover: "hover:bg-rose-500/20",
        },
    ];

    async function toggleAnchoredSession() {
        if (!isAAL3Verified) {
            await aal3.performHandshake();
            isAAL3Verified = true;
        } else {
            isAAL3Verified = false;
        }
    }

    function openWebShard(label: string) {
        activeWebShard = `https://${label.toLowerCase()}.age-protocol.io`;
    }
</script>

<div class="space-y-10" in:fade>
    <SovereignMarketSearch
        bind:searchQuery
        {isAAL3Verified}
        onToggleAnchored={toggleAnchoredSession}
        {suggestions}
    />

    <section class="space-y-6">
        <div class="flex gap-4 overflow-x-auto pb-4 custom-scrollbar">
            {#each categories as category}
                <button
                    onclick={() => (activeCategory = category)}
                    class="whitespace-nowrap px-8 py-3 rounded-2xl text-[9px] font-black uppercase tracking-[0.2em] transition-all border
                    {activeCategory === category
                        ? 'bg-white text-black border-white'
                        : 'bg-black/40 text-white/40 border-white/5 hover:border-white/20'}"
                >
                    {category.replace("_", " ")}
                </button>
            {/each}
        </div>

        <SovereignMarketVoom {isZenMode} />

        <div
            class="grid grid-cols-4 md:grid-cols-10 gap-2 md:gap-4 py-8 {isZenMode
                ? 'border-black/5'
                : 'border-white/5'} border-t"
        >
            {#each quickShards as shard}
                <button
                    onclick={() => openWebShard(shard.label)}
                    class="flex flex-col items-center gap-2 group transition-all"
                >
                    <div
                        class="w-14 h-14 rounded-[1.8rem] {shard.color} {shard.hover} flex items-center justify-center border border-white/5 group-hover:scale-105 transition-all shadow-lg group-active:scale-95"
                    >
                        <shard.icon size={22} />
                    </div>
                    <span
                        class="text-[7px] font-black tracking-widest uppercase text-white/30 group-hover:text-white transition-colors"
                        >{shard.label}</span
                    >
                </button>
            {/each}
        </div>

        <SovereignStories />

        <SovereignMarketDiscovery />
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div class="lg:col-span-8 space-y-8">
            <SovereignMarketItems items={marketplaceItems} {onSelect} />
        </div>
        <div class="lg:col-span-4">
            <SovereignMarketSidebar {marketplaceItems} {onSelect} />
        </div>
    </div>
</div>

<SovereignMarketIsomorphicHub
    bind:show={showIsomorphicHub}
    onClose={() => (showIsomorphicHub = false)}
/>

<SovereignMarketKBrowser
    url={activeWebShard}
    onClose={() => (activeWebShard = null)}
/>

<button
    onclick={() => (showIsomorphicHub = !showIsomorphicHub)}
    class="fixed bottom-10 right-10 w-14 h-14 bg-white text-black rounded-full shadow-[0_0_50px_rgba(255,255,255,0.2)] flex items-center justify-center hover:scale-110 transition-all z-[60] group"
>
    <Languages size={24} />
</button>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        height: 4px;
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
