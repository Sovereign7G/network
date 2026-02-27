// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN OPENCODE ENGINE
// ═══════════════════════════════════════════════════════════════════════════════
// Inspired by Oh-My-OpenCode (code-yeongyu) — Multi-Agent Orchestration Framework
// Applies 7 core innovations:
//   1. Multi-Agent Specialization (11 specialized agents with tool restrictions)
//   2. Category System (domain-specific agent presets: deep, quick, visual, ultrabrain)
//   3. Skill System (injectable knowledge + MCP tools with combo strategies)
//   4. Hook System (44 lifecycle hooks across 5 tiers)
//   5. Task System (dependency-aware parallel execution with blockedBy/blocks)
//   6. Background Agents (parallel multi-model execution with result retrieval)
//   7. Self-Referential Loops (Ralph Loop / ULW Loop until-completion patterns)
//
// [IN]:  agent requests, tasks, skills, hooks
// [OUT]: AgentSpecialist[], TaskGraph, HookPipeline, SkillRegistry, LoopController
// ═══════════════════════════════════════════════════════════════════════════════

export * from '../types/opencode-engine.types';
import type {
    AgentRole, AgentSpec, CategoryId,
    CategoryConfig, Skill, HookTier, Hook,
    HookContext, HookResult, Task, TaskGraph, BackgroundAgent,
    LoopType, LoopState, LoopIteration, OpenCodeMetrics
} from '../types/opencode-engine.types';
import { AGENT_SPECS, CATEGORY_PRESETS, BUILTIN_SKILLS, BUILTIN_HOOKS } from '../registries/opencode-engine.registries';



// Registries removed — now imported from ../registries/opencode-engine.registries

// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN OPENCODE ORCHESTRATOR
// ═══════════════════════════════════════════════════════════════════════════════

class SovereignOpenCode {
    // ── Reactive Registries ──
    private agents = new Map<AgentRole, AgentSpec>();
    private categories = new Map<CategoryId, CategoryConfig>();
    private skills = new Map<string, Skill>();
    private hooks = $state<Hook[]>([]);
    private tasks = $state<Task[]>([]);
    private backgroundAgents = $state<BackgroundAgent[]>([]);
    private spaceMemory = $state<Map<string, any>>(new Map()); // Space Intelligence layer
    private activeLoop = $state<LoopState | null>(null);
    private disabledHooks = $state(new Set<string>());

    // ── Reactive Metrics ──
    private _metrics = $state<OpenCodeMetrics>({
        totalAgentInvocations: 0,
        agentUsage: {} as Record<AgentRole, number>,
        categoryUsage: {} as Record<string, number>,
        hooksFired: 0,
        hooksByTier: { context: 0, productivity: 0, quality: 0, recovery: 0, continuation: 0 },
        tasksCreated: 0,
        tasksCompleted: 0,
        tasksFailed: 0,
        backgroundAgentsSpawned: 0,
        loopIterationsTotal: 0,
        skillsLoaded: 0,
        avgTaskLatencyMs: 0,
        avgAgentLatencyMs: 0,
        tokensSaved: 0,
        modelFallbacks: 0,
    });

    constructor() {
        // Initialize non-reactive registries
        for (const spec of AGENT_SPECS) {
            this.agents.set(spec.role, spec);
        }
        for (const cat of CATEGORY_PRESETS) {
            this.categories.set(cat.id, cat);
        }
        for (const skill of BUILTIN_SKILLS) {
            this.skills.set(skill.id, skill);
        }
        // Initialize reactive hooks
        this.hooks = [...BUILTIN_HOOKS];
    }

    // ═══ AGENT DISPATCH ══════════════════════════════════════════════════════

    getAgent(role: AgentRole): AgentSpec | undefined {
        return this.agents.get(role);
    }

    get allAgents(): AgentSpec[] {
        return [...this.agents.values()];
    }

