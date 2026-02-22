<script lang="ts">
    import UnifiedWorkspace from "./UnifiedWorkspace.svelte";
    import FloatingCommand from "$lib/components/command/FloatingCommand.svelte";
    import VerticalNav from "./VerticalNav.svelte";
    import ToolPanel from "$lib/components/tools/ToolPanel.svelte";

    export let resonance = 98;

    let commandOpen = false;
    let navCollapsed = false;
</script>

<div class="app-layout">
    <UnifiedWorkspace>
        <div class="workspace-layout">
            <VerticalNav bind:collapsed={navCollapsed} />
            <main class="workspace-main">
                <slot />
            </main>
        </div>
    </UnifiedWorkspace>

    <FloatingCommand bind:open={commandOpen} />
    <ToolPanel />
</div>

<style>
    .app-layout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        background: #0a0a0f;
        color: white;
    }

    .workspace-layout {
        display: flex;
        gap: 0;
        flex: 1;
        min-height: 100%;
    }

    .workspace-main {
        flex: 1;
        min-width: 0;
        padding-top: 1rem;
    }

    @media (max-width: 768px) {
        .workspace-layout {
            flex-direction: column;
        }
    }
</style>
