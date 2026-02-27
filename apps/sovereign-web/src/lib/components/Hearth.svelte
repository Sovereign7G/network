<script lang="ts">
    import { hearthStore } from "$lib/stores/master-store";
    import { MEMORY_TYPES } from "$lib/stores/constants";
    import MemoryForm from "./MemoryForm.svelte";
    import MemoryCard from "./MemoryCard.svelte";
    import StreakDisplay from "./StreakDisplay.svelte";
    import ResonanceBalance from "./ResonanceBalance.svelte";
    import { fade, slide } from "svelte/transition";

    import type { Memory } from "$lib/types";

    let showForm = $state(false);
    let selectedType = $state("all");
    let searchQuery = $state("");

    // Derived: filtered memories
    let filteredMemories = $derived(
        hearthStore.state.memories.filter((memory: Memory) => {
            const matchesType =
                selectedType === "all" || memory.type === selectedType;
            const matchesSearch =
                searchQuery === "" ||
                memory.content
                    .toLowerCase()
                    .includes(searchQuery.toLowerCase()) ||
                memory.title?.toLowerCase().includes(searchQuery.toLowerCase());
            return matchesType && matchesSearch;
        }),
    );

    // Update store when filters change
    $effect(() => {
        hearthStore.setFilter("type", selectedType as any);
        hearthStore.setFilter("search", searchQuery);
    });

    function handleNewMemory(memory: any) {
        hearthStore.addMemory(memory);
        showForm = false;
    }
</script>

<div class="hearth-container">
    <!-- Header with stats -->
    <div class="hearth-header">
        <h1 class="hearth-title">
            <span class="hearth-icon">🔥</span>
            Hearth
        </h1>

        <div class="stats-row">
            <StreakDisplay streak={hearthStore.state.streak} />
            <ResonanceBalance resonance={hearthStore.state.totalResonance} />
        </div>
    </div>

    <!-- Action bar -->
    <div class="action-bar">
        <button
            class="new-memory-btn"
            onclick={() => (showForm = !showForm)}
            class:active={showForm}
        >
            <span class="btn-icon">{showForm ? "✕" : "+"}</span>
            <span>{showForm ? "Cancel" : "New Memory"}</span>
        </button>

        <div class="filters">
            <select
                class="type-filter"
                bind:value={selectedType}
                aria-label="Filter by type"
            >
                <option value="all">All Memories</option>
                {#each Object.values(MEMORY_TYPES) as type}
                    <option value={type.id}>
                        {type.icon}
                        {type.label}
                    </option>
                {/each}
            </select>

            <input
                type="text"
                class="search-filter"
                placeholder="Search memories..."
                bind:value={searchQuery}
            />
        </div>
    </div>

    <!-- Memory form (slides in) -->
    {#if showForm}
        <div transitionslide={{ duration: 200 }}>
            <MemoryForm
                onsubmit={handleNewMemory}
                oncancel={() => (showForm = false)}
            />
        </div>
    {/if}

    <!-- Memories list -->
    <div class="memories-list">
        {#if filteredMemories.length === 0}
            <div class="empty-state" transition:fade>
                {#if hearthStore.state.memories.length === 0}
                    <p>
                        ✨ Your hearth is empty. Add your first memory to start
                        building resonance.
                    </p>
                {:else}
                    <p>🔍 No memories match your filters.</p>
                {/if}
            </div>
        {:else}
            {#each filteredMemories as memory (memory.id)}
                <div transition:fade>
                    <MemoryCard
                        {memory}
                        ondelete={() => hearthStore.deleteMemory(memory.id)}
                    />
                </div>
            {/each}
        {/if}
    </div>

    <!-- Quick tips for new users -->
    {#if hearthStore.state.memories.length === 0 && !showForm}
        <div class="tips-card" transition:fade>
            <h3>✨ Memory Types & Resonance</h3>
            <div class="tips-grid">
                {#each Object.values(MEMORY_TYPES) as type}
                    <div class="tip" style="--tip-color: {type.color}">
                        <span class="tip-icon">{type.icon}</span>
                        <div>
                            <strong>{type.label}</strong>
                            <span class="tip-value"
                                >+{type.resonance} resonance</span
                            >
                        </div>
                    </div>
                {/each}
            </div>
            <p class="tip-note">Post daily to maintain your streak!</p>
        </div>
    {/if}
</div>

<style>
    .hearth-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
        color: white;
    }

    .hearth-header {
        margin-bottom: 2rem;
        text-align: center;
    }

    .hearth-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .hearth-icon {
        font-size: 3rem;
        animation: flicker 3s infinite;
    }

    @keyframes flicker {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.8;
            transform: scale(1.05);
        }
    }

    .stats-row {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .action-bar {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .new-memory-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
        border: none;
        border-radius: 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        flex-shrink: 0;
    }

    .new-memory-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(147, 112, 219, 0.4);
    }

    .new-memory-btn.active {
        background: #666;
        transform: scale(0.95);
    }

    .btn-icon {
        font-size: 1.2rem;
    }

    .filters {
        display: flex;
        gap: 0.5rem;
        flex: 1;
        min-width: 250px;
    }

    .type-filter {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
    }

    .type-filter option {
        background: #1a1a1a;
    }

    .search-filter {
        flex: 1;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        min-width: 150px;
    }

    .search-filter:focus {
        outline: none;
        border-color: #9370db;
    }

    .memories-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        min-height: 200px;
    }

    .empty-state {
        text-align: center;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 1rem;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.5);
    }

    .tips-card {
        margin-top: 2rem;
        padding: 1.5rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid rgba(147, 112, 219, 0.3);
        border-radius: 1rem;
    }

    .tips-card h3 {
        margin: 0 0 1rem 0;
        color: #9370db;
    }

    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .tip {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0.5rem;
        border-left: 3px solid var(--tip-color);
    }

    .tip-icon {
        font-size: 1.5rem;
    }

    .tip-value {
        display: block;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .tip-note {
        text-align: center;
        font-style: italic;
        opacity: 0.7;
        margin: 0;
    }

    @media (max-width: 600px) {
        .action-bar {
            flex-direction: column;
            align-items: stretch;
        }

        .filters {
            flex-direction: column;
        }

        .stats-row {
            gap: 1rem;
        }
    }
</style>
