<script lang="ts">
    import { onMount } from "svelte";

    let workspace;
    let nodes = [
        { id: 1, x: 100, y: 100, label: "Intent", active: true },
        { id: 2, x: 300, y: 150, label: "Logic Gate", active: false },
        { id: 3, x: 500, y: 100, label: "Execution", active: false },
    ];
    let connections = [
        { from: 1, to: 2 },
        { from: 2, to: 3 },
    ];

    let draggingNode = null;

    function handleDrag(e, node) {
        if (!draggingNode) return;

        // grid snapping
        const grid = 20;
        const x =
            Math.round(
                (e.clientX - workspace.getBoundingClientRect().left) / grid,
            ) * grid;
        const y =
            Math.round(
                (e.clientY - workspace.getBoundingClientRect().top) / grid,
            ) * grid;

        // subtle magnetic feedback could go here via a store/event

        const idx = nodes.findIndex((n) => n.id === node.id);
        nodes[idx] = { ...node, x, y };
    }
</script>

<div class="compose-workspace" bind:this={workspace} role="application">
    <svg class="connections" width="100%" height="100%">
        {#each connections as conn}
            {@const fromNode = nodes.find((n) => n.id === conn.from)}
            {@const toNode = nodes.find((n) => n.id === conn.to)}
            <line
                class="flow-line"
                class:active={fromNode.active}
                x1={fromNode.x + 50}
                y1={fromNode.y + 25}
                x2={toNode.x + 50}
                y2={toNode.y + 25}
            />
        {/each}
    </svg>

    {#each nodes as node}
        <div
            class="node {node.active ? 'active-glow' : ''}"
            style="transform: translate({node.x}px, {node.y}px)"
            on:mousedown={() => (draggingNode = node)}
            on:mousemove={(e) => {
                if (draggingNode?.id === node.id) handleDrag(e, node);
            }}
            on:mouseup={() => (draggingNode = null)}
            role="button"
            tabindex="0"
        >
            {node.label}
        </div>
    {/each}
</div>

<style>
    .compose-workspace {
        position: relative;
        width: 100%;
        height: 500px;
        background: #111;
        background-image: radial-gradient(
            rgba(255, 255, 255, 0.1) 1px,
            transparent 1px
        );
        background-size: 20px 20px;
        border-radius: 12px;
        overflow: hidden;
    }

    .connections {
        position: absolute;
        inset: 0;
        pointer-events: none;
    }

    .flow-line {
        stroke: rgba(255, 255, 255, 0.2);
        stroke-width: 2;
    }

    .flow-line.active {
        stroke: #9c27b0;
        stroke-dasharray: 10;
        animation: dash-flow 1s linear infinite;
        filter: drop-shadow(0 0 5px #9c27b0);
    }

    @keyframes dash-flow {
        to {
            stroke-dashoffset: -20;
        }
    }

    .node {
        position: absolute;
        width: 100px;
        height: 50px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        cursor: grab;
        user-select: none;
        transition:
            transform 0.1s,
            box-shadow 0.3s;
    }

    .node:active {
        cursor: grabbing;
    }

    .active-glow {
        box-shadow: 0 0 15px rgba(33, 150, 243, 0.6);
        border-color: #2196f3;
        animation: node-pulse 2s infinite;
    }

    @keyframes node-pulse {
        0%,
        100% {
            filter: brightness(1);
        }
        50% {
            filter: brightness(1.3);
        }
    }
</style>
