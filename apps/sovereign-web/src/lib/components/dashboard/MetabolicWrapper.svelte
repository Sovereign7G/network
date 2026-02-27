<script lang="ts">
    import { designEngineering } from "$lib/services/design-engineering-engine.svelte";

    let { children } = $props();

    const metabolicClass = $derived(
        `metabolic-${designEngineering.metabolicState.toLowerCase()}`,
    );
    const kineticClass = $derived(
        designEngineering.isHardwareAccelerated ? "kinetic-accelerated" : "",
    );

    // Da Vinci: Chiaroscuro — Light source shifts with metabolic state
    const lightColor = $derived.by(() => {
        switch (designEngineering.metabolicState) {
            case "GRACE":
                return "0, 163, 108"; // Jade warmth
            case "CAUTION":
                return "245, 158, 11"; // Amber warning
            case "EMERGENCY":
                return "0, 0, 0"; // Absence of light
            default:
                return "34, 211, 238"; // Cool cyan
        }
    });

    const lightIntensity = $derived(
        designEngineering.metabolicState === "EMERGENCY" ? 0 : 0.04,
    );
</script>

<div class="metabolic-manifold {metabolicClass} {kineticClass}">
    <!-- Da Vinci I: CHIAROSCURO — Dynamic Light Source -->
    <div
        class="chiaroscuro-source"
        style="
            --light-rgb: {lightColor};
            --light-intensity: {lightIntensity};
        "
    ></div>

    <!-- Da Vinci II: SFUMATO — Atmospheric Depth Veils -->
    <div class="sfumato-layer">
        <div class="sfumato-veil sfumato-veil-near"></div>
        <div class="sfumato-veil sfumato-veil-mid"></div>
        <div class="sfumato-veil sfumato-veil-far"></div>
    </div>

    <!-- Content Substrate -->
    {@render children()}

    <!-- Da Vinci III: SENSORY OVERLAY — State-Specific Atmosphere -->
    <div class="sensory-overlay">
        {#if designEngineering.metabolicState === "GRACE"}
            <div class="grace-crystallization"></div>
            <div class="golden-spiral-overlay"></div>
            <div class="grace-vein grace-vein-1"></div>
            <div class="grace-vein grace-vein-2"></div>
            <div class="grace-vein grace-vein-3"></div>
        {/if}
        {#if designEngineering.metabolicState === "EMERGENCY"}
            <div class="emergency-static"></div>
            <div class="emergency-vignette"></div>
        {/if}
        {#if designEngineering.metabolicState === "CAUTION"}
            <div class="caution-perimeter"></div>
        {/if}
    </div>

    <!-- Da Vinci IV: CONTRAPPOSTO — Breathing Heartbeat -->
    <div class="contrapposto-pulse"></div>
</div>

<style>
    .metabolic-manifold {
        min-height: 100vh;
        width: 100%;
        position: relative;
        transition:
            filter 2s cubic-bezier(0.16, 1, 0.3, 1),
            background 2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* 🎨 CHIAROSCURO — Dynamic Light Source                          */
    /* ═══════════════════════════════════════════════════════════════ */
    .chiaroscuro-source {
        position: fixed;
        top: -20%;
        left: -10%;
        width: 60%;
        height: 60%;
        background: radial-gradient(
            ellipse at center,
            rgba(var(--light-rgb), var(--light-intensity)) 0%,
            rgba(var(--light-rgb), calc(var(--light-intensity) * 0.3)) 40%,
            transparent 70%
        );
        pointer-events: none;
        z-index: 1;
        mix-blend-mode: screen;
        transition: all 3s cubic-bezier(0.16, 1, 0.3, 1);
        animation: chiaroscuro-breathe 12s ease-in-out infinite alternate;
    }

    @keyframes chiaroscuro-breathe {
        0% {
            transform: translate(0, 0) scale(1);
            opacity: 0.7;
        }
        50% {
            transform: translate(5%, 3%) scale(1.05);
            opacity: 1;
        }
        100% {
            transform: translate(-2%, 5%) scale(0.98);
            opacity: 0.8;
        }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* 🌫️ SFUMATO — Atmospheric Depth Veils                           */
    /* ═══════════════════════════════════════════════════════════════ */
    .sfumato-layer {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 2;
        mix-blend-mode: soft-light;
    }

    .sfumato-veil {
        position: absolute;
        inset: 0;
        border-radius: 50%;
    }

    /* Near veil — tight, warm, focused */
    .sfumato-veil-near {
        background: radial-gradient(
            ellipse at 50% 40%,
            rgba(255, 255, 255, 0.008) 0%,
            transparent 50%
        );
        animation: sfumato-near 10s ease-in-out infinite alternate;
    }

    /* Mid veil — diffuse, organic movement */
    .sfumato-veil-mid {
        background: radial-gradient(
            ellipse at 30% 70%,
            rgba(255, 255, 255, 0.005) 0%,
            transparent 60%
        );
        animation: sfumato-mid 14s ease-in-out infinite alternate-reverse;
    }

    /* Far veil — atmospheric haze at the edges */
    .sfumato-veil-far {
        background: radial-gradient(
            ellipse at 80% 20%,
            rgba(255, 255, 255, 0.003) 0%,
            transparent 70%
        );
        animation: sfumato-far 18s ease-in-out infinite alternate;
    }

    @keyframes sfumato-near {
        from {
            transform: scale(0.95) translate(0, 0);
        }
        to {
            transform: scale(1.05) translate(2%, 3%);
        }
    }
    @keyframes sfumato-mid {
        from {
            transform: scale(1.1) translate(-3%, 2%);
        }
        to {
            transform: scale(0.9) translate(5%, -2%);
        }
    }
    @keyframes sfumato-far {
        from {
            transform: scale(1.2) translate(2%, -3%);
        }
        to {
            transform: scale(0.85) translate(-4%, 4%);
        }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* ✨ SENSORY OVERLAY — State-Specific Atmosphere                 */
    /* ═══════════════════════════════════════════════════════════════ */
    .sensory-overlay {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 10000;
    }

    /* GRACE: Jade crystallization veins propagating across glass */
    .grace-crystallization {
        position: absolute;
        inset: 0;
        background: radial-gradient(
                circle at 10% 90%,
                rgba(0, 163, 108, 0.04) 0%,
                transparent 40%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0, 163, 108, 0.03) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 50% 50%,
                rgba(0, 163, 108, 0.02) 0%,
                transparent 60%
            );
        animation: grace-crystallize 10s ease-in-out infinite alternate;
    }

    .grace-vein {
        position: absolute;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(0, 163, 108, 0.15),
            transparent
        );
        animation: vein-propagate 8s ease-in-out infinite;
    }

    .grace-vein-1 {
        top: 30%;
        left: 0;
        width: 100%;
        animation-delay: 0s;
    }
    .grace-vein-2 {
        top: 55%;
        left: 0;
        width: 100%;
        animation-delay: 2.5s;
        transform: rotate(0.5deg);
    }
    .grace-vein-3 {
        top: 78%;
        left: 0;
        width: 100%;
        animation-delay: 5s;
        transform: rotate(-0.3deg);
    }

    @keyframes grace-crystallize {
        from {
            opacity: 0.3;
            filter: blur(0px);
        }
        to {
            opacity: 0.7;
            filter: blur(1px);
        }
    }

    @keyframes vein-propagate {
        0% {
            transform: scaleX(0);
            transform-origin: left;
            opacity: 0;
        }
        30% {
            transform: scaleX(1);
            opacity: 0.6;
        }
        70% {
            transform: scaleX(1);
            opacity: 0.3;
        }
        100% {
            transform: scaleX(0);
            transform-origin: right;
            opacity: 0;
        }
    }

    /* EMERGENCY: Oxygen leaving the room */
    .emergency-static {
        position: absolute;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.04;
        mix-blend-mode: color-burn;
        animation: static-flicker 0.15s steps(3) infinite;
    }

    .emergency-vignette {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            ellipse at center,
            transparent 40%,
            rgba(0, 0, 0, 0.4) 100%
        );
        animation: vignette-close 4s ease-in-out infinite alternate;
    }

    @keyframes static-flicker {
        0% {
            opacity: 0.03;
        }
        50% {
            opacity: 0.05;
        }
        100% {
            opacity: 0.02;
        }
    }

    @keyframes vignette-close {
        from {
            background-size: 150% 150%;
        }
        to {
            background-size: 120% 120%;
        }
    }

    /* CAUTION: Amber perimeter warning */
    .caution-perimeter {
        position: absolute;
        inset: 0;
        border: 1px solid rgba(245, 158, 11, 0.08);
        box-shadow:
            inset 0 0 80px rgba(245, 158, 11, 0.02),
            inset 0 0 200px rgba(245, 158, 11, 0.01);
        animation: caution-border-pulse 4s ease-in-out infinite;
    }

    @keyframes caution-border-pulse {
        0%,
        100% {
            border-color: rgba(245, 158, 11, 0.05);
        }
        50% {
            border-color: rgba(245, 158, 11, 0.12);
        }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* 💓 CONTRAPPOSTO — Breathing Heartbeat                          */
    /* ═══════════════════════════════════════════════════════════════ */
    .contrapposto-pulse {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40%;
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(var(--light-rgb, 34, 211, 238), 0.15),
            transparent
        );
        z-index: 10001;
        animation: heartbeat-line 5s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes heartbeat-line {
        0%,
        100% {
            transform: translateX(-50%) scaleX(0.6);
            opacity: 0.3;
        }
        15% {
            transform: translateX(-50%) scaleX(1);
            opacity: 0.8;
        }
        25% {
            transform: translateX(-50%) scaleX(0.8);
            opacity: 0.5;
        }
        35% {
            transform: translateX(-50%) scaleX(0.95);
            opacity: 0.7;
        }
        50% {
            transform: translateX(-50%) scaleX(0.7);
            opacity: 0.4;
        }
    }
</style>
