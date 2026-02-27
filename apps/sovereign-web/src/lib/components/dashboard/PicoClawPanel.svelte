<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🕹️ SOVEREIGN PICOCLAW: EDGE ORCHESTRATION PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // Visualizing Ultra-Lightweight AI Agents and Edge Node Connectivity.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, slide } from "svelte/transition";
    import {
        Cpu,
        Zap,
        HardDrive,
        Network,
        MessageSquare,
        Power,
        Plus,
        Activity,
        Terminal,
        Microchip,
        Radio,
    } from "lucide-svelte";
    import {
        sovereignPicoClaw,
        type EdgeNode,
    } from "$lib/services/picoclaw-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<"nodes" | "bridges" | "memory">("nodes");
    let newNodeName = $state("");
    let newNodeArch = $state<EdgeNode["architecture"]>("riscv");
    let isAddingNode = $state(false);

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    function createNode() {
        if (newNodeName) {
            sovereignPicoClaw.spawnNode(newNodeName, newNodeArch);
            newNodeName = "";
            isAddingNode = false;
        }
    }

    function getArchIcon(arch: string) {
        if (arch === "riscv") return Microchip;
        return Cpu;
    }
</script>

<div class="picoclaw-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <Radio size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Sovereign PicoClaw</h3>
                <p>Ultra-Lightweight Edge Intelligence</p>
            </div>
        </div>
        <div class="metrics-bar">
            <div class="metric">
                <span class="label">MEMORY</span>
                <span class="value">{sovereignPicoClaw.stats.totalMemory}</span>
            </div>
            <div class="metric">
                <span class="label">BOOT</span>
                <span class="value success"
                    >{sovereignPicoClaw.stats.avgBoot}</span
                >
            </div>
            <div class="metric">
                <span class="label">NODES</span>
                <span class="value glow"
                    >{sovereignPicoClaw.stats.onlineCount}/{sovereignPicoClaw
                        .stats.nodeCount}</span
                >
            </div>
        </div>
    </header>

    <!-- 📑 TABS -->
    <div class="tabs">
        <button
            class:active={activeTab === "nodes"}
            onclick={() => (activeTab = "nodes")}
        >
            <Network size={14} /> <span>Edge Nodes</span>
        </button>
        <button
            class:active={activeTab === "bridges"}
            onclick={() => (activeTab = "bridges")}
        >
            <MessageSquare size={14} /> <span>Bridges</span>
        </button>
        <button
            class:active={activeTab === "memory"}
            onclick={() => (activeTab = "memory")}
        >
            <HardDrive size={14} /> <span>Edge Memory</span>
        </button>
    </div>

    <!-- 🎚️ CONTENT AREA -->
    <div class="content-scroll">
        {#if activeTab === "nodes"}
            <div class="nodes-view" in:fade>
                <div class="grid">
                    {#each sovereignPicoClaw.allNodes as node, i (node.id)}
                        {@const Icon = getArchIcon(node.architecture)}
                        <div
                            class="node-card"
                            class:online={node.status === "online"}
                            class:hibernated={node.status === "hibernating"}
                            in:fly={{ y: 20, delay: i * 50 }}
                        >
                            <div class="node-header">
                                <div class="node-title">
                                    <Icon size={16} class="arch-icon" />
                                    <h4>{node.name}</h4>
                                </div>
                                <div class="status-indicator">
                                    <span class="dot"></span>
                                    <span class="status-text"
                                        >{node.status}</span
                                    >
                                </div>
                            </div>

                            <div class="node-stats">
                                <div class="stat">
                                    <span class="s-label">ARCH</span>
                                    <span class="s-value"
                                        >{node.architecture}</span
                                    >
                                </div>
                                <div class="stat">
                                    <span class="s-label">MEM</span>
                                    <span class="s-value"
                                        >{node.memoryUsageMb.toFixed(1)} MB</span
                                    >
                                </div>
                                <div class="stat">
                                    <span class="s-label">BOOT</span>
                                    <span class="s-value"
                                        >{node.bootTimeMs}ms</span
                                    >
                                </div>
                            </div>

                            <div class="node-footer">
                                <div class="bridges">
                                    {#each node.activeBridges as bridge}
                                        <span class="bridge-tag">{bridge}</span>
                                    {/each}
                                </div>
                                <button
                                    class="action-btn"
                                    onclick={() =>
                                        sovereignPicoClaw.toggleHibernate(
                                            node.id,
                                        )}
                                >
                                    <Power size={13} />
                                    <span
                                        >{node.status === "hibernating"
                                            ? "Wake"
                                            : "Sleep"}</span
                                    >
                                </button>
                            </div>
                        </div>
                    {/each}

                    <button
                        class="add-node-card"
                        onclick={() => (isAddingNode = !isAddingNode)}
                    >
                        <Plus size={24} />
                        <span>Deploy Node</span>
                    </button>
                </div>

                {#if isAddingNode}
                    <div class="add-node-overlay" transition:slide>
                        <div class="form">
                            <input
                                type="text"
                                bind:value={newNodeName}
                                placeholder="Node Identity..."
                                spellcheck="false"
                            />
                            <select bind:value={newNodeArch}>
                                <option value="riscv">RISC-V (High-Eff)</option>
                                <option value="arm64"
                                    >ARM64 (Mobile Edge)</option
                                >
                                <option value="x86_64">x86_64 (Standard)</option
                                >
                            </select>
                            <button onclick={createNode}>SPAWN BINARY</button>
                        </div>
                    </div>
                {/if}
            </div>
        {:else if activeTab === "bridges"}
            <div class="bridges-view" in:fade>
                <div class="bridge-info">
                    <Zap size={24} class="accent" />
                    <div class="txt">
                        <h5>Omnichannel Bridges Active</h5>
                        <p>
                            PicoClaw instances are currently connected to 4
                            external gateways.
                        </p>
                    </div>
                </div>
                <div class="bridge-list">
                    <div class="bridge-item">
                        <div class="b-brand">Telegram</div>
                        <div class="b-status active">Connected • 12ms</div>
                        <Activity size={12} class="activity-pulse" />
                    </div>
                    <div class="bridge-item">
                        <div class="b-brand">Discord</div>
                        <div class="b-status active">Connected • 18ms</div>
                        <Activity size={12} class="activity-pulse" />
                    </div>
                    <div class="bridge-item dimmed">
                        <div class="b-brand">Matrix</div>
                        <div class="b-status offline">Disconnected</div>
                    </div>
                </div>
            </div>
        {:else if activeTab === "memory"}
            <div class="memory-view" in:fade>
                <div class="memory-header">
                    <Terminal size={14} />
                    <span>Persistent Markdown Buffer</span>
                </div>
                {#if sovereignPicoClaw.allMemories.length === 0}
                    <div class="empty-memory">
                        <HardDrive size={32} class="muted" />
                        <p>
                            No edge memories committed. Commit a state to
                            persist to Markdown binary.
                        </p>
                    </div>
                {:else}
                    <div class="memory-list">
                        {#each sovereignPicoClaw.allMemories as memory}
                            <div class="memory-card">
                                <div class="m-head">
                                    <span class="m-key">@{memory.key}</span>
                                    <span class="m-time"
                                        >{new Date(
                                            memory.timestamp,
                                        ).toLocaleTimeString()}</span
                                    >
                                </div>
                                <div class="m-body">{memory.content}</div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .picoclaw-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(10, 11, 15, 0.7);
        backdrop-filter: blur(20px);
        color: #e0e6ed;
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
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
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
        color: #3b82f6;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
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
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* NODES VIEW */
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1rem;
    }

    .node-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        transition: all 0.25s;
    }

    .node-card.online {
        border-left: 2px solid #10b981;
        background: rgba(16, 185, 129, 0.02);
    }

    .node-card.online .dot {
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    .node-card.hibernated {
        opacity: 0.6;
        filter: grayscale(0.5);
    }

    .node-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .node-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    :global(.arch-icon) {
        color: #64748b;
    }

    .node-title h4 {
        margin: 0;
        font-size: 0.8rem;
        font-weight: 700;
        color: #f8fafc;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.6rem;
        text-transform: uppercase;
        font-weight: 800;
        color: #64748b;
    }

    .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #475569;
    }

    .node-stats {
        display: flex;
        justify-content: space-between;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.5rem;
        border-radius: 6px;
    }

    .stat {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .s-label {
        font-size: 0.55rem;
        color: #475569;
        font-weight: 700;
    }

    .s-value {
        font-size: 0.65rem;
        font-weight: 700;
        color: #cbd5e1;
        font-family: "JetBrains Mono", monospace;
    }

    .node-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: auto;
    }

    .bridge-tag {
        font-size: 0.6rem;
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }

    .action-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #94a3b8;
        padding: 0.35rem 0.6rem;
        border-radius: 4px;
        font-size: 0.65rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #f8fafc;
    }

    .add-node-card {
        background: rgba(255, 255, 255, 0.01);
        border: 2px dashed rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s;
        min-height: 140px;
    }

    .add-node-card:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(16, 185, 129, 0.3);
        color: #10b981;
    }

    .add-node-overlay {
        margin-top: 1rem;
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 10px;
        padding: 1rem;
    }

    .form {
        display: flex;
        gap: 0.75rem;
    }

    .form input {
        flex: 1;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        color: white;
        font-size: 0.8rem;
        outline: none;
    }

    .form select {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #94a3b8;
        padding: 0.5rem;
        border-radius: 6px;
        font-size: 0.8rem;
    }

    .form button {
        background: #10b981;
        color: white;
        border: none;
        padding: 0 1.25rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
        cursor: pointer;
    }

    /* BRIDGES VIEW */
    .bridges-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .bridge-info {
        display: flex;
        gap: 1rem;
        align-items: center;
        background: rgba(59, 130, 246, 0.05);
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }

    .bridge-info h5 {
        margin: 0;
        font-size: 0.9rem;
    }
    .bridge-info p {
        margin: 0;
        font-size: 0.75rem;
        color: #94a3b8;
    }
    :global(.accent) {
        color: #3b82f6;
    }

    .bridge-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .bridge-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .b-brand {
        font-weight: 700;
        font-size: 0.85rem;
    }
    .b-status {
        font-size: 0.7rem;
    }
    .b-status.active {
        color: #10b981;
    }
    .b-status.offline {
        color: #ef4444;
    }

    :global(.activity-pulse) {
        color: #10b981;
        animation: pulse 2s infinite;
    }

    /* MEMORY VIEW */
    .memory-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 1rem;
    }

    .memory-card {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }

    .m-head {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-family: "JetBrains Mono", monospace;
    }

    .m-key {
        font-size: 0.7rem;
        color: #34d399;
        font-weight: 700;
    }
    .m-time {
        font-size: 0.6rem;
        color: #475569;
    }

    .m-body {
        font-size: 0.75rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    @keyframes pulse {
        0% {
            opacity: 0.4;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.4;
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
