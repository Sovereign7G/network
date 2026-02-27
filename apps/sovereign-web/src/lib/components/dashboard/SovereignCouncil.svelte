<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly, scale } from "svelte/transition";
    import {
        Globe,
        Grape,
        Handshake,
        ShieldAlert,
        Landmark,
        Users,
        ChevronRight,
        Activity,
        Gavel,
        BarChart3,
        Clock,
    } from "lucide-svelte";
    import { sovereignStore } from "$lib/stores/sovereign-store.svelte";
    import { celebrationStore } from "$lib/stores/celebration-store.svelte";

    type DigitalNation = {
        id: string;
        name: string;
        type:
            | "CHARTER_CITY"
            | "NETWORK_STATE"
            | "GHOST_JURISDICTION"
            | "SOVEREIGN_DAO";
        citizens: number;
        trustScore: number;
        tags: string[];
        activeTreaties: number;
    };

    const advancedMode = $derived(
        sovereignStore.state.preferences.advancedMode,
    );
    let activeTab = $state("voting");

    $effect(() => {
        if (!advancedMode && activeTab !== "voting") {
            activeTab = "voting";
        }
    });

    let selectedNationId = $state("paragon-01");

    const nations: DigitalNation[] = [
        {
            id: "paragon-01",
            name: "Paragon_Prime",
            type: "NETWORK_STATE",
            citizens: 124500,
            trustScore: 98.4,
            tags: ["High_Tech", "Meritocracy", "AAL4"],
            activeTreaties: 12,
        },
        {
            id: "nagano-02",
            name: "Free_State_Nagano",
            type: "CHARTER_CITY",
            citizens: 82000,
            trustScore: 95.2,
            tags: ["Hardware_Fab", "Zen_Logic", "Local"],
            activeTreaties: 8,
        },
        {
            id: "void-03",
            name: "The_Void_Syndicate",
            type: "SOVEREIGN_DAO",
            citizens: 450000,
            trustScore: 82.1,
            tags: ["Anonymity", "Compute_Heavy", "ZK"],
            activeTreaties: 4,
        },
        {
            id: "solana-04",
            name: "Cyber_Estonia_v3",
            type: "GHOST_JURISDICTION",
            citizens: 12000,
            trustScore: 99.8,
            tags: ["Legacy_Bridge", "e_Residency", "Euro_Legal"],
            activeTreaties: 24,
        },
    ];

    const treaties = [
        {
            id: "tr-001",
            parties: ["Paragon_Prime", "Free_State_Nagano"],
            title: "Silicon_Peace_Accord",
            status: "VERIFIED",
            type: "Mutual_Defense",
            expires: "Never",
        },
        {
            id: "tr-002",
            parties: ["Paragon_Prime", "The_Void_Syndicate"],
            title: "Zero_Knowledge_Trade_Route",
            status: "AUDITING",
            type: "Economic",
            expires: "2027-03-31",
        },
    ];

    const selectedNation = $derived(
        nations.find((n) => n.id === selectedNationId),
    );

    function switchJurisdiction(id: string) {
        selectedNationId = id;
        manifold.recordEvent(
            "JURISDICTION_SHIFT",
            `Workspace ruleset shifted to ${id} governance protocols.`,
        );
    }
</script>

<div
    class="h-full bg-zinc-950/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden flex flex-col shadow-2xl relative group"
