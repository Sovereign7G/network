<script lang="ts">
    import { onMount } from "svelte";
    import { fly, fade } from "svelte/transition";
    import { quintOut } from "svelte/easing";

    // Node telemetry mock data
    let globalTps = 8472;
    let activeNodes = 378000;
    let networkLoad = 68;
    let bandwidth = 847; // Tbps

    // Region data
    let regions = [
        { name: "North America", nodes: 124000, load: 75, status: "stable" },
        { name: "Europe", nodes: 98000, load: 62, status: "stable" },
        { name: "Asia Pacific", nodes: 145000, load: 88, status: "high" },
        { name: "South America", nodes: 8000, load: 45, status: "stable" },
        { name: "Africa", nodes: 3000, load: 30, status: "stable" },
    ];

    // Specific user nodes
    let myNodes = [
        {
            id: "n-1",
            name: "Validator Alpha",
            type: "S4 Backbone",
            uptime: "99.99%",
            earnings: "450 SYND/mo",
            status: "online",
        },
        {
            id: "n-2",
            name: "Edge Node Beta",
            type: "S3 Edge",
            uptime: "99.95%",
            earnings: "120 SYND/mo",
            status: "online",
        },
        {
            id: "n-3",
            name: "Storage Gamma",
            type: "S2 Storage",
            uptime: "99.8%",
            earnings: "85 SYND/mo",
            status: "syncing",
        },
    ];

    // Canvas context
    let canvas;
    let ctx;
    let animationFrame;
    let particles = [];

    onMount(() => {
        initCanvas();

        // Simulate real-time data
        const interval = setInterval(() => {
            globalTps = Math.floor(8000 + Math.random() * 1000);
            networkLoad = Math.floor(65 + Math.random() * 5);

            // Update region loads occasionally
            if (Math.random() > 0.7) {
                const randomRegion = Math.floor(Math.random() * regions.length);
                regions[randomRegion].load = Math.max(
                    30,
                    Math.min(
                        100,
                        regions[randomRegion].load + (Math.random() * 10 - 5),
                    ),
                );
                regions[randomRegion].status =
                    regions[randomRegion].load > 85 ? "high" : "stable";
            }
        }, 2000);

        return () => {
            clearInterval(interval);
            cancelAnimationFrame(animationFrame);
        };
    });

    function initCanvas() {
        canvas = document.getElementById("telemetry-canvas");
        if (!canvas) return;

        ctx = canvas.getContext("2d");
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        // Init particles
        for (let i = 0; i < 300; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 2 + 1,
                color: Math.random() > 0.8 ? "#FFD700" : "#4CAF50",
            });
        }

        animate();
    }

    function animate() {
        if (!ctx || !canvas) return;

        ctx.fillStyle = "rgba(10, 10, 15, 0.2)"; // Trail effect
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        particles.forEach((p) => {
            p.x += p.vx * (globalTps / 4000); // Speed scales with TPS
            p.y += p.vy * (globalTps / 4000);

            // Wrap around
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = p.color;
            ctx.fill();
        });

        // Draw central node pulse
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const pulseSize = 50 + Math.sin(Date.now() / 200) * 10;

        ctx.beginPath();
        ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);

        const gradient = ctx.createRadialGradient(
            centerX,
            centerY,
            0,
            centerX,
            centerY,
            pulseSize,
        );
        gradient.addColorStop(0, "rgba(255, 215, 0, 0.8)");
        gradient.addColorStop(1, "rgba(255, 215, 0, 0)");

        ctx.fillStyle = gradient;
        ctx.fill();

        // Draw connection lines from center occasionally
        ctx.strokeStyle = "rgba(255, 215, 0, 0.1)";
        ctx.lineWidth = 1;
        particles.forEach((p) => {
            if (Math.random() > 0.99) {
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(p.x, p.y);
                ctx.stroke();
            }
        });

        animationFrame = requestAnimationFrame(animate);
    }
</script>

