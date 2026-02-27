<script lang="ts">
    import { fade, slide, fly, scale } from "svelte/transition";
    import { spring } from "svelte/motion";
    import {
        Sparkles,
        ChevronRight,
        ChevronLeft,
        X,
        Undo2,
        Bell,
        History,
        BrainCircuit,
        Zap,
        ShieldCheck,
        Vote,
        Activity,
        AlertTriangle,
    } from "lucide-svelte";
    import { suggestionEngine } from "$lib/engines/suggestion-engine.svelte";
    import { learningEngine } from "$lib/engines/learning-engine.svelte";
    import LearningInsights from "./LearningInsights.svelte";
    import type { Suggestion } from "$lib/types";

    let collapsed = $state(true);
    let activeTab = $state<"suggestions" | "history" | "settings">(
        "suggestions",
    );
    let lastDismissed = $state<Suggestion | null>(null);
    let undoTimeout: ReturnType<typeof setTimeout> | null = null;

    const visibleSuggestions = $derived(
        suggestionEngine.suggestions.filter((s) => !s.dismissed),
    );

    // Physics-based spring for the width/expansion
    const panelWidth = spring(60, {
        stiffness: 0.1,
        damping: 0.8,
    });

    $effect(() => {
        panelWidth.set(collapsed ? 60 : 380);
    });

    function toggleCollapse() {
        collapsed = !collapsed;
    }

    function handleDismiss(id: string) {
        const sugg = suggestionEngine.suggestions.find((s) => s.id === id);
        if (sugg) {
            lastDismissed = { ...sugg };
            suggestionEngine.dismiss(id);

            if (undoTimeout) clearTimeout(undoTimeout);
            undoTimeout = setTimeout(() => {
                lastDismissed = null;
            }, 5000);
        }
    }

    function handleAction(suggestion: Suggestion) {
        learningEngine.trackInteraction({
            suggestionId: suggestion.id,
            type: suggestion.type,
            action: "acted",
            timestamp: Date.now(),
            source: suggestion.context.source,
        });
        suggestion.action?.handler();
    }

    function undoDismiss() {
        if (lastDismissed) {
            // Re-inject the suggestion (need a method in engine or just push)
            // For now, assume engine has a way to restore or we just manually re-enable
            // This would require engine logic support
            lastDismissed = null;
            if (undoTimeout) clearTimeout(undoTimeout);
        }
    }

    const typeIcons = {
        "idle-asset": Zap,
        "governance-proposal": Vote,
        "bridge-opportunity": ChevronRight,
        "milestone-completion": Sparkles,
        "anomaly-detected": AlertTriangle,
        "recovery-available": ShieldCheck,
        "stake-opportunity": Activity,
        "zk-opportunity": BrainCircuit,
        general: Bell,
    };

    function getIcon(type: string) {
        return typeIcons[type as keyof typeof typeIcons] || Bell;
    }
</script>

<aside
    class="concierge-hub glass-panel"
    class:collapsed
    style="width: {$panelWidth}px"
