<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { Activity, Zap, ShieldAlert, Cpu } from "lucide-svelte";

    // Simulating the Mesh Performance
    let targetGuardians = $state(10);
    let currentDabbas = $state(0);
    let peakCapacity = $state(0);
    let activeNodes = $state(3);

    let isTesting = $state(false);
    let testProgress = $state(0);
    let testResults = $state<any>(null);

    let maxCapacityPerNode = 1500; // Dabbas per second

    // Chart simulation
    let timeSeries = $state<number[]>([]);
    const MAX_POINTS = 30;

    $effect(() => {
        // Calculate theoretical limit
        peakCapacity = activeNodes * maxCapacityPerNode;
    });

    async function runStressTest() {
        if (isTesting) return;

        isTesting = true;
        testProgress = 0;
        testResults = null;
        timeSeries = Array(MAX_POINTS).fill(0);

        activeNodes = targetGuardians; // Simulate network scaling up
        currentDabbas = 0;

        // Haptic feedback
        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate(50);
        }

        const duration = 5000;
        const interval = 50;
        const steps = duration / interval;
        let currentStep = 0;

        const timer = setInterval(() => {
            currentStep++;
            testProgress = (currentStep / steps) * 100;

            // Ramp up load (simulating incoming Guardians)
            const targetLoad = peakCapacity * (1.2 * (currentStep / steps)); // Try to push 120% capacity

            // Add some jitter
            currentDabbas = Math.floor(
                targetLoad * (0.9 + Math.random() * 0.2),
            );

            timeSeries = [...timeSeries.slice(1), currentDabbas];

            if (currentStep >= steps) {
                clearInterval(timer);
                finishTest();
            }
        }, interval);
    }

    function finishTest() {
        isTesting = false;

        // Calculate results
        const isSuccessful = currentDabbas <= peakCapacity * 1.05; // 5% variance grace

        testResults = {
            success: isSuccessful,
            maxSustained: Math.floor(
                peakCapacity * (isSuccessful ? 0.98 : 0.85),
            ),
            packetLoss: isSuccessful ? "0.001%" : "12.4%",
            latencyAvg: isSuccessful ? "12ms" : "145ms",
        };

        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate([100, 50, 100]); // Success pattern
        }
    }
</script>

<div
    class="chiaroscuro-card p-6 border-white/10 backdrop-blur-2xl text-white relative overflow-hidden"
    in:fade