<div class="node-dashboard">
    <div
        class="header-section"
        in:fly={{ y: -20, duration: 600, easing: quintOut }}
    >
        <div class="title-area">
            <h1><span class="glow">⚡</span> Node Telemetry</h1>
            <p>Sovereign infrastructure command center</p>
        </div>

        <div class="quick-actions">
            <button
                class="action-btn primary"
                title="Deploy a new sovereign node to the mesh"
                >Deploy New Node</button
            >
            <button
                class="action-btn secondary"
                title="View live node logs and telemetry">View Logs</button
            >
        </div>
    </div>

    <div class="main-grid">
        <!-- Centerpiece: Live Telemetry Canvas -->
        <div
            class="telemetry-panel glass-card"
            in:fade={{ duration: 800 }}
            title="Live WebGL particle visualization of TPS and network coherence"
        >
            <canvas id="telemetry-canvas"></canvas>
            <div class="telemetry-overlay">
                <div
                    class="big-metric"
                    title="Current Global Transactions Per Second (TPS)"
                >
                    <span class="value">{globalTps.toLocaleString()}</span>
                    <span class="label">Live TPS</span>
                </div>
                <div class="status-indicator">
                    <span class="dot active"></span>
                    Mesh Coherent
                </div>
            </div>
        </div>

        <!-- Quick Stats column -->
        <div class="stats-column">
            <div
                class="stat-card glass-card"
                in:fly={{ x: 20, duration: 400, delay: 100 }}
                title="Total active nodes on the Sovereign network"
            >
                <span class="label">Active Nodes</span>
                <span class="value success">{activeNodes.toLocaleString()}</span
                >
            </div>
            <div
                class="stat-card glass-card"
                in:fly={{ x: 20, duration: 400, delay: 200 }}
                title="Current global network load capacity"
            >
                <span class="label">Network Load</span>
                <div class="progress-bar">
                    <div
                        class="fill"
                        style="width: {networkLoad}%"
                        class:warning={networkLoad > 80}
                    ></div>
                </div>
                <span class="sub-label">{networkLoad}% Capacity</span>
            </div>
            <div
                class="stat-card glass-card"
                in:fly={{ x: 20, duration: 400, delay: 300 }}
                title="Total global bandwidth running through the mesh"
            >
                <span class="label">Global Bandwidth</span>
                <span class="value highlight">{bandwidth} Tbps</span>
            </div>
        </div>

        <!-- Regional Distribution -->
        <div
            class="regions-panel glass-card"
            in:fly={{ y: 20, duration: 500, delay: 200 }}
            title="Live distribution of node clusters across the globe"
        >
            <h3>Regional Load Distribution</h3>
            <div class="region-list">
                {#each regions as region}
                    <div class="region-item">
                        <div class="region-info">
                            <span class="region-name">{region.name}</span>
                            <span class="region-nodes"
                                >{(region.nodes / 1000).toFixed(1)}k nodes</span
                            >
                        </div>
                        <div class="region-load">
                            <div class="load-bar">
                                <div
                                    class="load-fill"
                                    style="width: {region.load}%"
                                    class:high={region.status === "high"}
                                ></div>
                            </div>
                            <span class="load-text"
                                >{Math.round(region.load)}%</span
                            >
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- My Nodes -->
        <div
            class="my-nodes-panel glass-card"
            in:fly={{ y: 20, duration: 500, delay: 400 }}
            title="Your personally deployed and managed nodes"
        >
            <h3>My Fleet</h3>
            <div class="node-table-wrapper">
                <table class="node-table">
                    <thead>
                        <tr>
                            <th>Node Name</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Uptime</th>
                            <th>Yield (Epoch)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each myNodes as node}
                            <tr>
                                <td class="node-name-cell">
                                    <span class="node-icon">⚡</span>
                                    {node.name}
                                </td>
                                <td
                                    ><span class="badge type">{node.type}</span
                                    ></td
                                >
                                <td>
                                    <span class="badge status {node.status}">
                                        <span class="dot"></span>
                                        {node.status}
                                    </span>
                                </td>
                                <td class="uptime">{node.uptime}</td>
                                <td class="yield">{node.earnings}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<style>
    .node-dashboard {
        padding: 2rem;
        max-width: 1600px;
        margin: 0 auto;
        color: white;
    }

    .header-section {
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
        color: #ffd700;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }

    .title-area p {
        color: rgba(255, 255, 255, 0.5);
        margin: 0;
        font-size: 1.1rem;
    }

    .quick-actions {
        display: flex;
        gap: 1rem;
    }

    .action-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .action-btn.primary {
        background: #ffd700;
        color: #0a0a0f;
        border: none;
    }
    .action-btn.primary:hover {
        background: #ffc000;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }

    .action-btn.secondary {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .action-btn.secondary:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .main-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        grid-template-rows: auto auto;
        gap: 1.5rem;
    }

    .glass-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        transition:
            border-color 0.3s ease,
            box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Telemetry Panel */
    .telemetry-panel {
        grid-column: 1;
        position: relative;
        height: 350px;
        padding: 0;
        overflow: hidden;
    }

    #telemetry-canvas {
        width: 100%;
        height: 100%;
        display: block;
    }

    .telemetry-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 2rem;
        background: linear-gradient(to top, rgba(10, 10, 15, 0.9), transparent);
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .big-metric .value {
        display: block;
        font-size: 4rem;
        font-weight: 300;
        line-height: 1;
        background: linear-gradient(90deg, #ffd700, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .big-metric .label {
        text-transform: uppercase;
        letter-spacing: 2px;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 0, 0, 0.5);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(76, 175, 80, 0.3);
        color: #4caf50;
        font-size: 0.9rem;
    }

    .status-indicator .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4caf50;
        box-shadow: 0 0 10px #4caf50;
        animation: pulse 2s infinite;
    }

    /* Stats Column */
    .stats-column {
        grid-column: 2;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .stat-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex: 1;
    }

    .stat-card .label {
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .stat-card .value {
        font-size: 2.5rem;
        font-weight: 300;
    }
    .stat-card .value.success {
        color: #4caf50;
    }
    .stat-card .value.highlight {
        color: #ffd700;
    }

    .progress-bar {
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    .progress-bar .fill {
        height: 100%;
        background: #2196f3;
        transition: width 0.3s ease;
    }
    .progress-bar .fill.warning {
        background: #ff9800;
    }

    .sub-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        align-self: flex-end;
    }

    /* Regions Panel */
    .regions-panel {
        grid-column: 1;
    }

    h3 {
        margin: 0 0 1.5rem 0;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.9);
    }

    .region-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .region-item {
        display: grid;
        grid-template-columns: 1fr 2fr;
        align-items: center;
        gap: 2rem;
    }

    .region-info {
        display: flex;
        flex-direction: column;
    }

    .region-name {
        font-weight: 500;
    }
    .region-nodes {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
    }

    .region-load {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .load-bar {
        flex: 1;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
    }

    .load-fill {
        height: 100%;
        background: #4caf50;
        border-radius: 2px;
        transition: width 0.5s ease;
    }
    .load-fill.high {
        background: #ff9800;
        box-shadow: 0 0 8px rgba(255, 152, 0, 0.5);
    }

    .load-text {
        width: 40px;
        text-align: right;
        font-family: monospace;
        color: rgba(255, 255, 255, 0.7);
    }

    /* My Nodes Panel */
    .my-nodes-panel {
        grid-column: 1 / -1;
    }

    .node-table-wrapper {
        overflow-x: auto;
    }

    .node-table {
        width: 100%;
        border-collapse: collapse;
    }

    .node-table th,
    .node-table td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .node-table th {
        color: rgba(255, 255, 255, 0.5);
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    .node-table tr:hover td {
        background: rgba(255, 215, 0, 0.02);
    }

    .node-name-cell {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 500;
    }

    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .badge.type {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.8);
    }

    .badge.status.online {
        background: rgba(76, 175, 80, 0.1);
        color: #4caf50;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }
    .badge.status.syncing {
        background: rgba(33, 150, 243, 0.1);
        color: #2196f3;
        border: 1px solid rgba(33, 150, 243, 0.2);
    }

    .badge.status .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }
    .badge.status.online .dot {
        background: #4caf50;
    }
    .badge.status.syncing .dot {
        background: #2196f3;
        animation: blink 1s infinite;
    }

    .uptime {
        font-family: monospace;
        color: rgba(255, 255, 255, 0.7);
    }
    .yield {
        color: #ffd700;
        font-weight: 500;
    }

    @keyframes pulse {
        0% {
            opacity: 0.5;
            transform: scale(0.8);
        }
        50% {
            opacity: 1;
            transform: scale(1.2);
        }
        100% {
            opacity: 0.5;
            transform: scale(0.8);
        }
    }

    @keyframes blink {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.3;
        }
    }

    @media (max-width: 1024px) {
        .main-grid {
            grid-template-columns: 1fr;
        }
        .stats-column {
            grid-column: 1;
            flex-direction: row;
        }
    }

    @media (max-width: 768px) {
        .stats-column {
            flex-direction: column;
        }
        .region-item {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
    }
</style>
