// ═══════════════════════════════════════════════════════════════════════════════
// 🧠 SOVEREIGN CODE INTELLIGENCE ENGINE
// ═══════════════════════════════════════════════════════════════════════════════
// Inspired by FastCode (HKUDS) — Semantic-Structural Code Understanding
// Applies 3 core innovations:
//   1. Multi-Layer Graph Modeling (Call Graph, Dependency Graph, Inheritance Graph)
//   2. Hybrid Retrieval (Semantic + BM25 Keyword + Graph Traversal)
//   3. Budget-Aware Context Management (Token efficiency, cost-optimized)
//
// [IN]: codebase file trees, query strings, agent-gateway
// [OUT]: CodeElement[], GraphAnalysis, RetrievalResult[], BudgetReport
// ═══════════════════════════════════════════════════════════════════════════════

// ─── TYPES: CODE ELEMENT INDEXING ────────────────────────────────────────────

export type CodeElementType = 'file' | 'class' | 'function' | 'method' | 'module' | 'type' | 'interface' | 'documentation';
export type CodeLanguage = 'typescript' | 'svelte' | 'rust' | 'elixir' | 'python' | 'dart' | 'go' | 'motoko' | 'solidity';

export interface CodeElement {
    id: string;
    type: CodeElementType;
    name: string;
    filePath: string;
    relativePath: string;
    language: CodeLanguage;
    startLine: number;
    endLine: number;
    signature: string | null;
    docstring: string | null;
    summary: string | null;
    dependencies: string[];          // IDs of elements this depends on
    dependents: string[];            // IDs of elements that depend on this
    complexity: number;              // Cyclomatic complexity estimate
    tokenCount: number;              // Estimated token cost to include
    embedding?: number[];            // Semantic embedding vector
    metadata: Record<string, unknown>;
    repoName: string;                // e.g. 'sovereign-web', 'kernel/rust', 'kernel/elixir'
}

// ─── TYPES: MULTI-LAYER GRAPH MODELING ──────────────────────────────────────

// import { browser } from '$app/environment';
// export * from '../types/fastcode.types';
export type GraphEdgeType = 'calls' | 'imports' | 'inherits' | 'implements' | 'uses_type' | 'co_located';

export interface GraphEdge {
    source: string;     // CodeElement ID
    target: string;     // CodeElement ID
    type: GraphEdgeType;
    weight: number;     // Strength of relationship (0-1)
    metadata?: Record<string, unknown>;
}

export interface GraphNode {
    elementId: string;
    label: string;
    type: CodeElementType;
    language: CodeLanguage;
    centrality: number;          // PageRank-style centrality score
    cluster: string;             // Community/module cluster
    inDegree: number;
    outDegree: number;
}

export interface CodeGraph {
    nodes: Map<string, GraphNode>;
    edges: GraphEdge[];
    callGraph: GraphEdge[];
    dependencyGraph: GraphEdge[];
    inheritanceGraph: GraphEdge[];
    stats: GraphStats;
}

export interface GraphStats {
    totalNodes: number;
    totalEdges: number;
    avgDegree: number;
    maxCentrality: { elementId: string; score: number };
    connectedComponents: number;
    density: number;
}

// ─── TYPES: HYBRID RETRIEVAL ────────────────────────────────────────────────

export interface RetrievalResult {
    element: CodeElement;
    score: number;                   // Combined relevance score (0-1)
    semanticScore: number;           // Cosine similarity from embeddings
    keywordScore: number;            // BM25 keyword match score
    graphScore: number;              // Graph proximity score
    explanation: string;             // Why this result was retrieved
    tokenCost: number;               // Estimated tokens to include this
}

export interface RetrievalConfig {
    semanticWeight: number;          // Default 0.6
    keywordWeight: number;           // Default 0.3
    graphWeight: number;             // Default 0.1
    maxResults: number;              // Default 10
    minSimilarity: number;           // Default 0.3
    diversityPenalty: number;        // Default 0.1
    maxTokenBudget: number;          // Default 4000
    enableGraphTraversal: boolean;   // Default true
    graphTraversalDepth: number;     // Default 2
}

// ─── TYPES: BUDGET-AWARE CONTEXT ────────────────────────────────────────────

export interface BudgetReport {
    totalTokensUsed: number;
    totalTokenBudget: number;
    utilization: number;             // 0-1
    elementsIncluded: number;
    elementsSkipped: number;
    costEstimate: number;            // USD estimate
    confidenceLevel: number;         // How confident are we in the answer (0-1)
    iterationsUsed: number;
    stoppingReason: 'budget_exhausted' | 'confidence_reached' | 'max_iterations' | 'no_more_results';
}

export interface QueryContext {
    query: string;
    intent: 'understand' | 'debug' | 'refactor' | 'impact_analysis' | 'architecture' | 'search';
    keywords: string[];
    expandedTerms: string[];
    filters: {
        language?: CodeLanguage[];
        type?: CodeElementType[];
        repo?: string[];
        path?: string;
    };
    complexity: 'simple' | 'moderate' | 'complex';
    estimatedTokenBudget: number;
}

// ─── TYPES: SCOUT-FIRST NAVIGATION ─────────────────────────────────────────

