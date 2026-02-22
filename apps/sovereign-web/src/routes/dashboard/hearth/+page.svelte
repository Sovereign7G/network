<script lang="ts">
    import { onMount } from "svelte";
    import { hearthStore, RESONANCE_TIERS } from "$lib/stores/master-store";
    import MemoryCard from "$lib/components/hearth/MemoryCard.svelte";
    import MemoryForm from "$lib/components/hearth/MemoryForm.svelte";
    import ResonanceHistory from "$lib/components/hearth/ResonanceHistory.svelte";
    import InsightPanel from "$lib/components/hearth/InsightPanel.svelte";
    import AchievementWall from "$lib/components/hearth/AchievementWall.svelte";

    import Tile from "$lib/components/ui/Tile.svelte";
    import GlassCard from "$lib/components/ui/GlassCard.svelte";
    import QuickActions from "$lib/components/dashboard/QuickActions.svelte";
    import { tooltip } from "$lib/actions/tooltip";
    import { fade, fly, scale } from "svelte/transition";

    let mounted = false;
    let showForm = false;
    let selectedType = "all";
    let searchQuery = "";
    let dateRange = "all";
    let viewMode = "grid"; // grid or list
    let selectedMemory: any = null;

    onMount(() => {
        mounted = true;
    });

    // Update store filters
    $: if (mounted) {
        hearthStore.setFilter("type", selectedType);
        hearthStore.setFilter("search", searchQuery);
        hearthStore.setFilter("dateRange", dateRange);
    }

    // Get filtered memories
    $: filteredMemories = $hearthStore.memories.filter((memory: any) => {
        const matchesType =
            selectedType === "all" || memory.type === selectedType;
        const matchesSearch =
            searchQuery === "" ||
            memory.content?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            memory.title?.toLowerCase().includes(searchQuery.toLowerCase());

        let matchesDate = true;
        const now = new Date();
        if (dateRange === "week") {
            const weekAgo = new Date(now.setDate(now.getDate() - 7));
            matchesDate = new Date(memory.timestamp) >= weekAgo;
        } else if (dateRange === "month") {
            const monthAgo = new Date(now.setMonth(now.getMonth() - 1));
            matchesDate = new Date(memory.timestamp) >= monthAgo;
        } else if (dateRange === "year") {
            const yearAgo = new Date(now.setFullYear(now.getFullYear() - 1));
            matchesDate = new Date(memory.timestamp) >= yearAgo;
        }

        return matchesType && matchesSearch && matchesDate;
    });

    $: currentTier = hearthStore.getResonanceTier($hearthStore.totalResonance);
    $: nextTier = RESONANCE_TIERS.find(
        (t: any) => t.threshold > $hearthStore.totalResonance,
    );
    $: progressToNext =
        nextTier && currentTier
            ? (($hearthStore.totalResonance - currentTier.threshold) /
                  (nextTier.threshold - currentTier.threshold)) *
              100
            : 100;

    function handleNewMemory(event: any) {
        hearthStore.addMemory(event.detail);
        showForm = false;
    }

    function handleMemoryClick(memory: any) {
        selectedMemory = selectedMemory?.id === memory.id ? null : memory;
    }
</script>

<svelte:head>
    <title>Hearth · AGE Protocol</title>
</svelte:head>

