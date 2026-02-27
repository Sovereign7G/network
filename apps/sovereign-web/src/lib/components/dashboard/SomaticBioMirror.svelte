<script lang="ts">
    import { onMount } from "svelte";
    import { fade, scale } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import {
        Activity,
        Heart,
        ShieldCheck,
        RefreshCw,
        ArrowUpRight,
        Moon,
        Sun,
        Droplets,
        Thermometer,
    } from "lucide-svelte";

    let vitals: any = $state(null);
    let isLoading = $state(true);
    let moralCreditYield = $state(0.024);

    onMount(async () => {
        // Simulate bio-sync
        setTimeout(() => {
            vitals = {
                energy: { score: 88, level: "HIGH" },
                movement: { steps: 12420, goal: 15000 },
                sleep: { duration: "7.5h", quality: "EXCELLENT" },
                resonance: 94.2,
                temp: 36.6,
                hydration: 82,
            };
            isLoading = false;
        }, 1200);
    });

    function getPulseColor(score: number) {
        if (score > 80) return "#10b981";
        if (score > 50) return "#22d3ee";
        return "#f43f5e";
    }
</script>

<div class="bio-mirror-shell">
    <!-- Institutional Header -->
    <header class="bio-header">
        <div class="header-brand">
            <div class="logo-box">
                <Heart size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Somatic_Bio-Mirror</h2>
                <div class="flex items-center gap-2">
                    <span class="resonance-label"
                        >Resonance: {vitals?.resonance || "--"}%</span
                    >
                    <div class="resonance-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry text-right">
            <span class="tel-label">MORAL_YIELD_BOOST</span>
            <div class="flex items-center gap-2 justify-end">
                <ArrowUpRight size={12} class="text-emerald-400" />
                <span class="tel-value text-emerald-400"
                    >+{moralCreditYield}%_PF</span
                >
            </div>
        </div>
    </header>

    <div class="bio-body">
        <!-- Ambient Bio-Atmosphere -->
        <div class="bio-aura"></div>

        {#if isLoading}
            <div class="loading-vessel" in:fade>
                <div class="sync-spinner">
                    <RefreshCw size={40} class="animate-spin text-white/10" />
                </div>
                <p class="sync-label">Syncing_Bio-Shards...</p>
            </div>
        {:else if vitals}
            <!-- Kinetic Bio-Rhythm -->
            <div
                class="bio-visualizer"
                in:scale={{ duration: 800, easing: cubicOut }}
            >
                <div class="visualizer-rings">
                    <svg viewBox="0 0 200 200" class="ring-svg">
                        <circle cx="100" cy="100" r="90" class="ring-track" />
                        <circle cx="100" cy="100" r="75" class="ring-track" />
                        <circle cx="100" cy="100" r="60" class="ring-track" />

                        <!-- Energy Ring -->
                        <circle
                            cx="100"
                            cy="100"
                            r="90"
                            class="ring-progress"
                            style="stroke: {getPulseColor(
                                vitals.energy.score,
                            )}; stroke-dasharray: 565; stroke-dashoffset: {565 *
                                (1 - vitals.energy.score / 100)}"
                        />
                        <!-- Movement Ring -->
                        <circle
                            cx="100"
                            cy="100"
                            r="75"
                            class="ring-progress opacity-60"
                            style="stroke: #34d399; stroke-dasharray: 471; stroke-dashoffset: {471 *
                                (1 -
                                    vitals.movement.steps /
                                        vitals.movement.goal)}"
                        />
                        <!-- Hydration Ring -->
                        <circle
                            cx="100"
                            cy="100"
                            r="60"
                            class="ring-progress opacity-40"
                            style="stroke: #22d3ee; stroke-dasharray: 377; stroke-dashoffset: {377 *
                                (1 - vitals.hydration / 100)}"
                        />
                    </svg>

                    <div class="core-heart">
                        <Activity size={44} class="text-white animate-pulse" />
                        <div class="core-metrics">
                            <span class="m-value">{vitals.energy.score}</span>
                            <span class="m-label">Bio_Vigor</span>
                        </div>
                    </div>
                </div>

                <!-- Floating Metrics Overlay -->
                <div class="floating-vitals f-left">
                    <div class="v-pill">
                        <Thermometer size={14} class="text-rose-400" />
                        <span>{vitals.temp}°C</span>
                    </div>
                </div>
                <div class="floating-vitals f-right">
                    <div class="v-pill">
                        <Droplets size={14} class="text-cyan-400" />
                        <span>{vitals.hydration}% H2O</span>
                    </div>
                </div>
            </div>

            <!-- Detailed Metrics Matrix -->
            <div class="bio-stats-grid">
                <div class="stat-card">
                    <div class="card-icon c-amber">
                        <Moon size={20} />
                    </div>
                    <div class="card-info">
                        <span class="c-label">Sleep_Coherence</span>
                        <div class="c-value-row">
                            <span class="c-value">{vitals.sleep.duration}</span>
                            <span class="c-tag tag-emerald"
                                >{vitals.sleep.quality}</span
                            >
                        </div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-icon c-cyan">
                        <Sun size={20} />
                    </div>
                    <div class="card-info">
                        <span class="c-label">Active_Metabolism</span>
                        <div class="c-value-row">
                            <span class="c-value"
                                >{vitals.movement.steps.toLocaleString()}</span
                            >
                            <span class="c-tag">STEPS</span>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <!-- Assurance Footer -->
    <footer class="bio-footer">
        <div class="assurance-block">
            <ShieldCheck size={18} class="text-emerald-400" />
            <div class="flex flex-col">
                <span class="a-title">Identity_Shard_Lock: ACTIVE</span>
                <span class="a-meta">Biometric Veracity: 99.99_ZK</span>
            </div>
        </div>
        <button class="yield-btn"> Claim_Moral_Yield </button>
    </footer>
