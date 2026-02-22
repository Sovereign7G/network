<script lang="ts">
    export let resonance = 0;

    // Animation for resonance changes
    import { onMount } from "svelte";

    let displayResonance = resonance;
    let previousResonance = resonance;

    onMount(() => {
        const interval = setInterval(() => {
            if (displayResonance < resonance) {
                displayResonance = Math.min(displayResonance + 1, resonance);
            } else if (displayResonance > resonance) {
                displayResonance = Math.max(displayResonance - 1, resonance);
            }
        }, 20);

        return () => clearInterval(interval);
    });

    $: if (resonance !== previousResonance) {
        previousResonance = resonance;
    }
</script>

<div class="resonance-container">
    <span class="resonance-icon">✨</span>
    <div class="resonance-info">
        <span class="resonance-label">Resonance</span>
        <span class="resonance-value">{displayResonance}</span>
    </div>
</div>

<style>
    .resonance-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(147, 112, 219, 0.1);
        border-radius: 2rem;
        border: 1px solid rgba(147, 112, 219, 0.2);
    }

    .resonance-icon {
        font-size: 1.2rem;
        animation: spin 4s linear infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .resonance-info {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }

    .resonance-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .resonance-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #9370db;
        line-height: 1;
    }
</style>
