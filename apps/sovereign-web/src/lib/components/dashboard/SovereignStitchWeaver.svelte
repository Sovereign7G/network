<script lang="ts">
    import {
        Sparkles,
        Database,
        Layout,
        Lock,
        Code2,
        Play,
    } from "lucide-svelte";
    import { fade, slide, scale } from "svelte/transition";

    let intentQuery = $state("");
    let status = $state("IDLE"); // IDLE, WEAVING_LAYOUT, STITCHING_DATA, SECURING_AUTH, ACTIVE
    let logs = $state<string[]>([]);
    let generatedNodes = $state<{ id: number; type: string; color: string }[]>(
        [],
    );

    function startWeaving() {
        if (!intentQuery) return;
        status = "WEAVING_LAYOUT";
        logs = [
            "Initializing AntiGravity Space...",
            "Transcribing Intent into Layout Topology...",
        ];

        setTimeout(() => {
            status = "STITCHING_DATA";
            logs.push("Layout materialized.");
            logs.push("Connecting to Stitch Backend...");
            logs.push("Provisioning Serverless Data Matrix...");
        }, 2000);

        setTimeout(() => {
            status = "SECURING_AUTH";
            logs.push("Data flowing... 100%");
            logs.push("Engaging Stitch Auth Layer...");
        }, 4000);

        setTimeout(() => {
            status = "ACTIVE";
            logs.push("Weave Complete. Dashboard Live.");
            generatedNodes = [
                {
                    id: 1,
                    type: "Data Grid",
                    color: "bg-cyan-500/20 text-cyan-400 border-cyan-500/30",
                },
                {
                    id: 2,
                    type: "Auth Gate",
                    color: "bg-purple-500/20 text-purple-400 border-purple-500/30",
                },
                {
                    id: 3,
                    type: "Metrics",
                    color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
                },
            ];
        }, 6000);
    }
</script>

<div
    class="h-full bg-[#030509] rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 flex flex-col gap-6 shadow-[0_0_50px_rgba(34,211,238,0.05)] relative overflow-hidden"
