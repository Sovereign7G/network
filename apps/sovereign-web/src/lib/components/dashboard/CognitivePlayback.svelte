<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { Brain, Play, Terminal } from "lucide-svelte";

    // 🧠 COGNITIVE PLAYBACK: Sophia's Thought Scrubber
    const logs = $derived(manifold.cognitiveHistory);

    let activeLogId = $state("");
    const activeLog = $derived(logs.find((l) => l.id === activeLogId));

    $effect(() => {
        if (!activeLogId && logs.length > 0) {
            activeLogId = logs[0]?.id || "";
        }
    });

    function playback(id: string) {
        activeLogId = id;
        manifold.recordEvent(
            "COGNITIVE_REPLAY",
            `Replaying Sophia thought log: ${id}`,
        );
    }
</script>

<div
    class="flex flex-col h-full bg-black/80 rounded-[2.5rem] border-2 border-white/10 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl relative"
>
    <div class="flex items-center gap-3">
        <div
            class="p-3 bg-fuchsia-600 text-white rounded-2xl shadow-[0_0_20px_rgba(192,38,211,0.3)]"
        >
            <Brain size={20} />
        </div>
        <div>
            <h2
                class="text-sm font-black uppercase tracking-tighter text-white"
            >
                Cognitive_Playback
            </h2>
            <div class="flex items-center gap-2">
                <span
                    class="w-1.5 h-1.5 rounded-full bg-fuchsia-400 animate-pulse"
                ></span>
                <span
                    class="text-[8px] font-black text-fuchsia-400/60 uppercase tracking-widest"
                    >Thought_Scrubber // ABI_0x57</span
                >
            </div>
        </div>
    </div>

    <!-- Active Thought Render -->
    <div
        class="p-5 bg-white/5 border border-white/10 rounded-3xl min-h-[120px] flex flex-col gap-3"
    >
        {#if activeLog}
            <div class="flex items-center justify-between">
                <span
                    class="text-[8px] font-black text-fuchsia-400 uppercase tracking-widest"
                    >{activeLog.epoch}</span
                >
                <span
                    class="text-[8px] font-black text-white/20 uppercase tracking-tighter"
                    >{activeLog.id}</span
                >
            </div>
            <p
                class="text-[11px] font-bold text-white/80 leading-relaxed italic"
            >
                "{activeLog.thought}"
            </p>
            <div class="mt-auto flex items-center justify-between">
                <div
                    class="px-2 py-1 bg-fuchsia-500/20 rounded text-[7px] font-black text-fuchsia-400 uppercase"
                >
                    Mood: {activeLog.mood}
                </div>
                {#if activeLog.epoch !== "STAKED"}
                    <button
                        class="px-3 py-1 bg-cyan-400 text-black text-[7px] font-black uppercase rounded hover:bg-white transition-all shadow-lg"
                        onclick={() =>
                            manifold.stakeCognitiveEpoch(activeLog.id)}
                    >
                        Provision_As_Liquidity
                    </button>
                {:else}
                    <span
                        class="text-[7px] font-black text-cyan-400 uppercase italic"
                        >Active_Collateral</span
                    >
                {/if}
            </div>
        {/if}
    </div>

    <!-- Log List -->
    <div class="flex-1 space-y-2 overflow-y-auto custom-scrollbar">
        <p
            class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
        >
            Historic_Epochs
        </p>
        {#each logs as log}
            <button
                class="w-full text-left p-3 rounded-xl border border-white/5 transition-all flex items-center justify-between group {activeLogId ===
                log.id
                    ? 'bg-fuchsia-500/10 border-fuchsia-500/30'
                    : 'hover:bg-white/5'}"
                onclick={() => playback(log.id)}
            >
                <div class="flex flex-col">
                    <span
                        class="text-[9px] font-black text-white uppercase group-hover:text-fuchsia-400 transition-colors"
                        >{log.epoch}</span
                    >
                    <span
                        class="text-[7px] font-bold text-white/30 uppercase tracking-tighter"
                        >{log.id}</span
                    >
                </div>
                <Play
                    size={12}
                    class="{activeLogId === log.id
                        ? 'text-fuchsia-400'
                        : 'text-white/20 opacity-0 group-hover:opacity-100'} transition-all"
                />
            </button>
        {/each}
    </div>

    <div
        class="flex items-center justify-between text-[7px] font-black text-white/20 uppercase border-t border-white/5 pt-4"
    >
        <div class="flex items-center gap-2">
            <Terminal size={12} />
            <span>Trace Signal: ENCRYPTED</span>
        </div>
        <span>v9.6C</span>
    </div>
</div>
