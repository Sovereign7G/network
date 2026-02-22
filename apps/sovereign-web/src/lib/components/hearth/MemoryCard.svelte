<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { MEMORY_TYPES } from "$lib/stores/master-store";

    export let memory;
    export let isExpanded = false;

    const dispatch = createEventDispatcher();

    let showDeleteConfirm = false;
    let reflectionText = "";

    $: memoryType =
        MEMORY_TYPES[memory?.type?.toUpperCase()] || MEMORY_TYPES.GRATITUDE;

    $: formattedDate = memory?.timestamp
        ? new Intl.DateTimeFormat("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
              hour: "2-digit",
              minute: "2-digit",
          }).format(new Date(memory.timestamp))
        : "";

    function handleDelete() {
        if (showDeleteConfirm) {
            dispatch("delete");
            showDeleteConfirm = false;
        } else {
            showDeleteConfirm = true;
            setTimeout(() => (showDeleteConfirm = false), 3000);
        }
    }

    function handleAddReflection() {
        if (reflectionText.trim()) {
            dispatch("reflect", reflectionText.trim());
            reflectionText = "";
        }
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<div
    class="memory-card"
    class:expanded={isExpanded}
    style="--card-color: {memoryType.color}"
    on:click={() => dispatch("click")}
    on:keydown={(e) => e.key === "Enter" && dispatch("click")}
    role="article"
    tabindex="0"
>
    <div class="memory-header">
        <div class="memory-type">
            <span class="type-icon" style="background: {memoryType.color}20;">
                {memoryType.icon}
            </span>
            <div>
                <span class="type-label">{memoryType.label}</span>
                <span class="memory-date">{formattedDate}</span>
            </div>
        </div>

        <div class="memory-actions">
            <span
                class="resonance-badge"
                style="border-color: {memoryType.color};"
            >
                <span class="badge-icon">✨</span>
                +{memory.resonance || memoryType.resonance}
            </span>

            <button
                class="delete-btn"
                class:confirm={showDeleteConfirm}
                on:click|stopPropagation={handleDelete}
                aria-label="Delete memory"
            >
                {showDeleteConfirm ? "✓" : "✕"}
            </button>
        </div>
    </div>

    <div class="memory-body">
        {#if memory.title}
            <h3 class="memory-title">{memory.title}</h3>
        {/if}

        <p class="memory-content">{memory.content}</p>

        {#if memory.tags && memory.tags.length > 0}
            <div class="memory-tags">
                {#each memory.tags as tag}
                    <span class="tag">#{tag}</span>
                {/each}
            </div>
        {/if}
    </div>

    {#if isExpanded}
        <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
        <div class="memory-expanded" on:click|stopPropagation>
            {#if memory.reflections && memory.reflections.length > 0}
                <div class="reflections-section">
                    <h4 class="reflections-title">Reflections</h4>
                    {#each memory.reflections as reflection}
                        <div class="reflection-item">
                            <span class="reflection-icon">💭</span>
                            <div>
                                <p class="reflection-content">
                                    {reflection.content}
                                </p>
                                <span class="reflection-date">
                                    {new Intl.DateTimeFormat("en-US", {
                                        month: "short",
                                        day: "numeric",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    }).format(new Date(reflection.timestamp))}
                                </span>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}

            <div class="add-reflection">
                <input
                    type="text"
                    class="reflection-input"
                    placeholder="Add a reflection..."
                    bind:value={reflectionText}
                    on:keydown={(e) =>
                        e.key === "Enter" && handleAddReflection()}
                />
                <button
                    class="add-reflection-btn"
                    on:click={handleAddReflection}
                    disabled={!reflectionText.trim()}
                >
                    Add
                </button>
            </div>
        </div>
    {/if}

    <div class="memory-footer">
        <span class="expand-hint">
            {isExpanded ? "▼ Click to collapse" : "▶ Click to expand"}
        </span>
    </div>
</div>

<style>
    .memory-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1.25rem;
        transition: all 0.2s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .memory-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: var(--card-color);
        transform: translateY(-2px);
        box-shadow: 0 5px 20px -5px var(--card-color);
    }

    .memory-card.expanded {
        background: rgba(255, 255, 255, 0.04);
        border-color: var(--card-color);
        box-shadow: 0 0 30px -10px var(--card-color);
    }

    .memory-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .memory-type {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .type-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .type-label {
        display: block;
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--card-color);
    }

    .memory-date {
        font-size: 0.7rem;
        opacity: 0.5;
    }

    .memory-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .resonance-badge {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid;
        border-radius: 2rem;
        font-size: 0.8rem;
    }

    .badge-icon {
        font-size: 0.9rem;
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

    .memory-body {
        margin-bottom: 1rem;
    }

    .memory-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }

    .memory-content {
        margin: 0 0 0.75rem 0;
        line-height: 1.6;
        opacity: 0.9;
        white-space: pre-wrap;
    }

    .memory-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .tag {
        padding: 0.2rem 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        font-size: 0.7rem;
        color: var(--card-color);
    }

    .memory-expanded {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .reflections-section {
        margin-bottom: 1rem;
    }

    .reflections-title {
        margin: 0 0 0.75rem 0;
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .reflection-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .reflection-icon {
        font-size: 1rem;
        opacity: 0.5;
    }

    .reflection-content {
        margin: 0 0 0.25rem 0;
        font-size: 0.9rem;
    }

    .reflection-date {
        font-size: 0.6rem;
        opacity: 0.5;
    }

    .add-reflection {
        display: flex;
        gap: 0.5rem;
    }

    .reflection-input {
        flex: 1;
        padding: 0.5rem;
        box-sizing: border-box;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-size: 0.9rem;
    }

    .reflection-input:focus {
        outline: none;
        border-color: var(--card-color);
    }

    .add-reflection-btn {
        padding: 0.5rem 1rem;
        background: var(--card-color);
        border: none;
        border-radius: 0.5rem;
        color: white;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .add-reflection-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 2px 10px var(--card-color);
    }

    .add-reflection-btn:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }

    .memory-footer {
        margin-top: 0.75rem;
        text-align: right;
    }

    .expand-hint {
        font-size: 0.7rem;
        opacity: 0.3;
        transition: opacity 0.2s;
    }

    .memory-card:hover .expand-hint {
        opacity: 0.8;
    }

    .memory-card:focus-visible {
        outline: 2px solid var(--card-color);
        outline-offset: 2px;
    }
</style>