    /**
     * Select the best agent for a given query using keyword matching + category inference.
     */
    selectAgent(query: string, category?: CategoryId): AgentSpec {
        const q = query.toLowerCase();

        // Category-based selection
        if (category) {
            const catConfig = this.categories.get(category);
            if (catConfig?.isUnstable) {
                // Unstable categories force background execution
                return this.agents.get('junior')!;
            }
            // Map category to appropriate agent
            if (['visual-engineering', 'artistry'].includes(category)) return this.agents.get('junior')!;
            if (['ultrabrain', 'deep', 'kernel-ops', 'security-audit'].includes(category)) return this.agents.get('hephaestus')!;
            if (['quick'].includes(category)) return this.agents.get('junior')!;
        }

        // Keyword-based agent selection
        if (q.includes('review') || q.includes('architecture') || q.includes('debug')) return this.agents.get('oracle')!;
        if (q.includes('plan') || q.includes('strategy') || q.includes('design')) return this.agents.get('prometheus')!;
        if (q.includes('search') || q.includes('find') || q.includes('where is')) return this.agents.get('explore')!;
        if (q.includes('documentation') || q.includes('how does') || q.includes('example')) return this.agents.get('librarian')!;
        if (q.includes('image') || q.includes('screenshot') || q.includes('pdf') || q.includes('diagram')) return this.agents.get('multimodal')!;
        if (q.includes('validate') || q.includes('critique') || q.includes('check plan')) return this.agents.get('momus')!;

        // Default: orchestrator
        return this.agents.get('sisyphus')!;
    }

    /**
     * Check if an agent is allowed to use a specific tool.
     */
    isToolAllowed(agent: AgentSpec, toolName: string): boolean {
        if (agent.toolRestrictions.includes('allowlist')) {
            return (agent.allowedTools ?? []).includes(toolName);
        }
        return !agent.blockedTools.includes(toolName);
    }

    // ═══ CATEGORY SYSTEM ═════════════════════════════════════════════════════

    getCategory(id: CategoryId): CategoryConfig | undefined {
        return this.categories.get(id);
    }

    get allCategories(): CategoryConfig[] {
        return [...this.categories.values()];
    }

    /**
     * Auto-detect category from task description — OpenCode's smart routing.
     */
    detectCategory(description: string): CategoryId {
        const d = description.toLowerCase();

        if (d.includes('ui') || d.includes('css') || d.includes('animation') || d.includes('responsive') || d.includes('design')) return 'visual-engineering';
        if (d.includes('architecture') || d.includes('complex') || d.includes('reasoning') || d.includes('analyze deeply')) return 'ultrabrain';
        if (d.includes('fix typo') || d.includes('rename') || d.includes('simple')) return 'quick';
        if (d.includes('creative') || d.includes('artistic') || d.includes('novel')) return 'artistry';
        if (d.includes('document') || d.includes('write') || d.includes('prose')) return 'writing';
        if (d.includes('kernel') || d.includes('rust') || d.includes('elixir') || d.includes('consensus')) return 'kernel-ops';
        if (d.includes('governance') || d.includes('proposal') || d.includes('voting') || d.includes('policy')) return 'governance';
        if (d.includes('security') || d.includes('audit') || d.includes('zk') || d.includes('proof')) return 'security-audit';
        if (d.includes('defi') || d.includes('trading') || d.includes('vault') || d.includes('swap')) return 'sovereign-finance';
        if (d.includes('research') || d.includes('investigate') || d.includes('deep')) return 'deep';

        return 'unspecified-low';
    }

    // ═══ SKILL SYSTEM ════════════════════════════════════════════════════════

    getSkill(id: string): Skill | undefined {
        return this.skills.get(id);
    }

    get allSkills(): Skill[] {
        return [...this.skills.values()];
    }

    /**
     * Auto-detect relevant skills from query/context.
     */
    detectSkills(query: string): Skill[] {
        const q = query.toLowerCase();
        return [...this.skills.values()].filter(skill =>
            skill.triggers.some(trigger => q.includes(trigger.toLowerCase()))
        );
    }

    /**
     * Get combo strategy — matching Category + Skills for optimal agent.
     */
    getComboStrategy(category: CategoryId, query: string): {
        category: CategoryConfig;
        skills: Skill[];
        agent: AgentSpec;
        description: string;
    } {
        const cat = this.categories.get(category)!;
        const skills = this.detectSkills(query);
        const agent = this.selectAgent(query, category);

        return {
            category: cat,
            skills,
            agent,
            description: `${agent.icon} ${agent.name} + ${skills.map(s => s.icon).join('')} [${category}]`,
        };
    }

