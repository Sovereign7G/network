<script lang="ts">
    import { toolStore } from "$lib/stores/tool-store";
    import CalculatorTool from "./CalculatorTool.svelte";
    import ConverterTool from "./ConverterTool.svelte";
    import ZkProofTool from "./ZkProofTool.svelte";
    import MultiSigTool from "./MultiSigTool.svelte";
    import TimeLockTool from "./TimeLockTool.svelte";
    import RecoveryTool from "./RecoveryTool.svelte";
    import { fade, fly } from "svelte/transition";

    let activeTool: any;

    toolStore.subscribe((state) => {
        activeTool = state.activeTool;
    });

    function closePanel() {
        toolStore.deactivateTool();
    }
</script>

{#if activeTool}
    <div
        class="tool-panel-overlay"
        on:click={closePanel}
        transition:fade={{ duration: 200 }}
    >
        <div
            class="tool-panel"
            on:click|stopPropagation
            transition:fly={{ x: -20, duration: 200 }}
        >
            <div class="tool-header">
                <span class="tool-icon">{activeTool.icon}</span>
                <h3>{activeTool.name}</h3>
                <button class="close-btn" on:click={closePanel}>×</button>
            </div>

            <div class="tool-content">
                {#if activeTool.action === "calculator"}
                    <CalculatorTool />
                {:else if activeTool.action === "converter"}
                    <ConverterTool />
                {:else if activeTool.action === "zk-proof"}
                    <ZkProofTool />
                {:else if activeTool.action === "multi-sig"}
                    <MultiSigTool />
                {:else if activeTool.action === "time-lock"}
                    <TimeLockTool />
                {:else if activeTool.action === "recovery"}
                    <RecoveryTool />
                {:else}
                    <div class="tool-placeholder">
                        <p>Tool coming soon: {activeTool.name}</p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}

<style>
    .tool-panel-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 300px; /* Offset for nav */
        z-index: 1000;
    }

    .tool-panel {
        width: 400px;
        max-width: 90vw;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .tool-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1.5rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .tool-icon {
        font-size: 1.5rem;
    }

    .tool-header h3 {
        flex: 1;
        margin: 0;
        color: white;
    }

    .close-btn {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 50%;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .close-btn:hover {
        background: #ffd700;
        color: #0a0a0f;
    }

    .tool-content {
        padding: 1.5rem;
    }

    .tool-placeholder {
        padding: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        border: 1px dashed rgba(255, 255, 255, 0.1);
    }

    @media (max-width: 768px) {
        .tool-panel-overlay {
            padding-left: 0;
            justify-content: center;
        }
    }
</style>
