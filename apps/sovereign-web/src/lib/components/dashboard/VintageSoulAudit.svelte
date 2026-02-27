<script lang="ts">
    import {
        Coffee,
        Anchor,
        PenTool,
        Flame,
        History,
        ShieldCheck,
        ChevronRight,
        Palette,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let patinaDepth = $state(42);
    let individualVision = $state(98);
    let aestheticBoldness = $state(85);

    const soulAuditFeed = [
        {
            id: 1,
            type: "Soul",
            message: "Individual_Vision_Verified",
            status: "Passed",
        },
        {
            id: 2,
            type: "Aesthetic",
            message: "Chromatic_Optimism_Stable",
            status: "Active",
        },
        {
            id: 3,
            type: "Craft",
            message: "Intentional_Idiosyncrasy_Audit",
            status: "Authentic",
        },
        {
            id: 4,
            type: "Memory",
            message: "Patina_Manifest_Sync",
            status: "Aging_Gracefully",
        },
    ];

    onMount(() => {
        const interval = setInterval(() => {
            patinaDepth = Math.min(100, patinaDepth + 0.01); // Slowly aging
            individualVision = Math.min(
                100,
                Math.max(95, individualVision + (Math.random() - 0.5)),
            );
        }, 5000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="vintage-soul-manifold bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group font-serif"
>
    <!-- Background Texture (Subtle Grain/Noise) -->
    <div
        class="absolute inset-0 opacity-[0.03] pointer-events-none mix-blend-overlay"
        style:background-image="url('https://www.transparenttextures.com/patterns/natural-paper.png')"
    ></div>

    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-amber-500/10 rounded-2xl text-amber-500 border border-amber-500/20 shadow-[0_0_20px_rgba(245,158,11,0.1)]"
            >
                <Anchor size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Vintage_Soul_Audit
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Individual_Vision // Patina_Protocol
                </p>
            </div>
        </div>
        <div
            class="flex items-center gap-3 px-4 py-2 bg-amber-400/10 border border-amber-400/20 rounded-full"
        >
            <ShieldCheck size={12} class="text-amber-400" />
            <span
                class="text-[9px] font-black text-amber-400 uppercase tracking-widest"
                >AUTHENTIC_CRAFT</span
            >
        </div>
    </header>

    <!-- Metrics Grid -->
    <div class="flex-1 grid grid-cols-2 gap-8 z-10">
        <!-- Left: Individual Vision & Patina -->
        <div class="flex flex-col gap-6">
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center"
            >
                <div class="absolute top-4 left-6 flex items-center gap-2">
                    <PenTool size={14} class="text-amber-500" />
                    <span
                        class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >Individual_Vision</span
                    >
                </div>

                <div
                    class="relative w-32 h-32 flex items-center justify-center"
                >
                    <div
                        class="absolute inset-0 border-4 border-amber-500/20 rounded-full"
                    ></div>
                    <div
                        class="absolute inset-0 border-4 border-amber-500 rounded-full border-t-transparent animate-[spin_10s_linear_infinite]"
                    ></div>
                    <Flame size={40} class="text-amber-500 animate-pulse" />
                </div>
                <span class="text-2xl font-black text-white mt-4"
                    >{individualVision.toFixed(0)}%</span
                >
                <span
                    class="text-[8px] font-black text-amber-400 uppercase tracking-widest"
                    >COHESIVE_SOUL</span
                >
            </div>

            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-2"
            >
                <div class="flex justify-between items-center">
                    <span class="text-[8px] font-black text-white/20 uppercase"
                        >Patina_Depth</span
                    >
                    <History size={12} class="text-white/40" />
                </div>
                <div class="flex items-baseline gap-2">
                    <span class="text-2xl font-black text-white"
                        >{patinaDepth.toFixed(2)}</span
                    >
                    <span class="text-[10px] font-bold text-white/20 uppercase"
                        >EPHEMERAL_VALUE</span
                    >
                </div>
                <!-- Patina Progress Bar (Organic looking) -->
                <div
                    class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden mt-2 relative"
                >
                    <div
                        class="h-full bg-amber-600/50 blur-[1px]"
                        style:width="{patinaDepth}%"
                    ></div>
                    <div
                        class="h-full absolute top-0 left-0 bg-amber-400"
                        style:width="{patinaDepth}%"
                    ></div>
                </div>
            </div>
        </div>

        <!-- Right: Boldness & Soul Audit -->
        <div class="flex flex-col gap-6">
            <div
                class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4"
            >
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <Palette size={14} class="text-orange-400" />
                        <span
                            class="text-[10px] font-black text-white uppercase tracking-widest"
                            >Aesthetic_Boldness</span
                        >
                    </div>
                    <span class="text-xs font-mono text-orange-400"
                        >{aestheticBoldness}%</span
                    >
                </div>
                <div class="flex gap-2">
                    {#each ["bg-orange-500", "bg-red-500", "bg-amber-500", "bg-blue-600", "bg-emerald-600"] as color}
                        <div
                            class="flex-1 h-2 {color} rounded-full overflow-hidden shadow-inner opacity-80 hover:opacity-100 transition-opacity"
                        ></div>
                    {/each}
                </div>
            </div>

            <!-- Audit Feed -->
            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
            >
                <div class="flex justify-between items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                        >Soul_Audit_Logs</span
                    >
                    <Coffee size={12} class="text-white/10" />
                </div>
                <div
                    class="space-y-3 overflow-y-auto max-h-[150px] custom-scrollbar"
                >
                    {#each soulAuditFeed as log}
                        <div
                            class="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/5 hover:border-amber-500/30 transition-all hover:bg-white/10 group/log"
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-1.5 h-1.5 rounded-full bg-amber-400"
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
                            <ChevronRight
                                size={10}
                                class="text-white/10 group-hover/log:translate-x-1 transition-all"
                            />
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>

    <!-- Fine Detail Print -->
    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 opacity-20">
        <span class="text-[6px] font-serif uppercase tracking-[1em] text-white"
            >Crafted_For_The_Century</span
        >
    </div>
</div>
