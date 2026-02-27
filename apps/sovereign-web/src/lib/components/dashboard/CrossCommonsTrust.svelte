<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    
    import {
        Handshake,
        Globe,
        ArrowRightLeft,
        ShieldCheck,
    } from "lucide-svelte";

    // 🤝 CROSS-COMMONS TRUST: Relational Power Visualizer
    const matrix = $derived(manifold.trustMatrix);
</script>

<div
    class="flex flex-col h-full bg-black/60 rounded-[2rem] border-2 border-white/5 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl"
>
    <div class="flex items-center gap-3">
        <div
            class="p-3 bg-emerald-500 text-white rounded-2xl shadow-[0_0_20px_rgba(16,185,129,0.3)]"
        >
            <Handshake size={20} />
        </div>
        <div>
            <h2
                class="text-sm font-black uppercase tracking-tighter text-white"
            >
                Cross_Commons_Trust
            </h2>
            <div class="flex items-center gap-2">
                <span
                    class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"
                ></span>
                <span
                    class="text-[8px] font-black text-emerald-400/60 uppercase tracking-widest"
                    >Relational_Mesh Active</span
                >
            </div>
        </div>
    </div>

    <div class="flex-1 overflow-y-auto space-y-3 custom-scrollbar">
        {#each matrix as link}
            <div
                class="bg-white/5 border border-white/5 rounded-2xl p-4 hover:bg-white/10 transition-all group"
            >
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                        <span
                            class="text-[9px] font-black px-2 py-0.5 bg-white/10 rounded-md text-white/60"
                            >{link.source}</span
                        >
                        <ArrowRightLeft
                            size={10}
                            class="text-white/20 group-hover:text-emerald-400 transition-colors"
                        />
                        <span
                            class="text-[9px] font-black px-2 py-0.5 bg-white/10 rounded-md text-white/60"
                            >{link.target}</span
                        >
                    </div>
                    <ShieldCheck
                        size={14}
                        class="text-emerald-400 opacity-60"
                    />
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase"
                                >Trust_Score</span
                            >
                            <span class="text-[9px] font-black text-emerald-400"
                                >{(link.trust * 100).toFixed(0)}%</span
                            >
                        </div>
                        <div
                            class="h-1 bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="h-full bg-emerald-500"
                                style:width="{link.trust * 100}%"
                            ></div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase"
                                >Alignment</span
                            >
                            <span class="text-[9px] font-black text-cyan-400"
                                >{(link.alignment * 100).toFixed(0)}%</span
                            >
                        </div>
                        <div
                            class="h-1 bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="h-full bg-cyan-400"
                                style:width="{link.alignment * 100}%"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        {/each}

        <button
            class="w-full py-4 border-2 border-dashed border-white/5 rounded-2xl text-[9px] font-black text-white/20 uppercase hover:border-white/20 hover:text-emerald-400/40 transition-all"
        >
            + Initiate New Trust Channel
        </button>
    </div>

    <div class="pt-4 border-t border-white/5 flex items-center justify-between">
        <div class="flex items-center gap-2">
            <Globe size={12} class="text-white/20" />
            <span
                class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                >Global_Pact_v4.2</span
            >
        </div>
        <span class="text-[8px] font-black text-emerald-400">COHERENT</span>
    </div>
</div>
