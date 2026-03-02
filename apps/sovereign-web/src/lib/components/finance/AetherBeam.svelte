<script lang="ts">
    // @ts-nocheck
    import { fade, fly, scale } from "svelte/transition";
    import { elasticOut } from "svelte/easing";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { zkAttesterEngine } from "$lib/services/zk-attester-engine.svelte";
    import {
        Search,
        Fingerprint,
        Zap,
        CheckCircle2,
        ChevronUp,
    } from "lucide-svelte";

    // 🌬️ AETHER BEAM: Sovereign Venmo (v26.2)
    // Frictionless P2P value transfer masked by Halo2 Nullifiers.
    // Uses Swipe-to-Beam haptic physics to create an emotional connection to value transfer.

    let recipient = $state("");
    let amountStr = $state("");
    let amount = $derived(parseFloat(amountStr) || 0);

    let searchActive = $state(false);
    let selectedPeer = $state<any>(null);

    // Mock peers in the local shard
    const peers = [
        {
            handle: "@atlas.pagn",
            name: "Atlas Protocol",
            avatar: "A",
            merit: 0.95,
        },
        { handle: "@cipher.punk", name: "Cipher", avatar: "C", merit: 0.88 },
        {
            handle: "@dabba.hub",
            name: "Dabba Logistics Core",
            avatar: "D",
            merit: 0.99,
        },
    ];

    let filteredPeers = $derived(
        recipient.length > 0
            ? peers.filter((p) =>
                  p.handle.toLowerCase().includes(recipient.toLowerCase()),
              )
            : peers,
    );

    // Beam Physics State
    let dragY = $state.raw(0);
    let startY = $state.raw(0);
    let isDragging = $state.raw(false);
    let beamStatus = $state("IDLE"); // IDLE, CHARGING, BEAMING, SUCCESS

    function selectPeer(peer: any) {
        selectedPeer = peer;
        recipient = peer.handle;
        searchActive = false;
    }

    function handleTouchStart(e: TouchEvent | MouseEvent) {
        if (
            !selectedPeer ||
            amount <= 0 ||
            amount > manifold.walletState.resBalance
        )
            return;
        isDragging = true;
        startY = "touches" in e ? e.touches[0].clientY : e.clientY;
    }

    function handleTouchMove(e: TouchEvent | MouseEvent) {
        if (!isDragging) return;
        const currentY = "touches" in e ? e.touches[0].clientY : e.clientY;
        const delta = startY - currentY;

        if (delta > 0) {
            dragY = Math.min(delta, 250); // Max drag resistance
            if (dragY > 120) beamStatus = "CHARGING";
            else beamStatus = "IDLE";
        }
    }

    async function handleTouchEnd() {
        if (!isDragging) return;
        isDragging = false;

        if (dragY >= 150) {
            // Trigger Beam
            beamStatus = "BEAMING";
            dragY = 600; // Shoot out of screen (The Beam)

            // Vibrate if mobile (Simulating Deep Haptics)
            if (typeof navigator !== "undefined" && navigator.vibrate) {
                navigator.vibrate([100, 50, 100]);
            }

            // Simulate ZK-Nullifier generation (The invisible guardian)
            await new Promise((r) => setTimeout(r, 600));

            const success = zkAttesterEngine.verifyStateTransition(
                "0xNULLIFIER-" + Math.random().toString(16).slice(2),
                "client_side_wasm",
            );

            if (success) {
                // Settle transaction locally instantly (<500ms)
                manifold.walletState.resBalance -= amount;
                manifold.recordEvent(
                    "AETHER_BEAM",
                    `Privately beamed ${amount} SLC to ${selectedPeer.handle}`,
                );
                beamStatus = "SUCCESS";

                if (typeof navigator !== "undefined" && navigator.vibrate) {
                    navigator.vibrate([200]); // Final success thud
                }

                setTimeout(() => {
                    resetBeam();
                }, 3000);
            }
        } else {
            // Snap back
            dragY = 0;
            beamStatus = "IDLE";
        }
    }

    function resetBeam() {
        beamStatus = "IDLE";
        dragY = 0;
        amountStr = "";
        selectedPeer = null;
        recipient = "";
        searchActive = false;
    }
</script>

