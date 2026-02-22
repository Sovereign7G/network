<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { fly } from "svelte/transition";

    export let type: "text" | "tile" | "chart" | "table" | "canvas" = "text";
    export let content: any = {};
    export let id = crypto.randomUUID();
    export let isEditing = false;

    const dispatch = createEventDispatcher();

    let isDragging = false;
    let dragOffset = { x: 0, y: 0 };

    function handleDragStart(e) {
        isDragging = true;
        const rect = e.target.getBoundingClientRect();
        dragOffset = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        };
        e.dataTransfer.setData("text/plain", id);
        dispatch("dragstart", { id, type, content });
    }

    function handleDragEnd() {
        isDragging = false;
        dispatch("dragend", { id });
    }

    function handleDoubleClick() {
        isEditing = true;
        dispatch("editstart", { id });
    }

    function handleBlur() {
        isEditing = false;
        dispatch("editend", { id, content });
    }
</script>

<div
    class="composable-block block-{type}"
    class:is-dragging={isDragging}
    class:is-editing={isEditing}
    draggable="true"
    on:dragstart={handleDragStart}
    on:dragend={handleDragEnd}
    on:dblclick={handleDoubleClick}
    transition:fly={{ y: 10, duration: 200 }}
>
    {#if type === "tile"}
        <slot name="tile" {content} />
    {:else if type === "canvas"}
        <slot name="canvas" {content} />
    {:else if type === "chart"}
        <slot name="chart" {content} />
    {:else if type === "table"}
        <slot name="table" {content} />
    {:else if isEditing}
        <textarea
            bind:value={content.text}
            class="block-editor"
            autofocus
            on:blur={handleBlur}
            placeholder="Type something..."
        ></textarea>
    {:else}
        <div class="block-content">
            {content.text || "Empty block"}
        </div>
    {/if}
</div>

<style>
    .composable-block {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: grab;
        position: relative;
    }

    .composable-block:hover {
        background: rgba(255, 215, 0, 0.05);
    }

    .composable-block.is-dragging {
        opacity: 0.5;
        cursor: grabbing;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .composable-block.is-editing {
        cursor: text;
        background: rgba(255, 215, 0, 0.1);
    }

    .block-editor {
        width: 100%;
        min-height: 100px;
        background: transparent;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 8px;
        color: white;
        padding: 1rem;
        font-family: inherit;
        font-size: 1rem;
        resize: vertical;
    }

    .block-editor:focus {
        outline: none;
        border-color: #ffd700;
    }

    .block-content {
        min-height: 2rem;
    }

    .block-canvas {
        min-height: 400px;
    }
</style>
