<script lang="ts">
    import { flip } from "svelte/animate";
    import ComposableBlock from "./ComposableBlock.svelte";
    import type { Snippet } from "svelte";

    let {
        columns = $bindable([]),
        tile,
        canvas,
        chart,
        table,
        onLayoutChange,
        onAddBlock,
    } = $props<{
        columns?: { id: string; blocks: any[] }[];
        tile?: Snippet<[any]>;
        canvas?: Snippet<[any]>;
        chart?: Snippet<[any]>;
        table?: Snippet<[any]>;
        onLayoutChange?: (columns: { id: string; blocks: any[] }[]) => void;
        onAddBlock?: (data: { columnIndex: number }) => void;
    }>();

    const flipDurationMs = 200;

    let draggedBlock = $state(null as any);
    let dragSourceColumnIdx = $state(-1);

    function handleDragStart(block: any, columnIdx: number) {
        draggedBlock = block;
        dragSourceColumnIdx = columnIdx;
    }

    function handleDrop(columnIdx: number, targetIdx?: number) {
        if (!draggedBlock || dragSourceColumnIdx === -1) return;

        // Remove from source
        columns[dragSourceColumnIdx].blocks = columns[
            dragSourceColumnIdx
        ].blocks.filter((b: any) => b.id !== draggedBlock.id);

        // Add to destination
        if (targetIdx !== undefined) {
            columns[columnIdx].blocks.splice(targetIdx, 0, draggedBlock);
        } else {
            columns[columnIdx].blocks.push(draggedBlock);
        }

        columns = [...columns];
        draggedBlock = null;
        dragSourceColumnIdx = -1;
        if (onLayoutChange) onLayoutChange(columns);
    }

    function handleDragOver(e: DragEvent) {
        e.preventDefault(); // Necessary to allow dropping
    }

    function addColumn() {
        columns = [...columns, { id: `col-${Date.now()}`, blocks: [] }];
    }
</script>

<div class="workspace-canvas-grid" style="--col-count: {columns.length}">
    {#each columns as column, i}
        <div class="canvas-column" role="list" aria-label="Workspace column">
            <div
                class="drop-zone"
                role="status"
                aria-label="Empty column drop zone"
                ondragover={handleDragOver}
                ondrop={(e) => {
                    e.preventDefault();
                    handleDrop(i);
                }}
            >
                {#each column.blocks as block, bIdx (block.id)}
                    <div
                        animate:flip={{ duration: flipDurationMs }}
                        ondragover={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            e.dataTransfer!.dropEffect = "move";
                        }}
                        ondrop={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            handleDrop(i, bIdx);
                        }}
                        role="listitem"
                    >
                        <ComposableBlock
                            id={block.id}
                            type={block.type as any}
                            content={block.content}
                            ondragstart={() => handleDragStart(block, i)}
                            ondragend={() => {
                                draggedBlock = null;
                                dragSourceColumnIdx = -1;
                            }}
                            {tile}
                            {canvas}
                            {chart}
                            {table}
                        />
                    </div>
                {/each}
            </div>

            <button
                class="add-block-btn"
                onclick={() => onAddBlock && onAddBlock({ columnIndex: i })}
            >
                + Add Block
            </button>
        </div>
    {/each}

    <button class="add-column-btn" onclick={addColumn}> + Add Column </button>
</div>

<style>
    .workspace-canvas-grid {
        display: grid;
        grid-template-columns: repeat(var(--col-count), 1fr);
        gap: 1.5rem;
        min-height: 60vh;
    }

    .canvas-column {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .drop-zone {
        min-height: 100px;
        height: 100%;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        transition: outline 0.2s ease;
    }

    .add-block-btn,
    .add-column-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        color: rgba(255, 255, 255, 0.5);
        padding: 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
        font-size: 0.9rem;
    }

    .add-block-btn:hover,
    .add-column-btn:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #ffd700;
        color: #ffd700;
    }

    .add-column-btn {
        height: 100%;
        min-height: 200px;
    }

    @media (max-width: 768px) {
        .workspace-canvas-grid {
            grid-template-columns: 1fr;
        }

        .add-column-btn {
            min-height: auto;
            height: 60px;
        }
    }
</style>
