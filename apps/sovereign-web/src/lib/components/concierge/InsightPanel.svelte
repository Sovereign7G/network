<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let insights = [];
    const dispatch = createEventDispatcher();

    function getInsightIcon(type) {
        switch (type) {
            case "pattern":
                return "🔍";
            case "opportunity":
                return "💎";
            case "achievement":
                return "🏆";
            case "conversation":
                return "💬";
            default:
                return "💡";
        }
    }

    function getConfidenceColor(confidence) {
        if (confidence >= 0.8) return "#4CAF50";
        if (confidence >= 0.5) return "#FFD700";
        return "#FF6B6B";
    }

    function formatTime(timestamp) {
        if (!timestamp) return "Just now";
        const now = new Date();
        const date = new Date(timestamp);
        const diff = now - date;

        if (diff < 60000) return "Just now";
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }
</script>

<div class="insight-panel">
    {#if insights.length === 0}
        <div class="empty-insights">
            <span class="empty-icon">💭</span>
            <p>No insights yet</p>
        </div>
    {:else}
        {#each insights as insight}
            <div
                class="insight-card"
                style="--confidence-color: {getConfidenceColor(
                    insight.confidence,
                )};"
            >
                <div class="insight-header">
                    <span class="insight-icon"
                        >{getInsightIcon(insight.type)}</span
                    >
                    <span class="insight-time"
                        >{formatTime(insight.timestamp)}</span
                    >
                    <button
                        class="dismiss-btn"
                        on:click={() => dispatch("dismiss", insight.id)}
                        aria-label="Dismiss insight"
                    >
                        ✕
                    </button>
                </div>

                <h4 class="insight-title">{insight.title}</h4>
                <p class="insight-description">{insight.description}</p>

                <div class="insight-footer">
                    <div class="confidence-indicator">
                        <span class="confidence-label">Confidence</span>
                        <div class="confidence-bar">
                            <div
                                class="confidence-fill"
                                style="width: {insight.confidence * 100}%;"
                            ></div>
                        </div>
                    </div>

                    {#if insight.actionable}
                        <button
                            class="action-btn"
                            on:click={() => dispatch("execute", insight.id)}
                        >
                            {insight.action || "Take Action"} →
                        </button>
                    {/if}
                </div>
            </div>
        {/each}
    {/if}
</div>

<style>
    .insight-panel {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .empty-insights {
        text-align: center;
        padding: 2rem;
        opacity: 0.5;
    }

    .empty-icon {
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    .empty-insights p {
        margin: 0;
        font-size: 0.9rem;
    }

    .insight-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.75rem;
        padding: 0.75rem;
        transition: all 0.2s;
    }

    .insight-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: #9370db;
    }

    .insight-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .insight-icon {
        font-size: 1rem;
    }

    .insight-time {
        flex: 1;
        font-size: 0.6rem;
        opacity: 0.5;
    }

    .dismiss-btn {
        width: 1.5rem;
        height: 1.5rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 0.8rem;
    }

    .dismiss-btn:hover {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
    }

    .insight-title {
        margin: 0 0 0.25rem 0;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .insight-description {
        margin: 0 0 0.75rem 0;
        font-size: 0.8rem;
        opacity: 0.7;
        line-height: 1.4;
    }

    .insight-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .confidence-indicator {
        flex: 1;
    }

    .confidence-label {
        display: block;
        font-size: 0.6rem;
        opacity: 0.5;
        margin-bottom: 0.25rem;
    }

    .confidence-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
        width: 80px;
    }

    .confidence-fill {
        height: 100%;
        background: var(--confidence-color);
        transition: width 0.3s;
    }

    .action-btn {
        padding: 0.25rem 0.75rem;
        background: rgba(147, 112, 219, 0.2);
        border: 1px solid #9370db;
        border-radius: 1rem;
        color: #9370db;
        font-size: 0.7rem;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }

    .action-btn:hover {
        background: #9370db;
        color: white;
    }
</style>
