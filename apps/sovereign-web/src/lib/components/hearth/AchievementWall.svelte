<script lang="ts">
    export let achievements = [];
</script>

<div class="achievement-wall">
    {#each achievements as achievement}
        <div
            class="achievement-item"
            class:earned={achievement.earned}
            class:locked={!achievement.earned}
        >
            <div
                class="achievement-icon"
                style="background: {achievement.earned
                    ? '#9370DB20'
                    : 'rgba(255, 255, 255, 0.02)'};"
            >
                <span class="icon">{achievement.icon}</span>
            </div>

            <div class="achievement-info">
                <div class="achievement-header">
                    <span class="achievement-title">{achievement.title}</span>
                    {#if achievement.earned}
                        <span
                            class="earned-badge"
                            title={achievement.earnedAt?.toLocaleDateString()}
                        >
                            ✓ Earned
                        </span>
                    {/if}
                </div>

                <p class="achievement-description">{achievement.description}</p>

                {#if achievement.progress !== undefined && !achievement.earned}
                    <div class="achievement-progress">
                        <div class="progress-bar">
                            <div
                                class="progress-fill"
                                style="width: {Math.min(
                                    100,
                                    (achievement.progress /
                                        achievement.target) *
                                        100,
                                )}%;"
                            ></div>
                        </div>
                        <span class="progress-text">
                            {achievement.progress}/{achievement.target}
                        </span>
                    </div>
                {/if}
            </div>
        </div>
    {/each}
</div>

<style>
    .achievement-wall {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .achievement-item {
        display: flex;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.75rem;
        transition: all 0.2s;
    }

    .achievement-item.earned {
        background: rgba(147, 112, 219, 0.05);
        border-color: #9370db;
    }

    .achievement-item.locked {
        opacity: 0.6;
    }

    .achievement-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .icon {
        font-size: 1.2rem;
    }

    .achievement-info {
        flex: 1;
    }

    .achievement-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.25rem;
    }

    .achievement-title {
        font-weight: 600;
        font-size: 0.9rem;
    }

    .earned-badge {
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        background: #4caf50;
        border-radius: 1rem;
        color: white;
    }

    .achievement-description {
        margin: 0 0 0.5rem 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .achievement-progress {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .progress-bar {
        flex: 1;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #9370db, #ff6b6b);
        transition: width 0.3s;
    }

    .progress-text {
        font-size: 0.7rem;
        color: #9370db;
    }
</style>
