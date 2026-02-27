<script lang="ts">
    import { fade, slide } from "svelte/transition";

    let { blockId, comments = $bindable([]), onClose } = $props();

    let newComment = $state("");

    function submitComment() {
        if (!newComment.trim()) return;
        comments = [
            ...comments,
            {
                id: crypto.randomUUID(),
                author: "@sovereign_citizen",
                text: newComment,
                time: "Just now",
            },
        ];
        newComment = "";
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submitComment();
        }
    }
</script>

<div
    class="annotation-panel"
    in:slide={{ duration: 250 }}
    out:slide={{ duration: 250 }}
>
    <div class="panel-header">
        <div class="title-with-icon">
            <span class="icon">🏷️</span>
            <h4>Block Annotations</h4>
        </div>
        <button class="close-btn" onclick={onClose}>×</button>
    </div>

    <div class="comments-list">
        {#if comments.length === 0}
            <div class="empty-state">
                No annotations yet. Start the discussion.
            </div>
        {/if}

        {#each comments as comment (comment.id)}
            <div class="comment-item" in:fade>
                <div class="comment-header">
                    <span class="author">{comment.author}</span>
                    <span class="time">{comment.time}</span>
                </div>
                <p class="text">{comment.text}</p>
            </div>
        {/each}
    </div>

    <div class="input-area">
        <textarea
            bind:value={newComment}
            placeholder="Type @ to mention..."
            onkeydown={handleKeydown}
        ></textarea>
        <div class="actions">
            <button class="tool-btn" title="Bookmark">🔖</button>
            <button class="tool-btn" title="Highlight">🖍️</button>
            <button
                class="submit-btn"
                onclick={submitComment}
                disabled={!newComment.trim()}
            >
                Send
            </button>
        </div>
    </div>
</div>

<style>
    .annotation-panel {
        position: absolute;
        top: 1rem;
        right: -320px;
        width: 300px;
        background: rgba(15, 15, 20, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        z-index: 50;
        max-height: 400px;
        overflow: hidden;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
    }

    .title-with-icon {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    h4 {
        margin: 0;
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .close-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
    }

    .close-btn:hover {
        color: #ffd700;
    }

    .comments-list {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .empty-state {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.85rem;
        padding: 2rem 0;
    }

    .comment-item {
        background: rgba(0, 0, 0, 0.2);
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 2px solid #ffd700;
    }

    .comment-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
    }

    .author {
        color: #ffd700;
        font-size: 0.8rem;
        font-weight: bold;
    }

    .time {
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.7rem;
    }

    .text {
        margin: 0;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.85rem;
        line-height: 1.4;
    }

    .input-area {
        padding: 1rem;
        border-top: 1px solid rgba(255, 215, 0, 0.1);
        background: rgba(0, 0, 0, 0.2);
    }

    textarea {
        width: 100%;
        height: 60px;
        padding: 0.5rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        color: white;
        resize: none;
        font-family: inherit;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        box-sizing: border-box;
    }

    textarea:focus {
        outline: none;
        border-color: #ffd700;
    }

    .actions {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .tool-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.6);
        cursor: pointer;
        font-size: 1rem;
        padding: 0.25rem;
        border-radius: 4px;
        transition: all 0.2s;
    }

    .tool-btn:hover {
        background: rgba(255, 215, 0, 0.1);
    }

    .submit-btn {
        margin-left: auto;
        background: #ffd700;
        color: #0a0a0f;
        border: none;
        padding: 0.4rem 1rem;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.8rem;
        cursor: pointer;
    }

    .submit-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
