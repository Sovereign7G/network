<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly, slide } from "svelte/transition";
    import {
        Workflow,
        Zap,
        ArrowRight,
        Plus,
        Trash2,
        Play,
        Shield,
        Cpu,
        Database,
        CircleDot,
        Activity,
        Terminal,
    } from "lucide-svelte";

    interface LogicLink {
        id: string;
        trigger: string;
        action: string;
        status: "active" | "paused";
    }

    let links: LogicLink[] = $state([
        {
            id: "1",
            trigger: "Hilbert Index < 0.95",
            action: "Harden Protocol",
            status: "active",
        },
        {
            id: "2",
            trigger: "Compute Demand > 80%",
            action: "Scale Node Nagano",
            status: "active",
        },
    ]);

    let isAdding = $state(false);
    let newTrigger = $state("");
    let newAction = $state("");

    function addLink() {
        if (!newTrigger || !newAction) return;
        links = [
            ...links,
            {
                id: Math.random().toString(36).substring(7),
                trigger: newTrigger,
                action: newAction,
                status: "active",
            },
        ];
        newTrigger = "";
        newAction = "";
        isAdding = false;
        manifold.recordEvent(
            "LOGIC_LINK_CREATED",
            `New autonomous link: ${newAction} triggered by ${newTrigger}`,
        );
    }

    function removeLink(id: string) {
        links = links.filter((l) => l.id !== id);
    }

    function toggleStatus(id: string) {
        links = links.map((l) =>
            l.id === id
                ? { ...l, status: l.status === "active" ? "paused" : "active" }
                : l,
        );
    }
</script>

