<script lang="ts">
    export let activities: any[] = [];


    function getActivityIcon(type) {
        switch (type) {
            case "vote":
                return "🗳️";
            case "proposal":
                return "📝";
            case "delegate":
                return "🤝";
            default:
                return "📌";
        }
    }

    function formatTime(timestamp) {

        const now = new Date();
        const diff = now - timestamp;

        if (diff < 60000) return "Just now";
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return timestamp.toLocaleDateString();
    }
</script>

<div class="activity-feed">
    {#each activities as activity}
        <div class="activity-item">
            <span class="activity-icon">{getActivityIcon(activity.type)}</span>

            <div class="activity-content">
                <p class="activity-text">
                    <span class="activity-user">{activity.user}</span>
                    {activity.action}
                </p>
                <div class="activity-footer">
                    <span class="activity-time"
                        >{formatTime(activity.timestamp)}</span
                    >
                    {#if activity.resonance}
                        <span class="activity-resonance"
                            >✨ +{activity.resonance}</span
                        >
                    {/if}
                </div>
            </div>
        </div>
    {/each}
</div>

<style>
    .activity-feed {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .activity-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0.5rem;
        transition: all 0.2s;
    }

    .activity-item:hover {
        background: rgba(255, 255, 255, 0.04);
    }

    .activity-icon {
        font-size: 1.2rem;
    }

    .activity-content {
        flex: 1;
    }

    .activity-text {
        margin: 0 0 0.25rem 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    .activity-user {
        font-weight: 600;
        color: #9370db;
    }

    .activity-footer {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
    }

    .activity-time {
        opacity: 0.5;
    }

    .activity-resonance {
        color: #ffd700;
    }
</style>
