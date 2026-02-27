<script lang="ts">
    import {
        Search,
        ShoppingBag,
        Zap,
        CheckCircle2,
        XCircle,
        ArrowUpRight,
        Target,
        ShieldCheck,
        Activity,
        X,
        LayoutGrid,
        List,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
    import SovereignAnnotation from "./SovereignAnnotation.svelte";
    import { spawnSparkles } from "$lib/utils/SparkleEmitter";

    let showBanknote = $state(false);

    let activeFilter = $state("ALL MISSIONS");
    let viewMode = $state("GRID"); // GRID or DATA
    const filters = ["ALL MISSIONS", "ESSENTIAL", "COMMUNITY", "URGENT"];

    const listings = [
        {
            id: "0x1",
            title: "NEIGHBORHOOD PATROL",
            location: "SHACKLETON",
            reward: "45.0 Credits",
            icon: ShieldCheck,
            status: "VERIFIED",
        },
        {
            id: "0x2",
            title: "RELAY MAINTENANCE",
            location: "CORE MESH",
            reward: "125.5 Credits",
            icon: Activity,
            status: "URGENT",
        },
        {
            id: "0x3",
            title: "ENVIRONMENTAL SYNC",
            location: "CITY HABITAT",
            reward: "12.0 Credits",
            icon: ShieldCheck,
            status: "VERIFIED",
        },
    ];

    /** @type {any} */
    let selectedListing = $state(null);

    let initiationError = $state("");
    let isProcessing = $state(false);

    function handleInitiateMission() {
        initiationError = "";
        isProcessing = true;

        // 🧩 TEMPORAL BRIDGE: [State: INITIATING]
        // Simulate cryptographic handshake delay for interaction context
        setTimeout(() => {
            isProcessing = false;
            const isSuccess = Math.random() > 0.15; // 85% success rate for simulation

            if (isSuccess) {
                showBanknote = true;
                // Trigger sparkles at the middle of the button
                const btn = document.getElementById("initiate_btn");
                if (btn) {
                    const rect = btn.getBoundingClientRect();
                    spawnSparkles(
                        rect.left + rect.width / 2,
                        rect.top + rect.height / 2,
                        "#fbbf24",
                    );
                }
                setTimeout(() => {
                    showBanknote = false;
                    selectedListing = null;
                }, 1200);
            } else {
                // 🚨 ERROR-PATH PRIORITY: [State: PROTOCOL_BREACH]
                initiationError = "RESONANCE FLUX DETECTED. RETRY SYNC.";
                setTimeout(() => {
                    initiationError = "";
                }, 3000);
            }
        }, 1200);
    }
</script>

<div
    class="px-8 py-12 max-w-7xl mx-auto transition-all duration-700 {selectedListing
        ? 'opacity-30 blur-sm overflow-hidden scale-[0.98]'
        : 'opacity-100 blur-0 scale-100'}"
    in:fade