<div class="logic-manifold" in:fade>
    <div class="manifold-glass"></div>
    <div class="manifold-aura"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="flex items-center gap-4">
            <div class="icon-vessel">
                <Workflow size={20} class="text-emerald-400" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Logic</h2>
                <div class="flex items-center gap-2">
                    <span class="subtitle">Autonomous_Orchestrator_v1.0</span>
                    <div class="status-pulse"></div>
                </div>
            </div>
        </div>
        <button onclick={() => (isAdding = !isAdding)} class="add-btn">
            <Plus size={14} />
            <span>Instantiate_Link</span>
        </button>
    </header>

    <!-- Active Causal Links -->
    <div class="manifold-body scrollbar-hide">
        {#each links as link (link.id)}
            <div class="causal-vessel group" in:fly={{ y: 20 }}>
                <div class="vessel-aura"></div>
                <div class="vessel-content">
                    <div class="flex items-center justify-between mb-5">
                        <div class="flex items-center gap-3">
                            <div
                                class="status-indicator {link.status ===
                                'active'
                                    ? 'active'
                                    : ''}"
                            ></div>
                            <span
                                class="status-label {link.status === 'active'
                                    ? 'active'
                                    : ''}"
                            >
                                {link.status === "active"
                                    ? "Operational"
                                    : "Quiescent"}
                            </span>
                        </div>
                        <div class="vessel-actions">
                            <button
                                onclick={() => toggleStatus(link.id)}
                                class="act-btn"
                            >
                                <Play
                                    size={14}
                                    fill={link.status === "paused"
                                        ? "currentColor"
                                        : "none"}
                                />
                            </button>
                            <button
                                onclick={() => removeLink(link.id)}
                                class="act-btn rose"
                            >
                                <Trash2 size={14} />
                            </button>
                        </div>
                    </div>

                    <div class="causal-chain">
                        <div class="link-segment">
                            <span class="seg-label">TRIGGER_CONDITION</span>
                            <div class="seg-box">
                                <CircleDot size={12} class="text-white/20" />
                                <span class="seg-value font-mono"
                                    >{link.trigger}</span
                                >
                            </div>
                        </div>
                        <div class="chain-arrow">
                            <ArrowRight size={16} />
                        </div>
                        <div class="link-segment">
                            <span class="seg-label">PROTOCOL_EFFECT</span>
                            <div class="seg-box emerald">
                                <Zap size={12} class="text-emerald-400" />
                                <span class="seg-value font-black"
                                    >{link.action}</span
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/each}

        {#if isAdding}
            <div class="instantiation-matrix" transition:slide>
                <div class="matrix-header">
                    <Terminal size={14} class="text-emerald-400" />
                    <span>New_Autonomous_Link_Config</span>
                </div>
                <div class="matrix-inputs">
                    <div class="input-block">
                        <label for="trigger-cond">Condition_Vector</label>
                        <input
                            id="trigger-cond"
                            bind:value={newTrigger}
                            placeholder="e.g. RESONANCE < 0.8"
                        />
                    </div>
                    <div class="input-block">
                        <label for="exec-payload">Execution_Payload</label>
                        <input
                            id="exec-payload"
                            bind:value={newAction}
                            placeholder="e.g. INITIATE_LOCKDOWN"
                        />
                    </div>
                </div>
                <button onclick={addLink} class="deploy-btn">
                    <span>Deploy_Causal_Instruction</span>
                </button>
            </div>
        {/if}
    </div>

    <!-- System Controls -->
    <footer class="manifold-footer">
        <div class="control-grid">
            <button class="ctrl-card group">
                <Shield size={16} class="text-cyan-400" />
                <span>Safe_Mode</span>
            </button>
            <button class="ctrl-card group">
                <Cpu size={16} class="text-purple-400" />
                <span>Auto_Scale</span>
            </button>
            <button class="ctrl-card group">
                <Database size={16} class="text-amber-400" />
                <span>Sync_Vault</span>
            </button>
        </div>

        <div class="telemetry-bar">
            <div class="flex items-center gap-2">
                <Activity size={12} class="text-emerald-400" />
                <span
                    class="text-[8px] font-black uppercase tracking-[0.2em] opacity-40"
                    >Orchestration_Active // Buffer: STABLE</span
                >
            </div>
            <div class="flex -space-x-1">
                {#each Array(3) as _}
                    <div
                        class="w-4 h-4 rounded-full border border-zinc-950 bg-zinc-800"
                    ></div>
                {/each}
            </div>
        </div>
    </footer>
</div>

<style>
    .logic-manifold {
        height: 100%;
        background: rgba(10, 5, 20, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        position: relative;
        overflow: hidden;
    }

    .manifold-glass {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.02),
            transparent
        );
        pointer-events: none;
    }

    .manifold-aura {
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: radial-gradient(
            circle at center,
            rgba(16, 185, 129, 0.05),
            transparent 70%
        );
        pointer-events: none;
    }

    .manifold-header {
        padding: 2rem 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .icon-vessel {
        width: 44px;
        height: 44px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .title {
        font-size: 14px;
        font-weight: 950;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
    }
    .subtitle {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .status-pulse {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }

    .add-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1.25rem;
        border-radius: 100px;
        color: white;
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    .add-btn:hover {
        background: white;
        color: black;
        border-color: white;
        transform: translateY(-2px);
    }

    .manifold-body {
        flex: 1;
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        overflow-y: auto;
    }

    .causal-vessel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        padding: 1.75rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .causal-vessel:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
    }

    .vessel-aura {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 0% 0%,
            rgba(16, 185, 129, 0.05),
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.4s;
    }
    .causal-vessel:hover .vessel-aura {
        opacity: 1;
    }

    .vessel-content {
        position: relative;
        z-index: 10;
    }

    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
    }
    .status-indicator.active {
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
    }
    .status-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .status-label.active {
        color: #10b981;
    }

    .vessel-actions {
        display: flex;
        gap: 0.5rem;
    }
    .act-btn {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.2s;
    }
    .act-btn:hover {
        color: white;
        transform: scale(1.1);
    }
    .act-btn.rose:hover {
        color: #f43f5e;
    }

    .causal-chain {
        display: flex;
        align-items: flex-end;
        gap: 1.5rem;
    }
    .link-segment {
        flex: 1;
    }
    .seg-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: block;
        margin-bottom: 0.75rem;
    }
    .seg-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 0.85rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .seg-box.emerald {
        background: rgba(16, 185, 129, 0.05);
        border-color: rgba(16, 185, 129, 0.2);
    }
    .seg-value {
        font-size: 11px;
        color: white;
    }

    .chain-arrow {
        margin-bottom: 1.25rem;
        color: rgba(255, 255, 255, 0.1);
    }

    .instantiation-matrix {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 32px;
        padding: 2rem;
    }
    .matrix-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 10px;
        font-weight: 950;
        color: #10b981;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    .matrix-inputs {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .input-block {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .input-block label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }
    .input-block input {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.85rem 1.25rem;
        color: white;
        font-size: 11px;
        font-weight: 500;
        outline: none;
    }

    .deploy-btn {
        width: 100%;
        height: 52px;
        background: #10b981;
        border: none;
        border-radius: 16px;
        color: black;
        font-size: 10px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.3s;
    }
    .deploy-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }

    .manifold-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .control-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .ctrl-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
        color: rgba(255, 255, 255, 0.3);
        cursor: pointer;
        transition: all 0.3s;
    }
    .ctrl-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: white/20;
        color: white;
        transform: translateY(-2px);
    }
    .ctrl-card span {
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
    }

    .telemetry-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
