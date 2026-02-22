<script lang="ts">
    export let value = 0;
    export let tier;
    export let progress = 0;
    export let nextTier = null;

    $: formattedValue = new Intl.NumberFormat().format(value);
</script>

<div class="resonance-meter">
    <div class="meter-header">
        <div class="tier-info">
            <span class="tier-icon">{tier?.icon || "✨"}</span>
            <span class="tier-name">{tier?.title || "Spark"}</span>
        </div>
        <span class="resonance-value">{formattedValue}</span>
    </div>

    <div class="meter-bar">
        <div class="meter-fill" style="width: {progress}%;"></div>
    </div>

    {#if nextTier}
        <div class="meter-footer">
            <span class="next-tier">
                Next: {nextTier.title} ({nextTier.threshold - value} resonance needed)
            </span>
        </div>
    {:else}
        <div class="meter-footer">
            <span class="max-tier">Maximum tier reached!</span>
        </div>
    {/if}
</div>

<style>
    .resonance-meter {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
    }

    .meter-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .tier-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tier-icon {
        font-size: 1.2rem;
    }

    .tier-name {
        font-weight: 600;
        color: #9370db;
    }

    .resonance-value {
        font-size: 1.1rem;
        font-weight: 600;
    }

    .meter-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

    .meter-fill {
        height: 100%;
        background: linear-gradient(90deg, #9370db, #ff6b6b);
        border-radius: 4px;
        transition: width 0.3s;
    }

    .meter-footer {
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .next-tier {
        color: #ffd700;
    }

    .max-tier {
        color: #4caf50;
    }
</style>