>
    <!-- 👁️ ESSENTIAL ACTION: Background dimmed to focus on selectedListing -->
    <!-- Briefing Header -->
    <div
        class="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-8"
    >
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-amber-400 uppercase mb-4"
            >
                Agora Bazaar // L0
            </div>
            <h1 class="text-6xl font-black italic uppercase tracking-tighter">
                Mission <span class="text-amber-400">Market</span>
            </h1>
        </div>

        <div class="flex items-center gap-4">
            <div class="relative group">
                <Search
                    class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20 group-focus-within:text-amber-400 transition-colors"
                />
                <input
                    type="text"
                    placeholder="Trace mission..."
                    class="w-64 h-14 pl-12 pr-4 rounded-2xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-amber-400/30 transition-all placeholder:text-white/10"
                />
            </div>
            <button
                class="premium-scale premium-shimmer h-14 px-8 rounded-2xl bg-amber-400 text-black text-[10px] font-black tracking-widest uppercase transition-all flex items-center gap-2"
            >
                <Zap size={16} /> LIST ASSET
            </button>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-12">
        <!-- Sidebar: Status -->
        <div id="market_intel_sidebar" class="space-y-8">
            <div class="glass-panel p-8 space-y-8 border-white/5">
                <div>
                    <div
                        class="text-[10px] font-black text-white/20 uppercase tracking-widest mb-6 px-1 italic"
                    >
                        Network Load
                    </div>
                    <div class="space-y-6">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-bold text-white/40"
                                >Active Nodes</span
                            >
                            <span
                                class="text-sm font-black text-amber-400 tabular-nums"
                                >0014</span
                            >
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-bold text-white/40"
                                >Peak Traffic</span
                            >
                            <span
                                class="text-sm font-black text-amber-400 tabular-nums"
                                >42.8%</span
                            >
                        </div>
                    </div>
                </div>

                <div class="h-px bg-white/5"></div>

                <div>
                    <div
                        class="text-[10px] font-black text-white/20 uppercase tracking-widest mb-6 px-1 italic"
                    >
                        Mission Intel
                    </div>
                    <div
                        class="p-6 rounded-2xl bg-white/[0.02] border border-white/5 premium-shimmer"
                    >
                        <div
                            class="text-[10px] text-white/40 font-bold leading-relaxed italic mb-4"
                        >
                            Current mission saturation at 12%. High demand
                            detected for Sector 4 defense nodes.
                        </div>
                        <div class="flex items-center gap-3">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-emerald-400 radiant-aura"
                            ></div>
                            <span
                                class="text-[8px] font-black text-emerald-400 tracking-widest uppercase"
                                >Resonance Stable</span
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Marketplace Content -->
        <div class="lg:col-span-3 space-y-12">
            <!-- Featured Mission Card (Bento Priority) -->
            <div
                id="featured_mission"
                class="liquid-glass p-12 relative overflow-hidden group border-amber-500/20"
            >
                <div
                    class="absolute -top-32 -right-32 w-96 h-96 bg-amber-400/10 blur-[120px] rounded-full"
                ></div>

                <div
                    class="relative z-10 flex flex-col md:flex-row items-center gap-12"
                >
                    <div class="flex-1">
                        <div
                            class="text-[10px] font-black tracking-[0.4em] text-amber-400 uppercase mb-4"
                        >
                            Priority Mission
                        </div>
                        <h2
                            class="text-4xl font-black italic uppercase tracking-tighter mb-4 leading-none"
                        >
                            COMMUNITY RELIEF // SHACKLETON PH-1
                        </h2>
                        <p
                            class="text-white/40 font-bold leading-relaxed max-w-xl italic"
                        >
                            Allocation of resources to Sector 4 expansion to
                            support 5,000 incoming citizens via Sophia-directed
                            grounding.
                        </p>
                    </div>
                    <button
                        class="premium-scale premium-shimmer h-16 px-12 rounded-2xl bg-amber-400 text-black font-black italic tracking-widest flex items-center justify-center gap-3 transition-all"
                    >
                        JOIN MISSION
                    </button>
                </div>
            </div>

            <!-- Category Chips and View Toggle -->
            <div
                class="flex justify-between items-center bg-white/5 p-2 rounded-2xl border border-white/5"
            >
                <div class="flex gap-2">
                    {#each filters as filter}
                        <button
                            onclick={() => (activeFilter = filter)}
                            class="px-5 py-2 rounded-xl text-[10px] font-black tracking-widest transition-all {activeFilter ===
                            filter
                                ? 'bg-amber-400 text-black shadow-[0_0_20px_rgba(251,191,36,0.2)]'
                                : 'text-white/40 hover:text-white'}"
                        >
                            {filter}
                        </button>
                    {/each}
                </div>

                <div class="flex bg-black/40 p-1 rounded-xl gap-1">
                    <button
                        onclick={() => (viewMode = "GRID")}
                        class="px-4 py-2 rounded-lg transition-all {viewMode ===
                        'GRID'
                            ? 'bg-white/10 text-white'
                            : 'text-white/20 hover:text-white/40'}"
                    >
                        <LayoutGrid size={16} />
                    </button>
                    <button
                        onclick={() => (viewMode = "DATA")}
                        class="px-4 py-2 rounded-lg transition-all {viewMode ===
                        'DATA'
                            ? 'bg-white/10 text-white'
                            : 'text-white/20 hover:text-white/40'}"
                    >
                        <List size={16} />
                    </button>
                </div>
            </div>

            {#if viewMode === "GRID"}
                <!-- Listings Feed (Bento Grid) -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {#each listings as listing, i}
                        {@const Icon = listing.icon}
                        <div
                            role="button"
                            tabindex="0"
                            onclick={() => (selectedListing = listing)}
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" &&
                                (selectedListing = listing)}
                            class="premium-scale liquid-glass p-8 flex flex-col justify-between min-h-[280px] hover:border-amber-400/40 transition-all cursor-pointer group"
                            in:fly={{ y: 20, delay: i * 100 }}
                        >
                            <div>
                                <div
                                    class="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform mb-8"
                                >
                                    <Icon size={24} class="text-amber-400" />
                                </div>
                                <h3
                                    class="text-2xl font-black italic uppercase tracking-tighter group-hover:text-amber-400 transition-colors mb-2"
                                >
                                    {listing.title}
                                </h3>
                                <div
                                    class="text-[8px] font-black text-white/30 tracking-widest uppercase"
                                >
                                    {listing.location} // {listing.status}
                                </div>
                            </div>

                            <div class="flex justify-between items-end mt-8">
                                <div>
                                    <div
                                        class="text-2xl font-black italic tabular-nums text-white premium-gradient-text"
                                    >
                                        {listing.reward}
                                    </div>
                                    <div
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                    >
                                        Residue Estimate
                                    </div>
                                </div>
                                <button
                                    class="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center text-white/40 group-hover:bg-amber-400 group-hover:text-black group-hover:border-amber-400 transition-all"
                                >
                                    <ArrowUpRight size={16} />
                                </button>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <!-- Institutional Data View (Bloomberg Pattern) -->
                <div class="liquid-glass overflow-hidden border-white/5">
                    <table class="hardened-table">
                        <thead>
                            <tr>
                                <th>Mission Stream</th>
                                <th>Status</th>
                                <th>Jurisdiction</th>
                                <th>Reward Flux</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each listings as listing}
                                <tr
                                    class="cursor-pointer group"
                                    onclick={() => (selectedListing = listing)}
                                >
                                    <td
                                        class="font-black italic text-sm tracking-tight"
                                        >{listing.title}</td
                                    >
                                    <td>
                                        <span
                                            class="px-2 py-0.5 rounded-sm bg-amber-400/10 text-amber-400 text-[8px] font-black uppercase"
                                        >
                                            {listing.status}
                                        </span>
                                    </td>
                                    <td
                                        class="text-white/40 text-[10px] font-bold"
                                        >{listing.location}</td
                                    >
                                    <td
                                        class="font-black italic text-amber-400 tabular-nums"
                                        >{listing.reward}</td
                                    >
                                    <td class="text-right">
                                        <ArrowUpRight
                                            size={14}
                                            class="inline text-white/10 group-hover:text-amber-400 transition-colors"
                                        />
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
    </div>
