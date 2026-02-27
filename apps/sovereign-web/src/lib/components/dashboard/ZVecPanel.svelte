<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 📦 SOVEREIGN ZVEC: EMBEDDED VECTOR DASHBOARD
    // ═══════════════════════════════════════════════════════════════════════════
    // Visualizing High-Performance On-Device RAG and Native Knowledge Bases.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, slide } from "svelte/transition";
    import {
        Database,
        Search,
        Zap,
        Shield,
        HardDrive,
        Activity,
        BarChart3,
        Layers,
        Plus,
        Cpu,
        Terminal,
        Clock,
    } from "lucide-svelte";
    import {
        sovereignZVec,
        type ZVecCollection,
    } from "$lib/services/zvec-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<"collections" | "query" | "nodes">("collections");
    let selectedCollectionId = $state<string | null>(null);
    let queryInput = $state("");
    let isSearching = $state(false);
    let searchResults = $state<any[]>([]);

    const selectedCollection = $derived(
        sovereignZVec.allCollections.find(
            (c: ZVecCollection) => c.id === selectedCollectionId,
        ),
    );

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    async function runSearch() {
        if (!selectedCollectionId || !queryInput) return;
        isSearching = true;
        // Simulate embedding generation + zVec query
        await new Promise((r) => setTimeout(r, 600));
        searchResults = await sovereignZVec.query(selectedCollectionId, [], 5);
        isSearching = false;
    }
</script>

