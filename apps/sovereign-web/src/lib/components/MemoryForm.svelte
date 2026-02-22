<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { MEMORY_TYPES } from "$lib/stores/hearth-store";

    export let initialType = MEMORY_TYPES.GRATITUDE.id;

    const dispatch = createEventDispatcher();

    let content = "";
    let title = "";
    let type = initialType;
    let error = "";

    function handleSubmit() {
        if (!content.trim()) {
            error = "Please write something";
            return;
        }

        dispatch("submit", {
            content: content.trim(),
            title: title.trim() || null,
            type,
        });

        // Reset form
        content = "";
        title = "";
        type = MEMORY_TYPES.GRATITUDE.id;
        error = "";
    }

    function handleCancel() {
        dispatch("cancel");
    }
</script>

<form class="memory-form" on:submit|preventDefault={handleSubmit}>
    <div class="form-header">
        <h3>New Memory</h3>
        <button type="button" class="close-btn" on:click={handleCancel}
            >✕</button
        >
    </div>

    <div class="form-group">
        <label for="memory-type">Memory Type</label>
        <select
            id="memory-type"
            bind:value={type}
            class="type-select"
            style="--selected-color: {MEMORY_TYPES[type.toUpperCase()]?.color}"
        >
            {#each Object.values(MEMORY_TYPES) as memoryType}
                <option value={memoryType.id}>
                    {memoryType.icon}
                    {memoryType.label} (+{memoryType.resonance})
                </option>
            {/each}
        </select>
    </div>

    <div class="form-group">
        <label for="memory-title">Title (optional)</label>
        <input
            id="memory-title"
            type="text"
            bind:value={title}
            placeholder="Give your memory a title..."
            class="title-input"
        />
    </div>

    <div class="form-group">
        <label for="memory-content">Memory *</label>
        <textarea
            id="memory-content"
            bind:value={content}
            placeholder="What would you like to remember?"
            rows="4"
            class="content-input"
            class:error
        ></textarea>
        {#if error}
            <span class="error-message">{error}</span>
        {/if}
    </div>

    <div
        class="preview-card"
        style="--type-color: {MEMORY_TYPES[type.toUpperCase()]?.color}"
    >
        <div class="preview-header">
            <span class="preview-icon"
                >{MEMORY_TYPES[type.toUpperCase()]?.icon}</span
            >
            <span class="preview-type"
                >{MEMORY_TYPES[type.toUpperCase()]?.label}</span
            >
            <span class="preview-resonance"
                >+{MEMORY_TYPES[type.toUpperCase()]?.resonance}</span
            >
        </div>
        {#if title}
            <strong class="preview-title">{title}</strong>
        {/if}
        <p class="preview-content">
            {content || "Your memory will appear here..."}
        </p>
    </div>

    <div class="form-actions">
        <button type="button" class="cancel-btn" on:click={handleCancel}>
            Cancel
        </button>
        <button type="submit" class="submit-btn" disabled={!content.trim()}>
            Save to Hearth
        </button>
    </div>
</form>

<style>
    .memory-form {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }

    .form-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .form-header h3 {
        margin: 0;
        color: #9370db;
    }

    .close-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.5rem;
    }

    .close-btn:hover {
        color: white;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .type-select {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 2px solid var(--selected-color, #9370db);
        border-radius: 0.5rem;
        color: white;
        font-size: 1rem;
        cursor: pointer;
    }

    .title-input,
    .content-input {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: inherit;
        resize: vertical;
    }

    .title-input:focus,
    .content-input:focus,
    .type-select:focus {
        outline: none;
        border-color: #9370db;
    }

    .content-input.error {
        border-color: #ff6b6b;
    }

    .error-message {
        display: block;
        margin-top: 0.25rem;
        color: #ff6b6b;
        font-size: 0.8rem;
    }

    .preview-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid var(--type-color);
    }

    .preview-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    .preview-icon {
        font-size: 1.2rem;
    }

    .preview-type {
        font-weight: 600;
        color: var(--type-color);
    }

    .preview-resonance {
        margin-left: auto;
        color: #ffd700;
    }

    .preview-title {
        display: block;
        margin-bottom: 0.25rem;
    }

    .preview-content {
        margin: 0;
        opacity: 0.8;
        font-style: italic;
    }

    .form-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
    }

    .cancel-btn,
    .submit-btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .cancel-btn {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .cancel-btn:hover {
        background: rgba(255, 255, 255, 0.15);
    }

    .submit-btn {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
    }

    .submit-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(147, 112, 219, 0.4);
    }

    .submit-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
