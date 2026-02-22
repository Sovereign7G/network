<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { MEMORY_TYPES } from "$lib/stores/hearth-store";

    export let memory;

    const dispatch = createEventDispatcher();

    const memoryType =
        MEMORY_TYPES[memory.type.toUpperCase()] || MEMORY_TYPES.GRATITUDE;
    const formattedDate = new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(memory.timestamp));

    let showDeleteConfirm = false;

    function handleDelete() {
        if (showDeleteConfirm) {
            dispatch("delete");
            showDeleteConfirm = false;
        } else {
            showDeleteConfirm = true;
            // Auto-hide after 3 seconds
            setTimeout(() => {
                showDeleteConfirm = false;
            }, 3000);
        }
    }
</script>

<div
    class="memory-card"
    style="--card-color: {memoryType.color}"
    class:delete-mode={showDeleteConfirm}
>
    <div class="memory-header">
        <div class="memory-type">
            <span class="type-icon">{memoryType.icon}</span>
            <span class="type-label">{memoryType.label}</span>
        </div>

        <div class="memory-actions">
            <span class="resonance-badge">+{memoryType.resonance}</span>
            <button
                class="delete-btn"
                on:click={handleDelete}
                aria-label="Delete memory"
                class:confirm={showDeleteConfirm}
            >
                {showDeleteConfirm ? "✓ Confirm?" : "✕"}
            </button>
        </div>
    </div>

    {#if memory.title}
        <h3 class="memory-title">{memory.title}</h3>
    {/if}

    <p class="memory-content">{memory.content}</p>

    <div class="memory-footer">
        <span class="memory-date">{formattedDate}</span>
    </div>
</div>

<style>
    .memory-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1.25rem;
        transition: all 0.2s;
        border-left: 4px solid var(--card-color);
    }

    .memory-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(4px);
    }

    .memory-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .memory-type {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .type-icon {
        font-size: 1.2rem;
    }

    .type-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--card-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .memory-actions {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .resonance-badge {
        font-size: 0.8rem;
        padding: 0.25rem 0.5rem;
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 1rem;
        color: #ffd700;
    }

    .delete-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.3);
        font-size: 1rem;
        cursor: pointer;
        padding: 0.25rem;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s;
    }

    .delete-btn:hover {
        color: #ff6b6b;
        background: rgba(255, 107, 107, 0.1);
    }

    .delete-btn.confirm {
        color: white;
        background: #ff6b6b;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }

    .memory-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }

    .memory-content {
        margin: 0 0 0.75rem 0;
        line-height: 1.5;
        opacity: 0.9;
        white-space: pre-wrap;
    }

    .memory-footer {
        display: flex;
        justify-content: flex-end;
    }

    .memory-date {
        font-size: 0.7rem;
        opacity: 0.5;
    }

    .memory-card.delete-mode {
        border-color: #ff6b6b;
        background: rgba(255, 107, 107, 0.05);
    }
</style>
