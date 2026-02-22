<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    // Mock vault store to prevent import errors if it doesn't exist
    // Replace with actual import if it exists properly
    import { writable } from "svelte/store";
    const vaultStore = writable({ balance: "124900.00" });
    (vaultStore as any).loadVaultData = async () => {
        return new Promise((resolve) => setTimeout(resolve, 1000));
    };

    import { fly, fade } from "svelte/transition";
    import { quintOut, cubicInOut } from "svelte/easing";

    // Chain configuration
    const chains = {
        base: {
            name: "Base",
            color: "#0052FF",
            icon: "🔵",
            rpc: "base.mainnet",
            tps: 124,
        },
        optimism: {
            name: "Optimism",
            color: "#FF0420",
            icon: "🔴",
            rpc: "optimism.mainnet",
            tps: 89,
        },
        arbitrum: {
            name: "Arbitrum",
            color: "#28A0F0",
            icon: "🔷",
            rpc: "arbitrum.mainnet",
            tps: 156,
        },
        polygon: {
            name: "Polygon",
            color: "#8247E5",
            icon: "🟣",
            rpc: "polygon.mainnet",
            tps: 212,
        },
    };

    let fromChain = "base";
    let toChain = "optimism";
    let amount = "";
    let asset = "USDC";
    let isProcessing = false;
    let showConfirmation = false;
    let transferId = "";
    let transferProgress = 0;
    let hoveredChain = null;

    // For the living topology visualization
    let canvasCtx;
    let particles = [];
    let animationFrame;

    onMount(() => {
        initParticleNetwork();
        initCanvas();
        return () => cancelAnimationFrame(animationFrame);
    });

    function initParticleNetwork() {
        // Create particle system representing network activity
        for (let i = 0; i < 100; i++) {
            particles.push({
                x: Math.random(),
                y: Math.random(),
                vx: (Math.random() - 0.5) * 0.002,
                vy: (Math.random() - 0.5) * 0.002,
                targetChain: Math.random() > 0.5 ? "base" : "optimism",
            });
        }
    }

    function initCanvas() {
        const canvas = document.getElementById("chain-topology");
        if (!canvas) return;

        canvasCtx = canvas.getContext("2d");
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        function animate() {
            if (!canvasCtx) return;

            canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw connections between chains
            canvasCtx.strokeStyle = "rgba(255, 255, 255, 0.1)";
            canvasCtx.lineWidth = 1;

            // Draw chain nodes
            const chainPositions = {
                base: { x: canvas.width * 0.2, y: canvas.height * 0.5 },
                optimism: { x: canvas.width * 0.4, y: canvas.height * 0.3 },
                arbitrum: { x: canvas.width * 0.6, y: canvas.height * 0.7 },
                polygon: { x: canvas.width * 0.8, y: canvas.height * 0.4 },
            };

            // Draw all connections
            Object.keys(chainPositions).forEach((from) => {
                Object.keys(chainPositions).forEach((to) => {
                    if (from !== to) {
                        canvasCtx.beginPath();
                        canvasCtx.moveTo(
                            chainPositions[from].x,
                            chainPositions[from].y,
                        );
                        canvasCtx.lineTo(
                            chainPositions[to].x,
                            chainPositions[to].y,
                        );
                        canvasCtx.strokeStyle = "rgba(255, 255, 255, 0.05)";
                        canvasCtx.stroke();
                    }
                });
            });

            // Draw active transfer if processing
            if (isProcessing && fromChain && toChain) {
                const start = chainPositions[fromChain];
                const end = chainPositions[toChain];

                // Animated orb traveling along path
                const t = (Date.now() % 3000) / 3000; // 3 second journey

                canvasCtx.beginPath();
                canvasCtx.moveTo(start.x, start.y);
                canvasCtx.lineTo(end.x, end.y);
                canvasCtx.strokeStyle = chains[fromChain].color;
                canvasCtx.lineWidth = 2;
                canvasCtx.stroke();

                // Orb
                const orbX = start.x + (end.x - start.x) * t;
                const orbY = start.y + (end.y - start.y) * t;

                canvasCtx.beginPath();
                canvasCtx.arc(orbX, orbY, 8, 0, Math.PI * 2);
                canvasCtx.fillStyle = chains[toChain].color;
                canvasCtx.shadowColor = chains[toChain].color;
                canvasCtx.shadowBlur = 20;
                canvasCtx.fill();
                canvasCtx.shadowBlur = 0;
            }

            // Draw chain nodes
            Object.entries(chainPositions).forEach(([chain, pos]) => {
                const isSelected = chain === fromChain || chain === toChain;
                const isHovered = chain === hoveredChain;

                canvasCtx.beginPath();
                canvasCtx.arc(
                    pos.x,
                    pos.y,
                    isSelected ? 20 : 15,
                    0,
                    Math.PI * 2,
                );

                // Gradient fill
                const gradient = canvasCtx.createRadialGradient(
                    pos.x - 5,
                    pos.y - 5,
                    5,
                    pos.x,
                    pos.y,
                    30,
                );
                gradient.addColorStop(0, chains[chain].color);
                gradient.addColorStop(1, "rgba(0,0,0,0.5)");

                canvasCtx.fillStyle = gradient;
                canvasCtx.shadowColor = chains[chain].color;
                canvasCtx.shadowBlur = isSelected ? 30 : 15;
                canvasCtx.fill();

                // Label
                canvasCtx.shadowBlur = 0;
                canvasCtx.fillStyle = "white";
                canvasCtx.font = isSelected ? "bold 14px Inter" : "12px Inter";
                canvasCtx.textAlign = "center";
                canvasCtx.fillText(chains[chain].name, pos.x, pos.y - 30);

                // TPS indicator
                canvasCtx.font = "10px Inter";
                canvasCtx.fillStyle = "rgba(255,255,255,0.5)";
                canvasCtx.fillText(
                    `${chains[chain].tps} TPS`,
                    pos.x,
                    pos.y + 35,
                );
            });

            animationFrame = requestAnimationFrame(animate);
        }

        animate();
    }

    // Somatic weight - press and hold for execution
    let holdProgress = 0;
    let holdInterval;

    function startHold() {
        if (!amount || !fromChain || !toChain) return;

        holdProgress = 0;
        holdInterval = setInterval(() => {
            holdProgress += 2;
            if (holdProgress >= 100) {
                clearInterval(holdInterval);
                executeBridge();
            }
        }, 30); // 1.5 seconds to full hold
    }

    function cancelHold() {
        clearInterval(holdInterval);
        holdProgress = 0;
    }

    async function executeBridge() {
        isProcessing = true;

        try {
            // Simulate cross-chain transfer
            transferId = `0x${Math.random().toString(16).substring(2)}`;

            // Progress simulation
            for (let i = 0; i <= 100; i += 5) {
                transferProgress = i;
                await new Promise((r) => setTimeout(r, 150));
            }

            showConfirmation = true;

            // Update vault after bridge
            await (vaultStore as any).loadVaultData();
        } catch (error) {
            console.error("Bridge failed:", error);
        } finally {
            isProcessing = false;
        }
    }
