<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let value: string;
    export let type: "text" | "number" | "date" = "text";
    export let placeholder = "";

    const dispatch = createEventDispatcher();

    let isEditing = false;
    let editValue = value;
    let inputElement: HTMLElement;

    function startEditing() {
        isEditing = true;
        editValue = value;
        setTimeout(() => inputElement?.focus(), 50);
    }

    function saveEdit() {
        isEditing = false;
        if (editValue !== value) {
            value = editValue;
            dispatch("change", { value: editValue });
        }
    }

    function handleKeyDown(e: KeyboardEvent) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            saveEdit();
        }
        if (e.key === "Escape") {
            isEditing = false;
            editValue = value;
        }
    }
</script>

{#if isEditing}
    {#if type === "text"}
        <textarea
            bind:this={inputElement}
            bind:value={editValue}
            onblur={saveEdit}
            onkeydown={handleKeyDown}
            class="inline-editor"
            {placeholder}
        ></textarea>
    {:else if type === "number"}
        <input
            bind:this={inputElement}
            type="number"
            bind:value={editValue}
            onblur={saveEdit}
            onkeydown={handleKeyDown}
            class="inline-editor"
        />
    {:else}
        <input
            bind:this={inputElement}
            type="text"
            bind:value={editValue}
            onblur={saveEdit}
            onkeydown={handleKeyDown}
            class="inline-editor"
            {placeholder}
        />
    {/if}
{:else}
    <span
        class="inline-display"
        ondblclick={startEditing}
        title="Double-click to edit"
    >
        {value || placeholder || "—"}
        <span class="edit-icon">✎</span>
    </span>
{/if}

<style>
    .inline-display {
        position: relative;
        cursor: pointer;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        transition: all 0.2s ease;
    }

    .inline-display:hover {
        background: rgba(255, 215, 0, 0.1);
    }

    .inline-display:hover .edit-icon {
        opacity: 1;
    }

    .edit-icon {
        position: absolute;
        top: -0.5rem;
        right: -0.5rem;
        font-size: 0.8rem;
        color: #ffd700;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    .inline-editor {
        width: 100%;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #ffd700;
        border-radius: 4px;
        color: white;
        padding: 0.2rem 0.5rem;
        font-family: inherit;
        font-size: inherit;
    }

    .inline-editor:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
    }
</style>
