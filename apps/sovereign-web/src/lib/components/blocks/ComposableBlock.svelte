<script lang="ts">
//     import { fly } from "svelte/transition";
    import type { Snippet } from "svelte";
    import BlockAnnotation from "./BlockAnnotation.svelte";

    let {
        type = "text",
        content = {},
        id = crypto.randomUUID(),
        isEditing = $bindable(false),
        ondragstart,
        ondragend,
        oneditstart,
        oneditend,
        tile,
        canvas,
        chart,
        table,
    } = $props<{
        type?: "text" | "tile" | "chart" | "table" | "canvas";
        content?: any;
        id?: string;
        isEditing?: boolean;
        ondragstart?: (data: any) => void;
        ondragend?: (data: any) => void;
        oneditstart?: (data: any) => void;
        oneditend?: (data: any) => void;
        tile?: Snippet<[any]>;
        canvas?: Snippet<[any]>;
        chart?: Snippet<[any]>;
        table?: Snippet<[any]>;
    }>();

    let isDragging = $state(false);
    let showAnnotations = $state(false);

    function handleDragStart(e: DragEvent) {
        isDragging = true;
        e.dataTransfer?.setData("text/plain", id);
        if (ondragstart) ondragstart({ id, type, content });
    }

    function handleDragEnd() {
        isDragging = false;
        if (ondragend) ondragend({ id });
    }

    function handleDoubleClick() {
        isEditing = true;
        if (oneditstart) oneditstart({ id });
    }

    function handleBlur() {
        isEditing = false;
        if (oneditend) oneditend({ id, content });
    }
</script>

<div
    class="composable-block block-{type}"
    class:is-dragging={isDragging}
    class:is-editing={isEditing}
    draggable="true"
    ondragstart={handleDragStart}
    ondragend={handleDragEnd}
    ondblclick={handleDoubleClick}
    onkeydown={(e: KeyboardEvent) => {
        if (e.key === "Enter" && !isEditing) handleDoubleClick();
    }}
    role="button"
    tabindex="0"
    aria-label="Composable block {type}"
    transitionfly={{ y: 10, duration: 200 }}
>
    <!-- Block Toolbar for Annotations -->
    <div
        class="block-toolbar"
        onclick={(e: MouseEvent) => e.stopPropagation()}
        onkeydown={(e: KeyboardEvent) => e.stopPropagation()}
        role="toolbar"
        aria-label="Block tools"
        tabindex="0"
    >
        <button
            class="annotate-btn"
            onclick={() => (showAnnotations = !showAnnotations)}
            title="Annotations"
        >
            💬
        </button>
    </div>

    {#if showAnnotations}
        <BlockAnnotation
            blockId={id}
            onClose={() => (showAnnotations = false)}
        />
    {/if}

    {#if type === "tile"}
        {@render tile?.(content)}
    {:else if type === "canvas"}
        {@render canvas?.(content)}
    {:else if type === "chart"}
        {@render chart?.(content)}
    {:else if type === "table"}
        {@render table?.(content)}
    {:else if isEditing}
        <textarea
            bind:value={content.text}
            class="block-editor"
            onblur={handleBlur}
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

    .block-toolbar {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        z-index: 10;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    .composable-block:hover .block-toolbar {
        opacity: 1;
    }

    .annotate-btn {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 6px;
        color: white;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        font-size: 1rem;
        backdrop-filter: blur(4px);
    }

    .annotate-btn:hover {
        border-color: #ffd700;
        background: rgba(255, 215, 0, 0.2);
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
