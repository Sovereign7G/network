<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import {
        conciergeStore,
        sovereignStore,
        hearthStore,
        vaultStore,
        governanceStore,
    } from "$lib/stores/master-store";
    import { CONCIERGE_PERSONALITIES } from "$lib/stores/constants";
    import ConversationList from "$lib/components/concierge/ConversationList.svelte";
    import ChatInterface from "$lib/components/concierge/ChatInterface.svelte";
    import InsightPanel from "$lib/components/concierge/InsightPanel.svelte";
    import PersonalitySelector from "$lib/components/concierge/PersonalitySelector.svelte";
    import { fade, fly } from "svelte/transition";

    let mounted = false;
    let showSidebar = true;
    let userContext = {};

    onMount(() => {
        mounted = true;
        console.log("🤖 Concierge mounted");

        // Generate initial user context
        updateContext();
    });

    function updateContext() {
        userContext = conciergeStore.generateUserContext(
            $sovereignStore,
            hearthStore.state,
            $vaultStore,
            $governanceStore,
        );
    }

    // Send message handler
    function handleSendMessage(event) {
        const content = event.detail;
        updateContext(); // Refresh context before sending
        conciergeStore.sendMessage(content, userContext);
    }

    // Watch for store changes to update context
    $: {
        if (mounted) {
            updateContext();
        }
    }
</script>

<svelte:head>
    <title>Sovereign Concierge · AGE Protocol</title>
</svelte:head>

<div class="concierge">
    <!-- Header -->
    <div class="concierge-header" in:fade>
        <div class="header-left">
            <button
                class="menu-toggle"
                onclick={() => (showSidebar = !showSidebar)}
                aria-label="Toggle sidebar"
            >
                <span class="menu-icon">{showSidebar ? "◀" : "▶"}</span>
            </button>

            <h1 class="concierge-title">
                <span class="title-icon">🤵</span>
                Sovereign Concierge
            </h1>
        </div>

        <div class="header-right">
            <PersonalitySelector
                currentPersonality={conciergeStore.state.personality}
                personalities={CONCIERGE_PERSONALITIES}
                onchange={(e) => conciergeStore.setPersonality(e.detail)}
            />
        </div>
    </div>

    <!-- Main grid -->
    <div class="concierge-grid">
        <!-- Left sidebar: Conversations & Insights -->
        {#if showSidebar}
            <div
                class="concierge-sidebar"
                in:fly={{ x: -20, duration: 300 }}
                out:fly={{ x: -20, duration: 200 }}
            >
                <div class="sidebar-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <span class="title-icon">💬</span>
                            Conversations
                        </h2>
                        <button
                            class="new-chat-btn"
                            onclick={() => conciergeStore.newConversation()}
                            title="New conversation"
                        >
                            <span class="btn-icon">+</span>
                        </button>
                    </div>

                    <ConversationList
                        conversations={conciergeStore.state.conversations}
                        currentId={conciergeStore.state.currentConversationId}
                        onselect={(e) =>
                            conciergeStore.switchConversation(e.detail)}
                        ondelete={(e) =>
                            conciergeStore.deleteConversation(e.detail)}
                    />
                </div>

                <div class="sidebar-section insights-section">
                    <h2 class="section-title">
                        <span class="title-icon">💡</span>
                        Active Insights
                        {#if conciergeStore.state.insights.length > 0}
                            <span class="insight-badge"
                                >{conciergeStore.state.insights.length}</span
                            >
                        {/if}
                    </h2>

                    <InsightPanel
                        insights={conciergeStore.state.insights}
                        ondismiss={(e) =>
                            conciergeStore.dismissInsight(e.detail)}
                        onexecute={(e) =>
                            conciergeStore.executeInsightAction(e.detail)}
                    />
                </div>

                <!-- User context summary -->
                <div class="sidebar-section context-summary">
                    <h2 class="section-title">
                        <span class="title-icon">📊</span>
                        Current State
                    </h2>
                    <div class="context-items">
                        <div class="context-item">
                            <span class="context-icon">🔥</span>
                            <span class="context-label">Resonance</span>
                            <span class="context-value"
                                >{userContext.totalResonance}</span
                            >
                        </div>
                        <div class="context-item">
                            <span class="context-icon">📅</span>
                            <span class="context-label">Streak</span>
                            <span class="context-value"
                                >{userContext.streak} days</span
                            >
                        </div>
                        <div class="context-item">
                            <span class="context-icon">💰</span>
                            <span class="context-label">Assets</span>
                            <span class="context-value"
                                >${userContext.totalValue?.toFixed(2) ||
                                    "0.00"}</span
                            >
                        </div>
                        <div class="context-item">
                            <span class="context-icon">🗳️</span>
                            <span class="context-label">Voting Power</span>
                            <span class="context-value"
                                >{userContext.votingPower}</span
                            >
                        </div>
                    </div>
                </div>
            </div>
        {/if}

        <!-- Main chat area -->
        <div class="concierge-main" class:sidebar-hidden={!showSidebar}>
            <ChatInterface
                conversation={conciergeStore.state.conversations.find(
                    (c) => c.id === conciergeStore.state.currentConversationId,
                )}
                personality={CONCIERGE_PERSONALITIES[
                    conciergeStore.state.personality.toUpperCase() as keyof typeof CONCIERGE_PERSONALITIES
                ] || CONCIERGE_PERSONALITIES.WISE}
                onsend={handleSendMessage}
                onnew={() => conciergeStore.newConversation()}
            />
        </div>
    </div>
</div>

<style>
    .concierge {
        height: calc(100vh - 80px); /* Full height minus header */
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        flex-direction: column;
    }

    .concierge-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .menu-toggle {
        width: 2.5rem;
        height: 2.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .menu-toggle:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .concierge-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 1.8rem;
    }

    .title-icon {
        font-size: 2rem;
    }

    .concierge-grid {
        display: flex;
        flex: 1;
        gap: 2rem;
        min-height: 0; /* Important for flex child scrolling */
        padding: 1rem 0;
    }

    .concierge-sidebar {
        width: 300px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }

    .title-icon {
        font-size: 1.2rem;
    }

    .insight-badge {
        background: #ff6b6b;
        color: white;
        font-size: 0.7rem;
        padding: 0.1rem 0.4rem;
        border-radius: 1rem;
    }

    .new-chat-btn {
        width: 2rem;
        height: 2rem;
        background: none;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .new-chat-btn:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .btn-icon {
        font-size: 1.2rem;
    }

    .insights-section {
        flex: 1;
        overflow-y: auto;
    }

    .context-summary {
        background: rgba(147, 112, 219, 0.05);
        border-color: rgba(147, 112, 219, 0.2);
    }

    .context-items {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .context-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0.5rem;
    }

    .context-icon {
        font-size: 1.1rem;
    }

    .context-label {
        flex: 1;
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .context-value {
        font-weight: 600;
        color: #9370db;
    }

    .concierge-main {
        flex: 1;
        min-width: 0;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        overflow: hidden;
        transition: all 0.3s;
    }

    .concierge-main.sidebar-hidden {
        margin-left: 0;
    }

    @media (max-width: 768px) {
        .concierge {
            padding: 0 1rem;
        }

        .concierge-grid {
            flex-direction: column;
        }

        .concierge-sidebar {
            width: 100%;
            max-height: 300px;
        }
    }
</style>