</script>

<div class="bridge-cathedral">
    <!-- Background Living Topology -->
    <canvas id="chain-topology" class="topology-canvas"></canvas>

    <!-- Main Bridge Interface -->
    <div
        class="bridge-interface glass-panel"
        in:fly={{ y: 20, duration: 600, easing: quintOut }}
    >
        <h1 class="chapter-title">
            <span class="title-glow">⚡</span>
            Cross-Chain Logistics
        </h1>
        <p class="chapter-subtitle">Move assets across the sovereign mesh</p>

        <!-- Chain Selectors - 3D style -->
        <div class="chain-selectors">
            <div
                class="chain-panel from"
                on:mouseenter={() => (hoveredChain = fromChain)}
                on:mouseleave={() => (hoveredChain = null)}
            >
                <label>From</label>
                <div
                    class="chain-display"
                    style="border-color: {chains[fromChain].color}"
                >
                    <span class="chain-icon">{chains[fromChain].icon}</span>
                    <select bind:value={fromChain} class="chain-select">
                        {#each Object.entries(chains) as [key, chain]}
                            <option value={key}>{chain.name}</option>
                        {/each}
                    </select>
                </div>
                <div class="chain-metrics">
                    <span>TPS: {chains[fromChain].tps}</span>
                    <span>Gas: 0.47 Gwei</span>
                </div>
            </div>

            <div class="bridge-arrow">
                <span class="arrow-icon">→</span>
                <span class="arrow-glow"></span>
            </div>

            <div
                class="chain-panel to"
                on:mouseenter={() => (hoveredChain = toChain)}
                on:mouseleave={() => (hoveredChain = null)}
            >
                <label>To</label>
                <div
                    class="chain-display"
                    style="border-color: {chains[toChain].color}"
                >
                    <span class="chain-icon">{chains[toChain].icon}</span>
                    <select bind:value={toChain} class="chain-select">
                        {#each Object.entries(chains) as [key, chain]}
                            <option value={key}>{chain.name}</option>
                        {/each}
                    </select>
                </div>
                <div class="chain-metrics">
                    <span>Finality: 1.2s</span>
                    <span>Bridge Liquidity: $124.7M</span>
                </div>
            </div>
        </div>

        <!-- Asset Input with Weight -->
        <div class="asset-section">
            <div class="asset-label">
                <span>Amount</span>
                <span class="balance-hint"
                    >Available: ${$vaultStore?.balance || "0"}</span
                >
            </div>

            <div class="asset-input-group">
                <input
                    type="number"
                    bind:value={amount}
                    placeholder="0.00"
                    class="asset-input glass-input"
                    step="0.01"
                />

                <select bind:value={asset} class="asset-select glass-select">
                    <option value="USDC">USDC</option>
                    <option value="AGE">AGE</option>
                    <option value="SYND">SYND</option>
                </select>
            </div>
        </div>

        <!-- Fee Preview -->
        <div class="fee-preview">
            <div class="fee-row">
                <span>Bridge Fee</span>
                <span>0.05% ($0.47)</span>
            </div>
            <div class="fee-row">
                <span>Estimated Time</span>
                <span>~3 minutes</span>
            </div>
            <div class="fee-row total">
                <span>You'll Receive</span>
                <span
                    >${amount
                        ? (parseFloat(amount) * 0.9995).toFixed(2)
                        : "0.00"}
                    {asset}</span
                >
            </div>
        </div>

        <!-- Press and Hold Button (Somatic Weight) -->
        <div class="hold-container">
            <button
                class="hold-button"
                class:processing={isProcessing}
                on:mousedown={startHold}
                on:mouseup={cancelHold}
                on:mouseleave={cancelHold}
                disabled={!amount || isProcessing}
            >
                <span class="hold-text">
                    {isProcessing ? "Bridging..." : "Hold to Bridge"}
                </span>
                <div class="hold-progress" style="width: {holdProgress}%"></div>
            </button>
            <div class="hold-instruction">
                Press and hold for irreversible action
            </div>
        </div>

        <!-- Processing State with Resonance Breath -->
        {#if isProcessing}
            <div class="processing-state" transition:fade>
                <div class="resonance-breath"></div>
                <div class="processing-details">
                    <span class="tx-id"
                        >Transfer ID: {transferId?.slice(0, 16)}...</span
                    >
                    <div class="progress-bar">
                        <div
                            class="progress-fill"
                            style="width: {transferProgress}%"
                        ></div>
                    </div>
                    <span class="progress-text"
                        >{transferProgress}% • Confirming on {toChain}</span
                    >
                </div>
            </div>
        {/if}

        <!-- Confirmation Ceremony -->
        {#if showConfirmation}
            <div
                class="confirmation-ceremony"
                transition:fly={{ y: 20, duration: 400 }}
            >
                <div class="ceremony-glow"></div>
                <div class="ceremony-content">
                    <span class="ceremony-icon">🏛️</span>
                    <h2>Transfer Complete</h2>
                    <p>Your assets have crossed the sovereign mesh</p>
                    <div class="ceremony-stats">
                        <div class="stat">
                            <span>Amount</span>
                            <strong>{amount} {asset}</strong>
                        </div>
                        <div class="stat">
                            <span>Route</span>
                            <strong>{fromChain} → {toChain}</strong>
                        </div>
                    </div>
                    <button
                        class="ceremony-button"
                        on:click={() => goto("/vault")}
                    >
                        View in Vault
                    </button>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .bridge-cathedral {
        position: relative;
        min-height: 100vh;
        background: #0a0a0f;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }

    .topology-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }

    .bridge-interface {
        position: relative;
        z-index: 10;
        width: 100%;
        max-width: 800px;
        background: rgba(20, 20, 30, 0.8);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 48px;
        padding: 3rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
    }

    .chapter-title {
        font-size: 2.5rem;
        margin: 0 0 0.5rem;
        font-weight: 300;
        letter-spacing: -0.02em;
    }

    .title-glow {
        color: #ffd700;
        margin-right: 0.5rem;
    }

    .chapter-subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 1rem;
        margin-bottom: 3rem;
    }

    .chain-selectors {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 2rem;
        align-items: center;
        margin-bottom: 3rem;
    }

    .chain-panel label {
        display: block;
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .chain-display {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 2px solid;
        border-radius: 16px;
        transition: all 0.3s ease;
    }

    .chain-display:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }

    .chain-icon {
        font-size: 1.5rem;
    }

    .chain-select {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 1.2rem;
        font-weight: 500;
        cursor: pointer;
    }

    .chain-metrics {
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.7rem;
    }

    .bridge-arrow {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .arrow-icon {
        font-size: 2rem;
        color: #ffd700;
        z-index: 2;
    }

    .arrow-glow {
        position: absolute;
        width: 60px;
        height: 60px;
        background: radial-gradient(
            circle,
            rgba(255, 215, 0, 0.3) 0%,
            transparent 70%
        );
        animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
        0%,
        100% {
            transform: scale(1);
            opacity: 0.5;
        }
        50% {
            transform: scale(1.2);
            opacity: 0.8;
        }
    }

    .asset-section {
        margin-bottom: 2rem;
    }

    .asset-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.8);
    }

    .balance-hint {
        color: #ffd700;
    }

    .asset-input-group {
        display: flex;
        gap: 1rem;
    }

    .asset-input {
        flex: 2;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 16px;
        color: white;
        font-size: 1.2rem;
    }

    .asset-select {
        flex: 1;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 16px;
        color: white;
    }

    .fee-preview {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .fee-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        color: rgba(255, 255, 255, 0.7);
    }

    .fee-row.total {
        margin-top: 0.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 215, 0, 0.2);
        font-size: 1.2rem;
        font-weight: bold;
        color: #ffd700;
    }

    .hold-container {
        position: relative;
        margin-bottom: 2rem;
    }

    .hold-button {
        position: relative;
        width: 100%;
        padding: 1.5rem;
        background: linear-gradient(135deg, #ffd700, #ffa500);
        border: none;
        border-radius: 100px;
        color: #0a0a0f;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .hold-button:hover:not(:disabled) {
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.3);
    }

    .hold-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .hold-progress {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 4px;
        background: white;
        transition: width 0.03s linear;
    }

    .hold-instruction {
        text-align: center;
        margin-top: 0.5rem;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.8rem;
    }

    .processing-state {
        margin-top: 2rem;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 24px;
        position: relative;
        overflow: hidden;
    }

    .resonance-breath {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(
            circle at 30% 50%,
            rgba(255, 215, 0, 0.1),
            transparent 70%
        );
        animation: breath 4s ease-in-out infinite;
    }

    @keyframes breath {
        0%,
        100% {
            opacity: 0.3;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.05);
        }
    }

    .tx-id {
        position: relative;
        z-index: 2;
        color: #ffd700;
        font-family: monospace;
    }

    .progress-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #ffa500);
        transition: width 0.15s ease;
    }

    .confirmation-ceremony {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .ceremony-glow {
        position: absolute;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at center,
            rgba(255, 215, 0, 0.2),
            transparent 70%
        );
        animation: ceremonyPulse 3s infinite;
    }

    @keyframes ceremonyPulse {
        0%,
        100% {
            opacity: 0.3;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
    }

    .ceremony-content {
        position: relative;
        text-align: center;
        max-width: 400px;
        padding: 3rem;
        background: rgba(20, 20, 30, 0.9);
        border: 1px solid #ffd700;
        border-radius: 48px;
    }

    .ceremony-icon {
        font-size: 4rem;
        display: block;
        margin-bottom: 1rem;
        animation: floatIcon 3s ease-in-out infinite;
    }

    @keyframes floatIcon {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }

    .ceremony-stats {
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 16px;
    }

    .stat {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        color: rgba(255, 255, 255, 0.8);
    }

    .stat strong {
        color: #ffd700;
    }

    .ceremony-button {
        padding: 1rem 2rem;
        background: transparent;
        border: 2px solid #ffd700;
        border-radius: 100px;
        color: #ffd700;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .ceremony-button:hover {
        background: #ffd700;
        color: #0a0a0f;
    }
</style>