>
    <!-- Background grid decoration -->
    <div
        class="absolute inset-0 grid-bg opacity-[0.03] pointer-events-none"
    ></div>

    <div class="flex justify-between items-start relative z-10 mb-6">
        <div>
            <h3
                class="text-xl font-black text-[#22d3ee] flex items-center gap-2"
            >
                <Activity size={20} />
                MESH STRESS SIMULATOR
            </h3>
            <p class="text-xs text-white/50 tracking-widest uppercase mt-1">
                Data Dabba Throughput & Tolerance
            </p>
        </div>

        <!-- Quick stats -->
        <div class="flex gap-4 text-right">
            <div>
                <div
                    class="text-[9px] text-white/40 font-bold tracking-widest uppercase"
                >
                    Target Guardians
                </div>
                <div class="text-lg font-mono text-amber-500 font-black">
                    {targetGuardians}
                </div>
            </div>
            <div>
                <div
                    class="text-[9px] text-white/40 font-bold tracking-widest uppercase"
                >
                    Theo. Limit (Dpk/s)
                </div>
                <div class="text-lg font-mono text-emerald-400 font-black">
                    {peakCapacity.toLocaleString()}
                </div>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
        <!-- Controls -->
        <div class="col-span-1 space-y-6 flex flex-col justify-between">
            <div class="space-y-4">
                <div class="control-group">
                    <div class="flex justify-between mb-2">
                        <label class="text-xs font-bold text-white/70 uppercase"
                            >Simulate Guardians</label
                        >
                        <span class="text-xs font-mono text-[#22d3ee]"
                            >{targetGuardians} Nodes</span
                        >
                    </div>
                    <input
                        type="range"
                        bind:value={targetGuardians}
                        min="1"
                        max="100"
                        disabled={isTesting}
                        class="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[#22d3ee]"
                    />
                </div>
            </div>

            <button
                class="w-full py-4 rounded-xl font-black uppercase tracking-widest transition-all
                       {isTesting
                    ? 'bg-amber-500/20 text-amber-500 border border-amber-500/50'
                    : 'bg-[#22d3ee]/20 text-[#22d3ee] border border-[#22d3ee]/50 hover:bg-[#22d3ee] hover:text-black'}"
                onclick={runStressTest}
                disabled={isTesting}
            >
                {#if isTesting}
                    <div class="flex justify-center items-center gap-2">
                        <div
                            class="w-4 h-4 rounded-full border-2 border-amber-500 border-t-transparent animate-spin"
                        ></div>
                        METERING MESH... {Math.round(testProgress)}%
                    </div>
                {:else}
                    EXECUTE STRESS INJECTION
                {/if}
            </button>
        </div>

        <!-- Live Chart Area -->
        <div
            class="col-span-2 bg-black/40 rounded-2xl border border-white/5 p-4 relative flex flex-col justify-end min-h-[200px] overflow-hidden"
        >
            {#if !isTesting && !testResults}
                <div
                    class="absolute inset-0 flex items-center justify-center.text-white/20 font-mono tracking-widest opacity-30 text-center flex-col justify-center"
                >
                    <Cpu size={32} class="mx-auto mb-2 text-white/20" />
                    SYSTEM IDLE<br />AWAITING INJECTION
                </div>
            {/if}

            <div class="absolute top-4 left-4 z-20">
                <div
                    class="text-[10px] uppercase font-bold text-white/40 tracking-widest"
                >
                    Live Dabbas/sec
                </div>
                <div
                    class="text-3xl font-mono font-black"
                    class:text-red-500={currentDabbas > peakCapacity}
                    class:text-emerald-400={currentDabbas <= peakCapacity &&
                        isTesting}
                >
                    {currentDabbas.toLocaleString()}
                </div>
            </div>

            <!-- Overload Warning -->
            {#if currentDabbas > peakCapacity}
                <div
                    class="absolute top-4 right-4 z-20 bg-red-500/20 text-red-500 border border-red-500/50 px-3 py-1 rounded-full text-[10px] font-bold flex items-center gap-1 animate-pulse"
                >
                    <ShieldAlert size={12} />
                    CAPACITY EXCEEDED
                </div>
            {/if}

            <div
                class="w-full h-32 flex items-end gap-[2px] z-10 mt-12 relative"
            >
                <!-- Limit Line -->
                {#if peakCapacity > 0}
                    <div
                        class="absolute w-full border-t border-dashed border-emerald-500/30 line-limit"
                        style="bottom: {Math.min(
                            100,
                            (peakCapacity / (peakCapacity * 1.5)) * 100,
                        )}%;"
                    >
                        <span
                            class="absolute right-0 -top-4 text-[8px] text-emerald-500 font-mono"
                            >100% CAP</span
                        >
                    </div>
                {/if}

                {#each timeSeries as val}
                    {@const heightPct = Math.min(
                        100,
                        (val / (peakCapacity * 1.5 || 1)) * 100,
                    )}
                    {@const isOverload = val > peakCapacity}
                    <div
                        class="flex-1 rounded-t-sm transition-all duration-75 {isOverload
                            ? 'bg-red-500'
                            : 'bg-[#22d3ee]'}"
                        style="height: {heightPct}%; min-height: 1px;"
                    ></div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Results Overlay -->
    {#if testResults}
        <div
            class="mt-6 pt-6 border-t border-white/10 grid grid-cols-3 gap-4"
            in:fade
        >
            <div class="bg-black/20 rounded-xl p-3 border border-white/5">
                <div
                    class="text-[9px] text-white/40 uppercase font-bold tracking-widest mb-1"
                >
                    Max Sustained Load
                </div>
                <div
                    class="text-xl font-black font-mono {testResults.success
                        ? 'text-emerald-400'
                        : 'text-red-400'}"
                >
                    {testResults.maxSustained.toLocaleString()} Dpk/s
                </div>
            </div>
            <div class="bg-black/20 rounded-xl p-3 border border-white/5">
                <div
                    class="text-[9px] text-white/40 uppercase font-bold tracking-widest mb-1"
                >
                    Packet Loss
                </div>
                <div
                    class="text-xl font-black font-mono {testResults.success
                        ? 'text-emerald-400'
                        : 'text-red-400'}"
                >
                    {testResults.packetLoss}
                </div>
            </div>
            <div class="bg-black/20 rounded-xl p-3 border border-white/5">
                <div
                    class="text-[9px] text-white/40 uppercase font-bold tracking-widest mb-1"
                >
                    Avg Latency
                </div>
                <div
                    class="text-xl font-black font-mono {testResults.success
                        ? 'text-emerald-400'
                        : 'text-red-400'}"
                >
                    {testResults.latencyAvg}
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .grid-bg {
        background-size: 20px 20px;
        background-image: linear-gradient(
                to right,
                rgba(255, 255, 255, 0.1) 1px,
                transparent 1px
            ),
            linear-gradient(
                to bottom,
                rgba(255, 255, 255, 0.1) 1px,
                transparent 1px
            );
    }
</style>
