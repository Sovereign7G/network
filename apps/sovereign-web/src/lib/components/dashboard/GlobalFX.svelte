<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade } from "svelte/transition";

    const fx = $derived(manifold.visualFX);
</script>

<!-- Ambient State Depth -->
{#if manifold.web3.isConnected}
    <div
        class="ambient-aura"
        style="background: radial-gradient(circle at 50% 110%, rgba(34, 211, 238, 0.12) 0%, transparent 70%);"
        in:fade={{ duration: 2000 }}
    ></div>
{/if}

<!-- Protocol Glitch Layer -->
{#if fx.glitchActive}
    <div class="glitch-overlay" in:fade={{ duration: 150 }}>
        <div class="noise-grain"></div>
        <div class="glitch-chromatic"></div>

        <!-- Scanlines -->
        <div class="scanline sl-1"></div>
        <div class="scanline sl-2"></div>
    </div>
{/if}

<!-- Institutional Panic Layer -->
{#if fx.panicOverlay}
    <div class="panic-overlay" in:fade={{ duration: 400 }}>
        <div class="panic-vignette"></div>
        <div class="panic-border"></div>
    </div>
{/if}

<style>
    .ambient-aura {
        position: fixed;
        inset: 0;
        z-index: -1;
        pointer-events: none;
        transition: all 1.5s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .glitch-overlay {
        position: fixed;
        inset: 0;
        z-index: 10000;
        pointer-events: none;
        overflow: hidden;
    }

    .noise-grain {
        position: absolute;
        inset: -100%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.05;
        animation: noise 0.2s steps(2) infinite;
    }

    .glitch-chromatic {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to bottom,
            rgba(34, 211, 238, 0.1),
            transparent,
            rgba(244, 63, 94, 0.1)
        );
        mix-blend-mode: screen;
        animation: pulse 4s ease-in-out infinite;
    }

    .scanline {
        position: absolute;
        width: 100%;
        height: 1px;
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }

    .sl-1 {
        animation: scanline 3s linear infinite;
    }
    .sl-2 {
        animation: scanline 5s linear infinite 1s;
    }

    .panic-overlay {
        position: fixed;
        inset: 0;
        z-index: 10001;
        pointer-events: none;
    }

    .panic-vignette {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle,
            transparent 40%,
            rgba(244, 63, 94, 0.15) 100%
        );
    }

    .panic-border {
        position: absolute;
        inset: 0;
        border: 24px solid rgba(244, 63, 94, 0.1);
        animation: panicPulse 1.5s ease-in-out infinite;
    }

    @keyframes noise {
        0% {
            transform: translate(0, 0);
        }
        10% {
            transform: translate(-5%, -5%);
        }
        20% {
            transform: translate(-10%, 5%);
        }
        30% {
            transform: translate(5%, -10%);
        }
        40% {
            transform: translate(-5%, 15%);
        }
        50% {
            transform: translate(-10%, 5%);
        }
        60% {
            transform: translate(15%, 0);
        }
        70% {
            transform: translate(0, 10%);
        }
        80% {
            transform: translate(-15%, 0);
        }
        90% {
            transform: translate(10%, 5%);
        }
        100% {
            transform: translate(5%, 0);
        }
    }

    @keyframes scanline {
        from {
            transform: translateY(-100vh);
        }
        to {
            transform: translateY(100vh);
        }
    }

    @keyframes panicPulse {
        0%,
        100% {
            opacity: 0.5;
            border-width: 24px;
        }
        50% {
            opacity: 1;
            border-width: 40px;
        }
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 0.3;
        }
        50% {
            opacity: 0.6;
        }
    }
</style>
