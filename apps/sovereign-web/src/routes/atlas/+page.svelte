<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { fly, fade } from "svelte/transition";
    import { quintOut } from "svelte/easing";

    // Network data
    let nodes = [
        {
            id: "node-1",
            name: "S-Node Lisbon",
            type: "backbone",
            location: "Lisbon, PT",
            status: "active",
            uptime: 99.99,
            peers: 47,
            latency: 12,
        },
        {
            id: "node-2",
            name: "S-Node Tokyo",
            type: "edge",
            location: "Tokyo, JP",
            status: "active",
            uptime: 99.97,
            peers: 89,
            latency: 24,
        },
        {
            id: "node-3",
            name: "S-Node NYC",
            type: "backbone",
            location: "New York, US",
            status: "active",
            uptime: 99.99,
            peers: 124,
            latency: 8,
        },
        {
            id: "node-4",
            name: "S-Node São Paulo",
            type: "edge",
            location: "São Paulo, BR",
            status: "degraded",
            uptime: 98.2,
            peers: 23,
            latency: 47,
        },
        {
            id: "node-5",
            name: "S-Node Berlin",
            type: "backbone",
            location: "Berlin, DE",
            status: "active",
            uptime: 99.98,
            peers: 92,
            latency: 15,
        },
        {
            id: "node-6",
            name: "S-Node Singapore",
            type: "edge",
            location: "Singapore, SG",
            status: "active",
            uptime: 99.95,
            peers: 67,
            latency: 19,
        },
        {
            id: "node-7",
            name: "S-Node Cape Town",
            type: "edge",
            location: "Cape Town, ZA",
            status: "active",
            uptime: 99.4,
            peers: 12,
            latency: 42,
        },
        {
            id: "node-8",
            name: "S-Node Sydney",
            type: "edge",
            location: "Sydney, AU",
            status: "maintenance",
            uptime: 99.2,
            peers: 8,
            latency: 38,
        },
    ];

    // Network statistics
    let stats = {
        totalNodes: 389000,
        activeNodes: 378000,
        backboneNodes: 847,
        edgeNodes: 389000 - 847,
        totalPeers: 1247000,
        avgLatency: 47,
        networkLoad: 67,
        bandwidth: "847 Tbps",
    };

    // Filter state
    let filterStatus = $state("all");
    let filterType = $state("all");
    let searchQuery = $state("");

    let filteredNodes = $derived(
        nodes.filter((node) => {
            if (filterStatus !== "all" && node.status !== filterStatus)
                return false;
            if (filterType !== "all" && node.type !== filterType) return false;
            if (
                searchQuery &&
                !node.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
                !node.location.toLowerCase().includes(searchQuery.toLowerCase())
            )
                return false;
            return true;
        }),
    );

    let selectedNode: string | null = $state(null);
    let hoveredNode: string | null = $state(null);

    // Canvas visualization
    let canvas: HTMLCanvasElement | null = $state(null);
    let ctx: CanvasRenderingContext2D | null = $state(null);
    let animationFrame: number = $state(0);
    let mounted = $state(false);

    onMount(() => {
        mounted = true;
        initCanvas();
        return () => {
            if (animationFrame) cancelAnimationFrame(animationFrame);
        };
    });

    function initCanvas() {
        canvas = document.getElementById('network-canvas') as HTMLCanvasElement | null as HTMLCanvasElement;
        if (!canvas) return;

        ctx = canvas.getContext("2d");
        if (!ctx) return;

        canvas.width = canvas.offsetWidth;
        canvas.height = 400;

        animate();
    }

    function animate() {
        if (!ctx || !canvas) return;

        const currentCtx = ctx;
        const currentCanvas = canvas;

        currentCtx.clearRect(0, 0, currentCanvas.width, currentCanvas.height);

        // Draw network connections
        currentCtx.strokeStyle = "rgba(255, 215, 0, 0.1)";
        currentCtx.lineWidth = 1;

        // Draw nodes as glowing orbs
        const nodePositions = nodes.map((node, i) => ({
            x: 100 + ((i * 120) % (currentCanvas.width - 200)),
            y: 100 + Math.floor(i / 6) * 100,
            node,
        }));

        // Draw connections between nearby nodes
        for (let i = 0; i < nodePositions.length; i++) {
            for (let j = i + 1; j < nodePositions.length; j++) {
                const dist = Math.hypot(
                    nodePositions[i].x - nodePositions[j].x,
                    nodePositions[i].y - nodePositions[j].y,
                );

                if (dist < 150) {
                    currentCtx.beginPath();
                    currentCtx.moveTo(nodePositions[i].x, nodePositions[i].y);
                    currentCtx.lineTo(nodePositions[j].x, nodePositions[j].y);
                    currentCtx.strokeStyle = `rgba(255, 215, 0, ${0.1 * (1 - dist / 150)})`;
                    currentCtx.stroke();
                }
            }
        }

        // Draw nodes
        nodePositions.forEach((pos, i) => {
            const isSelected = selectedNode === nodes[i].id;
            const isHovered = hoveredNode === nodes[i].id;

            currentCtx.beginPath();
            currentCtx.arc(pos.x, pos.y, isSelected ? 12 : 8, 0, Math.PI * 2);

            // Color based on status
            let color;
            switch (nodes[i].status) {
                case "active":
                    color = "#4CAF50";
                    break;
                case "degraded":
                    color = "#FF9800";
                    break;
                case "maintenance":
                    color = "#9C27B0";
                    break;
                default:
                    color = "#FFD700";
            }

            const gradient = currentCtx.createRadialGradient(
                pos.x - 3,
                pos.y - 3,
                0,
                pos.x,
                pos.y,
                20,
            );
            gradient.addColorStop(0, color);
            gradient.addColorStop(1, "rgba(0,0,0,0.5)");

            currentCtx.fillStyle = gradient;
            currentCtx.shadowColor = color;
            currentCtx.shadowBlur = isSelected ? 30 : 15;
            currentCtx.fill();

            // Label on hover
            if (isHovered) {
                currentCtx.shadowBlur = 0;
                currentCtx.fillStyle = "white";
                currentCtx.font = "12px Inter";
                currentCtx.textAlign = "center";
                currentCtx.fillText(nodes[i].name, pos.x, pos.y - 20);
            }
        });

        animationFrame = requestAnimationFrame(animate);
    }

    function handleNodeClick(nodeId: string) {
        selectedNode = selectedNode === nodeId ? null : nodeId;
    }
