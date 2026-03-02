<script lang="ts">
    import { fade, scale } from "svelte/transition";
    import { elasticOut } from "svelte/easing";
    import { LockKeyhole } from "lucide-svelte";
    import { zkAttesterEngine } from "$lib/services/zk-attester-engine.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { goto } from "$app/navigation";

    let { onsuccess } = $props<{ onsuccess: () => void }>();

    let containerRef = $state<HTMLDivElement | null>(null);

    // State
    let isDragging = $state(false);
    let isBurning = $state(false);
    let isComplete = $state(false);
    let showWhiteout = $state(false);

    let orbX = $state(0);
    let orbY = $state(0);
    let burnProgress = $state(0); // 0 to 1

    let cx = $state(0);
    let cy = $state(0);
    let maxDist = $state(0);

    function initOrb() {
        if (!containerRef) return;
        const rect = containerRef.getBoundingClientRect();
        cx = rect.width / 2;
        cy = rect.height / 2;
        maxDist = Math.min(cx, cy) - 40; // 40 is orb radius roughly

        if (!isDragging && burnProgress === 0) {
            orbX = cx;
            orbY = cy - maxDist; // Top of the circle
        }
    }

    // Call initOrb when mounted or window resizes
    $effect(() => {
        initOrb();
        const handleResize = () => initOrb();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    });

    function startDrag(e: MouseEvent | TouchEvent) {
        if (isBurning || isComplete) return;
        isDragging = true;
        updatePosition(e);
    }

    function doDrag(e: MouseEvent | TouchEvent) {
        if (!isDragging || isBurning || isComplete) return;
        updatePosition(e);
    }

    function stopDrag() {
        if (!isDragging || isBurning || isComplete) return;
        isDragging = false;

        // If not enough pressure, snap back
        if (burnProgress < 0.99) {
            burnProgress = 0;
            orbX = cx;
            orbY = cy - maxDist;
        }
    }

    function updatePosition(e: MouseEvent | TouchEvent) {
        if (!containerRef) return;
        const rect = containerRef.getBoundingClientRect();

        let clientX, clientY;
        if ("touches" in e) {
            // Provide explicit type assertion or checking if 'touches' exists.
            const touchEvent = e as TouchEvent;
            clientX = touchEvent.touches[0].clientX;
            clientY = touchEvent.touches[0].clientY;
        } else {
            const mouseEvent = e as MouseEvent;
            clientX = mouseEvent.clientX;
            clientY = mouseEvent.clientY;
        }

        // Local coordinates
        let lx = clientX - rect.left;
        let ly = clientY - rect.top;

        let dx = lx - cx;
        let dy = ly - cy;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > maxDist) {
            // Constrain to circle
            lx = cx + (dx / dist) * maxDist;
            ly = cy + (dy / dist) * maxDist;
            dist = maxDist;
        }

        orbX = lx;
        orbY = ly;

        // Progress goes from 0 (at maxDist) to 1 (at center)
        let newProgress = 1 - dist / maxDist;
        newProgress = Math.max(0, Math.min(1, newProgress));

        burnProgress = newProgress;

        // Haptic feedback
        if (typeof navigator !== "undefined" && navigator.vibrate) {
            // Vibrate based on progress
            if (newProgress > 0.5 && Math.random() > 0.5) {
                navigator.vibrate([Math.floor(newProgress * 10)]);
            }
        }

        if (burnProgress >= 0.99) {
            triggerBurn();
        }
    }

    async function triggerBurn() {
        isDragging = false;
        isBurning = true;

        // The "Quiet before the Storm"
        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate(0); // Silence the haptics
            setTimeout(() => navigator.vibrate([200, 100, 500]), 200);
        }

        manifold.recordEvent(
            "BURN_INITIATED",
            "Gate of Sacrifice sequence engaged. 0x00 Irrevocable Burn executing.",
        );

        await new Promise((r) => setTimeout(r, 1500));

        // Prepare the Zero-Copy buffer for the 0x00 Burn
        const burnManifestBuffer = new ArrayBuffer(64);
        const success = zkAttesterEngine.verifyZeroCopyBuffer(
            burnManifestBuffer,
            "client_side_wasm",
        );

        if (success) {
            isBurning = false;

            // The Visual Whiteout
            showWhiteout = true;

            manifold.recordEvent(
                "PASSPORT_MINTED",
                "ZK-Passport v21.2 Minted. Sovereign Sentinel Dashboard unlocked.",
            );

            setTimeout(() => {
                isComplete = true;
                showWhiteout = false;
                onsuccess();
                setTimeout(() => {
                    goto("/dashboard/sovereign");
                }, 1500);
            }, 1000);
        }
    }
</script>

