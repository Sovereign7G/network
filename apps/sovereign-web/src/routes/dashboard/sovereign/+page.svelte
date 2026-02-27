<script lang="ts">
//     import { onMount } from "svelte";

    // Mocking the charts structure for the UI placeholder
    const dashboard = {
        summary: { netWorth: 18.5, dailyNet: 0.85, projectedNet: 35.0 },
        earnings: { total: 20.0, today: 1.05, topAsset: "Search History" },
        spending: { total: 1.5, today: 0.2, topAPI: "OpenAI GPT-4" },
        intelligence: {
            successRate: 0.95,
            bountiesSolved: 12,
            averageBounty: 0.5,
        },
        sovereignty: {
            conversionRate: 0.15,
            dataRequests: 200,
            averageDataPrice: 0.05,
        },
        topInsights: [
            {
                type: "positive",
                message:
                    "🔥 Data sales are up 50% today! Your search history is valuable.",
            },
            {
                type: "info",
                message:
                    "Your AI spent $0.20 on LLMs today. It's getting smarter.",
            },
        ],
        alerts: [],
    };
</script>

<div class="dashboard">
    <header>
        <h1>🏛️ Sovereign Dashboard</h1>
        <p class="subtitle">Your digital commonwealth, quantified</p>
    </header>

    <div class="net-worth-card">
        <h2>Net Sovereign Worth</h2>
        <div class="net-worth-value">
            ${dashboard.summary.netWorth.toFixed(2)}
            <span
                class="trend {dashboard.summary.dailyNet > 0
                    ? 'positive'
                    : 'negative'}"
            >
                {dashboard.summary.dailyNet > 0 ? "▲" : "▼"} ${Math.abs(
                    dashboard.summary.dailyNet,
                ).toFixed(2)} today
            </span>
        </div>
        <div class="projected">
            Projected: ${dashboard.summary.projectedNet.toFixed(2)}/month
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card earnings">
            <h3>💰 Earnings</h3>
            <div class="metric-value">
                ${dashboard.earnings.total.toFixed(2)}
            </div>
            <div class="metric-detail">
                Today: ${dashboard.earnings.today.toFixed(2)}
            </div>
            <div class="metric-detail">
                Top Asset: {dashboard.earnings.topAsset}
            </div>
        </div>

        <div class="metric-card spending">
            <h3>⚡ Spending</h3>
            <div class="metric-value">
                ${dashboard.spending.total.toFixed(2)}
            </div>
            <div class="metric-detail">
                Today: ${dashboard.spending.today.toFixed(2)}
            </div>
            <div class="metric-detail">
                Top API: {dashboard.spending.topAPI}
            </div>
        </div>

        <div class="metric-card intelligence">
            <h3>🧠 Intelligence</h3>
            <div class="metric-value">
                {(dashboard.intelligence.successRate * 100).toFixed(0)}%
            </div>
            <div class="metric-detail">
                {dashboard.intelligence.bountiesSolved} solved
            </div>
            <div class="metric-detail">
                Avg: ${dashboard.intelligence.averageBounty.toFixed(2)}
            </div>
        </div>

        <div class="metric-card sovereignty">
            <h3>🛡️ Sovereignty</h3>
            <div class="metric-value">
                {(dashboard.sovereignty.conversionRate * 100).toFixed(0)}%
            </div>
            <div class="metric-detail">
                {dashboard.sovereignty.dataRequests} requests
            </div>
            <div class="metric-detail">
                ${dashboard.sovereignty.averageDataPrice.toFixed(2)}/query
            </div>
        </div>
    </div>

    <div class="insights">
        <h3>🔮 Insights</h3>
        {#each dashboard.topInsights as insight}
            <div class="insight {insight.type}">
                {insight.message}
            </div>
        {/each}
    </div>
</div>

<style>
    .dashboard {
        max-width: 1200px;
        margin: 40px auto;
        padding: 20px;
        font-family: "Inter", sans-serif;
    }

    header {
        margin-bottom: 24px;
    }
    h1 {
        margin: 0;
        color: #fff;
    }
    .subtitle {
        color: #888;
        margin-top: 4px;
    }

    .net-worth-card {
        background: linear-gradient(135deg, #111 0%, #1a1a1a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
    }

    .net-worth-card h2 {
        margin: 0 0 16px 0;
        font-size: 16px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .net-worth-value {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
        color: #fff;
    }

    .trend {
        font-size: 18px;
        margin-left: 15px;
    }

    .trend.positive {
        color: #a5d6a5;
    }
    .trend.negative {
        color: #ffcdd2;
    }
    .projected {
        color: rgba(255, 255, 255, 0.4);
        font-size: 14px;
        margin-top: 8px;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    .metric-card {
        background: #111;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .metric-card h3 {
        margin: 0 0 16px 0;
        color: #aaa;
        font-size: 15px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
        font-family: "Menlo", monospace;
    }

    .metric-detail {
        color: #666;
        font-size: 13px;
        margin-top: 4px;
    }

    .earnings .metric-value {
        color: #4caf50;
    }
    .spending .metric-value {
        color: #ff6b6b;
    }
    .intelligence .metric-value {
        color: #2196f3;
    }
    .sovereignty .metric-value {
        color: #9c27b0;
    }

    .insights {
        background: #111;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 30px;
    }

    .insights h3 {
        margin: 0 0 20px 0;
        color: #fff;
    }

    .insight {
        padding: 16px;
        margin: 12px 0;
        border-radius: 8px;
        font-weight: 500;
    }

    .insight.positive {
        background: rgba(76, 175, 80, 0.1);
        color: #4caf50;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    .insight.info {
        background: rgba(33, 150, 243, 0.1);
        color: #2196f3;
        border: 1px solid rgba(33, 150, 243, 0.3);
    }
    .insight.warning {
        background: rgba(255, 170, 0, 0.1);
        color: #ffaa00;
        border: 1px solid rgba(255, 170, 0, 0.3);
    }
</style>
