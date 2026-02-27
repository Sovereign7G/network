<script lang="ts">
    export let stats = {};
</script>

<div class="governance-stats">
    <div class="stat-card">
        <span class="stat-icon">📊</span>
        <div>
            <span class="stat-label">Total Proposals</span>

            <span class="stat-value">{stats.totalProposals || 0}</span>
        </div>
    </div>

    <div class="stat-card">
        <span class="stat-icon">🗳️</span>
        <div>
            <span class="stat-label">Active</span>
            <span class="stat-value">{stats.activeProposals || 0}</span>

        </div>
    </div>

    <div class="stat-card">
        <span class="stat-icon">✅</span>
        <div>
            <span class="stat-label">Pass Rate</span>
            <span class="stat-value">{stats.passRate || 0}%</span>
        </div>

    </div>

    <div class="stat-card">
        <span class="stat-icon">👥</span>
        <div>
            <span class="stat-label">Voters</span>
            <span class="stat-value">{stats.totalVoters || 0}</span>
        </div>

    </div>
</div>

<style>
    .governance-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
    }

    .stat-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        transition: all 0.2s;
    }

    .stat-card:hover {
        background: rgba(147, 112, 219, 0.05);
        border-color: #9370db;
    }

    .stat-icon {
        font-size: 2rem;
    }

    .stat-label {
        display: block;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .stat-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #9370db;
    }
</style>