<div class="altar-container" in:fade>
    {#if showWhiteout}
        <div class="whiteout-screen" transition:fade={{ duration: 500 }}></div>
    {/if}

    {#if !isComplete}
        <h3
            class="mb-4 text-center font-black tracking-widest text-[#22d3ee] uppercase z-10 opacity-70"
        >
            The Gravity Well
        </h3>

        <!-- The interaction area -->
        <div
            class="gravity-well-container"
            bind:this={containerRef}
            onmousemove={doDrag}
            onmouseup={stopDrag}
            onmouseleave={stopDrag}
            ontouchmove={(e) => {
                e.preventDefault();
                doDrag(e);
            }}
            ontouchend={stopDrag}
            ontouchcancel={stopDrag}
            role="presentation"
        >
            <!-- Center Void -->
            <div
                class="void-core"
                style="transform: translate(-50%, -50%) scale({1 +
                    burnProgress * 0.5}); box-shadow: 0 0 {burnProgress *
                    100}px {burnProgress *
                    20}px rgba(34, 211, 238, {burnProgress * 0.5})"
            >
                <div class="void-abyss"></div>
                <div
                    class="void-ring"
                    style="opacity: {0.3 + burnProgress * 0.7}"
                ></div>
            </div>

            <div
                class="void-overlay-text"
                style="opacity: {burnProgress > 0.8 ? 1 : 0.2}"
            >
                {burnProgress >= 0.99
                    ? "INITIALIZING SHARD BIRTH..."
                    : "DRAG TO THE VOID"}
            </div>

            <!-- The Dying Star ($AGE) -->
            {#if !isBurning}
                <div
                    class="dying-star"
                    role="slider"
                    aria-valuenow={burnProgress * 100}
                    tabindex="0"
                    aria-label="Drag 10,000 AGE to the center well"
                    style="left: {orbX}px; top: {orbY}px; opacity: {1 -
                        burnProgress * 0.5}; box-shadow: 0 0 {30 -
                        burnProgress * 20}px rgba(245,158,11,1);"
                    onmousedown={startDrag}
                    ontouchstart={(e) => {
                        e.preventDefault();
                        startDrag(e);
                    }}
                >
                    <div class="amount-text">10,000 AGE</div>
                </div>
            {/if}

            {#if isBurning}
                <div
                    class="absolute inset-0 flex flex-col items-center justify-center z-50"
                >
                    <div class="loader"></div>
                    <div
                        class="text-[#22d3ee] font-mono text-xs tracking-widest animate-pulse mt-6 text-center shadow-black drop-shadow-lg p-2 rounded bg-black/50 backdrop-blur"
                    >
                        EXECUTING 0x00 BURN...<br />
                        MINTING ZK-PASSPORT...
                    </div>
                </div>
            {/if}
        </div>
    {:else}
        <div
            class="success-state"
            in:scale={{ duration: 1000, easing: elasticOut }}
        >
            <LockKeyhole
                size={64}
                class="mx-auto text-[#22d3ee] mb-6 drop-shadow-[0_0_30px_rgba(34,211,238,0.8)]"
            />
            <h3
                class="text-3xl font-black tracking-[0.2em] mb-2 uppercase text-white"
            >
                Welcome Home
            </h3>
            <p class="text-white/50 text-sm mb-6">
                Your Sentinel is now active.
            </p>
            <div
                class="text-xs font-mono text-[#22d3ee] bg-black/60 p-4 rounded-xl border border-[#22d3ee]/30"
            >
                ZK-PASSPORT v21.2 VERIFIED
            </div>
        </div>
    {/if}
</div>

<style>
    .altar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0;
        background: radial-gradient(circle at center, #0a0a0c, #000);
        border-radius: 40px;
        min-height: 500px;
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
        position: relative;
        overflow: hidden;
    }

    .whiteout-screen {
        position: fixed;
        inset: 0;
        background: #e0ffff;
        z-index: 9999;
        mix-blend-mode: screen;
        pointer-events: none;
    }

    .gravity-well-container {
        position: relative;
        width: 100%;
        height: 400px;
        background: radial-gradient(
            circle at center,
            rgba(34, 211, 238, 0.05) 0%,
            transparent 70%
        );
        border-radius: 50%;
        touch-action: none;
        user-select: none;
        overflow: hidden;
    }

    .void-core {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
        transition: transform 0.1s;
        background: black;
    }

    .void-abyss {
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at center,
            #000 40%,
            rgba(34, 211, 238, 0.2) 100%
        );
        border-radius: 50%;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 1);
    }

    .void-ring {
        position: absolute;
        inset: -10px;
        border: 2px dashed rgba(34, 211, 238, 0.4);
        border-radius: 50%;
        animation: spinReverse 15s linear infinite;
        pointer-events: none;
    }

    .void-overlay-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: monospace;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-align: center;
        color: #22d3ee;
        pointer-events: none;
        z-index: 5;
        width: 150px;
    }

    .dying-star {
        position: absolute;
        width: 64px;
        height: 64px;
        background: radial-gradient(circle at center, #fff, #fbbf24);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        cursor: grab;
        z-index: 20;
        display: flex;
        align-items: center;
        justify-content: center;
        transition:
            opacity 0.1s,
            box-shadow 0.1s;
    }

    .dying-star:active {
        cursor: grabbing;
    }

    .amount-text {
        font-family: sans-serif;
        font-size: 0.55rem;
        font-weight: 900;
        color: black;
        text-align: center;
        line-height: 1.1;
        pointer-events: none;
    }

    .loader {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(34, 211, 238, 0.2);
        border-top-color: #22d3ee;
        border-radius: 50%;
        animation: spin-loader 1s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }

    @keyframes spinReverse {
        0% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(0deg);
        }
    }

    @keyframes spin-loader {
        100% {
            transform: rotate(360deg);
        }
    }

    .success-state {
        text-align: center;
        z-index: 20;
    }
</style>
