<script lang="ts">
    let { tile, value = undefined, loading = false, onclick } = $props();

    let isHovered = $state(false);
    let isPressed = $state(false);
    let pulseScale = $state(1);

    let pulseInterval: ReturnType<typeof setInterval> | null = null;

    $effect(() => {
        if (isHovered) {
            if (!pulseInterval) {
                pulseInterval = setInterval(() => {
                    pulseScale = pulseScale === 1 ? 1.02 : 1;
                }, 1000);
            }
        } else {
            if (pulseInterval) {
                clearInterval(pulseInterval);
                pulseInterval = null;
                pulseScale = 1;
            }
        }
        return () => {
            if (pulseInterval) {
                clearInterval(pulseInterval);
                pulseInterval = null;
            }
        };
    });
</script>

<!-- svelte-ignore a11y-mouse-events-have-key-events a11y-no-noninteractive-element-interactions a11y-click-events-have-key-events -->
<div
    class="tile"
    style="--tile-color: {tile.color}; --tile-color-rgb: {tile.colorRgb ||
        '147, 112, 219'}; transform: scale({isPressed
        ? 0.98
        : isHovered
          ? 1.02
          : pulseScale});"
    class:hovered={isHovered}
    class:pressed={isPressed}
    onmouseenter={() => (isHovered = true)}
    onmouseleave={() => {
        isHovered = false;
        isPressed = false;
    }}
    onmousedown={() => (isPressed = true)}
    onmouseup={() => {
        isPressed = false;
        if (onclick) onclick();
    }}
    onclick={() => onclick && onclick()}
    onkeydown={(e: KeyboardEvent) => {
        if (e.key === "Enter" || e.key === " ") {
            isPressed = true;
            setTimeout(() => {
                isPressed = false;
                if (onclick) onclick();
            }, 100);
        }
    }}
    role="button"
    tabindex="0"
    aria-label={`${tile.title} tile: ${tile.description}`}
>
    <!-- Animated background glow -->
    <div class="tile-glow" class:active={isHovered}></div>

    <!-- Tile content -->
    <div class="tile-content">
        <div class="tile-header">
            <span class="tile-icon" aria-hidden="true">{tile.icon}</span>
            {#if tile.badge}
                <span class="badge new-badge">{tile.badge}</span>
            {/if}
        </div>

        <div class="tile-body">
            <h3 class="tile-title">{tile.title}</h3>
            {#if loading}
                <div class="skeleton-value"></div>
            {:else if value !== undefined}
                <div class="tile-value">{value}</div>
            {/if}
            <p class="tile-description">{tile.description}</p>
        </div>

        <div class="tile-footer">
            <span class="tile-category">{tile.category}</span>
            <span class="tile-hint">Click to enter</span>
        </div>
    </div>
</div>

<style>
    .tile {
        position: relative;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 2rem;
        padding: 2rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow:
            0 8px 32px 0 rgba(0, 0, 0, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.05);
    }

    /* Glass Highlight Overlay */
    .tile::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.05),
            transparent
        );
        transition: 0.5s;
        pointer-events: none;
    }

    .tile.hovered::before {
        left: 100%;
    }

    /* Glass Edge Glow */
    .tile::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 2rem;
        padding: 1px;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.2),
            transparent 40%,
            transparent 60%,
            rgba(var(--tile-color-rgb), 0.3)
        );
        -webkit-mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
        mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
        opacity: 0.5;
        transition: opacity 0.3s;
    }

    .tile.hovered::after {
        opacity: 1;
    }

    .tile.hovered {
        border-color: rgba(255, 255, 255, 0.3);
        box-shadow:
            0 20px 40px rgba(0, 0, 0, 0.2),
            0 0 20px rgba(var(--tile-color-rgb), 0.3),
            inset 0 0 0 1px rgba(255, 255, 255, 0.2);
    }

    .tile.pressed {
        box-shadow:
            0 4px 16px rgba(0, 0, 0, 0.1),
            0 0 30px rgba(var(--tile-color-rgb), 0.5) inset;
    }

    .tile-glow {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle at center,
            var(--tile-color) 0%,
            transparent 50%
        );
        opacity: 0;
        transition: opacity 0.8s cubic-bezier(0.23, 1, 0.32, 1);
        pointer-events: none;
        mix-blend-mode: soft-light;
    }

    .tile-glow.active {
        opacity: 0.2;
        animation: glow-orbit 10s linear infinite;
    }

    @keyframes glow-orbit {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
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

    .tile-body {
        flex: 1;
    }

    .tile-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
    }

    .tile-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--tile-color);
        margin-bottom: 0.5rem;
        font-family: "JetBrains Mono", monospace;
        letter-spacing: -1px;
    }

    .skeleton-value {
        height: 2.5rem;
        width: 80%;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        animation: pulse 2s infinite;
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

    .tile-category {
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

    .tile:focus-visible {
        outline: 2px solid #9370db;
        outline-offset: 2px;
    }
</style>
