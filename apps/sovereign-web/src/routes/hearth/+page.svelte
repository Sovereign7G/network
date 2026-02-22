<script lang="ts">
    import { onMount } from "svelte";
    import { fly, fade } from "svelte/transition";
    import { quintOut } from "svelte/easing";

    // Memory Data
    let memories = [
        {
            id: "m-1",
            date: "2022-03-14",
            title: "Genesis Block",
            type: "prime",
            value: "First Node Deployed",
            kintsugi: false,
        },
        {
            id: "m-2",
            date: "2023-08-21",
            title: "Great Fork",
            type: "bifurcation",
            value: "Protocol Defense",
            kintsugi: true,
            scar: "Restored from 51% Attack",
        },
        {
            id: "m-3",
            date: "2024-01-05",
            title: "Sovereign Bridge",
            type: "connection",
            value: "Cross-chain Logistics",
            kintsugi: false,
        },
        {
            id: "m-4",
            date: "2024-11-12",
            title: "Node Desync",
            type: "failure",
            value: "Downtime recovery",
            kintsugi: true,
            scar: "Rebuilt Consensus",
        },
        {
            id: "m-5",
            date: "2025-06-30",
            title: "Wealth Milestone",
            type: "milestone",
            value: "$1M TVL Surpassed",
            kintsugi: false,
        },
        {
            id: "m-6",
            date: "2026-02-18",
            title: "Cathedral Launch",
            type: "prime",
            value: "Sentient Grid Online",
            kintsugi: false,
        },
    ];

    let selectedMemory = memories[memories.length - 1];
    let hoveredMemory = null;

    // 3D Canvas
    let canvas;
    let ctx;
    let animationFrame;
    let rotationX = 0;
    let rotationY = 0;
    let targetRotationX = 0;
    let targetRotationY = 0;
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    // 3D Vertices for an Icosahedron (Crystal Shape)
    const t = (1.0 + Math.sqrt(5.0)) / 2.0;
    let vertices = [
        [-1, t, 0],
        [1, t, 0],
        [-1, -t, 0],
        [1, -t, 0],
        [0, -1, t],
        [0, 1, t],
        [0, -1, -t],
        [0, 1, -t],
        [t, 0, -1],
        [t, 0, 1],
        [-t, 0, -1],
        [-t, 0, 1],
    ];

    // Normalize vertices and scale
    const scale = 120;
    vertices = vertices.map((v) => {
        const length = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
        return [
            (v[0] / length) * scale,
            (v[1] / length) * scale,
            (v[2] / length) * scale,
        ];
    });

    const faces = [
        [0, 11, 5],
        [0, 5, 1],
        [0, 1, 7],
        [0, 7, 10],
        [0, 10, 11],
        [1, 5, 9],
        [5, 11, 4],
        [11, 10, 2],
        [10, 7, 6],
        [7, 1, 8],
        [3, 9, 4],
        [3, 4, 2],
        [3, 2, 6],
        [3, 6, 8],
        [3, 8, 9],
        [4, 9, 5],
        [2, 4, 11],
        [6, 2, 10],
        [8, 6, 7],
        [9, 8, 1],
    ];

    onMount(() => {
        initCanvas();
        return () => cancelAnimationFrame(animationFrame);
    });

    function initCanvas() {
        canvas = document.getElementById("crystal-canvas");
        if (!canvas) return;

        ctx = canvas.getContext("2d");
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        animate();
    }

    function rotate3D(x, y, z, rx, ry) {
        // Rotation around Y
        let x1 = x * Math.cos(ry) - z * Math.sin(ry);
        let z1 = z * Math.cos(ry) + x * Math.sin(ry);

        // Rotation around X
        let y2 = y * Math.cos(rx) - z1 * Math.sin(rx);
        let z2 = z1 * Math.cos(rx) + y * Math.sin(rx);

        return [x1, y2, z2];
    }

    function animate() {
        if (!ctx || !canvas) return;

        // Smooth dampening for mouse rotation
        if (!isDragging) {
            targetRotationY += 0.005; // Auto rotate
        }
        rotationX += (targetRotationX - rotationX) * 0.1;
        rotationY += (targetRotationY - rotationY) * 0.1;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2 + 20;

        // Draw Kintsugi background aura
        const auraGradient = ctx.createRadialGradient(
            centerX,
            centerY,
            0,
            centerX,
            centerY,
            200,
        );
        auraGradient.addColorStop(0, "rgba(255, 215, 0, 0.15)");
        auraGradient.addColorStop(1, "rgba(0, 0, 0, 0)");
        ctx.fillStyle = auraGradient;
        ctx.beginPath();
        ctx.arc(centerX, centerY, 200, 0, Math.PI * 2);
        ctx.fill();

        // Transform vertices
        let transformedVertices = vertices.map((v) =>
            rotate3D(v[0], v[1], v[2], rotationX, rotationY),
        );

        // Z-sort faces
        let projectedFaces = faces.map((face) => {
            let p0 = transformedVertices[face[0]];
            let p1 = transformedVertices[face[1]];
            let p2 = transformedVertices[face[2]];

            let zSum = p0[2] + p1[2] + p2[2];

            // Normal vector for lighting
            let ux = p1[0] - p0[0],
                uy = p1[1] - p0[1],
                uz = p1[2] - p0[2];
            let vx = p2[0] - p0[0],
                vy = p2[1] - p0[1],
                vz = p2[2] - p0[2];
            let nx = uy * vz - uz * vy;
            let ny = uz * vx - ux * vz;
            let nz = ux * vy - uy * vx;

            return { face, zSum, normalZ: nz, pts: [p0, p1, p2] };
        });

        projectedFaces.sort((a, b) => a.zSum - b.zSum);

        // Draw faces
        projectedFaces.forEach((f, i) => {
            // Only draw forward-facing or use transparency for glass effect
            const lightIntense = Math.max(0, f.normalZ / 10000);
            const isBackFace = f.zSum < 0;

            ctx.beginPath();
            ctx.moveTo(centerX + f.pts[0][0], centerY + f.pts[0][1]);
            ctx.lineTo(centerX + f.pts[1][0], centerY + f.pts[1][1]);
            ctx.lineTo(centerX + f.pts[2][0], centerY + f.pts[2][1]);
            ctx.closePath();

            // Base color based on Kintsugi or standard
            let baseHue = selectedMemory?.kintsugi ? 45 : 220;
            let sat = selectedMemory?.kintsugi ? "100%" : "60%";
            let light = isBackFace ? "20%" : `${30 + lightIntense * 40}%`;
            let alpha = isBackFace ? 0.3 : 0.8;

            // Face Fill
            ctx.fillStyle = `hsla(${baseHue}, ${sat}, ${light}, ${alpha})`;
            ctx.fill();

            // Stroke (Kintsugi Gold or Glass edge)
            if (selectedMemory?.kintsugi && Math.random() > 0.8) {
                ctx.strokeStyle = "#FFD700"; // Pure Gold scar
                ctx.lineWidth = 3;
                ctx.shadowColor = "#FFD700";
                ctx.shadowBlur = 10;
            } else {
                ctx.strokeStyle = `hsla(${baseHue}, ${sat}, 70%, ${isBackFace ? 0.2 : 0.8})`;
                ctx.lineWidth = 1;
                ctx.shadowBlur = 0;
            }
            ctx.stroke();
        });

        animationFrame = requestAnimationFrame(animate);
    }

    // Mouse interactions for 3D spin
    function handleMouseDown(e) {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
    }

    function handleMouseMove(e) {
        if (!isDragging) return;
        const deltaMove = {
            x: e.clientX - previousMousePosition.x,
            y: e.clientY - previousMousePosition.y,
        };

        targetRotationY += deltaMove.x * 0.01;
        targetRotationX += deltaMove.y * 0.01;

        // Clamp X rotation
        targetRotationX = Math.max(-1.5, Math.min(1.5, targetRotationX));

        previousMousePosition = { x: e.clientX, y: e.clientY };
    }

    function handleMouseUp() {
        isDragging = false;
    }
