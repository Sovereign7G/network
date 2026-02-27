<script lang="ts">
    import { MEMORY_TYPES } from "$lib/stores/constants";

    let { onsubmit, oncancel } = $props();

    let content = $state("");
    let title = $state("");
    let type = $state("gratitude");
    let tags = $state("");
    let error = $state("");

    let typeOptions = $derived(Object.values(MEMORY_TYPES));

    function handleSubmit(e: Event) {
        e.preventDefault();
        if (!content.trim()) {
            error = "Please write something";
            return;
        }

        const tagArray = tags
            .split(",")
            .map((t) => t.trim())
            .filter((t) => t.length > 0)
            .map((t) => t.replace(/^#/, ""));

        if (onsubmit) {
            onsubmit({
                content: content.trim(),
                title: title.trim() || null,
                type,
                tags: tagArray,
            });
        }
    }
</script>

<form class="memory-form" onsubmit={handleSubmit}>
    <div class="form-header">
        <h3 class="form-title">
            <span class="title-icon">✨</span>
            Capture a Memory
        </h3>
        <button
            type="button"
            class="close-btn"
            onclick={() => oncancel && oncancel()}
        >
            ✕
        </button>
    </div>

    <fieldset class="form-group border-none p-0 m-0">
        <legend class="form-label mb-2 text-sm opacity-80">Memory Type</legend>
        <div class="type-selector">
            {#each typeOptions as option}
                <button
                    type="button"
                    class="type-option"
                    class:selected={type === option.id}
                    style="--option-color: {option.color};"
                    onclick={() => (type = option.id)}
                    aria-pressed={type === option.id}
                >
                    <span class="option-icon" aria-hidden="true"
                        >{option.icon}</span
                    >
                    <span class="option-label">{option.label}</span>
                    <span class="option-resonance">+{option.resonance}</span>
                </button>
            {/each}
        </div>
    </fieldset>

    <div class="form-group">
        <label for="memory-title" class="form-label">Title (Optional)</label>
        <input
            type="text"
            id="memory-title"
            class="form-input"
            bind:value={title}
            placeholder="Give your memory a title..."
        />
    </div>

    <div class="form-group">
        <label for="memory-content" class="form-label">
            Memory <span class="required">*</span>
        </label>
        <textarea
            id="memory-content"
            class="form-textarea"
            class:error
            bind:value={content}
            placeholder="What would you like to remember?"
            rows="4"
        ></textarea>
        {#if error}
            <span class="error-message">{error}</span>
        {/if}
    </div>

    <div class="form-group">
        <label for="memory-tags" class="form-label"
            >Tags (Optional, comma-separated)</label
        >
        <input
            type="text"
            id="memory-tags"
            class="form-input"
            bind:value={tags}
            placeholder="gratitude, growth, family, etc."
        />
    </div>

    <div class="form-preview">
        <div class="preview-header">
            <span class="preview-icon">👁️</span>
            <span class="preview-label">Preview</span>
        </div>
        <div
            class="preview-content"
            style="--preview-color: {MEMORY_TYPES[type.toUpperCase()]?.color}"
        >
            <div class="preview-type">
                <span>{MEMORY_TYPES[type.toUpperCase()]?.icon}</span>
                <span>{MEMORY_TYPES[type.toUpperCase()]?.label}</span>
                <span class="preview-resonance"
                    >+{MEMORY_TYPES[type.toUpperCase()]?.resonance}</span
                >
            </div>
            {#if title}
                <strong class="preview-title">{title}</strong>
            {/if}
            <p class="preview-text">
                {content || "Your memory will appear here..."}
            </p>
        </div>
    </div>

    <div class="form-actions">
        <button
            type="button"
            class="cancel-btn"
            onclick={() => oncancel && oncancel()}
        >
            Cancel
        </button>
        <button type="submit" class="submit-btn" disabled={!content.trim()}>
            <span class="btn-icon">✨</span>
            Save to Hearth
        </button>
    </div>
</form>

<style>
    .memory-form {
        background: rgba(20, 20, 20, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }

    .form-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .form-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 1.2rem;
    }

    .title-icon {
        font-size: 1.5rem;
    }

    .close-btn {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        font-size: 1.2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .required {
        color: #ff6b6b;
    }

    .type-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.5rem;
    }

    .type-option {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .type-option:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--option-color);
    }

    .type-option.selected {
        background: var(--option-color);
        border-color: var(--option-color);
        color: white;
    }

    .option-icon {
        font-size: 1.2rem;
    }

    .option-label {
        flex: 1;
        font-size: 0.9rem;
    }

    .option-resonance {
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .type-option.selected .option-resonance {
        opacity: 1;
    }

    .form-input,
    .form-textarea {
        width: 100%;
        box-sizing: border-box;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: inherit;
        transition: all 0.2s;
    }

    .form-input:focus,
    .form-textarea:focus {
        outline: none;
        border-color: #9370db;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
    }

    .form-textarea.error {
        border-color: #ff6b6b;
    }

    .error-message {
        display: block;
        margin-top: 0.25rem;
        color: #ff6b6b;
        font-size: 0.8rem;
    }

    .form-preview {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0.5rem;
    }

    .preview-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .preview-icon {
        font-size: 0.9rem;
        opacity: 0.5;
    }

    .preview-label {
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .preview-content {
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-left: 3px solid var(--preview-color);
        border-radius: 0.5rem;
    }

    .preview-type {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: var(--preview-color);
    }

    .preview-resonance {
        margin-left: auto;
        font-size: 0.8rem;
    }

    .preview-title {
        display: block;
        margin-bottom: 0.25rem;
    }

    .preview-text {
        margin: 0;
        opacity: 0.8;
        font-style: italic;
    }

    .form-actions {
        display: flex;
        gap: 1rem;
    }

    .cancel-btn,
    .submit-btn {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .cancel-btn {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .cancel-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .submit-btn {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .submit-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .submit-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .btn-icon {
        font-size: 1.1rem;
    }

    @media (max-width: 768px) {
        .type-selector {
            grid-template-columns: 1fr;
        }
    }
</style>
