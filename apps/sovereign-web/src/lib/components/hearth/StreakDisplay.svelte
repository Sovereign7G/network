<script lang="ts">
    export let streak = 0;

    $: flames = Math.min(streak, 7);
    $: flameArray = Array(flames).fill("🔥");
</script>

<div class="streak-display" class:active={streak > 0}>
    <div class="streak-flames">
        {#each flameArray as flame, i}
            <span class="flame" style="animation-delay: {i * 0.1}s;">
                {flame}
            </span>
        {/each}
    </div>

    <div class="streak-info">
        <span class="streak-number">{streak}</span>
        <span class="streak-label">day streak</span>
    </div>

    {#if streak >= 7}
        <div class="streak-bonus">
            <span class="bonus-icon">✨</span>
            <span>Bonus active!</span>
        </div>
    {/if}
</div>

<style>
    .streak-display {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 2rem;
        transition: all 0.3s;
    }

    .streak-display.active {
        background: rgba(255, 107, 107, 0.15);
        border-color: #ff6b6b;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.2);
    }

    .streak-flames {
        display: flex;
        gap: 0.25rem;
    }

    .flame {
        font-size: 1.2rem;
        animation: flicker 2s infinite;
    }

    @keyframes flicker {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.8;
            transform: scale(1.1);
        }
    }

    .streak-info {
        display: flex;
        align-items: baseline;
        gap: 0.25rem;
    }

    .streak-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ff6b6b;
        line-height: 1;
    }

    .streak-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .streak-bonus {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.5rem;
        background: rgba(255, 215, 0, 0.2);
        border-radius: 1rem;
        font-size: 0.8rem;
        color: #ffd700;
    }

    .bonus-icon {
        font-size: 0.9rem;
    }
</style>
