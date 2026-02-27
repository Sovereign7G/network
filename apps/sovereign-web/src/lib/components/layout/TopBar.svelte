<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";

    import {
        Search,
        Bell,
        Settings,
        Zap,
        Activity,
        Shield,
        ChevronRight,
        Command,
        User,
    } from "lucide-svelte";
    import { manifold as manifoldStore } from "$lib/stores/master-store.svelte";
    import { sovereignStore } from "$lib/stores/sovereign-store.svelte";
    import { fade } from "svelte/transition";

    // Breadcrumb derivation
    const crumbs = $derived(
        $page.url.pathname
            .split("/")
            .filter(Boolean)
            .map((seg: string, i: number, arr: string[]) => ({
                label: seg.charAt(0).toUpperCase() + seg.slice(1),
                path: "/" + arr.slice(0, i + 1).join("/"),
            })),
    );

    let searchFocused = $state(false);
    let notifCount = $state(3);

    function openCommand() {
        document.dispatchEvent(
            new CustomEvent("command:open", { detail: { prompt: "/" } }),
        );
    }
</script>

<header class="topbar glass-panel-chiaroscuro sfumato-depth-1">
    <div class="topbar-glass"></div>

    <!-- Left: Breadcrumbs + Context -->
    <div class="topbar-left">
        <button
            class="home-anchor"
            onclick={() => goto("/dashboard")}
            aria-label="Go to dashboard"
        >
            <div class="anchor-glyph"></div>
        </button>

        <div class="breadcrumb-trail">
            {#each crumbs as crumb, i}
                {#if i > 0}
                    <ChevronRight
                        size={12}
                        class="text-white/10"
                        strokeWidth={3}
                    />
                {/if}
                <button
                    class="crumb"
                    class:active={i === crumbs.length - 1}
                    onclick={() => goto(crumb.path)}
                >
                    {crumb.label}
                </button>
            {/each}

            {#if crumbs.length === 0}
                <span class="crumb active">Home</span>
            {/if}
        </div>
    </div>

    <!-- Center: Command Search -->
    <div class="topbar-center">
        <button
            class="search-trigger group"
            class:focused={searchFocused}
            onclick={openCommand}
        >
            <Search
                size={14}
                class="text-white/20 group-hover:text-white/60 transition-colors"
            />
            <span class="search-placeholder">Search or command...</span>
            <div class="kbd-hint">
                <Command size={10} />
                <span>K</span>
            </div>
        </button>
    </div>

    <!-- Right: Telemetry + Actions -->
    <div class="topbar-right">
        <!-- Live Telemetry -->
        <div
            class="telemetry-strip"
            role="status"
            aria-label="Network telemetry"
        >
            <div class="tel-item" title="Network Resonance">
                <Activity size={12} class="text-emerald-400" />
                <span class="tel-val">{manifoldStore.resonance}%</span>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-item" title="Manifold Status">
                <Zap size={12} class="text-cyan-400" />
                <span class="tel-val"
                    >{manifoldStore.status === "COHERENT"
                        ? "STABLE"
                        : manifoldStore.status}</span
                >
            </div>
            <div class="tel-divider"></div>
            <div class="tel-item" title="Institutional Moat Level">
                <Shield size={12} class="text-indigo-400" />
                <span class="tel-val">E8.42</span>
            </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-cluster">
            <button
                class="topbar-btn"
                onclick={() => {}}
                aria-label={`Notifications: ${notifCount} unread`}
                title="Notifications"
            >
                <Bell size={16} />
                {#if notifCount > 0}
                    <div class="notif-badge" role="presentation">
                        {notifCount}
                    </div>
                {/if}
            </button>

            <button
                class="topbar-btn"
                onclick={() => goto("/settings")}
                aria-label="Settings"
                title="Settings"
            >
                <Settings size={16} />
            </button>

            <!-- Sovereign Mode Toggle -->
            <div class="mode-toggle-container">
                <button
                    class="mode-toggle-btn"
                    class:advanced={sovereignStore.state.preferences
                        .advancedMode}
                    onclick={() => sovereignStore.toggleAdvancedMode()}
                    title={sovereignStore.state.preferences.advancedMode
                        ? "Advanced Mode Active"
                        : "Enable Advanced Mode"}
                >
                    <div class="toggle-track">
                        <div class="toggle-thumb">
                            {#if sovereignStore.state.preferences.advancedMode}
                                <Zap size={10} fill="currentColor" />
                            {:else}
                                <div class="basic-dot"></div>
                            {/if}
                        </div>
                    </div>
                </button>
                {#if !sovereignStore.state.preferences.advancedMode}
                    <span class="mode-label" in:fade>Basic</span>
                {:else}
                    <span class="mode-label advanced kintsugi-text" in:fade
                        >Sovereign</span
                    >
                {/if}
            </div>

            <!-- Identity Pill -->
            <button
                class="identity-pill group glass-panel-chiaroscuro elevation-2"
                onclick={() => goto("/vault")}
                aria-label="View wallet profile"
            >
                <div class="id-avatar" role="presentation">
                    <User size={14} />
                </div>
                <span class="id-label">
                    {#if manifoldStore.web3?.isConnected}
                        {manifoldStore.web3.address?.slice(
                            0,
                            6,
                        )}...{manifoldStore.web3.address?.slice(-4)}
                    {:else}
                        Connect
                    {/if}
                </span>
            </button>
        </div>
    </div>
</header>

<style>
    .topbar {
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        background: rgba(5, 7, 10, 0.4);
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        position: sticky;
        top: 0;
        z-index: 500;
        font-family: "Outfit", sans-serif;
        gap: 2rem;
    }

    .topbar-glass {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            90deg,
            rgba(14, 165, 233, 0.02),
            transparent 30%,
            transparent 70%,
            rgba(99, 102, 241, 0.02)
        );
        pointer-events: none;
    }

    /* Left */
    .topbar-left {
        display: flex;
        align-items: center;
        gap: 1rem;
        min-width: 0;
    }

    .home-anchor {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
        flex-shrink: 0;
    }
    .home-anchor:hover {
        background: rgba(14, 165, 233, 0.1);
        border-color: rgba(14, 165, 233, 0.3);
    }
    .anchor-glyph {
        width: 10px;
        height: 10px;
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        border-radius: 3px;
        transform: rotate(45deg);
    }

    .breadcrumb-trail {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        overflow: hidden;
    }
    .crumb {
        font-size: 12px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.25);
        background: none;
        border: none;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 6px;
        transition: all 0.2s;
        white-space: nowrap;
        text-transform: capitalize;
    }
    .crumb:hover {
        color: white;
        background: rgba(255, 255, 255, 0.05);
    }
    .crumb.active {
        color: white;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    /* Center */
    .topbar-center {
        flex: 1;
        max-width: 480px;
        display: flex;
        justify-content: center;
    }

    .search-trigger {
        width: 100%;
        max-width: 400px;
        height: 36px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0 1rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .search-trigger:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
    }
    .search-placeholder {
        font-size: 12px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.2);
        flex: 1;
        text-align: left;
    }
    .kbd-hint {
        display: flex;
        align-items: center;
        gap: 3px;
        padding: 2px 6px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
    }

    /* Right */
    .topbar-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .telemetry-strip {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0 1rem;
        height: 32px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 8px;
    }
    .tel-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .tel-val {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        font-family: "JetBrains Mono", monospace;
    }
    .tel-divider {
        width: 1px;
        height: 14px;
        background: rgba(255, 255, 255, 0.05);
    }

    .action-cluster {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .topbar-btn {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.3);
        cursor: pointer;
        position: relative;
        transition: all 0.2s;
    }
    .topbar-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    /* Mode Toggle */
    .mode-toggle-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0 0.5rem;
        height: 36px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 100px;
    }

    .mode-toggle-btn {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
    }

    .toggle-track {
        width: 32px;
        height: 18px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        position: relative;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .toggle-thumb {
        position: absolute;
        top: 2px;
        left: 2px;
        width: 12px;
        height: 12px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #000;
    }

    .basic-dot {
        width: 4px;
        height: 4px;
        background: white;
        border-radius: 50%;
    }

    .mode-toggle-btn.advanced .toggle-track {
        background: rgba(255, 215, 0, 0.15);
        border-color: rgba(255, 215, 0, 0.3);
    }

    .mode-toggle-btn.advanced .toggle-thumb {
        left: 16px;
        background: var(--color-gold);
        box-shadow: 0 0 10px var(--color-gold);
    }

    .mode-label {
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
        min-width: 50px;
    }

    .mode-label.advanced {
        background-size: 200% auto;
    }

    .notif-badge {
        position: absolute;
        top: 4px;
        right: 4px;
        width: 14px;
        height: 14px;
        background: #f43f5e;
        border-radius: 50%;
        font-size: 8px;
        font-weight: 900;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .identity-pill {
        height: 36px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0 1rem 0 0.5rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .identity-pill:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(14, 165, 233, 0.2);
    }

    .id-avatar {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    .id-label {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        font-family: "JetBrains Mono", monospace;
    }

    @media (max-width: 1024px) {
        .telemetry-strip {
            display: none;
        }
        .search-trigger {
            max-width: 280px;
        }
    }

    @media (max-width: 768px) {
        .topbar-center {
            display: none;
        }
        .breadcrumb-trail {
            max-width: 200px;
        }
    }
</style>
