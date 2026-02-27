<script lang="ts">
    import { fade, fly } from "svelte/transition";

    import {
        Hammer,
        Activity,
        CheckCircle2,
        Zap,
        Terminal,
        Play,
        Loader2,
        Shield,
        Cpu,
        Lock,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type LawWafer = {
        id: string;
        name: string;
        region: string;
        riskLevel: "LOW" | "MEDIUM" | "HIGH";
        status: "DRAFT" | "SIMULATING" | "DEPLOYED";
        logic: string;
        coverage: number;
    };

    let wafers = $state<LawWafer[]>([
        {
            id: "WF-0x01",
            name: "Nagano Privacy Shard",
            region: "Nagano",
            riskLevel: "LOW",
            status: "DEPLOYED",
            logic: "IF citizen:verify(AAL3) THEN grant(0xAA_ACCESS)",
            coverage: 99.8,
        },
        {
            id: "WF-0x42",
            name: "Zug SwissVault-9",
            region: "Zug",
            riskLevel: "MEDIUM",
            status: "DRAFT",
            logic: "IF outbound:tx > 1000 ETH THEN trigger(0x5C_QUARANTINE)",
            coverage: 84.2,
        },
    ]);

    let activeWaferId = $state("WF-0x01");
    let activeWafer = $derived(wafers.find((w) => w.id === activeWaferId));

    let isSimulating = $state(false);
    let simProgress = $state(0);
    let simResults = $state<string[]>([]);

    async function runStressSimulation() {
        if (!activeWafer) return;
        isSimulating = true;
        simProgress = 0;
        simResults = [
            "Initializing Borel-Simple simulation mesh...",
            "Fuzzing input vectors for invariant 0x5C...",
        ];

        const steps = [
            { p: 30, res: "Transaction flood test: PASSED (Latency < 2ms)" },
            {
                p: 60,
                res: "Sybil attack simulation: NEUTRALIZED (Reputation gate active)",
            },
            {
                p: 85,
                res: "Cross-jurisdiction leak test: SECURE (ZK-Mirror confirmed)",
            },
            {
                p: 100,
                res: "Policy Integrity: 99.98% / Deployment Recommended.",
            },
        ];

        for (const step of steps) {
            await new Promise((r) => setTimeout(r, 800));
            simProgress = step.p;
            simResults = [...simResults, step.res];
        }
        isSimulating = false;
    }

    function deployWafer() {
        if (activeWafer) {
            activeWafer.status = "DEPLOYED";
            manifold.recordEvent(
                "WAFER_DEPLOY",
                `Law Wafer ${activeWafer.id} baked and deployed to ${activeWafer.region} manifold.`,
            );
        }
    }
</script>

<div class="fabricator-shell">
    <!-- Institutional Header -->
    <header class="fabricator-header">
        <div class="header-brand">
            <div class="logo-box">
                <Hammer size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Policy_Fabricator</h2>
                <div class="flex items-center gap-2">
                    <span class="fabric-label">Fabrication_Gear: V3.2_ZK</span>
                    <div class="fabric-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">WAFERS_IN_VAULT</span>
                <span class="tel-value">{wafers.length}_COMMITTED</span>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block">
                <span class="tel-label">SYSTEM_INTEGRITY</span>
                <span class="tel-value text-cyan-400">0.9998_PF</span>
            </div>
        </div>
    </header>

    <div class="fabricator-body">
        <!-- Wafer Archive Sidebar -->
        <aside class="wafer-sidebar scrollbar-hide">
            <h3 class="sidebar-title">Wafer_Archive</h3>
            <div class="wafer-list">
                {#each wafers as wafer}
                    <button
                        onclick={() => (activeWaferId = wafer.id)}
                        class="wafer-btn"
                        class:active={activeWaferId === wafer.id}
                    >
                        <div class="wafer-btn-meta">
                            <span class="w-id">{wafer.id}</span>
                            <div
                                class="w-status-pip"
                                class:on={wafer.status === "DEPLOYED"}
                            ></div>
                        </div>
                        <h4 class="w-title">{wafer.name}</h4>
                        <div class="w-footer">
                            <span class="w-region">{wafer.region}</span>
                            <span class="w-coverage">{wafer.coverage}% Cov</span
                            >
                        </div>
                    </button>
                {/each}
            </div>
        </aside>

        <!-- Workbench Viewport -->
        <main class="workbench-viewport scrollbar-hide">
            {#if activeWafer}
                <div class="workbench-content" in:fade={{ duration: 400 }}>
                    <!-- Policy Status HUD -->
                    <div class="status-hud">
                        <div class="hud-main">
                            <div class="flex items-center gap-4 mb-4">
                                <span class="hud-chip">Policy_Module</span>
                                <h1 class="hud-title">{activeWafer.name}</h1>
                            </div>
                            <p class="hud-desc">
                                Institutional Enforcement Logic for
                                jurisdictional sharding and ZK-Verified state
                                transitions.
                            </p>
                        </div>
                        <div class="hud-stats">
                            <div class="hud-stat">
                                <span class="s-label">Risk_Vector</span>
                                <span
                                    class="s-value"
                                    class:text-emerald-400={activeWafer.riskLevel ===
                                        "LOW"}
                                    class:text-amber-400={activeWafer.riskLevel ===
                                        "MEDIUM"}
                                >
                                    {activeWafer.riskLevel}_RESISTANCE
                                </span>
                            </div>
                            <div class="hud-stat">
                                <span class="s-label">Assurance_Level</span>
                                <span class="s-value">AAL4_Sovereign</span>
                            </div>
                        </div>
                    </div>

                    <!-- Logic Baking Lab -->
                    <div class="logic-lab">
                        <header class="lab-header">
                            <div class="flex items-center gap-3">
                                <Cpu size={14} class="text-cyan-400" />
                                <h3>Logic_Baking_Matrix</h3>
                            </div>
                            <div class="flex items-center gap-4">
                                <Terminal size={12} class="opacity-20" />
                                <Lock size={12} class="opacity-20" />
                            </div>
                        </header>
                        <div class="logic-editor">
                            <div class="logic-code">
                                <code>{activeWafer.logic}</code>
                                <span class="cursor-blink">|</span>
                            </div>
                            <div class="logic-overlay"></div>
                        </div>
                    </div>

                    <!-- Simulation & Stress Lab -->
                    <div class="simulation-lab">
                        {#if isSimulating}
                            <div class="sim-overlay" in:fade>
                                <div class="sim-loader">
                                    <div class="loader-ring"></div>
                                    <Loader2
                                        size={32}
                                        class="animate-spin text-cyan-400"
                                    />
                                </div>
                                <div class="sim-progress-box">
                                    <div class="sim-track">
                                        <div
                                            class="sim-fill"
                                            style="width: {simProgress}%"
                                        ></div>
                                    </div>
                                    <span class="sim-label"
                                        >Fuzzing Invariants: {simProgress}%</span
                                    >
                                </div>
                            </div>
                        {/if}

                        <header class="lab-header">
                            <div class="flex items-center gap-3">
                                <Activity size={14} class="text-amber-400" />
                                <h3>Borel-Simple_Simulation</h3>
                            </div>
                            <button
                                onclick={runStressSimulation}
                                disabled={isSimulating}
                                class="action-btn"
                            >
                                <Play size={10} fill="currentColor" />
                                <span>Run_Stress_Test</span>
                            </button>
                        </header>

                        <div class="results-stack scrollbar-hide">
                            {#each simResults as result, i}
                                <div
                                    class="result-item"
                                    in:fly={{ x: -20, delay: i * 100 }}
                                >
                                    <CheckCircle2
                                        size={12}
                                        class="text-emerald-400"
                                    />
                                    <span>{result}</span>
                                </div>
                            {/each}
                            {#if simResults.length === 0}
                                <div class="results-placeholder">
                                    <Shield size={24} class="opacity-10 mb-4" />
                                    <p>
                                        Ready for Formal Verification Simulation
                                    </p>
                                </div>
                            {/if}
                        </div>
                    </div>

                    <button
                        onclick={deployWafer}
                        disabled={activeWafer.status === "DEPLOYED" ||
                            isSimulating}
                        class="deploy-btn"
                    >
                        <Zap size={14} />
                        <span>Bake_&_Deploy_to_Mainnet</span>
                    </button>
                </div>
            {/if}
        </main>
    </div>
</div>

<style>
    .fabricator-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
    }

    .fabricator-header {
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .logo-box {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #06b6d4, #22d3ee);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(6, 182, 212, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .fabric-label {
        font-size: 8px;
        font-weight: 800;
        color: #22d3ee;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-style: italic;
    }

    .fabric-pulsar {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #06b6d4;
        box-shadow: 0 0 10px #06b6d4;
        animation: pulse 1s infinite;
    }

    .header-telemetry {
        display: flex;
        gap: 2rem;
    }

    .tel-block {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
        margin-bottom: 2px;
    }

    .tel-value {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .tel-divider {
        width: 1px;
        height: 24px;
        background: rgba(255, 255, 255, 0.05);
    }

    .fabricator-body {
        flex: 1;
        display: flex;
        overflow: hidden;
    }

    .wafer-sidebar {
        width: 320px;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(0, 0, 0, 0.1);
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .sidebar-title {
        font-size: 10px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .wafer-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .wafer-btn {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .wafer-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(4px);
    }

    .wafer-btn.active {
        background: rgba(6, 182, 212, 0.1);
        border-color: rgba(6, 182, 212, 0.3);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }

    .wafer-btn-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .w-id {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
    }

    .w-status-pip {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
    }

    .w-status-pip.on {
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    .w-title {
        font-size: 12px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
    }

    .w-footer {
        display: flex;
        justify-content: space-between;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.2);
    }

    .workbench-viewport {
        flex: 1;
        padding: 3rem;
        overflow-y: auto;
    }

    .workbench-content {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 2.5rem;
    }

    .status-hud {
        display: flex;
        justify-content: space-between;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 36px;
        padding: 2.5rem;
    }

    .hud-chip {
        font-size: 8px;
        font-weight: 950;
        color: #22d3ee;
        background: rgba(6, 182, 212, 0.1);
        padding: 4px 10px;
        border-radius: 8px;
        text-transform: uppercase;
    }

    .hud-title {
        font-size: 28px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: -0.02em;
    }

    .hud-desc {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
        max-width: 400px;
    }

    .hud-stats {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 1.5rem;
        text-align: right;
    }

    .hud-stat {
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
        font-size: 14px;
        font-weight: 950;
        text-transform: uppercase;
        color: white;
    }

    .logic-lab {
        background: #090e1a;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        overflow: hidden;
    }

    .lab-header {
        padding: 1.25rem 2rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .lab-header h3 {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .logic-editor {
        padding: 2.5rem;
        position: relative;
    }

    .logic-code {
        font-family: "JetBrains Mono", monospace;
        font-size: 13px;
        color: #22d3ee;
        line-height: 1.6;
        min-height: 100px;
    }

    .cursor-blink {
        animation: blink 1s infinite;
        color: white;
    }

    .simulation-lab {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        position: relative;
        overflow: hidden;
    }

    .sim-overlay {
        position: absolute;
        inset: 0;
        background: rgba(9, 14, 26, 0.8);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 20;
        gap: 2rem;
    }

    .sim-loader {
        position: relative;
        width: 64px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .loader-ring {
        position: absolute;
        inset: 0;
        border: 2px solid rgba(6, 182, 212, 0.1);
        border-radius: 50%;
    }

    .sim-progress-box {
        width: 300px;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }

    .sim-track {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }

    .sim-fill {
        height: 100%;
        background: #06b6d4;
        transition: width 0.3s;
    }

    .sim-label {
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.2em;
    }

    .action-btn {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }

    .action-btn:hover {
        background: rgba(245, 158, 11, 0.2);
    }

    .results-stack {
        padding: 2rem;
        height: 200px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .result-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 10px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.01);
        padding: 0.75rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }

    .results-placeholder {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.15);
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
    }

    .deploy-btn {
        width: 100%;
        padding: 1.5rem;
        background: #06b6d4;
        border: none;
        border-radius: 24px;
        color: black;
        font-size: 12px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
    }

    .deploy-btn:hover:not(:disabled) {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(6, 182, 212, 0.4);
    }

    .deploy-btn:disabled {
        opacity: 0.2;
        cursor: not-allowed;
        filter: grayscale(1);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.05);
        }
    }
    @keyframes blink {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0;
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
