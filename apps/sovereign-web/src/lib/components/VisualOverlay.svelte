<script lang="ts">
    import { onMount } from "svelte";
    import { systemHealth } from "$lib/stores/master-store";

    let mousePosition = { x: 0, y: 0 };
    let scanlineOffset = 0;

    onMount(() => {
        // Track mouse for overlay effects

        const handleMouseMove = (e) => {
            mousePosition = { x: e.clientX, y: e.clientY };
        };

        // Animate scanline
        const scanlineInterval = setInterval(() => {
            scanlineOffset = (scanlineOffset + 1) % 100;
        }, 50);

        window.addEventListener("mousemove", handleMouseMove);

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            clearInterval(scanlineInterval);
        };
    });

    $: isQuietMode = $systemHealth?.quietMode || false;
</script>

<div class="visual-overlay" class:quiet-mode={isQuietMode}>
    <!-- Grid overlay -->
    <div class="grid-overlay"></div>

    <!-- Scanline effect -->
    <div
        class="scanline"
        style="transform: translateY({scanlineOffset}vh);"
    ></div>

    <!-- Mouse glow -->
    <div
        class="mouse-glow"
        style="left: {mousePosition.x}px; top: {mousePosition.y}px;"
    ></div>

    <!-- Corner accents -->
    <div class="corner top-left"></div>
    <div class="corner top-right"></div>
    <div class="corner bottom-left"></div>
    <div class="corner bottom-right"></div>

    <!-- Static noise (subtle) -->
    <div class="noise"></div>
</div>

<style>
    .visual-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 9999;
        opacity: 0.3;
        transition: opacity 0.5s;
    }

    .visual-overlay.quiet-mode {
        opacity: 0.1;
    }

    .grid-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: linear-gradient(
                rgba(147, 112, 219, 0.05) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(147, 112, 219, 0.05) 1px,
                transparent 1px
            );
        background-size: 50px 50px;
    }

    .scanline {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(147, 112, 219, 0.2),
            rgba(255, 107, 107, 0.2),
            transparent
        );
        opacity: 0.5;
        animation: scan 8s linear infinite;
    }

    @keyframes scan {
        0% {
            transform: translateY(0);
        }
        100% {
            transform: translateY(100vh);
        }
    }

    .mouse-glow {
        position: absolute;
        width: 200px;
        height: 200px;
        background: radial-gradient(
            circle,
            rgba(147, 112, 219, 0.1) 0%,
            transparent 70%
        );
        transform: translate(-50%, -50%);
        pointer-events: none;
    }

    .corner {
        position: absolute;
        width: 50px;
        height: 50px;
        border-style: solid;
        border-color: rgba(147, 112, 219, 0.3);
        border-width: 0;
    }

    .corner.top-left {
        top: 20px;
        left: 20px;
        border-top-width: 2px;
        border-left-width: 2px;
    }

    .corner.top-right {
        top: 20px;
        right: 20px;
        border-top-width: 2px;
        border-right-width: 2px;
    }

    .corner.bottom-left {
        bottom: 20px;
        left: 20px;
        border-bottom-width: 2px;
        border-left-width: 2px;
    }

    .corner.bottom-right {
        bottom: 20px;
        right: 20px;
        border-bottom-width: 2px;
        border-right-width: 2px;
    }

    .noise {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48ZmlsdGVyIGlkPSJmIj48ZmVUdXJidWxlbmNlIHR5cGU9ImZyYWN0YWxOb2lzZSIgYmFzZUZyZXF1ZW5jeT0iLjc0IiBudW1PY3RhdmVzPSIzIiAvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbHRlcj0idXJsKCNmKSIgb3BhY2l0eT0iMC4wNCIgLz48L3N2Zz4=");
        opacity: 0.02;
        pointer-events: none;
    }
</style>
