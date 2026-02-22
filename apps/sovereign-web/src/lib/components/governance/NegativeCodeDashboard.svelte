<script lang="ts">
    import { onMount } from "svelte";

    let codeBurns = [];
    let totalLinesBurned = 0;
    let totalRewardsPaid = 0;

    onMount(async () => {
        // Mock the contract data load
        codeBurns = [
            {
                developer: "0x123...abc",
                linesDeleted: 1450,
                reward: 14500,
                impact: "🔥🔥🔥",
            },
            {
                developer: "0xdef...789",
                linesDeleted: 350,
                reward: 3500,
                impact: "🔥",
            },
            {
                developer: "0xabc...123",
                linesDeleted: 55,
                reward: 550,
                impact: "✨",
            },
        ];

        totalLinesBurned = codeBurns.reduce(
            (sum, b) => sum + b.linesDeleted,
            0,
        );
        totalRewardsPaid = codeBurns.reduce((sum, b) => sum + b.reward, 0);
    });

    async function proposeCodeBurn() {
        const repo = prompt("Repository: (e.g., age-mobile)");
        const linesDeleted = prompt("Lines deleted (net):");
        const description = prompt("Description of the simplification:");

        // Simulate creating a Council Proposal from the Negative Code Treasury
        alert(`Proposal created! Burned ${linesDeleted} lines in ${repo}.`);
    }
</script>

<div class="dashboard">
    <h1>🔥 Negative Code Treasury</h1>

    <div class="stats">
        <div class="stat-card">
            <h3>Total Lines Burned</h3>
            <p class="stat">{totalLinesBurned.toLocaleString()}</p>
            <p class="sub">Lines of complexity eliminated</p>
        </div>

        <div class="stat-card">
            <h3>Rewards Paid</h3>
            <p class="stat">{totalRewardsPaid} AGE</p>
            <p class="sub">{totalRewardsPaid * 0.5} USD @ $0.50</p>
        </div>

        <div class="stat-card">
            <h3>Intent Density</h3>
            <p class="stat">∞</p>
            <p class="sub">Lines of code per intent → 0</p>
        </div>
    </div>

    <div class="leaderboard">
        <h2>🏆 Code Burners Leaderboard</h2>

        <table>
            <thead>
                <tr>
                    <th>Developer</th>
                    <th>Lines Burned</th>
                    <th>Reward</th>
                    <th>Impact</th>
                </tr>
            </thead>
            <tbody>
                {#each codeBurns as burn}
                    <tr>
                        <td>{burn.developer}</td>
                        <td>{burn.linesDeleted}</td>
                        <td>{burn.reward} AGE</td>
                        <td>
                            <span class="impact">
                                {burn.impact}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <div class="propose">
        <button on:click={proposeCodeBurn} class="primary">
            🔥 Propose Code Burn
        </button>
        <p class="hint">
            Get paid to delete code. The Cathedral rewards simplicity.
        </p>
    </div>

    <div class="philosophy">
        <h2>📜 The Anti-Complexity Manifesto</h2>
        <blockquote>
            "The best code is the code that never existed. The second best is
            the code that was deleted. The worst is the code that was written
            but never deleted."
        </blockquote>

        <div class="metrics">
            <h3>Why Lines of Code is a Lie</h3>
            <ul>
                <li>❌ 50,000 lines could be 50,000 bugs</li>
                <li>❌ 50,000 lines could be 50,000 lines of copy-paste</li>
                <li>
                    ❌ 50,000 lines could be 50,000 lines of AI-generated
                    garbage
                </li>
                <li>✅ 5,000 lines that work = INFINITE value</li>
            </ul>
        </div>
    </div>
</div>

<style>
    .dashboard {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        color: white;
        font-family: "Inter", sans-serif;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 30px 0;
    }

    .stat-card {
        background: linear-gradient(135deg, #111 0%, #222 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
    }

    .stat {
        font-size: 36px;
        font-weight: bold;
        color: #ff6b6b;
        margin: 10px 0;
    }

    .sub {
        font-size: 13px;
        opacity: 0.6;
    }

    .leaderboard {
        background: #111;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin: 30px 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
    }

    th {
        text-align: left;
        padding: 12px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.5);
    }

    td {
        padding: 16px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .impact {
        font-size: 20px;
    }

    .propose {
        text-align: center;
        margin: 40px 0;
    }

    button.primary {
        background: #ff6b6b;
        color: white;
        border: none;
        padding: 16px 32px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.2s all;
    }

    button.primary:hover {
        background: #ff5252;
        transform: translateY(-2px);
    }

    .hint {
        color: rgba(255, 255, 255, 0.5);
        margin-top: 12px;
    }

    .philosophy {
        background: rgba(255, 107, 107, 0.05);
        border: 1px solid rgba(255, 107, 107, 0.2);
        padding: 30px;
        border-radius: 12px;
        margin: 40px 0;
    }

    blockquote {
        font-style: italic;
        font-size: 18px;
        color: #ff6b6b;
        border-left: 4px solid #ff6b6b;
        padding-left: 20px;
        margin: 20px 0;
        line-height: 1.5;
    }

    .metrics {
        margin-top: 24px;
    }

    .metrics ul {
        list-style: none;
        padding: 0;
    }

    .metrics li {
        margin: 10px 0;
        font-size: 16px;
        opacity: 0.8;
    }
</style>
