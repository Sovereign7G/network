<script lang="ts">
    import { onMount } from "svelte";

    let globalStatus: any = {
        emergencyStopped: false,
        globalDailyLimit: 1000n,
        globalSpentToday: 350n,
    };
    let userAllowances: any[] = [
        { user: "0x123...abc", limit: 2n, attempted: 1n, remaining: 1n },
        { user: "0xabc...123", limit: 5n, attempted: 6n, remaining: 0n },
    ];
    let alerts: any[] = [
        {
            by: "0x999...999",
            reason: "Abnormal LLM spend spike detected",
            timestamp: Date.now() - 3600000,
        },
    ];

    onMount(async () => {
        // Mocked contract logic since we are not connecting live web3 yet
    });

    async function setAllowance() {
        const user = prompt("User address:");
        const limit = prompt("Daily limit (AGE):");
        alert(`Setting allowance for ${user} to ${limit} AGE`);
    }

    async function emergencyStop() {
        const reason = prompt("Reason for emergency stop:");
        globalStatus.emergencyStopped = true;
        alerts = [
            { by: "0xYou...Me", reason, timestamp: Date.now() },
            ...alerts,
        ];
    }

    async function restore() {
        if (confirm("Restore normal operations?")) {
            globalStatus.emergencyStopped = false;
        }
    }
</script>

<div class="circuit-breaker">
    <header>
        <h1>⚡ Emergency Council</h1>
        <p class="subtitle">
            The Circuit Breaker that protects the machine economy
        </p>
    </header>

    <div
        class="status-card {globalStatus?.emergencyStopped
            ? 'emergency'
            : 'normal'}"
    >
        <h2>Global Status</h2>
        <div class="status-value">
            {globalStatus?.emergencyStopped
                ? "🚨 EMERGENCY STOP"
                : "✅ Normal Operations"}
        </div>

        <div class="global-metrics">
            <div>
                <span class="label">Daily Limit</span>
                <div class="value">
                    {globalStatus?.globalDailyLimit?.toString() || 0} AGE
                </div>
            </div>
            <div>
                <span class="label">Spent Today</span>
                <div class="value">
                    {globalStatus?.globalSpentToday?.toString() || 0} AGE
                </div>
            </div>
            <div>
                <span class="label">Remaining</span>
                <div id="cb-rem" class="value" role="group">
                    {(
                        (globalStatus?.globalDailyLimit || 0n) -
                        (globalStatus?.globalSpentToday || 0n)
                    ).toString()} AGE
                </div>
            </div>
        </div>

        <div class="council-actions">
            <button onclick={setAllowance} class="secondary"
                >Set Allowance</button
            >
            <button onclick={emergencyStop} class="danger">🔴 Stop</button>
            <button onclick={restore} class="success">🟢 Restore</button>
        </div>
    </div>

    <div class="recent-alerts">
        <h3>Recent Alerts</h3>
        {#each alerts as alert}
            <div class="alert">
                <span class="time"
                    >{new Date(alert.timestamp).toLocaleTimeString()}</span
                >
                <span class="reason">🚨 {alert.reason}</span>
                <span class="by"
                    >by {alert.by.slice(0, 6)}...{alert.by.slice(-4)}</span
                >
            </div>
        {/each}
    </div>

    <div class="user-allowances">
        <h3>Top Spenders</h3>
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Daily Limit</th>
                    <th>Attempted</th>
                    <th>Remaining</th>
                </tr>
            </thead>
            <tbody>
                {#each userAllowances as ua}
                    <tr>
                        <td>{ua.user}</td>
                        <td>{ua.limit} AGE</td>
                        <td>{ua.attempted} AGE</td>
                        <td>{ua.remaining} AGE</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    .circuit-breaker {
        max-width: 1000px;
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

    .status-card {
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
    }

    .status-card.normal {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
    }

    .status-card.emergency {
        background: linear-gradient(135deg, #b71c1c 0%, #c62828 100%);
    }

    .status-value {
        font-size: 32px;
        font-weight: bold;
        margin: 15px 0;
    }

    .global-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 20px 0;
    }

    .global-metrics div {
        text-align: center;
    }

    .global-metrics .label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .global-metrics .value {
        display: block;
        font-size: 24px;
        font-weight: bold;
        margin-top: 8px;
    }

    .council-actions {
        display: flex;
        gap: 12px;
        margin-top: 24px;
    }

    button {
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
    }

    button.danger {
        background: #ff4444;
        color: white;
    }

    button.success {
        background: #4caf50;
        color: white;
    }

    button.secondary {
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }

    .recent-alerts {
        background: #1e1e1e;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: #fff;
    }

    .alert {
        display: flex;
        gap: 15px;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .alert .time {
        color: #aaa;
        font-size: 13px;
        width: 80px;
    }

    .alert .reason {
        flex: 1;
        color: #fff;
    }

    .alert .by {
        color: #666;
        font-size: 13px;
    }

    .user-allowances {
        background: #1e1e1e;
        padding: 24px;
        border-radius: 12px;
        color: #fff;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
    }

    th {
        text-align: left;
        padding: 12px 10px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        color: #888;
        text-transform: uppercase;
        font-size: 12px;
    }

    td {
        padding: 16px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #ccc;
        font-family: "Menlo", monospace;
        font-size: 14px;
    }
</style>