<div class="zvec-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <Database size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Sovereign zVec</h3>
                <p>Alibaba Proxima-Powered Edge RAG</p>
            </div>
        </div>
        <div class="metrics-bar">
            <div class="metric">
                <span class="label">VECTORS</span>
                <span class="value">{sovereignZVec.stats.vectors}</span>
            </div>
            <div class="metric">
                <span class="label">LATENCY</span>
                <span class="value success">{sovereignZVec.stats.latency}</span>
            </div>
            <div class="metric">
                <span class="label">DISK</span>
                <span class="value glow">{sovereignZVec.stats.disk}</span>
            </div>
        </div>
    </header>

    <!-- 📑 TABS -->
    <div class="tabs">
        <button
            class:active={activeTab === "collections"}
            onclick={() => (activeTab = "collections")}
        >
            <Layers size={14} /> <span>Collections</span>
        </button>
        <button
            class:active={activeTab === "query"}
            onclick={() => (activeTab = "query")}
        >
            <Search size={14} /> <span>Query Lab</span>
        </button>
        <button
            class:active={activeTab === "nodes"}
            onclick={() => (activeTab = "nodes")}
        >
            <BarChart3 size={14} /> <span>Analytics</span>
        </button>
    </div>

    <!-- 🎚️ CONTENT AREA -->
    <div class="content-scroll">
        {#if activeTab === "collections"}
            <div class="collections-view" in:fade>
                <div class="actions-header">
                    <h4>Active Collections</h4>
                    <button
                        class="add-btn"
                        onclick={() =>
                            console.log(
                                "Create new vector persistence context",
                            )}
                    >
                        <Plus size={14} /> <span>Store Context</span>
                    </button>
                </div>

                <div class="grid">
                    {#each sovereignZVec.allCollections as col, i (col.id)}
                        <div
                            class="col-card"
                            role="button"
                            tabindex="0"
                            class:selected={selectedCollectionId === col.id}
                            in:fly={{ y: 20, delay: i * 100 }}
                            onclick={() => (selectedCollectionId = col.id)}
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" &&
                                (selectedCollectionId = col.id)}
                        >
                            <div class="card-head">
                                <div class="c-info">
                                    <h5>{col.name}</h5>
                                    <span class="id-tag">{col.id}</span>
                                </div>
                                {#if col.isEncrypted}
                                    <Shield size={12} class="crypt-icon" />
                                {/if}
                            </div>

                            <div class="card-stats">
                                <div class="c-stat">
                                    <span class="c-val"
                                        >{col.documentCount.toLocaleString()}</span
                                    >
                                    <span class="c-lab">DOCS</span>
                                </div>
                                <div class="c-stat">
                                    <span class="c-val">{col.dimension} d</span>
                                    <span class="c-lab">DIM</span>
                                </div>
                                <div class="c-stat">
                                    <span class="c-val">{col.indexType}</span>
                                    <span class="c-lab">INDEX</span>
                                </div>
                            </div>

                            {#if selectedCollectionId === col.id}
                                <div class="card-expanded" transition:slide>
                                    <div class="exp-row">
                                        <HardDrive size={12} />
                                        <span>{col.persistencePath}</span>
                                    </div>
                                    <div class="exp-actions">
                                        <button
                                            class="action-btn"
                                            onclick={(e: MouseEvent) => {
                                                e.stopPropagation();
                                                activeTab = "query";
                                            }}>Query</button
                                        >
                                        <button
                                            class="action-btn danger"
                                            onclick={(e: MouseEvent) => {
                                                e.stopPropagation();
                                                sovereignZVec.deleteCollection(
                                                    col.id,
                                                );
                                            }}>Wipe</button
                                        >
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeTab === "query"}
            <div class="query-view" in:fade>
                <div class="query-box">
                    <div class="q-header">
                        <Terminal size={14} />
                        <span>Vector Search Protocol (Proxima Engine)</span>
                        {#if selectedCollection}
                            <span class="target-tag"
                                >TARGET: {selectedCollection.name}</span
                            >
                        {/if}
                    </div>
                    <div class="q-input">
                        <input
                            bind:value={queryInput}
                            placeholder="Enter natural language query for RAG retrieval..."
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" && runSearch()}
                        />
                        <button onclick={runSearch} disabled={isSearching}>
                            {#if isSearching}
                                <Activity size={14} class="spin-icon" />
                            {:else}
                                <Zap size={14} />
                            {/if}
                        </button>
                    </div>
                </div>

                {#if searchResults.length > 0}
                    <div class="results" in:slide>
                        <div class="results-header">
                            <BarChart3 size={12} />
                            <span
                                >RETRIEVED {searchResults.length} DOCUMENTS</span
                            >
                        </div>
                        {#each searchResults as res}
                            <div class="res-item">
                                <div class="res-meta">
                                    <span class="score"
                                        >Score: {res.score.toFixed(4)}</span
                                    >
                                    <span class="res-id">{res.id}</span>
                                </div>
                                <p>{res.metadata.snippet}</p>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="empty-query">
                        <Search size={48} class="muted" />
                        <p>Awaiting Vector Input...</p>
                    </div>
                {/if}
            </div>
        {:else if activeTab === "nodes"}
            <div class="analytics-view" in:fade>
                <div class="stats-row">
                    <div class="stat-box">
                        <BarChart3 size={20} class="accent" />
                        <div class="v">
                            <span class="l">Current QPS</span>
                            <span class="n"
                                >{sovereignZVec.metrics.peakQPS.toLocaleString()}</span
                            >
                        </div>
                    </div>
                    <div class="stat-box">
                        <Cpu size={20} class="accent" />
                        <div class="v">
                            <span class="l">Memory Isolation</span>
                            <span class="n"
                                >{sovereignZVec.metrics.memoryFootprintMb.toFixed(
                                    1,
                                )} MB</span
                            >
                        </div>
                    </div>
                </div>

                <div class="history-list">
                    <div class="h-head">
                        <Clock size={12} />
                        <span>RECENT QUERY TELEMETRY</span>
                    </div>
                    {#each sovereignZVec.queryHistory as log}
                        <div class="h-item">
                            <span class="h-query">{log.query}</span>
                            <span class="h-stat success"
                                >{log.latency.toFixed(2)}ms</span
                            >
                            <span class="h-stat">{log.results} matches</span>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .zvec-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(10, 11, 15, 0.7);
        backdrop-filter: blur(20px);
        color: #e0e6ed;
        font-family: "Inter", system-ui, sans-serif;
    }

    .panel-header {
        padding: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .brand {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    .logo-orb {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #f59e0b, #ed64a6);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }

    .title-group h3 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .title-group p {
        margin: 0;
        font-size: 0.7rem;
        color: #94a3b8;
    }

    .metrics-bar {
        display: flex;
        gap: 1.5rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .metric .label {
        font-size: 0.6rem;
        color: #64748b;
        font-weight: 600;
    }

    .metric .value {
        font-size: 0.9rem;
        font-weight: 700;
        font-family: "JetBrains Mono", monospace;
    }

    .value.success {
        color: #10b981;
    }
    .value.glow {
        color: #ed64a6;
        text-shadow: 0 0 10px rgba(237, 100, 166, 0.4);
    }

    /* TABS */
    .tabs {
        padding: 0.5rem 1.25rem;
        display: flex;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.02);
    }

    .tabs button {
        background: none;
        border: none;
        color: #94a3b8;
        padding: 0.5rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
        border-radius: 6px;
        transition: all 0.2s;
    }

    .tabs button:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #f8fafc;
    }

    .tabs button.active {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* COLLECTIONS VIEW */
    .actions-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .actions-header h4 {
        margin: 0;
        font-size: 0.8rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .add-btn {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .add-btn:hover {
        background: rgba(245, 158, 11, 0.2);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1.25rem;
    }

    .col-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.25s;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .col-card:hover {
        border-color: rgba(245, 158, 11, 0.4);
        background: rgba(255, 255, 255, 0.05);
    }
    .col-card.selected {
        border-color: #f59e0b;
        background: rgba(245, 158, 11, 0.05);
    }

    .card-head {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .c-info h5 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .id-tag {
        font-size: 0.65rem;
        color: #475569;
        font-family: "JetBrains Mono";
    }
    :global(.crypt-icon) {
        color: #f59e0b;
    }

    .card-stats {
        display: flex;
        justify-content: space-between;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.75rem;
        border-radius: 8px;
    }

    .c-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .c-val {
        font-size: 0.75rem;
        font-weight: 800;
        font-family: "JetBrains Mono";
        color: #f1f5f9;
    }
    .c-lab {
        font-size: 0.55rem;
        font-weight: 700;
        color: #475569;
    }

    .card-expanded {
        margin-top: 0.5rem;
        padding-top: 1rem;
        border-top: 1px dashed rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .exp-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.65rem;
        color: #64748b;
        font-family: "JetBrains Mono";
    }

    .exp-actions {
        display: flex;
        gap: 0.5rem;
    }
    .action-btn {
        flex: 1;
        padding: 0.4rem;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        font-size: 0.7rem;
        font-weight: 700;
        cursor: pointer;
    }

    .action-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    .action-btn.danger:hover {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border-color: #ef4444;
    }

    /* QUERY VIEW */
    .query-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .query-box {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }

    .q-header {
        padding: 0.6rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.65rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
    }

    .target-tag {
        margin-left: auto;
        color: #f59e0b;
        background: rgba(245, 158, 11, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }

    .q-input {
        display: flex;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    .q-input input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        padding: 0.75rem;
        font-size: 0.9rem;
        outline: none;
    }

    .q-input button {
        background: #f59e0b;
        border: none;
        width: 42px;
        height: 42px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: transform 0.2s;
    }

    .q-input button:hover {
        transform: scale(1.05);
    }
    .q-input button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .results {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .results-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.6rem;
        font-weight: 900;
        color: #475569;
    }

    .res-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
    }

    .res-meta {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-family: "JetBrains Mono";
        font-size: 0.65rem;
    }
    .score {
        color: #10b981;
        font-weight: 700;
    }
    .res-id {
        color: #64748b;
    }
    .res-item p {
        margin: 0;
        font-size: 0.8rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    .empty-query {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 300px;
        color: #334155;
    }
    .empty-query p {
        margin-top: 1rem;
        font-size: 0.85rem;
    }

    /* ANALYTICS */
    .analytics-view {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    .stats-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .stat-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.25rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .stat-box .v {
        display: flex;
        flex-direction: column;
    }
    .stat-box .l {
        font-size: 0.7rem;
        font-weight: 600;
        color: #64748b;
    }
    .stat-box .n {
        font-size: 1.1rem;
        font-weight: 800;
        color: #f8fafc;
        font-family: "JetBrains Mono";
    }
    :global(.accent) {
        color: #f59e0b;
    }

    .history-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .h-head {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.65rem;
        font-weight: 800;
        color: #475569;
        margin-bottom: 0.5rem;
    }

    .h-item {
        display: flex;
        justify-content: space-between;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-family: "JetBrains Mono";
    }

    .h-stat {
        color: #64748b;
    }
    .h-stat.success {
        color: #10b981;
    }

    :global(.spin-icon) {
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
