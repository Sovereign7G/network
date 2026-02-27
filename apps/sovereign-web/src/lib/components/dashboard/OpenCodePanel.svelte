<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🏛️ SOVEREIGN OPENCODE CONTROL PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // Oh-My-OpenCode architecture visualization:
    //   Multi-Agent Dispatch, Category System, Skill Combos,
    //   Hook Pipeline, Task Graph, Background Agents, Loop Control
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade } from "svelte/transition";
    import {
        Bot,
        Layers,
        Zap,
        Target,
        Shield,
        Play,
        Square,
        RefreshCw,
        AlertTriangle,
        Search,
        Activity,
        Workflow,
        Terminal,
        Cog,
        Sparkles,
    } from "lucide-svelte";
    import {
        sovereignOpenCode,
        type AgentRole,
        type CategoryId,
    } from "$lib/services/opencode-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<
        "agents" | "categories" | "skills" | "hooks" | "tasks" | "loops"
    >("agents");
    let selectedAgent = $state<AgentRole | null>(null);
    let taskSubject = $state("");
    let taskDescription = $state("");
    let taskBlockedBy = $state("");
    let taskCategory = $state<CategoryId>("unspecified-low");
    let loopObjective = $state("");
    let loopMaxIter = $state(100);
    let queryInput = $state("");

    // ─── DERIVED ────────────────────────────────────────────────────────────

    const engine = sovereignOpenCode;
    let engineStats = $derived(engine.stats);

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    function createTask() {
        if (!taskSubject.trim()) return;
        engine.createTask({
            subject: taskSubject,
            description: taskDescription,
            blockedBy: taskBlockedBy
                .split(",")
                .map((s) => s.trim())
                .filter(Boolean),
            category: taskCategory,
        });
        taskSubject = "";
        taskDescription = "";
        taskBlockedBy = "";
    }

    function startLoop(type: "ralph" | "ulw") {
        if (!loopObjective.trim()) return;
        engine.startLoop(type, loopObjective, loopMaxIter);
    }

    function getDetectedCombo() {
        if (!queryInput.trim()) return null;
        const cat = engine.detectCategory(queryInput);
        return engine.getComboStrategy(cat, queryInput);
    }

    const tabs = [
        { id: "agents" as const, label: "Agents", icon: Bot },
        { id: "categories" as const, label: "Categories", icon: Layers },
        { id: "skills" as const, label: "Skills", icon: Sparkles },
        { id: "hooks" as const, label: "Hooks", icon: Workflow },
        { id: "tasks" as const, label: "Tasks", icon: Target },
        { id: "loops" as const, label: "Loops", icon: RefreshCw },
    ];

    function getTierColor(tier: string): string {
        const c: Record<string, string> = {
            context: "#22d3ee",
            productivity: "#a855f7",
            quality: "#10b981",
            recovery: "#f59e0b",
            continuation: "#ef4444",
        };
        return c[tier] ?? "#888";
    }

    function getStatusColor(status: string): string {
        const c: Record<string, string> = {
            pending: "#64748b",
            in_progress: "#3b82f6",
            completed: "#10b981",
            failed: "#ef4444",
            running: "#3b82f6",
            deleted: "#374151",
        };
        return c[status] ?? "#888";
    }

    function getCategoryColor(cat: string): string {
        const c: Record<string, string> = {
            "visual-engineering": "#f472b6",
            ultrabrain: "#8b5cf6",
            deep: "#6366f1",
            artistry: "#ec4899",
            quick: "#22d3ee",
            "unspecified-low": "#64748b",
            "unspecified-high": "#a78bfa",
            writing: "#fbbf24",
            "kernel-ops": "#dea584",
            governance: "#10b981",
            "security-audit": "#ef4444",
            "sovereign-finance": "#facc15",
        };
        return c[cat] ?? "#888";
    }

    const pipelineEvents: Array<
        | "PreToolUse"
        | "PostToolUse"
        | "Message"
        | "Event"
        | "Transform"
        | "Params"
    > = [
        "PreToolUse",
        "PostToolUse",
        "Message",
        "Event",
        "Transform",
        "Params",
    ];
</script>

