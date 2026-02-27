<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🚀 SOVEREIGN EDGE SCALER: PROACTIVE AUTOSCALING PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // Visualizing predictive resource manifolds and SLO-aware edge scaling.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, slide } from "svelte/transition";
    import {
        Zap,
        TrendingUp,
        TrendingDown,
        Activity,
        Timer,
        Cpu,
        ShieldAlert,
        Clock,
    } from "lucide-svelte";
    import { sovereignEdgeScaler } from "$lib/services/edge-scaler.svelte";
    import { sovereignStore } from "$lib/stores/sovereign-store.svelte";
    import { Flame } from "lucide-svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    const advancedMode = $derived(
        sovereignStore.state.preferences.advancedMode,
    );
    let activeTab = $state<"nodes" | "predictive" | "events" | "stress">(
        "nodes",
    );

    $effect(() => {
        if (!advancedMode && activeTab !== "nodes") {
            activeTab = "nodes";
        }
    });

    // ─── UTILS ──────────────────────────────────────────────────────────────

    function getStatusColor(status: string) {
        switch (status) {
            case "healthy":
                return "#10b981";
            case "starting":
                return "#3b82f6";
            case "scaling_down":
                return "#f59e0b";
            case "exhausted":
                return "#ef4444";
            default:
                return "#94a3b8";
        }
    }
</script>

