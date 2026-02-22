<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { flip } from "svelte/animate";
    import ComposableBlock from "./ComposableBlock.svelte";

    export let columns: Array<
        Array<{ id: string; type: string; content: any }>
    > = [];

    const dispatch = createEventDispatcher();
    const flipDurationMs = 200;

    let draggedBlock: any = null;
    let dragSourceColumnIdx: number = -1;

    function handleDragStart(block: any, columnIdx: number) {
        draggedBlock = block;
        dragSourceColumnIdx = columnIdx;
    }

    function handleDrop(columnIdx: number, targetIdx?: number) {
        if (!draggedBlock || dragSourceColumnIdx === -1) return;

        // Remove from source
        columns[dragSourceColumnIdx] = columns[dragSourceColumnIdx].filter(
            (b) => b.id !== draggedBlock.id,
        );

        // Add to destination
        if (targetIdx !== undefined) {
            columns[columnIdx].splice(targetIdx, 0, draggedBlock);
        } else {
            columns[columnIdx].push(draggedBlock);
        }

        columns = [...columns];
        draggedBlock = null;
        dragSourceColumnIdx = -1;
        dispatch("layoutChange", columns);
    }

    function handleDragOver(e: DragEvent) {
        e.preventDefault(); // Necessary to allow dropping
    }

    function addColumn() {
        columns = [...columns, []];
    }
</script>

<div class="workspace-canvas-grid" style="--col-count: {columns.length}">
    {#each columns as column, i}
        <div class="canvas-column">
            <div
                class="drop-zone"
                on:dragover={handleDragOver}
                on:drop={(e) => {
                    e.preventDefault();
                    handleDrop(i);
                }}
            >
                {#each column as block, bIdx (block.id)}
                    <div
                        animate:flip={{ duration: flipDurationMs }}
                        on:dragover|stopPropagation={(e) => {
                            e.preventDefault();
                            e.dataTransfer!.dropEffect = "move";
                        }}
                        on:drop|stopPropagation={(e) => {
                            e.preventDefault();
                            handleDrop(i, bIdx);
                        }}
                    >
                        <ComposableBlock
                            id={block.id}
                            type={block.type as any}
                            content={block.content}
                            on:dragstart={() => handleDragStart(block, i)}
                            on:dragend={() => {
                                draggedBlock = null;
                                dragSourceColumnIdx = -1;
                            }}
                        >
                            <svelte:fragment slot="tile" let:content>
                                <slot name="tile" {content} />
                            </svelte:fragment>
                            <svelte:fragment slot="canvas" let:content>
                                <slot name="canvas" {content} />
                            </svelte:fragment>
                            <svelte:fragment slot="chart" let:content>
                                <slot name="chart" {content} />
                            </svelte:fragment>
                            <svelte:fragment slot="table" let:content>
                                <slot name="table" {content} />
                            </svelte:fragment>
                        </ComposableBlock>
                    </div>
                {/each}
            </div>

            <button
                class="add-block-btn"
                on:click={() => dispatch("addBlock", { columnIndex: i })}
            >
                + Add Block
            </button>
        </div>
    {/each}

    <button class="add-column-btn" on:click={addColumn}> + Add Column </button>
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
