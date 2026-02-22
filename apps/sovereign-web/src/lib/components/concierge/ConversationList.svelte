<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { Conversation } from "$lib/types";

    export let conversations: Conversation[];
    export let currentId: string | null;

    const dispatch = createEventDispatcher<{
        select: string;
        delete: string;
    }>();

    let deletingId: string | null = null;

    function formatDate(timestamp: Date): string {
        const now = new Date();
        const date = new Date(timestamp);

        if (date.toDateString() === now.toDateString()) {
            return new Intl.DateTimeFormat("en-US", {
                hour: "2-digit",
                minute: "2-digit",
            }).format(date);
        }

        if (date.getFullYear() === now.getFullYear()) {
            return new Intl.DateTimeFormat("en-US", {
                month: "short",
                day: "numeric",
            }).format(date);
        }

        return new Intl.DateTimeFormat("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric",
        }).format(date);
    }

    function handleDelete(id: string, event: MouseEvent): void {
        event.stopPropagation();

        if (deletingId === id) {
            dispatch("delete", id);
            deletingId = null;
        } else {
            deletingId = id;
            setTimeout(() => (deletingId = null), 3000);
        }
    }
</script>

<div class="conversation-list">
    {#each conversations as conv (conv.id)}
        <div
            class="conversation-item"
            class:active={conv.id === currentId}
            class:deleting={conv.id === deletingId}
        >
            <button
                class="conversation-content"
                on:click={() => dispatch("select", conv.id)}
            >
                <span class="conv-icon">💬</span>
                <div class="conv-info">
                    <span class="conv-title">{conv.title}</span>
                    <span class="conv-preview">{conv.lastMessage}</span>
                </div>
                <span class="conv-time">{formatDate(conv.timestamp)}</span>
            </button>

            {#if conv.id === currentId}
                <button
                    class="delete-btn"
                    class:confirm={conv.id === deletingId}
                    on:click={(e) => handleDelete(conv.id, e)}
                    aria-label="Delete conversation"
                >
                    {deletingId === conv.id ? "✓" : "✕"}
                </button>
            {/if}
        </div>
    {/each}
</div>

<style>
    .conversation-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .conversation-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-radius: 0.5rem;
        transition: all 0.2s;
    }

    .conversation-item.active {
        background: rgba(147, 112, 219, 0.1);
    }

    .conversation-item.deleting {
        background: rgba(255, 107, 107, 0.1);
    }

    .conversation-content {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        text-align: left;
        border-radius: 0.5rem;
    }

    .conversation-content:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .conv-icon {
        font-size: 1.2rem;
    }

    .conv-info {
        flex: 1;
        min-width: 0;
    }

    .conv-title {
        display: block;
        font-size: 0.9rem;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .conv-preview {
        display: block;
        font-size: 0.7rem;
        opacity: 0.5;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .conv-time {
        font-size: 0.6rem;
        opacity: 0.3;
        white-space: nowrap;
    }

    .delete-btn {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.3);
        cursor: pointer;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
        margin-right: 0.5rem;
    }

    .delete-btn:hover {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
    }

    .delete-btn.confirm {
        background: #ff6b6b;
        color: white;
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
</style>