    // ═══ HOOK PIPELINE ═══════════════════════════════════════════════════════

    get allHooks(): Hook[] {
        return [...this.hooks];
    }

    get hooksByTier(): Record<HookTier, Hook[]> {
        const result: Record<HookTier, Hook[]> = {
            context: [], productivity: [], quality: [], recovery: [], continuation: [],
        };
        for (const hook of this.hooks) {
            result[hook.tier].push(hook);
        }
        return result;
    }

    /**
     * Run hooks for a specific event — sorted by priority, respecting disabled state.
     */
    runHooks(ctx: HookContext): HookResult[] {
        const applicable = this.hooks
            .filter(h => h.enabled && !this.disabledHooks.has(h.id) && h.events.includes(ctx.event))
            .sort((a, b) => b.priority - a.priority);

        const results: HookResult[] = [];
        for (const hook of applicable) {
            try {
                const result = hook.handler(ctx);
                results.push(result);
                this._metrics.hooksFired++;
                this._metrics.hooksByTier[hook.tier]++;

                if (result.action === 'block') break; // Block halts pipeline
            } catch (err) {
                console.warn(`[HOOK ${hook.id}] Error:`, err);
            }
        }
        return results;
    }

    disableHook(hookId: string): void {
        this.disabledHooks.add(hookId);
    }

    enableHook(hookId: string): void {
        this.disabledHooks.delete(hookId);
    }

    addHook(hook: Hook): void {
        this.hooks.push(hook);
        this.hooks.sort((a, b) => b.priority - a.priority);
    }

    // ═══ TASK SYSTEM ═════════════════════════════════════════════════════════

