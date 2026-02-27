<script lang="ts">
    import { fly, fade } from "svelte/transition";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    let blocks = [
        {
            id: "wealth-tracker",
            name: "Wealth Tracker",
            author: "@treasury",
            downloads: 12470,
            rating: 4.9,
            price: "FREE",
            verified: true,
            icon: "💰",
            category: "Finance",
            description:
                "Institutional-grade treasury metrics and yield monitoring.",
        },
        {
            id: "node-heatmap",
            name: "Node Heatmap",
            author: "@network",
            downloads: 8470,
            rating: 4.8,
            price: "50 SYND",
            verified: true,
            icon: "🔥",
            category: "Infrastructure",
            description: "Live geographic heatmap of validator node density.",
        },
        {
            id: "gov-timeline",
            name: "Governance Timeline",
            author: "@council",
            downloads: 3470,
            rating: 4.7,
            price: "FREE",
            verified: true,
            icon: "📊",
            category: "Council",
            description: "Track proposal lifecycles and voting tallies.",
        },
        {
            id: "bridge-radar",
            name: "Bridge Radar",
            author: "@crosschain",
            downloads: 5120,
            rating: 4.9,
            price: "30 SYND",
            verified: false,
            icon: "🌉",
            category: "DeFi",
            description: "Monitor cross-chain liquidity and pending bridges.",
        },
    ];

    let selectedCategory = "All";
    const categories = ["All", "Finance", "Infrastructure", "Council", "DeFi"];

    $: filteredBlocks =
        selectedCategory === "All"
            ? blocks
            : blocks.filter((b) => b.category === selectedCategory);

    function installBlock(block: any) {
        // Scaffold out the installation logic
        dispatch("install", block);
    }
</script>

<div class="marketplace-container" in:fly={{ y: 20, duration: 400 }}>
    <div class="marketplace-header">
        <div class="header-titles">
            <h2>Sovereign Registry</h2>
            <p>
                Discover, install, and share Composable Blocks for your Infinite
                Canvas.
            </p>
        </div>
        <button class="submit-btn" disabled>+ Submit Block</button>
    </div>

    <div class="category-filters">
        {#each categories as cat}
            <button
                class="filter-tag"
                class:active={selectedCategory === cat}
                onclick={() => (selectedCategory = cat)}
            >
                {cat}
            </button>
        {/each}
    </div>

    <div class="block-grid">
        {#each filteredBlocks as block (block.id)}
            <div class="block-card" in:fade>
                <div class="card-header">
                    <span class="block-icon">{block.icon}</span>
                    {#if block.verified}
                        <span class="verified-badge" title="Verified by Council"
                            >✓</span
                        >
                    {/if}
                </div>

                <h3>{block.name}</h3>
                <p class="author">by {block.author}</p>
                <p class="description">{block.description}</p>

                <div class="metrics">
                    <span class="metric"
                        >⬇️ {(block.downloads / 1000).toFixed(1)}k</span
                    >
                    <span class="metric">⭐ {block.rating}</span>
                </div>

                <div class="card-footer">
                    <div class="price" class:free={block.price === "FREE"}>
                        {block.price}
                    </div>
                    <button
                        class="install-btn"
                        onclick={() => installBlock(block)}
                    >
                        Install
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .marketplace-container {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        color: white;
    }

    .marketplace-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .header-titles h2 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(90deg, #fff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .header-titles p {
        margin: 0;
        color: rgba(255, 255, 255, 0.6);
        font-size: 1.1rem;
    }

    .submit-btn {
        padding: 0.75rem 1.5rem;
        background: rgba(255, 215, 0, 0.1);
        border: 1px dashed rgba(255, 215, 0, 0.5);
        border-radius: 12px;
        color: #ffd700;
        font-weight: 600;
        cursor: not-allowed;
        transition: all 0.2s;
    }

    .category-filters {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }

    .filter-tag {
        padding: 0.5rem 1.25rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 100px;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .filter-tag:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: rgba(255, 215, 0, 0.3);
    }

    .filter-tag.active {
        background: rgba(255, 215, 0, 0.2);
        border-color: #ffd700;
        color: #ffd700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1);
    }

    .block-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    .block-card {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .block-card:hover {
        border-color: rgba(255, 215, 0, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .block-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at top right,
            rgba(255, 215, 0, 0.05),
            transparent 60%
        );
        pointer-events: none;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .block-icon {
        font-size: 2.5rem;
        line-height: 1;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }

    .verified-badge {
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }

    .block-card h3 {
        margin: 0 0 0.25rem 0;
        font-size: 1.25rem;
        color: white;
    }

    .author {
        margin: 0 0 1rem 0;
        color: #ffd700;
        font-size: 0.85rem;
        opacity: 0.8;
    }

    .description {
        margin: 0 0 1.5rem 0;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        line-height: 1.5;
        flex-grow: 1;
    }

    .metrics {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding: 0.5rem 0;
        border-top: 1px dashed rgba(255, 255, 255, 0.1);
        border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
    }

    .metric {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .price {
        font-weight: 700;
        color: white;
        font-size: 1.1rem;
    }

    .price.free {
        color: #4caf50;
    }

    .install-btn {
        padding: 0.5rem 1.25rem;
        background: #ffd700;
        color: #0a0a0f;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .install-btn:hover {
        background: #fff;
        transform: scale(1.05);
    }

    @media (max-width: 768px) {
        .marketplace-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
        }
    }
</style>