export interface ScoutResult {
    phase: 'semantic_map' | 'structure_navigation' | 'target_loading' | 'answer_generation';
    elementsDiscovered: number;
    elementsLoaded: number;
    tokensSaved: number;             // vs. naive file-loading approach
    pathsTaken: string[];            // Navigation breadcrumbs
    confidence: number;
}

// ═══════════════════════════════════════════════════════════════════════════════
// THE ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * BM25 Okapi Implementation — Fast keyword retrieval
 * Adapted from FastCode's rank_bm25 approach for TypeScript
 */
class BM25Index {
    private documents: string[][] = [];
    private docFreqs: Map<string, number> = new Map();
    private avgDocLen = 0;
    private k1 = 1.5;
    private b = 0.75;

    index(elements: CodeElement[]) {
        this.documents = [];
        this.docFreqs = new Map();

        for (const elem of elements) {
            const tokens = this._tokenize(elem);
            this.documents.push(tokens);

            const uniqueTokens = new Set(tokens);
            for (const token of uniqueTokens) {
                this.docFreqs.set(token, (this.docFreqs.get(token) ?? 0) + 1);
            }
        }

        this.avgDocLen = this.documents.reduce((s, d) => s + d.length, 0) / (this.documents.length || 1);
    }

    search(query: string, topK: number = 10): { index: number; score: number }[] {
        const queryTokens = query.toLowerCase().split(/\s+/).filter(Boolean);
        const n = this.documents.length;
        const scores: { index: number; score: number }[] = [];

        for (let i = 0; i < n; i++) {
            const doc = this.documents[i];
            if (!doc) continue;
            let score = 0;

            for (const term of queryTokens) {
                const tf = doc.filter(t => t === term).length;
                const df = this.docFreqs.get(term) ?? 0;
                if (df === 0 || tf === 0) continue;

                const idf = Math.log((n - df + 0.5) / (df + 0.5) + 1);
                const tfNorm = (tf * (this.k1 + 1)) / (tf + this.k1 * (1 - this.b + this.b * (doc.length / this.avgDocLen)));
                score += idf * tfNorm;
            }

            if (score > 0) scores.push({ index: i, score });
        }

        return scores.sort((a, b) => b.score - a.score).slice(0, topK);
    }

    private _tokenize(elem: CodeElement): string[] {
        const parts = [
            elem.name,
            elem.type,
            elem.language,
            elem.relativePath,
            elem.signature ?? '',
            elem.docstring ?? '',
            elem.summary ?? '',
        ];
        return parts.join(' ').toLowerCase().split(/\s+/).filter(Boolean);
    }
}

/**
 * Semantic Embedding — Cosine similarity search
 * Uses pre-computed embeddings for fast retrieval
 */
class SemanticIndex {
    private embeddings: Map<string, number[]> = new Map();

    index(elements: CodeElement[]) {
        this.embeddings.clear();
        for (const elem of elements) {
            // Generate a simple hash-based pseudo-embedding for demo
            // In production, this would use a real embedding model
            const embedding = this._generateEmbedding(elem);
            this.embeddings.set(elem.id, embedding);
            elem.embedding = embedding;
        }
    }

    search(queryEmbedding: number[], topK: number = 10): { elementId: string; score: number }[] {
        const results: { elementId: string; score: number }[] = [];

        for (const [elementId, embedding] of this.embeddings) {
            const score = this._cosineSimilarity(queryEmbedding, embedding);
            if (score > 0.1) results.push({ elementId, score });
        }

        return results.sort((a, b) => b.score - a.score).slice(0, topK);
    }

    getQueryEmbedding(query: string): number[] {
        return this._hashEmbedding(query, 64);
    }

    private _generateEmbedding(elem: CodeElement): number[] {
        const text = `${elem.name} ${elem.type} ${elem.summary ?? ''} ${elem.signature ?? ''}`;
        return this._hashEmbedding(text, 64);
    }

    private _hashEmbedding(text: string, dims: number): number[] {
        const vec = new Array(dims).fill(0);
        for (let i = 0; i < text.length; i++) {
            const code = text.charCodeAt(i);
            vec[i % dims] += Math.sin(code * 0.1 + i * 0.05) * 0.5;
            vec[(i + 7) % dims] += Math.cos(code * 0.15 + i * 0.03) * 0.3;
        }
        // Normalize
        const mag = Math.sqrt(vec.reduce((s, v) => s + v * v, 0)) || 1;
        return vec.map(v => v / mag);
    }

    private _cosineSimilarity(a: number[], b: number[]): number {
        if (a.length !== b.length) return 0;
        let dot = 0, magA = 0, magB = 0;
        for (let i = 0; i < a.length; i++) {
            const valA = a[i] ?? 0;
            const valB = b[i] ?? 0;
            dot += valA * valB;
            magA += valA * valA;
            magB += valB * valB;
        }
        const denom = Math.sqrt(magA) * Math.sqrt(magB);
        return denom === 0 ? 0 : dot / denom;
    }
}

/**
 * Code Graph Builder — Multi-layer relationship modeling
 * Builds Call Graph, Dependency Graph, and Inheritance Graph
 */
class CodeGraphBuilder {
    private nodes: Map<string, GraphNode> = new Map();
    private callEdges: GraphEdge[] = [];
    private depEdges: GraphEdge[] = [];
    private inheritEdges: GraphEdge[] = [];

