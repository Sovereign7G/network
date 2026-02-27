<!--
  ═══════════════════════════════════════════════════════════════════════════════
  🏛️ SOVEREIGN AGENT GATEWAY — OBSERVABILITY PANEL
  ═══════════════════════════════════════════════════════════════════════════════
  The real-time control plane for the AI Agent Gateway.
  Applies: Observability by Default (OpenTelemetry-style traces, metrics, audit)
  
  "Governance is ineffective if evidence arrives after the fact."
  ═══════════════════════════════════════════════════════════════════════════════
-->

<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import {
        agentGateway,

        type AgentGatewayEvent,
        type GatewayJob,
        type GatewayMetrics,
    } from "$lib/services/agent-gateway";
    import { manifold } from "$lib/stores/master-store.svelte";

    // ── Reactive State ──
    let metrics = $state<GatewayMetrics>(agentGateway.metrics);
    let recentEvents = $state<AgentGatewayEvent[]>([]);
    let recentJobs = $state<GatewayJob[]>([]);
    let selectedJob = $state<GatewayJob | null>(null);
    let policyRuleCount = $state(agentGateway.getPolicies().length);
    let isSimulating = $state(false);

    let unsubscribe: (() => void) | null = null;
    let refreshInterval: ReturnType<typeof setInterval> | null = null;

    onMount(() => {
        // Wire gateway context to live manifold state
        agentGateway.setContextResolver(() => ({
            currentResonance: manifold.resonance,
            permissionLevel: manifold.permissionLevel,
            isTurbulence: manifold.turbulence,
            isMoatActive: manifold.isMoatActive,
            timeOfDay: new Date().getHours(),
            dayOfWeek: new Date().getDay(),
            activeJobCount: agentGateway.metrics.activeJobs,
        }));

        // Subscribe to live events
        unsubscribe = agentGateway.subscribe((event) => {
            recentEvents = [event, ...recentEvents].slice(0, 50);
            refreshData();
        });

        // Periodic refresh
        refreshInterval = setInterval(refreshData, 2000);
        refreshData();
    });

    onDestroy(() => {
        unsubscribe?.();
        if (refreshInterval) clearInterval(refreshInterval);
    });

    function refreshData() {
        metrics = agentGateway.metrics;
        recentJobs = agentGateway.getRecentJobs(15);
        policyRuleCount = agentGateway.getPolicies().length;
    }

    // ── Simulation: Send test requests to the gateway ──
    async function simulateAgentBurst() {
        if (isSimulating) return;
        isSimulating = true;

        const capabilities = [
            "oracle:fetch",
            "zk:verify",
            "vault:rebalance",
            "governance:vote",
            "llm:query",
            "stable:repeg",
            "mesh:stress_drill",
        ] as const;

        const trusts = ["REGISTERED", "VERIFIED", "SOVEREIGN"] as const;

        for (let i = 0; i < 8; i++) {
            const cap =
                capabilities[Math.floor(Math.random() * capabilities.length)];
            const trust = trusts[Math.floor(Math.random() * trusts.length)];

            const request = agentGateway.buildRequest(
                cap,
                { id: `agent-sim-${i}`, trust, provider: "simulation" },
                { round: i },
            );

            await agentGateway.submitRequest(request);
            await new Promise((r) => setTimeout(r, 100));
        }

        isSimulating = false;
    }

    async function simulateDenial() {
        // Send a request that will be denied (UNTRUSTED trying HIGH-tier action)
        const request = agentGateway.buildRequest(
            "kernel:hard_reset",
            { id: "rogue-agent", trust: "UNTRUSTED", provider: "adversary" },
            { reason: "test" },
        );
        await agentGateway.submitRequest(request);
    }

    async function simulateTurbulenceLockdown() {
        manifold.turbulence = true;
        manifold.status = "DEGRADED";

        const request = agentGateway.buildRequest(
            "vault:rebalance",
            { id: "regular-agent", trust: "REGISTERED", provider: "test" },
            {},
        );
        await agentGateway.submitRequest(request);

        setTimeout(() => {
            manifold.turbulence = false;
            manifold.status = "COHERENT";
        }, 3000);
    }

    function selectJob(job: GatewayJob) {
        selectedJob = selectedJob?.jobId === job.jobId ? null : job;
    }

    function getStatusColor(status: string): string {
        switch (status) {
            case "COMPLETED":
                return "var(--color-emerald)";
            case "FAILED":
            case "POLICY_DENIED":
                return "var(--color-crimson)";
            case "EXECUTING":
                return "var(--color-amber)";
            case "QUEUED":
                return "var(--color-cyan)";
            default:
                return "var(--color-slate)";
        }
    }

    function getEventIcon(type: string): string {
        const iconMap: Record<string, string> = {
            REQUEST_RECEIVED: "📨",
            POLICY_EVALUATED: "✅",
            POLICY_DENIED: "🛑",
            JOB_QUEUED: "📋",
            SANDBOX_CREATED: "🏗️",
            EXECUTION_STARTED: "⚡",
            EXECUTION_COMPLETED: "✨",
            EXECUTION_FAILED: "💥",
            SANDBOX_DESTROYED: "🧹",
            APPROVAL_REQUIRED: "🔐",
            SLO_VIOLATION: "⚠️",
        };
        return iconMap[type] || "📌";
    }

    function formatMs(ms: number): string {
        return ms < 1 ? "<1ms" : `${Math.round(ms)}ms`;
    }
