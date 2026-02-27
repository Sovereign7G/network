// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ OPENCODE ENGINE REGISTRIES
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  opencode-engine.types.ts
// [OUT]: AGENT_SPECS, CATEGORY_PRESETS, BUILTIN_SKILLS, BUILTIN_HOOKS
// [POS]: Static configuration data for the OpenCode engine. consolidates
//        knowledge and defaults per Ousterhout's principle of separating
//        general-purpose logic from special-purpose configuration.
// Protocol: When updating me, sync this header + parent folder's .folder.md
// ═══════════════════════════════════════════════════════════════════════════════

import type { AgentSpec, CategoryConfig, Skill, Hook } from '../types/opencode-engine.types';

// ─── AGENT SPECIALISTS REGISTRY ──────────────────────────────────────────────

export const AGENT_SPECS: AgentSpec[] = [
    {
        role: 'sisyphus',
        name: 'Sisyphus · Sovereign Orchestrator',
        description: 'Default orchestrator. Plans, delegates, and executes using specialized subagents with parallel execution. Todo-driven workflow with extended thinking.',
        defaultModel: 'claude-opus-4',
        fallbackChain: ['gpt-5-codex', 'claude-sonnet-4', 'gemini-3-pro'],
        toolRestrictions: [],
        blockedTools: [],
        maxThinkingBudget: 32000,
        capabilities: ['plan', 'delegate', 'execute', 'parallel', 'monitor'],
        icon: '🏔️',
    },
    {
        role: 'hephaestus',
        name: 'Hephaestus · Deep Craftsman',
        description: 'Autonomous deep worker. Goal-oriented execution with thorough research before action. Explores codebase patterns, completes tasks end-to-end.',
        defaultModel: 'gpt-5-codex',
        fallbackChain: ['claude-opus-4', 'claude-sonnet-4'],
        toolRestrictions: [],
        blockedTools: [],
        maxThinkingBudget: 64000,
        capabilities: ['research', 'implement', 'refactor', 'test', 'document'],
        icon: '🔨',
    },
    {
        role: 'oracle',
        name: 'Oracle · Sovereign Advisor',
        description: 'Read-only consultant for architecture decisions, code review, and debugging. Stellar logical reasoning.',
        defaultModel: 'gpt-5-codex',
        fallbackChain: ['claude-opus-4', 'claude-sonnet-4'],
        toolRestrictions: ['read_only'],
        blockedTools: ['write', 'edit', 'task', 'call_agent'],
        maxThinkingBudget: 32000,
        capabilities: ['review', 'analyze', 'advise', 'debug'],
        icon: '🔮',
    },
    {
        role: 'librarian',
        name: 'Librarian · Knowledge Curator',
        description: 'Multi-repo analysis, documentation lookup, OSS implementation examples. Deep codebase understanding with evidence-based answers.',
        defaultModel: 'claude-sonnet-4',
        fallbackChain: ['claude-haiku-4', 'gpt-5-mini'],
        toolRestrictions: ['no_write', 'no_edit', 'no_delegate'],
        blockedTools: ['write', 'edit', 'task', 'call_agent'],
        maxThinkingBudget: 16000,
        capabilities: ['search', 'document', 'reference', 'explain'],
        icon: '📚',
    },
    {
        role: 'explore',
        name: 'Explore · Fast Scout',
        description: 'Fast codebase exploration and contextual grep. Lightweight and rapid.',
        defaultModel: 'claude-haiku-4',
        fallbackChain: ['gpt-5-mini', 'gemini-3-flash'],
        toolRestrictions: ['no_write', 'no_edit', 'no_delegate'],
        blockedTools: ['write', 'edit', 'task', 'call_agent'],
        maxThinkingBudget: 4000,
        capabilities: ['grep', 'glob', 'navigate', 'skim'],
        icon: '🗺️',
    },
    {
        role: 'multimodal',
        name: 'Multimodal Looker · Visual Analyst',
        description: 'Visual content specialist. Analyzes PDFs, images, diagrams to extract information.',
        defaultModel: 'gemini-3-pro',
        fallbackChain: ['gemini-3-flash', 'claude-opus-4', 'claude-sonnet-4'],
        toolRestrictions: ['allowlist'],
        blockedTools: [],
        allowedTools: ['read', 'look_at'],
        maxThinkingBudget: 8000,
        capabilities: ['vision', 'ocr', 'diagram', 'pdf'],
        icon: '👁️',
    },
    {
        role: 'prometheus',
        name: 'Prometheus · Strategic Planner',
        description: 'Strategic planner with interview mode. Creates detailed work plans through iterative questioning.',
        defaultModel: 'claude-opus-4',
        fallbackChain: ['gpt-5-codex', 'claude-sonnet-4'],
        toolRestrictions: [],
        blockedTools: [],
        maxThinkingBudget: 32000,
        capabilities: ['plan', 'interview', 'decompose', 'prioritize'],
        icon: '🔥',
    },
    {
        role: 'metis',
        name: 'Metis · Plan Consultant',
        description: 'Pre-planning analysis. Identifies hidden intentions, ambiguities, and AI failure points.',
        defaultModel: 'claude-opus-4',
        fallbackChain: ['gpt-5-codex', 'claude-sonnet-4'],
        toolRestrictions: [],
        blockedTools: [],
        maxThinkingBudget: 32000,
        capabilities: ['analyze', 'critique', 'anticipate', 'validate'],
        icon: '🦉',
    },
    {
        role: 'momus',
        name: 'Momus · Plan Critic',
        description: 'Plan reviewer — validates plans against clarity, verifiability, and completeness standards.',
        defaultModel: 'gpt-5-codex',
        fallbackChain: ['claude-opus-4'],
        toolRestrictions: ['no_write', 'no_edit', 'no_delegate'],
        blockedTools: ['write', 'edit', 'task'],
        maxThinkingBudget: 16000,
        capabilities: ['review', 'score', 'critique', 'verify'],
        icon: '🎭',
    },
    {
        role: 'atlas',
        name: 'Atlas · Task Executor',
        description: 'Todo-list orchestrator. Executes planned tasks systematically, managing todo items and coordinating work.',
        defaultModel: 'claude-sonnet-4',
        fallbackChain: ['claude-opus-4', 'gpt-5-codex'],
        toolRestrictions: ['no_delegate'],
        blockedTools: ['task', 'call_agent'],
        maxThinkingBudget: 16000,
        capabilities: ['execute', 'track', 'verify', 'report'],
        icon: '🌍',
    },
    {
        role: 'junior',
        name: 'Sisyphus-Junior · Delegated Executor',
        description: 'Category-spawned executor. Cannot re-delegate tasks. Model selected by category.',
        defaultModel: 'claude-sonnet-4',
        fallbackChain: ['claude-haiku-4', 'gpt-5-mini'],
        toolRestrictions: ['no_delegate'],
        blockedTools: ['task', 'call_agent'],
        maxThinkingBudget: 8000,
        capabilities: ['execute', 'implement'],
        icon: '⚡',
    },
    {
        role: 'spacebot',
        name: 'Spacebot · Concurrent Intelligence',
        description: 'Multi-user concurrent agent. Thinks, executes, and responds in parallel. Never blocks, never forgets. Powered by Space Intelligence shared memory.',
        defaultModel: 'claude-opus-4',
        fallbackChain: ['gpt-5-codex', 'gemini-3-pro'],
        toolRestrictions: [],
        blockedTools: [],
        maxThinkingBudget: 64000,
        capabilities: ['concurrency', 'memory', 'collaborate', 'execute'],
        icon: '🌌',
    },
];

