<script lang="ts">
    import { onMount } from "svelte";
    import { fade, slide } from "svelte/transition";
    import {
        Search,
        BookOpen,
        FileSearch,
        Layers,
        Database,
        Globe,
        Zap,
        Coins,
        Loader2,
        Terminal,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type Mission = {
        id: string;
        title: string;
        status: "LIBRARIAN" | "SCRIBE" | "FINALIZING" | "COMPLETE";
        progress: number;
        resolution: number;
        staked: number;
        tags: string[];
        lastFinding: string;
    };

    let missions = $state<Mission[]>([
        {
            id: "MSR-001",
            title: "Post-Quantum Privacy Vectors",
            status: "LIBRARIAN",
            progress: 45,
            resolution: 0.8,
            staked: 12500,
            tags: ["Security", "Cryptography"],
            lastFinding: "Extracting lattice-based key exchange benchmarks...",
        },
        {
            id: "MSR-042",
            title: "Hyper-Regional Currency Shards",
            status: "SCRIBE",
            progress: 88,
            resolution: 0.95,
            staked: 25000,
            tags: ["Economics", "Nagano"],
            lastFinding: "Synthesizing Law_Wafer.json for regional parity...",
        },
    ]);

    let activeMissionId = $state("MSR-001");
    let activeMission = $derived(
        missions.find((m) => m.id === activeMissionId),
    );

    let researchLogs = $state([
        { time: "20:30:12", msg: "Initializing MISSION_ID: MSR-001" },
        {
            time: "20:31:45",
            msg: "Librarian Phase: Web3-Onboard documentation indexed.",
        },
        { time: "20:33:02", msg: "Source archived: kernel_panic_0xAA.log" },
        {
            time: "20:35:10",
            msg: "Checklist 0.85 pass: All ZK citations verified.",
        },
    ]);

    function stakeToMission(amount: number) {
        if (activeMission) {
            activeMission.staked += amount;
            manifold.recordEvent(
                "RESEARCH_STAKE",
                `Staked ${amount} AGE to ${activeMission.title}`,
            );
        }
    }

    onMount(() => {
        const interval = setInterval(() => {
            if (activeMission && activeMission.progress < 100) {
                activeMission.progress += Math.random() * 2;
                if (activeMission.progress > 100) activeMission.progress = 100;
            }
        }, 5000);
        return () => clearInterval(interval);
    });
</script>

<div class="research-shell">
    <!-- Institutional Header -->
    <header class="research-header">
        <div class="header-brand">
            <div class="logo-box">
                <FileSearch size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Research</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label"
                        >Protocol_Phase: {activeMission?.status}</span
                    >
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">MISSION_RESOLUTION</span>
                <span class="tel-value text-indigo-400"
                    >{(activeMission?.resolution || 0) * 100}%</span
                >
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block">
                <span class="tel-label">KNOWLEDGE_DENSITY</span>
                <span class="tel-value">1.2 TB/min</span>
            </div>
        </div>
    </header>

    <div class="research-body">
        <!-- Explorer Sidebar -->
        <aside class="mission-sidebar scrollbar-hide">
            <h3 class="sidebar-title">Autonomous_Missions</h3>
            <div class="mission-list">
                {#each missions as mission}
                    <button
                        onclick={() => (activeMissionId = mission.id)}
                        class="mission-btn"
                        class:active={activeMissionId === mission.id}
                    >
                        <div class="mission-btn-meta">
                            <span class="m-id">{mission.id}</span>
                            <span class="m-status">{mission.status}</span>
                        </div>
                        <h4 class="m-title">{mission.title}</h4>
                        <div class="m-progress-track">
                            <div
                                class="m-progress-fill"
                                style="width: {mission.progress}%"
                            ></div>
                        </div>
                    </button>
                {/each}
            </div>

            <button class="new-vector-btn">
                <Search size={14} />
                <span>Source_New_Vectors</span>
            </button>
        </aside>

        <!-- Command Interface -->
        <main class="mission-control scrollbar-hide">
            {#if activeMission}
                <div class="control-viewport" in:fade={{ duration: 400 }}>
                    <!-- Prime Identity Card -->
                    <section class="identity-card">
                        <div class="identity-aura">
                            <Layers size={240} strokeWidth={1} />
                        </div>
                        <div class="identity-content">
                            <div class="tag-row">
                                {#each activeMission.tags as tag}
                                    <span class="mission-tag">{tag}</span>
                                {/each}
                            </div>
                            <h2 class="hero-title">{activeMission.title}</h2>
                            <div class="stats-row">
                                <div class="stat-item">
                                    <span class="s-label">Staked_Equity</span>
                                    <span class="s-value"
                                        >{activeMission.staked.toLocaleString()}
                                        <small>AGE</small></span
                                    >
                                </div>
                                <div class="stat-item">
                                    <span class="s-label">Protocol_Yield</span>
                                    <span class="s-value text-emerald-400"
                                        >8.42%</span
                                    >
                                </div>
                                <div class="stat-item">
                                    <span class="s-label">Active_Agents</span>
                                    <span class="s-value text-indigo-400"
                                        >42_UNITS</span
                                    >
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Tactical Outputs -->
                    <div class="tactical-grid">
                        <section class="log-vessel">
                            <header class="vessel-header">
                                <Terminal size={12} class="text-white/40" />
                                <h3>Causal_Inference_Stream</h3>
                            </header>
                            <div class="vessel-content scrollbar-hide">
                                {#each researchLogs as log}
                                    <div class="log-entry" transition:slide>
                                        <span class="log-time">{log.time}</span>
                                        <p class="log-msg">{log.msg}</p>
                                    </div>
                                {/each}
                                <div class="log-active animate-pulse">
                                    <Loader2
                                        size={12}
                                        class="animate-spin text-indigo-500"
                                    />
                                    <span class="log-finding"
                                        >{activeMission.lastFinding}</span
                                    >
                                </div>
                            </div>
                        </section>

                        <section class="action-vessel">
                            <header class="vessel-header">
                                <Database size={12} class="text-white/40" />
                                <h3>Knowledge_Repository</h3>
                            </header>
                            <div class="kb-grid">
                                <div class="kb-tile">
                                    <BookOpen
                                        size={16}
                                        class="text-indigo-400"
                                    />
                                    <span>Economics/KB</span>
                                </div>
                                <div class="kb-tile">
                                    <Database size={16} class="text-cyan-400" />
                                    <span>Technical/KB</span>
                                </div>
                                <div class="kb-tile">
                                    <Globe size={16} class="text-emerald-400" />
                                    <span>Social/KB</span>
                                </div>
                                <div class="kb-tile">
                                    <Zap size={16} class="text-amber-400" />
                                    <span>Law_Wafers/KB</span>
                                </div>
                            </div>
                            <button
                                onclick={() => stakeToMission(1000)}
                                class="stake-btn"
                            >
                                <Coins size={14} />
                                <span>Inject_1,000_AGE_Equity</span>
                            </button>
                        </section>
                    </div>
                </div>
            {/if}
        </main>
    </div>
</div>

<style>
    .research-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
    }

    .research-header {
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .logo-box {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .phase-label {
        font-size: 8px;
        font-weight: 800;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-style: italic;
    }

    .phase-pulsar {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6366f1;
        box-shadow: 0 0 10px #6366f1;
        animation: pulse 1s infinite;
    }

    .header-telemetry {
        display: flex;
        gap: 2rem;
    }

    .tel-block {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
        margin-bottom: 2px;
    }

    .tel-value {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .tel-divider {
        width: 1px;
        height: 24px;
        background: rgba(255, 255, 255, 0.05);
    }

    .research-body {
        flex: 1;
        display: flex;
        overflow: hidden;
    }

    .mission-sidebar {
        width: 320px;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(0, 0, 0, 0.1);
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .sidebar-title {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .mission-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .mission-btn {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.25rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .mission-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(4px);
    }

    .mission-btn.active {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.2);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }

    .mission-btn-meta {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }

    .m-id {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
    }

    .m-status {
        font-size: 7px;
        font-weight: 950;
        color: #818cf8;
        background: rgba(99, 102, 241, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }

    .m-title {
        font-size: 11px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .m-progress-track {
        height: 3px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }

    .m-progress-fill {
        height: 100%;
        background: #6366f1;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }

    .new-vector-btn {
        margin-top: auto;
        padding: 1rem;
        background: none;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        color: rgba(255, 255, 255, 0.2);
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s;
    }

    .new-vector-btn:hover {
        border-color: rgba(255, 255, 255, 0.3);
        color: white;
        background: rgba(255, 255, 255, 0.02);
    }

    .mission-control {
        flex: 1;
        padding: 2.5rem;
        overflow-y: auto;
    }

    .identity-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        padding: 3rem;
        position: relative;
        overflow: hidden;
        margin-bottom: 2.5rem;
    }

    .identity-aura {
        position: absolute;
        top: -50px;
        right: -50px;
        opacity: 0.03;
        color: #6366f1;
        transform: rotate(15deg);
    }

    .mission-tag {
        font-size: 8px;
        font-weight: 950;
        color: #818cf8;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 4px 12px;
        border-radius: 100px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .tag-row {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 36px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: -0.04em;
        font-style: italic;
        margin-bottom: 2.5rem;
        line-height: 1;
    }

    .stats-row {
        display: flex;
        gap: 4rem;
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .s-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .s-value {
        font-size: 18px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .s-value small {
        font-size: 10px;
        opacity: 0.4;
    }

    .tactical-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 2.5rem;
    }

    .vessel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .vessel-header h3 {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .log-vessel {
        display: flex;
        flex-direction: column;
    }

    .vessel-content {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        height: 280px;
        overflow-y: auto;
    }

    .log-entry {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }

    .log-time {
        font-family: "JetBrains Mono", monospace;
        font-size: 8px;
        color: rgba(255, 255, 255, 0.1);
    }

    .log-msg {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.5;
    }

    .log-active {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
    }

    .log-finding {
        font-size: 10px;
        color: #818cf8;
        font-style: italic;
    }

    .kb-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .kb-tile {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }

    .kb-tile:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .kb-tile span {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
    }

    .stake-btn {
        width: 100%;
        padding: 1.25rem;
        background: white;
        border-radius: 18px;
        color: black;
        font-size: 11px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .stake-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(255, 255, 255, 0.2);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
