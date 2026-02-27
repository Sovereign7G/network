<script lang="ts">
    import { Play, Settings2, Save, Database } from "lucide-svelte";
    import { fade, slide } from "svelte/transition";

    let simActive = $state(false);
    let outcomeScore = $state(0);
    let simulationVars = $state({
        budgetMultiplier: 1.0,
        yieldRate: 0.05,
        delegationThreshold: 500000,
    });

    function runSimulation() {
        simActive = true;
        // Simulate ML prediction delay
        outcomeScore = 0;
        setTimeout(() => {
            // Mock dynamic score based on vars
            outcomeScore = Math.min(
                100,
                Math.max(
                    0,
                    75 +
                        simulationVars.budgetMultiplier * 10 -
                        simulationVars.yieldRate * 100,
                ),
            );
        }, 1500);
    }
</script>

<div class="simulator-card">
    <header class="card-header">
        <div class="flex items-center gap-2">
            <Settings2 size={16} class="text-rose-400" />
            <h3 class="title">Borel Stable Simulator</h3>
        </div>
        <span class="badge">SANDBOX_ACTIVE</span>
    </header>

    <div class="card-body">
        <p class="desc">
            Test parameter permutations against real-time mainnet telemetry
            before drafting a formal governance proposal. Runs locally in a
            WebWorker sandbox.
        </p>

        <div class="controls-grid">
            <div class="control-group">
                <div class="c-header">
                    <label for="budget-mul">Treasury Budget Multiplier</label>
                    <span class="val"
                        >{simulationVars.budgetMultiplier.toFixed(2)}x</span
                    >
                </div>
                <input
                    id="budget-mul"
                    type="range"
                    min="0.5"
                    max="2.0"
                    step="0.1"
                    bind:value={simulationVars.budgetMultiplier}
                />
            </div>

            <div class="control-group">
                <div class="c-header">
                    <label for="yield-rate">Base Yield Epoch Rate</label>
                    <span class="val"
                        >{(simulationVars.yieldRate * 100).toFixed(1)}%</span
                    >
                </div>
                <input
                    id="yield-rate"
                    type="range"
                    min="0.01"
                    max="0.15"
                    step="0.01"
                    bind:value={simulationVars.yieldRate}
                />
            </div>

            <div class="control-group">
                <div class="c-header">
                    <label for="delegation-thresh"
                        >Min Delegation Threshold</label
                    >
                    <span class="val"
                        >{simulationVars.delegationThreshold / 1000}k SYND</span
                    >
                </div>
                <input
                    id="delegation-thresh"
                    type="range"
                    min="100000"
                    max="2000000"
                    step="100000"
                    bind:value={simulationVars.delegationThreshold}
                />
            </div>
        </div>

        <div class="action-row">
            <button class="run-btn" onclick={runSimulation}>
                <Play size={14} />
                <span>Execute Simulation</span>
            </button>
            <button class="draft-btn" disabled={!simActive}>
                <Save size={14} />
                <span>Draft Proposal</span>
            </button>
        </div>

        {#if simActive}
            <div class="results-panel" in:slide>
                <div class="res-header">
                    <Database size={12} class="text-cyan-400" />
                    <h4>Simulation Metrics</h4>
                </div>
                {#if outcomeScore === 0}
                    <div class="loading-state">
                        <div class="spinner"></div>
                        <span>Processing Monte Carlo permutations...</span>
                    </div>
                {:else}
                    <div class="res-grid" in:fade>
                        <div class="r-card">
                            <span class="r-label">Pass Probability</span>
                            <span
                                class="r-val"
                                style:color={outcomeScore > 50
                                    ? "#10b981"
                                    : "#f43f5e"}
                                >{outcomeScore.toFixed(1)}%</span
                            >
                        </div>
                        <div class="r-card">
                            <span class="r-label">Network Entropy</span>
                            <span class="r-val text-cyan-400">-12.4%</span>
                        </div>
                        <div class="r-card">
                            <span class="r-label">Yield Impact</span>
                            <span class="r-val text-emerald-400"
                                >+{(
                                    simulationVars.yieldRate *
                                    100 *
                                    1.2
                                ).toFixed(2)}%</span
                            >
                        </div>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .simulator-card {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        overflow: hidden;
        font-family: "Outfit", sans-serif;
    }
    .card-header {
        padding: 1.25rem 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .title {
        font-size: 11px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
    }
    .badge {
        font-size: 7px;
        font-weight: 950;
        padding: 4px 8px;
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.2);
        border-radius: 6px;
        letter-spacing: 0.1em;
    }
    .card-body {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    .desc {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
    }

    .controls-grid {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }

    .control-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .c-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .c-header label {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 0.1em;
    }

    .c-header .val {
        font-size: 10px;
        font-weight: 950;
        color: #22d3ee;
        font-family: "JetBrains Mono", monospace;
    }

    input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        background: transparent;
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        height: 14px;
        width: 14px;
        border-radius: 50%;
        background: #22d3ee;
        cursor: pointer;
        margin-top: -5px;
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
    }

    input[type="range"]::-webkit-slider-runnable-track {
        width: 100%;
        height: 4px;
        cursor: pointer;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
    }

    .action-row {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1rem;
    }

    .run-btn {
        background: #f43f5e;
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 10px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.3s;
    }
    .run-btn:hover {
        background: #e11d48;
        transform: translateY(-2px);
    }

    .draft-btn {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s;
    }
    .draft-btn:not(:disabled) {
        color: white;
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }

    .results-panel {
        background: rgba(34, 211, 238, 0.05);
        border: 1px solid rgba(34, 211, 238, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
    }

    .res-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.25rem;
    }

    .res-header h4 {
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.5);
        letter-spacing: 0.1em;
    }

    .loading-state {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
    }

    .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-top-color: #22d3ee;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .res-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }

    .r-card {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .r-label {
        font-size: 7px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
    }

    .r-val {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
