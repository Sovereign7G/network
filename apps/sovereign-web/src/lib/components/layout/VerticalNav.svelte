<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { fly } from "svelte/transition";
    import { toolStore } from "$lib/stores/tool-store.svelte";

    let { collapsed = false } = $props();

    // NAVIGATION SECTION - Core app routes (7 cards)
    const navItems = [
        {
            name: "Dashboard",
            path: "/dashboard",
            icon: "🏛️",
            desc: "Main overview",
        },
        {
            name: "Marketplace",
            path: "/marketplace",
            icon: "🔌",
            desc: "Block registry",
        },
        { name: "Vault", path: "/vault", icon: "💰", desc: "Manage assets" },
        { name: "Hearth", path: "/hearth", icon: "🔥", desc: "Memory log" },
        { name: "Council", path: "/council", icon: "⚖️", desc: "Governance" },
        { name: "Atlas", path: "/atlas", icon: "🗺️", desc: "Network map" },
        { name: "Node", path: "/node", icon: "⚡", desc: "Node management" },
    ];

    // ACTION SECTION - Quick actions (4 cards)
    const actionItems = [
        {
            name: "Send",
            path: "/send",
            icon: "📤",
            color: "#4CAF50",
            desc: "Send assets",
        },
        {
            name: "Bridge",
            path: "/bridge",
            icon: "🌉",
            color: "#2196F3",
            desc: "Cross-chain",
        },
        {
            name: "Stake",
            path: "/stake",
            icon: "📈",
            color: "#9C27B0",
            desc: "Earn yield",
        },
        {
            name: "Swap",
            path: "/swap",
            icon: "🔄",
            color: "#FF9800",
            desc: "Swap tokens",
        },
    ];

    // TOOL SECTION - Quick utilities and capabilities
    const toolItems = [
        {
            name: "Calculator",
            icon: "🧮",
            action: "calculator",
            desc: "Quick calculations",
        },
        {
            name: "Converter",
            icon: "💱",
            action: "converter",
            desc: "Currency/unit converter",
        },
        {
            name: "Gas Estimator",
            icon: "⛽",
            action: "gas",
            desc: "Estimate transaction fees",
        },
        { name: "QR Scanner", icon: "📷", action: "qr", desc: "Scan QR codes" },
        { name: "Notes", icon: "📝", action: "notes", desc: "Quick notes" },
        {
            name: "Templates",
            icon: "📋",
            action: "templates",
            desc: "Block templates",
        },
    ];

    // CAPABILITIES SECTION - Protocol features
    const capabilityItems = [
        {
            name: "ZK-Proofs",
            icon: "🔐",
            status: "active",
            desc: "Zero-knowledge proofs",
            action: "zk-proof",
        },
        {
            name: "Multi-sig",
            icon: "🔑",
            status: "active",
            desc: "Multi-signature",
            action: "multi-sig",
        },
        {
            name: "Time Lock",
            icon: "⏰",
            status: "active",
            desc: "Timelocked transactions",
            action: "time-lock",
        },
        {
            name: "Recovery",
            icon: "🛡️",
            status: "active",
            desc: "Account recovery",
            action: "recovery",
        },
        {
            name: "Delegation",
            icon: "🤝",
            status: "beta",
            desc: "Delegate authority",
            action: "delegation",
        },
        {
            name: "Vesting",
            icon: "📊",
            status: "beta",
            desc: "Create vesting schedules",
            action: "vesting",
        },
    ];

    let activeTool = $derived(toolStore.state.activeTool);

    let showTools = $state(true);
    let showCapabilities = $state(true);
    let quickStats = { resonance: 98, tps: 1247, nodes: "389k" };

    function navigate(path: string) {
        goto(path);
    }

    function executeTool(tool: any) {
        toolStore.activateTool(tool);
    }

    function isActive(path: string): boolean {
        return (
            $page.url.pathname === path ||
            $page.url.pathname.startsWith(path + "/")
        );
    }
</script>

