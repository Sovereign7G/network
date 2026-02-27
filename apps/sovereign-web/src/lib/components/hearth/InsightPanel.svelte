<script lang="ts">
    export let insights: any[] = [];
</script>

<div class="insight-panel">
    {#each insights as insight}
        <div
            class="insight-item"
            style="--insight-color: {insight.type === 'pattern'
                ? '#4ECDC4'
                : '#FFD700'}"
        >
            <span class="insight-icon">{insight.icon}</span>
            <div>
                <strong class="insight-title">{insight.title}</strong>
                <p class="insight-description">{insight.description}</p>
            </div>
        </div>
    {/each}
</div>

<style>
    .insight-panel {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .insight-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-left: 3px solid var(--insight-color);
        border-radius: 0.5rem;
    }

    .insight-icon {
        font-size: 1.5rem;
    }

    .insight-title {
        display: block;
        margin-bottom: 0.25rem;
        font-size: 0.9rem;
        color: var(--insight-color);
    }

    .insight-description {
        margin: 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }
</style>
