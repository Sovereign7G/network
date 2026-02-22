<script lang="ts">
    import {
        Camera,
        Shield,
        Layers,
        Music,
        Verified,
        AlertCircle,
        ChevronRight,
        Play,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    let activeProject = $state({
        title: "Original Myth: The First Shard",
        status: "Production Mesh Active",
        meshResilience: 0.884,
        ritualIndex: 0.942,
        vocalStability: 0.781,
        narrativeImprint: 0.915,
    });

    const protocols = [
        {
            id: "HOLLY-1",
            name: "Production Mesh",
            value: activeProject.meshResilience,
            status: "STABLE",
        },
        {
            id: "CINEMA-1",
            name: "Ritual Integrity",
            value: activeProject.ritualIndex,
            status: "VERIFIED",
        },
        {
            id: "VOX-1",
            name: "Vocal Lineage",
            value: activeProject.vocalStability,
            status: "PROTECTED",
        },
        {
            id: "DRAMA-1",
            name: "Narrative Sovereign",
            value: activeProject.narrativeImprint,
            status: "SIGNED",
        },
    ];
</script>

<div class="grid grid-cols-1 lg:grid-cols-12 gap-8" in:fade>
    <!-- Left Column: Mesh Status -->
    <div class="lg:col-span-8 space-y-8">
        <section class="glass-panel p-8 relative overflow-hidden">
            <div
                class="absolute -top-24 -right-24 w-64 h-64 bg-neon-amber/5 rounded-full blur-3xl"
            ></div>

            <div class="flex justify-between items-start mb-12">
                <div>
                    <h2
                        class="text-3xl font-black italic tracking-tighter uppercase mb-2"
                    >
                        SOVEREIGN STUDIO MESH
                    </h2>
                    <p
                        class="text-xs mono-font text-neon-amber tracking-widest font-bold"
                    >
                        HOLLY-1 // CINEMA-1 PROTOCOLS ACTIVE
                    </p>
                </div>
                <div
                    class="p-3 bg-neon-amber/10 rounded-xl border border-neon-amber/20"
                >
                    <Camera size={24} class="text-neon-amber" />
                </div>
            </div>

            <!-- Active Project Card -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8 backdrop-blur-md"
            >
                <div class="flex justify-between items-center mb-8">
                    <div>
                        <div
                            class="text-[10px] mono-font opacity-40 uppercase tracking-[0.2em] mb-1"
                        >
                            Production Target
                        </div>
                        <h3 class="text-2xl font-black italic tracking-tight">
                            {activeProject.title}
                        </h3>
                    </div>
                    <div class="flex items-center space-x-2 text-green-400">
                        <div
                            class="w-2 h-2 rounded-full bg-green-400 animate-pulse"
                        ></div>
                        <span
                            class="text-[10px] font-black mono-font uppercase tracking-widest"
                            >{activeProject.status}</span
                        >
                    </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                    {#each protocols as protocol}
                        <div class="space-y-3">
                            <div class="flex justify-between items-end">
                                <span
                                    class="text-[8px] font-black mono-font opacity-50 uppercase tracking-widest"
                                    >{protocol.id}</span
                                >
                                <span class="text-xs font-black text-neon-amber"
                                    >{(protocol.value * 100).toFixed(1)}%</span
                                >
                            </div>
                            <div
                                class="h-1 w-full bg-white/5 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-neon-amber shadow-[0_0_10px_#ffaa00]"
                                    style="width: {protocol.value * 100}%"
                                ></div>
                            </div>
                            <div
                                class="text-[9px] font-bold opacity-30 uppercase tracking-tighter"
                            >
                                {protocol.name}
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- Narrative Shards -->
            <div class="space-y-4">
                <h4
                    class="text-[10px] font-black mono-font opacity-40 uppercase tracking-[0.3em] mb-4"
                >
                    NARRATIVE CONSENSUS SHARDS
                </h4>
                {#each [1, 2, 3] as shard}
                    <div
                        class="flex items-center justify-between p-4 bg-white/3 rounded-xl border border-white/5 hover:border-neon-amber/20 transition-all cursor-pointer group"
                    >
                        <div class="flex items-center space-x-4">
                            <div
                                class="w-10 h-10 rounded-lg flex items-center justify-center bg-white/5 text-white/40 group-hover:text-neon-amber transition-colors"
                            >
                                <Play size={16} />
                            </div>
                            <div>
                                <p class="text-sm font-bold">
                                    Script Cluster #{shard * 1024}
                                </p>
                                <p
                                    class="text-[9px] mono-font opacity-30 uppercase tracking-widest"
                                >
                                    Verified by Sovereign Historian
                                </p>
                            </div>
                        </div>
                        <ChevronRight
                            size={16}
                            class="opacity-20 group-hover:opacity-100 group-hover:translate-x-1 transition-all"
                        />
                    </div>
                {/each}
            </div>
        </section>
    </div>

    <!-- Right Column: Infrastructure Details -->
    <div class="lg:col-span-4 space-y-8">
        <aside class="glass-panel p-8 card-glow">
            <h3
                class="text-xl font-black italic uppercase tracking-tighter mb-8 text-neon-amber"
            >
                PRODUCTION NODES
            </h3>
            <div class="space-y-6 mb-12">
                {#each ["LA-Base-Shard", "London-VFX-Hub", "Tokyo-Studio-A", "Virtual-Render-Mesh 04"] as node}
                    <div
                        class="flex items-center justify-between border-b border-white/5 pb-3 last:border-0"
                    >
                        <div class="flex items-center space-x-3">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-neon-amber/50"
                            ></div>
                            <span class="text-xs font-bold text-white/70"
                                >{node}</span
                            >
                        </div>
                        <span class="text-[10px] mono-font text-green-400"
                            >ONLINE</span
                        >
                    </div>
                {/each}
            </div>

            <button
                class="w-full bg-neon-amber text-black font-black py-5 italic tracking-tighter uppercase rounded-xl hover:scale-[1.02] active:scale-[0.98] transition-all shadow-[0_0_20px_rgba(255,170,0,0.3)]"
            >
                DEPLOY PRODUCTION MESH
            </button>
        </aside>

        <aside class="glass-panel p-8 bg-neon-amber/5 border-neon-amber/20">
            <div class="flex items-center space-x-3 mb-6">
                <Shield size={20} class="text-neon-amber" />
                <h3 class="font-black italic uppercase text-sm tracking-widest">
                    Sovereign Protection
                </h3>
            </div>
            <p class="text-xs text-white/60 leading-relaxed mb-8">
                Your vocal lineage is protected under the VOX-1 protocol. No
                synthetic replicas can be generated without your VoidAuth
                signature.
            </p>
            <div
                class="px-4 py-3 bg-black/40 rounded-lg border border-neon-amber/30 text-[9px] mono-font text-neon-amber font-bold flex justify-between"
            >
                <span>V-SIGNATURE VALID</span>
                <span>0x8A...2F9</span>
            </div>
        </aside>
    </div>
</div>

<style>
    .neon-amber {
        color: var(--color-neon-amber);
    }
</style>
