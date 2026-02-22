<script lang="ts">
    import { goto } from "$app/navigation";
    import { fly } from "svelte/transition";

    const DOCK_ITEMS = [
        {
            id: "dashboard",
            icon: "🏠",
            label: "Dashboard",
            route: "/dashboard",
        },
        {
            id: "hearth",
            icon: "🔥",
            label: "Hearth",
            route: "/dashboard/hearth",
        },
        { id: "vault", icon: "💰", label: "Vault", route: "/dashboard/vault" },
        {
            id: "governance",
            icon: "⚖️",
            label: "Council",
            route: "/dashboard/governance",
        },
        { id: "atlas", icon: "🗺️", label: "Atlas", route: "/atlas" },
        {
            id: "command",
            icon: "⌨️",
            label: "Command",
            route: "/dashboard/command",
        },
    ];

    let activeItem = "dashboard";
    let hoveredItem = null;

    function handleClick(route, id) {
        activeItem = id;
        goto(route);
    }
</script>

<div class="dock" in:fly={{ y: 100, duration: 500 }}>
    <div class="dock-content">
        {#each DOCK_ITEMS as item (item.id)}
            <button
                class="dock-item"
                class:active={activeItem === item.id}
                class:hovered={hoveredItem === item.id}
                on:click={() => handleClick(item.route, item.id)}
                on:mouseenter={() => (hoveredItem = item.id)}
                on:mouseleave={() => (hoveredItem = null)}
                aria-label={item.label}
            >
                <span class="dock-icon">{item.icon}</span>
                <span class="dock-label">{item.label}</span>
                {#if hoveredItem === item.id}
                    <span
                        class="dock-tooltip"
                        in:fly={{ y: -5, duration: 100 }}
                    >
                        {item.label}
                    </span>
                {/if}
            </button>
        {/each}
    </div>
</div>

<style>
    .dock {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 3rem;
        padding: 0.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .dock-content {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .dock-item {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.75rem 1.25rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 2rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .dock-item.hovered {
        background: rgba(147, 112, 219, 0.15);
        color: white;
    }

    .dock-item.active {
        background: rgba(147, 112, 219, 0.25);
        color: #9370db;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.3);
    }

    .dock-icon {
        font-size: 1.5rem;
        transition: all 0.2s;
    }

    .dock-item.hovered .dock-icon {
        transform: translateY(-2px);
    }

    .dock-label {
        font-size: 0.7rem;
        margin-top: 0.25rem;
        opacity: 0.7;
    }

    .dock-tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-bottom: 0.5rem;
        padding: 0.25rem 0.75rem;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        font-size: 0.8rem;
        white-space: nowrap;
        pointer-events: none;
    }

    @media (max-width: 768px) {
        .dock {
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            transform: none;
            border-radius: 2rem;
        }

        .dock-content {
            justify-content: space-around;
        }

        .dock-item {
            padding: 0.5rem;
        }

        .dock-label {
            display: none;
        }

        .dock-icon {
            font-size: 1.2rem;
        }
    }
</style>
