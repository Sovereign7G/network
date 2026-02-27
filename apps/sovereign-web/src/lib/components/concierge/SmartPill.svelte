<script lang="ts">
    import { fade, fly } from "svelte/transition";
    import { backOut } from "svelte/easing";
    import { X } from "lucide-svelte";
    import { suggestionEngine } from "$lib/engines/suggestion-engine.svelte";
    import { learningEngine } from "$lib/engines/learning-engine.svelte";
    import type { Suggestion } from "$lib/types";

    let { suggestion, ondismiss } = $props<{
        suggestion: Suggestion;
        ondismiss?: () => void;
    }>();

    let visible = $state(true);
    let progress = $state(100);
    let interval: ReturnType<typeof setInterval>;

    $effect(() => {
        if (suggestion.expiresAt) {
            const total =
                suggestion.expiresAt -
                (suggestion.context.data?.createdAt || Date.now());
            interval = setInterval(() => {
                const remaining = suggestion.expiresAt! - Date.now();
                progress = Math.max(0, (remaining / total) * 100);
                if (remaining <= 0) {
                    dismiss();
                }
            }, 100);
        }
        return () => clearInterval(interval);
    });

    function dismiss() {
        visible = false;
        setTimeout(() => {
            if (ondismiss) ondismiss();
            suggestionEngine.dismiss(suggestion.id);
        }, 300);
    }

    function handleAction() {
        learningEngine.trackInteraction({
            suggestionId: suggestion.id,
            type: suggestion.type,
            action: "acted",
            timestamp: Date.now(),
            source: suggestion.context.source,
        });

        if (suggestion.action?.handler) {
            suggestion.action.handler();
            dismiss();
        }
    }
</script>

{#if visible}
    <div
        class="smart-pill {suggestion.type}"
        in:fly={{ x: 20, duration: 500, easing: backOut }}
        out:fade={{ duration: 300 }}
    >
        <div class="pill-glow"></div>
        <div class="pill-content">
            <span class="pill-title">{suggestion.title}</span>
            <button class="pill-action" onclick={handleAction}>
                {suggestion.action?.label || "View"}
            </button>
        </div>

        <button class="pill-close" onclick={dismiss}>
            <X size={10} />
        </button>

        {#if suggestion.expiresAt}
            <div class="pill-progress">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
        {/if}
    </div>
{/if}

<style>
    .smart-pill {
        position: relative;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 12px;
        padding-right: 8px;
        background: rgba(20, 20, 25, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        pointer-events: auto;
        overflow: hidden;
    }

    .pill-glow {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 20% 50%,
            rgba(251, 191, 36, 0.1),
            transparent 70%
        );
        pointer-events: none;
    }

    .pill-content {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .pill-title {
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.9);
        white-space: nowrap;
    }

    .pill-action {
        padding: 2px 10px;
        background: #fbbf24;
        color: black;
        border: none;
        border-radius: 1rem;
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        cursor: pointer;
        transition: transform 0.2s;
    }

    .pill-action:hover {
        transform: scale(1.05);
    }

    .pill-close {
        color: rgba(255, 255, 255, 0.2);
        transition: color 0.2s;
    }

    .pill-close:hover {
        color: #ef4444;
    }

    .pill-progress {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
    }

    .progress-fill {
        height: 100%;
        background: #fbbf24;
        transition: width 0.1s linear;
    }

    /* Types */
    .smart-pill.anomaly-detected {
        border-color: rgba(239, 68, 68, 0.4);
        background: rgba(40, 10, 10, 0.9);
    }

    .smart-pill.anomaly-detected .pill-glow {
        background: radial-gradient(
            circle at 20% 50%,
            rgba(239, 68, 68, 0.2),
            transparent 70%
        );
    }

    .smart-pill.anomaly-detected .pill-action {
        background: #ef4444;
        color: white;
    }
</style>