// ─── CATEGORY PRESETS ────────────────────────────────────────────────────────

export const CATEGORY_PRESETS: CategoryConfig[] = [
    {
        id: 'visual-engineering',
        description: 'Frontend, UI/UX, design, styling, animation',
        defaultModel: 'gemini-3-pro',
        modelTier: 'quality',
        temperature: 0.7,
        topP: 0.95,
        promptAppend: 'You are a designer-turned-developer. Craft stunning UI/UX with bold aesthetic direction, distinctive typography, and cohesive color palettes.',
        maxTokens: 8000,
        thinkingBudget: 16000,
        reasoningEffort: 'medium',
        isUnstable: false,
    },
    {
        id: 'ultrabrain',
        description: 'Deep logical reasoning, complex architecture decisions requiring extensive analysis',
        defaultModel: 'gpt-5-codex',
        modelTier: 'max',
        temperature: 0.3,
        topP: 0.9,
        promptAppend: 'Apply maximum logical rigor. Think step-by-step. Consider edge cases exhaustively. Provide formal reasoning where possible.',
        maxTokens: 16000,
        thinkingBudget: 64000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'deep',
        description: 'Goal-oriented autonomous problem-solving. Thorough research before action.',
        defaultModel: 'gpt-5-codex',
        modelTier: 'quality',
        temperature: 0.5,
        topP: 0.9,
        promptAppend: 'Autonomous deep worker. Research thoroughly before acting. Complete tasks end-to-end without premature stopping.',
        maxTokens: 12000,
        thinkingBudget: 32000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'artistry',
        description: 'Highly creative/artistic tasks, novel ideas',
        defaultModel: 'gemini-3-pro',
        modelTier: 'max',
        temperature: 1.2,
        topP: 0.98,
        promptAppend: 'Be maximally creative. Push boundaries. Surprise with unexpected but delightful solutions.',
        maxTokens: 8000,
        thinkingBudget: 16000,
        reasoningEffort: 'medium',
        isUnstable: false,
    },
    {
        id: 'quick',
        description: 'Trivial tasks — single file changes, typo fixes, simple modifications',
        defaultModel: 'claude-haiku-4',
        modelTier: 'speed',
        temperature: 0.3,
        topP: 0.85,
        promptAppend: 'Be concise and fast. Make the minimal change needed. Do not over-engineer.',
        maxTokens: 2000,
        thinkingBudget: 2000,
        reasoningEffort: 'low',
        isUnstable: false,
    },
    {
        id: 'unspecified-low',
        description: 'Default for low-effort tasks',
        defaultModel: 'claude-sonnet-4',
        modelTier: 'balanced',
        temperature: 0.5,
        topP: 0.9,
        promptAppend: '',
        maxTokens: 4000,
        thinkingBudget: 8000,
        reasoningEffort: 'medium',
        isUnstable: false,
    },
    {
        id: 'unspecified-high',
        description: 'Default for high-effort tasks',
        defaultModel: 'claude-opus-4',
        modelTier: 'quality',
        temperature: 0.5,
        topP: 0.9,
        promptAppend: '',
        maxTokens: 8000,
        thinkingBudget: 32000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'writing',
        description: 'Documentation, prose, technical writing',
        defaultModel: 'claude-sonnet-4',
        modelTier: 'balanced',
        temperature: 0.8,
        topP: 0.95,
        promptAppend: 'Write clearly and engagingly. Use active voice. Organize with headers and examples.',
        maxTokens: 8000,
        thinkingBudget: 8000,
        reasoningEffort: 'medium',
        isUnstable: false,
    },
    {
        id: 'kernel-ops',
        description: 'Rust/Elixir/Go kernel operations — p2p, consensus, ZK',
        defaultModel: 'gpt-5-codex',
        modelTier: 'deep',
        temperature: 0.2,
        topP: 0.85,
        promptAppend: 'Systems-level precision. Rust safety guarantees are paramount. Consider memory, concurrency, and formal verification.',
        maxTokens: 12000,
        thinkingBudget: 32000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'governance',
        description: 'DAO proposals, voting, policy fabrication, diplomacy',
        defaultModel: 'claude-opus-4',
        modelTier: 'quality',
        temperature: 0.4,
        topP: 0.9,
        promptAppend: 'Governance precision. Consider game theory, incentive alignment, and constitutional constraints. All proposals must be verifiable.',
        maxTokens: 8000,
        thinkingBudget: 32000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'security-audit',
        description: 'ZK proofs, smart contract security, adversarial analysis',
        defaultModel: 'claude-opus-4',
        modelTier: 'max',
        temperature: 0.1,
        topP: 0.8,
        promptAppend: 'Security-first analysis. Assume adversarial actors. Check for reentrancy, overflow, front-running, and privilege escalation.',
        maxTokens: 16000,
        thinkingBudget: 64000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
    {
        id: 'sovereign-finance',
        description: 'DeFi protocols, trading engine, vault operations, payment flows',
        defaultModel: 'gpt-5-codex',
        modelTier: 'quality',
        temperature: 0.3,
        topP: 0.85,
        promptAppend: 'Financial precision. All calculations must be exact. Consider slippage, MEV, oracle manipulation, and liquidity risks.',
        maxTokens: 8000,
        thinkingBudget: 32000,
        reasoningEffort: 'high',
        isUnstable: false,
    },
];

// ─── BUILT-IN SKILLS ─────────────────────────────────────────────────────────

export const BUILTIN_SKILLS: Skill[] = [
    {
        id: 'git-master',
        name: 'Git Master',
        description: 'Commit Architect + Rebase Surgeon + History Archaeologist. Auto-detects commit style, splits atomic commits, formulates rebase strategies.',
        triggers: ['commit', 'rebase', 'squash', 'who wrote', 'git log', 'git blame', 'when was'],
        promptInjection: `You are a Git expert with three specializations:
1. COMMIT ARCHITECT: Split changes into atomic commits. 3+ files → 2+ commits, 5+ files → 3+, 10+ files → 5+. Auto-detect language and style from last 30 commits.
2. REBASE SURGEON: History rewriting, conflict resolution, branch cleanup.
3. HISTORY ARCHAEOLOGIST: Find when/where specific changes were introduced.`,
        icon: '🌿',
    },
    {
        id: 'frontend-ui-ux',
        name: 'Frontend UI/UX Designer',
        description: 'Designer-turned-developer persona. Crafts stunning UI/UX with bold aesthetics, distinctive typography, cohesive palettes.',
        triggers: ['ui', 'ux', 'design', 'styling', 'animation', 'component', 'layout'],
        promptInjection: `Design Process: Purpose → Tone → Constraints → Differentiation.
Aesthetic Direction: Choose extreme — brutalist, maximalist, retro-futuristic, luxury, playful.
Typography: Distinctive fonts. AVOID generic (Inter, Roboto, Arial).
Color: Cohesive palettes with sharp accents. AVOID purple-on-white AI slop.
Motion: High-impact staggered reveals, scroll-triggered, surprising hover states.
Anti-Patterns: Generic fonts, predictable layouts, cookie-cutter components.`,
        icon: '🎨',
    },
    {
        id: 'sovereign-kernel',
        name: 'Sovereign Kernel Specialist',
        description: 'Deep knowledge of AGE Protocol kernel architecture across Rust, Elixir, Python, Go.',
        triggers: ['kernel', 'p2p', 'consensus', 'backplane', 'rag', 'gateway', 'mesh'],
        promptInjection: `You are a kernel specialist for the AGE Protocol sovereign stack:
- Rust Kernel: p2p mesh networking, consensus engine, ZK proof verification
- Elixir Backplane: real-time event distribution, manifold synchronization, GenServer orchestration
- Python RAG: retrieval-augmented generation, embedding pipelines, knowledge base
- Go Gateway: API routing, rate limiting, authentication middleware
Always consider cross-kernel communication patterns and the sovereign trust model.`,
        icon: '⚙️',
    },
    {
        id: 'zk-prover',
        name: 'Zero-Knowledge Specialist',
        description: 'ZK-proof generation, verification circuits, privacy-preserving computation.',
        triggers: ['zk', 'zero-knowledge', 'proof', 'circuit', 'plonk', 'groth16', 'snark', 'stark'],
        promptInjection: `Expert in zero-knowledge proof systems:
- Circuit design, constraint generation, witness computation
- Multi-prover diversity (Plonk, Groth16, STARK, Halo2)
- Batch verification for throughput optimization
- Client-side proving for sovereign privacy
Apply zkEVM statelessness and proof-verified execution patterns.`,
        icon: '🔐',
    },
    {
        id: 'defi-architect',
        name: 'DeFi Architecture Specialist',
        description: 'Decentralized finance protocol design, AMM mechanics, vault strategies.',
        triggers: ['defi', 'amm', 'vault', 'yield', 'liquidity', 'swap', 'trading', 'settlement'],
        promptInjection: `Sovereign DeFi specialist. Design patterns:
- Cross-chain AMMs with sovereign settlement
- Vault strategies with risk-adjusted rebalancing
- MEV-resistant order execution
- Oracle-resilient price feeds with multi-source aggregation
All financial operations must be deterministic and auditable.`,
        icon: '💎',
    },
    {
        id: 'browser-automation',
        name: 'Browser Automation',
        description: 'Playwright-powered browser interaction, testing, screenshots, web scraping.',
        triggers: ['browser', 'playwright', 'screenshot', 'scrape', 'test', 'e2e'],
        promptInjection: 'Use Playwright MCP for all browser tasks. MUST USE for verification, browsing, web scraping, testing, and screenshots.',
        mcpServers: [{ name: 'playwright', command: 'npx', args: ['@playwright/mcp@latest'] }],
        icon: '🌐',
    },
];

// ─── BUILT-IN HOOKS ──────────────────────────────────────────────────────────

export const BUILTIN_HOOKS: Hook[] = [
    {
        id: 'hook-context-inject',
        name: 'Context Injection',
        description: 'Auto-injects AGENTS.md when reading files. Walks from file to project root.',
        events: ['PreToolUse', 'PostToolUse'],
        tier: 'context',
        priority: 100,
        enabled: true,
        handler: (ctx) => {
            if (ctx.event === 'PreToolUse' && ctx.toolName === 'read') {
                return { action: 'inject', injectedContext: '// Sovereign context injected' };
            }
            return { action: 'continue' };
        },
    },
    {
        id: 'hook-context-window',
        name: 'Context Window Monitor',
        description: 'Monitors context window usage and tracks token consumption.',
        events: ['Event'],
        tier: 'context',
        priority: 95,
        enabled: true,
        handler: (ctx) => {
            if (ctx.contextWindowUsage > 0.85) {
                return { action: 'inject', message: '⚠️ Context window at 85%+. Consider compacting.' };
            }
            return { action: 'continue' };
        },
    },
    {
        id: 'hook-preemptive-compact',
        name: 'Preemptive Compaction',
        description: 'Proactively compacts sessions before hitting token limits.',
        events: ['Event'],
        tier: 'context',
        priority: 90,
        enabled: true,
        handler: (ctx) => {
            if (ctx.contextWindowUsage > 0.95) {
                return { action: 'modify', message: '🔄 Preemptive compaction triggered.' };
            }
            return { action: 'continue' };
        },
    },
    {
        id: 'hook-keyword-detector',
        name: 'Keyword Detector',
        description: 'Detects keywords and activates modes: ultrawork, search, analyze.',
        events: ['Message', 'Transform'],
        tier: 'productivity',
        priority: 80,
        enabled: true,
        handler: (ctx) => {
            const msg = (ctx.message || '').toLowerCase();
            if (msg.includes('ultrawork') || msg.includes('ulw')) {
                return { action: 'inject', injectedContext: 'MODE: ULTRAWORK — Maximum parallel execution, aggressive exploration.' };
            }
            if (msg.includes('analyze') || msg.includes('investigate')) {
                return { action: 'inject', injectedContext: 'MODE: DEEP ANALYSIS — Thorough investigation required.' };
            }
            return { action: 'continue' };
        },
    },
    {
        id: 'hook-think-mode',
        name: 'Think Mode Detector',
        description: 'Auto-detects extended thinking needs. Catches "think deeply", "ultrathink".',
        events: ['Params'],
        tier: 'productivity',
        priority: 75,
        enabled: true,
        handler: (ctx) => {
            const msg = (ctx.message || '').toLowerCase();
            if (msg.includes('think deeply') || msg.includes('ultrathink')) {
                // This is a partial implementation showing the concept
                return { action: 'modify', injectedContext: 'MODE: ULTRATHINK — Maximum thought iteration.' };
            }
            return { action: 'continue' };
        },
    },
];
