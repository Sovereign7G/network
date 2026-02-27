<script lang="ts">
    import {
        HardDrive,
        Share2,
        ShieldCheck,
        RefreshCcw,
        Link,
        FileText,
        LayoutGrid,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let localHealth = $state(100);
    let syncStatus = $state("Synchronized");
    let crdtVectors = $state(1420);
    let graphNodes = $state(85);

    const storageAudit = [
        {
            id: 1,
            type: "Sync",
            message: "CRDT_Vector_Clock_Stable",
            status: "Passed",
        },
        {
            id: 2,
            type: "Residency",
            message: "Local_First_Shard_Verified",
            status: "Sovereign",
        },
        {
            id: 3,
            type: "Graph",
            message: "Backlink_Manifold_Indexed",
            status: "Active",
        },
        {
            id: 4,
            type: "Security",
            message: "Digital_Bunker_Hardening",
            status: "Secure",
        },
    ];

    onMount(() => {
        const interval = setInterval(() => {
            localHealth = Math.min(
                100,
                Math.max(98, localHealth + (Math.random() - 0.5) * 0.1),
            );
            crdtVectors += Math.floor(Math.random() * 5);
        }, 3000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="sovereign-storage-manifold bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group"
>
    <!-- Background Graph Shards (Decorative) -->
    <div class="absolute inset-0 opacity-[0.05] pointer-events-none">
        <svg class="w-full h-full">
            <line
                x1="10%"
                y1="20%"
                x2="40%"
                y2="50%"
                stroke="white"
                stroke-width="1"
            />
            <line
                x1="40%"
                y1="50%"
                x2="70%"
                y2="30%"
                stroke="white"
                stroke-width="1"
            />
            <line
                x1="40%"
                y1="50%"
                x2="20%"
                y2="80%"
                stroke="white"
                stroke-width="1"
            />
            <circle cx="10%" cy="20%" r="4" fill="white" />
            <circle cx="40%" cy="50%" r="6" fill="white" />
            <circle cx="70%" cy="30%" r="4" fill="white" />
            <circle cx="20%" cy="80%" r="4" fill="white" />
        </svg>
    </div>

    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-cyan-500/10 rounded-2xl text-cyan-400 border border-cyan-500/20 shadow-[0_0_20px_rgba(34,211,238,0.1)]"
            >
                <HardDrive size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Sovereign_Storage_Audit
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Local-First // CRDT_Sync_Protocol
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-3 px-4 py-2 bg-cyan-400/10 border border-cyan-400/20 rounded-full"
        >
            <ShieldCheck size={12} class="text-cyan-400" />
            <span
                class="text-[9px] font-black text-cyan-400 uppercase tracking-widest"
                >BUNKER_PROTOCOL_ACTIVE</span
            >
        </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 grid grid-cols-2 gap-8 z-10">
        <!-- Left: Local Health & Sync Stats -->
        <div class="flex flex-col gap-6">
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center"
            >
                <div class="absolute top-4 left-6 flex items-center gap-2">
                    <RefreshCcw size={14} class="text-cyan-500" />
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Sync_Integrity</span
                    >
                </div>

                <div
                    class="relative w-32 h-32 flex items-center justify-center"
                >
                    <svg class="w-full h-full">
                        <circle
                            cx="64"
                            cy="64"
                            r="60"
                            fill="none"
                            class="stroke-white/5"
                            stroke-width="4"
                            stroke-dasharray="10 5"
                        />
                        <circle
                            cx="64"
                            cy="64"
                            r="60"
                            fill="none"
                            class="stroke-cyan-400"
                            stroke-width="4"
                            stroke-dasharray="200"
                            stroke-dashoffset="0"
                        />
                    </svg>
                    <div
                        class="absolute inset-0 flex flex-col items-center justify-center"
                    >
                        <span class="text-3xl font-black text-white"
                            >{localHealth.toFixed(1)}%</span
                        >
                        <span
                            class="text-[8px] font-black text-cyan-400 uppercase"
                            >Residency</span
                        >
                    </div>
                </div>
                <span
                    class="text-[10px] font-mono text-white/60 mt-4 tracking-tighter uppercase"
                    >{syncStatus}</span
                >
            </div>

            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-2 group/stat"
            >
                <div class="flex justify-between items-center">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >CRDT_Vector_Clocks</span
                    >
                    <Share2 size={12} class="text-cyan-400" />
                </div>
                <div class="flex items-baseline gap-2">
                    <span class="text-2xl font-black text-white"
                        >{crdtVectors.toLocaleString()}</span
                    >
                    <span class="text-[10px] font-bold text-white/20 uppercase"
                        >VECTORS</span
                    >
                </div>
            </div>
        </div>

        <!-- Right: Graph & Audit Feed -->
        <div class="flex flex-col gap-6">
            <!-- Node Count / Networked Thought -->
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <Link size={14} class="text-indigo-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Networked_Thought_Graph</span
                        >
                    </div>
                    <span class="text-xs font-mono text-indigo-400"
                        >{graphNodes} NODES</span
                    >
                </div>
                <div class="flex gap-2">
                    {#each Array(8) as _, i}
                        <div
                            class="flex-1 h-1 rounded-full bg-indigo-500/20 transition-all duration-300"
                            style:background-color={i < 5 ? "#818cf8" : ""}
                        ></div>
                    {/each}
                </div>
                <p
                    class="text-[8px] text-white/30 italic uppercase tracking-widest"
                >
                    Hierarchy_Obsolescence_Detected
                </p>
            </div>

            <!-- Storage Audit Feed -->
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
            >
                <div class="flex justify-between items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                        >Storage_Audit_Stream</span
                    >
                    <FileText size={12} class="text-white/10" />
                </div>
                <div
                    class="space-y-3 overflow-y-auto max-h-[150px] custom-scrollbar"
                >
                    {#each storageAudit as log}
                        <div
                            class="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-all hover:bg-white/10 group/log"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-1.5 h-1.5 rounded-full bg-cyan-400"
                                ></div>
                                <div class="flex flex-col">
                                    <span
                                        class="text-[9px] font-bold text-white/80"
                                        >{log.message}</span
                                    >
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase"
                                        >{log.type}</span
                                    >
                                </div>
                            </div>
                            <div
                                class="text-[8px] font-black text-cyan-400/50 uppercase"
                            >
                                {log.status}
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>

    <!-- Footer Decor -->
    <div class="absolute bottom-4 right-8 opacity-20 flex items-center gap-2">
        <LayoutGrid size={10} class="text-white" />
        <span
            class="text-[7px] font-black text-white uppercase tracking-widest italic"
            >Digital_Bunker_v1.0</span
        >
    </div>
</div>
