<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 📜 SOVEREIGN SDD: SPEC-DRIVEN DEVELOPMENT PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // Visualizing Executable Architecture and continuous intent validation.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, slide } from "svelte/transition";
    import {
        FileCheck,
        AlertTriangle,
        CheckCircle2,
        GitBranch,
        Search,
        Plus,
        Activity,
        Code2,
        ShieldCheck,
        RefreshCw,
        History,
    } from "lucide-svelte";
    import {
        sovereignSDD,

        type SovereignSpec,
    } from "$lib/services/sdd-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let view = $state<"registry" | "editor" | "validation">("registry");
    let selectedSpecId = $state<string | null>(null);
    let validationProgress = $state(0);
    let isValidating = $state(false);

    const selectedSpec = $derived(
        sovereignSDD.allSpecs.find(
            (s: SovereignSpec) => s.id === selectedSpecId,
        ),
    );

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    async function triggerValidation() {
        if (!selectedSpecId) return;
        isValidating = true;
        validationProgress = 0;

        const interval = setInterval(() => {
            validationProgress += 10;
            if (validationProgress >= 100) {
                clearInterval(interval);
                sovereignSDD.validateSpec(selectedSpecId!);
                isValidating = false;
            }
        }, 150);
    }
</script>

<div class="sdd-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <FileCheck size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Sovereign SDD</h3>
                <p>Intent-First Executable Architecture</p>
            </div>
        </div>
        <div class="global-metrics">
            <div class="m-item">
                <span class="l">COVERAGE</span>
                <span class="v">{sovereignSDD.stats.coverage}</span>
            </div>
            <div class="m-item">
                <span class="l">DRIFT</span>
                <span class="v warning"
                    >{sovereignSDD.stats.drift} DETECTED</span
                >
            </div>
        </div>
    </header>

    <!-- 🎚️ VIEW CONTROLS -->
    <div class="view-tabs">
        <button
            class:active={view === "registry"}
            onclick={() => (view = "registry")}>Registry</button
        >
        <button
            class:active={view === "editor"}
            onclick={() => (view = "editor")}>Spec Editor</button
        >
        <button
            class:active={view === "validation"}
            onclick={() => (view = "validation")}>Integrity</button
        >
    </div>

    <!-- 📄 REGISTRY VIEW -->
    <div class="content-scroll">
        {#if view === "registry"}
            <div class="registry-view" in:fade>
                <div class="search-bar">
                    <Search size={14} />
                    <input placeholder="Filter specifications..." />
                    <button class="create-btn">
                        <Plus size={14} /> <span>New Spec</span>
                    </button>
                </div>

                <div class="spec-list">
                    {#each sovereignSDD.allSpecs as spec, i (spec.id)}
                        <div
                            class="spec-card"
                            role="button"
                            tabindex="0"
                            class:selected={selectedSpecId === spec.id}
                            class:drift={spec.driftDetected}
                            in:fly={{ x: -20, delay: i * 50 }}
                            onclick={() => (selectedSpecId = spec.id)}
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" && (selectedSpecId = spec.id)}
                        >
                            <div class="card-top">
                                <Code2 size={14} class="type-icon" />
                                <span class="spec-type">{spec.type}</span>
                                <span class="status-tag {spec.status}"
                                    >{spec.status.replace("_", " ")}</span
                                >
                            </div>
                            <h5>{spec.name}</h5>
                            <div class="card-meta">
                                <span>v{spec.version}</span>
                                <span class="divider">•</span>
                                <span>{spec.author}</span>
                            </div>

                            {#if spec.driftDetected}
                                <div class="drift-alert" transition:slide>
                                    <AlertTriangle size={12} />
                                    <span>Architectural Drift Detected</span>
                                </div>
                            {/if}

                            {#if selectedSpecId === spec.id}
                                <div class="expanded-info" transition:slide>
                                    <div class="metric-row">
                                        <div class="mini-m">
                                            <span class="ml"
                                                >Last Validated</span
                                            >
                                            <span class="mv"
                                                >{new Date(
                                                    spec.lastValidated,
                                                ).toLocaleTimeString()}</span
                                            >
                                        </div>
                                        <button
                                            class="validate-btn"
                                            onclick={(e: MouseEvent) => {
                                                e.stopPropagation();
                                                triggerValidation();
                                            }}
                                            disabled={isValidating}
                                        >
                                            {#if isValidating}
                                                <RefreshCw
                                                    size={12}
                                                    class="spin"
                                                />
                                            {:else}
                                                <ShieldCheck size={12} />
                                            {/if}
                                            Validate
                                        </button>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {:else if view === "editor"}
            <div class="editor-view" in:fade>
                {#if selectedSpec}
                    <div class="editor-header">
                        <div class="e-info">
                            <h4>{selectedSpec.name}</h4>
                            <span>{selectedSpec.id}</span>
                        </div>
                        <div class="e-actions">
                            <button class="e-btn"
                                ><GitBranch size={14} /> Fork</button
                            >
                            <button class="e-btn primary">Save Patch</button>
                        </div>
                    </div>
                    <div class="code-area">
                        <pre><code>{selectedSpec.content}</code></pre>
                    </div>
                {:else}
                    <div class="empty-state">
                        <Code2 size={48} class="muted" />
                        <p>Select a specification to view intent</p>
                    </div>
                {/if}
            </div>
        {:else if view === "validation"}
            <div class="validation-view" in:fade>
                <div class="integrity-header">
                    <Activity size={18} />
                    <h4>System Integrity Analysis</h4>
                </div>

                <div class="metrics-grid">
                    <div class="stat-box">
                        <span class="label">Pass Rate</span>
                        <span class="value success"
                            >{sovereignSDD.stats.passRate}</span
                        >
                    </div>
                    <div class="stat-box">
                        <span class="label">Agent Confidence</span>
                        <span class="value"
                            >{sovereignSDD.metrics.agentConfidenceScore}%</span
                        >
                    </div>
                </div>

                <div class="activity-log">
                    <div class="log-head">
                        <History size={14} />
                        <span>Recent Enforcement Events</span>
                    </div>
                    <div class="log-item">
                        <CheckCircle2 size={12} class="success" />
                        <span class="log-msg"
                            >Applied OpenAPI constraints to OpenCode Gateway</span
                        >
                        <span class="log-time">2m ago</span>
                    </div>
                    <div class="log-item">
                        <AlertTriangle size={12} class="warning" />
                        <span class="log-msg"
                            >Draft v2.0 of Kernel Spec deviates from current
                            impl</span
                        >
                        <span class="log-time">15m ago</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .sdd-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(13, 15, 23, 0.8);
        backdrop-filter: blur(25px);
        color: #f1f5f9;
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
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
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
        gap: 1.5rem;
    }

    .m-item {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .m-item .l {
        font-size: 0.6rem;
        font-weight: 700;
        color: #475569;
    }
    .m-item .v {
        font-size: 0.9rem;
        font-weight: 800;
        font-family: "JetBrains Mono";
    }
    .v.warning {
        color: #f59e0b;
    }

    .view-tabs {
        padding: 0.5rem 1.25rem;
        display: flex;
        gap: 1rem;
        background: rgba(255, 255, 255, 0.02);
    }

    .view-tabs button {
        background: none;
        border: none;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.4rem 0.2rem;
        cursor: pointer;
        position: relative;
    }

    .view-tabs button.active {
        color: #3b82f6;
    }

    .view-tabs button.active::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #3b82f6;
        border-radius: 2px;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* REGISTRY */
    .search-bar {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.6rem 0.8rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
    }

    .search-bar input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 0.8rem;
        outline: none;
    }

    .create-btn {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
    }

    .spec-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .spec-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .spec-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        background: rgba(255, 255, 255, 0.05);
    }
    .spec-card.selected {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.05);
    }
    .spec-card.drift {
        border-left: 3px solid #f59e0b;
    }

    .card-top {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .spec-type {
        font-size: 0.65rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
    }
    .status-tag {
        font-size: 0.6rem;
        padding: 1px 6px;
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
    }
    .status-tag.published {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    .status-tag.under_review {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
    }
    .status-tag.draft {
        background: rgba(148, 163, 184, 0.1);
        color: #94a3b8;
    }

    .spec-card h5 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .card-meta {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.7rem;
        color: #475569;
    }

    .drift-alert {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        padding: 0.4rem 0.6rem;
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .expanded-info {
        margin-top: 0.5rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .mini-m {
        display: flex;
        flex-direction: column;
    }
    .ml {
        font-size: 0.6rem;
        color: #475569;
        font-weight: 600;
    }
    .mv {
        font-size: 0.7rem;
        color: #94a3b8;
        font-family: "JetBrains Mono";
    }

    .validate-btn {
        background: #3b82f6;
        border: none;
        color: white;
        padding: 0.4rem 0.75rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
    }

    .validate-btn:disabled {
        opacity: 0.5;
        cursor: wait;
    }

    /* EDITOR */
    .editor-view {
        display: flex;
        flex-direction: column;
        height: 100%;
        gap: 1rem;
    }
    .editor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .e-info h4 {
        margin: 0;
        font-size: 1rem;
    }
    .e-info span {
        font-size: 0.65rem;
        color: #475569;
        font-family: "JetBrains Mono";
    }
    .e-actions {
        display: flex;
        gap: 0.5rem;
    }
    .e-btn {
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .e-btn.primary {
        background: #3b82f6;
        border-color: #2563eb;
    }

    .code-area {
        flex: 1;
        background: #000;
        border-radius: 12px;
        padding: 1rem;
        overflow: auto;
    }
    .code-area code {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.8rem;
        color: #38bdf8;
        line-height: 1.5;
    }

    /* VALIDATION */
    .validation-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    .integrity-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #3b82f6;
    }
    .integrity-header h4 {
        margin: 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    .stat-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .stat-box .label {
        font-size: 0.65rem;
        color: #64748b;
        font-weight: 700;
    }
    .stat-box .value {
        font-size: 1.25rem;
        font-weight: 800;
        font-family: "JetBrains Mono";
    }
    .value.success {
        color: #10b981;
    }

    .activity-log {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .log-head {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.7rem;
        font-weight: 800;
        color: #475569;
    }
    .log-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.75rem;
        border-radius: 8px;
    }
    .log-msg {
        flex: 1;
        font-size: 0.75rem;
        line-height: 1.4;
        color: #cbd5e1;
    }
    .log-time {
        font-size: 0.6rem;
        color: #475569;
    }

    .success {
        color: #10b981;
    }
    .warning {
        color: #f59e0b;
    }
    .spin {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
        color: #334155;
    }
    .empty-state p {
        margin-top: 1rem;
        font-size: 0.85rem;
    }

    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
