<!--
[IN]: manifold, lucide-svelte
[OUT]: MeshStressTest Component
[POS]: High-frequency manifold replication stress testing workstation. / \u9ad8\u9891\u6d41\u5f62\u53e0\u52a0\u5e94\u529b\u6d4b\u8bd5\u5de5\u4f5c\u7ad9\u3022
Protocol: When updating me, sync this header + parent folder's .folder.md
-->
<script lang="ts">
    import { fade } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Activity,
        ShieldAlert,
        Zap,
        Globe,
        Gauge,
        Cpu,
        RefreshCw,
    } from "lucide-svelte";

    let stress = $derived(manifold.meshStressState);
    let isTesting = $derived(stress.active);
    let latency = $derived(stress.latencyHistory);
    let nodesOnline = $derived(stress.nodesOnline);
    let errorRate = $derived(stress.errorRate);
    let testPhase = $derived(stress.phase);

    async function runStressTest() {
        await manifold.runMeshStressDrill();
    }

    let avgLatency = $derived(
        latency.length > 0
            ? (latency.reduce((a, b) => a + b, 0) / latency.length).toFixed(1)
            : "0.0",
    );
</script>

<div class="mesh-stress-panel glass-panel p-6" in:fade>
    <div class="flex items-center gap-3 mb-6">
        <div
            class="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-emerald-400"
        >
            <Activity size={18} />
        </div>
        <div>
            <h3
                class="text-[8px] font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                Infrastructure Resilience
            </h3>
            <h2
                class="text-xl font-black text-white uppercase tracking-tighter"
            >
                Mesh Stress Test
            </h2>
        </div>
    </div>

    <div class="space-y-6">
        <!-- Live Metrics Grid -->
        <div class="grid grid-cols-3 gap-3">
            <div class="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <div
                    class="flex items-center gap-1 text-[7px] font-black uppercase text-white/20 mb-1"
                >
                    <Globe size={10} />
                    <span>Nodes</span>
                </div>
                <span class="text-xs font-black text-white">{nodesOnline}</span>
            </div>
            <div class="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <div
                    class="flex items-center gap-1 text-[7px] font-black uppercase text-white/20 mb-1"
                >
                    <Gauge size={10} />
                    <span>Latency</span>
                </div>
                <span class="text-xs font-black text-cyan-400"
                    >{avgLatency}ms</span
                >
            </div>
            <div class="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <div
                    class="flex items-center gap-1 text-[7px] font-black uppercase text-white/20 mb-1"
                >
                    <ShieldAlert size={10} />
                    <span>Errors</span>
                </div>
                <span class="text-xs font-black text-rose-400"
                    >{(errorRate * 100).toFixed(3)}%</span
                >
            </div>
        </div>

        <!-- Latency Waveform -->
        <div
            class="h-24 bg-black/40 border border-white/5 rounded-2xl flex items-end gap-0.5 p-4 overflow-hidden relative"
        >
            <div
                class="absolute inset-x-4 top-2 flex justify-between text-[6px] font-mono text-white/10 uppercase"
            >
                <span>Burst_Response_Trace</span>
                <span>REPL_FACTOR: 12</span>
            </div>
            {#each latency as lat}
                <div
                    class="flex-1 bg-cyan-400/30 rounded-t-sm"
                    style="height: {Math.max(
                        10,
                        lat * 2,
                    )}%; border-top: 1px solid rgba(34,211,238,0.5)"
                ></div>
            {/each}
            {#if latency.length === 0}
                <div
                    class="w-full h-full flex items-center justify-center text-white/5 text-[8px] font-black uppercase tracking-widest"
                >
                    Ready for probe...
                </div>
            {/if}
        </div>

        <!-- Test Trigger -->
        <div class="space-y-4">
            <button
                onclick={runStressTest}
                disabled={isTesting}
                class="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] transition-all flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(16,185,129,0.3)] disabled:opacity-50"
            >
                {#if isTesting}
                    <RefreshCw size={14} class="animate-spin" />
                    Executing_Drill...
                {:else}
                    <Zap size={14} />
                    Initiate Stress Drill
                {/if}
            </button>

            {#if testPhase}
                <div
                    class="p-3 bg-black/40 border border-emerald-500/20 rounded-xl flex items-center gap-3"
                >
                    <Cpu size={14} class="text-emerald-400 animate-pulse" />
                    <span
                        class="text-[8px] font-mono text-emerald-400 uppercase"
                        >{testPhase}</span
                    >
                </div>
            {/if}
        </div>
    </div>

    <!-- Security Note -->
    <div
        class="mt-6 pt-4 border-t border-white/5 opacity-30 text-[7px] font-black uppercase tracking-tighter text-white/40 text-center leading-relaxed"
    >
        Warning: High-frequency stress probes may cause temporary manifold drift
        in adjacent shards.
    </div>
</div>

<style>
    .mesh-stress-panel {
        background: linear-gradient(
            135deg,
            rgba(16, 185, 129, 0.05) 0%,
            rgba(15, 23, 42, 0.4) 100%
        );
    }
</style>
