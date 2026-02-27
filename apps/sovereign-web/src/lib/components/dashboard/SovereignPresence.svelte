<script lang="ts">
    import { fade, scale } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import {
        Cpu,
        Activity,
        ShieldCheck,
        CheckCircle2,
        Network,
        Database,
        Eye,
        Gauge,
        ArrowUpRight,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type OperatorRole = "VALIDATOR" | "VERIFIER" | "COMPUTE" | "OBSERVER";

    let activeRoles = $state<Set<OperatorRole>>(new Set());
    let isDeploying = $state(false);
    let deployProgress = $state(0);
    let podStatus = $state<"OFFLINE" | "SYNCING" | "OPERATIONAL">("OFFLINE");

    const roles = [
        {
            id: "VALIDATOR",
            label: "Validator",
            icon: ShieldCheck,
            color: "text-emerald-400",
            bg: "bg-emerald-400/10",
            requirement: "100k AGE Stake + NIST AAL3",
            yield: "12.5% APY",
            load: "High",
        },
        {
            id: "VERIFIER",
            label: "ZK-Verifier",
            icon: Eye,
            color: "text-cyan-400",
            bg: "bg-cyan-400/10",
            requirement: "Veracity Shard v1.2",
            yield: "8.2% APY",
            load: "Medium",
        },
        {
            id: "COMPUTE",
            label: "Compute Node",
            icon: Cpu,
            color: "text-indigo-400",
            bg: "bg-indigo-400/10",
            requirement: "Nvidia 4090+ / H100",
            yield: "Var/TFLOP",
            load: "High",
        },
        {
            id: "OBSERVER",
            label: "Relay Node",
            icon: Network,
            color: "text-amber-400",
            bg: "bg-amber-400/10",
            requirement: "Low Latency Fiber",
            yield: "2.1% APY",
            load: "Minimal",
        },
    ];

    function toggleRole(role: OperatorRole) {
        if (activeRoles.has(role)) {
            activeRoles.delete(role);
        } else {
            activeRoles.add(role);
        }
        activeRoles = new Set(activeRoles); // Trigger reactivity
    }

    async function deployPod() {
        if (activeRoles.size === 0) return;

        isDeploying = true;
        deployProgress = 0;
        podStatus = "SYNCING";

        manifold.recordEvent(
            "POD_DEPLOY",
            `Initializing Sovereign Pod with roles: ${Array.from(activeRoles).join(", ")}`,
        );

        const steps = [
            { p: 20, msg: "Pulling Sovereign Atlas Image..." },
            { p: 45, msg: "Initializing UDC_SCHEMA on local NVMe..." },
            { p: 70, msg: "Syncing Authoritative Maps..." },
            { p: 90, msg: "Binding IdentityAttest 0x70..." },
            { p: 100, msg: "Pod Operational." },
        ];

        for (const step of steps) {
            await new Promise((r) => setTimeout(r, 800));
            deployProgress = step.p;
            if (step.p === 100) {
                isDeploying = false;
                podStatus = "OPERATIONAL";
                manifold.recordEvent(
                    "POD_READY",
                    "Sovereign Pod is now auditing and validating world-state.",
                );
            }
        }
    }

    let stats = $state({
        uptime: 99.98,
        latency: 12,
        throughput: 1420,
    });
</script>

<div class="presence-shell">
    <!-- Institutional Header HUD -->
    <header class="presence-header">
        <div class="header-brand">
            <div class="logo-box">
                <Network size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Presence</h2>
                <div class="flex items-center gap-2">
                    <div
                        class="status-dot"
                        class:active={podStatus === "OPERATIONAL"}
                        class:syncing={podStatus === "SYNCING"}
                    ></div>
                    <span class="status-text">{podStatus}</span>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">GLOBAL_WEIGHT</span>
                <span class="tel-value">0.024%</span>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block">
                <span class="tel-label">NETWORK_UPTIME</span>
                <span class="tel-value text-emerald-400">{stats.uptime}%</span>
            </div>
        </div>
    </header>

    <!-- Main Command Interface -->
    <div class="presence-content scrollbar-hide">
        <!-- Contribution Vectors (Role Selection) -->
        <section class="config-section">
            <div class="section-meta">
                <h3 class="section-title">Contribution_Vectors</h3>
                <p class="section-desc">
                    Host high-assurance roles on your Sovereign Pod to maximize
                    collective resilience.
                </p>
            </div>

            <div class="role-matrix">
                {#each roles as role}
                    <button
                        onclick={() => toggleRole(role.id as OperatorRole)}
                        disabled={podStatus === "OPERATIONAL"}
                        class="role-card"
                        class:active={activeRoles.has(role.id as OperatorRole)}
                    >
                        <div class="role-card-top">
                            <div class="role-icon-shell {role.bg} {role.color}">
                                <role.icon size={18} />
                            </div>
                            <div class="flex flex-col">
                                <span class="role-label">{role.label}</span>
                                <span class="role-load">Load: {role.load}</span>
                            </div>
                            {#if activeRoles.has(role.id as OperatorRole)}
                                <div
                                    class="role-check"
                                    in:scale={{
                                        duration: 300,
                                        easing: cubicOut,
                                    }}
                                >
                                    <CheckCircle2
                                        size={12}
                                        class="text-white"
                                    />
                                </div>
                            {/if}
                        </div>

                        <div class="role-card-metrics">
                            <div class="metric">
                                <span class="m-label">Requirement</span>
                                <span class="m-value">{role.requirement}</span>
                            </div>
                            <div class="metric text-right">
                                <span class="m-label">Est_Yield</span>
                                <span class="m-value text-emerald-400"
                                    >{role.yield}</span
                                >
                            </div>
                        </div>
                    </button>
                {/each}
            </div>
        </section>

        <!-- Deployment Control Center -->
        <section class="deployment-section">
            <div class="control-canvas">
                {#if podStatus === "OFFLINE" && !isDeploying}
                    <div class="init-view" in:fade>
                        <div class="init-icon-box">
                            <Database size={48} />
                            <div class="init-aura"></div>
                        </div>
                        <div class="init-text">
                            <h3>Initialize_Sovereign_Pod</h3>
                            <p>
                                Instantiate a local Sovereign Data Core (SDC)
                                and bind IdentityAttest.
                            </p>
                        </div>
                        <button
                            onclick={deployPod}
                            disabled={activeRoles.size === 0}
                            class="deploy-btn"
                        >
                            <span>Execute_One-Click_Deploy</span>
                            <ArrowUpRight size={16} />
                        </button>
                    </div>
                {:else if isDeploying}
                    <div class="sync-view" in:fade>
                        <div class="sync-progress-outer">
                            <div
                                class="sync-progress-inner"
                                style="width: {deployProgress}%"
                            ></div>
                        </div>
                        <div class="sync-status">
                            <Activity
                                size={16}
                                class="text-emerald-400 animate-pulse"
                            />
                            <span class="sync-label"
                                >Hyper_Synchronizing_SDC_v2</span
                            >
                        </div>
                        <div class="sync-indicators">
                            {#each Array(4) as _}
                                <div class="indicator-bar">
                                    <div class="fill animate-bounce"></div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {:else if podStatus === "OPERATIONAL"}
                    <div class="operational-view" in:fade>
                        <div class="op-metrics-grid">
                            <div class="op-stat">
                                <div class="op-stat-icon text-emerald-400">
                                    <Gauge size={24} />
                                </div>
                                <span class="op-stat-val">124.5</span>
                                <span class="op-stat-label">TFLOPS_Shared</span>
                            </div>
                            <div class="op-stat">
                                <div class="op-stat-icon text-cyan-400">
                                    <Activity size={24} />
                                </div>
                                <span class="op-stat-val">4.2ms</span>
                                <span class="op-stat-label">Shard_Latency</span>
                            </div>
                        </div>

                        <div class="reward-box">
                            <div class="flex items-center justify-between mb-4">
                                <span class="reward-label"
                                    >Accumulated_Yield</span
                                >
                                <span class="reward-val text-emerald-400"
                                    >+124.50 AGE</span
                                >
                            </div>
                            <button class="claim-btn"
                                >Claim_Sovereign_Yield</button
                            >
                        </div>

                        <button
                            onclick={() => {
                                podStatus = "OFFLINE";
                                activeRoles.clear();
                                activeRoles = new Set();
                            }}
                            class="terminate-btn"
                        >
                            Terminate_Operations
                        </button>
                    </div>
                {/if}
            </div>
        </section>
    </div>

    <!-- Institutional Footer -->
    <footer class="presence-footer">
        <div class="footer-peer-density">
            <Network size={14} class="text-indigo-400" />
            <span>Mesh_Peer_Density: 1,421 Nodes</span>
        </div>
        <div class="footer-compliance">
            <span>Borel-Simple_Compliant</span>
            <div class="compliance-divider"></div>
            <span>SDC_v2_Active</span>
        </div>
    </footer>
</div>

<style>
    .presence-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
        position: relative;
    }

    .presence-header {
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
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
    }

    .status-dot.active {
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
    }
    .status-dot.syncing {
        background: #3b82f6;
        animation: pulse 1s infinite;
    }

    .status-text {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
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

    .presence-content {
        flex: 1;
        padding: 2.5rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2.5rem;
        overflow-y: auto;
    }

    .section-title {
        font-size: 10px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 0.75rem;
    }

    .section-desc {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .role-matrix {
        display: grid;
        gap: 1rem;
    }

    .role-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.25rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }

    .role-card:hover:not(:disabled) {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .role-card.active {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
    }

    .role-card-top {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.25rem;
    }

    .role-icon-shell {
        width: 36px;
        height: 36px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .role-label {
        font-size: 11px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .role-load {
        font-size: 8px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .role-check {
        margin-left: auto;
        width: 20px;
        height: 20px;
        background: #10b981;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .role-card-metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .m-label {
        display: block;
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .m-value {
        font-size: 9px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.6);
    }

    .control-canvas {
        height: 100%;
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        padding: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .init-view {
        text-align: center;
        max-width: 280px;
    }

    .init-icon-box {
        position: relative;
        width: 100px;
        height: 100px;
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3b82f6;
        margin: 0 auto 2rem;
    }

    .init-aura {
        position: absolute;
        inset: -10px;
        background: radial-gradient(
            circle,
            rgba(59, 130, 246, 0.1),
            transparent 70%
        );
        filter: blur(10px);
        animation: pulse 2s infinite;
    }

    .init-text h3 {
        font-size: 18px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
    }

    .init-text p {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.3);
        line-height: 1.6;
        margin-bottom: 2.5rem;
    }

    .deploy-btn {
        width: 100%;
        padding: 1.25rem;
        background: white;
        border: none;
        border-radius: 18px;
        color: black;
        font-size: 11px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .deploy-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(255, 255, 255, 0.2);
    }

    .deploy-btn:disabled {
        opacity: 0.1;
        cursor: not-allowed;
    }

    .sync-view {
        width: 100%;
        text-align: center;
    }

    .sync-progress-outer {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        margin-bottom: 2.5rem;
        overflow: hidden;
    }

    .sync-progress-inner {
        height: 100%;
        background: #10b981;
        transition: width 0.5s ease;
    }

    .sync-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
    }

    .sync-label {
        font-size: 10px;
        font-weight: 900;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .sync-indicators {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }

    .indicator-bar {
        width: 4px;
        height: 24px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 100px;
        overflow: hidden;
    }

    .indicator-bar .fill {
        width: 100%;
        height: 100%;
        background: #10b981;
    }

    .operational-view {
        width: 100%;
    }

    .op-metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .op-stat {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
    }

    .op-stat-icon {
        margin-bottom: 1rem;
    }

    .op-stat-val {
        display: block;
        font-size: 20px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
        margin-bottom: 0.25rem;
    }

    .op-stat-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .reward-box {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .reward-label {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
    }

    .reward-val {
        font-size: 13px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .claim-btn {
        width: 100%;
        padding: 0.75rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 12px;
        color: #10b981;
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s;
    }

    .claim-btn:hover {
        background: rgba(16, 185, 129, 0.2);
    }

    .terminate-btn {
        width: 100%;
        background: none;
        border: none;
        color: rgba(244, 63, 94, 0.3);
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        cursor: pointer;
        transition: color 0.3s;
    }

    .terminate-btn:hover {
        color: #f43f5e;
    }

    .presence-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .footer-peer-density {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
    }

    .footer-compliance {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        font-style: italic;
    }

    .compliance-divider {
        width: 1px;
        height: 12px;
        background: rgba(255, 255, 255, 0.05);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