<div class="vertical-nav" class:collapsed>
    <!-- Collapse Toggle -->
    <div class="nav-header">
        <button
            class="collapse-button"
            onclick={() => (collapsed = !collapsed)}
        >
            {collapsed ? "→" : "←"}
        </button>
    </div>

    <!-- NAVIGATION SECTION - Top -->
    <div class="nav-section">
        <div class="section-title" class:hidden={collapsed}>NAVIGATION</div>
        <div class="section-items">
            {#each navItems as item}
                <button
                    class="nav-item"
                    title={collapsed ? item.desc : ""}
                    class:active={isActive(item.path)}
                    onclick={() => navigate(item.path)}
                >
                    <span class="nav-icon">{item.icon}</span>
                    {#if !collapsed}
                        <span class="nav-label">{item.name}</span>
                    {/if}
                </button>
            {/each}
        </div>
    </div>

    <!-- ACTION SECTION -->
    <div class="nav-section">
        <div class="section-title" class:hidden={collapsed}>ACTIONS</div>
        <div class="section-items">
            {#each actionItems as item}
                <button
                    class="nav-item action-item"
                    title={collapsed ? item.desc : ""}
                    style="--action-color: {item.color}"
                    onclick={() => navigate(item.path)}
                >
                    <span class="nav-icon">{item.icon}</span>
                    {#if !collapsed}
                        <span class="nav-label">{item.name}</span>
                    {/if}
                </button>
            {/each}
        </div>
    </div>

    <!-- TOOLS SECTION - Expandable -->
    <div class="nav-section expandable-section">
        <button
            class="section-header"
            id="tools-header"
            onclick={() => (showTools = !showTools)}
            onkeydown={(e) => e.key === "Enter" && (showTools = !showTools)}
            aria-expanded={showTools}
            aria-controls="tools-section"
        >
            <span class="section-title" class:hidden={collapsed}>TOOLS</span>
            <span class="section-toggle" class:hidden={collapsed}
                >{showTools ? "▼" : "▶"}</span
            >
        </button>

        {#if showTools}
            <div
                id="tools-section"
                role="region"
                aria-labelledby="tools-header"
                class="section-items"
                transition:fly={{ y: -10, duration: 150 }}
            >
                {#each toolItems as item}
                    <button
                        class="nav-item tool-item"
                        title={collapsed ? item.desc : ""}
                        class:active={activeTool?.action === item.action}
                        onclick={() => executeTool(item)}
                    >
                        <span class="nav-icon">{item.icon}</span>
                        {#if !collapsed}
                            <span class="nav-label">{item.name}</span>
                        {/if}
                    </button>
                {/each}
            </div>
        {/if}
    </div>

    <!-- CAPABILITIES SECTION - Protocol features -->
    <div class="nav-section expandable-section">
        <button
            class="section-header"
            id="capabilities-header"
            onclick={() => (showCapabilities = !showCapabilities)}
            onkeydown={(e) =>
                e.key === "Enter" && (showCapabilities = !showCapabilities)}
            aria-expanded={showCapabilities}
            aria-controls="capabilities-section"
        >
            <span class="section-title" class:hidden={collapsed}
                >CAPABILITIES</span
            >
            <span class="section-toggle" class:hidden={collapsed}
                >{showCapabilities ? "▼" : "▶"}</span
            >
        </button>

        {#if showCapabilities}
            <div
                id="capabilities-section"
                role="region"
                aria-labelledby="capabilities-header"
                class="section-items"
                transition:fly={{ y: -10, duration: 150 }}
            >
                {#each capabilityItems as item}
                    <button
                        class="capability-item"
                        title={collapsed ? item.desc : ""}
                        onclick={() => executeTool(item)}
                    >
                        <span class="nav-icon">{item.icon}</span>
                        {#if !collapsed}
                            <span class="nav-label">{item.name}</span>
                            <span class="capability-status {item.status}"
                                >{item.status}</span
                            >
                        {/if}
                    </button>
                {/each}
            </div>
        {/if}
    </div>

    <!-- QUICK STATS - At bottom -->
    <div class="nav-footer">
        {#if !collapsed}
            <div class="quick-stats">
                <div class="stat">
                    <span class="stat-label">Resonance</span>
                    <span class="stat-value">{quickStats.resonance}%</span>
                </div>
                <div class="stat">
                    <span class="stat-label">TPS</span>
                    <span class="stat-value">{quickStats.tps}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Nodes</span>
                    <span class="stat-value">{quickStats.nodes}</span>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .vertical-nav {
        width: 280px;
        height: 100vh;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(25px) saturate(180%);
        border-right: 1px solid rgba(255, 215, 0, 0.2);
        display: flex;
        flex-direction: column;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow-y: auto;
        position: sticky;
        top: 0;
        left: 0;
        z-index: 100;
    }

    .vertical-nav.collapsed {
        width: 80px;
    }

    .nav-header {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        margin-bottom: 1rem;
    }

    .collapse-button {
        width: 100%;
        padding: 0.75rem;
        background: rgba(255, 215, 0, 0.05);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 12px;
        color: #ffd700;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .collapse-button:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #ffd700;
    }

    .nav-section {
        padding: 0 0.75rem;
        margin-bottom: 1.5rem;
    }

    .expandable-section {
        margin-bottom: 1rem;
    }

    .section-header {
        display: flex;
        align-items: center;
        width: 100%;
        background: transparent;
        border: none;
        justify-content: space-between;
        padding: 0.5rem 0.75rem;
        cursor: pointer;
        border-radius: 8px;
        transition: background 0.2s ease;
    }

    .section-header:hover {
        background: rgba(255, 215, 0, 0.05);
    }

    .section-title {
        color: rgba(255, 215, 0, 0.5);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .section-title.hidden {
        display: none;
    }

    .section-toggle {
        color: rgba(255, 215, 0, 0.5);
        font-size: 0.8rem;
    }

    .section-toggle.hidden {
        display: none;
    }

    .section-items {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .nav-item,
    .capability-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
        padding: 0.75rem 1rem;
        background: transparent;
        border: none;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
        position: relative;
    }

    .nav-item:hover,
    .capability-item:hover {
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
        transform: translateX(4px);
    }

    .nav-item.active {
        background: rgba(255, 215, 0, 0.15);
        color: #ffd700;
        border-left: 3px solid #ffd700;
    }

    .action-item:hover {
        background: rgba(var(--action-color), 0.15);
        color: var(--action-color);
    }

    .tool-item {
        font-size: 0.9rem;
    }

    .capability-item {
        cursor: default;
        display: flex;
        align-items: center;
    }

    .capability-status {
        font-size: 0.6rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-left: auto;
    }

    .capability-status.active {
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
    }

    .capability-status.beta {
        background: rgba(255, 152, 0, 0.2);
        color: #ff9800;
    }

    .nav-icon {
        font-size: 1.2rem;
        min-width: 24px;
        text-align: center;
    }

    .nav-label {
        flex: 1;
        font-size: 0.9rem;
    }

    .collapsed .nav-label,
    .collapsed .capability-status,
    .collapsed .section-toggle {
        display: none;
    }

    .collapsed .nav-item,
    .collapsed .capability-item {
        justify-content: center;
        padding: 0.75rem 0;
    }

    .collapsed .section-header {
        justify-content: center;
        padding: 0.5rem 0;
    }

    .nav-footer {
        margin-top: auto;
        padding: 1rem;
        border-top: 1px solid rgba(255, 215, 0, 0.1);
    }

    .quick-stats {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .stat {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
    }

    .stat-value {
        color: #ffd700;
        font-weight: bold;
    }

    /* Scrollbar styling */
    .vertical-nav::-webkit-scrollbar {
        width: 4px;
    }

    .vertical-nav::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    .vertical-nav::-webkit-scrollbar-thumb {
        background: rgba(255, 215, 0, 0.3);
        border-radius: 4px;
    }
</style>
