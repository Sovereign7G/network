<script lang="ts">
    export let streak = 0;

    // Generate flame icons based on streak
    $: flames = Math.min(streak, 5); // Max 5 flames
    $: flameArray = Array(flames).fill("🔥");
</script>

<div class="streak-container" class:active={streak > 0}>
    <div class="streak-icon">
        {#each flameArray as flame}
            <span class="flame">{flame}</span>
        {/each}
    </div>
    <div class="streak-info">
        <span class="streak-count">{streak}</span>
        <span class="streak-label">day streak</span>
    </div>
</div>

<style>
    .streak-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 107, 107, 0.1);
        border-radius: 2rem;
        border: 1px solid rgba(255, 107, 107, 0.2);
    }

    .streak-container.active {
        background: rgba(255, 107, 107, 0.15);
        border-color: rgba(255, 107, 107, 0.4);
    }

    .streak-icon {
        display: flex;
        gap: 0.25rem;
    }

    .flame {
        font-size: 1.2rem;
        animation: flicker 2s infinite;
        animation-delay: calc(var(--index) * 0.2s);
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

    .streak-count {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ff6b6b;
        line-height: 1;
    }

    .streak-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }
</style>
