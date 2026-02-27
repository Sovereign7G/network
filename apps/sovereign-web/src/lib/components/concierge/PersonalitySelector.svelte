<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let currentPersonality;
    export let personalities;

    const dispatch = createEventDispatcher();

    let isOpen = false;
</script>

<div class="personality-selector">
    <button class="selector-button" onclick={() => (isOpen = !isOpen)}>
        <span class="current-icon"
            >{personalities[currentPersonality?.toUpperCase()]?.icon ||
                "🧙"}</span
        >
        <span class="current-name"
            >{personalities[currentPersonality?.toUpperCase()]?.name ||
                "The Sage"}</span
        >
        <span class="dropdown-arrow">{isOpen ? "▲" : "▼"}</span>
    </button>

    {#if isOpen}
        <div class="dropdown-menu">
            {#each Object.values(personalities) as personality}
                <button
                    class="personality-option"
                    class:active={personality.id === currentPersonality}
                    onclick={() => {
                        dispatch("change", personality.id);
                        isOpen = false;
                    }}
                >
                    <span class="option-icon">{personality.icon}</span>
                    <div class="option-info">
                        <span class="option-name">{personality.name}</span>
                        <span class="option-desc"
                            >{personality.description}</span
                        >
                    </div>
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .personality-selector {
        position: relative;
    }

    .selector-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .selector-button:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .current-icon {
        font-size: 1.2rem;
    }

    .current-name {
        font-size: 0.9rem;
    }

    .dropdown-arrow {
        font-size: 0.7rem;
        opacity: 0.7;
    }

    .dropdown-menu {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 0.5rem;
        background: #1a1a1a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 0.5rem;
        min-width: 200px;
        z-index: 100;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .personality-option {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem;
        background: none;
        border: none;
        color: white;
        text-align: left;
        cursor: pointer;
        border-radius: 0.5rem;
        transition: all 0.2s;
    }

    .personality-option:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .personality-option.active {
        background: rgba(147, 112, 219, 0.2);
    }

    .option-icon {
        font-size: 1.5rem;
    }

    .option-info {
        flex: 1;
    }

    .option-name {
        display: block;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .option-desc {
        display: block;
        font-size: 0.7rem;
        opacity: 0.5;
    }
</style>