>
    <!-- Header / Toggle -->
    <div
        class="hub-header"
        onclick={toggleCollapse}
        role="button"
        tabindex="0"
        onkeydown={(e) => e.key === "Enter" && toggleCollapse()}
    >
        <div class="ai-orb">
            <BrainCircuit size={20} class="text-amber-400" />
            {#if visibleSuggestions.length > 0 && collapsed}
                <span class="notification-dot" in:scale></span>
            {/if}
        </div>

        {#if !collapsed}
            <div class="header-text" in:fade={{ delay: 100 }}>
                <h3
                    class="text-xs font-black uppercase tracking-widest text-white/80"
                >
                    Sovereign Concierge
                </h3>
                <span
                    class="text-[9px] text-emerald-400 font-bold uppercase tracking-tighter"
                    >Proactive Intelligence Active</span
                >
            </div>
            <button
                class="ml-auto text-white/20 hover:text-white"
                onclick={(e) => {
                    e.stopPropagation();
                    toggleCollapse();
                }}
            >
                <ChevronLeft size={16} />
            </button>
        {/if}
    </div>

    {#if !collapsed}
        <!-- Tabs -->
        <nav class="hub-tabs" in:fade={{ delay: 150 }}>
            <button
                class:active={activeTab === "suggestions"}
                onclick={() => (activeTab = "suggestions")}
            >
                <Bell size={14} />
                <span>Insights</span>
            </button>
            <button
                class:active={activeTab === "history"}
                onclick={() => (activeTab = "history")}
            >
                <History size={14} />
                <span>Archive</span>
            </button>
            <button
                class:active={activeTab === "settings"}
                onclick={() => (activeTab = "settings")}
            >
                <BrainCircuit size={14} />
                <span>Profile</span>
            </button>
        </nav>

        <!-- Content Area -->
        <div class="hub-content" in:fade={{ delay: 200 }}>
            {#if activeTab === "suggestions"}
                <div class="suggestions-stack">
                    {#if visibleSuggestions.length > 0}
                        {#each visibleSuggestions as suggestion (suggestion.id)}
                            {@const IconComp = getIcon(suggestion.type)}
                            <div
                                class="suggestion-card {suggestion.type}"
                                in:fly={{ x: 20, duration: 400 }}
                                out:slide={{ duration: 300 }}
                            >
                                <div class="card-glow"></div>
                                <div class="card-icon">
                                    <IconComp size={16} />
                                </div>
                                <div class="card-body">
                                    <div
                                        class="flex justify-between items-start mb-1"
                                    >
                                        <h4
                                            class="text-[11px] font-black text-white uppercase italic"
                                        >
                                            {suggestion.title}
                                        </h4>
                                        <button
                                            class="dismiss-btn"
                                            onclick={() =>
                                                handleDismiss(suggestion.id)}
                                        >
                                            <X size={12} />
                                        </button>
                                    </div>
                                    <p
                                        class="text-[10px] text-white/50 leading-relaxed mb-3"
                                    >
                                        {suggestion.description}
                                    </p>

                                    <div class="flex items-center gap-2">
                                        <button
                                            class="action-btn"
                                            onclick={() =>
                                                handleAction(suggestion)}
                                        >
                                            {suggestion.action?.label ||
                                                "View Details"}
                                        </button>
                                        <span
                                            class="text-[8px] font-black uppercase tracking-widest text-white/20 ml-auto"
                                        >
                                            {suggestion.context.source}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    {:else}
                        <div class="empty-state" in:fade>
                            <div class="zen-circle"></div>
                            <p
                                class="text-[10px] font-bold uppercase tracking-[0.2em] text-white/30"
                            >
                                The Cathedral is Serene
                            </p>
                            <p
                                class="text-[9px] text-white/10 uppercase tracking-widest mt-2"
                            >
                                No urgent actions detected
                            </p>
                        </div>
                    {/if}

                    {#if lastDismissed}
                        <div class="undo-toast" transitionfly={{ y: 20 }}>
                            <span class="text-[10px] text-white/60"
                                >Insight Archived</span
                            >
                            <button class="undo-btn" onclick={undoDismiss}>
                                <Undo2 size={12} />
                                <span>Undo</span>
                            </button>
                        </div>
                    {/if}
                </div>
            {:else if activeTab === "history"}
                <div class="history-view p-8 text-center" in:fade>
                    <p
                        class="text-[10px] text-white/20 uppercase tracking-widest"
                    >
                        Historical logs arriving in Phase 3.3
                    </p>
                </div>
            {:else if activeTab === "settings"}
                <div class="settings-view h-full" in:fade>
                    <LearningInsights />
                </div>
            {/if}
        </div>
    {/if}
</aside>

<style>
    .concierge-hub {
        position: fixed;
        right: 20px;
        top: 100px;
        bottom: 20px;
        z-index: 50;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transition: border-color 0.3s;
        border-radius: 2rem;
        background: linear-gradient(
            135deg,
            rgba(20, 20, 25, 0.8) 0%,
            rgba(10, 10, 15, 0.9) 100%
        );
        backdrop-filter: blur(40px);
    }

    .concierge-hub.collapsed {
        cursor: pointer;
        border-color: rgba(251, 191, 36, 0.2);
    }

    .concierge-hub.collapsed:hover {
        border-color: rgba(251, 191, 36, 0.4);
        background: rgba(251, 191, 36, 0.05);
    }

    .hub-header {
        height: 60px;
        padding: 0 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .ai-orb {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .notification-dot {
        position: absolute;
        top: -2px;
        right: -2px;
        width: 10px;
        height: 10px;
        background: #fbbf24;
        border-radius: 50%;
        box-shadow: 0 0 10px #fbbf24;
    }

    .hub-tabs {
        display: flex;
        padding: 12px;
        gap: 4px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .hub-tabs button {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 8px;
        border-radius: 12px;
        background: transparent;
        border: 1px solid transparent;
        color: rgba(255, 255, 255, 0.2);
        transition: all 0.2s;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .hub-tabs button.active {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .hub-content {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
    }

    .suggestions-stack {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .suggestion-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }

    .card-icon {
        position: absolute;
        top: 20px;
        left: -8px;
        width: 32px;
        height: 32px;
        background: black;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.6);
    }

    .suggestion-card.anomaly-detected {
        border-color: rgba(239, 68, 68, 0.2);
    }

    .suggestion-card.idle-asset {
        border-color: rgba(251, 191, 36, 0.2);
    }

    .action-btn {
        padding: 6px 16px;
        background: white;
        color: black;
        border: none;
        border-radius: 10px;
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: transform 0.2s;
    }

    .action-btn:hover {
        transform: scale(1.05);
    }

    .dismiss-btn {
        color: rgba(255, 255, 255, 0.1);
        transition: color 0.2s;
    }

    .dismiss-btn:hover {
        color: #ef4444;
    }

    .empty-state {
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .zen-circle {
        width: 100px;
        height: 100px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        margin-bottom: 24px;
        position: relative;
        animation: rotate 20s linear infinite;
    }

    .zen-circle::after {
        content: "";
        position: absolute;
        top: -2px;
        left: 50%;
        width: 4px;
        height: 4px;
        background: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 10px #34d399;
    }

    .undo-toast {
        position: sticky;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        padding: 12px 20px;
        border-radius: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .undo-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #fbbf24;
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
    }

    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .toggle-mock {
        width: 24px;
        height: 12px;
        background: #333;
        border-radius: 10px;
        position: relative;
    }

    .toggle-mock.active {
        background: #34d399;
    }

    .toggle-mock.active::after {
        content: "";
        position: absolute;
        right: 2px;
        top: 2px;
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
    }
</style>
