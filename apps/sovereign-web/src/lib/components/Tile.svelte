<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { fly } from "svelte/transition";

    export let tile;
    export let isPinned = false;
    export let isHovered = false;

    const dispatch = createEventDispatcher();

    let showContextMenu = false;
    let contextMenuPosition = { x: 0, y: 0 };

    function handleClick(event) {
        if (!showContextMenu) {
            dispatch("click");
        }
    }

    function handleContextMenu(event) {
        event.preventDefault();
        contextMenuPosition = { x: event.clientX, y: event.clientY };
        showContextMenu = true;

        // Auto-hide after 3 seconds
        setTimeout(() => {
            showContextMenu = false;
        }, 3000);
    }

    function handlePin() {
        dispatch(isPinned ? "unpin" : "pin");
        showContextMenu = false;
    }

    function handleHide() {
        dispatch("hide");
        showContextMenu = false;
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<div
    class="tile"
    class:pinned={isPinned}
    class:hovered={isHovered}
    style="--tile-color: {tile.color}"
    on:click={handleClick}
    on:mouseenter={() => dispatch("hover")}
    on:mouseleave={() => dispatch("leave")}
    on:contextmenu={handleContextMenu}
    role="button"
    tabindex="0"
    aria-label="{tile.title} tile"
    aria-description={tile.description}
    on:keydown={(e) => e.key === "Enter" && dispatch("click")}
>
    <!-- Animated background glow -->
    <div class="tile-glow"></div>

    <!-- Tile content -->
    <div class="tile-content">
        <div class="tile-header">
            <span class="tile-icon" aria-hidden="true">{tile.icon}</span>
            <div class="tile-badges">
                {#if tile.badge}
                    <span class="badge new-badge">{tile.badge}</span>
                {/if}
                {#if isPinned}
                    <span class="badge pin-badge" title="Pinned tile">📌</span>
                {/if}
            </div>
        </div>

        <div class="tile-body">
            <h3 class="tile-title">{tile.title}</h3>
            <p class="tile-description">{tile.description}</p>
        </div>

        <div class="tile-footer">
            <span class="tile-module">{tile.module}</span>
            <span class="tile-hint">Click to enter</span>
        </div>
    </div>

    <!-- Context menu -->
    {#if showContextMenu}
        <div
            class="context-menu"
            style="left: {contextMenuPosition.x}px; top: {contextMenuPosition.y}px;"
            in:fly={{ y: 5, duration: 100 }}
            out:fly={{ y: 5, duration: 100 }}
            on:click|stopPropagation
        >
            <button class="context-item" on:click={handlePin}>
                <span class="context-icon">{isPinned ? "📌" : "📍"}</span>
                <span>{isPinned ? "Unpin tile" : "Pin tile"}</span>
            </button>
            <button class="context-item" on:click={handleHide}>
                <span class="context-icon">👁️</span>
                <span>Hide tile</span>
            </button>
        </div>
    {/if}
</div>

<style>
    .tile {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        backdrop-filter: blur(10px);
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    /* The breathing effect */
    .tile.hovered {
        transform: translateY(-4px) scale(1.02);
        border-color: var(--tile-color);
        box-shadow: 0 10px 30px -10px var(--tile-color);
    }

    .tile.pinned {
        border-width: 2px;
        border-color: var(--tile-color);
        background: rgba(255, 255, 255, 0.05);
    }

    /* Animated glow */
    .tile-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(
            circle at 30% 30%,
            var(--tile-color),
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.5s;
        pointer-events: none;
    }

    .tile.hovered .tile-glow {
        opacity: 0.15;
        animation: breathe 3s infinite;
    }

    @keyframes breathe {
        0%,
        100% {
            opacity: 0.15;
        }
        50% {
            opacity: 0.25;
        }
    }

    .tile-content {
        position: relative;
        z-index: 1;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .tile-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .tile-icon {
        font-size: 2.5rem;
        line-height: 1;
        filter: drop-shadow(0 0 10px var(--tile-color));
        transition: all 0.3s;
    }

    .tile.hovered .tile-icon {
        transform: scale(1.1) rotate(5deg);
    }

    .tile-badges {
        display: flex;
        gap: 0.5rem;
    }

    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.7rem;
        font-weight: 600;
    }

    .new-badge {
        background: #ff6b6b;
        color: white;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }

    .pin-badge {
        background: rgba(255, 255, 255, 0.1);
    }

    .tile-body {
        flex: 1;
    }

    .tile-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
    }

    .tile-description {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.7;
        line-height: 1.5;
    }

    .tile-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .tile-module {
        font-size: 0.8rem;
        padding: 0.25rem 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        color: var(--tile-color);
        text-transform: capitalize;
    }

    .tile-hint {
        font-size: 0.7rem;
        opacity: 0.3;
        transition: opacity 0.2s;
    }

    .tile.hovered .tile-hint {
        opacity: 0.8;
    }

    /* Context menu */
    .context-menu {
        position: fixed;
        z-index: 1000;
        background: rgba(20, 20, 20, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .context-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem 1rem;
        background: none;
        border: none;
        color: white;
        font-size: 0.9rem;
        text-align: left;
        cursor: pointer;
        border-radius: 0.5rem;
        transition: all 0.2s;
        white-space: nowrap;
    }

    .context-item:hover {
        background: rgba(147, 112, 219, 0.2);
    }

    .context-icon {
        font-size: 1rem;
        opacity: 0.7;
    }

    /* Focus styles for accessibility */
    .tile:focus-visible {
        outline: 2px solid #9370db;
        outline-offset: 2px;
    }

    .context-item:focus-visible {
        outline: 2px solid #9370db;
        outline-offset: -2px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .tile {
            padding: 1.25rem;
        }

        .tile-icon {
            font-size: 2rem;
        }

        .tile-title {
            font-size: 1.1rem;
        }

        .tile-description {
            font-size: 0.8rem;
        }
    }
</style>
