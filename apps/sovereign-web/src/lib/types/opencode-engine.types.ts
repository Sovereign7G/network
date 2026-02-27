// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ OPENCODE ENGINE TYPE DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  None (pure type definitions)
// [OUT]: All OpenCode types — Agents, Categories, Skills, Hooks, Tasks, Loops
// [POS]: Separated from opencode-engine.svelte.ts per Ousterhout's principle:
//        "Different layer, different abstraction."
// Protocol: When updating me, sync this header + parent folder's .folder.md
// ═══════════════════════════════════════════════════════════════════════════════

// ─── AGENT SPECIALIZATION ────────────────────────────────────────────────────

export type AgentRole =
    | 'sisyphus'        // Default orchestrator — plans, delegates, executes
    | 'hephaestus'      // Deep autonomous worker — goal-oriented, thorough research
    | 'oracle'          // Read-only consultant — architecture, review, debugging
    | 'librarian'       // Multi-repo analysis — documentation, OSS examples
    | 'explore'         // Fast codebase exploration — contextual grep
    | 'multimodal'      // Visual content specialist — PDFs, images, diagrams
    | 'prometheus'      // Strategic planner — iterative questioning, work plans
    | 'metis'           // Plan consultant — hidden intentions, ambiguities
    | 'momus'           // Plan reviewer — clarity, verifiability, completeness
    | 'atlas'           // Todo-list orchestrator — systematic task execution
    | 'spacebot'        // Concurrent agent — multi-user, non-blocking, shared memory
    | 'junior';         // Category-spawned executor — delegated specialist

export type ToolRestriction = 'read_only' | 'no_write' | 'no_edit' | 'no_delegate' | 'allowlist';

export type AgentModelTier = 'speed' | 'balanced' | 'quality' | 'deep' | 'max';

export interface AgentSpec {
    role: AgentRole;
    name: string;
    description: string;
    defaultModel: string;
    fallbackChain: string[];
    toolRestrictions: ToolRestriction[];
    blockedTools: string[];
    allowedTools?: string[];  // Only for allowlist mode
    maxThinkingBudget: number;
    capabilities: string[];
    icon: string;
}

// ─── CATEGORY SYSTEM ─────────────────────────────────────────────────────────

export type CategoryId =
    | 'visual-engineering'  // Frontend, UI/UX, design, styling, animation
    | 'ultrabrain'          // Deep logical reasoning, complex architecture
    | 'deep'                // Goal-oriented autonomous problem-solving
    | 'artistry'            // Highly creative/artistic tasks
    | 'quick'               // Trivial tasks — single file changes, typos
    | 'unspecified-low'     // Default low-effort
    | 'unspecified-high'    // Default high-effort
    | 'writing'             // Documentation, prose, technical writing
    | 'kernel-ops'          // Rust/Elixir/Go kernel operations
    | 'governance'          // DAO proposals, voting, policy
    | 'security-audit'      // ZK proofs, security review
    | 'sovereign-finance';  // DeFi, trading, vault operations

export interface CategoryConfig {
    id: CategoryId;
    description: string;
    defaultModel: string;
    modelTier: AgentModelTier;
    temperature: number;
    topP: number;
    promptAppend: string;
    maxTokens: number;
    thinkingBudget: number;
    reasoningEffort: 'low' | 'medium' | 'high';
    isUnstable: boolean;  // Forces background mode
}

// ─── SKILL SYSTEM ────────────────────────────────────────────────────────────

export interface Skill {
    id: string;
    name: string;
    description: string;
    triggers: string[];            // Keywords that auto-activate this skill
    promptInjection: string;       // Injected into system prompt
    mcpServers?: MCPServerConfig[];
    category?: CategoryId;
    icon: string;
}

export interface MCPServerConfig {
    name: string;
    command: string;
    args: string[];
    env?: Record<string, string>;
}

// ─── HOOK SYSTEM ─────────────────────────────────────────────────────────────