</script>

{#if mounted}
    <div class="atlas-cathedral">
        <!-- Header -->
        <div
            class="atlas-header"
            in:fly={{ y: -20, duration: 500, easing: quintOut }}
        >
            <div>
                <h1 class="chapter-title">
                    <span class="title-glow">🗺️</span>
                    Sovereign Atlas
                </h1>
                <p class="chapter-subtitle">
                    Live network topology and node intelligence
                </p>
            </div>

            <div class="global-stats">
                <div
                    class="stat-pill"
                    title="Total active and inactive nodes known to the network"
                >
                    <span class="stat-label">Total Nodes</span>
                    <span class="stat-value"
                        >{stats.totalNodes.toLocaleString()}</span
                    >
                </div>
                <div
                    class="stat-pill"
                    title="Currently active and validating nodes"
                >
                    <span class="stat-label">Active</span>
                    <span class="stat-value success"
                        >{stats.activeNodes.toLocaleString()}</span
                    >
                </div>
                <div
                    class="stat-pill"
                    title="Average network latency in milliseconds"
                >
                    <span class="stat-label">Latency</span>
                    <span class="stat-value">{stats.avgLatency}ms</span>
                </div>
                <div class="stat-pill" title="Total global network bandwidth">
                    <span class="stat-label">Bandwidth</span>
                    <span class="stat-value">{stats.bandwidth}</span>
                </div>
            </div>
        </div>

        <!-- Network Visualization Canvas -->
        <div
            class="network-canvas-container glass-panel"
            in:fade={{ duration: 600 }}
            title="Live Canvas topological representation of network nodes"
        >
            <canvas id="network-canvas" class="network-canvas"></canvas>
        </div>

        <!-- Controls -->
        <div
            class="atlas-controls glass-panel"
            in:fly={{ y: 20, duration: 500, delay: 100 }}
        >
            <div class="filters">
                <div class="filter-group">
                    <label for="status-filter">Status</label>
                    <select
                        id="status-filter"
                        bind:value={filterStatus}
                        class="glass-select"
                    >
                        <option value="all">All Nodes</option>
                        <option value="active">Active</option>
                        <option value="degraded">Degraded</option>
                        <option value="maintenance">Maintenance</option>
                    </select>
                </div>

                <div class="filter-group">
                    <label for="type-filter">Type</label>
                    <select
                        id="type-filter"
                        bind:value={filterType}
                        class="glass-select"
                    >
                        <option value="all">All Types</option>
                        <option value="backbone">Backbone (S4)</option>
                        <option value="edge">Edge (S3)</option>
                    </select>
                </div>

                <div class="filter-group search">
                    <label for="search-filter">Search</label>
                    <input
                        id="search-filter"
                        type="text"
                        bind:value={searchQuery}
                        placeholder="Search nodes..."
                        class="glass-input"
                    />
                </div>
            </div>

            <div class="legend">
                <div class="legend-item">
                    <span class="legend-dot active"></span>
                    <span>Active</span>
                </div>
                <div class="legend-item">
                    <span class="legend-dot degraded"></span>
                    <span>Degraded</span>
                </div>
                <div class="legend-item">
                    <span class="legend-dot maintenance"></span>
                    <span>Maintenance</span>
                </div>
                <div class="legend-item">
                    <span class="legend-dot backbone"></span>
                    <span>Backbone (S4)</span>
                </div>
                <div class="legend-item">
                    <span class="legend-dot edge"></span>
                    <span>Edge (S3)</span>
                </div>
            </div>
        </div>

        <!-- Node Cards Grid - NOT plain text, elegant glass cards -->
        <div class="nodes-grid">
            {#each filteredNodes as node}
                <div
                    class="node-card glass-panel"
                    role="button"
                    tabindex="0"
                    class:selected={selectedNode === node.id}
                    onmouseenter={() => (hoveredNode = node.id)}
                    onmouseleave={() => (hoveredNode = null)}
                    onclick={() => handleNodeClick(node.id)}
                    onkeydown={(e: KeyboardEvent) =>
                        e.key === "Enter" && handleNodeClick(node.id)}
                    title="Click to view details for {node.name}"
                    in:fly={{
                        y: 20,
                        duration: 400,
                        delay: 100 + Math.random() * 100,
                    }}
                >
                    <div class="node-header">
                        <div class="node-status">
                            <span class="status-indicator {node.status}"></span>
                            <span class="node-type">{node.type}</span>
                        </div>
                        <span class="node-icon">
                            {node.type === "backbone" ? "🏛️" : "⚡"}
                        </span>
                    </div>

                    <h3 class="node-name">{node.name}</h3>
                    <p class="node-location">{node.location}</p>

                    <div class="node-metrics">
                        <div class="metric">
                            <span class="metric-label">Uptime</span>
                            <span class="metric-value">{node.uptime}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Peers</span>
                            <span class="metric-value">{node.peers}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Latency</span>
                            <span class="metric-value">{node.latency}ms</span>
                        </div>
                    </div>

                    {#if selectedNode === node.id}
                        <div class="node-actions">
                            <button
                                class="node-action"
                                onclick={(e: MouseEvent) => {
                                    e.stopPropagation();
                                    goto(`/node/${node.id}`);
                                }}
                                title="Manage Sovereign Node"
                            >
                                Manage
                            </button>
                            <button
                                class="node-action"
                                onclick={(e: MouseEvent) => {
                                    e.stopPropagation();
                                    goto(`/node/${node.id}/logs`);
                                }}
                                title="View System Logs"
                            >
                                Logs
                            </button>
                        </div>
                    {/if}
                </div>
            {/each}
        </div>

        <!-- Empty state -->
        {#if filteredNodes.length === 0}
            <div class="empty-state glass-panel">
                <span class="empty-icon">🔍</span>
                <h3>No nodes found</h3>
                <p>Try adjusting your filters</p>
            </div>
        {/if}
    </div>
{/if}

<style>
    .atlas-cathedral {
        padding: 2rem;
        max-width: 1600px;
        margin: 0 auto;
    }

    .atlas-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        gap: 1rem;
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
        margin: 0;
    }

    .global-stats {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }

    .stat-pill {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 100px;
        padding: 0.5rem 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stat-label {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
    }

    .stat-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffd700;
    }

    .stat-value.success {
        color: #4caf50;
    }

    .glass-panel {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 24px;
        transition: all 0.3s ease;
    }

    .glass-panel:hover {
        border-color: rgba(255, 215, 0, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .network-canvas-container {
        width: 100%;
        height: 400px;
        margin-bottom: 2rem;
        overflow: hidden;
        padding: 0;
    }

    .network-canvas {
        width: 100%;
        height: 100%;
        display: block;
    }

    .atlas-controls {
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .filters {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }

    .filter-group {
        flex: 1;
        min-width: 150px;
    }

    .filter-group label {
        display: block;
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
    }

    .glass-select,
    .glass-input {
        width: 100%;
        padding: 0.75rem 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 12px;
        color: white;
        font-size: 0.9rem;
    }

    .glass-select:focus,
    .glass-input:focus {
        outline: none;
        border-color: #ffd700;
    }

    .legend {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        justify-content: center;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
    }

    .legend-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .legend-dot.active {
        background: #4caf50;
        box-shadow: 0 0 10px #4caf50;
    }
    .legend-dot.degraded {
        background: #ff9800;
        box-shadow: 0 0 10px #ff9800;
    }
    .legend-dot.maintenance {
        background: #9c27b0;
        box-shadow: 0 0 10px #9c27b0;
    }
    .legend-dot.backbone {
        background: #ffd700;
        box-shadow: 0 0 10px #ffd700;
    }
    .legend-dot.edge {
        background: #2196f3;
        box-shadow: 0 0 10px #2196f3;
    }

    .nodes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .node-card {
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        gap: 1rem;
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 24px;
        text-align: left;
    }

    .node-card:hover {
        transform: translateY(-4px);
        border-color: #ffd700;
    }

    .node-card.selected {
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
    }

    .node-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .node-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }

    .status-indicator.active {
        background: #4caf50;
        box-shadow: 0 0 10px #4caf50;
    }

    .status-indicator.degraded {
        background: #ff9800;
        box-shadow: 0 0 10px #ff9800;
    }

    .status-indicator.maintenance {
        background: #9c27b0;
        box-shadow: 0 0 10px #9c27b0;
    }

    .node-type {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.7rem;
        text-transform: uppercase;
    }

    .node-icon {
        font-size: 1.5rem;
    }

    .node-name {
        font-size: 1.2rem;
        margin: 0;
        color: white;
    }

    .node-location {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        margin: 0;
    }

    .node-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.5rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
    }

    .metric-label {
        font-size: 0.6rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
    }

    .metric-value {
        font-size: 1rem;
        font-weight: 600;
        color: #ffd700;
    }

    .node-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    .node-action {
        flex: 1;
        padding: 0.5rem;
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 8px;
        color: #ffd700;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .node-action:hover {
        background: #ffd700;
        color: #0a0a0f;
    }

    .empty-state {
        grid-column: 1 / -1;
        padding: 3rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
    }

    .empty-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 1rem;
    }

    .empty-state h3 {
        margin: 0 0 0.5rem;
        color: white;
    }

    @media (max-width: 768px) {
        .atlas-header {
            flex-direction: column;
            align-items: flex-start;
        }

        .filters {
            flex-direction: column;
        }

        .legend {
            justify-content: flex-start;
        }
    }
</style>
