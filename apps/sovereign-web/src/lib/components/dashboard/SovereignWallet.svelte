<script lang="ts">
    import {
        Wallet,
        ArrowUpRight,
        ArrowDownLeft,
        ArrowLeftRight,
        Plus,
        History,
        CreditCard,
        Eye,
        EyeOff,
        TrendingUp,
    } from "lucide-svelte";
    import { fade, slide } from "svelte/transition";
//     import DonutChart from "./DonutChart.svelte";

    let showBalance = $state(true);

    const assets = [
        {
            name: "AGE Protocol",
            symbol: "AGE",
            amount: "1,000.00",
            value: "$1,000.00",
            color: "text-neon-cyan",
            bg: "bg-neon-cyan/10",
        },
        {
            name: "Universal Coherence",
            symbol: "UCT",
            amount: "5,240.21",
            value: "$5,240.21",
            color: "text-amber-400",
            bg: "bg-amber-400/10",
        },
        {
            name: "Ethereum",
            symbol: "ETH",
            amount: "1.42",
            value: "$4,260.00",
            color: "text-purple-400",
            bg: "bg-purple-400/10",
        },
        {
            name: "Bitcoin",
            symbol: "BTC",
            amount: "0.02",
            value: "$1,950.00",
            color: "text-orange-400",
            bg: "bg-orange-400/10",
        },
    ];

    let processingId = $state<string | null>(null);

    const actions = [
        {
            icon: ArrowUpRight,
            label: "Send",
            color: "bg-white/5 hover:bg-white/10",
        },
        {
            icon: ArrowDownLeft,
            label: "Receive",
            color: "bg-white/5 hover:bg-white/10",
        },
        {
            icon: ArrowLeftRight,
            label: "Swap",
            color: "bg-white/5 hover:bg-white/10",
        },
        {
            icon: Plus,
            label: "Buy",
            color: "bg-neon-cyan text-black hover:scale-105 shadow-[0_0_20px_rgba(0,242,255,0.2)]",
        },
    ];
</script>

