<script lang="ts">
    import { onMount } from "svelte";

    let burningOpportunities: any[] = [];
    let totalBurnableLines = 0;
    let totalPotentialReward = 0;

    onMount(async () => {
        // Mocking the complexity scanner output for the dashboard
        const scan = {
            opportunities: [
                {
                    path: "packages/age-bridge/src/index.ts",
                    repo: "age-core",
                    lines: 1800,
                    currentDensity: 0.1,
                    targetDensity: 0.9,
                    simplificationStrategy:
                        "Collapse 25 bridge router adapters into a single mathematical invariant router interface.",
                    severity: "critical",
                },
                {
                    path: "packages/age-types/src/qr-parsers.ts",
                    repo: "age-types",
                    lines: 1400,
                    currentDensity: 0.2,
                    targetDensity: 0.85,
                    simplificationStrategy:
                        "Deprecate 5 distinct QR parsers. Replace with a single URI regex parser yielding polymorphic Intent structs.",
                    severity: "high",
                },
                {
                    path: "packages/age-concierge/prompts/",
                    repo: "age-ai",
                    lines: 2970,
                    currentDensity: 0.05,
                    targetDensity: 0.95,
                    simplificationStrategy:
                        "Destroy 30 separate text files. Create one dynamic meta-prompt that composes actions contextually.",
                    severity: "critical",
                },
                {
                    path: "age-mobile/src/components/common/",
                    repo: "age-mobile",
                    lines: 4000,
                    currentDensity: 0.3,
                    targetDensity: 0.8,
                    simplificationStrategy:
                        "Consolidate 40 separate React Native layout components into 12 primitive Cathedral composition blocks.",
                    severity: "high",
                },
            ],
            totalLines: 10170,
        };

        burningOpportunities = scan.opportunities;
        totalBurnableLines = scan.totalLines;
        totalPotentialReward = scan.totalLines * 10; // 10 AGE per line
    });

    async function proposeBurn(opportunity: any) {
        // Abstracting execution to Council Proposal
        alert(
            `Initiating Negative Code Burn Proposal:\n\nTarget: ${opportunity.path}\nExpected Burn: ${opportunity.lines} Lines\nReward: ${opportunity.lines * 10} AGE`,
        );
    }

    function showDetails(opportunity: any) {
        alert(
            `Current Density: ${opportunity.currentDensity}\nStrategy: ${opportunity.simplificationStrategy}`,
        );
    }
</script>

<div class="burn-dashboard">
    <header class="burn-header">
        <h1>🔥 The Great Simplification</h1>
        <div class="burn-stats">
            <div class="stat">
                <label>Burnable Lines</label>
                <value>{totalBurnableLines.toLocaleString()}</value>
            </div>
            <div class="stat">
                <label>Potential Reward</label>
                <value>{totalPotentialReward.toLocaleString()} AGE</value>
            </div>
            <div class="stat">
                <label>Density Gain</label>
                <value>+{(totalBurnableLines / 1000).toFixed(1)}x</value>
            </div>
        </div>
    </header>

    <div class="opportunities">
        {#each burningOpportunities as opp}
            <div
                class="opportunity-card"
                style="border-left-color: {opp.severity === 'critical'
                    ? '#ff4444'
                    : '#ffaa00'}"
            >
                <div class="card-header">
                    <h3>{opp.path}</h3>
                    <span class="lines">{opp.lines} lines</span>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <label>Current Density</label>
                        <div
                            class="value {opp.currentDensity < 0.3
                                ? 'bad'
                                : opp.currentDensity < 0.7
                                  ? 'ok'
                                  : 'good'}"
                        >
                            {opp.currentDensity.toFixed(2)}
                        </div>
                    </div>
                    <div class="metric">
                        <label>Target Density</label>
                        <div class="value good">
                            {opp.targetDensity.toFixed(2)}
                        </div>
                    </div>
                    <div class="metric">
                        <label>Potential Reward</label>
                        <div class="value">{opp.lines * 10} AGE</div>
                    </div>
                </div>

                <div class="strategy">
                    <strong>🔥 Burn Strategy:</strong>
                    <p>{opp.simplificationStrategy}</p>
                </div>

                <div class="actions">
                    <button on:click={() => proposeBurn(opp)} class="burn">
                        🔥 Propose Burn
                    </button>
                    <button on:click={() => showDetails(opp)} class="inspect">
                        🔍 Inspect
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .burn-dashboard {
        max-width: 1200px;
        margin: 40px auto;
        padding: 20px;
        font-family: "Inter", sans-serif;
    }

    .burn-header {
        background: linear-gradient(135deg, #111 0%, #2a0808 100%);
        border: 1px solid #ff4444;
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
    }

    h1 {
        margin-top: 0;
        color: #ff6b6b;
    }

    .burn-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 20px;
    }

    .stat {
        text-align: center;
        background: rgba(0, 0, 0, 0.5);
        padding: 16px;
        border-radius: 8px;
    }

    .stat label {
        font-size: 14px;
        opacity: 0.9;
        color: #ff8e8e;
    }

    .stat value {
        display: block;
        font-size: 32px;
        font-weight: bold;
        margin-top: 8px;
    }

    .opportunities {
        display: grid;
        gap: 20px;
    }

    .opportunity-card {
        background: #1a1a1a;
        color: white;
        border-left: 6px solid;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .card-header h3 {
        margin: 0;
        font-family: "Menlo", monospace;
        font-size: 16px;
        color: #ccc;
    }

    .lines {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }

    .metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 20px;
        padding: 20px;
        background: #111;
        border-radius: 8px;
    }

    .metric {
        text-align: center;
    }

    .metric label {
        font-size: 13px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric .value {
        display: block;
        font-size: 20px;
        font-weight: bold;
        margin-top: 8px;
    }

    .bad {
        color: #ff4444;
    }
    .ok {
        color: #ffaa00;
    }
    .good {
        color: #00c851;
    }

    .strategy {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 15px;
        line-height: 1.5;
        color: #ddd;
    }

    .strategy strong {
        color: #ff8e8e;
    }

    .actions {
        display: flex;
        gap: 12px;
    }

    .burn {
        background: #ff4444;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
        transition: 0.2s all;
    }

    .burn:hover {
        background: #ff0000;
        transform: translateY(-2px);
    }

    .inspect {
        background: #333;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: 0.2s all;
    }

    .inspect:hover {
        background: #444;
    }
</style>
