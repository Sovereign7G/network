<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { spring } from "svelte/motion";

    // 1. Spacial interaction variables
    let mousePoint = spring({ x: 0, y: 0 }, { stiffness: 0.05, damping: 0.3 });
    let isHovering = $state(false);

    let container: HTMLElement | null = null;
    let time = $state(0);
    let frameId: number;

    // The "living" beat of the Cathedral
    onMount(() => {
        const animate = () => {
            time = Date.now() / 1000;
            frameId = requestAnimationFrame(animate);
        };
        animate();
    });

    onDestroy(() => {
        if (typeof cancelAnimationFrame !== "undefined") {
            cancelAnimationFrame(frameId);
        }
    });

    function handleMouseMove(e: MouseEvent) {
        if (!container) return;
        const rect = container.getBoundingClientRect();

        // Normalize mouse coordinates (-0.5 to 0.5)
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        mousePoint.set({ x: x * 30, y: y * -30 }); // Degrees of rotation
    }

    function handleMouseEnter() {
        isHovering = true;
    }
    function handleMouseLeave() {
        isHovering = false;
        mousePoint.set({ x: 0, y: 0 });
    }
</script>

<div class="void-space">
    <!-- Generative Starfield / Nebula Background -->
    <div
        class="generative-nebula"
        style="opacity: {0.4 + Math.sin(time * 0.5) * 0.15};"
    ></div>
    <!-- Chiaroscuro dynamic dynamic lighting -->
    <div
        class="chiaroscuro-light"
        style="transform: translate({$mousePoint.x * 10}px, {$mousePoint.y *
            -10}px)"
    ></div>

    <div class="sanctum">
        <header in:fly={{ y: -30, duration: 1500, delay: 200 }}>
            <h1 class="sfumato-text">The Resonance Chamber</h1>
            <p class="subtitle" in:fade={{ duration: 2000, delay: 1000 }}>
                Sovereignty is felt, not just seen.
            </p>
        </header>

        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
            class="spatial-portal {isHovering ? 'hovering' : ''}"
            bind:this={container}
            onmousemove={handleMouseMove}
            onmouseenter={handleMouseEnter}
            onmouseleave={handleMouseLeave}
            style="
                transform: perspective(1500px) 
                           rotateY({$mousePoint.x}deg) 
                           rotateX({$mousePoint.y}deg) 
                           scale({isHovering ? 1.05 : 1});
                box-shadow: {isHovering
                ? `${-$mousePoint.x * 2}px ${$mousePoint.y * 2}px 60px rgba(34,211,238,0.25)`
                : '0 30px 60px rgba(0,0,0,0.5)'};
            "
        >
            <!-- 1. Deepest base layer (Sfumato Depth) -->
            <div class="strata back-layer"></div>

            <!-- 2. Mid glass layer with breathing lattice -->
            <div class="strata glass-layer">
                <div
                    class="breathing-lattice"
                    style="opacity: {0.4 +
                        Math.sin(time) * 0.2}; transform: scale({1 +
                        Math.sin(time * 0.5) * 0.02})"
                ></div>
            </div>

            <!-- 3. Topmost tactile interaction layer -->
            <div class="strata interaction-layer">
                <div class="sacred-geometry">
                    <div
                        class="ring outer-ring"
                        style="transform: rotate({time * 15}deg)"
                    ></div>
                    <div
                        class="ring inner-ring"
                        style="transform: rotate({time * -20}deg)"
                    ></div>
                    <!-- Central breathing crystal representing the soul -->
                    <div
                        class="crystal-core"
                        style="transform: scale({1 +
                            Math.sin(time * 3) * 0.1}); 
                                box-shadow: 0 0 {30 +
                            Math.sin(time * 3) * 20}px rgba(34, 211, 238, {0.6 +
                            Math.sin(time) * 0.4})"
                    ></div>
                </div>

                <div
                    class="metrics"
                    style="transform: translateZ({isHovering ? 40 : 20}px)"
                >
                    <div class="vital-sign">
                        <span class="label">Coherence Matrix</span>
                        <div class="bar-track">
                            <div
                                class="bar-fill cyan"
                                style="width: {88 + Math.sin(time * 4) * 4}%"
                            ></div>
                        </div>
                    </div>
                    <div class="vital-sign">
                        <span class="label">Temporal Resonance</span>
                        <div class="bar-track">
                            <div
                                class="bar-fill amber"
                                style="width: {75 + Math.cos(time * 2.5) * 6}%"
                            ></div>
                        </div>
                    </div>
                </div>

                <!-- Physical Metaphor: Casting a stone into a pool -->
                <button
                    class="cast-stone-btn"
                    style="transform: translateZ({isHovering ? 60 : 30}px)"
                >
                    <span>Initiate Communion</span>
                    <div
                        class="light-sweep"
                        style="left: {((time * 80) % 250) - 50}%"
                    ></div>
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    /* THE VOID */
    .void-space {
        position: relative;
        width: 100%;
        min-height: 100vh;
        background: radial-gradient(circle at center, #0b0e17 0%, #030407 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        font-family: "Inter", system-ui, sans-serif;
        color: #fff;
    }

    /* SFUMATO & CHIAROSCURO LIGHTING */
    .generative-nebula {
        position: absolute;
        top: -50%;
        left: -50%;
        right: -50%;
        bottom: -50%;
        background: radial-gradient(
                circle at 50% 30%,
                rgba(34, 211, 238, 0.08) 0%,
                transparent 60%
            ),
            radial-gradient(
                circle at 70% 70%,
                rgba(139, 92, 246, 0.05) 0%,
                transparent 50%
            );
        pointer-events: none;
        z-index: 1;
        transition: opacity 0.5s ease-out;
    }

    .chiaroscuro-light {
        position: absolute;
        width: 600px;
        height: 600px;
        background: radial-gradient(
            circle,
            rgba(255, 255, 255, 0.03) 0%,
            transparent 70%
        );
        filter: blur(40px);
        pointer-events: none;
        z-index: 2;
        transition: transform 0.1s;
    }

    .sanctum {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3rem;
    }

    header {
        text-align: center;
        z-index: 20;
    }

    .sfumato-text {
        font-size: 3rem;
        font-weight: 200;
        letter-spacing: 0.1em;
        background: linear-gradient(
            180deg,
            #ffffff 0%,
            rgba(255, 255, 255, 0.4) 100%
        );
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 4px 30px rgba(34, 211, 238, 0.3);
        margin: 0 0 0.5rem 0;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 1rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    /* SPATIAL PORTAL - The Cathedral Window */
    .spatial-portal {
        position: relative;
        width: 380px;
        height: 520px;
        border-radius: 24px;
        transform-style: preserve-3d;
        cursor: crosshair;
        /* Chiaroscuro borders mimicking ancient stone/glass bindings */
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(10, 15, 25, 0.3);
        backdrop-filter: blur(20px);
        transition:
            transform 0.1s cubic-bezier(0.2, 0.8, 0.2, 1),
            box-shadow 0.3s ease;
    }

    .spatial-portal::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 24px;
        padding: 1px;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.15) 0%,
            transparent 100%
        );
        -webkit-mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    /* STRATA - Deep temporal and spatial layering */
    .strata {
        position: absolute;
        inset: 0;
        border-radius: 24px;
        transform-style: preserve-3d;
    }

    .back-layer {
        background: linear-gradient(
            to bottom right,
            rgba(16, 24, 39, 0.8),
            rgba(0, 0, 0, 0.9)
        );
        transform: translateZ(-20px);
    }

    .glass-layer {
        transform: translateZ(20px);
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .breathing-lattice {
        width: 100%;
        height: 100%;
        background-image: linear-gradient(
                rgba(34, 211, 238, 0.03) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(34, 211, 238, 0.03) 1px,
                transparent 1px
            );
        background-size: 20px 20px;
        border-radius: 24px;
        transition:
            opacity 1s,
            transform 2s;
    }

    /* INTERACTION & TACTILE DIGITIALITY */
    .interaction-layer {
        transform: translateZ(50px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 2.5rem 2rem;
        pointer-events: none; /* Let parent catch events */
    }

    .sacred-geometry {
        position: relative;
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
        transform: translateZ(30px);
    }

    .ring {
        position: absolute;
        border-radius: 50%;
        border: 1px solid rgba(34, 211, 238, 0.2);
    }
    .outer-ring {
        width: 100px;
        height: 100px;
        border-top-color: rgba(34, 211, 238, 0.8);
        border-left-color: rgba(139, 92, 246, 0.5);
    }
    .inner-ring {
        width: 60px;
        height: 60px;
        border-bottom-color: rgba(245, 158, 11, 0.8);
        border-right-color: rgba(34, 211, 238, 0.5);
    }

    .crystal-core {
        width: 12px;
        height: 12px;
        background: #fff;
        border-radius: 50%;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.8);
    }

    .metrics {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    .vital-sign {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .label {
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
    }

    .bar-track {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.1s linear;
    }
    .bar-fill.cyan {
        background: linear-gradient(90deg, #0ea5e9, #22d3ee);
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
    }
    .bar-fill.amber {
        background: linear-gradient(90deg, #d97706, #fbbf24);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }

    .cast-stone-btn {
        pointer-events: auto; /* Enable clicks */
        position: relative;
        width: 100%;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-family: "Inter", system-ui, sans-serif;
        font-weight: 500;
        letter-spacing: 0.05em;
        cursor: pointer;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .cast-stone-btn:hover {
        background: rgba(34, 211, 238, 0.1);
        border-color: rgba(34, 211, 238, 0.3);
        box-shadow:
            0 0 20px rgba(34, 211, 238, 0.2),
            inset 0 0 10px rgba(34, 211, 238, 0.1);
        color: #fff;
    }

    .cast-stone-btn:active {
        transform: translateZ(10px) scale(0.98) !important;
        background: rgba(34, 211, 238, 0.2);
    }

    .light-sweep {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 30%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transform: skewX(-20deg);
        pointer-events: none;
    }
</style>