</script>

<svelte:window on:mouseup={handleMouseUp} on:mousemove={handleMouseMove} />

<div class="hearth-cathedral">
    <!-- Header -->
    <div
        class="hearth-header"
        in:fly={{ y: -20, duration: 600, easing: quintOut }}
    >
        <div class="title-area">
            <h1><span class="glow">🔥</span> Hearth</h1>
            <p>Sovereign memory crystal and Kintsugi ledger</p>
        </div>

        <div class="memory-stats">
            <div
                class="stat-badge"
                title="Total number of memories in the archive"
            >
                <span class="val">{memories.length}</span>
                <span class="lbl">Total Memories</span>
            </div>
            <div
                class="stat-badge kintsugi"
                title="Memories representing resolved crises and node recovery"
            >
                <span class="val"
                    >{memories.filter((m) => m.kintsugi).length}</span
                >
                <span class="lbl">Golden Scars</span>
            </div>
        </div>
    </div>

    <div class="content-grid">
        <!-- 3D Cathedral Crystal -->
        <div
            class="crystal-panel glass-card"
            in:fade={{ duration: 800 }}
            title="Interactable 3D representation of the sovereign memory archive"
        >
            <div class="canvas-wrapper" on:mousedown={handleMouseDown}>
                <canvas id="crystal-canvas"></canvas>
            </div>

            <div
                class="crystal-details"
                in:fly={{ y: 20, duration: 400, delay: 200 }}
            >
                {#if selectedMemory}
                    <div
                        class="selected-memory-card"
                        class:kintsugi={selectedMemory.kintsugi}
                    >
                        <div class="mem-header">
                            <span class="mem-date">{selectedMemory.date}</span>
                            <span class="mem-type">{selectedMemory.type}</span>
                        </div>
                        <h2>{selectedMemory.title}</h2>
                        <p class="mem-value">{selectedMemory.value}</p>

                        {#if selectedMemory.kintsugi}
                            <div class="kintsugi-scar">
                                <span class="icon">🔨</span>
                                <div class="scar-details">
                                    <span class="scar-lbl"
                                        >Recovered Node Memory</span
                                    >
                                    <span class="scar-txt"
                                        >{selectedMemory.scar}</span
                                    >
                                </div>
                            </div>
                        {/if}
                    </div>
                {/if}
            </div>
            <div class="drag-hint">Drag to rotate crystal</div>
        </div>

        <!-- Timeline of Memories -->
        <div
            class="timeline-panel glass-card"
            in:fly={{ x: 20, duration: 600, delay: 200 }}
            title="Chronological record of the Sovereign Network"
        >
            <h3>Chronological Strata</h3>

            <div class="timeline-container">
                <!-- Connecting line -->
                <div class="timeline-spine"></div>

                {#each [...memories].reverse() as mem, i}
                    <div
                        class="timeline-node"
                        class:selected={selectedMemory.id === mem.id}
                        class:is-kintsugi={mem.kintsugi}
                        on:click={() => (selectedMemory = mem)}
                        title={mem.kintsugi
                            ? "Recovered Sovereign Memory (Kintsugi)"
                            : "Sovereign Memory Record"}
                        in:fly={{ y: 20, duration: 300, delay: 300 + i * 100 }}
                    >
                        <!-- Timeline Dot -->
                        <div class="timeline-dot"></div>

                        <div class="node-content">
                            <div class="node-time">{mem.date}</div>
                            <div class="node-title">{mem.title}</div>
                            {#if mem.kintsugi}
                                <div class="node-gold-dust"></div>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .hearth-cathedral {
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        color: white;
    }

    .hearth-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
    }

    .title-area h1 {
        font-size: 2.5rem;
        font-weight: 300;
        margin: 0 0 0.5rem 0;
        letter-spacing: -1px;
    }
    .glow {
        color: #ff6b6b;
        text-shadow: 0 0 15px rgba(255, 107, 107, 0.5);
    }

    .title-area p {
        color: rgba(255, 255, 255, 0.5);
        margin: 0;
        font-size: 1.1rem;
    }

    .memory-stats {
        display: flex;
        gap: 1rem;
    }

    .stat-badge {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(20, 20, 30, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
    }
    .stat-badge.kintsugi {
        border-color: rgba(255, 215, 0, 0.3);
        background: rgba(255, 215, 0, 0.05);
    }

    .stat-badge .val {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .stat-badge.kintsugi .val {
        color: #ffd700;
    }
    .stat-badge .lbl {
        font-size: 0.7rem;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.5);
    }

    .content-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        min-height: 600px;
    }

    .glass-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
    }

    /* Crystal Panel */
    .crystal-panel {
        padding: 0;
        align-items: center;
        justify-content: center;
    }

    .canvas-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        cursor: grab;
    }
    .canvas-wrapper:active {
        cursor: grabbing;
    }

    #crystal-canvas {
        width: 100%;
        height: 100%;
        display: block;
    }

    .drag-hint {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.8rem;
        pointer-events: none;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .crystal-details {
        position: absolute;
        top: 2rem;
        left: 2rem;
        max-width: 350px;
        z-index: 10;
        pointer-events: none;
    }

    .selected-memory-card {
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(15px);
        border-left: 3px solid #2196f3;
        padding: 1.5rem;
        border-radius: 0 16px 16px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .selected-memory-card.kintsugi {
        border-left-color: #ffd700;
    }

    .mem-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .mem-date {
        font-family: monospace;
        color: rgba(255, 255, 255, 0.5);
    }
    .mem-type {
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 1px;
        color: #2196f3;
    }
    .selected-memory-card.kintsugi .mem-type {
        color: #ffd700;
    }

    .selected-memory-card h2 {
        margin: 0 0 0.5rem 0;
        font-weight: 400;
    }

    .mem-value {
        margin: 0;
        color: rgba(255, 255, 255, 0.8);
    }

    .kintsugi-scar {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px dashed rgba(255, 215, 0, 0.3);
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }

    .scar-details {
        display: flex;
        flex-direction: column;
    }
    .scar-lbl {
        color: #ffd700;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .scar-txt {
        color: white;
        font-size: 0.9rem;
        font-style: italic;
    }

    /* Timeline Panel */
    .timeline-panel h3 {
        margin: 0 0 2rem 0;
        font-weight: 300;
        letter-spacing: 1px;
        color: rgba(255, 255, 255, 0.7);
    }

    .timeline-container {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        flex: 1;
        overflow-y: auto;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Custom scrollbar for timeline */
    .timeline-container::-webkit-scrollbar {
        width: 4px;
    }
    .timeline-container::-webkit-scrollbar-track {
        background: transparent;
    }
    .timeline-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    .timeline-spine {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 1.5rem; /* center of dot */
        width: 2px;
        background: linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0) 100%
        );
        z-index: 1;
    }

    .timeline-node {
        position: relative;
        display: flex;
        gap: 1.5rem;
        cursor: pointer;
        z-index: 2;
        transition: transform 0.2s ease;
    }

    .timeline-node:hover {
        transform: translateX(5px);
    }

    .timeline-dot {
        width: 1rem;
        height: 1rem;
        border-radius: 50%;
        background: #0a0a0f;
        border: 2px solid rgba(255, 255, 255, 0.3);
        z-index: 2;
        margin-top: 0.2rem;
        transition: all 0.3s ease;
    }

    .timeline-node.selected .timeline-dot {
        background: #2196f3;
        border-color: #2196f3;
        box-shadow: 0 0 15px rgba(33, 150, 243, 0.5);
    }

    .timeline-node.is-kintsugi .timeline-dot {
        border-color: #ffd700;
    }
    .timeline-node.selected.is-kintsugi .timeline-dot {
        background: #ffd700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }

    .node-content {
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .node-time {
        font-family: monospace;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 0.25rem;
    }
    .node-title {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        transition: color 0.3s ease;
    }

    .timeline-node.selected .node-title {
        color: white;
        font-weight: 500;
    }
    .timeline-node.is-kintsugi .node-title {
        color: rgba(255, 215, 0, 0.7);
    }
    .timeline-node.selected.is-kintsugi .node-title {
        color: #ffd700;
    }

    @media (max-width: 1024px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
        .crystal-panel {
            height: 400px;
        }
        .crystal-details {
            max-width: 250px;
        }
    }
</style>
