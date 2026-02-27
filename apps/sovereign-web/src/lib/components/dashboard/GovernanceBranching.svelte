<script lang="ts">
    import { fade, slide, fly } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        GitBranch,
        Box,
        ShieldCheck,
        AlertCircle,
        RefreshCcw,
        Zap,
        Binary,
        Layers,
        Cpu,
    } from "lucide-svelte";

    let experimentId = $state("EXP_ECON_001");
    let isBranching = $derived(manifold.branchingState.active);
    let isAdmin = $derived(manifold.permissionLevel === "SOVEREIGN_OVERSEER");

    function startBranch() {
        manifold.initiateBranch(experimentId);
    }

    function mergeBranch() {
        if (!isAdmin) return;
        manifold.recordEvent(
            "GOV_BRANCH_MERGED",
            `Policy parameters from ${manifold.branchingState.branchId} merged into Core Shard.`,
        );
        manifold.branchingState.active = false;
    }

    // High-assurance metadata for simulations
    const simulatedMetrics = [
        { label: "COHESION", value: "0.992", status: "STABLE" },
        { label: "ENTROPY", value: "0.008", status: "NOMINAL" },
        { label: "LATENCY", value: "1.2ms", status: "OPTIMIZED" },
    ];
</script>

<div class="branching-manifold" in:fade>
    <div class="manifold-glass"></div>
    <div class="manifold-aura {isBranching ? 'active' : ''}"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="flex items-center gap-4">
            <div class="icon-vessel {isBranching ? 'branching' : ''}">
                <GitBranch size={20} />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Governance_Lab</h2>
                <div class="flex items-center gap-2">
                    <span class="subtitle">Policy_Branching_Simulator</span>
                    <div class="status-dot {isBranching ? 'active' : ''}"></div>
                </div>
            </div>
        </div>
        <div class="header-telemetry">
            <span class="tel-label">SHARD_INDEX</span>
            <span class="tel-value">ROOT_0xFD</span>
        </div>
    </header>

    <div class="manifold-body scrollbar-hide">
        {#if !isBranching}
            <section class="initialization-view" in:fly={{ y: 20 }}>
                <div class="info-block">
                    <Binary size={14} class="text-amber-400/60" />
                    <p>
                        Spin up a high-fidelity Copy-on-Write (COW) data branch
                        to safely simulate governance or economic shards using
                        real-time protocol telemetry.
                    </p>
                </div>

                <div class="input-stratum">
                    <label for="exp-id">Dimension_Context</label>
                    <div class="input-wrapper">
                        <input
                            id="exp-id"
                            bind:value={experimentId}
                            placeholder="EXP_ID_000"
                        />
                        <Layers size={14} class="text-white/10" />
                    </div>
                </div>

                <button onclick={startBranch} class="initiate-btn">
                    <div class="btn-shine"></div>
                    <Box size={16} />
                    <span>Initiate COW Manifest</span>
                </button>
            </section>
        {:else}
            <section class="simulation-view" in:slide>
                <!-- Active Branch Status -->
                <div class="active-status-card">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                            <span class="label">ACTIVE_BRANCH</span>
                            <span class="hash"
                                >{manifold.branchingState.branchId}</span
                            >
                        </div>
                        <div class="epoch-badge">EPOCH_8.42</div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="progress-container">
                        <div class="flex justify-between mb-2">
                            <span class="prog-label"
                                >SIMULATION_STRESS_TEST</span
                            >
                            <span class="prog-value"
                                >{manifold.branchingState.progress}%</span
                            >
                        </div>
                        <div class="prog-track">
                            <div
                                class="prog-fill"
                                style:width="{manifold.branchingState
                                    .progress}%"
                            ></div>
                        </div>
                    </div>
                </div>

                <!-- Simulation Metrics -->
                <div class="metrics-grid">
                    {#each simulatedMetrics as metric}
                        <div class="metric-card">
                            <span class="m-label">{metric.label}</span>
                            <div class="flex items-center justify-between mt-1">
                                <span class="m-value">{metric.value}</span>
                                <span class="m-status">{metric.status}</span>
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- Branch Metadata -->
                <div class="metadata-stratum">
                    <div class="meta-item">
                        <span class="meta-label">ECONOMIC_SHIFT</span>
                        <div class="flex items-center gap-2 mt-1">
                            <Zap
                                size={10}
                                class={manifold.branchingState
                                    .economicMoodShift === "BULLISH"
                                    ? "text-emerald-400"
                                    : "text-white/40"}
                            />
                            <span
                                class="meta-value {manifold.branchingState
                                    .economicMoodShift === 'BULLISH'
                                    ? 'text-emerald-400'
                                    : 'text-white'}"
                            >
                                {manifold.branchingState.economicMoodShift}
                            </span>
                        </div>
                    </div>
                    <div class="meta-divider"></div>
                    <div class="meta-item text-right">
                        <span class="meta-label">PARENT_HASH</span>
                        <span class="meta-value font-mono opacity-40 block mt-1"
                            >{manifold.branchingState.parentBranch.slice(
                                0,
                                12,
                            )}...</span
                        >
                    </div>
                </div>

                <!-- Assurance Section -->
                {#if manifold.branchingState.proofGenerated}
                    <div class="assurance-manifold" in:fade>
                        <header class="assurance-header">
                            <ShieldCheck size={16} class="text-emerald-400" />
                            <h3>Borel-Stable Proof Secured</h3>
                        </header>
                        <p>
                            Simulation coherent. Policy delta verified against
                            10M synthetic iterations via ZK-STARK proof set.
                        </p>

                        {#if isAdmin}
                            <button onclick={mergeBranch} class="commit-btn">
                                <Zap size={14} />
                                <span>Commit to Protocol Mainnet</span>
                            </button>
                        {:else}
                            <div class="admin-lock">
                                <AlertCircle size={12} class="text-rose-400" />
                                <span
                                    >Overseer level required to finalize merge</span
                                >
                            </div>
                        {/if}
                    </div>
                {:else}
                    <div class="optimizing-card">
                        <div class="flex items-center gap-4">
                            <div class="spinner-vessel">
                                <RefreshCcw
                                    size={16}
                                    class="animate-spin text-amber-400"
                                />
                            </div>
                            <div class="flex flex-col">
                                <span class="opt-title"
                                    >Policy_Optimization_Loop</span
                                >
                                <span class="opt-desc"
                                    >Running synthetic stress test in isolated
                                    sandbox...</span
                                >
                            </div>
                        </div>
                    </div>
                {/if}
            </section>
        {/if}
    </div>

    <!-- Footer Control Area -->
    <footer class="manifold-footer">
        <div class="flex items-center gap-4">
            <div class="flex items-center gap-2 opacity-20">
                <Cpu size={12} />
                <span class="text-[8px] font-black uppercase tracking-[0.2em]"
                    >Causal_Engine_v4.2</span
                >
            </div>
            <div class="footer-divider"></div>
            <div class="flex items-center gap-2 text-cyan-400/40">
                <span class="text-[8px] font-black uppercase tracking-widest"
                    >Shard: MAINNET_BORN</span
                >
            </div>
        </div>
        <div class="flex -space-x-1">
            {#each Array(4) as _}
                <div
                    class="w-4 h-4 rounded-full border border-zinc-950 bg-zinc-800"
                ></div>
            {/each}
        </div>
    </footer>
</div>

<style>
    .branching-manifold {
        height: 100%;
        background: rgba(10, 5, 20, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        position: relative;
        overflow: hidden;
    }

    .manifold-glass {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(251, 191, 36, 0.03),
            transparent
        );
        pointer-events: none;
    }

    .manifold-aura {
        position: absolute;
        inset: -100px;
        background: radial-gradient(
            circle at center,
            rgba(251, 191, 36, 0.05),
            transparent 70%
        );
        opacity: 0;
        transition: opacity 1s;
        pointer-events: none;
    }
    .manifold-aura.active {
        opacity: 1;
    }

    .manifold-header {
        padding: 2rem 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .icon-vessel {
        width: 44px;
        height: 44px;
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid rgba(251, 191, 36, 0.2);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fbbf24;
        transition: all 0.4s;
    }
    .icon-vessel.branching {
        background: rgba(34, 211, 238, 0.1);
        border-color: rgba(34, 211, 238, 0.3);
        color: #22d3ee;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.2);
    }

    .title {
        font-size: 14px;
        font-weight: 950;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
    }
    .subtitle {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
    }
    .status-dot.active {
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    .header-telemetry {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 2px;
    }
    .tel-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .tel-value {
        font-size: 11px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .manifold-body {
        flex: 1;
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        overflow-y: auto;
    }

    .info-block {
        display: flex;
        gap: 1.25rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .info-block p {
        font-size: 11px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
        font-style: italic;
    }

    .input-stratum {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .input-stratum label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    .input-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 0 1.25rem;
    }
    .input-wrapper input {
        flex: 1;
        background: transparent;
        border: none;
        height: 52px;
        color: #fbbf24;
        font-size: 13px;
        font-weight: 800;
        font-family: "JetBrains Mono", monospace;
        outline: none;
    }

    .initiate-btn {
        width: 100%;
        height: 60px;
        background: #fbbf24;
        border: none;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        color: black;
        font-size: 11px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.4s;
        box-shadow: 0 10px 30px rgba(251, 191, 36, 0.2);
    }
    .initiate-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(251, 191, 36, 0.3);
    }

    .active-status-card {
        background: rgba(251, 191, 36, 0.05);
        border: 1px solid rgba(251, 191, 36, 0.1);
        border-radius: 24px;
        padding: 1.75rem;
    }
    .active-status-card .label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(251, 191, 36, 0.6);
        text-transform: uppercase;
    }
    .active-status-card .hash {
        font-size: 12px;
        font-weight: 950;
        color: #fbbf24;
        font-family: "JetBrains Mono", monospace;
    }
    .epoch-badge {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
        padding: 4px 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
    }

    .progress-container {
        margin-top: 1.5rem;
    }
    .prog-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .prog-value {
        font-size: 9px;
        font-weight: 950;
        color: #fbbf24;
    }
    .prog-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 100px;
        overflow: hidden;
    }
    .prog-fill {
        height: 100%;
        background: #fbbf24;
        border-radius: 100px;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.4);
        transition: width 0.4s ease;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
    }
    .m-label {
        font-size: 6px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }
    .m-value {
        font-size: 11px;
        font-weight: 950;
        color: white;
    }
    .m-status {
        font-size: 6px;
        font-weight: 950;
        color: #10b981;
    }

    .metadata-stratum {
        display: flex;
        align-items: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .meta-item {
        flex: 1;
    }
    .meta-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
    }
    .meta-value {
        font-size: 10px;
        font-weight: 800;
        display: block;
    }
    .meta-divider {
        width: 1px;
        height: 32px;
        background: rgba(255, 255, 255, 0.05);
        margin: 0 1.5rem;
    }

    .assurance-manifold {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 28px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .assurance-manifold h3 {
        font-size: 13px;
        font-weight: 950;
        color: #10b981;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .assurance-manifold p {
        font-size: 10px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .commit-btn {
        width: 100%;
        height: 52px;
        background: #10b981;
        border: none;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        color: black;
        font-size: 10px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.3s;
    }
    .commit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }

    .admin-lock {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 1rem;
        background: rgba(244, 63, 94, 0.05);
        border: 1px solid rgba(244, 63, 94, 0.1);
        border-radius: 12px;
        color: #f43f5e;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
    }

    .optimizing-card {
        background: rgba(0, 0, 0, 0.2);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .opt-title {
        font-size: 11px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        display: block;
    }
    .opt-desc {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.2);
    }

    .manifold-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .footer-divider {
        width: 1px;
        height: 12px;
        background: rgba(255, 255, 255, 0.05);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
