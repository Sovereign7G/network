<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly, fade } from "svelte/transition";
    import { ShieldAlert, FileCode2, UserCheck, Scale } from "lucide-svelte";

    const courtCases = $derived(manifold?.governanceState?.courtCases);
    const lawWafers = $derived(manifold?.governanceState?.lawWafers);

    function handleVote(caseId: string, vote: "APPROVE" | "DENY" | "ABSTAIN") {
        manifold.voteCourtCase(caseId, vote);
    }
</script>

<div class="judicial-shell" in:fade>
    <!-- Background Gradient Aura -->
    <div class="judicial-aura"></div>

    <!-- Institutional Header -->
    <header class="judicial-header">
        <div class="header-brand">
            <div class="logo-box">
                <Scale size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Kernel_Governance_Court</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label">JUDICIAL_SESSION_ACTIVE</span>
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>
    </header>

    <div class="judicial-body scrollbar-hide">
        <!-- Court Cases -->
        <section class="case-viewport">
            <header class="section-header">
                <ShieldAlert size={12} class="text-rose-400" />
                <h3>Pending_Trials</h3>
            </header>

            <div class="case-list">

                {#each courtCases.filter((c) => c.status === "PENDING") as caseItem}
                    <div class="case-card" in:fly={{ y: 20 }}>
                        <div class="case-meta">
                            <span class="c-id"
                                >0x{caseItem.id.split("-")[1]}</span
                            >
                            <span class="c-status">PENDING</span>
                        </div>
                        <h4 class="c-title">{caseItem.id.replace("-", "_")}</h4>
                        <p class="c-desc">
                            Institutional consensus required for state
                            transition.
                        </p>

                        <div class="case-actions">
                            <button
                                class="act-btn approve"
                                onclick={() =>
                                    handleVote(caseItem.id, "APPROVE")}
                            >
                                Approve
                            </button>
                            <button
                                class="act-btn deny"
                                onclick={() => handleVote(caseItem.id, "DENY")}
                            >
                                Deny
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
        </section>

        <!-- Law Wafers -->
        <section class="wafer-viewport">
            <header class="section-header">
                <FileCode2 size={12} class="text-cyan-400" />
                <h3>Law_Wafer_Foundry</h3>
            </header>

            <div class="wafer-list">
                {#each lawWafers as wafer}
                    <div class="wafer-card group">
                        <div class="wafer-holo"></div>
                        <div class="wafer-content">
                            <div class="wafer-icon">
                                <FileCode2 size={16} class="text-cyan-400" />
                            </div>
                            <div class="wafer-info">
                                <h4 class="w-title">LAW_WAFER_{wafer.id}</h4>
                                <p class="w-meta">
                                    {wafer.template} // {wafer.region}
                                </p>
                            </div>
                        </div>

                        {#if wafer.status === "FABRICATING"}
                            <div class="wafer-deploy">
                                <div class="deploy-label">
                                    STABILIZING_SUBSTRATE...
                                </div>
                                <div class="progress-track">
                                    <div
                                        class="progress-fill"
                                        style:width="{(wafer.progress || 0) *
                                            100}%"
                                    ></div>
                                </div>
                            </div>
                        {/if}
                    </div>
                {/each}

                <button
                    class="fabricate-btn"
                    onclick={() =>
                        manifold.fabricateWafer("EU", "GDPR-MESH-v2")}
                >
                    <div class="btn-inner">
                        <span>+ Fabricate New Policy</span>
                    </div>
                </button>
            </div>
        </section>
    </div>

    <!-- Court Footer -->
    <footer class="judicial-footer">
        <div class="footer-stats">
            <div class="stat-item">
                <span class="s-label">Jurists_Online</span>
                <span class="s-value">12 / 12</span>
            </div>
            <div class="stat-item">
                <span class="s-label">Consensus_Protocol</span>
                <span class="s-value">BFT_Majority</span>
            </div>
        </div>
        <div class="footer-assurance">
            <UserCheck size={12} class="text-emerald-400" />
            <span>Identity_Verified // Session_Secure</span>
        </div>
    </footer>
</div>

<style>
    .judicial-shell {
        height: 100%;
        background: rgba(10, 5, 5, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
        position: relative;
    }

    .judicial-aura {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at 0% 0%,
            rgba(244, 63, 94, 0.05) 0%,
            transparent 70%
        );
        pointer-events: none;
    }

    .judicial-header {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 10;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logo-box {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(244, 63, 94, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .phase-label {
        font-size: 8px;
        font-weight: 800;
        color: #f43f5e;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .phase-pulsar {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #f43f5e;
        box-shadow: 0 0 10px #f43f5e;
        animation: pulse 2s infinite;
    }

    .judicial-body {
        flex: 1;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1px;
        background: rgba(255, 255, 255, 0.05);
        overflow: hidden;
    }

    .case-viewport,
    .wafer-viewport {
        background: rgba(10, 5, 5, 0.2);
        padding: 2rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .section-header h3 {
        font-size: 10px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .case-list,
    .wafer-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .case-card,
    .wafer-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .case-card:hover {
        border-color: rgba(244, 63, 94, 0.3);
    }
    .wafer-card:hover {
        border-color: rgba(34, 211, 238, 0.3);
    }

    .case-meta,
    .wafer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .c-id {
        font-family: "JetBrains Mono", monospace;
        font-size: 9px;
        color: #f43f5e;
    }
    .c-status {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
    }

    .c-title,
    .w-title {
        font-size: 14px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .c-desc {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.5;
    }

    .case-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .act-btn {
        padding: 0.75rem;
        border-radius: 12px;
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        transition: all 0.2s;
    }

    .approve {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .approve:hover {
        background: #10b981;
        color: white;
    }

    .deny {
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.2);
    }
    .deny:hover {
        background: #f43f5e;
        color: white;
    }

    .wafer-holo {
        position: absolute;
        top: -20px;
        right: -20px;
        width: 80px;
        height: 80px;
        background: radial-gradient(
            circle,
            rgba(34, 211, 238, 0.1) 0%,
            transparent 70%
        );
        border-radius: 50%;
        filter: blur(20px);
        opacity: 0;
        transition: opacity 0.3s;
    }

    .wafer-card:hover .wafer-holo {
        opacity: 1;
    }

    .wafer-icon {
        width: 32px;
        height: 32px;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .w-meta {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .wafer-deploy {
        margin-top: 1.5rem;
    }
    .deploy-label {
        font-size: 7px;
        font-weight: 900;
        color: #22d3ee;
        margin-bottom: 0.5rem;
        letter-spacing: 0.1em;
    }

    .progress-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
    }

    .fabricate-btn {
        width: 100%;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.01);
        border: 2px dashed rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        transition: all 0.3s;
    }

    .fabricate-btn:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .btn-inner {
        font-size: 10px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-family: "JetBrains Mono", monospace;
    }

    .judicial-footer {
        padding: 1.5rem 2rem;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .footer-stats {
        display: flex;
        gap: 2rem;
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .s-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }
    .s-value {
        font-size: 11px;
        font-weight: 950;
        color: white;
    }

    .footer-assurance {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.2);
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
