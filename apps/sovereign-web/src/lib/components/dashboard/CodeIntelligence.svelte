<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🧠 SOVEREIGN CODE INTELLIGENCE PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // FastCode-inspired UI: Graph visualization, hybrid search, budget tracking
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade } from "svelte/transition";
    import {
        Search,
        Brain,
        GitBranch,
        Zap,
        BarChart3,
        Network,
        Target,
        ShieldCheck,
        DollarSign,
        ArrowRight,
        Activity,
        Layers,
        Database,
        Code,
        Eye,
        AlertTriangle,
    } from "lucide-svelte";
    import {
        codeIntelligence,
        type RetrievalResult,
        type CodeElement,
    } from "$lib/services/fastcode-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<"search" | "graph" | "impact" | "stats">("search");
    let searchQuery = $state("");
    let isSearching = $state(false);
    let searchResults = $state<RetrievalResult[]>([]);
    let expandedResult = $state<string | null>(null);
    let impactTarget = $state<string>("");
    let impactResult = $state<{
        directlyAffected: CodeElement[];
        transitivelyAffected: CodeElement[];
        riskLevel: string;
        recommendation: string;
    } | null>(null);

    // ─── DERIVED ────────────────────────────────────────────────────────────

    const engine = codeIntelligence;
    let engineStats = $derived(engine.stats);
    let lastBudget = $derived(engine.lastBudget);
    let lastScout = $derived(engine.lastScout);
    let graphStats = $derived(engine.graph?.stats ?? null);

    let elements = $derived(engine.elements);

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    async function handleSearch() {
        if (!searchQuery.trim()) return;
        isSearching = true;
        try {
            searchResults = await engine.search(searchQuery, {});
        } finally {
            isSearching = false;
        }
    }

    function handleImpactAnalysis() {
        if (!impactTarget) return;
        const elem = elements.find(

            (e) =>
                e.id === impactTarget ||
                e.name.toLowerCase().includes(impactTarget.toLowerCase()),
        );
        if (elem) {
            impactResult = engine.analyzeImpact(elem.id);
        }
    }

    function getLanguageColor(lang: string): string {
        const colors: Record<string, string> = {
            typescript: "#3178c6",
            svelte: "#ff3e00",
            rust: "#dea584",
            elixir: "#6e4a7e",
            python: "#3572A5",
            dart: "#00B4AB",
            go: "#00ADD8",
            motoko: "#6B3FA0",
            solidity: "#363636",
        };
        return colors[lang] ?? "#888";
    }

    function getLanguageEmoji(lang: string): string {
        const emojis: Record<string, string> = {
            typescript: "🔷",
            svelte: "🔶",
            rust: "🦀",
            elixir: "💜",
            python: "🐍",
            dart: "🎯",
            go: "🐹",
            motoko: "∞",
            solidity: "⟠",
        };
        return emojis[lang] ?? "📄";
    }

    function getRiskColor(risk: string): string {
        const colors: Record<string, string> = {
            low: "#22d3ee",
            medium: "#facc15",
            high: "#f97316",
            critical: "#ef4444",
        };
        return colors[risk] ?? "#888";
    }

    const tabs = [
        { id: "search" as const, label: "Hybrid Search", icon: Search },
        { id: "graph" as const, label: "Code Graph", icon: Network },
        {
            id: "impact" as const,
            label: "Impact Analysis",
            icon: AlertTriangle,
        },
        { id: "stats" as const, label: "Intelligence", icon: BarChart3 },
    ];
</script>