    build(elements: CodeElement[]): CodeGraph {
        this.nodes.clear();
        this.callEdges = [];
        this.depEdges = [];
        this.inheritEdges = [];

        // Phase 1: Build nodes
        for (const elem of elements) {
            this.nodes.set(elem.id, {
                elementId: elem.id,
                label: elem.name,
                type: elem.type,
                language: elem.language,
                centrality: 0,
                cluster: this._inferCluster(elem),
                inDegree: 0,
                outDegree: 0,
            });
        }

        // Phase 2: Build edges from dependency data
        const elemById = new Map(elements.map(e => [e.id, e]));

        for (const elem of elements) {
            for (const depId of elem.dependencies) {
                if (elemById.has(depId)) {
                    const edgeType = this._inferEdgeType(elem, elemById.get(depId)!);
                    const edge: GraphEdge = {
                        source: elem.id,
                        target: depId,
                        type: edgeType,
                        weight: this._computeEdgeWeight(elem, elemById.get(depId)!, edgeType),
                    };

                    switch (edgeType) {
                        case 'calls': this.callEdges.push(edge); break;
                        case 'imports': this.depEdges.push(edge); break;
                        case 'inherits': case 'implements': this.inheritEdges.push(edge); break;
                        default: this.depEdges.push(edge);
                    }

                    // Update degrees
                    const sourceNode = this.nodes.get(elem.id);
                    const targetNode = this.nodes.get(depId);
                    if (sourceNode) sourceNode.outDegree++;
                    if (targetNode) targetNode.inDegree++;
                }
            }
        }

        // Phase 3: Compute centrality (simplified PageRank)
        this._computeCentrality();

        const allEdges = [...this.callEdges, ...this.depEdges, ...this.inheritEdges];

        return {
            nodes: this.nodes,
            edges: allEdges,
            callGraph: this.callEdges,
            dependencyGraph: this.depEdges,
            inheritanceGraph: this.inheritEdges,
            stats: this._computeStats(allEdges),
        };
    }

    /**
     * Graph-based retrieval: find related elements within N hops
     */
    getRelatedElements(elementId: string, maxDepth: number = 2): Map<string, number> {
        const visited = new Map<string, number>();
        const queue: { id: string; depth: number; score: number }[] = [{ id: elementId, depth: 0, score: 1.0 }];
        const allEdges = [...this.callEdges, ...this.depEdges, ...this.inheritEdges];

        while (queue.length > 0) {
            const current = queue.shift()!;
            if (visited.has(current.id) || current.depth > maxDepth) continue;

            visited.set(current.id, current.score);

            // Find connected nodes
            for (const edge of allEdges) {
                let neighbor: string | null = null;
                if (edge.source === current.id) neighbor = edge.target;
                else if (edge.target === current.id) neighbor = edge.source;

                if (neighbor && !visited.has(neighbor)) {
                    const decayedScore = current.score * edge.weight * Math.pow(0.5, current.depth);
                    queue.push({ id: neighbor, depth: current.depth + 1, score: decayedScore });
                }
            }
        }

        visited.delete(elementId); // Remove self
        return visited;
    }

    private _inferCluster(elem: CodeElement): string {
        const pathParts = elem.relativePath.split('/');
        return (pathParts.length > 1 ? pathParts[0] : 'root') || 'root';
    }

    private _inferEdgeType(source: CodeElement, target: CodeElement): GraphEdgeType {
        if (source.type === 'file' && target.type === 'file') return 'imports';
        if (source.type === 'class' && target.type === 'class') return 'inherits';
        if ((source.type === 'function' || source.type === 'method') &&
            (target.type === 'function' || target.type === 'method')) return 'calls';
        return 'uses_type';
    }

    private _computeEdgeWeight(source: CodeElement, target: CodeElement, type: GraphEdgeType): number {
        let weight = 0.5;
        if (source.language === target.language) weight += 0.2;
        if (type === 'calls') weight += 0.1;
        if (type === 'inherits') weight += 0.15;
        const pathSim = this._pathSimilarity(source.relativePath, target.relativePath);
        weight += pathSim * 0.15;
        return Math.min(1, weight);
    }

    private _pathSimilarity(a: string, b: string): number {
        const partsA = a.split('/');
        const partsB = b.split('/');
        let common = 0;
        for (let i = 0; i < Math.min(partsA.length, partsB.length); i++) {
            if (partsA[i] === partsB[i]) common++;
            else break;
        }
        return common / Math.max(partsA.length, partsB.length);
    }

    private _computeCentrality() {
        // Simplified iterative centrality (3 iterations)
        const scores = new Map<string, number>();
        for (const [id] of this.nodes) scores.set(id, 1.0 / this.nodes.size);

        const allEdges = [...this.callEdges, ...this.depEdges, ...this.inheritEdges];
        const damping = 0.85;

        for (let iter = 0; iter < 3; iter++) {
            const newScores = new Map<string, number>();
            for (const [id] of this.nodes) newScores.set(id, (1 - damping) / this.nodes.size);

            for (const edge of allEdges) {
                const sourceNode = this.nodes.get(edge.source);
                if (sourceNode && sourceNode.outDegree > 0) {
                    const contribution = (scores.get(edge.source) ?? 0) * damping / sourceNode.outDegree;
                    newScores.set(edge.target, (newScores.get(edge.target) ?? 0) + contribution);
                }
            }

            for (const [id, score] of newScores) scores.set(id, score);
        }

        for (const [id, score] of scores) {
            const node = this.nodes.get(id);
            if (node) node.centrality = score;
        }
    }

