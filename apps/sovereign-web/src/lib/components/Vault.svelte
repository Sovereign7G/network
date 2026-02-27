<script lang="ts">
    import {
        ArrowUpRight,
        ArrowDownLeft,
        History,

        TrendingUp,
        Plus,
        Layers3,
        Activity,
        CreditCard,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";


    const summaryStats = [
        {

            label: "NET RESOURCE VOLUME",
            value: "842,450.00",
            trend: "+5.2%",
            status: "OPTIMAL",
        },
    ];

    const actions = [
        {
            id: "send",
            label: "SEND SHARD",
            icon: ArrowUpRight,
            color: "bg-cyan-400",
            textColor: "text-black",
        },
        {
            id: "receive",
            label: "RECEIVE",
            icon: ArrowDownLeft,
            color: "bg-white/5",
            border: "border-white/10",
            textColor: "text-white",
        },
        {
            id: "swap",
            label: "SWAP",
            icon: Layers3,
            color: "bg-white/5",
            border: "border-white/10",
            textColor: "text-white",
        },
    ];

    const assets = [
        {
            name: "Earth Fiat",
            symbol: "USD",
            amount: "125,000.00",
            color: "bg-blue-400",
        },
        {
            name: "Network Liquidity",
            symbol: "H2O",
            amount: "45.00",
            color: "bg-cyan-400",
        },
        {
            name: "Sovereign Bonds",
            symbol: "BOND",
            amount: "0.05",
            color: "bg-amber-400",
        },
    ];

    const activity = [
        {
            label: "Incoming Drip",
            amount: "+500.00 Credits",
            time: "2m ago",
            color: "text-emerald-400",
        },
        {
            label: "Tax Orchestration",
            amount: "-12.40 Credits",
            time: "1h ago",
            color: "text-rose-400",
        },
    ];
</script>

<div class="px-8 py-12 max-w-6xl mx-auto" in:fade>
    <!-- Briefing Header -->
    <div class="mb-12 flex items-end justify-between">
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
            >
                Sovereign Vault // Secure
            </div>
            <h1 class="text-6xl font-black italic uppercase tracking-tighter">
                Resource <span class="text-cyan-400">Hub</span>
            </h1>
        </div>
        <div class="flex items-center gap-4 mb-2">
            <div
                class="px-4 py-2 rounded-lg bg-white/5 border border-white/5 flex items-center gap-2"
            >
                <div
                    class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"
                ></div>
                <span
                    class="text-[10px] font-black text-white/40 tracking-widest italic uppercase"
                    >Lattice Sync</span
                >
            </div>
        </div>
    </div>

    <!-- Main Operational Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Dashboard Body -->
        <div class="lg:col-span-2 space-y-8">
            <!-- Portfolio Overview -->
            <div
                class="glass-panel p-12 relative overflow-hidden group border-white/5"
            >
                <div
                    class="absolute -top-24 -right-24 w-80 h-80 bg-cyan-400/5 blur-[100px] rounded-full"
                ></div>

                <div class="relative z-10 flex flex-col items-center py-8">
                    <div
                        class="text-[10px] font-black tracking-widest text-white/20 uppercase mb-8"
                    >
                        Net Protocol Equity
                    </div>
                    <div
                        class="text-8xl font-black italic tracking-tighter tabular-nums mb-6"
                    >
                        842,450<span class="text-2xl text-white/20">.00</span>
                    </div>

                    <div
                        class="flex items-center gap-4 px-6 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/10"
                    >
                        <TrendingUp size={14} class="text-emerald-400" />
                        <span class="text-xs font-black text-emerald-400 italic"
                            >5.2% GROWTH TREND</span
                        >
                    </div>
                </div>

                <div class="mt-12 flex gap-4">
                    {#each actions as action}
                        {@const Icon = action.icon}
                        <button
                            class="flex-1 h-16 rounded-2xl {action.color} {action.border ||
                                ''} {action.textColor} font-black italic tracking-widest text-xs flex items-center justify-center gap-3 hover:scale-[1.02] transition-all"
                        >
                            <Icon size={18} />
                            {action.label}
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Asset Inventory List -->
            <div class="space-y-4">
                <div class="flex items-center justify-between px-2">
                    <div
                        class="text-[10px] font-black tracking-widest text-white/20 uppercase italic"
                    >
                        Primary Inventory
                    </div>
                    <button
                        class="text-[10px] font-black text-cyan-400 uppercase tracking-widest hover:text-white transition-colors"
                        >Manage All</button
                    >
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {#each assets as asset}
                        <div
                            class="glass-panel p-6 flex items-center justify-between border-white/5 hover:border-white/10 transition-all cursor-pointer"
                        >
                            <div class="flex items-center gap-4">
                                <div
                                    class="w-10 h-10 rounded-xl {asset.color}/10 flex items-center justify-center"
                                >
                                    <CreditCard
                                        size={18}
                                        class={asset.color.replace(
                                            "bg-",
                                            "text-",
                                        )}
                                    />
                                </div>
                                <div
                                    class="font-black italic uppercase text-sm tracking-tight"
                                >
                                    {asset.name}
                                </div>
                            </div>
                            <div class="text-right">
                                <div
                                    class="text-sm font-black italic tracking-tighter tabular-nums"
                                >
                                    {asset.amount}
                                </div>
                                <div
                                    class="text-[8px] font-black text-white/20 uppercase"
                                >
                                    {asset.symbol}
                                </div>
                            </div>
                        </div>
                    {/each}
                    <!-- Add Asset Dummy -->
                    <button
                        class="glass-panel p-6 border-dashed border-white/10 flex items-center justify-center gap-3 text-white/20 hover:text-white/40 hover:border-white/20 transition-all"
                    >
                        <Plus size={16} />
                        <span
                            class="text-[10px] font-black tracking-widest uppercase"
                            >Import Shard</span
                        >
                    </button>
                </div>
            </div>
        </div>

        <!-- Sidebar: Intelligence -->
        <div class="space-y-8">
            <div class="glass-panel p-8 space-y-8 border-white/5">
                <div>
                    <div class="flex items-center gap-4 mb-6">
                        <Activity size={16} class="text-cyan-400" />
                        <div
                            class="text-[10px] font-black tracking-widest text-white/40 uppercase"
                        >
                            System Activity
                        </div>
                    </div>

                    <div class="space-y-6">
                        {#each activity as event}
                            <div class="flex justify-between items-start">
                                <div>
                                    <div
                                        class="text-xs font-black italic uppercase text-white/80"
                                    >
                                        {event.label}
                                    </div>
                                    <div
                                        class="text-[8px] font-black text-white/10 italic"
                                    >
                                        {event.time}
                                    </div>
                                </div>
                                <div
                                    class="text-xs font-black italic tabular-nums {event.color}"
                                >
                                    {event.amount}
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <div class="h-px bg-white/5"></div>

                <div>
                    <div
                        class="text-[10px] font-black tracking-widest text-white/20 uppercase mb-4"
                    >
                        Integrity Snapshot
                    </div>
                    <div
                        class="p-6 rounded-2xl bg-white/[0.02] border border-white/5"
                    >
                        <div
                            class="text-[10px] text-white/40 font-bold leading-relaxed italic mb-4"
                        >
                            All resources are currently audited via ZK-Pulse.
                            High-resonance stability detected in Sector 4.
                        </div>
                        <div class="flex items-center gap-2">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-emerald-400"
                            ></div>
                            <span
                                class="text-[8px] font-black text-emerald-400 tracking-widest uppercase"
                                >Verified Secure</span
                            >
                        </div>
                    </div>
                </div>
            </div>

            <button
                class="w-full py-4 rounded-xl bg-white/5 border border-white/5 text-[10px] font-black tracking-widest text-white/30 hover:bg-white/10 hover:text-white transition-all uppercase italic"
            >
                Export Audit Trace
            </button>
        </div>
    </div>
</div>
