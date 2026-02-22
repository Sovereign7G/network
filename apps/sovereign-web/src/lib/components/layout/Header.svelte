<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { createEventDispatcher } from "svelte";

    export let resonance = 98;

    const dispatch = createEventDispatcher();

    let showUserMenu = false;

    const userMenuItems = [
        { name: "Profile", path: "/profile", icon: "👤" },
        { name: "Settings", path: "/settings", icon: "⚙️" },
        { name: "Command", path: "/command", icon: "⌨️" },
        { name: "Help", path: "/help", icon: "❓" },
        { name: "Logout", path: "/logout", icon: "🚪", action: "logout" },
    ];

    function navigate(path: string) {
        goto(path);
        showUserMenu = false;
    }

    function openCommand() {
        dispatch("command");
        showUserMenu = false;
    }
</script>

<header class="main-header">
    <div class="header-left">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
            class="logo-area"
            on:click={() => navigate("/dashboard")}
            title="Go to Dashboard"
        >
            <span class="logo-icon">🏛️</span>
            <span class="logo-text">AGE Protocol</span>
        </div>

        <div class="breadcrumbs">
            <span class="crumb">{$page.url.pathname}</span>
        </div>
    </div>

    <div class="header-right">
        <div class="resonance-indicator" title="Global System Resonance Score">
            <span class="resonance-label">Resonance</span>
            <span class="resonance-value">{resonance}%</span>
            <div class="resonance-bar">
                <div class="resonance-fill" style="width: {resonance}%"></div>
            </div>
        </div>

        <button
            class="command-button"
            on:click={openCommand}
            title="Command Palette (⌘K)"
        >
            <span class="command-icon">⌘</span>
            <span class="command-text">Commands</span>
        </button>

        <div class="user-menu-container">
            <button
                class="user-button"
                on:click={() => (showUserMenu = !showUserMenu)}
                title="User Menu"
            >
                <span class="user-icon">👤</span>
                <span class="user-name">Citizen</span>
                <span class="dropdown-arrow">{showUserMenu ? "▲" : "▼"}</span>
            </button>

            {#if showUserMenu}
                <div class="user-dropdown">
                    {#each userMenuItems as item}
                        <button
                            class="dropdown-item"
                            on:click={() =>
                                item.action === "logout"
                                    ? console.log("logout")
                                    : navigate(item.path)}
                            title="{item.name} Page"
                        >
                            <span class="item-icon">{item.icon}</span>
                            <span class="item-name">{item.name}</span>
                        </button>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</header>

<style>
    .main-header {
        height: 64px;
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(25px) saturate(180%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    .logo-area {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }

    .logo-icon {
        font-size: 1.5rem;
    }

    .logo-text {
        font-weight: bold;
        color: white;
    }

    .breadcrumbs {
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.9rem;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    .resonance-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .resonance-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }

    .resonance-value {
        color: #4caf50;
        font-weight: bold;
    }

    .resonance-bar {
        width: 60px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
    }

    .resonance-fill {
        height: 100%;
        background: #4caf50;
        transition: width 0.3s ease;
    }

    .command-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .command-button:hover {
        background: rgba(76, 175, 80, 0.2);
        border-color: #4caf50;
        transform: translateY(-1px);
    }

    .command-icon {
        color: #4caf50;
    }

    .user-menu-container {
        position: relative;
    }

    .user-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: white;
        cursor: pointer;
    }

    .user-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 0.5rem;
        width: 200px;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
        z-index: 1000;
    }

    .dropdown-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem;
        background: transparent;
        border: none;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.8);
        cursor: pointer;
        text-align: left;
        transition: all 0.2s ease;
    }

    .dropdown-item:hover {
        background: rgba(76, 175, 80, 0.15);
        color: #4caf50;
    }

    .item-icon {
        font-size: 1.1rem;
    }
</style>