<div class="code-intel-panel" in:fly={{ y: 20, duration: 400 }}>
    <!-- Header -->
    <div class="panel-header">
        <div class="header-left">
            <Brain size={18} class="text-cyan-400" />
            <h3>Sovereign Code Intelligence</h3>
            <span class="badge">FastCode-Powered</span>
        </div>
        <div class="header-right">
            <div class="stat-pill">
                <Database size={10} />
                <span>{engineStats.totalElements} elements</span>
            </div>
            <div class="stat-pill">
                <Zap size={10} />
                <span>{engineStats.avgSearchTimeMs.toFixed(0)}ms avg</span>
            </div>
            <div class="stat-pill savings">
                <DollarSign size={10} />
                <span
                    >{(engineStats.tokensSaved / 1000).toFixed(1)}k tokens saved</span
                >
            </div>
        </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-nav">
        {#each tabs as tab}
            <button
                class="tab-btn"
                class:active={activeTab === tab.id}
                onclick={() => (activeTab = tab.id)}
            >
                <tab.icon size={14} />
                <span>{tab.label}</span>
            </button>
        {/each}
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
        <!-- ═══ HYBRID SEARCH TAB ═══ -->
        {#if activeTab === "search"}
            <div class="search-section" in:fade={{ duration: 200 }}>
                <!-- Search Bar -->
                <div class="search-bar">
                    <Search size={16} class="search-icon" />
                    <input
                        type="text"
                        bind:value={searchQuery}
                        placeholder="How does authentication work? / What would break if I change User model?"
                        onkeydown={(e: KeyboardEvent) => e.key === "Enter" && handleSearch()}
                    />
                    <button
                        class="search-btn"
                        onclick={handleSearch}
                        disabled={isSearching}
                    >
                        {#if isSearching}
                            <Activity size={14} class="animate-pulse" />
                        {:else}
                            <ArrowRight size={14} />
                        {/if}
                    </button>
                </div>

                <!-- Scout Trail (FastCode approach visualization) -->
                {#if lastScout}
                    <div class="scout-trail" in:fly={{ y: 10, duration: 300 }}>
                        <div class="scout-header">
                            <Target size={12} />
                            <span>Scout-First Navigation</span>
                            <span class="confidence"
                                >Confidence: {(
                                    lastScout.confidence * 100
                                ).toFixed(0)}%</span
                            >
                        </div>
                        <div class="scout-steps">
                            {#each lastScout.pathsTaken as step, i}
                                <div
                                    class="scout-step"
                                    in:fly={{
                                        x: -10,
                                        delay: i * 80,
                                        duration: 200,
                                    }}
                                >
                                    <div
                                        class="step-indicator"
                                        style="--step-color: {i < 2
                                            ? '#22d3ee'
                                            : i < 4
                                              ? '#a855f7'
                                              : '#10b981'}"
                                    >
                                        {i + 1}
                                    </div>
                                    <span>{step}</span>
                                </div>
                            {/each}
                        </div>
                        <div class="scout-savings">
                            <Zap size={12} class="text-emerald-400" />
                            <span
                                >{(lastScout.tokensSaved / 1000).toFixed(1)}k
                                tokens saved vs naive approach</span
                            >
                        </div>
                    </div>
                {/if}

                <!-- Budget Report -->
                {#if lastBudget}
                    <div
                        class="budget-report"
                        in:fly={{ y: 10, duration: 300, delay: 100 }}
                    >
                        <div class="budget-bar">
                            <div
                                class="budget-fill"
                                style="width: {lastBudget.utilization * 100}%"
                            ></div>
                        </div>
                        <div class="budget-stats">
                            <span
                                >{lastBudget.totalTokensUsed} / {lastBudget.totalTokenBudget}
                                tokens</span
                            >
                            <span
                                >{lastBudget.elementsIncluded} included · {lastBudget.elementsSkipped}
                                skipped</span
                            >
                            <span class="cost"
                                >~${lastBudget.costEstimate.toFixed(4)}</span
                            >
                        </div>
                    </div>
                {/if}

                <!-- Search Results -->
                <div class="results-list">
                    {#each searchResults as result, i (result.element.id)}
                        <div
                            class="result-card"
                            in:fly={{ y: 15, delay: i * 60, duration: 300 }}
                            role="button"
                            tabindex="0"
                            onclick={() =>
                                (expandedResult =
                                    expandedResult === result.element.id
                                        ? null
                                        : result.element.id)}
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" &&
                                (expandedResult =
                                    expandedResult === result.element.id
                                        ? null
                                        : result.element.id)}
                        >
                            <div class="result-header">
                                <div class="result-title">
                                    <span
                                        class="lang-badge"
                                        style="background: {getLanguageColor(
                                            result.element.language,
                                        )}20; color: {getLanguageColor(
                                            result.element.language,
                                        )}; border-color: {getLanguageColor(
                                            result.element.language,
                                        )}40"
                                    >
                                        {getLanguageEmoji(
                                            result.element.language,
                                        )}
                                        {result.element.language}
                                    </span>
                                    <span class="result-name"
                                        >{result.element.name}</span
                                    >
                                    <span class="result-type"
                                        >{result.element.type}</span
                                    >
                                </div>
                                <div
                                    class="score-ring"
                                    style="--score: {result.score}"
                                >
                                    <span
                                        >{(result.score * 100).toFixed(0)}</span
                                    >
                                </div>
                            </div>

                            <div class="result-path">
                                {result.element.relativePath}
                            </div>
                            <div class="result-explanation">
                                {result.explanation}
                            </div>

                            <!-- Score Breakdown -->
                            <div class="score-breakdown">
                                <div
                                    class="score-bar"
                                    title="Semantic: {(
                                        result.semanticScore * 100
                                    ).toFixed(0)}%"
                                >
                                    <div class="bar-label">SEM</div>
                                    <div class="bar-track">
                                        <div
                                            class="bar-fill semantic"
                                            style="width: {result.semanticScore *
                                                100}%"
                                        ></div>
                                    </div>
                                </div>
                                <div
                                    class="score-bar"
                                    title="Keyword: {(
                                        result.keywordScore * 100
                                    ).toFixed(0)}%"
                                >
                                    <div class="bar-label">BM25</div>
                                    <div class="bar-track">
                                        <div
                                            class="bar-fill keyword"
                                            style="width: {result.keywordScore *
                                                100}%"
                                        ></div>
                                    </div>
                                </div>
                                <div
                                    class="score-bar"
                                    title="Graph: {(
                                        result.graphScore * 100
                                    ).toFixed(0)}%"
                                >
                                    <div class="bar-label">GRAPH</div>
                                    <div class="bar-track">
                                        <div
                                            class="bar-fill graph"
                                            style="width: {result.graphScore *
                                                100}%"
                                        ></div>
                                    </div>
                                </div>
                            </div>

                            <!-- Expanded Details -->
                            {#if expandedResult === result.element.id}
                                <div
                                    class="result-details"
                                    in:fly={{ y: 10, duration: 200 }}
                                >
                                    <div class="detail-row">
                                        <span class="detail-label">Summary</span
                                        >
                                        <span class="detail-value"
                                            >{result.element.summary}</span
                                        >
                                    </div>
                                    <div class="detail-row">
                                        <span class="detail-label"
                                            >Token Cost</span
                                        >
                                        <span class="detail-value"
                                            >{result.tokenCost} tokens</span
                                        >
                                    </div>
                                    <div class="detail-row">
                                        <span class="detail-label"
                                            >Dependencies</span
                                        >
                                        <span class="detail-value"
                                            >{result.element.dependencies
                                                .length} deps · {result.element
                                                .dependents.length} dependents</span
                                        >
                                    </div>
                                    <div class="detail-row">
                                        <span class="detail-label"
                                            >Complexity</span
                                        >
                                        <span class="detail-value"
                                            >C={result.element.complexity}</span
                                        >
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}

                    {#if searchResults.length === 0 && searchQuery}
                        <div class="empty-state">
                            <Search size={32} class="text-white/10" />
                            <p>Enter a query and press Enter to search</p>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- ═══ CODE GRAPH TAB ═══ -->
        {:else if activeTab === "graph"}
            <div class="graph-section" in:fade={{ duration: 200 }}>
                {#if graphStats}
                    <div class="graph-stats-grid">
                        <div class="graph-stat">
                            <Layers size={16} />
                            <div>
                                <span class="stat-value"
                                    >{graphStats.totalNodes}</span
                                >
                                <span class="stat-label">Nodes</span>
                            </div>
                        </div>
                        <div class="graph-stat">
                            <GitBranch size={16} />
                            <div>
                                <span class="stat-value"
                                    >{graphStats.totalEdges}</span
                                >
                                <span class="stat-label">Edges</span>
                            </div>
                        </div>
                        <div class="graph-stat">
                            <Activity size={16} />
                            <div>
                                <span class="stat-value"
                                    >{graphStats.avgDegree.toFixed(1)}</span
                                >
                                <span class="stat-label">Avg Degree</span>
                            </div>
                        </div>
                        <div class="graph-stat">
                            <Target size={16} />
                            <div>
                                <span class="stat-value"
                                    >{graphStats.density.toFixed(4)}</span
                                >
                                <span class="stat-label">Density</span>
                            </div>
                        </div>
                    </div>

                    <!-- Graph Visualization (ASCII art representation) -->
                    <div class="graph-viz">
                        <div class="graph-title">
                            <Network size={14} />
                            <span>Multi-Layer Code Relationship Graph</span>
                        </div>
                        <div class="graph-layers">
                            {#each ["Call Graph", "Dependency Graph", "Inheritance Graph"] as layer, i}
                                <div
                                    class="layer-card"
                                    in:fly={{
                                        x: -20,
                                        delay: i * 100,
                                        duration: 300,
                                    }}
                                >
                                    <div
                                        class="layer-header"
                                        style="--layer-color: {[
                                            '#22d3ee',
                                            '#a855f7',
                                            '#f97316',
                                        ][i]}"
                                    >
                                        <span class="layer-dot"></span>
                                        <span>{layer}</span>
                                    </div>
                                    <div class="layer-stats">
                                        {#if engine.graph}
                                            <span
                                                >{[
                                                    engine.graph.callGraph
                                                        .length,
                                                    engine.graph.dependencyGraph
                                                        .length,
                                                    engine.graph
                                                        .inheritanceGraph
                                                        .length,
                                                ][i]} edges</span
                                            >
                                        {/if}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>

                    <!-- Element Registry -->
                    <div class="element-registry">
                        <div class="registry-header">
                            <Code size={14} />
                            <span>Indexed Elements by Language</span>
                        </div>

                        {#each [...new Set(elements.map((e) => e.language))] as lang}
                            {@const langElements = elements.filter(

                                (e) => e.language === lang,
                            )}
                            <div class="lang-group">
                                <div class="lang-header">
                                    <span class="lang-emoji"
                                        >{getLanguageEmoji(lang)}</span
                                    >
                                    <span class="lang-name">{lang}</span>
                                    <span class="lang-count"
                                        >{langElements.length}</span
                                    >
                                </div>
                                <div class="lang-elements">
                                    {#each langElements as elem}
                                        <div class="elem-pill">
                                            <span class="elem-type"
                                                >{elem.type}</span
                                            >
                                            <span class="elem-name"
                                                >{elem.name}</span
                                            >
                                            <span class="elem-tokens"
                                                >{elem.tokenCount}t</span
                                            >
                                        </div>
                                    {/each}
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>

            <!-- ═══ IMPACT ANALYSIS TAB ═══ -->
        {:else if activeTab === "impact"}
            <div class="impact-section" in:fade={{ duration: 200 }}>
                <div class="impact-search">
                    <AlertTriangle size={16} class="text-amber-400" />
                    <input
                        type="text"
                        bind:value={impactTarget}
                        placeholder="Enter element name (e.g., MasterStore, ConsensusEngine)..."
                        onkeydown={(e: KeyboardEvent) =>
                            e.key === "Enter" && handleImpactAnalysis()}
                    />
                    <button class="impact-btn" onclick={handleImpactAnalysis}>
                        <Eye size={14} />
                        Analyze
                    </button>
                </div>

                <!-- Quick Select -->
                <div class="quick-select">
                    {#each elements.slice(0, 8) as elem}
                        <button
                            class="quick-btn"
                            onclick={() => {
                                impactTarget = elem.name;
                                handleImpactAnalysis();
                            }}
                        >
                            {getLanguageEmoji(elem.language)}
                            {elem.name}
                        </button>
                    {/each}
                </div>

                {#if impactResult}
                    <div
                        class="impact-result"
                        in:fly={{ y: 15, duration: 300 }}
                    >
                        <div
                            class="risk-badge"
                            style="background: {getRiskColor(
                                impactResult.riskLevel,
                            )}20; border-color: {getRiskColor(
                                impactResult.riskLevel,
                            )}40; color: {getRiskColor(impactResult.riskLevel)}"
                        >
                            <ShieldCheck size={14} />
                            <span
                                >{impactResult.riskLevel.toUpperCase()} RISK</span
                            >
                        </div>

                        <p class="impact-recommendation">
                            {impactResult.recommendation}
                        </p>

                        {#if impactResult.directlyAffected.length > 0}
                            <div class="affected-group">
                                <h4>
                                    🎯 Directly Affected ({impactResult
                                        .directlyAffected.length})
                                </h4>
                                {#each impactResult.directlyAffected as elem}
                                    <div class="affected-item direct">
                                        <span
                                            class="lang-badge-sm"
                                            style="color: {getLanguageColor(
                                                elem.language,
                                            )}"
                                            >{getLanguageEmoji(
                                                elem.language,
                                            )}</span
                                        >
                                        <span>{elem.name}</span>
                                        <span class="affected-path"
                                            >{elem.relativePath}</span
                                        >
                                    </div>
                                {/each}
                            </div>
                        {/if}

                        {#if impactResult.transitivelyAffected.length > 0}
                            <div class="affected-group">
                                <h4>
                                    🌊 Transitively Affected ({impactResult
                                        .transitivelyAffected.length})
                                </h4>
                                {#each impactResult.transitivelyAffected as elem}
                                    <div class="affected-item transitive">
                                        <span
                                            class="lang-badge-sm"
                                            style="color: {getLanguageColor(
                                                elem.language,
                                            )}"
                                            >{getLanguageEmoji(
                                                elem.language,
                                            )}</span
                                        >
                                        <span>{elem.name}</span>
                                        <span class="affected-path"
                                            >{elem.relativePath}</span
                                        >
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                {/if}
            </div>

            <!-- ═══ STATS TAB ═══ -->
        {:else if activeTab === "stats"}
            <div class="stats-section" in:fade={{ duration: 200 }}>
                <div class="stats-hero">
                    <div class="hero-stat">
                        <span class="hero-value"
                            >{engineStats.queriesProcessed}</span
                        >
                        <span class="hero-label">Queries Processed</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-value"
                            >{(engineStats.tokensSaved / 1000).toFixed(
                                1,
                            )}k</span
                        >
                        <span class="hero-label">Tokens Saved</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-value"
                            >${engineStats.costSaved.toFixed(3)}</span
                        >
                        <span class="hero-label">Cost Saved</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-value"
                            >{engineStats.avgSearchTimeMs.toFixed(0)}ms</span
                        >
                        <span class="hero-label">Avg Latency</span>
                    </div>
                </div>

                <div class="methodology">
                    <h4>⚡ FastCode Methodology Applied</h4>
                    <div class="method-grid">
                        <div class="method-card">
                            <div class="method-icon">🏗️</div>
                            <h5>Semantic-Structural Representation</h5>
                            <p>
                                Multi-level indexing: files, classes, functions,
                                modules across 7 languages with AST-based
                                parsing.
                            </p>
                        </div>
                        <div class="method-card">
                            <div class="method-icon">🧭</div>
                            <h5>Scout-First Navigation</h5>
                            <p>
                                Build semantic map → Navigate structure → Load
                                targets. Never loads unnecessary code.
                            </p>
                        </div>
                        <div class="method-card">
                            <div class="method-icon">💰</div>
                            <h5>Budget-Aware Context</h5>
                            <p>
                                5-factor decision: confidence, complexity,
                                codebase size, cost, iterations. Value-first
                                selection.
                            </p>
                        </div>
                        <div class="method-card">
                            <div class="method-icon">📊</div>
                            <h5>Hybrid Retrieval</h5>
                            <p>
                                BM25 keyword (30%) + Semantic embedding (60%) +
                                Graph traversal (10%). Diversity-penalized
                                ranking.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="comparison">
                    <h4>📊 Approach Comparison</h4>
                    <div class="comparison-table">
                        <div class="comp-row header">
                            <span></span>
                            <span>Traditional</span>
                            <span>Sovereign (FastCode)</span>
                        </div>
                        <div class="comp-row">
                            <span>Approach</span>
                            <span class="bad">Load all files → Search</span>
                            <span class="good">Scout → Navigate → Target</span>
                        </div>
                        <div class="comp-row">
                            <span>Token Usage</span>
                            <span class="bad"
                                >{engineStats.totalTokensIndexed} tokens</span
                            >
                            <span class="good"
                                >~{Math.ceil(
                                    engineStats.totalTokensIndexed * 0.1,
                                )} tokens (90% less)</span
                            >
                        </div>
                        <div class="comp-row">
                            <span>Cost per Query</span>
                            <span class="bad"
                                >~${(
                                    engineStats.totalTokensIndexed * 0.000003
                                ).toFixed(4)}</span
                            >
                            <span class="good"
                                >~${(
                                    engineStats.totalTokensIndexed * 0.0000003
                                ).toFixed(4)}</span
                            >
                        </div>
                        <div class="comp-row">
                            <span>Multi-Language</span>
                            <span class="bad">Single repo only</span>
                            <span class="good">7 languages, cross-kernel</span>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .code-intel-panel {
        background: linear-gradient(
            135deg,
            rgba(0, 0, 0, 0.95) 0%,
            rgba(10, 10, 30, 0.95) 100%
        );
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 24px;
        overflow: hidden;
        font-family: "Inter", "SF Pro", system-ui, sans-serif;
        box-shadow:
            0 0 60px rgba(34, 211, 238, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        background: rgba(34, 211, 238, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .header-left h3 {
        font-size: 13px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }

    .badge {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        background: rgba(34, 211, 238, 0.15);
        color: #22d3ee;
        padding: 2px 8px;
        border-radius: 20px;
        letter-spacing: 0.1em;
        border: 1px solid rgba(34, 211, 238, 0.3);
    }

    .header-right {
        display: flex;
        gap: 8px;
    }

    .stat-pill {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 9px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 3px 10px;
        border-radius: 20px;
    }
    .stat-pill.savings {
        color: #10b981;
        border-color: rgba(16, 185, 129, 0.2);
    }

    .tab-nav {
        display: flex;
        gap: 2px;
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .tab-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: rgba(255, 255, 255, 0.3);
        background: transparent;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.2s;
    }
    .tab-btn:hover {
        color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.03);
    }
    .tab-btn.active {
        color: #22d3ee;
        background: rgba(34, 211, 238, 0.08);
        border-color: rgba(34, 211, 238, 0.2);
    }

    .tab-content {
        padding: 16px;
        max-height: 600px;
        overflow-y: auto;
    }
    .tab-content::-webkit-scrollbar {
        width: 4px;
    }
    .tab-content::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    /* Search Section */
    .search-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 4px 4px 4px 16px;
    }
    .search-icon {
        color: rgba(255, 255, 255, 0.2);
        flex-shrink: 0;
    }
    .search-bar input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: white;
        font-size: 12px;
        font-weight: 500;
    }
    .search-bar input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }
    .search-btn {
        padding: 8px 14px;
        border-radius: 12px;
        border: none;
        background: #22d3ee;
        color: black;
        cursor: pointer;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    .search-btn:hover {
        transform: scale(1.05);
    }
    .search-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* Scout Trail */
    .scout-trail {
        margin-top: 12px;
        padding: 12px;
        background: rgba(34, 211, 238, 0.03);
        border: 1px solid rgba(34, 211, 238, 0.1);
        border-radius: 12px;
    }
    .scout-header {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 9px;
        font-weight: 800;
        color: #22d3ee;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    .confidence {
        margin-left: auto;
        color: #10b981;
        background: rgba(16, 185, 129, 0.1);
        padding: 2px 8px;
        border-radius: 10px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .scout-steps {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .scout-step {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 500;
    }
    .step-indicator {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--step-color, #22d3ee);
        color: black;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 8px;
        font-weight: 900;
        flex-shrink: 0;
    }
    .scout-savings {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        font-size: 10px;
        font-weight: 700;
        color: #10b981;
        padding-top: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Budget Report */
    .budget-report {
        margin-top: 12px;
        padding: 10px 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    .budget-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        overflow: hidden;
    }
    .budget-fill {
        height: 100%;
        background: linear-gradient(90deg, #22d3ee, #a855f7);
        border-radius: 4px;
        transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .budget-stats {
        display: flex;
        justify-content: space-between;
        margin-top: 6px;
        font-size: 9px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.3);
    }
    .budget-stats .cost {
        color: #10b981;
    }

    /* Results */
    .results-list {
        margin-top: 16px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .result-card {
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        cursor: pointer;
        transition: all 0.2s;
    }
    .result-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(34, 211, 238, 0.15);
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .result-title {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .lang-badge {
        font-size: 8px;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 8px;
        border: 1px solid;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .result-name {
        font-size: 12px;
        font-weight: 800;
        color: white;
    }
    .result-type {
        font-size: 8px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .score-ring {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: conic-gradient(
            #22d3ee calc(var(--score) * 100%),
            rgba(255, 255, 255, 0.05) 0
        );
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .score-ring span {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 8px;
        font-weight: 900;
        color: #22d3ee;
    }

    .result-path {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.2);
        font-family: monospace;
        margin-top: 4px;
    }
    .result-explanation {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 4px;
        font-weight: 500;
    }

    .score-breakdown {
        display: flex;
        gap: 12px;
        margin-top: 8px;
    }
    .score-bar {
        flex: 1;
    }
    .bar-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 2px;
    }
    .bar-track {
        height: 3px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s;
    }
    .bar-fill.semantic {
        background: #22d3ee;
    }
    .bar-fill.keyword {
        background: #a855f7;
    }
    .bar-fill.graph {
        background: #f97316;
    }

    .result-details {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .detail-row {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
    }
    .detail-label {
        color: rgba(255, 255, 255, 0.3);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .detail-value {
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        text-align: right;
        max-width: 60%;
    }

    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: rgba(255, 255, 255, 0.15);
    }
    .empty-state p {
        font-size: 11px;
        font-weight: 600;
        margin-top: 10px;
    }

    /* Graph Section */
    .graph-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 16px;
    }
    .graph-stat {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #22d3ee;
    }
    .stat-value {
        font-size: 18px;
        font-weight: 900;
        color: white;
        display: block;
    }
    .stat-label {
        font-size: 8px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: block;
    }

    .graph-viz {
        padding: 16px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 16px;
    }
    .graph-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }
    .graph-layers {
        display: flex;
        gap: 8px;
    }
    .layer-card {
        flex: 1;
        padding: 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .layer-header {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.6);
    }
    .layer-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--layer-color);
        box-shadow: 0 0 8px var(--layer-color);
    }
    .layer-stats {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.3);
        margin-top: 4px;
        font-weight: 600;
    }

    .element-registry {
        margin-top: 16px;
    }
    .registry-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }
    .lang-group {
        margin-bottom: 12px;
    }
    .lang-header {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 10px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 6px;
    }
    .lang-emoji {
        font-size: 12px;
    }
    .lang-count {
        margin-left: auto;
        font-size: 9px;
        font-weight: 800;
        background: rgba(255, 255, 255, 0.05);
        padding: 1px 6px;
        border-radius: 8px;
    }
    .lang-elements {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
    }
    .elem-pill {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 9px;
        padding: 3px 8px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .elem-type {
        color: rgba(255, 255, 255, 0.2);
        font-weight: 700;
        text-transform: uppercase;
        font-size: 7px;
    }
    .elem-name {
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
    }
    .elem-tokens {
        color: rgba(255, 255, 255, 0.15);
        font-size: 8px;
    }

    /* Impact Section */
    .impact-search {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(251, 191, 36, 0.15);
        border-radius: 16px;
        padding: 4px 4px 4px 16px;
    }
    .impact-search input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: white;
        font-size: 12px;
        font-weight: 500;
    }
    .impact-search input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }
    .impact-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 12px;
        border: none;
        background: #f59e0b;
        color: black;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s;
    }
    .impact-btn:hover {
        transform: scale(1.05);
    }

    .quick-select {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin-top: 10px;
    }
    .quick-btn {
        font-size: 9px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        background: rgba(255, 255, 255, 0.02);
        color: rgba(255, 255, 255, 0.4);
        cursor: pointer;
        transition: all 0.2s;
    }
    .quick-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .impact-result {
        margin-top: 16px;
    }
    .risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 10px;
        border: 1px solid;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 0.06em;
    }
    .impact-recommendation {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.5);
        margin: 10px 0;
        font-weight: 500;
        line-height: 1.5;
    }

    .affected-group {
        margin-top: 14px;
    }
    .affected-group h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 8px;
    }
    .affected-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        border-radius: 8px;
        margin-bottom: 4px;
        font-size: 10px;
        font-weight: 600;
    }
    .affected-item.direct {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid rgba(239, 68, 68, 0.1);
        color: rgba(255, 255, 255, 0.6);
    }
    .affected-item.transitive {
        background: rgba(251, 191, 36, 0.03);
        border: 1px solid rgba(251, 191, 36, 0.08);
        color: rgba(255, 255, 255, 0.4);
    }
    .affected-path {
        margin-left: auto;
        font-family: monospace;
        font-size: 8px;
        color: rgba(255, 255, 255, 0.2);
    }

    /* Stats Section */
    .stats-hero {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 20px;
    }
    .hero-stat {
        text-align: center;
        padding: 16px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
    }
    .hero-value {
        font-size: 22px;
        font-weight: 900;
        color: #22d3ee;
        display: block;
    }
    .hero-label {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: block;
        margin-top: 4px;
    }

    .methodology {
        margin-bottom: 20px;
    }
    .methodology h4 {
        font-size: 12px;
        font-weight: 800;
        color: white;
        margin-bottom: 12px;
    }
    .method-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    .method-card {
        padding: 14px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .method-icon {
        font-size: 20px;
        margin-bottom: 8px;
    }
    .method-card h5 {
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.7);
        margin: 0 0 4px;
    }
    .method-card p {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.3);
        line-height: 1.5;
        margin: 0;
        font-weight: 500;
    }

    .comparison h4 {
        font-size: 12px;
        font-weight: 800;
        color: white;
        margin-bottom: 12px;
    }
    .comparison-table {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .comp-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        font-size: 9px;
        font-weight: 600;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .comp-row.header {
        background: rgba(255, 255, 255, 0.03);
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .comp-row span {
        padding: 8px 12px;
        display: flex;
        align-items: center;
    }
    .comp-row span:first-child {
        color: rgba(255, 255, 255, 0.4);
        font-weight: 700;
    }
    .comp-row .bad {
        color: rgba(239, 68, 68, 0.7);
    }
    .comp-row .good {
        color: #10b981;
    }

    .lang-badge-sm {
        font-size: 12px;
    }
    .lang-name {
        text-transform: capitalize;
    }
</style>