>
    <!-- Background Decor -->
    <div class="absolute inset-0 pointer-events-none opacity-20">
        <div
            class="absolute top-0 right-0 w-64 h-64 bg-cyan-500/30 rounded-full blur-[100px]"
        ></div>
        <div
            class="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/20 rounded-full blur-[100px]"
        ></div>
    </div>

    <!-- Header -->
    <div class="flex items-center justify-between relative z-10">
        <div class="flex items-center gap-3">
            <div class="p-2 bg-white/5 rounded-xl border border-white/10">
                <Code2 size={20} class="text-cyan-400" />
            </div>
            <div>
                <h3
                    class="text-[12px] font-black uppercase tracking-[0.2em] text-white"
                >
                    Stitch_Weaver
                </h3>
                <span
                    class="text-[8px] font-black uppercase text-cyan-400/60 tracking-widest"
                >
                    AntiGravity Intention Matrix
                </span>
            </div>
        </div>
        <div class="flex gap-2">
            <div
                class="w-2 h-2 rounded-full {status === 'ACTIVE'
                    ? 'bg-emerald-400 animate-pulse'
                    : 'bg-white/20'}"
            ></div>
        </div>
    </div>

    <!-- Interface Prompt -->
    {#if status === "IDLE"}
        <div
            class="flex-1 flex flex-col justify-center items-center gap-6 relative z-10"
            in:fade
        >
            <div class="w-full max-w-md">
                <label
                    for="intent-query"
                    class="block text-[10px] font-black text-white/40 uppercase tracking-widest mb-3 pl-2"
                >
                    Define Interface Parameters
                </label>
                <div class="relative group">
                    <Sparkles
                        size={16}
                        class="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-400 opacity-50 group-focus-within:opacity-100 transition-opacity"
                    />
                    <input
                        id="intent-query"
                        type="text"
                        bind:value={intentQuery}
                        placeholder="e.g. Generate a secure crypto treasury dashboard..."
                        class="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-cyan-400/50 outline-none rounded-2xl py-4 pl-12 pr-4 text-sm font-medium text-white placeholder:text-white/20 transition-all"
                        onkeydown={(e: KeyboardEvent) => e.key === "Enter" && startWeaving()}
                    />
                    <button
                        onclick={startWeaving}
                        class="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-cyan-400 text-black rounded-xl hover:scale-105 active:scale-95 transition-all"
                    >
                        <Play size={14} class="fill-current" />
                    </button>
                </div>
            </div>

            <div
                class="flex gap-4 opacity-50 text-[10px] font-black uppercase tracking-widest mt-4"
            >
                <span class="flex items-center gap-1"
                    ><Layout size={12} /> Zero Code</span
                >
                <span class="flex items-center gap-1"
                    ><Database size={12} /> Live Stitch Data</span
                >
                <span class="flex items-center gap-1"
                    ><Lock size={12} /> Auto-Auth</span
                >
            </div>
        </div>
    {:else}
        <!-- Weaving State -->
        <div
            class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10"
            in:fade
        >
            <!-- Terminal Output -->
            <div
                class="bg-black/40 rounded-3xl border border-white/5 p-6 flex flex-col font-mono text-xs overflow-hidden relative"
            >
                <div
                    class="flex items-center justify-between mb-4 border-b border-white/10 pb-2"
                >
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Compiler Logs</span
                    >
                    {#if status !== "ACTIVE"}
                        <span class="text-xs animate-spin-slow">⏳</span>
                    {/if}
                </div>
                <div
                    class="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar flex flex-col justify-end"
                >
                    {#each logs as log}
                        <div class="text-white/70" in:slide={{ duration: 200 }}>
                            <span class="text-cyan-400 mr-2">></span>
                            {log}
                        </div>
                    {/each}
                </div>

                <!-- Status Indicators -->
                <div
                    class="mt-4 pt-4 border-t border-white/10 grid grid-cols-3 gap-2"
                >
                    <div
                        class="flex flex-col gap-1 items-center p-2 rounded-xl border {status ===
                        'WEAVING_LAYOUT'
                            ? 'border-amber-400 bg-amber-400/10 text-amber-400'
                            : status === 'IDLE'
                              ? 'border-white/5 text-white/20'
                              : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'} transition-colors"
                    >
                        <Layout size={14} />
                        <span class="text-[7px] font-black uppercase"
                            >Layout</span
                        >
                    </div>
                    <div
                        class="flex flex-col gap-1 items-center p-2 rounded-xl border {status ===
                        'STITCHING_DATA'
                            ? 'border-amber-400 bg-amber-400/10 text-amber-400'
                            : status === 'IDLE' || status === 'WEAVING_LAYOUT'
                              ? 'border-white/5 text-white/20'
                              : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'} transition-colors"
                    >
                        <Database size={14} />
                        <span class="text-[7px] font-black uppercase">Data</span
                        >
                    </div>
                    <div
                        class="flex flex-col gap-1 items-center p-2 rounded-xl border {status ===
                        'SECURING_AUTH'
                            ? 'border-amber-400 bg-amber-400/10 text-amber-400'
                            : status === 'ACTIVE'
                              ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
                              : 'border-white/5 text-white/20'} transition-colors"
                    >
                        <Lock size={14} />
                        <span class="text-[7px] font-black uppercase">Auth</span
                        >
                    </div>
                </div>
            </div>

            <!-- Visual Output -->
            <div
                class="bg-gradient-to-br from-white/5 to-transparent rounded-3xl border border-white/5 p-6 flex flex-col relative grid-stack"
            >
                {#if status !== "ACTIVE"}
                    <div
                        class="w-full h-full flex items-center justify-center opacity-30 animate-pulse"
                    >
                        <div
                            class="text-[8px] font-black tracking-[0.5em] text-white uppercase text-center leading-loose"
                        >
                            Synthesizing<br />Geometry
                        </div>
                    </div>
                {:else}
                    <div
                        class="w-full h-full space-y-4"
                        in:fade={{ duration: 500 }}
                    >
                        <div
                            class="flex items-center justify-between pb-4 border-b border-white/10"
                        >
                            <h4
                                class="text-[10px] font-black uppercase text-white tracking-widest"
                            >
                                {intentQuery.slice(0, 15)}...
                            </h4>
                            <div
                                class="px-2 py-1 bg-emerald-500/20 text-emerald-400 text-[8px] rounded font-black uppercase tracking-widest"
                            >
                                Live
                            </div>
                        </div>
                        <div class="css-carousel gap-3 pb-2 no-scrollbar">
                            {#each generatedNodes as node (node.id)}
                                <div
                                    class="carousel-item w-28 h-28 shrink-0 rounded-2xl border p-3 flex flex-col justify-between {node.color}"
                                    in:scale={{ delay: node.id * 100 }}
                                >
                                    <div
                                        class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"
                                    >
                                        {#if node.id === 1}
                                            <Database size={10} />
                                        {:else if node.id === 2}
                                            <Lock size={10} />
                                        {:else}
                                            <Layout size={10} />
                                        {/if}
                                    </div>
                                    <p
                                        class="text-[10px] font-black uppercase tracking-widest"
                                    >
                                        {node.type}
                                    </p>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>
    .animate-spin-slow {
        animation: spin 3s linear infinite;
        display: inline-block;
    }
    @keyframes spin {
        100% {
            transform: rotate(360deg);
        }
    }
    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(34, 211, 238, 0.2);
        border-radius: 4px;
    }
    .grid-stack > * {
        grid-area: 1 / 1;
    }
</style>