</div>

<style>
    .bio-mirror-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
    }

    .bio-header {
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .logo-box {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #10b981, #34d399);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .resonance-label {
        font-size: 8px;
        font-weight: 800;
        color: #34d399;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-style: italic;
    }

    .resonance-pulsar {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 1s infinite;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
        margin-bottom: 4px;
        display: block;
    }

    .tel-value {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .bio-body {
        flex: 1;
        padding: 3rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .bio-aura {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at center,
            rgba(16, 185, 129, 0.08),
            transparent 70%
        );
        pointer-events: none;
        animation: breath 8s infinite ease-in-out;
    }

    .loading-vessel {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }

    .sync-label {
        font-size: 10px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.3em;
    }

    .bio-visualizer {
        position: relative;
        width: 320px;
        height: 320px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .visualizer-rings {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .ring-svg {
        position: absolute;
        width: 100%;
        height: 100%;
        transform: rotate(-90deg);
    }

    .ring-track {
        fill: none;
        stroke: rgba(255, 255, 255, 0.03);
        stroke-width: 4;
    }

    .ring-progress {
        fill: none;
        stroke-width: 8;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .core-heart {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        z-index: 10;
    }

    .core-metrics {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .m-value {
        font-size: 48px;
        font-weight: 950;
        color: white;
        letter-spacing: -0.05em;
        line-height: 1;
    }

    .m-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .floating-vitals {
        position: absolute;
        z-index: 5;
    }

    .f-left {
        left: -40px;
        top: 80px;
    }
    .f-right {
        right: -40px;
        bottom: 80px;
    }

    .v-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 8px 16px;
        border-radius: 100px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 10px;
        font-weight: 950;
        color: white;
    }

    .bio-stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        width: 100%;
        margin-top: 4rem;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 28px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.25rem;
        transition: all 0.3s;
    }

    .stat-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
    }

    .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .c-amber {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
    }
    .c-cyan {
        background: rgba(6, 182, 212, 0.1);
        color: #06b6d4;
    }

    .card-info {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .c-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .c-value-row {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
    }

    .c-value {
        font-size: 16px;
        font-weight: 950;
        color: white;
    }

    .c-tag {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
    }

    .tag-emerald {
        color: #10b981;
    }

    .bio-footer {
        padding: 2rem 3rem;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .assurance-block {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .a-title {
        font-size: 9px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .a-meta {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .yield-btn {
        padding: 0.75rem 1.5rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 12px;
        color: #10b981;
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.3s;
    }

    .yield-btn:hover {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.05);
        }
    }
    @keyframes breath {
        0%,
        100% {
            opacity: 0.05;
            transform: scale(0.9);
        }
        50% {
            opacity: 0.15;
            transform: scale(1.1);
        }
    }
</style>
