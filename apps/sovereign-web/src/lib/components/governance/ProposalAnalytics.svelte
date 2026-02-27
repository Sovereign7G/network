<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import { BarChart, Users, TrendingUp, Cpu, History } from "lucide-svelte";

    interface ProposalPrediction {
        outcome: "PASS" | "FAIL" | "CONTESTED";
        confidence: number;
        factors: string[];
    }

    interface DelegateInfluence {
        id: string;
        name: string;
        votingPower: number;
        alignment: number; // 0-1 scale
    }

    // Mock data for Phase 5 implementation
    const propositionId = "PROP-842";

    const prediction: ProposalPrediction = {
        outcome: "PASS",
        confidence: 0.92,
        factors: [
            "High delegate alignment (+45%)",
            "Low historical contention on budget adjustments",
            "Whale endorsement (0xFD...2A)",
        ],
    };

    const delegates: DelegateInfluence[] = [
        {
            id: "del-1",
            name: "Sovereign Node Alpha",
            votingPower: 450000,
            alignment: 0.95,
        },
        {
            id: "del-2",
            name: "Cathedral Architects",
            votingPower: 320000,
            alignment: 0.82,
        },
        {
            id: "del-3",
            name: "Yield Collective Phase 2",
            votingPower: 180000,
            alignment: 0.45,
        },
    ];

    const distribution = {
        for: 68,
        against: 24,
        abstain: 8,
    };

    function formatPower(power: number) {
        return new Intl.NumberFormat("en-US", {
            notation: "compact",
            maximumFractionDigits: 1,
        }).format(power);
    }
</script>

<div class="analytics-card" in:fade>
    <header class="card-header">
        <div class="header-left">
            <BarChart size={16} class="text-indigo-400" />
            <h3 class="title">Deep Analytics: {propositionId}</h3>
        </div>
        <div class="header-right">
            <span class="badge prediction">AI_PREDICTION_ACTIVE</span>
        </div>
    </header>

    <div class="card-body">
        <!-- AI Prediction -->
        <section class="prediction-section" in:slide={{ delay: 100 }}>
            <div class="pred-header">
                <Cpu size={14} class="text-amber-400" />
                <h4>Outcome Simulation Engine</h4>
            </div>

            <div class="pred-result">
                <div class="outcome-box {prediction.outcome.toLowerCase()}">
                    <span class="label">Projected State</span>
                    <span class="value">{prediction.outcome}</span>
                </div>
                <div class="confidence-box">
                    <span class="label">Borel Confidence</span>
                    <span class="value"
                        >{(prediction.confidence * 100).toFixed(1)}%</span
                    >
                </div>
            </div>

            <div class="factors">
                {#each prediction.factors as factor}
                    <div class="factor-item">
                        <TrendingUp size={10} class="text-emerald-400" />
                        <span>{factor}</span>
                    </div>
                {/each}
            </div>
        </section>

        <!-- Vote Distribution -->
        <section class="distribution-section" in:slide={{ delay: 200 }}>
            <h4 class="section-title">Current Polarization</h4>

            <div class="dist-bar">
                <div
                    class="dist-segment for"
                    style:width="{distribution.for}%"
                ></div>
                <div
                    class="dist-segment against"
                    style:width="{distribution.against}%"
                ></div>
                <div
                    class="dist-segment abstain"
                    style:width="{distribution.abstain}%"
                ></div>
            </div>

            <div class="dist-legend">
                <div class="legend-item">
                    <div class="dot for"></div>
                    For: {distribution.for}%
                </div>
                <div class="legend-item">
                    <div class="dot against"></div>
                    Against: {distribution.against}%
                </div>
                <div class="legend-item">
                    <div class="dot abstain"></div>
                    Abstain: {distribution.abstain}%
                </div>
            </div>
        </section>

        <!-- Delegate Power Mapping -->
        <section class="delegates-section" in:slide={{ delay: 300 }}>
            <div class="section-top">
                <Users size={12} class="text-cyan-400" />
                <h4 class="section-title">Delegate Power Weighting</h4>
            </div>

            <div class="delegates-list">
                {#each delegates as delegate}
                    <div class="delegate-card">
                        <div class="d-info">
                            <span class="d-name">{delegate.name}</span>
                            <span class="d-power"
                                >{formatPower(delegate.votingPower)} SYND</span
                            >
                        </div>
                        <div class="alignment-bar">
                            <div
                                class="align-fill"
                                style:width="{delegate.alignment * 100}%"
                                style:background={delegate.alignment > 0.5
                                    ? "#10b981"
                                    : "#f43f5e"}
                            ></div>
                        </div>
                    </div>
                {/each}
            </div>
        </section>

        <section class="historical-section" in:slide={{ delay: 400 }}>
            <div class="section-top">
                <History size={12} class="text-white/40" />
                <h4 class="section-title">Similar Paradigm Shifts</h4>
            </div>
            <p class="history-context">
                Correlates 82% with PROP-142 (Passed, Epoch 4). Similar economic
                impact and contention velocity observed in initial 24h voting
                period.
            </p>
        </section>
    </div>
</div>

<style>
    .analytics-card {
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

    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
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
        border-radius: 6px;
        letter-spacing: 0.1em;
    }

    .badge.prediction {
        background: rgba(251, 191, 36, 0.1);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.2);
    }

    .card-body {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .section-title {
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }

    .pred-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .pred-header h4 {
        font-size: 10px;
        font-weight: 900;
        color: #fbbf24;
        text-transform: uppercase;
    }

    .pred-result {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .outcome-box,
    .confidence-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .outcome-box.pass .value {
        color: #10b981;
    }
    .outcome-box.fail .value {
        color: #f43f5e;
    }

    .label {
        font-size: 7px;
        font-weight: 800;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
    }

    .value {
        font-size: 16px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .factors {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .factor-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 9px;
        color: rgba(255, 255, 255, 0.6);
        background: rgba(0, 0, 0, 0.2);
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
    }

    .dist-bar {
        height: 8px;
        border-radius: 100px;
        overflow: hidden;
        display: flex;
        margin-bottom: 0.75rem;
    }

    .dist-segment {
        height: 100%;
    }
    .dist-segment.for {
        background: #10b981;
    }
    .dist-segment.against {
        background: #f43f5e;
    }
    .dist-segment.abstain {
        background: rgba(255, 255, 255, 0.2);
    }

    .dist-legend {
        display: flex;
        gap: 1.5rem;
        font-size: 9px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.4);
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }
    .dot.for {
        background: #10b981;
    }
    .dot.against {
        background: #f43f5e;
    }
    .dot.abstain {
        background: rgba(255, 255, 255, 0.2);
    }

    .section-top {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .section-top h4 {
        margin-bottom: 0;
    }

    .delegates-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .delegate-card {
        background: rgba(255, 255, 255, 0.02);
        padding: 0.75rem 1rem;
        border-radius: 10px;
    }

    .d-info {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }

    .d-name {
        font-size: 10px;
        font-weight: 800;
        color: white;
    }
    .d-power {
        font-size: 9px;
        font-weight: 900;
        color: #22d3ee;
        font-family: "JetBrains Mono", monospace;
    }

    .alignment-bar {
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        overflow: hidden;
    }
    .align-fill {
        height: 100%;
    }

    .history-context {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
    }
</style>
