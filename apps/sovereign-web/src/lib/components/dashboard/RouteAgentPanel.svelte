<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🗺️ SOVEREIGN ROUTE AGENT: AGENTIC OPTIMIZATION DASHBOARD
    // ═══════════════════════════════════════════════════════════════════════════
    // Tool-driven deterministic routing with structured outputs and auditable ETAs.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, slide } from "svelte/transition";
    import {
        Navigation,
        MapPin,
        Clock,
        Route,
        Zap,
        ShieldCheck,
        CheckCircle2,
        Trash2,
        Activity,
    } from "lucide-svelte";
    import {
        sovereignRouteAgent,
        TOKYO_SITES,
    } from "$lib/services/route-agent.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<"active" | "planner" | "analytics">("active");
    let selectedRouteId = $state<string | null>(null);
    let isPlanning = $state(false);

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    async function triggerPlan() {
        isPlanning = true;
        await sovereignRouteAgent.planRoute([...TOKYO_SITES], "ETA");
        isPlanning = false;
        activeTab = "active";
    }
</script>

<div class="route-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <Navigation size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Route Agent</h3>
                <p>Deterministic Optimization</p>
            </div>
        </div>
        <div class="global-metrics">
            <div class="m-item">
                <span class="l">ETA ACCURACY</span>
                <span class="v">{sovereignRouteAgent.stats.accuracy}</span>
            </div>
            <div class="m-item">
                <span class="l">GAIN</span>
                <span class="v">{sovereignRouteAgent.stats.gain}</span>
            </div>
        </div>
    </header>

    <!-- 🎚️ VIEW CONTROLS -->
    <div class="view-tabs">
        <button
            class:active={activeTab === "active"}
            onclick={() => (activeTab = "active")}>Live Routes</button
        >
        <button
            class:active={activeTab === "planner"}
            onclick={() => (activeTab = "planner")}>Agentic Planner</button
        >
        <button
            class:active={activeTab === "analytics"}
            onclick={() => (activeTab = "analytics")}>Audit</button
        >
    </div>

    <!-- 📄 CONTENT AREA -->
    <div class="content-scroll">
        {#if activeTab === "active"}
            <div class="routes-view" in:fade>
                <div class="routes-list">
                    {#each sovereignRouteAgent.allRoutes as route, i (route.id)}
                        <div
                            class="route-card"
                            role="button"
                            tabindex="0"
                            class:selected={selectedRouteId === route.id}
                            in:fly={{ x: -20, delay: i * 50 }}
                            onclick={() =>
                                (selectedRouteId =
                                    route.id === selectedRouteId
                                        ? null
                                        : route.id)}
                            onkeydown={(e) =>
                                e.key === "Enter" &&
                                (selectedRouteId =
                                    route.id === selectedRouteId
                                        ? null
                                        : route.id)}
                        >
                            <div class="card-top">
                                <span class="route-id">{route.id}</span>
                                <span class="obj-tag"
                                    >{route.optimizationObjective}</span
                                >
                                <div class="status-dot {route.status}"></div>
                            </div>

                            <div class="path-viz">
                                <div class="p-node"></div>
                                <div class="p-line"></div>
                                <div class="p-node"></div>
                                <div class="p-line"></div>
                                <div class="p-node final"></div>
                            </div>

                            <div class="card-stats">
                                <div class="c-stat">
                                    <Route size={12} />
                                    <span>{route.totalDistanceKm} km</span>
                                </div>
                                <div class="c-stat">
                                    <Clock size={12} />
                                    <span>{route.totalDurationMin} min</span>
                                </div>
                            </div>

                            {#if selectedRouteId === route.id}
                                <div class="expanded-stops" transition:slide>
                                    {#each route.stops as stop}
                                        <div class="stop-item">
                                            <MapPin
                                                size={10}
                                                class="pin-icon"
                                            />
                                            <div class="stop-info">
                                                <span class="s-name"
                                                    >{stop.name}</span
                                                >
                                                <span class="s-time"
                                                    >{new Date(
                                                        stop.estimatedArrival,
                                                    ).toLocaleTimeString([], {
                                                        hour: "2-digit",
                                                        minute: "2-digit",
                                                    })}</span
                                                >
                                            </div>
                                            {#if stop.delayMinutes > 0}
                                                <span class="delay-tag"
                                                    >+{stop.delayMinutes}m</span
                                                >
                                            {/if}
                                        </div>
                                    {/each}
                                    <button
                                        class="delete-btn"
                                        onclick={(e) => {
                                            e.stopPropagation();
                                            sovereignRouteAgent.deleteRoute(
                                                route.id,
                                            );
                                        }}
                                    >
                                        <Trash2 size={12} /> Drop Route
                                    </button>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeTab === "planner"}
            <div class="planner-view" in:fade>
                <div class="prompt-box">
                    <Navigation size={24} class="muted-icon" />
                    <h4>Agentic Multi-Stop Planner</h4>
                    <p>
                        The agent will use 3 deterministic tools to calculate
                        distances, resolve site ambiguities, and rank
                        optimization candidates.
                    </p>
                </div>

                <div class="site-list">
                    <span class="s-label">Active Dispatch Points</span>
                    {#each TOKYO_SITES as site}
                        <div class="site-card">
                            <CheckCircle2 size={14} class="success" />
                            <span>{site.name}</span>
                        </div>
                    {/each}
                </div>

                <button
                    class="plan-btn"
                    onclick={triggerPlan}
                    disabled={isPlanning}
                >
                    {#if isPlanning}
                        <Activity size={16} class="spin" />
                        <span>Consulting Optimizer Tools...</span>
                    {:else}
                        <Zap size={16} />
                        <span>Run Optimized Dispatch</span>
                    {/if}
                </button>
            </div>
        {:else if activeTab === "analytics"}
            <div class="audit-view" in:fade>
                <div class="audit-header">
                    <ShieldCheck size={18} />
                    <h4>Deterministic Audit Trail</h4>
                </div>
                <div class="metrics-grid">
                    <div class="a-stat">
                        <span class="al">Optimization Gain</span>
                        <span class="av">{sovereignRouteAgent.stats.gain}</span>
                    </div>
                    <div class="a-stat">
                        <span class="al">Tool Confidence</span>
                        <span class="av success"
                            >{sovereignRouteAgent.stats.deterministic}</span
                        >
                    </div>
                </div>
                <div class="log-area">
                    <div class="l-entry">
                        <div class="l-dot"></div>
                        <p>
                            Verified Geodesic distance for <strong
                                >Shibuya Hub</strong
                            > via Tool 1.
                        </p>
                    </div>
                    <div class="l-entry">
                        <div class="l-dot"></div>
                        <p>
                            Structured Output validated against <code
                                >LogisticsSchema_v4</code
                            >.
                        </p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .route-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(13, 14, 20, 0.9);
        backdrop-filter: blur(20px);
        color: #e2e8f0;
        font-family: "Inter", system-ui, sans-serif;
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
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #10b981, #064e3b);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }
    .accent-icon {
        color: #fff;
    }

    .title-group h3 {
        margin: 0;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    .title-group p {
        margin: 0;
        font-size: 0.7rem;
        color: #64748b;
    }

    .global-metrics {
        display: flex;
        gap: 1.25rem;
    }
    .m-item {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .m-item .l {
        font-size: 0.55rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
    }
    .m-item .v {
        font-size: 0.85rem;
        font-weight: 800;
        color: #10b981;
        font-family: "JetBrains Mono";
    }

    .view-tabs {
        display: flex;
        gap: 1rem;
        padding: 0.5rem 1.25rem;
        background: rgba(0, 0, 0, 0.2);
    }
    .view-tabs button {
        background: none;
        border: none;
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.4rem 0.2rem;
        cursor: pointer;
        position: relative;
    }
    .view-tabs button.active {
        color: #10b981;
    }
    .view-tabs button.active::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #10b981;
        border-radius: 2px;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* ROUTES LIST */
    .routes-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .route-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .route-card:hover {
        border-color: rgba(16, 185, 129, 0.4);
        background: rgba(255, 255, 255, 0.05);
    }
    .route-card.selected {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.05);
    }

    .card-top {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .route-id {
        font-family: "JetBrains Mono";
        font-size: 0.75rem;
        font-weight: 800;
        color: #94a3b8;
    }
    .obj-tag {
        font-size: 0.6rem;
        font-weight: 800;
        background: rgba(0, 0, 0, 0.3);
        padding: 1px 6px;
        border-radius: 4px;
        color: #10b981;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-left: auto;
    }
    .status-dot.optimized {
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    .path-viz {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 0;
    }
    .p-node {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #1e293b;
        border: 2px solid #475569;
    }
    .p-node.final {
        background: #10b981;
        border-color: #10b981;
    }
    .p-line {
        flex: 1;
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
    }

    .card-stats {
        display: flex;
        gap: 1.25rem;
    }
    .c-stat {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 600;
    }

    .expanded-stops {
        margin-top: 0.5rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .stop-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
    }
    .pin-icon {
        color: #f43f5e;
    }
    .stop-info {
        flex: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .s-name {
        font-size: 0.75rem;
        font-weight: 600;
        color: #cbd5e1;
    }
    .s-time {
        font-size: 0.7rem;
        color: #64748b;
        font-family: "JetBrains Mono";
    }
    .delay-tag {
        color: #f59e0b;
        font-size: 0.6rem;
        font-weight: 800;
    }

    .delete-btn {
        margin-top: auto;
        padding-top: 1rem;
        background: none;
        border: none;
        color: #ef4444;
        font-size: 0.7rem;
        font-weight: 700;
        cursor: pointer;
        align-self: flex-end;
        display: flex;
        align-items: center;
        gap: 0.3rem;
        opacity: 0.6;
    }
    .delete-btn:hover {
        opacity: 1;
    }

    /* PLANNER */
    .planner-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    .prompt-box {
        background: rgba(0, 0, 0, 0.3);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
    }
    .prompt-box h4 {
        margin: 0.75rem 0 0.25rem;
        font-size: 0.95rem;
    }
    .prompt-box p {
        font-size: 0.75rem;
        color: #64748b;
        margin: 0;
        line-height: 1.5;
    }
    .muted-icon {
        color: #334155;
    }

    .site-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .s-label {
        font-size: 0.65rem;
        font-weight: 800;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .site-card {
        background: rgba(255, 255, 255, 0.02);
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .plan-btn {
        background: #10b981;
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.9rem;
        font-size: 0.85rem;
        font-weight: 800;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    .plan-btn:disabled {
        background: #334155;
        cursor: wait;
        box-shadow: none;
    }

    /* AUDIT */
    .audit-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    .audit-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #10b981;
    }
    .audit-header h4 {
        margin: 0;
        font-size: 0.9rem;
        text-transform: uppercase;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    .a-stat {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .al {
        font-size: 0.65rem;
        font-weight: 800;
        color: #475569;
    }
    .av {
        font-size: 1.15rem;
        font-weight: 900;
        font-family: "JetBrains Mono";
    }

    .log-area {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .l-entry {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
    }
    .l-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        margin-top: 0.4rem;
        flex-shrink: 0;
    }
    .l-entry p {
        margin: 0;
        font-size: 0.75rem;
        color: #94a3b8;
        line-height: 1.5;
    }
    .l-entry strong {
        color: #f1f5f9;
    }

    .success {
        color: #10b981;
    }
    .spin {
        animation: spin 1.5s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