</script>

<div class="gateway-panel">
    <!-- ═══ HEADER ═══ -->
    <header class="gateway-header">
        <div class="header-left">
            <div class="gateway-icon">🏛️</div>
            <div>
                <h2>Sovereign Agent Gateway</h2>
                <p class="subtitle">Least-Privilege AI Control Plane</p>
            </div>
        </div>
        <div class="header-badges">
            <span class="badge badge-policies">{policyRuleCount} Policies</span>
            <span class="badge badge-capabilities">22 Capabilities</span>
            <span
                class="badge"
                class:badge-healthy={metrics.denialRate < 0.02}
                class:badge-warn={metrics.denialRate >= 0.02}
            >
                {(metrics.denialRate * 100).toFixed(1)}% Denial Rate
            </span>
        </div>
    </header>

    <!-- ═══ METRICS GRID ═══ -->
    <section class="metrics-grid">
        <div class="metric-card">
            <span class="metric-label">Total Requests</span>
            <span class="metric-value">{metrics.totalRequests}</span>
        </div>
        <div class="metric-card metric-approved">
            <span class="metric-label">Approved</span>
            <span class="metric-value">{metrics.totalApproved}</span>
        </div>
        <div class="metric-card metric-denied">
            <span class="metric-label">Denied</span>
            <span class="metric-value">{metrics.totalDenied}</span>
        </div>
        <div class="metric-card metric-executed">
            <span class="metric-label">Executed</span>
            <span class="metric-value">{metrics.totalExecuted}</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Policy Latency</span>
            <span
                class="metric-value slo"
                class:slo-ok={metrics.avgPolicyLatencyMs < 100}
                class:slo-warn={metrics.avgPolicyLatencyMs >= 100}
            >
                {formatMs(metrics.avgPolicyLatencyMs)}
            </span>
            <span class="slo-target">SLO: &lt;100ms</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Exec Latency</span>
            <span class="metric-value"
                >{formatMs(metrics.avgExecutionLatencyMs)}</span
            >
        </div>
        <div class="metric-card">
            <span class="metric-label">Sandboxes</span>
            <span class="metric-value"
                >{metrics.sandboxesCreated} / {metrics.sandboxesDestroyed}</span
            >
            <span class="slo-target">Created / Destroyed</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Active Jobs</span>
            <span class="metric-value">{metrics.activeJobs}</span>
        </div>
    </section>

    <!-- ═══ SIMULATION CONTROLS ═══ -->
    <section class="sim-controls">
        <h3>🧪 Stress Lab</h3>
        <div class="sim-buttons">
            <button
                class="sim-btn sim-btn-primary"
                onclick={simulateAgentBurst}
                disabled={isSimulating}
            >
                {isSimulating
                    ? "⏳ Simulating..."
                    : "🚀 Agent Burst (8 requests)"}
            </button>
            <button class="sim-btn sim-btn-danger" onclick={simulateDenial}>
                🛑 Test Denial (Rogue Agent)
            </button>
            <button
                class="sim-btn sim-btn-warn"
                onclick={simulateTurbulenceLockdown}
            >
                🌪️ Turbulence Lockdown
            </button>
        </div>
    </section>

    <!-- ═══ SPLIT PANEL: JOBS + EVENTS ═══ -->
    <div class="split-panel">
        <!-- JOBS -->
        <section class="jobs-panel">
            <h3>📋 Recent Jobs</h3>
            <div class="jobs-list">
                {#each recentJobs as job (job.jobId)}
                    <button
                        class="job-row"
                        class:selected={selectedJob?.jobId === job.jobId}
                        onclick={() => selectJob(job)}
                    >
                        <span
                            class="job-status"
                            style="background: {getStatusColor(job.status)};"
                        ></span>
                        <span class="job-cap">{job.request.capability}</span>
                        <span class="job-actor">{job.request.actor.id}</span>
                        <span class="job-status-text">{job.status}</span>
                    </button>
                {/each}
                {#if recentJobs.length === 0}
                    <div class="empty-state">
                        No jobs yet. Run a simulation above.
                    </div>
                {/if}
            </div>
        </section>

        <!-- LIVE AUDIT LOG -->
        <section class="events-panel">
            <h3>📡 Live Audit Feed</h3>
            <div class="events-list">
                {#each recentEvents as event (event.eventId)}
                    <div
                        class="event-row"
                        class:event-deny={event.type === "POLICY_DENIED"}
                        class:event-slo={event.type === "SLO_VIOLATION"}
                    >
                        <span class="event-icon"
                            >{getEventIcon(event.type)}</span
                        >
                        <span class="event-type">{event.type}</span>
                        <span class="event-time"
                            >{new Date(
                                event.timestamp,
                            ).toLocaleTimeString()}</span
                        >
                    </div>
                {/each}
                {#if recentEvents.length === 0}
                    <div class="empty-state">Waiting for gateway events...</div>
                {/if}
            </div>
        </section>
    </div>

    <!-- ═══ JOB DETAIL / TRACE INSPECTOR ═══ -->
    {#if selectedJob}
        <section class="trace-inspector">
            <h3>🔬 Trace Inspector — {selectedJob.request.capability}</h3>
            <div class="trace-meta">
                <div>
                    <strong>Job ID:</strong> <code>{selectedJob.jobId}</code>
                </div>
                <div>
                    <strong>Actor:</strong>
                    {selectedJob.request.actor.id} ({selectedJob.request.actor
                        .trust})
                </div>
                <div>
                    <strong>Plan Hash:</strong>
                    <code>{selectedJob.request.planHash}</code>
                </div>
                <div>
                    <strong>Status:</strong>
                    <span style="color: {getStatusColor(selectedJob.status)}"
                        >{selectedJob.status}</span
                    >
                </div>
                <div>
                    <strong>Risk Tier:</strong>
                    {selectedJob.policy.riskTier}
                </div>
            </div>

            <h4>Policy Decision</h4>
            <div class="policy-rules">
                {#each selectedJob.policy.appliedRules as rule}
                    <div
                        class="rule-line"
                        class:rule-pass={rule.includes("✓")}
                        class:rule-fail={rule.includes("✗")}
                    >
                        {rule}
                    </div>
                {/each}
            </div>

            <h4>Trace Spans</h4>
            <div class="trace-spans">
                {#each selectedJob.trace as span}
                    <div class="span-row">
                        <span class="span-name">{span.name}</span>
                        <span class="span-dur">
                            {span.endTime
                                ? formatMs(span.endTime - span.startTime)
                                : "⏳"}
                        </span>
                        <span
                            class="span-status"
                            class:span-ok={span.status === "OK"}
                            class:span-error={span.status === "ERROR"}
                        >
                            {span.status}
                        </span>
                    </div>
                {/each}
            </div>

            {#if selectedJob.result}
                <h4>Result</h4>
                <pre class="result-json">{JSON.stringify(
                        selectedJob.result,
                        null,
                        2,
                    )}</pre>
            {/if}

            {#if selectedJob.error}
                <h4>Error</h4>
                <pre class="result-json error-json">{selectedJob.error}</pre>
            {/if}
        </section>
    {/if}
</div>

<style>
    /* ═══ DESIGN TOKENS ═══ */
    :root {
        --gw-bg: rgba(10, 12, 20, 0.95);
        --gw-card-bg: rgba(20, 24, 38, 0.85);
        --gw-border: rgba(100, 120, 180, 0.15);
        --gw-text: #e0e4ef;
        --gw-text-dim: #8892a8;
        --gw-accent: #6366f1;
        --color-emerald: #10b981;
        --color-crimson: #ef4444;
        --color-amber: #f59e0b;
        --color-cyan: #22d3ee;
        --color-slate: #64748b;
    }

    .gateway-panel {
        background: var(--gw-bg);
        border: 1px solid var(--gw-border);
        border-radius: 16px;
        padding: 24px;
        color: var(--gw-text);
        font-family: "Inter", system-ui, sans-serif;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    /* ═══ HEADER ═══ */
    .gateway-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--gw-border);
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .gateway-icon {
        font-size: 32px;
        filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.4));
    }
    .gateway-header h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        margin: 2px 0 0;
        font-size: 12px;
        color: var(--gw-text-dim);
    }
    .header-badges {
        display: flex;
        gap: 8px;
    }
    .badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .badge-policies {
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border-color: rgba(16, 185, 129, 0.2);
    }
    .badge-capabilities {
        background: rgba(34, 211, 238, 0.15);
        color: #67e8f9;
        border-color: rgba(34, 211, 238, 0.2);
    }
    .badge-healthy {
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border-color: rgba(16, 185, 129, 0.2);
    }
    .badge-warn {
        background: rgba(239, 68, 68, 0.15);
        color: #fca5a5;
        border-color: rgba(239, 68, 68, 0.2);
    }

    /* ═══ METRICS GRID ═══ */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
    }
    .metric-card {
        background: var(--gw-card-bg);
        border: 1px solid var(--gw-border);
        border-radius: 12px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: var(--gw-accent);
    }
    .metric-label {
        font-size: 11px;
        color: var(--gw-text-dim);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
    }
    .metric-approved .metric-value {
        color: var(--color-emerald);
    }
    .metric-denied .metric-value {
        color: var(--color-crimson);
    }
    .metric-executed .metric-value {
        color: var(--color-cyan);
    }
    .slo-ok {
        color: var(--color-emerald) !important;
    }
    .slo-warn {
        color: var(--color-crimson) !important;
    }
    .slo-target {
        font-size: 10px;
        color: var(--gw-text-dim);
    }

    /* ═══ SIM CONTROLS ═══ */
    .sim-controls h3 {
        margin: 0 0 10px;
        font-size: 14px;
        font-weight: 600;
    }
    .sim-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .sim-btn {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        color: white;
    }
    .sim-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .sim-btn-primary {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .sim-btn-primary:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .sim-btn-danger {
        background: linear-gradient(135deg, #dc2626, #ef4444);
        border-color: rgba(239, 68, 68, 0.4);
    }
    .sim-btn-danger:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    .sim-btn-warn {
        background: linear-gradient(135deg, #d97706, #f59e0b);
        border-color: rgba(245, 158, 11, 0.4);
    }
    .sim-btn-warn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }

    /* ═══ SPLIT PANEL ═══ */
    .split-panel {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    .jobs-panel,
    .events-panel {
        background: var(--gw-card-bg);
        border: 1px solid var(--gw-border);
        border-radius: 12px;
        padding: 14px;
    }
    .jobs-panel h3,
    .events-panel h3 {
        margin: 0 0 10px;
        font-size: 14px;
        font-weight: 600;
    }
    .jobs-list,
    .events-list {
        max-height: 280px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    /* ═══ JOB ROW ═══ */
    .job-row {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.15s ease;
        font-size: 12px;
        color: var(--gw-text);
        width: 100%;
        text-align: left;
    }
    .job-row:hover {
        background: rgba(99, 102, 241, 0.08);
        border-color: rgba(99, 102, 241, 0.2);
    }
    .job-row.selected {
        background: rgba(99, 102, 241, 0.15);
        border-color: var(--gw-accent);
    }
    .job-status {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .job-cap {
        font-weight: 600;
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        color: var(--color-cyan);
        flex: 1;
    }
    .job-actor {
        color: var(--gw-text-dim);
        font-size: 10px;
    }
    .job-status-text {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* ═══ EVENTS ═══ */
    .event-row {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        transition: background 0.15s ease;
    }
    .event-row:hover {
        background: rgba(255, 255, 255, 0.04);
    }
    .event-deny {
        background: rgba(239, 68, 68, 0.08);
    }
    .event-slo {
        background: rgba(245, 158, 11, 0.08);
    }
    .event-icon {
        font-size: 14px;
        flex-shrink: 0;
    }
    .event-type {
        font-weight: 600;
        font-family: "JetBrains Mono", monospace;
        font-size: 10px;
        flex: 1;
    }
    .event-time {
        color: var(--gw-text-dim);
        font-size: 10px;
    }

    .empty-state {
        padding: 24px;
        text-align: center;
        color: var(--gw-text-dim);
        font-size: 13px;
    }

    /* ═══ TRACE INSPECTOR ═══ */
    .trace-inspector {
        background: var(--gw-card-bg);
        border: 1px solid var(--gw-accent);
        border-radius: 12px;
        padding: 16px;
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .trace-inspector h3 {
        margin: 0 0 12px;
        font-size: 15px;
        font-weight: 700;
        color: var(--gw-accent);
    }
    .trace-inspector h4 {
        margin: 14px 0 6px;
        font-size: 12px;
        font-weight: 600;
        color: var(--gw-text-dim);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .trace-meta {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        font-size: 12px;
    }
    .trace-meta code {
        background: rgba(99, 102, 241, 0.15);
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 10px;
    }

    /* ═══ POLICY RULES ═══ */
    .policy-rules {
        display: flex;
        flex-direction: column;
        gap: 3px;
        max-height: 150px;
        overflow-y: auto;
    }
    .rule-line {
        font-size: 11px;
        font-family: "JetBrains Mono", monospace;
        padding: 3px 8px;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.02);
    }
    .rule-pass {
        color: var(--color-emerald);
    }
    .rule-fail {
        color: var(--color-crimson);
        background: rgba(239, 68, 68, 0.06);
    }

    /* ═══ TRACE SPANS ═══ */
    .trace-spans {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .span-row {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.03);
    }
    .span-name {
        font-weight: 600;
        flex: 1;
    }
    .span-dur {
        color: var(--gw-text-dim);
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
    }
    .span-status {
        font-size: 10px;
        font-weight: 700;
    }
    .span-ok {
        color: var(--color-emerald);
    }
    .span-error {
        color: var(--color-crimson);
    }

    /* ═══ RESULT JSON ═══ */
    .result-json {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid var(--gw-border);
        border-radius: 8px;
        padding: 10px 12px;
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        color: var(--color-cyan);
        overflow-x: auto;
        max-height: 180px;
        overflow-y: auto;
    }
    .error-json {
        color: var(--color-crimson);
    }

    /* ═══ SCROLLBARS ═══ */
    .jobs-list::-webkit-scrollbar,
    .events-list::-webkit-scrollbar,
    .policy-rules::-webkit-scrollbar,
    .result-json::-webkit-scrollbar {
        width: 4px;
    }
    .jobs-list::-webkit-scrollbar-thumb,
    .events-list::-webkit-scrollbar-thumb,
    .policy-rules::-webkit-scrollbar-thumb,
    .result-json::-webkit-scrollbar-thumb {
        background: var(--gw-accent);
        border-radius: 4px;
    }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 768px) {
        .gateway-header {
            flex-direction: column;
            gap: 10px;
        }
        .header-badges {
            flex-wrap: wrap;
        }
        .split-panel {
            grid-template-columns: 1fr;
        }
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .trace-meta {
            grid-template-columns: 1fr;
        }
    }
</style>