</div>

<!-- Simplified Asset Detail Modal -->
{#if selectedListing}
    <div
        class="fixed inset-0 z-[2000] flex items-center justify-center p-8 bg-black/80 backdrop-blur-xl"
        transition:fade
    >
        <div
            class="glass-panel p-16 max-w-2xl w-full relative overflow-hidden border-white/10"
            in:fly={{ y: 50 }}
        >
            <button
                onclick={() => (selectedListing = null)}
                class="absolute top-8 right-8 text-white/20 hover:text-white transition-colors"
            >
                <X size={24} />
            </button>

            <div
                class="text-[10px] font-black tracking-widest text-amber-400 uppercase mb-4"
            >
                Mission Detail // 0x5C
            </div>
            <h2
                class="text-5xl font-black italic uppercase tracking-tighter mb-8 leading-none"
            >
                {selectedListing.title}
            </h2>

            <div class="grid grid-cols-2 gap-8 mb-12">
                <div
                    class="p-6 rounded-2xl bg-white/[0.02] border border-white/5"
                >
                    <div
                        class="text-[8px] font-black text-white/20 uppercase mb-2"
                    >
                        Grounding Factor
                    </div>
                    <div
                        class="text-2xl font-black italic text-emerald-400 tabular-nums"
                    >
                        0.84 PASS
                    </div>
                </div>
                <div
                    class="p-6 rounded-2xl bg-white/[0.02] border border-white/5"
                >
                    <div
                        class="text-[8px] font-black text-white/20 uppercase mb-2"
                    >
                        Network Yield
                    </div>
                    <div
                        class="text-2xl font-black italic text-amber-400 tabular-nums"
                    >
                        12.5%
                    </div>
                </div>
            </div>

            {#if initiationError}
                <div
                    class="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 text-[10px] font-black tracking-widest text-center animate-pulse"
                >
                    🚨 {initiationError}
                </div>
            {/if}

            <button
                id="initiate_btn"
                onclick={handleInitiateMission}
                disabled={isProcessing}
                class="w-full h-16 rounded-2xl {isProcessing
                    ? 'bg-white/10 text-white/40'
                    : 'bg-amber-400 text-black shadow-[0_0_40px_rgba(251,191,36,0.2)]'} font-black italic tracking-widest flex items-center justify-center gap-3 hover:scale-[1.02] transition-all"
            >
                {#if isProcessing}
                    <div
                        class="w-4 h-4 border-2 border-amber-400 border-t-transparent rounded-full animate-spin"
                    ></div>
                    POLLING MESH...
                {:else}
                    INITIATE MISSION // {selectedListing.id}
                {/if}
            </button>
        </div>
    </div>
{/if}

{#if showBanknote}
    <div
        class="fixed inset-0 z-[3000] flex items-center justify-center pointer-events-none"
    >
        <div class="banknote-flow banknote-slide-in">
            {selectedListing?.reward}
        </div>
    </div>
{/if}

<SovereignAnnotation
    targetId="market_intel_sidebar"
    text="Intel stream optimized for Sector 4 expansion."
    type="strategic"
/>
<SovereignAnnotation
    targetId="featured_mission"
    text="Priority mission requires Sophia-level grounding."
    type="tactical"
/>
```
