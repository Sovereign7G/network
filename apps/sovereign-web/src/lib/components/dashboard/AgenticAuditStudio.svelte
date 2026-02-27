<script lang="ts">
    import { agentGateway } from "$lib/services/agent-gateway";
    import { auditEngine } from "$lib/services/audit-engine.svelte";
    import { fade, slide } from "svelte/transition";
    import { onMount } from "svelte";

    let logs = $state(agentGateway.getAuditLog());
    let lastAudit = $derived(auditEngine.lastAudit);
    let selectedJobId = $state<string | null>(null);
    let selectedJob = $derived(
        logs.find(
            (l) =>
                l.payload.jobId === selectedJobId ||
                l.payload.requestId === selectedJobId,
        ),
    );

    onMount(() => {
        const unsubscribe = agentGateway.subscribe((event) => {
            logs = [event, ...logs].slice(0, 100);
        });
        return unsubscribe;
    });

    function getEventColor(type: string) {
        if (type.includes("DENIED") || type.includes("FAILED"))
            return "text-rose-400";
        if (type.includes("COMPLETED") || type.includes("APPROVED"))
            return "text-emerald-400";
        if (type.includes("QUEUED")) return "text-cyan-400";
        return "text-slate-400";
    }
</script>

<div class="audit-studio">
    <header class="studio-header">
        <div class="title-wrap">
            <h1>Agentic Audit Studio</h1>
            <span class="version">v1.2.0 — METABOLIC_RESONANCE_V3</span>
        </div>
        <div class="metrics">
            <div class="metric">
                <span class="label">ANOMALIES</span>
                <span class="value" class:urgent={auditEngine.anomalies > 0}
                    >{auditEngine.anomalies}</span
                >
            </div>
            <div class="metric">
                <span class="label">APPROVAL_RATE</span>
                <span class="value"
                    >{((1 - agentGateway.metrics.denialRate) * 100).toFixed(
                        1,
                    )}%</span
                >
            </div>
        </div>
    </header>

    <div class="studio-content">
        <!-- Live Audit Trail (Sidebar style) -->
        <aside class="audit-trail">
            <div class="trail-header">
                <h2>LIVE AUDIT TRAIL</h2>
                <div class="live-blink"></div>
            </div>
            <div class="trail-list">
                {#each logs as event (event.eventId)}
                    <button
                        class="trail-item"
                        class:active={selectedJobId ===
                            (event.payload.jobId || event.payload.requestId)}
                        onclick={() =>
                            (selectedJobId =
                                (event.payload.jobId as string) ||
                                (event.payload.requestId as string))}
                        in:slide
                    >
                        <span class="timestamp"
                            >{new Date(event.timestamp).toLocaleTimeString([], {
                                hour12: false,
                                hour: "2-digit",
                                minute: "2-digit",
                                second: "2-digit",
                            })}</span
                        >
                        <span class="type {getEventColor(event.type)}"
                            >{event.type.replace("_", " ")}</span
                        >
                        <span class="payload-brief"
                            >{event.payload.capability ||
                                event.payload.requestId
                                    ?.toString()
                                    .slice(0, 8)}</span
                        >
                    </button>
                {/each}
            </div>
        </aside>

        <!-- Reasoning & Policy Canvas -->
        <main class="reasoning-canvas">
            {#if lastAudit}
                <section class="audit-summary-card" in:fade>
                    <div class="card-header">
                        <div class="status-indicator">
                            <span
                                class="status-pill status-{lastAudit.status.toLowerCase()}"
                                >{lastAudit.status}</span
                            >
                            <span class="score"
                                >RES_SCORE: {lastAudit.score}/100</span
                            >
                        </div>
                        <h3>METABOLIC AUDITIONING REPORT</h3>
                    </div>

                    <div class="recommendation">
                        <p>{lastAudit.recommendation}</p>
                    </div>

                    <div class="trace-view">
                        <h4>REASONING_TRACE</h4>
                        <div class="trace-lines">
                            {#each lastAudit.reasoningTrace as line, i}
                                <div
                                    class="trace-line"
                                    in:fade={{ delay: i * 50 }}
                                >
                                    <span class="line-num"
                                        >{i.toString().padStart(2, "0")}</span
                                    >
                                    <span class="line-content">{line}</span>
                                </div>
                            {/each}
                        </div>
                    </div>

                    {#if lastAudit.risks.length > 0}
                        <div class="risks-view">
                            <h4>DETECTED_RISKS</h4>
                            <div class="risk-pills">
                                {#each lastAudit.risks as risk}
                                    <span class="risk-pill">{risk}</span>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </section>
            {:else}
                <div class="empty-state">
                    <p>NO ACTIVE AUDIT DETECTED</p>
                    <span>Waiting for agentic intervention...</span>
                </div>
            {/if}

            {#if selectedJob}
                <section class="job-detail-card" in:slide>
                    <div class="card-header">
                        <h3>JOB_DETAIL: {selectedJobId?.slice(0, 13)}</h3>
                    </div>
                    <pre class="json-view">{JSON.stringify(
                            selectedJob.payload,
                            null,
                            2,
                        )}</pre>
                </section>
            {/if}
        </main>
    </div>
</div>

<style>
    .audit-studio {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: #0f1115;
        color: #e2e8f0;
        font-family: "Inter", system-ui, sans-serif;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
    }

    .studio-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 2rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .title-wrap h1 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .version {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.7rem;
        color: #64748b;
    }

    .metrics {
        display: flex;
        gap: 2rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .metric .label {
        font-size: 0.65rem;
        color: #64748b;
        font-weight: 700;
    }

    .metric .value {
        font-family: "JetBrains Mono", monospace;
        font-size: 1.1rem;
        font-weight: 500;
        color: #00ffcc;
    }

    .metric .value.urgent {
        color: #fb7185;
        text-shadow: 0 0 10px rgba(251, 113, 133, 0.3);
    }

    .studio-content {
        display: grid;
        grid-template-columns: 320px 1fr;
        flex: 1;
        overflow: hidden;
    }

    .audit-trail {
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        background: rgba(0, 0, 0, 0.2);
    }

    .trail-header {
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .trail-header h2 {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        margin: 0;
    }

    .live-blink {
        width: 6px;
        height: 6px;
        background: #00ffcc;
        border-radius: 50%;
        box-shadow: 0 0 8px #00ffcc;
        animation: pulse 1.5s infinite;
    }

    .trail-list {
        flex: 1;
        overflow-y: auto;
    }

    .trail-item {
        width: 100%;
        display: grid;
        grid-template-columns: 80px 120px 1fr;
        padding: 0.85rem 1.5rem;
        text-align: left;
        border: none;
        background: transparent;
        cursor: pointer;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.02);
        transition: background 0.2s;
    }

    .trail-item:hover {
        background: rgba(255, 255, 255, 0.03);
    }

    .trail-item.active {
        background: rgba(0, 255, 204, 0.05);
        color: #00ffcc;
    }

    .timestamp {
        color: #475569;
    }
    .payload-brief {
        color: #94a3b8;
        text-align: right;
    }

    .reasoning-canvas {
        padding: 2rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        background: radial-gradient(
            circle at top right,
            rgba(0, 255, 204, 0.03),
            transparent 40%
        );
    }

    .audit-summary-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
    }

    .card-header {
        display: flex;
        flex-direction: row-reverse;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .card-header h3 {
        margin: 0;
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748b;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .status-pill {
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .status-healthy {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid #10b981;
    }
    .status-dissonant {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid #f59e0b;
    }
    .status-amputation_risk {
        background: rgba(225, 29, 72, 0.1);
        color: #e11d48;
        border: 1px solid #e11d48;
    }

    .score {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .recommendation {
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #64748b;
        margin-bottom: 2rem;
    }

    .recommendation p {
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .trace-view h4,
    .risks-view h4 {
        font-size: 0.7rem;
        font-weight: 800;
        color: #475569;
        margin-bottom: 0.75rem;
        letter-spacing: 0.05em;
    }

    .trace-lines {
        background: #000;
        padding: 1rem;
        border-radius: 8px;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.8rem;
    }

    .trace-line {
        display: flex;
        gap: 1rem;
        line-height: 1.6;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 0.25rem 0;
    }

    .line-num {
        color: #334155;
        user-select: none;
    }
    .line-content {
        color: #94a3b8;
    }

    .risk-pills {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .risk-pill {
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        padding: 0.2rem 0.5rem;
        font-size: 0.65rem;
        font-weight: 600;
        border-radius: 4px;
        border: 1px solid rgba(244, 63, 94, 0.2);
    }

    .job-detail-card {
        background: #08090a;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
    }

    .json-view {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.75rem;
        color: #8b5cf6;
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 8px;
        max-height: 300px;
        overflow-y: auto;
    }

    .empty-state {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #475569;
    }

    .empty-state p {
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .empty-state span {
        font-size: 0.8rem;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
    }
</style>