<div class="space-y-8" in:fade>
    <!-- Balance & Quick Actions -->
    <section
        class="glass-panel p-10 relative overflow-hidden bg-gradient-to-br from-neon-cyan/5 to-transparent"
    >
        <div
            class="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative z-10"
        >
            <div class="space-y-4">
                <div class="flex items-center gap-3">
                    <span
                        class="text-[10px] font-black text-white/40 uppercase tracking-[0.2em]"
                        >Total Balance</span
                    >
                    <button
                        onclick={() => (showBalance = !showBalance)}
                        class="text-white/20 hover:text-white/40 transition-colors"
                    >
                        {#if showBalance}
                            <Eye size={14} />
                        {:else}
                            <EyeOff size={14} />
                        {/if}
                    </button>
                </div>
                <div class="flex items-baseline gap-4">
                    <h2 class="text-6xl font-black tracking-tighter">
                        {#if showBalance}
                            $12,450.00
                        {:else}
                            ••••••••
                        {/if}
                    </h2>
                    <span
                        class="text-green-400 font-bold flex items-center gap-1 text-sm"
                    >
                        <TrendingUp size={14} />
                        +4.2%
                    </span>
                </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 w-full md:w-auto">
                {#each actions as action}
                    {@const Icon = action.icon}
                    <button
                        onclick={() => {
                            processingId = action.label;
                            setTimeout(() => (processingId = null), 1500);
                        }}
                        class="flex flex-col items-center gap-3 p-5 rounded-3xl {action.color} transition-all border border-white/5 group min-w-[110px] active:scale-95 relative overflow-hidden"
                    >
                        {#if processingId === action.label}
                            <div
                                class="absolute inset-0 bg-neon-cyan/20 animate-pulse flex items-center justify-center z-10"
                            >
                                <div
                                    class="w-6 h-6 border-2 border-neon-cyan border-t-transparent rounded-full animate-spin"
                                ></div>
                            </div>
                        {/if}
                        <Icon
                            size={28}
                            class="group-hover:scale-110 transition-transform {action.label ===
                            'Send'
                                ? 'text-neon-cyan'
                                : ''}"
                        />
                        <span
                            class="text-[10px] font-black uppercase tracking-widest"
                            >{action.label}</span
                        >
                        {#if action.label === "Send"}
                            <div
                                class="h-0.5 w-4 bg-neon-cyan rounded-full mt-1"
                            ></div>
                        {/if}
                    </button>
                {/each}
            </div>
        </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Asset List -->
        <div class="lg:col-span-8">
            <section class="glass-panel p-8 space-y-8">
                <div
                    class="grid grid-cols-1 md:grid-cols-12 gap-10 items-center mb-12"
                >
                    <div class="md:col-span-5 flex justify-center">
                        <DonutChart
                            size={240}
                            strokeWidth={30}
                            data={[
                                { label: "AGE", value: 1000, color: "#00f2ff" },
                                { label: "UCT", value: 5240, color: "#fbbf24" },
                                { label: "ETH", value: 4260, color: "#a855f7" },
                                { label: "BTC", value: 1950, color: "#fb923c" },
                            ]}
                        />
                    </div>
                    <div class="md:col-span-7 space-y-4">
                        <h4
                            class="text-xs font-black uppercase tracking-[0.2em] text-white/30 mb-6"
                        >
                            Asset Allocation
                        </h4>
                        <div class="grid grid-cols-2 gap-4">
                            {#each assets as asset}
                                <div
                                    class="flex items-center gap-3 p-4 bg-white/5 rounded-2xl border border-white/5"
                                >
                                    <div
                                        class="w-2 h-2 rounded-full {asset.bg.replace(
                                            '/10',
                                            '',
                                        )}"
                                    ></div>
                                    <div class="flex flex-col">
                                        <span
                                            class="text-[10px] font-black uppercase tracking-widest"
                                            >{asset.name}</span
                                        >
                                        <span
                                            class="text-xs font-bold text-white/40"
                                            >{Math.round(
                                                (parseFloat(
                                                    asset.value
                                                        .replace("$", "")
                                                        .replace(",", ""),
                                                ) /
                                                    12450) *
                                                    100,
                                            )}%</span
                                        >
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <h3
                        class="text-xs font-black uppercase tracking-[0.2em] text-white/40"
                    >
                        Your Assets
                    </h3>
                    <button
                        class="text-[10px] font-black text-neon-cyan uppercase hover:underline"
                        >View All</button
                    >
                </div>

                <div class="space-y-4">
                    {#each assets as asset}
                        <div
                            class="flex items-center justify-between p-6 bg-white/[0.02] rounded-3xl border border-white/5 hover:bg-white/[0.05] hover:border-neon-cyan/20 transition-all cursor-pointer group relative overflow-hidden"
                        >
                            <div
                                class="absolute top-0 left-0 w-1 h-full bg-neon-cyan/20 terminal-pulse"
                            ></div>
                            <div class="flex items-center gap-6">
                                <div
                                    class="w-14 h-14 rounded-2xl {asset.bg} flex items-center justify-center text-xl font-black {asset.color}"
                                >
                                    {asset.symbol[0]}
                                </div>
                                <div class="flex flex-col">
                                    <div class="flex items-center gap-2">
                                        <span class="text-lg font-black"
                                            >{asset.name}</span
                                        >
                                        <div
                                            class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-xs font-bold text-white/40 uppercase tracking-widest"
                                        >{asset.symbol}</span
                                    >
                                </div>
                            </div>
                            <div class="flex flex-col items-end">
                                <span class="text-lg font-black"
                                    >{asset.amount}</span
                                >
                                <span class="text-xs font-bold text-white/40"
                                    >{asset.value}</span
                                >
                            </div>
                        </div>
                    {/each}
                </div>
            </section>
        </div>

        <!-- Right Side: Cards & History -->
        <div class="lg:col-span-4 space-y-8">
            <section class="glass-panel p-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3
                        class="text-xs font-black uppercase tracking-[0.2em] text-white/40 flex items-center gap-2"
                    >
                        <CreditCard size={14} />
                        Sovereign Card
                    </h3>
                </div>
                <div
                    class="aspect-[1.58/1] w-full bg-gradient-to-br from-neon-cyan to-blue-600 rounded-3xl p-8 relative overflow-hidden flex flex-col justify-between shadow-2xl shadow-neon-cyan/20"
                >
                    <div class="absolute top-0 right-0 p-8 opacity-20">
                        <Wallet size={80} />
                    </div>
                    <div class="flex justify-between items-start relative z-10">
                        <span class="text-black font-black italic text-xl"
                            >AGE</span
                        >
                        <div class="w-12 h-8 bg-white/20 rounded-lg"></div>
                    </div>
                    <div class="space-y-4 relative z-10">
                        <span
                            class="text-black/60 font-medium tracking-[0.3em] block"
                            >•••• •••• •••• 99A1</span
                        >
                        <div class="flex justify-between items-end">
                            <span class="text-black font-black uppercase"
                                >Sovereign Holder</span
                            >
                            <span
                                class="text-black/60 text-[10px] font-black uppercase"
                                >Exp 12/28</span
                            >
                        </div>
                    </div>
                </div>
                <button
                    class="w-full py-4 bg-white/5 rounded-xl text-[10px] font-black uppercase hover:bg-white/10 transition-all"
                    >MANAGE CARDS</button
                >
            </section>

            <section class="glass-panel p-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3
                        class="text-xs font-black uppercase tracking-[0.2em] text-white/40 flex items-center gap-2"
                    >
                        <History size={14} />
                        Recent Activity
                    </h3>
                </div>
                <div class="space-y-6">
                    {#each [1, 2, 3] as _}
                        <div class="flex items-center gap-4">
                            <div
                                class="w-10 h-10 rounded-full bg-green-400/10 flex items-center justify-center text-green-400"
                            >
                                <ArrowDownLeft size={16} />
                            </div>
                            <div class="flex flex-col flex-1">
                                <span class="text-xs font-black"
                                    >Received UCT</span
                                >
                                <span class="text-[10px] text-white/30"
                                    >From: 0xFD...7782</span
                                >
                            </div>
                            <span class="text-xs font-black text-green-400"
                                >+125.00</span
                            >
                        </div>
                    {/each}
                </div>
            </section>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(40px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
    }

    @keyframes terminal-pulse {
        0%,
        100% {
            opacity: 0.1;
        }
        50% {
            opacity: 0.4;
        }
    }

    .terminal-pulse {
        animation: terminal-pulse 2s ease-in-out infinite;
    }
</style>