<div class="hearth-container">
    <!-- Header Section -->
    <div class="hearth-header">
        <div class="greeting-section">
            <h1 class="glow-text">The <span class="accent">Hearth</span></h1>
            <p class="subtitle">
                Personal resonance manifold and memory orchestration
            </p>
        </div>

        <div class="header-actions">
            <button
                class="action-btn primary"
                on:click={() => (showForm = !showForm)}
                use:tooltip={"Record a new memory pulse to the hearth."}
            >
                <span>{showForm ? "✕ Close" : "+ New Memory"}</span>
            </button>
            <button
                class="action-btn"
                on:click={() =>
                    (viewMode = viewMode === "grid" ? "list" : "grid")}
                use:tooltip={"Toggle visual distribution of memories."}
            >
                <span>{viewMode === "grid" ? "📋 List" : "📱 Grid"}</span>
            </button>
        </div>
    </div>

    <!-- Primary Metrics Grid -->
    <div class="metrics-grid">
        <div
            use:tooltip={"Your current resonance tier and progress toward evolution."}
        >
            <Tile
                title="Resonance Tier"
                value={currentTier?.title || "Unknown"}
                icon={currentTier?.icon || "✨"}
                variant="primary"
                subtitle={`${Math.round(progressToNext)}% to next level`}
            />
        </div>

        <div use:tooltip={"Consecutive days of active resonance pulse."}>
            <Tile
                title="Active Streak"
                value={$hearthStore.streak + " Days"}
                icon="🔥"
                variant="warning"
                trend="+1"
            />
        </div>

        <div use:tooltip={"Total number of recorded memory facets."}>
            <Tile
                title="Memories"
                value={$hearthStore.memories.length.toString()}
                icon="📝"
                variant="info"
                subtitle="Immutable logs"
            />
        </div>

        <div
            use:tooltip={"Collective resonance generated across your lifetime."}
        >
            <Tile
                title="Lifetime Yield"
                value={$hearthStore.lifetimeResonance.toString()}
                icon="🏆"
                variant="success"
                trend="+15%"
            />
        </div>
    </div>

    <!-- Main Content Area - Three Column Layout -->
    <div class="hearth-main">
        <!-- Column 1: Memories & Feed -->
        <div class="column">
            <div
                use:tooltip={"The flow of your recorded temporal experiences."}
            >
                <GlassCard title="Memory Manifold" icon="📔" variant="primary">
                    <div class="search-bar">
                        <input
                            type="text"
                            placeholder="Search memories..."
                            bind:value={searchQuery}
                        />
                    </div>

                    {#if showForm}
                        <div
                            class="form-overlay"
                            in:fly={{ y: -20, duration: 300 }}
                        >
                            <MemoryForm
                                on:submit={handleNewMemory}
                                on:cancel={() => (showForm = false)}
                            />
                        </div>
                    {/if}

                    <div class="memories-list" class:grid={viewMode === "grid"}>
                        {#each filteredMemories as memory (memory.id)}
                            <MemoryCard
                                {memory}
                                isExpanded={selectedMemory?.id === memory.id}
                                on:click={() => handleMemoryClick(memory)}
                                on:delete={() =>
                                    hearthStore.deleteMemory(memory.id)}
                                on:reflect={(e) =>
                                    hearthStore.addReflection(
                                        memory.id,
                                        e.detail,
                                    )}
                            />
                        {/each}
                    </div>
                </GlassCard>
            </div>
        </div>

        <!-- Column 2: Analytics & History -->
        <div class="column">
            <div use:tooltip={"Temporal distribution of your resonance flow."}>
                <GlassCard title="Resonance Flow" icon="📈" variant="info">
                    <ResonanceHistory data={$hearthStore.resonanceHistory} />
                </GlassCard>
            </div>

            <div
                use:tooltip={"Deep recursive awareness patterns detected by the kernel."}
            >
                <GlassCard title="Deep Insights" icon="💡" variant="warning">
                    <InsightPanel insights={$hearthStore.insights} />
                </GlassCard>
            </div>
        </div>

        <!-- Column 3: Achievements & Tips -->
        <div class="column">
            <div
                use:tooltip={"Milestones earned through consistent resonance."}
            >
                <GlassCard title="Achievements" icon="🏆" variant="success">
                    <AchievementWall achievements={$hearthStore.achievements} />
                </GlassCard>
            </div>

            <div use:tooltip={"Guidance for optimizing your resonance yield."}>
                <GlassCard title="Resonance Tips" icon="✨" variant="info">
                    <div class="tips-list">
                        <div class="tip-item">
                            <span class="tip-icon">🔥</span>
                            <span
                                >Maintain daily pulse for streak multipliers</span
                            >
                        </div>
                        <div class="tip-item">
                            <span class="tip-icon">📚</span>
                            <span>Lessons generate +10 resonance</span>
                        </div>
                        <div class="tip-item">
                            <span class="tip-icon">🤝</span>
                            <span>Connections provide +15 resonance</span>
                        </div>
                    </div>
                </GlassCard>
            </div>
        </div>
    </div>

    <!-- Quick Actions Bar -->
    <div use:tooltip={"Unified access for rapid social and memory operations."}>
        <QuickActions />
    </div>
</div>

<style>
    .hearth-container {
        padding: 2rem;
        max-width: 1700px;
        margin: 0 auto;
    }

    .hearth-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        color: white;
    }

    .glow-text .accent {
        color: #ff6b6b;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin: 0.5rem 0 0;
    }

    .header-actions {
        display: flex;
        gap: 1rem;
    }

    .action-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
    }

    .action-btn.primary {
        background: linear-gradient(135deg, #ff6b6b, #ff4757);
        border: none;
    }

    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .hearth-main {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .column {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .search-bar {
        margin-bottom: 1.5rem;
    }

    .search-bar input {
        width: 100%;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        font-size: 0.9rem;
    }

    .form-overlay {
        background: rgba(255, 255, 255, 0.02);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
    }

    .memories-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-height: 800px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .memories-list.grid {
        display: grid;
        grid-template-columns: 1fr;
    }

    .memories-list::-webkit-scrollbar {
        width: 4px;
    }

    .memories-list::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
    }

    .tips-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .tip-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
    }

    .tip-icon {
        font-size: 1.25rem;
    }

    @media (max-width: 1400px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .hearth-main {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 768px) {
        .hearth-main {
            grid-template-columns: 1fr;
        }

        .hearth-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1.5rem;
        }
    }
</style>
