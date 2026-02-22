<script lang="ts">
    import {
        Brain,
        Activity,
        Clock,
        ShieldAlert,
        Zap,
        Fingerprint,
        Lock,
        Accessibility,
        BarChart3,
    } from "lucide-svelte";
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";

    let cognitiveLoad = $state(24.5);
    let decisionDensity = $state(12);
    let focusScore = $state(98);
    let uptime = $state("14:22:05");
    let identityStatus = $state("AAL3_VERIFIED");
    let isClinicalMode = $state(true);

    // Simulate real-time shift in "Wellbeing" metrics
    onMount(() => {
        const interval = setInterval(() => {
            cognitiveLoad = Math.max(
                10,
                Math.min(90, cognitiveLoad + (Math.random() * 4 - 2)),
            );
            decisionDensity = Math.max(
                5,
                Math.min(50, decisionDensity + (Math.random() * 2 - 1)),
            );

            // Randomly update uptime
            const now = new Date();
            uptime = now.toTimeString().split(" ")[0];
        }, 3000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="glass-panel p-8 bg-[#04060b]/60 border-white/[0.04] space-y-10 relative overflow-hidden group"
    in:fly={{ y: 20, duration: 800 }}
>
    <!-- Background Gradient Pulse (Clinic Grade) -->
    <div
        class="absolute -right-20 -top-20 w-64 h-64 bg-[#24AE7C]/5 rounded-full blur-[100px] group-hover:bg-[#24AE7C]/10 transition-all duration-1000"
    ></div>

    <header class="flex items-center justify-between">
        <div class="space-y-1">
            <h3
                class="text-[10px] font-black uppercase tracking-[0.4em] text-white/60"
            >
                INSTITUTIONAL_TRUST
            </h3>
            <div class="flex items-center gap-2">
                <div
                    class="w-2 h-2 rounded-full bg-[#24AE7C] animate-pulse"
                ></div>
                <span class="text-xs font-black italic"
                    >SOVEREIGN_WELLBEING</span
                >
            </div>
        </div>
        <div class="flex gap-2">
            <button
                class="p-2 bg-white/5 rounded-lg text-white/20 hover:text-white transition-all"
                aria-label="Universal Accessibility Settings"
            >
                <Accessibility size={14} />
            </button>
            <div class="p-2 bg-[#24AE7C]/10 rounded-lg text-[#24AE7C]">
                <Brain size={16} class="animate-pulse" />
            </div>
        </div>
    </header>

    <!-- AAL3 Identity Handshake (PILLAR 1) -->
    <section
        class="p-6 bg-[#24AE7C]/5 border border-[#24AE7C]/10 rounded-3xl space-y-4"
    >
        <div class="flex justify-between items-center">
            <div class="flex items-center gap-3">
                <div
                    class="w-10 h-10 rounded-xl bg-black border border-white/5 flex items-center justify-center text-[#24AE7C]"
                >
                    <Fingerprint size={20} />
                </div>
                <div>
                    <p
                        class="text-[7px] font-black text-white/30 uppercase tracking-widest"
                    >
                        AAL3_IDENTITY_STATUS
                    </p>
                    <p class="text-[10px] font-black text-[#24AE7C] uppercase">
                        {identityStatus}
                    </p>
                </div>
            </div>
            <Lock size={14} class="text-white/20" />
        </div>
        <div class="flex gap-2">
            <div class="h-1 flex-1 bg-[#24AE7C] rounded-full"></div>
            <div class="h-1 flex-1 bg-[#24AE7C] rounded-full"></div>
            <div
                class="h-1 flex-1 bg-[#24AE7C] rounded-full animate-pulse"
            ></div>
        </div>
        <p class="text-[8px] font-bold text-white/40 uppercase tracking-tight">
            Persistent Multi-Layered Authentication Active
        </p>
    </section>

    <!-- Wellbeing Telemetry Models -->
    <div class="space-y-8">
        <!-- Cognitive Load -->
        <div class="space-y-4">
            <div
                class="flex justify-between items-end text-[9px] font-bold uppercase tracking-widest"
            >
                <div class="space-y-1">
                    <span class="text-white/40">COGNITIVE_LOAD</span>
                    <p
                        class="text-xs font-black {cognitiveLoad > 70
                            ? 'text-red-400'
                            : 'text-white'}"
                    >
                        {cognitiveLoad.toFixed(1)}%
                    </p>
                </div>
                <span class="text-[8px] text-white/20">TARGET: &lt; 45%</span>
            </div>
            <div
                class="h-2 w-full bg-black/40 rounded-full overflow-hidden border border-white/5"
            >
                <div
                    class="h-full bg-gradient-to-r from-[#24AE7C] to-emerald-400 transition-all duration-1000 relative"
                    style="width: {cognitiveLoad}%"
                >
                    <div
                        class="absolute inset-0 bg-white/20 animate-pulse"
                    ></div>
                </div>
            </div>
            {#if cognitiveLoad > 70}
                <div
                    class="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl"
                    transition:scale
                >
                    <ShieldAlert size={14} class="text-red-500" />
                    <span class="text-[8px] font-black uppercase text-red-500"
                        >FATIGUE_CRITICAL: IMMEDIATE_COOLDOWN_RECOMMENDED</span
                    >
                </div>
            {/if}
        </div>

        <!-- Decision Density & Focus Score -->
        <div class="grid grid-cols-2 gap-6">
            <div
                class="bg-white/[0.02] border border-white/5 p-6 rounded-[2rem] space-y-3 hover:bg-white/[0.04] transition-all"
            >
                <div class="flex items-center gap-2 text-white/30">
                    <BarChart3 size={14} />
                    <span
                        class="text-[8px] font-black uppercase tracking-widest"
                        >DECISION_DENSITY</span
                    >
                </div>
                <div class="flex items-baseline gap-2">
                    <p class="text-2xl font-black italic tracking-tighter">
                        {decisionDensity.toFixed(0)}
                    </p>
                    <span class="text-[8px] font-bold text-white/20 uppercase"
                        >ops/hr</span
                    >
                </div>
            </div>
            <div
                class="bg-white/[0.02] border border-white/5 p-6 rounded-[2rem] space-y-3 hover:bg-white/[0.04] transition-all"
            >
                <div class="flex items-center gap-2 text-white/30">
                    <Zap size={14} />
                    <span
                        class="text-[8px] font-black uppercase tracking-widest"
                        >RELIABILITY</span
                    >
                </div>
                <div class="flex items-baseline gap-2">
                    <p
                        class="text-2xl font-black italic tracking-tighter text-[#24AE7C]"
                    >
                        {focusScore}%
                    </p>
                    <span class="text-[8px] font-bold text-white/20 uppercase"
                        >PRECISION</span
                    >
                </div>
            </div>
        </div>
    </div>

    <!-- Privacy-First Session Persistence -->
    <footer class="space-y-4 pt-6 border-t border-white/5">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-2 text-white/40">
                <Clock size={12} />
                <span class="text-[8px] font-black uppercase tracking-[0.2em]"
                    >SESSION_HEARTBEAT</span
                >
            </div>
            <span class="text-xs font-black italic mono-font text-[#24AE7C]"
                >{uptime}</span
            >
        </div>
        <div
            class="flex items-center justify-between p-4 bg-black/40 rounded-2xl border border-white/5"
        >
            <div class="flex items-center gap-2">
                <Activity size={12} class="text-white/20" />
                <span
                    class="text-[8px] font-black uppercase tracking-widest text-white/40"
                    >DATA_FOOTPRINT</span
                >
            </div>
            <span
                class="px-3 py-1 bg-[#24AE7C]/10 text-[#24AE7C] border border-[#24AE7C]/20 text-[9px] font-black rounded-lg uppercase italic shadow-[0_0_15px_rgba(36,174,124,0.1)]"
            >
                ZERO_LOCAL_FOOTPRINT
            </span>
        </div>
    </footer>

    <button
        class="w-full py-5 bg-white text-black hover:bg-[#24AE7C] transition-all rounded-2xl text-[10px] font-black uppercase tracking-[0.3em] flex items-center justify-center gap-3 active:scale-95 shadow-xl"
    >
        <Zap size={16} strokeWidth={3} />
        ACTIVATE_BEDTIME_PROTOCOL
    </button>
</div>

<style>
    .glass-panel {
        background: rgba(4, 6, 11, 0.6);
        backdrop-filter: blur(80px);
        box-shadow: 0 50px 100px -20px rgba(0, 0, 0, 0.9);
    }
</style>
