<script lang="ts">
    const activities = [
        {
            id: 1,
            type: "tx",
            content: "Sent 10.5 AGE to did:age:8x7f",
            time: "2m ago",
            icon: "🔄",
        },
        {
            id: 2,
            type: "node",
            content: "Node Node-847 joined the mesh",
            time: "15m ago",
            icon: "⚡",
        },
        {
            id: 3,
            type: "vote",
            content: "Voted on Prop #84: Emission Halving",
            time: "1h ago",
            icon: "⚖️",
        },
        {
            id: 4,
            type: "auth",
            content: "Security handshake with Shard 00",
            time: "3h ago",
            icon: "🛡️",
        },
        {
            id: 5,
            type: "wealth",
            content: "Staking rewards: +1.27 AGE",
            time: "5h ago",
            icon: "📈",
        },
    ];
</script>

<div class="activity-feed">
    {#each activities as act}
        <div class="activity-item">
            <div class="activity-icon">{act.icon}</div>
            <div class="activity-body">
                <p class="activity-content">{act.content}</p>
                <span class="activity-time">{act.time}</span>
            </div>
        </div>
    {/each}
</div>

<style>
    .activity-feed {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .activity-item {
        display: flex;
        gap: 1rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        align-items: center;
    }

    .activity-icon {
        font-size: 1.2rem;
        width: 32px;
        text-align: center;
    }

    .activity-body {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .activity-content {
        margin: 0;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
    }

    .activity-time {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
    }
</style>
