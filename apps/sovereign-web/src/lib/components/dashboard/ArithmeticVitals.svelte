<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { fade, fly } from "svelte/transition";
    // level 5 library integration
    import { ArithmeticAuditor } from "../../../../../../packages/age-forensics/src/index";
    import type { AuditReport } from "../../../../../../packages/age-types/src/sovereign-types";

    // State
    let audit: AuditReport | null = null;
    let interval: any;
    const auditor = new ArithmeticAuditor();

    async function updateVitals() {
        audit = await auditor.runFullAudit();
    }

    onMount(async () => {
        await updateVitals();
        interval = setInterval(updateVitals, 5000); // 5s cadence
    });

    onDestroy(() => {
        if (interval) clearInterval(interval);
    });

    $: isYellowAlert = (audit?.findings.sofr.current || 0) > 3.75;
    $: isSystemicBreach = (audit?.integrity || 1) < 0.38;
    $: riskLevel = isSystemicBreach
        ? "CRITICAL"
        : isYellowAlert
          ? "WARNING"
          : "STABLE";

    const THRESHOLDS = {
        SOFR: 3.8,
        GILT: 161,
        OAT: 57,
    };
</script>

<div
    class="vitals-card {riskLevel.toLowerCase()}"
    in:fly={{ y: 20, duration: 500 }}
>
    <div class="card-header">
        <h3 class="title">
            <span class="pulse-icon {riskLevel.toLowerCase()}"></span>
            Arithmetic Vitals (v20.0 Architecture)
        </h3>
        <span class="status-badge {riskLevel.toLowerCase()}">{riskLevel}</span>
    </div>

    {#if audit}
        <div class="integrity-section">
            <div class="integrity-header">
                <span class="label">Reality Integrity</span>
                <span class="value">{(audit.integrity * 100).toFixed(1)}%</span>
            </div>
            <div class="integrity-bar">
                <div
                    class="fill"
                    style="width: {audit.integrity *
                        100}%; background: {isSystemicBreach
                        ? '#ff3e3e'
                        : '#00ffcc'}"
                ></div>
                <div class="cliff-marker" style="left: 38%"></div>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric">
                <span class="label">SOFR (Price of Money)</span>
                <div class="value-row">
                    <span class="value"
                        >{audit.findings.sofr.current.toFixed(2)}%</span
                    >
                    <span class="limit">/ {THRESHOLDS.SOFR}%</span>
                </div>
                <div class="progress-bar">
                    <div
                        class="progress"
                        style="width: {(audit.findings.sofr.current /
                            THRESHOLDS.SOFR) *
                            100}%"
                    ></div>
                </div>
            </div>

            <div class="metric">
                <span class="label">Gilt-Bund Spread</span>
                <div class="value-row">
                    <span class="value"
                        >{audit.findings.spreads.giltBund} bps</span
                    >
                    <span class="limit">/ {THRESHOLDS.GILT} bps</span>
                </div>
                <div class="progress-bar">
                    <div
                        class="progress"
                        style="width: {(audit.findings.spreads.giltBund /
                            THRESHOLDS.GILT) *
                            100}%"
                    ></div>
                </div>
            </div>

            <div class="metric">
                <span class="label">XMR Rotation Signal</span>
                <div class="value-row">
                    <span class="value">{audit.findings.xmr.signal}</span>
                    <span class="status-text"
                        >{audit.findings.xmr.recommendation}</span
                    >
                </div>
            </div>
        </div>

        {#if audit.recommendations.length > 0}
            <div class="recommendations">
                {#each audit.recommendations as rec}
                    <div class="rec-item {rec.priority.toLowerCase()}" in:fade>
                        <strong>{rec.action}</strong>: {rec.reason}
                    </div>
                {/each}
            </div>
        {/if}
    {:else}
        <div class="loading">Fetching sovereign telemetry...</div>
    {/if}
</div>

<style>
    .vitals-card {
        background: rgba(13, 13, 15, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        font-family: "Inter", sans-serif;
    }

    .vitals-card.warning {
        border-color: rgba(255, 165, 0, 0.4);
    }
    .vitals-card.critical {
        border-color: rgba(255, 62, 62, 0.4);
        animation: shake 0.5s infinite;
    }

    @keyframes shake {
        0%,
        100% {
            transform: translateX(0);
        }
        25% {
            transform: translateX(-2px);
        }
        75% {
            transform: translateX(2px);
        }
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
    }

    .pulse-icon {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00ffcc;
        box-shadow: 0 0 10px #00ffcc;
    }

    .pulse-icon.warning {
        background: #ffa500;
        box-shadow: 0 0 10px #ffa500;
        animation: pulse 1s infinite;
    }
    .pulse-icon.critical {
        background: #ff3e3e;
        box-shadow: 0 0 10px #ff3e3e;
        animation: pulse 0.5s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.5);
            opacity: 0.5;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .status-badge {
        font-size: 0.7rem;
        padding: 0.25rem 0.6rem;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.05);
        color: #00ffcc;
        text-transform: uppercase;
        font-weight: 700;
    }

    .status-badge.warning {
        color: #ffa500;
        background: rgba(255, 165, 0, 0.1);
    }
    .status-badge.critical {
        color: #ff3e3e;
        background: rgba(255, 62, 62, 0.1);
    }

    .integrity-section {
        margin-bottom: 1.5rem;
    }
    .integrity-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .integrity-header .label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
    }
    .integrity-header .value {
        font-weight: 700;
        color: #00ffcc;
    }

    .integrity-bar {
        height: 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        position: relative;
        overflow: hidden;
    }

    .integrity-bar .fill {
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 6px;
    }
    .cliff-marker {
        position: absolute;
        height: 100%;
        width: 2px;
        background: #ff3e3e;
        top: 0;
        box-shadow: 0 0 5px #ff3e3e;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1.25rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }
    .label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .value-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
    }
    .value {
        font-weight: 700;
        font-size: 1.1rem;
        color: #fff;
    }
    .limit {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
    }

    .progress-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .progress {
        height: 100%;
        background: #00ffcc;
        transition: width 0.5s ease;
    }

    .status-text {
        font-size: 0.8rem;
        color: #00ffcc;
    }

    .recommendations {
        margin-top: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .rec-item {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 0.5rem;
        font-size: 0.85rem;
        border-left: 3px solid #00ffcc;
    }

    .rec-item.high {
        border-left-color: #ffa500;
    }
    .rec-item.immediate {
        border-left-color: #ff3e3e;
        background: rgba(255, 62, 62, 0.05);
    }

    .loading {
        text-align: center;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.9rem;
        padding: 2rem 0;
    }
</style>