export type HookEvent =
    | 'PreToolUse'     // Before tool execution — block, modify, inject
    | 'PostToolUse'    // After tool execution — warnings, modify output
    | 'Message'        // During message processing — transform, detect keywords
    | 'Event'          // Session lifecycle — recovery, fallback
    | 'Transform'      // Context transformation — inject context
    | 'Params';        // API parameters — adjust model settings

export type HookTier =
    | 'context'        // Context & Injection
    | 'productivity'   // Productivity & Control
    | 'quality'        // Quality & Safety
    | 'recovery'       // Recovery & Stability
    | 'continuation';  // Continuation & Orchestration

export interface Hook {
    id: string;
    name: string;
    description: string;
    events: HookEvent[];
    tier: HookTier;
    priority: number;          // Higher = runs first
    enabled: boolean;
    handler: (ctx: HookContext) => HookResult;
}

export interface HookContext {
    event: HookEvent;
    toolName?: string;
    toolInput?: unknown;
    toolOutput?: unknown;
    message?: string;
    sessionId: string;
    agentRole: AgentRole;
    contextWindowUsage: number;  // 0.0 - 1.0
    metadata: Record<string, unknown>;
}

export interface HookResult {
    action: 'continue' | 'block' | 'modify' | 'inject';
    modifiedInput?: unknown;
    modifiedOutput?: unknown;
    injectedContext?: string;
    message?: string;
}

// ─── TASK SYSTEM ─────────────────────────────────────────────────────────────

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'failed' | 'deleted';

export interface Task {
    id: string;                     // T-{uuid}
    subject: string;                // Imperative: "Run tests"
    description: string;
    status: TaskStatus;
    activeForm?: string;            // Present continuous: "Running tests"
    blocks: string[];               // Task IDs this blocks
    blockedBy: string[];            // Task IDs blocking this
    owner?: AgentRole | undefined;              // Assigned agent
    category?: CategoryId | undefined;
    skills?: string[] | undefined;              // Loaded skills
    metadata: Record<string, unknown>;
    createdAt: number;
    startedAt?: number;
    completedAt?: number;
    result?: unknown;
    error?: string;
}

export interface TaskGraph {
    tasks: Map<string, Task>;
    executionOrder: string[];       // Topologically sorted
    parallelGroups: string[][];     // Groups that can run concurrently
}

// ─── BACKGROUND AGENTS ───────────────────────────────────────────────────────

export interface BackgroundAgent {
    taskId: string;
    agentRole: AgentRole;
    category?: CategoryId | undefined;
    skills: string[];
    prompt: string;
    status: 'running' | 'completed' | 'failed';
    startedAt: number;
    completedAt?: number;
    result?: unknown;
    error?: string;
}

// ─── LOOP SYSTEM ─────────────────────────────────────────────────────────────

export type LoopType = 'ralph' | 'ulw' | 'boulder';

export interface LoopState {
    type: LoopType;
    iteration: number;
    maxIterations: number;
    objective: string;
    isComplete: boolean;
    completionSignal: string;
    history: LoopIteration[];
    startedAt: number;
}

export interface LoopIteration {
    index: number;
    action: string;
    result: string;
    tokensUsed: number;
    durationMs: number;
}

// ─── METRICS ─────────────────────────────────────────────────────────────────

export interface OpenCodeMetrics {
    totalAgentInvocations: number;
    agentUsage: Record<AgentRole, number>;
    categoryUsage: Record<string, number>;
    hooksFired: number;
    hooksByTier: Record<HookTier, number>;
    tasksCreated: number;
    tasksCompleted: number;
    tasksFailed: number;
    backgroundAgentsSpawned: number;
    loopIterationsTotal: number;
    skillsLoaded: number;
    avgTaskLatencyMs: number;
    avgAgentLatencyMs: number;
    tokensSaved: number;
    modelFallbacks: number;
}