<div class="opencode-shell" in:fly={{ y: 20, duration: 400 }}>
    <!-- Institutional Header -->
    <header class="opencode-header">
        <div class="header-brand">
            <div class="logo-box">
                <Terminal size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_OpenCode</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label">OPERATIONAL_STABLE</span>
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block text-right">
                <span class="tel-label">ACTIVE_WORKERS</span>
                <div class="flex items-center gap-1 justify-end">
                    <Activity size={10} class="text-emerald-400" />
                    <span class="tel-value text-emerald-400"
                        >{engineStats.activeHookCount}</span
                    >
                </div>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block text-right">
                <span class="tel-label">PROTOCOL_HOOKS</span>
                <div class="flex items-center gap-1 justify-end">
                    <Workflow size={10} class="text-cyan-400" />
                    <span class="tel-value text-cyan-400"
                        >{engineStats.activeHookCount}/{engineStats.hookCount}</span
                    >
                </div>
            </div>
        </div>
    </header>

    <!-- Smart Route Preview / Search -->
    <div class="opencode-search-area">
        <div class="search-vessel">
            <Search size={14} class="search-icon" />
            <input
                type="text"
                bind:value={queryInput}
                placeholder="Query Intelligence Hub..."
                class="search-input"
            />

            {#if queryInput.trim()}
                {@const combo = getDetectedCombo()}
                <div class="smart-preview" transition:fade>
                    {#if combo}
                        <div class="combo-tag">
                            <span
                                class="text-[7px] font-black text-white/20 uppercase mr-2"
                                >Strategy:</span
                            >
                            <span class="text-white font-black"
                                >{combo.agent.name}</span
                            >
                        </div>
                        <div class="skill-stack">
                            {#each combo.skills as skill}
                                <div class="skill-chip">
                                    <Sparkles size={8} class="text-amber-400" />
                                    <span>{skill}</span>
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <span class="no-skill-tag">NO_SKILL_MATCHED</span>
                    {/if}
                </div>
            {/if}
        </div>
    </div>

    <!-- Tab Navigation -->
    <nav class="opencode-nav">
        {#each tabs as tab}
            <button
                class="nav-btn"
                class:active={activeTab === tab.id}
                onclick={() => (activeTab = tab.id)}
            >
                <tab.icon size={13} />
                <span>{tab.label}</span>
                {#if activeTab === tab.id}
                    <div class="nav-active-bar" in:fade></div>
                {/if}
            </button>
        {/each}
    </nav>

    <!-- Tab Content -->
    <div class="tab-content">
        <!-- ═══ AGENTS TAB ═══ -->
        {#if activeTab === "agents"}
            <div class="agents-grid" in:fade={{ duration: 200 }}>
                {#each engine.allAgents as agent, i (agent.role)}
                    <div
                        class="agent-card"
                        class:selected={selectedAgent === agent.role}
                        in:fly={{ y: 15, delay: i * 40, duration: 250 }}
                        role="button"
                        tabindex="0"
                        onclick={() =>
                            (selectedAgent =
                                selectedAgent === agent.role
                                    ? null
                                    : agent.role)}
                        onkeydown={(e) =>
                            e.key === "Enter" &&
                            (selectedAgent =
                                selectedAgent === agent.role
                                    ? null
                                    : agent.role)}
                    >
                        <div class="agent-header">
                            <span class="agent-icon">{agent.icon}</span>
                            <div class="agent-info">
                                <span class="agent-name">{agent.name}</span>
                                <span class="agent-role">{agent.role}</span>
                            </div>
                        </div>
                        <p class="agent-desc">{agent.description}</p>

                        <div class="agent-model">
                            <span class="model-label">Model:</span>
                            <span class="model-name">{agent.defaultModel}</span>
                        </div>

                        <div class="agent-caps">
                            {#each agent.capabilities as cap}
                                <span class="cap-pill">{cap}</span>
                            {/each}
                        </div>

                        {#if agent.toolRestrictions.length > 0}
                            <div class="agent-restrictions">
                                <Shield size={10} />
                                <span>{agent.toolRestrictions.join(", ")}</span>
                            </div>
                        {/if}

                        {#if selectedAgent === agent.role}
                            <div
                                class="agent-detail"
                                in:fly={{ y: 10, duration: 200 }}
                            >
                                <div class="detail-section">
                                    <span class="detail-label"
                                        >Fallback Chain</span
                                    >
                                    <div class="fallback-chain">
                                        {#each agent.fallbackChain as model, fi}
                                            <span class="fallback-model"
                                                >{model}</span
                                            >
                                            {#if fi < agent.fallbackChain.length - 1}
                                                <span class="fallback-arrow"
                                                    >→</span
                                                >
                                            {/if}
                                        {/each}
                                    </div>
                                </div>
                                {#if agent.blockedTools.length > 0}
                                    <div class="detail-section">
                                        <span class="detail-label"
                                            >Blocked Tools</span
                                        >
                                        <div class="blocked-tools">
                                            {#each agent.blockedTools as tool}
                                                <span class="blocked-pill"
                                                    >🚫 {tool}</span
                                                >
                                            {/each}
                                        </div>
                                    </div>
                                {/if}
                                <div class="detail-section">
                                    <span class="detail-label"
                                        >Thinking Budget</span
                                    >
                                    <span class="detail-value"
                                        >{(
                                            agent.maxThinkingBudget / 1000
                                        ).toFixed(0)}k tokens</span
                                    >
                                </div>
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>

            <!-- ═══ CATEGORIES TAB ═══ -->
        {:else if activeTab === "categories"}
            <div class="categories-grid" in:fade={{ duration: 200 }}>
                {#each engine.allCategories as cat, i (cat.id)}
                    <div
                        class="category-card"
                        in:fly={{ y: 15, delay: i * 35, duration: 250 }}
                        style="--cat-color: {getCategoryColor(cat.id)}"
                    >
                        <div class="cat-header">
                            <span class="cat-id">{cat.id}</span>
                            <span class="cat-tier">{cat.modelTier}</span>
                        </div>
                        <p class="cat-desc">{cat.description}</p>
                        <div class="cat-config">
                            <div class="config-row">
                                <span>Model</span><span>{cat.defaultModel}</span
                                >
                            </div>
                            <div class="config-row">
                                <span>Temperature</span><span
                                    >{cat.temperature}</span
                                >
                            </div>
                            <div class="config-row">
                                <span>Reasoning</span><span
                                    >{cat.reasoningEffort}</span
                                >
                            </div>
                            <div class="config-row">
                                <span>Max Tokens</span><span
                                    >{cat.maxTokens}</span
                                >
                            </div>
                            <div class="config-row">
                                <span>Thinking</span><span
                                    >{(cat.thinkingBudget / 1000).toFixed(
                                        0,
                                    )}k</span
                                >
                            </div>
                        </div>
                        {#if cat.isUnstable}
                            <div class="unstable-badge">
                                <AlertTriangle size={10} /> Unstable — Background
                                Only
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>

            <!-- ═══ SKILLS TAB ═══ -->
        {:else if activeTab === "skills"}
            <div class="skills-section" in:fade={{ duration: 200 }}>
                <div class="skill-combo-guide">
                    <h4>⚡ Category + Skill Combo Strategies</h4>
                    <div class="combo-cards">
                        <div class="combo-card">
                            <span class="combo-title">🎨 The Designer</span>
                            <span class="combo-recipe"
                                >visual-engineering + frontend-ui-ux +
                                browser-automation</span
                            >
                            <span class="combo-effect"
                                >Implements aesthetic UI and verifies rendering
                                in browser</span
                            >
                        </div>
                        <div class="combo-card">
                            <span class="combo-title">🧠 The Architect</span>
                            <span class="combo-recipe"
                                >ultrabrain + (pure reasoning)</span
                            >
                            <span class="combo-effect"
                                >Deep system architecture analysis with maximum
                                logical rigor</span
                            >
                        </div>
                        <div class="combo-card">
                            <span class="combo-title">🏗️ The Maintainer</span>
                            <span class="combo-recipe">quick + git-master</span>
                            <span class="combo-effect"
                                >Fast fixes with clean atomic commits</span
                            >
                        </div>
                        <div class="combo-card">
                            <span class="combo-title">🔐 The Auditor</span>
                            <span class="combo-recipe"
                                >security-audit + zk-prover</span
                            >
                            <span class="combo-effect"
                                >Security review with ZK verification
                                capabilities</span
                            >
                        </div>
                    </div>
                </div>

                <div class="skills-grid">
                    {#each engine.allSkills as skill, i (skill.id)}
                        <div
                            class="skill-card"
                            in:fly={{ y: 15, delay: i * 50, duration: 250 }}
                        >
                            <div class="skill-header">
                                <span class="skill-icon">{skill.icon}</span>
                                <span class="skill-name">{skill.name}</span>
                            </div>
                            <p class="skill-desc">{skill.description}</p>
                            <div class="skill-triggers">
                                {#each skill.triggers as trigger}
                                    <span class="trigger-pill">{trigger}</span>
                                {/each}
                            </div>
                            {#if skill.mcpServers && skill.mcpServers.length > 0}
                                <div class="mcp-badge">
                                    <Cog size={10} />
                                    <span
                                        >MCP: {skill.mcpServers
                                            .map((m) => m.name)
                                            .join(", ")}</span
                                    >
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>

            <!-- ═══ HOOKS TAB ═══ -->
        {:else if activeTab === "hooks"}
            <div class="hooks-section" in:fade={{ duration: 200 }}>
                <div class="hooks-summary">
                    {#each Object.entries(engine.hooksByTier) as [tier, hooks], i}
                        <div
                            class="tier-card"
                            in:fly={{ x: -15, delay: i * 60, duration: 250 }}
                            style="--tier-color: {getTierColor(tier)}"
                        >
                            <div class="tier-header">
                                <span class="tier-dot"></span>
                                <span class="tier-name">{tier}</span>
                                <span class="tier-count">{hooks.length}</span>
                            </div>
                            <div class="tier-hooks">
                                {#each hooks as hook}
                                    <div
                                        class="hook-item"
                                        class:disabled={!hook.enabled}
                                    >
                                        <span class="hook-name"
                                            >{hook.name}</span
                                        >
                                        <div class="hook-events">
                                            {#each hook.events as event}
                                                <span class="event-pill"
                                                    >{event}</span
                                                >
                                            {/each}
                                        </div>
                                        <span class="hook-priority"
                                            >P{hook.priority}</span
                                        >
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>

                <div class="hook-pipeline-viz">
                    <h4>Hook Pipeline: Event Flow</h4>
                    <div class="pipeline-flow">
                        {#each pipelineEvents as event, i}
                            <div
                                class="pipeline-node"
                                in:fly={{
                                    x: -10,
                                    delay: i * 80,
                                    duration: 200,
                                }}
                            >
                                <span class="node-event">{event}</span>
                                <span class="node-count"
                                    >{engine.allHooks.filter((h) =>
                                        h.events.includes(event),
                                    ).length} hooks</span
                                >
                            </div>
                            {#if i < 5}
                                <span class="pipeline-arrow">→</span>
                            {/if}
                        {/each}
                    </div>
                </div>
            </div>

            <!-- ═══ TASKS TAB ═══ -->
        {:else if activeTab === "tasks"}
            <div class="tasks-section" in:fade={{ duration: 200 }}>
                <!-- Task Creator -->
                <div class="task-creator">
                    <h4>📋 Create Task</h4>
                    <div class="task-form">
                        <input
                            type="text"
                            bind:value={taskSubject}
                            placeholder="Subject (imperative: 'Build frontend')"
                            class="task-input"
                        />
                        <input
                            type="text"
                            bind:value={taskDescription}
                            placeholder="Description..."
                            class="task-input"
                        />
                        <div class="task-form-row">
                            <input
                                type="text"
                                bind:value={taskBlockedBy}
                                placeholder="Blocked by (comma-separated IDs)"
                                class="task-input"
                            />
                            <select
                                bind:value={taskCategory}
                                class="task-select"
                            >
                                {#each engine.allCategories as cat}
                                    <option value={cat.id}>{cat.id}</option>
                                {/each}
                            </select>
                            <button
                                class="task-submit"
                                onclick={createTask}
                                disabled={!taskSubject.trim()}
                            >
                                <Play size={12} /> Create
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Task List -->
                <div class="task-list">
                    {#each engine.allTasks as task, i (task.id)}
                        <div
                            class="task-card"
                            in:fly={{ y: 10, delay: i * 40, duration: 200 }}
                        >
                            <div class="task-header">
                                <span
                                    class="task-status"
                                    style="background: {getStatusColor(
                                        task.status,
                                    )}20; color: {getStatusColor(
                                        task.status,
                                    )}; border-color: {getStatusColor(
                                        task.status,
                                    )}40"
                                >
                                    {task.status}
                                </span>
                                <span class="task-id">{task.id}</span>
                                {#if task.category}
                                    <span
                                        class="task-cat"
                                        style="color: {getCategoryColor(
                                            task.category,
                                        )}">{task.category}</span
                                    >
                                {/if}
                            </div>
                            <span class="task-subject">{task.subject}</span>
                            {#if task.blockedBy.length > 0}
                                <div class="task-deps">
                                    <span class="deps-label"
                                        >⛓ Blocked by:</span
                                    >
                                    {#each task.blockedBy as dep}
                                        <span class="dep-pill">{dep}</span>
                                    {/each}
                                </div>
                            {/if}
                        </div>
                    {:else}
                        <div class="empty-state">
                            <Target size={32} />
                            <p>No tasks yet. Create one above.</p>
                        </div>
                    {/each}
                </div>

                <!-- Parallel Execution Viz -->
                {#if engine.allTasks.length > 0}
                    {@const graph = engine.buildTaskGraph()}
                    <div class="task-graph">
                        <h4>🔀 Execution Graph</h4>
                        {#each graph.parallelGroups as group, gi}
                            <div
                                class="parallel-group"
                                in:fly={{
                                    x: -10,
                                    delay: gi * 100,
                                    duration: 200,
                                }}
                            >
                                <span class="group-label">Wave {gi + 1}</span>
                                <div class="group-tasks">
                                    {#each group as taskId}
                                        {@const task = graph.tasks.get(taskId)}
                                        {#if task}
                                            <span
                                                class="graph-task"
                                                style="border-color: {getStatusColor(
                                                    task.status,
                                                )}40">{task.subject}</span
                                            >
                                        {/if}
                                    {/each}
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>

            <!-- ═══ LOOPS TAB ═══ -->
        {:else if activeTab === "loops"}
            <div class="loops-section" in:fade={{ duration: 200 }}>
                <div class="loop-launcher">
                    <h4>🔄 Self-Referential Execution Loops</h4>
                    <p class="loop-desc">
                        Agents work continuously toward a goal, auto-continuing
                        until completion is detected or max iterations reached.
                    </p>

                    <input
                        type="text"
                        bind:value={loopObjective}
                        placeholder="Loop objective: 'Build a REST API with authentication'"
                        class="loop-input"
                    />
                    <div class="loop-controls">
                        <div class="loop-iter">
                            <span>Max iterations:</span>
                            <input
                                type="number"
                                bind:value={loopMaxIter}
                                min={1}
                                max={500}
                                class="iter-input"
                            />
                        </div>
                        <button
                            class="loop-btn ralph"
                            onclick={() => startLoop("ralph")}
                        >
                            <Play size={12} /> Ralph Loop
                        </button>
                        <button
                            class="loop-btn ulw"
                            onclick={() => startLoop("ulw")}
                        >
                            <Zap size={12} /> ULW Loop
                        </button>
                    </div>
                </div>

                {#if engine.loopState}
                    <div class="loop-status" in:fly={{ y: 15, duration: 300 }}>
                        <div class="loop-header">
                            <span class="loop-type"
                                >{engine.loopState.type.toUpperCase()} Loop</span
                            >
                            <span class="loop-progress">
                                {engine.loopState.iteration}/{engine.loopState
                                    .maxIterations}
                            </span>
                            {#if engine.loopState.isComplete}
                                <span class="loop-done">✅ DONE</span>
                            {:else}
                                <span class="loop-running">⏳ Running</span>
                            {/if}
                        </div>
                        <div class="loop-objective">
                            {engine.loopState.objective}
                        </div>
                        <div class="loop-bar">
                            <div
                                class="loop-fill"
                                style="width: {(engine.loopState.iteration /
                                    engine.loopState.maxIterations) *
                                    100}%"
                            ></div>
                        </div>
                        {#if !engine.loopState.isComplete}
                            <button
                                class="cancel-btn"
                                onclick={() => engine.cancelLoop()}
                            >
                                <Square size={12} /> Cancel Loop
                            </button>
                        {/if}
                    </div>
                {/if}

                <!-- Loop Types Explained -->
                <div class="loop-types">
                    <div class="loop-type-card">
                        <h5>🏔️ Ralph Loop</h5>
                        <p>
                            Self-referential development loop. Agent works
                            toward goal, detects <code
                                >&lt;promise&gt;DONE&lt;/promise&gt;</code
                            > for completion. Auto-continues if agent stops without
                            finishing.
                        </p>
                    </div>
                    <div class="loop-type-card">
                        <h5>⚡ ULW Loop (Ultrawork)</h5>
                        <p>
                            Maximum intensity mode. Parallel agents, background
                            tasks, aggressive exploration. Everything runs at
                            full power.
                        </p>
                    </div>
                    <div class="loop-type-card">
                        <h5>🪨 Boulder Loop</h5>
                        <p>
                            Persistent state loop for Sisyphus-style work.
                            Resumes from last checkpoint. Never gives up.
                        </p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .opencode-panel {
        background: linear-gradient(
            135deg,
            rgba(0, 0, 0, 0.95) 0%,
            rgba(20, 10, 35, 0.95) 100%
        );
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 24px;
        overflow: hidden;
        font-family: "Inter", "SF Pro", system-ui, sans-serif;
        box-shadow:
            0 0 60px rgba(168, 85, 247, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        background: rgba(168, 85, 247, 0.03);
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
        background: rgba(168, 85, 247, 0.15);
        color: #a855f7;
        padding: 2px 8px;
        border-radius: 20px;
        letter-spacing: 0.1em;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .header-right {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
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
        padding: 3px 8px;
        border-radius: 20px;
    }
    .stat-pill.hooks {
        color: #a855f7;
        border-color: rgba(168, 85, 247, 0.2);
    }

    /* Route Preview */
    .route-preview {
        padding: 10px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .route-input {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(168, 85, 247, 0.1);
        border-radius: 12px;
        padding: 6px 12px;
    }
    .route-input :global(.route-icon) {
        color: rgba(255, 255, 255, 0.2);
        flex-shrink: 0;
    }
    .route-input input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: white;
        font-size: 11px;
        font-weight: 500;
    }
    .route-input input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }
    .route-combo {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        font-size: 10px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.5);
        flex-wrap: wrap;
    }
    .combo-agent {
        color: #a855f7;
        font-weight: 800;
    }
    .combo-cat {
        font-weight: 800;
    }
    .combo-skill {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 1px 6px;
        border-radius: 6px;
    }
    .combo-no-skill {
        color: rgba(255, 255, 255, 0.2);
        font-style: italic;
    }

    .tab-nav {
        display: flex;
        gap: 2px;
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        overflow-x: auto;
    }
    .tab-btn {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 7px 12px;
        border-radius: 10px;
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: rgba(255, 255, 255, 0.3);
        background: transparent;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }
    .tab-btn:hover {
        color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.03);
    }
    .tab-btn.active {
        color: #a855f7;
        background: rgba(168, 85, 247, 0.08);
        border-color: rgba(168, 85, 247, 0.2);
    }

    .tab-content {
        padding: 16px;
        max-height: 550px;
        overflow-y: auto;
    }
    .tab-content::-webkit-scrollbar {
        width: 4px;
    }
    .tab-content::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    /* Agents */
    .agents-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .agent-card {
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        cursor: pointer;
        transition: all 0.2s;
    }
    .agent-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(168, 85, 247, 0.15);
    }
    .agent-card.selected {
        border-color: rgba(168, 85, 247, 0.3);
        background: rgba(168, 85, 247, 0.05);
    }
    .agent-header {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .agent-icon {
        font-size: 20px;
    }
    .agent-name {
        font-size: 11px;
        font-weight: 800;
        color: white;
        display: block;
    }
    .agent-role {
        font-size: 8px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.25);
        text-transform: uppercase;
        display: block;
    }
    .agent-desc {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.35);
        margin: 6px 0;
        line-height: 1.4;
        font-weight: 500;
    }
    .agent-model {
        font-size: 9px;
        margin-bottom: 6px;
    }
    .model-label {
        color: rgba(255, 255, 255, 0.25);
        font-weight: 700;
    }
    .model-name {
        color: #a855f7;
        font-weight: 800;
        font-family: monospace;
    }
    .agent-caps {
        display: flex;
        flex-wrap: wrap;
        gap: 3px;
    }
    .cap-pill {
        font-size: 7px;
        font-weight: 800;
        text-transform: uppercase;
        background: rgba(168, 85, 247, 0.08);
        color: rgba(168, 85, 247, 0.6);
        padding: 2px 6px;
        border-radius: 6px;
    }
    .agent-restrictions {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 6px;
        font-size: 8px;
        color: #f59e0b;
        font-weight: 700;
    }
    .agent-detail {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .detail-section {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .detail-label {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
    }
    .detail-value {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.6);
    }
    .fallback-chain {
        display: flex;
        align-items: center;
        gap: 4px;
        flex-wrap: wrap;
    }
    .fallback-model {
        font-size: 9px;
        font-family: monospace;
        color: rgba(255, 255, 255, 0.4);
        font-weight: 600;
    }
    .fallback-arrow {
        color: rgba(255, 255, 255, 0.15);
        font-size: 10px;
    }
    .blocked-tools {
        display: flex;
        flex-wrap: wrap;
        gap: 3px;
    }
    .blocked-pill {
        font-size: 8px;
        color: #ef4444;
        background: rgba(239, 68, 68, 0.08);
        padding: 1px 6px;
        border-radius: 6px;
        font-weight: 700;
    }

    /* Categories */
    .categories-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 8px;
    }
    .category-card {
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 3px solid var(--cat-color);
    }
    .cat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .cat-id {
        font-size: 10px;
        font-weight: 900;
        color: var(--cat-color);
        text-transform: uppercase;
    }
    .cat-tier {
        font-size: 7px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.03);
        padding: 1px 6px;
        border-radius: 6px;
    }
    .cat-desc {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.35);
        margin: 6px 0;
        line-height: 1.4;
    }
    .cat-config {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .config-row {
        display: flex;
        justify-content: space-between;
        font-size: 8px;
        color: rgba(255, 255, 255, 0.2);
        font-weight: 600;
    }
    .config-row span:last-child {
        color: rgba(255, 255, 255, 0.4);
        font-family: monospace;
    }
    .unstable-badge {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 6px;
        font-size: 8px;
        font-weight: 800;
        color: #f59e0b;
        background: rgba(245, 158, 11, 0.08);
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Skills */
    .skills-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .skill-combo-guide {
        padding: 14px;
        background: rgba(16, 185, 129, 0.03);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 14px;
    }
    .skill-combo-guide h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.7);
        margin: 0 0 10px;
    }
    .combo-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
    }
    .combo-card {
        padding: 8px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    .combo-title {
        font-size: 10px;
        font-weight: 800;
        color: white;
        display: block;
    }
    .combo-recipe {
        font-size: 8px;
        color: #10b981;
        font-family: monospace;
        font-weight: 600;
        display: block;
        margin-top: 2px;
    }
    .combo-effect {
        font-size: 8px;
        color: rgba(255, 255, 255, 0.3);
        display: block;
        margin-top: 2px;
    }
    .skills-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .skill-card {
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .skill-header {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .skill-icon {
        font-size: 16px;
    }
    .skill-name {
        font-size: 11px;
        font-weight: 800;
        color: white;
    }
    .skill-desc {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.35);
        margin: 4px 0 6px;
        line-height: 1.4;
    }
    .skill-triggers {
        display: flex;
        flex-wrap: wrap;
        gap: 3px;
    }
    .trigger-pill {
        font-size: 7px;
        font-weight: 700;
        background: rgba(168, 85, 247, 0.08);
        color: rgba(168, 85, 247, 0.6);
        padding: 2px 6px;
        border-radius: 6px;
    }
    .mcp-badge {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 6px;
        font-size: 8px;
        color: #22d3ee;
        font-weight: 700;
    }

    /* Hooks */
    .hooks-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .hooks-summary {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .tier-card {
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .tier-header {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .tier-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--tier-color);
        box-shadow: 0 0 8px var(--tier-color);
    }
    .tier-name {
        font-size: 10px;
        font-weight: 900;
        color: var(--tier-color);
        text-transform: uppercase;
    }
    .tier-count {
        margin-left: auto;
        font-size: 9px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.05);
        padding: 1px 6px;
        border-radius: 8px;
    }
    .tier-hooks {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .hook-item {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 9px;
        background: rgba(255, 255, 255, 0.01);
    }
    .hook-item.disabled {
        opacity: 0.3;
    }
    .hook-name {
        font-weight: 700;
        color: rgba(255, 255, 255, 0.5);
        min-width: 120px;
    }
    .hook-events {
        display: flex;
        gap: 2px;
        flex: 1;
    }
    .event-pill {
        font-size: 7px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.03);
        padding: 1px 4px;
        border-radius: 4px;
    }
    .hook-priority {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
    }
    .hook-pipeline-viz {
        padding: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
    }
    .hook-pipeline-viz h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        margin: 0 0 12px;
    }
    .pipeline-flow {
        display: flex;
        align-items: center;
        gap: 4px;
        flex-wrap: wrap;
    }
    .pipeline-node {
        padding: 6px 10px;
        border-radius: 8px;
        background: rgba(168, 85, 247, 0.08);
        border: 1px solid rgba(168, 85, 247, 0.15);
        text-align: center;
    }
    .node-event {
        font-size: 8px;
        font-weight: 900;
        color: #a855f7;
        display: block;
        text-transform: uppercase;
    }
    .node-count {
        font-size: 7px;
        color: rgba(255, 255, 255, 0.3);
        font-weight: 600;
        display: block;
    }
    .pipeline-arrow {
        color: rgba(255, 255, 255, 0.15);
        font-size: 12px;
    }

    /* Tasks */
    .tasks-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .task-creator {
        padding: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
    }
    .task-creator h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 0 10px;
    }
    .task-form {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .task-input {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 6px 10px;
        color: white;
        font-size: 10px;
        outline: none;
    }
    .task-input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }
    .task-form-row {
        display: flex;
        gap: 6px;
    }
    .task-select {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 4px 8px;
        color: white;
        font-size: 9px;
    }
    .task-submit {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 6px 14px;
        border-radius: 8px;
        border: none;
        background: #a855f7;
        color: white;
        font-size: 10px;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s;
    }
    .task-submit:hover {
        transform: scale(1.05);
    }
    .task-submit:disabled {
        opacity: 0.5;
    }
    .task-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .task-card {
        padding: 10px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .task-header {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
    }
    .task-status {
        font-size: 7px;
        font-weight: 900;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid;
        text-transform: uppercase;
    }
    .task-id {
        font-size: 8px;
        font-family: monospace;
        color: rgba(255, 255, 255, 0.2);
    }
    .task-cat {
        font-size: 8px;
        font-weight: 800;
        margin-left: auto;
    }
    .task-subject {
        font-size: 10px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.6);
    }
    .task-deps {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 4px;
        flex-wrap: wrap;
    }
    .deps-label {
        font-size: 8px;
        color: rgba(255, 255, 255, 0.25);
        font-weight: 700;
    }
    .dep-pill {
        font-size: 7px;
        font-family: monospace;
        background: rgba(239, 68, 68, 0.08);
        color: rgba(239, 68, 68, 0.6);
        padding: 1px 6px;
        border-radius: 4px;
    }
    .empty-state {
        text-align: center;
        padding: 30px;
        color: rgba(255, 255, 255, 0.1);
    }
    .empty-state p {
        font-size: 10px;
        margin-top: 8px;
        font-weight: 600;
    }
    .task-graph {
        padding: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
    }
    .task-graph h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.5);
        margin: 0 0 12px;
    }
    .parallel-group {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .group-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        min-width: 50px;
        text-transform: uppercase;
    }
    .group-tasks {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
    }
    .graph-task {
        font-size: 8px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.5);
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid;
    }

    /* Loops */
    .loops-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .loop-launcher {
        padding: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
    }
    .loop-launcher h4 {
        font-size: 11px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 0 4px;
    }
    .loop-desc {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.3);
        margin: 0 0 10px;
        line-height: 1.4;
    }
    .loop-input {
        width: 100%;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 8px 12px;
        color: white;
        font-size: 11px;
        outline: none;
        box-sizing: border-box;
    }
    .loop-input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }
    .loop-controls {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }
    .loop-iter {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 9px;
        color: rgba(255, 255, 255, 0.3);
    }
    .iter-input {
        width: 60px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 4px 6px;
        color: white;
        font-size: 10px;
        text-align: center;
    }
    .loop-btn {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 6px 14px;
        border-radius: 8px;
        border: none;
        font-size: 10px;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s;
    }
    .loop-btn.ralph {
        background: #a855f7;
        color: white;
    }
    .loop-btn.ulw {
        background: #f59e0b;
        color: black;
    }
    .loop-btn:hover {
        transform: scale(1.05);
    }
    .loop-status {
        padding: 14px;
        background: rgba(168, 85, 247, 0.05);
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 14px;
    }
    .loop-header {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .loop-type {
        font-size: 10px;
        font-weight: 900;
        color: #a855f7;
    }
    .loop-progress {
        font-size: 10px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.4);
        font-family: monospace;
    }
    .loop-done {
        font-size: 9px;
        font-weight: 800;
        color: #10b981;
        margin-left: auto;
    }
    .loop-running {
        font-size: 9px;
        font-weight: 800;
        color: #f59e0b;
        margin-left: auto;
    }
    .loop-objective {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.5);
        margin: 6px 0 8px;
        font-weight: 500;
    }
    .loop-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        overflow: hidden;
    }
    .loop-fill {
        height: 100%;
        background: linear-gradient(90deg, #a855f7, #ec4899);
        border-radius: 4px;
        transition: width 0.5s;
    }
    .cancel-btn {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 8px;
        padding: 4px 12px;
        border-radius: 6px;
        border: 1px solid rgba(239, 68, 68, 0.3);
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        font-size: 9px;
        font-weight: 800;
        cursor: pointer;
    }
    .loop-types {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }
    .loop-type-card {
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .loop-type-card h5 {
        font-size: 10px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 0 4px;
    }
    .loop-type-card p {
        font-size: 8px;
        color: rgba(255, 255, 255, 0.3);
        line-height: 1.4;
        margin: 0;
    }
    .loop-type-card code {
        font-size: 8px;
        background: rgba(168, 85, 247, 0.1);
        color: #a855f7;
        padding: 1px 4px;
        border-radius: 3px;
    }
</style>