<div class="scaler-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <Zap size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Edge Scaler</h3>
                <p>Proactive Resource Manifold</p>
            </div>
        </div>
        <div class="global-metrics">
            {#if sovereignEdgeScaler.stats.concavity !== "flat"}
                <div
                    class="concavity-badge {sovereignEdgeScaler.stats
                        .concavity}"
                    in:fade
                >
                    <Activity size={10} />
                    <span
                        >{sovereignEdgeScaler.stats.concavity === "up"
                            ? "Accelerating Surge"
                            : "Decelerating Load"}</span
                    >
                </div>
            {/if}
            <div class="m-item">
                <span class="l">HEADROOM</span>
                <span
                    class="v"
                    class:warning={sovereignEdgeScaler.metrics.cpuHeadroom < 30}
                >
                    {sovereignEdgeScaler.stats.headroom}
                </span>
            </div>
            <div class="m-item">
                <span class="l">NODES</span>
                <span class="v">{sovereignEdgeScaler.stats.nodes}</span>
            </div>
        </div>
    </header>

    <!-- 🎚️ VIEW CONTROLS -->
    <div class="view-tabs">
        <button
            class:active={activeTab === "nodes"}
            onclick={() => (activeTab = "nodes")}>Nodes</button
        >
        {#if advancedMode}
            <button
                class:active={activeTab === "predictive"}
                onclick={() => (activeTab = "predictive")}
                transition:slide
            >
                Predictive
            </button>
            <button
                class:active={activeTab === "events"}
                onclick={() => (activeTab = "events")}
                transition:slide
            >
                Events
            </button>
            <button
                class:active={activeTab === "stress"}
                onclick={() => (activeTab = "stress")}
                transition:slide
                class="stress-tab"
            >
                Stress_Test
            </button>
        {/if}
    </div>

    <!-- 📄 CONTENT AREA -->
    <div class="content-scroll">
        {#if activeTab === "nodes"}
            <div class="nodes-grid" in:fade>
                {#each sovereignEdgeScaler.allReplicas as node (node.id)}
                    <div
                        class="node-card"
                        class:starting={node.status === "starting"}
                        in:fly={{ y: 20 }}
                    >
                        <div class="node-head">
                            <div
                                class="status-indicator"
                                style="background: {getStatusColor(
                                    node.status,
                                )}"
                            ></div>
                            <div class="node-info">
                                <h6>{node.id}</h6>
                                <span>{node.region}</span>
                            </div>
                            {#if node.status === "starting"}
                                <span class="startup-pct"
                                    >{node.startupCompletion}%</span
                                >
                            {/if}
                        </div>

                        <div class="node-body">
                            <div class="stat-row">
                                <div class="stat">
                                    <Cpu size={12} />
                                    <span>{node.cpuUsage.toFixed(1)}%</span>
                                </div>
                                <div class="stat">
                                    <Timer size={12} />
                                    <span>{node.latencyP95.toFixed(1)}ms</span>
                                </div>
                            </div>
                            <div class="progress-bar">
                                <div
                                    class="fill"
                                    style="width: {node.cpuUsage}%"
                                ></div>
                            </div>
                        </div>

                        {#if node.status === "starting"}
                            <div class="startup-overlay">
                                <Activity size={24} class="spin" />
                                <span>Booting Edge Instance...</span>
                            </div>
                        {/if}
                    </div>
                {/each}
                <div class="empty-slot">
                    <TrendingUp size={24} class="muted" />
                    <span>Awaiting Load Spike</span>
                </div>
            </div>
        {:else if activeTab === "predictive"}
            <div class="predictive-view" in:fade>
                <div class="sl-box">
                    <div class="sl-header">
                        <ShieldAlert size={16} />
                        <h4>Latency SLO Guard</h4>
                    </div>
                    <div class="sl-metrics">
                        <div class="sl-item">
                            <span class="label">P95 LATENCY</span>
                            <span class="value"
                                >{sovereignEdgeScaler.stats.latency}</span
                            >
                        </div>
                        <div class="sl-item">
                            <span class="label">ACCURACY</span>
                            <span class="value success"
                                >{sovereignEdgeScaler.stats.accuracy}</span
                            >
                        </div>
                    </div>
                    <div class="graph-placeholder">
                        <!-- Abstract Wave Representation -->
                        <div class="wave-container">
                            {#each Array(10) as _, i}
                                <div
                                    class="wave-bar"
                                    style="height: {30 +
                                        Math.random() *
                                            60}%; animation-delay: {i * 0.1}s"
                                ></div>
                            {/each}
                        </div>
                        <p class="graph-label">
                            Predictive Load Curve vs Spare Capacity
                        </p>
                    </div>
                </div>
            </div>
        {:else if activeTab === "events"}
            <div class="events-view" in:fade>
                <div class="events-list">
                    {#each sovereignEdgeScaler.allEvents as event}
                        <div class="event-item" transition:slide>
                            <div
                                class="event-icon"
                                class:up={event.type === "SCALE_UP"}
                                class:down={event.type === "SCALE_DOWN"}
                            >
                                {#if event.type === "SCALE_UP"}
                                    <TrendingUp size={14} />
                                {:else}
                                    <TrendingDown size={14} />
                                {/if}
                            </div>
                            <div class="event-details">
                                <div class="event-top">
                                    <span class="e-type">{event.type}</span>
                                    <span class="e-time"
                                        >{new Date(
                                            event.timestamp,
                                        ).toLocaleTimeString()}</span
                                    >
                                </div>
                                <p class="e-reason">{event.reason}</p>
                            </div>
                        </div>
                    {/each}

                    {#if sovereignEdgeScaler.allEvents.length === 0}
                        <div class="empty-events">
                            <Clock size={48} class="muted" />
                            <p>
                                No scaling events detected in this manifold
                                epoch.
                            </p>
                        </div>
                    {/if}
                </div>
            </div>
        {:else if activeTab === "stress"}
            <div class="stress-view" in:fade>
                <div class="stress-box">
                    <div class="stress-header">
                        <Flame size={24} class="text-orange-500" />
                        <h4>Institutional_Stress_Manifold</h4>
                    </div>
                    <p class="stress-desc">
                        Simulate extreme network congestion or institutional
                        attacks to verify edge resilience and autoscaling
                        vectors.
                    </p>
                    <div class="stress-controls">
                        <button
                            class="stress-btn"
                            onclick={() => alert("Simulating flash surge...")}
                        >
                            Simulate_Flash_Surge
                        </button>
                        <button
                            class="stress-btn peril"
                            onclick={() =>
                                alert("Simulating node exhaustion...")}
                        >
                            Simulate_Hostile_Exhaustion
                        </button>
                    </div>
                    <div class="stress-warning">
                        ⚠️ CAUTION: Stress testing increases resource usage and
                        may affect temporary resonance.
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .scaler-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(10, 12, 18, 0.85);
        backdrop-filter: blur(30px);
        color: #f1f5f9;
        font-family: "Outfit", sans-serif;
    }

    .panel-header {
        padding: 1.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .logo-orb {
        width: 34px;
        height: 34px;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
    }

    :global(.accent-icon) {
        color: #000;
        font-weight: 800;
    }

    .title-group h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    .title-group p {
        margin: 0;
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 500;
    }

    .global-metrics {
        display: flex;
        gap: 1.5rem;
        margin-left: auto;
        align-items: center;
    }

    .concavity-badge {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.6rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .concavity-badge.up {
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.2);
    }

    .concavity-badge.down {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .m-item {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .m-item .l {
        font-size: 0.6rem;
        font-weight: 800;
        color: #475569;
        letter-spacing: 0.05em;
    }
    .m-item .v {
        font-size: 0.95rem;
        font-weight: 800;
        font-family: "JetBrains Mono";
    }
    .v.warning {
        color: #f43f5e;
        text-shadow: 0 0 8px rgba(244, 63, 94, 0.3);
    }

    .view-tabs {
        padding: 0.5rem 1.25rem;
        display: flex;
        gap: 1.5rem;
        background: rgba(255, 255, 255, 0.01);
    }

    .view-tabs button {
        background: none;
        border: none;
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.5rem 0;
        cursor: pointer;
        position: relative;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: color 0.2s;
    }

    .view-tabs button.active {
        color: #fbbf24;
    }
    .view-tabs button.active::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #fbbf24;
        border-radius: 2px;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* NODES GRID */
    .nodes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        grid-auto-rows: auto;
        gap: 1rem;
        align-items: start;
    }

    .node-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        /* corner-shape: var(--ss-sem-geom-card); - Non-standard */
        clip-path: polygon(
            0 10px,
            10px 0,
            calc(100% - 10px) 0,
            100% 10px,
            100% calc(100% - 10px),
            calc(100% - 10px) 100%,
            10px 100%,
            0 calc(100% - 10px)
        ); /* High-Assurance Bevel Fallback */
        padding: 1rem;

        /* 📐 SUBGRID MANIFOLD */
        display: grid;
        grid-template-rows: subgrid;
        grid-row: span 2;
        gap: 0.75rem;

        position: relative;
        overflow: hidden;
    }

    .node-card.starting {
        border-color: #3b82f6;
    }

    .node-head {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        box-shadow: 0 0 10px currentColor;
    }
    .node-info h6 {
        margin: 0;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .node-info span {
        font-size: 0.65rem;
        color: #475569;
        font-weight: 700;
    }

    .node-body {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .stat-row {
        display: flex;
        gap: 1rem;
    }
    .stat {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 600;
    }

    .progress-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .progress-bar .fill {
        height: 100%;
        background: #fbbf24;
        border-radius: 2px;
        transition: width 0.5s ease-out;
    }

    .startup-overlay {
        position: absolute;
        inset: 0;
        background: rgba(10, 12, 18, 0.9);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .startup-overlay span {
        font-size: 0.65rem;
        font-weight: 800;
        color: #3b82f6;
        text-transform: uppercase;
    }
    .startup-pct {
        margin-left: auto;
        font-size: 0.7rem;
        font-weight: 800;
        color: #3b82f6;
    }

    .empty-slot {
        border: 2px dashed rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        color: #1e293b;
    }
    .empty-slot span {
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* PREDICTIVE */
    .sl-box {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .sl-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #f43f5e;
    }
    .sl-header h4 {
        margin: 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .sl-metrics {
        display: flex;
        gap: 2rem;
    }
    .sl-item {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .sl-item .label {
        font-size: 0.6rem;
        font-weight: 800;
        color: #475569;
    }
    .sl-item .value {
        font-size: 1.25rem;
        font-weight: 900;
        font-family: "JetBrains Mono";
    }

    .graph-placeholder {
        height: 120px;
        background: rgba(255, 255, 255, 0.01);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .wave-container {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 60px;
    }
    .wave-bar {
        width: 12px;
        background: linear-gradient(to top, #fbbf24, transparent);
        border-radius: 4px 4px 0 0;
        animation: wave 2s ease-in-out infinite;
    }

    @keyframes wave {
        0%,
        100% {
            transform: scaleY(1);
        }
        50% {
            transform: scaleY(0.6);
        }
    }

    .graph-label {
        margin-top: 1rem;
        font-size: 0.65rem;
        color: #475569;
        font-weight: 700;
    }

    /* EVENTS */
    .events-view {
        display: flex;
        flex-direction: column;
    }
    .events-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .event-item {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 0.75rem;
        display: flex;
        gap: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .event-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .event-icon.up {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    .event-icon.down {
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
    }

    .event-details {
        flex: 1;
    }
    .event-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .e-type {
        font-size: 0.65rem;
        font-weight: 800;
    }
    .e-time {
        font-size: 0.6rem;
        color: #475569;
        font-family: "JetBrains Mono";
    }
    .e-reason {
        margin: 0.25rem 0 0;
        font-size: 0.75rem;
        color: #94a3b8;
        font-weight: 500;
    }

    .empty-events {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
        color: #1e293b;
    }
    .empty-events p {
        margin-top: 1rem;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .success {
        color: #10b981;
    }
    :global(.spin) {
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .stress-tab {
        color: #f97316 !important;
    }
    .stress-tab.active::after {
        background: #f97316 !important;
    }

    .stress-box {
        background: rgba(249, 115, 22, 0.05);
        border: 1px solid rgba(249, 115, 22, 0.1);
        border-radius: 20px;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .stress-header {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .stress-header h4 {
        margin: 0;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #f97316;
    }

    .stress-desc {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.6;
    }

    .stress-controls {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .stress-btn {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s;
    }

    .stress-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }

    .stress-btn.peril:hover {
        background: rgba(244, 63, 94, 0.1);
        border-color: #f43f5e;
        color: #f43f5e;
    }

    .stress-warning {
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        font-size: 0.7rem;
        color: #94a3b8;
        font-style: italic;
    }

    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