    private _computeStats(allEdges: GraphEdge[]): GraphStats {
        const centralities = [...this.nodes.values()].map(n => ({ elementId: n.elementId, score: n.centrality }));
        const maxCentrality = centralities.sort((a, b) => b.score - a.score)[0] ?? { elementId: '', score: 0 };
        const totalEdges = allEdges.length;
        const n = this.nodes.size;

        return {
            totalNodes: n,
            totalEdges: totalEdges,
            avgDegree: n > 0 ? (totalEdges * 2) / n : 0,
            maxCentrality,
            connectedComponents: 1, // Simplified
            density: n > 1 ? totalEdges / (n * (n - 1)) : 0,
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN ENGINE CLASS
// ═══════════════════════════════════════════════════════════════════════════════

export class SovereignCodeIntelligence {
    // Indexes
    private bm25 = new BM25Index();
    private semantic = new SemanticIndex();
    private graphBuilder = new CodeGraphBuilder();

    // State
    elements = $state<CodeElement[]>([]);
    graph = $state<CodeGraph | null>(null);
    lastQuery = $state<QueryContext | null>(null);
    lastResults = $state<RetrievalResult[]>([]);
    lastBudget = $state<BudgetReport | null>(null);
    lastScout = $state<ScoutResult | null>(null);
    isIndexing = $state(false);
    isSearching = $state(false);

    // Configuration
    config = $state<RetrievalConfig>({
        semanticWeight: 0.6,
        keywordWeight: 0.3,
        graphWeight: 0.1,
        maxResults: 10,
        minSimilarity: 0.3,
        diversityPenalty: 0.1,
        maxTokenBudget: 4000,
        enableGraphTraversal: true,
        graphTraversalDepth: 2,
    });

    // Stats
    stats = $state({
        totalElements: 0,
        totalTokensIndexed: 0,
        avgSearchTimeMs: 0,
        queriesProcessed: 0,
        tokensSaved: 0,
        costSaved: 0,
    });

    constructor() {
        // Initialize with AGE Protocol codebase structure
        this._indexProtocolCodebase();
    }

    // ─── PUBLIC: INDEX ──────────────────────────────────────────────────────

    /**
     * Index a set of code elements (FastCode Phase 1: Semantic-Structural Representation)
     */
    async indexElements(elements: CodeElement[]): Promise<void> {
        this.isIndexing = true;

        try {
            this.elements = elements;

            // Build BM25 keyword index
            this.bm25.index(elements);

            // Build semantic embeddings
            this.semantic.index(elements);

            // Build multi-layer graph
            this.graph = this.graphBuilder.build(elements);

            // Update stats
            this.stats.totalElements = elements.length;
            this.stats.totalTokensIndexed = elements.reduce((s, e) => s + e.tokenCount, 0);
        } finally {
            this.isIndexing = false;
        }
    }

    // ─── PUBLIC: SEARCH ─────────────────────────────────────────────────────

    /**
     * Scout-first hybrid retrieval (FastCode Phase 2 + 3)
     * 
     * Traditional: Question → Load Files → Search → Load More → Answer 💸
     * FastCode:    Question → Build Semantic Map → Navigate Structure → Load Targets → Answer 💰
     */
    async search(query: string, overrides?: Partial<RetrievalConfig>): Promise<RetrievalResult[]> {
        this.isSearching = true;
        const startTime = performance.now();
        const cfg = { ...this.config, ...overrides };

        try {
            // Phase 1: Process query (intent detection, keyword extraction)
            const ctx = this._processQuery(query);
            this.lastQuery = ctx;

            // Phase 2: Scout — Build semantic map WITHOUT loading full files
            // const scoutStart = performance.now();
            const keywordHits = this.bm25.search(query, cfg.maxResults * 3);
            const queryEmbedding = this.semantic.getQueryEmbedding(query);
            const semanticHits = this.semantic.search(queryEmbedding, cfg.maxResults * 3);
            // const scoutTime = performance.now() - scoutStart;

            // Phase 3: Navigate structure — Use graph to find related context
            let graphHits = new Map<string, number>();
            if (cfg.enableGraphTraversal) {
                // Find graph neighbors of top semantic + keyword hits
                const topHitIds = [
                    ...keywordHits.slice(0, 3).map(h => this.elements[h.index]?.id).filter(Boolean),
                    ...semanticHits.slice(0, 3).map(h => h.elementId),
                ] as string[];

                for (const hitId of topHitIds) {
                    const related = this.graphBuilder.getRelatedElements(hitId, cfg.graphTraversalDepth);
                    for (const [relId, relScore] of related) {
                        graphHits.set(relId, Math.max(graphHits.get(relId) ?? 0, relScore));
                    }
                }
            }

            // Phase 4: Fuse scores (weighted combination)
            const fusedScores = new Map<string, { semantic: number; keyword: number; graph: number }>();

            // Normalize keyword scores
            const maxKw = keywordHits[0]?.score ?? 1;
            for (const hit of keywordHits) {
                const elem = this.elements[hit.index];
                if (!elem) continue;
                const existing = fusedScores.get(elem.id) ?? { semantic: 0, keyword: 0, graph: 0 };
                existing.keyword = hit.score / maxKw;
                fusedScores.set(elem.id, existing);
            }

            // Normalize semantic scores
            for (const hit of semanticHits) {
                const existing = fusedScores.get(hit.elementId) ?? { semantic: 0, keyword: 0, graph: 0 };
                existing.semantic = hit.score;
                fusedScores.set(hit.elementId, existing);
            }

            // Add graph scores
            for (const [elemId, gScore] of graphHits) {
                const existing = fusedScores.get(elemId) ?? { semantic: 0, keyword: 0, graph: 0 };
                existing.graph = gScore;
                fusedScores.set(elemId, existing);
            }

            // Phase 5: Budget-aware ranking — Apply cost-efficient context management
            const candidates: RetrievalResult[] = [];
            const elemMap = new Map(this.elements.map(e => [e.id, e]));

            for (const [elemId, scores] of fusedScores) {
                const elem = elemMap.get(elemId);
                if (!elem) continue;

                const combinedScore =
                    scores.semantic * cfg.semanticWeight +
                    scores.keyword * cfg.keywordWeight +
                    scores.graph * cfg.graphWeight;

                if (combinedScore < cfg.minSimilarity) continue;

                // Value-first selection: score / token cost ratio
                // const valueRatio = combinedScore / Math.max(1, elem.tokenCount / 100);

                candidates.push({
                    element: elem,
                    score: combinedScore,
                    semanticScore: scores.semantic,
                    keywordScore: scores.keyword,
                    graphScore: scores.graph,
                    explanation: this._generateExplanation(scores, elem, ctx),
                    tokenCost: elem.tokenCount,
                });
            }

            // Sort by combined score, apply diversity penalty
            candidates.sort((a, b) => b.score - a.score);
            const diversified = this._applyDiversityPenalty(candidates, cfg.diversityPenalty);

            // Budget-aware: include only what fits
            let tokenBudget = cfg.maxTokenBudget;
            const budgetResults: RetrievalResult[] = [];
            let tokensUsed = 0;

            for (const result of diversified) {
                if (tokensUsed + result.tokenCost > tokenBudget && budgetResults.length >= 3) break;
                budgetResults.push(result);
                tokensUsed += result.tokenCost;
                if (budgetResults.length >= cfg.maxResults) break;
            }

            // Phase 6: Generate budget report
            const endTime = performance.now();
            const naiveTokenCost = this.elements.reduce((s, e) => s + e.tokenCount, 0);

            this.lastBudget = {
                totalTokensUsed: tokensUsed,
                totalTokenBudget: tokenBudget,
                utilization: tokensUsed / tokenBudget,
                elementsIncluded: budgetResults.length,
                elementsSkipped: candidates.length - budgetResults.length,
                costEstimate: tokensUsed * 0.000003, // ~$3/1M tokens
                confidenceLevel: budgetResults.length > 0 ? Math.min(1, (budgetResults[0]?.score ?? 0) * 1.5) : 0,
                iterationsUsed: 1,
                stoppingReason: tokensUsed >= tokenBudget ? 'budget_exhausted'
                    : budgetResults.length >= cfg.maxResults ? 'confidence_reached'
                        : 'no_more_results',
            };

            this.lastScout = {
                phase: 'answer_generation',
                elementsDiscovered: fusedScores.size,
                elementsLoaded: budgetResults.length,
                tokensSaved: naiveTokenCost - tokensUsed,
                pathsTaken: [
                    `BM25: ${keywordHits.length} hits`,
                    `Semantic: ${semanticHits.length} hits`,
                    `Graph: ${graphHits.size} neighbors`,
                    `Fused: ${fusedScores.size} candidates`,
                    `Budget-filtered: ${budgetResults.length} results`,
                ],
                confidence: this.lastBudget.confidenceLevel,
            };

            // Update stats
            this.stats.queriesProcessed++;
            this.stats.tokensSaved += naiveTokenCost - tokensUsed;
            this.stats.costSaved += (naiveTokenCost - tokensUsed) * 0.000003;
            this.stats.avgSearchTimeMs = (this.stats.avgSearchTimeMs * (this.stats.queriesProcessed - 1) + (endTime - startTime)) / this.stats.queriesProcessed;

            this.lastResults = budgetResults;
            return budgetResults;

        } finally {
            this.isSearching = false;
        }
    }

    // ─── PUBLIC: IMPACT ANALYSIS ────────────────────────────────────────────

    /**
     * What would break if we change element X?
     * Uses graph traversal to trace all dependents (FastCode Example 2)
     */
    analyzeImpact(elementId: string): {
        directlyAffected: CodeElement[];
        transitivelyAffected: CodeElement[];
        riskLevel: 'low' | 'medium' | 'high' | 'critical';
        recommendation: string;
    } {
        const related = this.graphBuilder.getRelatedElements(elementId, 3);
        const elemMap = new Map(this.elements.map(e => [e.id, e]));

        const directlyAffected: CodeElement[] = [];
        const transitivelyAffected: CodeElement[] = [];

        for (const [relId, score] of related) {
            const elem = elemMap.get(relId);
            if (!elem) continue;
            if (score > 0.5) directlyAffected.push(elem);
            else transitivelyAffected.push(elem);
        }

        const totalAffected = directlyAffected.length + transitivelyAffected.length;
        const riskLevel: 'low' | 'medium' | 'high' | 'critical' =
            totalAffected > 20 ? 'critical' :
                totalAffected > 10 ? 'high' :
                    totalAffected > 3 ? 'medium' : 'low';

        return {
            directlyAffected,
            transitivelyAffected,
            riskLevel,
            recommendation: `Changing this element affects ${directlyAffected.length} direct dependents and ${transitivelyAffected.length} transitive. Risk level: ${riskLevel.toUpperCase()}.`,
        };
    }

    // ─── PRIVATE: QUERY PROCESSING ──────────────────────────────────────────

    private _processQuery(query: string): QueryContext {
        const lower = query.toLowerCase();

        // Intent detection
        let intent: QueryContext['intent'] = 'search';
        if (lower.includes('how does') || lower.includes('explain') || lower.includes('understand')) intent = 'understand';
        else if (lower.includes('bug') || lower.includes('error') || lower.includes('fix') || lower.includes('debug')) intent = 'debug';
        else if (lower.includes('refactor') || lower.includes('improve') || lower.includes('optimize')) intent = 'refactor';
        else if (lower.includes('impact') || lower.includes('break') || lower.includes('change')) intent = 'impact_analysis';
        else if (lower.includes('architecture') || lower.includes('structure') || lower.includes('design')) intent = 'architecture';

        // Keyword extraction
        const stopwords = new Set(['the', 'a', 'an', 'is', 'are', 'in', 'of', 'to', 'for', 'and', 'or', 'this', 'that', 'what', 'how', 'does', 'would', 'if', 'i', 'we']);
        const keywords = lower.split(/\s+/).filter(w => w.length > 2 && !stopwords.has(w));

        // Complexity estimation
        const complexity: QueryContext['complexity'] =
            keywords.length > 8 ? 'complex' :
                keywords.length > 4 ? 'moderate' : 'simple';

        // Budget estimation
        const budgetMap = { simple: 2000, moderate: 4000, complex: 8000 };

        return {
            query,
            intent,
            keywords,
            expandedTerms: this._expandTerms(keywords),
            filters: {},
            complexity,
            estimatedTokenBudget: budgetMap[complexity],
        };
    }

    private _expandTerms(keywords: string[]): string[] {
        const synonyms: Record<string, string[]> = {
            'auth': ['authentication', 'login', 'credential', 'identity'],
            'api': ['endpoint', 'route', 'handler', 'service'],
            'db': ['database', 'store', 'persistence', 'query'],
            'ui': ['component', 'view', 'render', 'interface'],
            'governance': ['policy', 'vote', 'council', 'branch'],
            'trading': ['order', 'market', 'perpetual', 'position'],
            'wallet': ['balance', 'transaction', 'transfer', 'vault'],
            'agent': ['ai', 'autonomous', 'bot', 'strategy'],
            'kernel': ['core', 'runtime', 'engine', 'system'],
            'mesh': ['network', 'validator', 'node', 'peer'],
        };

        const expanded: string[] = [];
        for (const kw of keywords) {
            if (synonyms[kw]) expanded.push(...synonyms[kw]);
        }
        return [...new Set(expanded)];
    }

    private _generateExplanation(
        scores: { semantic: number; keyword: number; graph: number },
        elem: CodeElement,
        ctx: QueryContext
    ): string {
        const parts: string[] = [];
        if (scores.semantic > 0.5) parts.push(`Strong semantic match (${(scores.semantic * 100).toFixed(0)}%)`);
        if (scores.keyword > 0.5) parts.push(`Keyword match for: ${ctx.keywords.slice(0, 3).join(', ')}`);
        if (scores.graph > 0.3) parts.push(`Graph-connected to related code`);
        parts.push(`${elem.type} in ${elem.relativePath}`);
        return parts.join(' · ');
    }

    private _applyDiversityPenalty(results: RetrievalResult[], penalty: number): RetrievalResult[] {
        const seen = new Set<string>();
        return results.map(r => {
            const cluster = r.element.relativePath.split('/')[0] ?? 'root';
            if (seen.has(cluster)) {
                return { ...r, score: r.score * (1 - penalty) };
            }
            seen.add(cluster);
            return r;
        }).sort((a, b) => b.score - a.score);
    }

    // ─── PRIVATE: INITIALIZE WITH AGE PROTOCOL CODEBASE ─────────────────────

    private _indexProtocolCodebase() {
        // Generate representative code elements for the AGE Protocol structure
        const elements: CodeElement[] = [
            // ── FRONTEND (sovereign-web) ──
            this._mkElem('fe-master-store', 'module', 'MasterStore', 'src/lib/stores/master-store.svelte.ts', 'typescript', 'sovereign-web', 420, 'Sovereign state management with manifold controller, resonance tracking, and governance branching'),
            this._mkElem('fe-manifold-ctrl', 'class', 'ManifoldController', 'src/lib/stores/manifold-controller.svelte.ts', 'typescript', 'sovereign-web', 380, 'Central manifold orchestrator — resilience, safety, mesh events'),
            this._mkElem('fe-agent-gateway', 'module', 'AgentGateway', 'src/lib/services/agent-gateway.ts', 'typescript', 'sovereign-web', 650, 'Multi-agent orchestration service with Qwen3, Claude, GPT routing'),
            this._mkElem('fe-agent-registry', 'module', 'AgentRegistry', 'src/lib/services/agent-gateway-registry.ts', 'typescript', 'sovereign-web', 250, 'Policy registry for Agent Gateway — RBAC, Safety, Change Window'),
            this._mkElem('fe-audit-engine', 'module', 'AuditEngine', 'src/lib/services/audit-engine.svelte.ts', 'typescript', 'sovereign-web', 120, 'Metabolic Auditioning engine for protocol interventions'),
            this._mkElem('fe-token-engine', 'module', 'TokenomicsEngine', 'src/lib/services/tokenomics-engine.svelte.ts', 'typescript', 'sovereign-web', 150, 'Deep module for protocol tokenomics and ARI projection'),
            this._mkElem('fe-mesh-engine', 'module', 'MeshStressEngine', 'src/lib/services/mesh-stress-engine.svelte.ts', 'typescript', 'sovereign-web', 160, 'Deep module for autonomous mesh stress drills'),
            this._mkElem('fe-zk-engine', 'module', 'ZkAttesterEngine', 'src/lib/services/zk-attester-engine.svelte.ts', 'typescript', 'sovereign-web', 230, 'Deep module for state transition proof verification'),
            this._mkElem('fe-trading-engine', 'class', 'SovereignTradingEngine', 'src/lib/services/sovereign-trading-engine.ts', 'typescript', 'sovereign-web', 740, 'Perpetual trading, prediction markets, sovereign card, fiat ramps, agentic commerce'),
            this._mkElem('fe-llm-service', 'module', 'LLMService', 'src/lib/services/llm-service.ts', 'typescript', 'sovereign-web', 350, 'LLM routing and prompt management for sovereign AI'),

            this._mkElem('fe-web3-service', 'module', 'Web3Service', 'src/lib/services/web3-service.ts', 'typescript', 'sovereign-web', 180, 'Web3 wallet connection, chain management, contract interaction'),
            this._mkElem('fe-icp-service', 'module', 'ICPService', 'src/lib/services/icp-service.ts', 'typescript', 'sovereign-web', 220, 'Internet Computer Protocol canister management'),
            this._mkElem('fe-workspace-canvas', 'class', 'WorkspaceCanvas', 'src/lib/components/blocks/WorkspaceCanvas.svelte', 'svelte', 'sovereign-web', 750, 'Drag-drop composable block layout with design mode'),
            this._mkElem('fe-composable-block', 'class', 'ComposableBlock', 'src/lib/components/blocks/ComposableBlock.svelte', 'svelte', 'sovereign-web', 820, 'Universal block renderer for all dashboard modules'),
            this._mkElem('fe-superapp', 'class', 'SovereignSuperApp', 'src/lib/components/dashboard/SovereignSuperApp.svelte', 'svelte', 'sovereign-web', 2040, 'SuperApp terminal: trade, predict, card, ramp, agents, yield'),
            this._mkElem('fe-dashboard', 'module', 'DashboardPage', 'src/routes/dashboard/+page.svelte', 'svelte', 'sovereign-web', 381, 'Main dashboard with module orchestration and command palette'),

            // ── RUST KERNEL ──
            this._mkElem('rs-consensus', 'module', 'ConsensusEngine', 'kernel/rust/src/consensus.rs', 'rust', 'kernel/rust', 450, 'BFT consensus layer with validator set management and block finality'),
            this._mkElem('rs-zkproof', 'module', 'ZKProofVerifier', 'kernel/rust/src/zk_verifier.rs', 'rust', 'kernel/rust', 380, 'Zero-knowledge proof verification — Groth16, PLONK, STARK, SP1'),
            this._mkElem('rs-state', 'module', 'StateManager', 'kernel/rust/src/state.rs', 'rust', 'kernel/rust', 520, 'Sovereign state tree with Merkle proofs and stateless verification'),
            this._mkElem('rs-runtime', 'module', 'SovereignRuntime', 'kernel/rust/src/runtime.rs', 'rust', 'kernel/rust', 610, 'WASM execution runtime for sovereign applications'),
            this._mkElem('rs-p2p', 'module', 'MeshNetwork', 'kernel/rust/src/p2p.rs', 'rust', 'kernel/rust', 340, 'Peer-to-peer mesh networking for validator communication'),

            // ── ELIXIR BACKPLANE ──
            this._mkElem('ex-backplane', 'module', 'BackplaneOrchestrator', 'kernel/elixir/lib/backplane.ex', 'elixir', 'kernel/elixir', 490, 'Real-time event distribution and manifold synchronization'),
            this._mkElem('ex-governance', 'module', 'GovernanceEngine', 'kernel/elixir/lib/governance.ex', 'elixir', 'kernel/elixir', 560, 'DAO governance with proposal lifecycle, voting, and execution'),
            this._mkElem('ex-settlement', 'module', 'SettlementLayer', 'kernel/elixir/lib/settlement.ex', 'elixir', 'kernel/elixir', 410, 'Cross-chain settlement finality with batch verification'),
            this._mkElem('ex-telemetry', 'module', 'TelemetryReactor', 'kernel/elixir/lib/telemetry.ex', 'elixir', 'kernel/elixir', 280, 'System telemetry, health monitoring, and SLO tracking'),

            // ── PYTHON AI ──
            this._mkElem('py-ml-pipeline', 'module', 'MLPipeline', 'kernel/python/ml/pipeline.py', 'python', 'kernel/python', 620, 'ML training pipeline with model registry and experiment tracking'),
            this._mkElem('py-rag-engine', 'module', 'RAGEngine', 'kernel/python/rag/engine.py', 'python', 'kernel/python', 480, 'Retrieval-augmented generation for sovereign knowledge base'),
            this._mkElem('py-embeddings', 'module', 'EmbeddingService', 'kernel/python/embeddings/service.py', 'python', 'kernel/python', 320, 'Multi-model embedding generation — OpenAI, local, hybrid'),

            // ── DART MOBILE ──
            this._mkElem('dart-app', 'class', 'SovereignApp', 'age-mobile/lib/main.dart', 'dart', 'age-mobile', 280, 'Flutter mobile app entry point with sovereign design system'),
            this._mkElem('dart-wallet', 'class', 'WalletScreen', 'age-mobile/lib/screens/wallet_screen.dart', 'dart', 'age-mobile', 450, 'Mobile wallet with balance, send, receive, and transaction history'),
            this._mkElem('dart-bento', 'class', 'SovereignBentoGrid', 'age-mobile/lib/widgets/sovereign_bento_grid.dart', 'dart', 'age-mobile', 380, 'Bento grid layout with sovereignty circuit visualization'),

            // ── GO SERVICES ──
            this._mkElem('go-gateway', 'module', 'APIGateway', 'kernel/go/gateway/main.go', 'go', 'kernel/go', 340, 'High-performance API gateway with rate limiting and auth'),
            this._mkElem('go-indexer', 'module', 'BlockIndexer', 'kernel/go/indexer/service.go', 'go', 'kernel/go', 420, 'Block indexing service for chain data aggregation'),
        ];

        // Build cross-references
        const el = (id: string) => elements.find(e => e.id === id);

        const masterStore = el('ts-master');
        const manifoldCtrl = el('ts-manifold');
        const gateway = el('ts-gateway');
        const trading = el('ts-trading');
        const llm = el('ts-llm');
        // const web3 = el('ts-web3');
        const canvas = el('svelte-canvas');
        const block = el('svelte-block');
        const superApp = el('svelte-superapp');
        const dashboard = el('svelte-dashboard');

        if (masterStore && manifoldCtrl) masterStore.dependencies = [manifoldCtrl.id];
        if (masterStore && trading) masterStore.dependencies.push(trading.id);
        if (manifoldCtrl && masterStore) manifoldCtrl.dependencies = [masterStore.id];
        if (gateway && llm) gateway.dependencies = [llm.id];
        if (trading && masterStore) trading.dependencies = [masterStore.id];
        if (trading && el('ts-web3')) trading.dependencies.push(el('ts-web3')!.id);
        if (canvas && block) canvas.dependencies = [block.id];
        if (canvas && masterStore) canvas.dependencies.push(masterStore.id);
        if (block && masterStore) block.dependencies = [masterStore.id];
        if (superApp && trading) superApp.dependencies = [trading.id];
        if (dashboard && masterStore) dashboard.dependencies = [masterStore.id];
        if (dashboard && canvas) dashboard.dependencies.push(canvas.id);
        if (dashboard && superApp) dashboard.dependencies.push(superApp.id);

        // Rust cross-deps
        if (elements[11] && elements[12] && elements[13]) elements[11].dependencies = [elements[12].id, elements[13].id]; // Consensus → ZK, State
        if (elements[12] && elements[13]) elements[12].dependencies = [elements[13].id]; // ZK → State
        if (elements[14] && elements[11]) elements[14].dependencies = [elements[11].id]; // P2P → Consensus

        // Elixir cross-deps
        if (elements[15] && elements[16] && elements[18]) elements[15].dependencies = [elements[16].id, elements[18].id]; // Backplane → Governance, Telemetry
        if (elements[16] && elements[17]) elements[16].dependencies = [elements[17].id]; // Governance → Settlement

        // Python deps
        if (elements[19] && elements[21]) elements[19].dependencies = [elements[21].id]; // MLPipeline → Embeddings
        if (elements[20] && elements[21]) elements[20].dependencies = [elements[21].id]; // RAG → Embeddings

        // Build dependents (reverse index)
        for (const elem of elements) {
            for (const depId of elem.dependencies) {
                const target = elements.find(e => e.id === depId);
                if (target && !target.dependents.includes(elem.id)) {
                    target.dependents.push(elem.id);
                }
            }
        }

        // Index everything
        this.indexElements(elements);
    }

    private _mkElem(
        id: string, type: CodeElementType, name: string, path: string,
        lang: CodeLanguage, repo: string, tokens: number, summary: string
    ): CodeElement {
        return {
            id, type, name, filePath: path, relativePath: path, language: lang,
            startLine: 1, endLine: tokens, signature: `${type} ${name}`,
            docstring: summary, summary, dependencies: [], dependents: [],
            complexity: Math.ceil(tokens / 100), tokenCount: tokens,
            metadata: {}, repoName: repo,
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export const codeIntelligence = new SovereignCodeIntelligence();