>
    <!-- Header -->
    <div class="p-8 border-b border-white/5 bg-white/[0.02] space-y-6">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="p-3 bg-purple-500/20 rounded-2xl text-purple-400">
                    <Landmark size={20} />
                </div>
                <div>
                    <h2
                        class="text-xs font-black uppercase tracking-widest text-white"
                    >
                        Sovereign_Council
                    </h2>
                    <span
                        class="text-[8px] font-black text-white/30 uppercase tracking-widest italic"
                        >Supranational_Digital_Governance</span
                    >
                </div>
            </div>

            <div
                class="flex gap-1.5 p-1 bg-white/5 rounded-xl border border-white/5"
            >
                {#each advancedMode ? ["nations", "treaties", "voting", "history", "analytics"] : ["voting"] as tab}
                    <button
                        onclick={() => (activeTab = tab)}
                        class="px-4 py-1.5 text-[8px] font-black uppercase tracking-widest rounded-lg transition-all {activeTab ===
                        tab
                            ? 'bg-white text-black'
                            : 'text-white/40 hover:text-white'}"
                    >
                        {tab}
                    </button>
                {/each}
            </div>
        </div>
    </div>

    <!-- Active Content Area -->
    <div class="flex-1 overflow-y-auto p-6 no-scrollbar">
        {#if activeTab === "nations"}
            <div class="space-y-6" in:fade>
                <!-- Featured Nation (Current Jurisdiction) -->
                {#if selectedNation}
                    <div
                        class="p-6 bg-gradient-to-br from-purple-500/10 to-transparent rounded-[2.5rem] border border-purple-500/20 relative overflow-hidden group/nation"
                    >
                        <div
                            class="absolute top-0 right-0 p-8 opacity-5 group-hover/nation:opacity-10 transition-opacity"
                        >
                            <Globe size={120} />
                        </div>

                        <div
                            class="relative z-10 flex justify-between items-start"
                        >
                            <div class="space-y-4">
                                <div class="flex items-center gap-3">
                                    <h3
                                        class="text-2xl font-black italic tracking-tighter text-white"
                                    >
                                        {selectedNation.name}
                                    </h3>
                                    <span
                                        class="px-2 py-0.5 bg-purple-500/20 rounded text-[7px] font-black text-purple-400 border border-purple-500/20 uppercase"
                                    >
                                        Active_Jurisdiction
                                    </span>
                                </div>
                                <div class="flex gap-4">
                                    <div class="flex flex-col">
                                        <span
                                            class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                            >Citizens</span
                                        >
                                        <span
                                            class="text-xs font-black text-white"
                                            >{(
                                                selectedNation.citizens / 1000
                                            ).toFixed(1)}k</span
                                        >
                                    </div>
                                    <div class="flex flex-col">
                                        <span
                                            class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                                            >Trust_Rating</span
                                        >
                                        <span
                                            class="text-xs font-black text-emerald-400"
                                            >{selectedNation.trustScore}%</span
                                        >
                                    </div>
                                </div>
                                <div class="flex gap-2">
                                    {#each selectedNation.tags as tag}
                                        <span
                                            class="text-[7px] font-black text-white/40 uppercase px-2 py-1 bg-white/5 rounded-lg border border-white/5"
                                            >{tag}</span
                                        >
                                    {/each}
                                </div>
                            </div>
                            <div class="text-right">
                                <Activity
                                    size={24}
                                    class="text-purple-400 ml-auto mb-2 animate-pulse"
                                />
                                <span
                                    class="text-[8px] font-black text-purple-400/40 uppercase tracking-widest block"
                                    >Neural_Consensus: HIGH</span
                                >
                            </div>
                        </div>

                        <button
                            class="w-full mt-8 py-3 bg-white text-black text-[9px] font-black uppercase tracking-widest rounded-2xl hover:scale-[1.02] transition-all shadow-xl shadow-white/5"
                        >
                            Open_Constitutional_Panel
                        </button>
                    </div>
                {/if}

                <!-- Other Societies -->
                <div class="space-y-3">
                    <h4
                        class="text-[9px] font-black text-white/20 uppercase tracking-widest px-2"
                    >
                        Known_Parallel_Societies
                    </h4>
                    <div class="grid grid-cols-1 gap-3">
                        {#each nations.filter((n) => n.id !== selectedNationId) as nation}
                            <button
                                onclick={() => switchJurisdiction(nation.id)}
                                class="flex items-center justify-between p-5 bg-white/[0.03] border border-white/5 rounded-3xl hover:border-white/20 transition-all group/item text-left"
                            >
                                <div class="flex items-center gap-4">
                                    <div
                                        class="w-10 h-10 rounded-2xl bg-white/5 flex items-center justify-center text-white/20 group-hover/item:text-white transition-colors"
                                    >
                                        <Users size={20} />
                                    </div>
                                    <div>
                                        <h5
                                            class="text-xs font-black text-white uppercase"
                                        >
                                            {nation.name}
                                        </h5>
                                        <span
                                            class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                                            >{nation.type}</span
                                        >
                                    </div>
                                </div>
                                <div class="flex items-center gap-4">
                                    <div class="text-right">
                                        <span
                                            class="text-[8px] font-black text-emerald-400/60 block"
                                            >{nation.trustScore}%</span
                                        >
                                        <span
                                            class="text-[7px] font-black text-white/10 uppercase italic"
                                            >Stability</span
                                        >
                                    </div>
                                    <ChevronRight
                                        size={14}
                                        class="text-white/10 group-hover/item:text-white transition-colors"
                                    />
                                </div>
                            </button>
                        {/each}
                    </div>
                </div>
            </div>
        {:else if activeTab === "treaties"}
            <div class="space-y-6" in:fly={{ y: 20 }}>
                <div class="flex justify-between items-center px-1">
                    <h3
                        class="text-[10px] font-black text-white/20 uppercase tracking-[0.2em]"
                    >
                        Diplomatic_Manifest
                    </h3>
                    <button
                        class="text-purple-400 text-[8px] font-black uppercase hover:underline"
                        >+ Propose Treaty</button
                    >
                </div>

                <div class="space-y-4">
                    {#each treaties as treaty}
                        <div
                            class="p-5 bg-white/[0.03] border border-white/5 rounded-3xl space-y-4 group/treaty"
                        >
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-3">
                                    <div
                                        class="p-2.5 bg-emerald-400/10 rounded-xl text-emerald-400"
                                    >
                                        <Handshake size={16} />
                                    </div>
                                    <div>
                                        <h5
                                            class="text-xs font-black text-white uppercase"
                                        >
                                            {treaty.title}
                                        </h5>
                                        <div class="flex items-center gap-2">
                                            <span
                                                class="text-[7px] font-black text-white/30 uppercase"
                                                >{treaty.parties[0]}</span
                                            >
                                            <span
                                                class="text-white/10 text-[10px]"
                                                >↔</span
                                            >
                                            <span
                                                class="text-[7px] font-black text-white/30 uppercase"
                                                >{treaty.parties[1]}</span
                                            >
                                        </div>
                                    </div>
                                </div>
                                <span
                                    class="text-[8px] font-black text-emerald-400 uppercase tracking-widest border border-emerald-400/20 px-2 py-1 rounded bg-emerald-400/5"
                                >
                                    {treaty.status}
                                </span>
                            </div>

                            <div class="grid grid-cols-2 gap-4 pt-2">
                                <div class="flex flex-col gap-1">
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest italic"
                                        >Treaty_Type</span
                                    >
                                    <span
                                        class="text-[10px] font-bold text-white/60"
                                        >{treaty.type}</span
                                    >
                                </div>
                                <div class="flex flex-col gap-1">
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase tracking-widest italic"
                                        >Persistence</span
                                    >
                                    <span
                                        class="text-[10px] font-bold text-white/60"
                                        >{treaty.expires}</span
                                    >
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>

                <div
                    class="p-6 border-t border-white/5 bg-black/40 rounded-3xl mt-8 flex items-center justify-between"
                >
                    <div class="flex items-center gap-3">
                        <ShieldAlert size={14} class="text-amber-400" />
                        <span
                            class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                            >AAL4 Integrity verified via Shard-Mesh</span
                        >
                    </div>
                    <button
                        class="text-[8px] font-black text-cyan-400 uppercase tracking-widest"
                        >Audit_Log</button
                    >
                </div>
            </div>
        {:else if activeTab === "voting"}
            <div class="h-full flex flex-col space-y-8 py-8" in:scale>
                <div class="text-center space-y-3">
                    <div
                        class="w-16 h-16 bg-purple-500/10 rounded-3xl border border-purple-500/30 flex items-center justify-center text-purple-400 mx-auto"
                    >
                        <Grape size={32} />
                    </div>
                    <h3
                        class="text-xl font-black italic tracking-tighter uppercase text-white"
                    >
                        Fractal_Democracy
                    </h3>
                    <p
                        class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em] max-w-xs mx-auto"
                    >
                        Quadratic voting weight across sharded jurisdictions.
                    </p>
                </div>

                <div class="space-y-4 px-4 flex-1">
                    <div
                        class="p-5 bg-white/5 border border-white/5 rounded-3xl space-y-4"
                    >
                        <div
                            class="flex justify-between items-center text-[8px] font-black uppercase tracking-widest"
                        >
                            <span class="text-white/40"
                                >Nagano_Fab_Expension</span
                            >
                            <span class="text-emerald-400">92% Yes</span>
                        </div>
                        <div
                            class="h-2 bg-white/10 rounded-full overflow-hidden flex"
                        >
                            <div
                                class="h-full bg-emerald-400 w-[92%]"
                                style="box-shadow: 0 0 15px rgba(16,185,129,0.3)"
                            ></div>
                        </div>
                        <div
                            class="flex justify-between text-[7px] font-black text-white/20 uppercase italic"
                        >
                            <span>Cost: 5,000 RES</span>
                            <span>Time Left: 2h 14m</span>
                        </div>
                    </div>

                    <div
                        class="p-5 bg-white/5 border border-white/5 rounded-3xl space-y-4 opacity-60"
                    >
                        <div
                            class="flex justify-between items-center text-[8px] font-black uppercase tracking-widest"
                        >
                            <span class="text-white/40"
                                >Euro_Node_Reciprocity</span
                            >
                            <span class="text-amber-400">45% Yes</span>
                        </div>
                        <div
                            class="h-2 bg-white/10 rounded-full overflow-hidden"
                        >
                            <div class="h-full bg-amber-400 w-[45%]"></div>
                        </div>
                        <div
                            class="flex justify-between text-[7px] font-black text-white/20 uppercase italic"
                        >
                            <span>Cost: 1,200 AGE</span>
                            <span>Time Left: 14h 05m</span>
                        </div>
                    </div>
                </div>

                <button
                    onclick={() => {
                        if (sovereignStore.markEventComplete("firstVote")) {
                            celebrationStore.trigger("vote");
                        }
                    }}
                    class="w-full py-4 bg-purple-500 text-white text-[10px] font-black uppercase tracking-widest rounded-2xl hover:scale-105 transition-all shadow-xl shadow-purple-500/20"
                >
                    Exercise_Voting_Sovereignty
                </button>
            </div>
        {:else if activeTab === "history"}
            <div class="space-y-6" in:fade>
                <h3
                    class="text-[10px] font-black text-white/20 uppercase tracking-[0.2em]"
                >
                    Governance_Persistence_Log
                </h3>
                <div class="space-y-3">
                    {#each [1, 2, 3, 4] as i}
                        <div
                            class="p-4 bg-white/5 border border-white/5 rounded-2xl flex items-center justify-between"
                        >
                            <div class="flex items-center gap-3">
                                <Clock size={14} class="text-white/20" />
                                <div>
                                    <h5
                                        class="text-[10px] font-bold text-white"
                                    >
                                        Proposal_{1024 - i}
                                    </h5>
                                    <span class="text-[8px] text-white/40"
                                        >Executed 2d ago</span
                                    >
                                </div>
                            </div>
                            <span class="text-[8px] text-emerald-400 font-black"
                                >PASSED</span
                            >
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeTab === "analytics"}
            <div class="space-y-8" in:fade>
                <div class="grid grid-cols-2 gap-4">
                    <div
                        class="p-6 bg-white/5 border border-white/5 rounded-3xl"
                    >
                        <BarChart3 size={20} class="text-purple-400 mb-4" />
                        <span
                            class="text-[8px] font-black text-white/20 uppercase"
                            >Quorum_Average</span
                        >
                        <div class="text-xl font-black italic">84.2%</div>
                    </div>
                    <div
                        class="p-6 bg-white/5 border border-white/5 rounded-3xl"
                    >
                        <Activity size={20} class="text-emerald-400 mb-4" />
                        <span
                            class="text-[8px] font-black text-white/20 uppercase"
                            >Network_Participation</span
                        >
                        <div class="text-xl font-black italic">12k+ Voters</div>
                    </div>
                </div>
                <div
                    class="p-8 bg-purple-500/5 border border-purple-500/20 rounded-[2.5rem] space-y-4"
                >
                    <h4
                        class="text-[10px] font-black uppercase tracking-widest text-purple-400"
                    >
                        Delegate_Analytics
                    </h4>
                    <p
                        class="text-[9px] text-white/40 leading-relaxed uppercase"
                    >
                        Analyzing representative alignment with your stored
                        values in the Sovereign Hearth.
                    </p>
                    <div class="h-1 bg-white/5 rounded-full overflow-hidden">
                        <div class="h-full bg-purple-500 w-[65%]"></div>
                    </div>
                    <div
                        class="flex justify-between text-[8px] font-black text-white/20 uppercase"
                    >
                        <span>Alignment</span>
                        <span>65% Match</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <!-- Footer: System Stats -->
    <div
        class="p-6 border-t border-white/5 bg-black/40 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <Gavel size={14} class="text-purple-400" />
            <span
                class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                >Autonomous_Judge: ACTIVE</span
            >
        </div>
        <div
            class="flex items-center gap-4 text-white/20 text-[9px] font-black uppercase italic"
        >
            <span>Global_Nodes: 4,102</span>
            <div class="h-4 w-[1px] bg-white/10"></div>
            <span>Law_Entropy: 0.002%</span>
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
</style>