    createTask(opts: {
        subject: string;
        description: string;
        blockedBy?: string[];
        blocks?: string[];
        owner?: AgentRole;
        category?: CategoryId;
        skills?: string[];
    }): Task {
        const task: Task = {
            id: `T-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
            subject: opts.subject,
            description: opts.description,
            status: 'pending',
            blocks: opts.blocks ?? [],
            blockedBy: opts.blockedBy ?? [],
            owner: opts.owner ?? undefined,
            category: opts.category ?? undefined,
            skills: opts.skills ?? undefined,
            metadata: {},
            createdAt: Date.now(),
        };
        this.tasks.push(task);
        this._metrics.tasksCreated++;
        return task;
    }

    getTask(id: string): Task | undefined {
        return this.tasks.find(t => t.id === id);
    }

    get allTasks(): Task[] {
        return this.tasks;
    }

    pendingTasks = $derived(this.tasks.filter(t => t.status === 'pending'));

    runnableTasks = $derived.by(() => {
        return this.tasks.filter(t => {
            if (t.status !== 'pending') return false;
            // All blockers must be completed
            return t.blockedBy.every(blockerId => {
                const b = this.tasks.find(tk => tk.id === blockerId);
                return b?.status === 'completed';
            });
        });
    });

    updateTask(id: string, updates: Partial<Task>): Task | undefined {
        const task = this.tasks.find(t => t.id === id);
        if (!task) return undefined;
        Object.assign(task, updates);

        if (updates.status === 'completed') {
            task.completedAt = Date.now();
            this._metrics.tasksCompleted++;
        }
        if (updates.status === 'failed') {
            task.completedAt = Date.now();
            this._metrics.tasksFailed++;
        }
        return task;
    }

    /**
     * Build task execution graph with parallel groups.
     */
    buildTaskGraph(): TaskGraph {
        const taskMap = new Map<string, Task>(this.tasks.map(t => [t.id, t]));
        const executionOrder: string[] = [];
        const visited = new Set<string>();

        const visit = (id: string, stack: Set<string>) => {
            if (visited.has(id) || stack.has(id)) return;
            stack.add(id);
            const task = taskMap.get(id);
            if (task) {
                for (const dep of task.blockedBy) visit(dep, stack);
                visited.add(id);
                executionOrder.push(id);
            }
            stack.delete(id);
        };

        for (const t of this.tasks) visit(t.id, new Set());

        const depths = new Map<string, number>();
        for (const id of executionOrder) {
            const task = taskMap.get(id)!;
            const maxDepth = task.blockedBy.reduce((m: number, bid: string) => Math.max(m, (depths.get(bid) ?? 0) + 1), 0);
            depths.set(id, maxDepth);
        }

        const groupsMap = new Map<number, string[]>();
        for (const [id, depth] of depths) {
            if (!groupsMap.has(depth)) groupsMap.set(depth, []);
            groupsMap.get(depth)!.push(id);
        }

        const parallelGroups = [...groupsMap.entries()]
            .sort(([a], [b]) => a - b)
            .map(([, group]) => group);

        return { tasks: taskMap, executionOrder, parallelGroups };
    }

    // ═══ BACKGROUND AGENTS ═══════════════════════════════════════════════════

    spawnBackground(opts: {
        agentRole: AgentRole;
        category?: CategoryId;
        skills?: string[];
        prompt: string;
    }): BackgroundAgent {
        const bg: BackgroundAgent = {
            taskId: `bg_${Date.now().toString(36)}`,
            agentRole: opts.agentRole,
            category: opts.category ?? undefined,
            skills: opts.skills ?? [],
            prompt: opts.prompt,
            status: 'running',
            startedAt: Date.now(),
        };
        this.backgroundAgents.push(bg);
        this._metrics.backgroundAgentsSpawned++;

        setTimeout(() => {
            bg.status = 'completed';
            bg.completedAt = Date.now();
            bg.result = { message: `Background task completed by ${opts.agentRole}` };
        }, 3000);

        return bg;
    }

    getBackgroundResult(taskId: string): BackgroundAgent | undefined {
        return this.backgroundAgents.find(a => a.taskId === taskId);
    }

    activeBackgroundAgents = $derived(this.backgroundAgents.filter(a => a.status === 'running'));

    // ═══ SPACE INTELLIGENCE (Memory Pool) ═════════════════════════════════════

    saveToSpace(key: string, value: any): void {
        this.spaceMemory.set(key, value);
    }

    getFromSpace(key: string): any {
        return this.spaceMemory.get(key);
    }

    get allSpaceMemory() {
        return Array.from(this.spaceMemory.entries());
    }

    // ═══ LOOP SYSTEM ═════════════════════════════════════════════════════════

    startLoop(type: LoopType, objective: string, maxIterations = 100): LoopState {
        this.activeLoop = {
            type,
            iteration: 0,
            maxIterations,
            objective,
            isComplete: false,
            completionSignal: '<promise>DONE</promise>',
            history: [],
            startedAt: Date.now(),
        };
        return this.activeLoop;
    }

    advanceLoop(action: string, result: string, tokensUsed: number): LoopState | null {
        if (!this.activeLoop || this.activeLoop.isComplete) return null;

        const iteration: LoopIteration = {
            index: this.activeLoop.iteration,
            action,
            result,
            tokensUsed,
            durationMs: Date.now() - this.activeLoop.startedAt,
        };
        this.activeLoop.history.push(iteration);
        this.activeLoop.iteration++;
        this._metrics.loopIterationsTotal++;

        if (result.includes(this.activeLoop.completionSignal) || this.activeLoop.iteration >= this.activeLoop.maxIterations) {
            this.activeLoop.isComplete = true;
        }

        return this.activeLoop;
    }

    cancelLoop(): void {
        if (this.activeLoop) this.activeLoop.isComplete = true;
    }

    get loopState(): LoopState | null {
        return this.activeLoop;
    }

    // ═══ METRICS & STATS ═════════════════════════════════════════════════════

    updateMetrics(updates: Partial<OpenCodeMetrics>): void {
        Object.assign(this._metrics, updates);
    }

    get metrics(): OpenCodeMetrics {
        return this._metrics;
    }

    stats = $derived.by(() => {
        return {
            agentCount: this.agents.size,
            categoryCount: this.categories.size,
            skillCount: this.skills.size,
            hookCount: this.hooks.length,
            activeHookCount: this.hooks.filter(h => h.enabled && !this.disabledHooks.has(h.id)).length,
            taskCount: this.tasks.length,
            backgroundCount: this.backgroundAgents.length,
            loopActive: !!this.activeLoop && !this.activeLoop.isComplete,
        };
    });
}

// ─── SINGLETON ───────────────────────────────────────────────────────────────

export const sovereignOpenCode: SovereignOpenCode = new SovereignOpenCode();


