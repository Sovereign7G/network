<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly, scale } from "svelte/transition";
    import { History, Play, Rewind, FastForward, Clock } from "lucide-svelte";

    interface WorkspaceBlock {
        id: string;
        type: string;
        content: Record<string, any>;
    }

    interface WorkspaceColumn {
        id: string;
        blocks: WorkspaceBlock[];
    }

    // 🕒 THE CAUSAL LOOM: Time-travel through mission epochs
    let { onRestore } = $props<{
        onRestore: (columns: WorkspaceColumn[]) => void;
    }>();

    let selectedIndex = $state(0);

    function selectSnapshot(index: number) {
        selectedIndex = index;
        const snap = manifold.causalSnapshots[index];
        if (snap) {
            onRestore(snap.columns as WorkspaceColumn[]);
            manifold.recordEvent(
                "EPOCH_RESTORED",
                `Workspace reverted to: ${snap.label}`,
            );
        }
    }
</script>

{#if manifold.causalSnapshots.length > 0}
    <div class="casual-loom-viewport" transitionfly={{ y: 50, duration: 800 }}>
        <div class="loom-glass"></div>
        <div class="loom-container">
            <header class="loom-header">
                <div class="flex items-center gap-3">
                    <div class="history-shell">
                        <History size={14} class="text-cyan-400" />
                    </div>
                    <div class="flex flex-col">
                        <span class="loom-title"
                            >Causal_Loom // Epoch_Scrubber</span
                        >
                        <div class="flex items-center gap-2">
                            <span class="loom-epoch">CURRENT: 8.42_STABLE</span>
                            <div class="epoch-pulsar"></div>
                        </div>
                    </div>
                </div>

                <div class="loom-controls">
                    <button class="ctrl-btn"><Rewind size={14} /></button>
                    <button class="ctrl-btn primary"
                        ><Play size={16} fill="currentColor" /></button
                    >
                    <button class="ctrl-btn"><FastForward size={14} /></button>
                </div>
            </header>

            <!-- Scrubber Area -->
            <div class="scrubber-pit">
                <div class="scrubber-line"></div>
                <div class="scrubber-track">
                    {#each manifold.causalSnapshots as snap, i}
                        <button
                            class="snapshot-node group"
                            class:active={i === selectedIndex}
                            onclick={() => selectSnapshot(i)}
                        >
                            <div class="node-dot"></div>
                            <div class="node-glow"></div>

                            <!-- Detailed Tooltip -->
                            <div class="node-tooltip">
                                <span class="t-label">EPOCH_SNAP</span>
                                <span class="t-value">{snap.label}</span>
                                <div class="t-meta">
                                    <Clock size={8} />
                                    <span>T+ {i * 15}m</span>
                                </div>
                            </div>

                            {#if i === selectedIndex}
                                <div class="active-tag" in:scale>LOCKED</div>
                            {/if}
                        </button>
                    {/each}
                </div>
            </div>

            <footer class="loom-footer">
                <div class="f-item">
                    <span class="f-label">AMBIENT_MOOD</span>
                    <span class="f-value text-purple-400"
                        >{manifold.ambientMood}</span
                    >
                </div>
                <div class="f-divider"></div>
                <div class="f-item">
                    <span class="f-label">CAUSAL_ENTROPY</span>
                    <span class="f-value text-rose-400"
                        >{(100 - manifold.resonance).toFixed(2)}%</span
                    >
                </div>
            </footer>
        </div>
    </div>
{/if}

<style>
    .casual-loom-viewport {
        position: fixed;
        bottom: 2.5rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 100%;
        max-width: 600px;
        font-family: "Outfit", sans-serif;
    }

    .loom-glass {
        position: absolute;
        inset: 0;
        background: rgba(10, 5, 20, 0.4);
        backdrop-filter: blur(60px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        box-shadow: 0 32px 64px rgba(0, 0, 0, 0.6);
        pointer-events: none;
    }

    .loom-container {
        position: relative;
        padding: 1.75rem;
    }

    .loom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .history-shell {
        width: 36px;
        height: 36px;
        background: rgba(34, 211, 238, 0.05);
        border: 1px solid rgba(34, 211, 238, 0.1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .loom-title {
        font-size: 10px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .loom-epoch {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    .epoch-pulsar {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    .loom-controls {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .ctrl-btn {
        border: none;
        background: transparent;
        color: rgba(255, 255, 255, 0.3);
        cursor: pointer;
        transition: all 0.3s;
    }
    .ctrl-btn:hover {
        color: white;
        transform: scale(1.1);
    }
    .ctrl-btn.primary {
        color: #22d3ee;
        filter: drop-shadow(0 0 8px rgba(34, 211, 238, 0.4));
    }

    .scrubber-pit {
        position: relative;
        height: 60px;
        display: flex;
        align-items: center;
        padding: 0 2rem;
    }

    .scrubber-line {
        position: absolute;
        left: 2rem;
        right: 2rem;
        height: 1px;
        background: linear-gradient(
            to right,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
    }

    .scrubber-track {
        display: flex;
        justify-content: space-between;
        width: 100%;
        position: relative;
        z-index: 10;
    }

    .snapshot-node {
        position: relative;
        width: 24px;
        height: 24px;
        background: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .node-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .node-glow {
        position: absolute;
        inset: -4px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(34, 211, 238, 0.2),
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.4s;
    }

    .snapshot-node:hover .node-dot {
        background: white;
        transform: scale(1.5);
    }
    .snapshot-node:hover .node-glow {
        opacity: 1;
    }

    .snapshot-node.active .node-dot {
        background: #22d3ee;
        transform: scale(2);
        box-shadow: 0 0 15px rgba(34, 211, 238, 0.6);
    }

    .node-tooltip {
        position: absolute;
        bottom: 150%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1rem;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        gap: 2px;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .snapshot-node:hover .node-tooltip {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }

    .t-label {
        font-size: 6px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
    }
    .t-value {
        font-size: 10px;
        font-weight: 950;
        color: white;
        white-space: nowrap;
    }
    .t-meta {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 7px;
        color: #22d3ee;
        margin-top: 4px;
    }

    .active-tag {
        position: absolute;
        top: 150%;
        left: 50%;
        transform: translateX(-50%);
        font-size: 7px;
        font-weight: 950;
        color: #22d3ee;
        letter-spacing: 0.1em;
        animation: pulse 2s infinite;
    }

    .loom-footer {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .f-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .f-label {
        font-size: 6px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
    }
    .f-value {
        font-size: 9px;
        font-weight: 950;
    }
    .f-divider {
        width: 1px;
        height: 16px;
        background: rgba(255, 255, 255, 0.05);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1) translateX(-50%);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1) translateX(-50%);
        }
    }
</style>
