<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { Share2, Zap, Activity, Archive } from "lucide-svelte";

    // 🌌 MULTIVERSAL ESCALATION: Cross-Shard Coordination
    const state = $derived(manifold.multiversalState);

    function triggerEscalation(shardId: string) {
        manifold.triggerEscalation(shardId);
    }
</script>

<div
    class="flex flex-col h-full bg-black/80 rounded-[2.5rem] border-2 border-white/10 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl relative"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="p-3 bg-indigo-600 text-white rounded-2xl shadow-[0_0_20px_rgba(79,70,229,0.3)]"
            >
                <Share2 size={20} />
            </div>
            <div>
                <h2
                    class="text-sm font-black uppercase tracking-tighter text-white"
                >
                    Multiversal_Escalation
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="w-1.5 h-1.5 rounded-full {state.syncStatus ===
                        'SYNCHRONIZED'
                            ? 'bg-emerald-400'
                            : 'bg-rose-500'} animate-pulse"
                    ></span>
                    <span
                        class="text-[8px] font-black {state.syncStatus ===
                        'SYNCHRONIZED'
                            ? 'text-emerald-400/60'
                            : 'text-rose-500/60'} uppercase tracking-widest"
                        >{state.syncStatus} // ABI_0xE0</span
                    >
                </div>
            </div>
        </div>
        <div class="flex gap-2">
            <button
                class="px-3 py-2 bg-rose-500/20 border border-rose-500/30 text-rose-400 text-[8px] font-black uppercase rounded-2xl hover:bg-rose-500 hover:text-white transition-all shadow-lg flex items-center gap-2"
                onclick={() => manifold.triggerMultiversalStressTest()}
            >
                <Activity size={12} />
                Global_Stress
            </button>
            <button
                class="px-3 py-2 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-[8px] font-black uppercase rounded-2xl hover:bg-indigo-500 hover:text-white transition-all shadow-lg flex items-center gap-2"
                onclick={() => manifold.spawnMultiversalShard()}
            >
                <Share2 size={12} />
                Spawn_Shard
            </button>
        </div>
    </div>

    <!-- Shard Scrubber -->
    <div class="flex-1 space-y-4 overflow-y-auto custom-scrollbar">
        <p
            class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
        >
            Active_Shards // Cross_Universe
        </p>

        {#each state.activeShards as shard}
            <div
                class="group bg-white/5 border border-white/5 rounded-2xl p-4 hover:border-indigo-500/30 transition-all"
            >
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full bg-indigo-400"></div>
                        <span
                            class="text-[10px] font-black text-white uppercase"
                            >{shard}</span
                        >
                    </div>
                    <span class="text-[8px] font-black text-white/30"
                        >0x{Math.floor(Math.random() * 0xffff)
                            .toString(16)
                            .toUpperCase()}</span
                    >
                </div>

                <button
                    class="w-full py-2 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[8px] font-black uppercase rounded-lg hover:bg-indigo-500 hover:text-white transition-all"
                    onclick={() => triggerEscalation(shard)}
                >
                    Escalate Shard Signature
                </button>
            </div>
        {/each}

        {#if state.archives.length > 0}
            <div class="mt-6 border-t border-white/5 pt-6">
                <p
                    class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em] mb-4"
                >
                    Sealed_Archives // Basel_IV
                </p>
                <div class="space-y-2">
                    {#each state.archives.slice(0, 3) as archive}
                        <div
                            class="bg-emerald-500/5 border border-emerald-500/10 rounded-xl p-3 flex justify-between items-center"
                        >
                            <div class="flex flex-col">
                                <span
                                    class="text-[8px] font-black text-white uppercase"
                                    >{archive.id}</span
                                >
                                <span
                                    class="text-[6px] font-bold text-emerald-400/40 uppercase"
                                    >Resonance: {archive.resonance.toFixed(
                                        1,
                                    )}%</span
                                >
                            </div>
                            <Archive size={12} class="text-emerald-400/50" />
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>

    <!-- Global Actions Footer -->
    <div class="flex flex-col gap-4">
        <!-- Escalation Gauge -->
        <div
            class="bg-indigo-500/5 p-4 rounded-3xl border border-indigo-500/10"
        >
            <div class="flex justify-between items-center mb-2">
                <span class="text-[8px] font-black text-white/40 uppercase"
                    >Federation_Pressure</span
                >
                <span class="text-[10px] font-black text-indigo-400"
                    >{state.escalationLevel}%</span
                >
            </div>
            <div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                <div
                    class="h-full bg-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.5)] transition-all duration-1000"
                    style:width="{state.escalationLevel}%"
                ></div>
            </div>
        </div>

        <button
            class="w-full py-4 bg-emerald-500 text-black text-[9px] font-black uppercase tracking-widest rounded-3xl hover:bg-white transition-all shadow-2xl flex items-center justify-center gap-3"
            onclick={() => manifold.archiveManifoldState()}
        >
            <Archive size={14} fill="currentColor" />
            <span>Seal_Archive_Epoch // Basel_IV</span>
        </button>
    </div>

    <div
        class="flex items-center justify-between text-[7px] font-black text-white/20 uppercase mt-2"
    >
        <div class="flex items-center gap-2">
            <Zap size={10} />
            <span>Omega_Point_Vector</span>
        </div>
        <span>Shard_Sync: ACTIVE</span>
    </div>
</div>
