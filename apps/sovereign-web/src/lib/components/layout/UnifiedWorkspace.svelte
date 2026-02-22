<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";

    // Workspace state - remembers last view per domain
    let workspaceState = {};

    onMount(() => {
        // Load saved workspace state
        const saved = localStorage.getItem("workspace-state");
        if (saved) workspaceState = JSON.parse(saved);
    });

    function saveWorkspaceState() {
        localStorage.setItem("workspace-state", JSON.stringify(workspaceState));
    }

    // Breadcrumb navigation (like Notion's path)
    $: breadcrumbs = $page.url.pathname.split("/").filter(Boolean);

    function handleCommandOpen() {
        // Dispatch an event to open the command palette
        const event = new CustomEvent("command:open", {
            detail: { prompt: "/" },
        });
        document.dispatchEvent(event);
    }

    function handleCommandWith(prompt: string) {
        const event = new CustomEvent("command:open", { detail: { prompt } });
        document.dispatchEvent(event);
    }
</script>

<div class="unified-workspace">
    <!-- Floating header - minimal, like Notion -->
    <header class="workspace-header">
        <div class="breadcrumbs">
            <span class="crumb">
                <button class="crumb-link" on:click={() => goto("/dashboard")}>
                    🏛️ AGE
                </button>
            </span>
            {#each breadcrumbs as crumb, i}
                <span class="crumb">
                    <span class="separator">/</span>
                    <button
                        class="crumb-link"
                        on:click={() =>
                            goto("/" + breadcrumbs.slice(0, i + 1).join("/"))}
                    >
                        {crumb}
                    </button>
                </span>
            {/each}
        </div>

        <div class="workspace-actions">
            <button
                class="icon-button"
                title="Search"
                on:click={handleCommandOpen}
            >
                <span class="icon">🔍</span>
            </button>
            <button
                class="icon-button"
                title="Settings"
                on:click={() => goto("/settings")}
            >
                <span class="icon">⚙️</span>
            </button>
        </div>
    </header>

    <!-- Main canvas - content flows continuously -->
    <main class="workspace-canvas">
        <slot />
    </main>

    <!-- Floating action button (like Notion's +) -->
    <button
        class="floating-action-button"
        on:click={() => handleCommandWith("/")}
    >
        <span class="fab-icon">+</span>
    </button>
</div>

<style>
    .unified-workspace {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        background: #0a0a0f;
        color: white;
        position: relative;
        width: 100%;
    }

    .workspace-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 2rem;
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .breadcrumbs {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }

    .crumb-link {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        transition: all 0.2s ease;
        text-transform: capitalize;
    }

    .crumb-link:hover {
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
    }

    .separator {
        margin: 0 0.25rem;
        color: rgba(255, 255, 255, 0.3);
    }

    .workspace-actions {
        display: flex;
        gap: 0.5rem;
    }

    .icon-button {
        width: 36px;
        height: 36px;
        background: transparent;
        border: none;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon-button:hover {
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
    }

    .workspace-canvas {
        flex: 1;
        overflow-y: auto;
        width: 100%;
    }

    .floating-action-button {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 56px;
        height: 56px;
        background: #ffd700;
        border: none;
        border-radius: 50%;
        color: #0a0a0f;
        font-size: 2rem;
        font-weight: 300;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .floating-action-button:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.4);
    }

    .fab-icon {
        line-height: 1;
    }
</style>