<div class="aether-beam-container">
    <div
        class="beam-viewport glass-panel"
        role="presentation"
        onmouseup={handleTouchEnd}
        onmouseleave={handleTouchEnd}
        ontouchend={handleTouchEnd}
        ontouchcancel={handleTouchEnd}
    >
        <!-- HEADER -->
        <div class="header">
            <h2 class="title">Aether Beam</h2>
            <div class="balance-pill">
                <span class="label">Local Balance</span>
                <span class="value"
                    >{manifold.walletState.resBalance.toFixed(2)} SLC</span
                >
            </div>
        </div>

        {#if beamStatus === "SUCCESS"}
            <!-- SUCCESS STATE -->
            <div
                class="success-state"
                in:scale={{ duration: 500, easing: elasticOut }}
            >
                <div class="check-circle">
                    <CheckCircle2 size={64} color="#00e5ff" />
                </div>
                <h3>Beam Inhaled</h3>
                <p>
                    Transfer to {selectedPeer?.handle} settled instantly via ZK-Nullifier.
                </p>

                <div class="receipt-box">
                    <div class="r-row">
                        <span>Amount</span> <span>{amount} SLC</span>
                    </div>
                    <div class="r-row">
                        <span>Fee (Merit Rebate)</span> <span>0.00 SLC</span>
                    </div>
                    <div class="r-row">
                        <span>Privacy</span>
                        <span class="text-emerald-400 font-mono"
                            >HALO2 MASKED</span
                        >
                    </div>
                </div>

                <button class="reset-btn" onclick={resetBeam}>Beam Again</button
                >
            </div>
        {:else}
            <!-- INPUT STATE -->
            <div
                class="input-section"
                style="transform: translateY(-{dragY * 0.2}px); opacity: {1 -
                    dragY / 300};"
            >
                <!-- Recipient Search -->
                <div class="search-box" class:active={searchActive}>
                    <Search size={18} class="search-icon text-white/40" />
                    <input
                        type="text"
                        placeholder="Search peers by handle (@)"
                        bind:value={recipient}
                        onfocus={() => (searchActive = true)}
                        onblur={() =>
                            setTimeout(() => (searchActive = false), 200)}
                    />
                    {#if selectedPeer}
                        <div class="selected-badge" in:scale>
                            {selectedPeer.avatar}
                        </div>
                    {/if}
                </div>

                {#if searchActive && !selectedPeer}
                    <div class="peer-dropdown">
                        {#each filteredPeers as peer}
                            <button
                                class="peer-row"
                                onclick={() => selectPeer(peer)}
                            >
                                <div class="avatar">{peer.avatar}</div>
                                <div class="peer-info">
                                    <div class="handle">{peer.handle}</div>
                                    <div class="name">{peer.name}</div>
                                </div>
                                <div class="merit-badge">
                                    M {peer.merit.toFixed(2)}
                                </div>
                            </button>
                        {/each}
                    </div>
                {/if}

                <!-- Amount Input -->
                <div class="amount-entry">
                    <span class="currency">SLC</span>
                    <input
                        type="number"
                        placeholder="0.00"
                        bind:value={amountStr}
                    />
                </div>
            </div>

            <!-- THE SWIPE INTERFACE -->
            <div class="swipe-area">
                {#if dragY > 0 && beamStatus !== "BEAMING"}
                    <div class="charging-text" in:fade>
                        {dragY > 150 ? "RELEASE TO BEAM" : "PULL TO CHARGE"}
                    </div>
                {/if}

                <!-- The Draggable Currency Orb -->
                <div
                    class="dragger"
                    role="slider"
                    aria-valuenow={dragY}
                    tabindex="0"
                    aria-label="Drag to Beam"
                    class:charging={beamStatus === "CHARGING"}
                    class:beaming={beamStatus === "BEAMING"}
                    class:disabled={!selectedPeer ||
                        amount <= 0 ||
                        amount > manifold.walletState.resBalance}
                    style="transform: translateY(-{dragY}px)"
                    onmousedown={handleTouchStart}
                    onmousemove={handleTouchMove}
                    ontouchstart={handleTouchStart}
                    ontouchmove={handleTouchMove}
                >
                    <div class="dragger-visual">
                        <Zap size={24} />
                    </div>
                </div>

                <div class="swipe-track">
                    <ChevronUp size={24} class="track-icon t1" />
                    <ChevronUp size={24} class="track-icon t2" />
                    <ChevronUp size={24} class="track-icon t3" />
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .aether-beam-container {
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        font-family: inherit;
        color: white;
    }

    .glass-panel {
        background: rgba(15, 15, 20, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        min-height: 600px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2.5rem;
    }

    .title {
        font-size: 1.25rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #fff, #00e5ff);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .balance-pill {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .balance-pill .label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.4);
    }

    .balance-pill .value {
        font-size: 1rem;
        font-weight: 800;
        font-variant-numeric: tabular-nums;
    }

    /* Input Section */
    .input-section {
        flex: 1;
        position: relative;
        transition: opacity 0.1s;
    }

    .search-box {
        position: relative;
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1rem 1.25rem;
        transition: all 0.3s;
        z-index: 10;
    }

    .search-box.active {
        background: rgba(0, 229, 255, 0.05);
        border-color: rgba(0, 229, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);
    }

    :global(.search-icon) {
        margin-right: 0.75rem;
    }

    .search-box input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: white;
        font-size: 1rem;
        font-weight: 600;
    }

    .search-box input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }

    .selected-badge {
        width: 24px;
        height: 24px;
        background: #00e5ff;
        color: black;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 900;
    }

    .peer-dropdown {
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        right: 0;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 0.5rem;
        z-index: 20;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .peer-row {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: transparent;
        border: none;
        border-radius: 14px;
        cursor: pointer;
        color: white;
        text-align: left;
        transition: all 0.2s;
    }

    .peer-row:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .avatar {
        width: 40px;
        height: 40px;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        color: #00e5ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
    }

    .peer-info {
        flex: 1;
    }

    .handle {
        font-weight: 800;
        font-size: 0.9rem;
    }

    .name {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 0.2rem;
    }

    .merit-badge {
        font-size: 0.65rem;
        font-weight: 900;
        color: #fbbf24;
        background: rgba(251, 191, 36, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 8px;
    }

    .amount-entry {
        margin-top: 4rem;
        text-align: center;
        position: relative;
    }

    .amount-entry input {
        background: transparent;
        border: none;
        outline: none;
        font-size: 4.5rem;
        font-weight: 900;
        color: white;
        text-align: center;
        width: 100%;
        letter-spacing: -0.05em;
    }

    .amount-entry input::placeholder {
        color: rgba(255, 255, 255, 0.1);
    }

    .currency {
        position: absolute;
        top: -1.5rem;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.8rem;
        font-weight: 800;
        color: #00e5ff;
        letter-spacing: 0.2em;
    }

    /* Swipe Interface */
    .swipe-area {
        position: absolute;
        bottom: 3rem;
        left: 0;
        right: 0;
        height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
    }

    .charging-text {
        position: absolute;
        top: -2rem;
        font-size: 0.7rem;
        font-weight: 900;
        letter-spacing: 0.2em;
        color: #00e5ff;
        animation: pulse 1s infinite alternate;
    }

    @keyframes pulse {
        from {
            opacity: 0.5;
        }
        to {
            opacity: 1;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
        }
    }

    .dragger {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: rgba(0, 229, 255, 0.1);
        border: 2px solid rgba(0, 229, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00e5ff;
        cursor: grab;
        z-index: 10;
        position: relative;
        transition:
            border-color 0.2s,
            box-shadow 0.2s;
    }

    .dragger:active {
        cursor: grabbing;
    }

    .dragger.disabled {
        border-color: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.2);
        background: transparent;
        pointer-events: none;
    }

    .dragger.charging {
        background: rgba(0, 229, 255, 0.2);
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.4);
        border-color: #00e5ff;
        transform: scale(1.1);
    }

    .dragger.beaming {
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
    }

    .dragger-visual {
        pointer-events: none;
    }

    .swipe-track {
        position: absolute;
        bottom: 100px;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        opacity: 0.3;
        z-index: 0;
    }

    :global(.track-icon) {
        color: rgba(255, 255, 255, 0.4);
        animation: floatUp 2s infinite linear;
    }

    :global(.track-icon.t1) {
        animation-delay: 0s;
    }
    :global(.track-icon.t2) {
        animation-delay: 0.3s;
    }
    :global(.track-icon.t3) {
        animation-delay: 0.6s;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(10px);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-20px);
            opacity: 0;
        }
    }

    /* Success State */
    .success-state {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        flex: 1;
    }

    .check-circle {
        margin-bottom: 2rem;
        filter: drop-shadow(0 0 20px rgba(0, 229, 255, 0.4));
    }

    .success-state h3 {
        font-size: 1.5rem;
        font-weight: 900;
        margin: 0 0 0.5rem 0;
        color: white;
    }

    .success-state p {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        margin: 0 0 3rem 0;
        max-width: 250px;
        line-height: 1.5;
    }

    .receipt-box {
        width: 100%;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 3rem;
    }

    .r-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
    }

    .r-row span:first-child {
        color: rgba(255, 255, 255, 0.4);
        font-weight: 600;
    }

    .r-row span:last-child {
        font-weight: 800;
        color: white;
    }

    .reset-btn {
        padding: 1rem 3rem;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        color: #00e5ff;
        border-radius: 100px;
        font-weight: 900;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.2s;
    }

    .reset-btn:hover {
        background: rgba(0, 229, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
    }
</style>
