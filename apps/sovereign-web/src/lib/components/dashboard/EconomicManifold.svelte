<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { TrendingUp, ShieldCheck, Globe, Lock, Coins, Zap, Activity } from "lucide-svelte";

    // Link to real manifold state
    let vault = $derived(manifold.vaultState);
    let stable = $derived(manifold.stablecoinState);
    let yieldRate = $derived(manifold.forensicYieldState.total.toFixed(2));
    let moralDividend = $state(0.084); // Institutional baseline
    let planetaryLiquidity = $derived(vault.totalValueLockedUsd);
    let mosaicIndex = $state(92.4);

    onMount(() => {
        const interval = setInterval(() => {
            mosaicIndex = Math.min(
                100,
                Math.max(80, mosaicIndex + (Math.random() - 0.5) * 0.2),
            );
        }, 3000);
        return () => clearInterval(interval);
    });

    function formatCurrency(val: number) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            notation: "compact",
            maximumFractionDigits: 1,
        }).format(val);
    }
</script>

<div class="manifold-shell" in:fade>
    <!-- Background Gradient Aura -->
    <div class="manifold-aura"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="header-brand">
            <div class="logo-box">
                <Globe size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Protocol_State_Manifold</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label">COHERENCE_STABLE</span>
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block text-right">
                <span class="tel-label">SYSTEM_TVL</span>
                <div class="flex items-center gap-1 justify-end">
                    <TrendingUp size={10} class="text-emerald-400" />
                    <span class="tel-value text-emerald-400"
                        >{formatCurrency(planetaryLiquidity)}</span
                    >
                </div>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block text-right">
                <span class="tel-label">ALGORITHMIC_YIELD</span>
                <div class="flex items-center gap-1 justify-end">
                    <Zap size={10} class="text-cyan-400" />
                    <span class="tel-value text-cyan-400">{yieldRate}%</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Orbital Economic Visualizer -->
    <div class="manifold-viz-area">
        <div class="orbital-vessel">
            <!-- Structural Geometry -->
            <div class="ring r-1"></div>
            <div class="ring r-2"></div>
            <div class="ring r-3"></div>

            <!-- Central Liquidity Core -->
            <div class="manifold-core">
                <div class="core-glow"></div>
                <div class="core-inner">
                    <ShieldCheck size={24} class="text-cyan-400/60" />
                    <div class="pulse-ring"></div>
                </div>
            </div>

            <!-- Orbiting Capital Shards -->
            <div class="shard-belt animate-spin-slow">
                <div class="shard-vessel shard-1">
                    <div class="shard-box">
                        <Coins size={14} class="text-white" />
                    </div>
                    <span class="shard-label">AGE_CORE</span>
                </div>
            </div>

            <div class="shard-belt animate-spin-reverse delay-1000">
                <div class="shard-vessel shard-2">
                    <div class="shard-box accent-emerald">
                        <Zap size={14} />
                    </div>
                    <span class="shard-label label-emerald">RES_STABLE</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Institutional Gauges -->
    <div class="manifold-gauges">
        <section class="gauge-card">
            <header class="g-header">
                <div class="g-title">
                    <div class="g-icon bg-emerald">
                        <TrendingUp size={12} />
                    </div>
                    <span>Moral_Dividend</span>
                </div>
                <span class="g-value text-emerald"
                    >{(moralDividend * 100).toFixed(1)}%</span
                >
            </header>
            <div class="progress-track">
                <div
                    class="progress-fill fill-emerald"
                    style="width: {moralDividend * 100}%"
                ></div>
            </div>
            <footer class="g-footer">
                <span>AAL3 COMPLIANT</span>
                <span class="text-emerald-400/40">PHASE 2</span>
            </footer>
        </section>

        <section class="gauge-card">
            <header class="g-header">
                <div class="g-title">
                    <div class="g-icon bg-cyan">
                        <Lock size={12} />
                    </div>
                    <span>Parity_Index</span>
                </div>
                <span class="g-value text-cyan">{stable.parity.toFixed(4)}</span
                >
            </header>
            <div class="parity-map">
                {#each Array(4) as _, i}
                    <div
                        class="map-dot"
                        class:active={i < 3 || stable.parity > 0.99}
                        class:error={i === 3 && stable.parity <= 0.99}
                    ></div>
                {/each}
            </div>
            <footer class="g-footer">
                <span>{stable.status}</span>
                <span class="text-cyan-400/40">ALGORITHMIC</span>
            </footer>
        </section>
    </div>

    <!-- Protocol Footer -->
    <footer class="manifold-footer">
        <div class="footer-assurance">
            <Activity size={10} class="text-white/20" />
            <span>Validated by DaVinci_v5 // Basel IV Protocol</span>
        </div>
        <div class="footer-status">
            <div class="status-pulsar shadow-cyan"></div>
            <span class="text-cyan-400/80">LIVE_MANIFOLD</span>
        </div>
    </footer>
</div>

<style>
    .manifold-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
        position: relative;
    }

    .manifold-aura {
        position: absolute;
        top: 0;
        right: 0;
        width: 320px;
        height: 320px;
        background: radial-gradient(
            circle,
            rgba(34, 211, 238, 0.05) 0%,
            transparent 70%
        );
        pointer-events: none;
    }

    .manifold-header {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logo-box {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(6, 182, 212, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .phase-label {
        font-size: 8px;
        font-weight: 800;
        color: #22d3ee;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .phase-pulsar {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    .header-telemetry {
        display: flex;
        gap: 1.5rem;
    }

    .tel-block {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
    }

    .tel-value {
        font-size: 13px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .tel-divider {
        width: 1px;
        height: 24px;
        background: rgba(255, 255, 255, 0.05);
    }

    .manifold-viz-area {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .orbital-vessel {
        position: relative;
        width: 256px;
        height: 256px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .ring {
        position: absolute;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 50%;
    }

    .r-1 {
        width: 256px;
        height: 256px;
    }
    .r-2 {
        width: 192px;
        height: 192px;
    }
    .r-3 {
        width: 128px;
        height: 128px;
    }

    .manifold-core {
        position: relative;
        z-index: 10;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .core-glow {
        position: absolute;
        inset: -10px;
        background: #22d3ee;
        filter: blur(20px);
        opacity: 0.1;
        border-radius: 50%;
    }

    .core-inner {
        width: 64px;
        height: 64px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .pulse-ring {
        position: absolute;
        inset: 0;
        background: rgba(34, 211, 238, 0.1);
        border-radius: 50%;
        animation: pulse-ring 2s infinite;
    }

    @keyframes pulse-ring {
        0% {
            transform: scale(1);
            opacity: 0.5;
        }
        100% {
            transform: scale(1.5);
            opacity: 0;
        }
    }

    .shard-belt {
        position: absolute;
        inset: 0;
        pointer-events: none;
    }

    .shard-vessel {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .shard-1 {
        top: 12px;
        left: 50%;
        transform: translateX(-50%);
    }
    .shard-2 {
        bottom: 12px;
        right: 12px;
    }

    .shard-box {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .shard-box.accent-emerald {
        background: rgba(16, 185, 129, 0.05);
        border-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }

    .shard-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .shard-label.label-emerald {
        color: rgba(16, 185, 129, 0.4);
    }

    .manifold-gauges {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        padding: 0 2rem 2rem;
    }

    .gauge-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .g-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .g-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 10px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
    }

    .g-icon {
        width: 24px;
        height: 24px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .bg-emerald {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    .bg-cyan {
        background: rgba(34, 211, 238, 0.1);
        color: #22d3ee;
    }

    .g-value {
        font-size: 13px;
        font-weight: 950;
    }

    .progress-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .fill-emerald {
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
    }

    .parity-map {
        display: flex;
        gap: 4px;
        height: 4px;
    }

    .map-dot {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        transition: all 0.5s;
    }

    .map-dot.active {
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
    }
    .map-dot.error {
        background: #ef4444;
        box-shadow: 0 0 10px #ef4444;
    }

    .g-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .manifold-footer {
        padding: 1.25rem 2rem;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .footer-assurance {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .footer-status {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .status-pulsar {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }

    .shadow-cyan {
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.2);
        }
    }

    .animate-spin-slow {
        animation: spin 40s linear infinite;
    }
    .animate-spin-reverse {
        animation: spin 30s linear infinite reverse;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
