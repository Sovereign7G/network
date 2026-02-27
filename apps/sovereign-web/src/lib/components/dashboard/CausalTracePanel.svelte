<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Activity,
        Clock,
        Terminal,
        Zap,
        Shield,
        Cpu,
        Search,
        Layers,
    } from "lucide-svelte";

    let logs = $derived(manifold.causalLog);

    function formatTime(ts: number) {
        return new Date(ts).toLocaleTimeString([], {
            hour12: false,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        });
    }

    function getTypeColor(type: string) {
        if (type.includes("START") || type.includes("INIT"))
            return "text-cyan-400";
        if (type.includes("COMPLETE") || type.includes("PASS"))
            return "text-emerald-400";
        if (type.includes("WARN") || type.includes("SHIFT"))
            return "text-amber-400";
        if (type.includes("ERR") || type.includes("FAIL"))
            return "text-rose-400";
        return "text-white/40";
    }
</script>

<div class="trace-manifold" in:fade>
    <div class="manifold-glass"></div>
    <div class="manifold-aura"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="header-brand">
            <div class="icon-vessel">
                <Search size={18} class="text-cyan-400" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Causal_Trace</h2>
                <div class="flex items-center gap-2">
                    <span class="subtitle">Event_Propagation_Stream</span>
                    <div class="status-dot"></div>
                </div>
            </div>
        </div>
        <div class="header-telemetry">
            <span class="tel-label">BUFFER_SATURATION</span>
            <div class="flex items-center gap-2">
                <span class="tel-value"
                    >{((logs.length / 50) * 100).toFixed(0)}%</span
                >
                <Layers size={10} class="text-white/20" />
            </div>
        </div>
    </header>

    <!-- Event Stream -->
    <div class="manifold-body scrollbar-hide">
        {#if logs.length === 0}
            <div class="empty-state">
                <div class="glimmer-circle"></div>
                <p>Awaiting Systemic Events...</p>
            </div>
        {:else}
            <div class="event-stream">
                {#each logs as log (log.id)}
                    <div
                        class="event-vessel group"
                        in:slide={{ duration: 400 }}
                    >
                        <div class="vessel-line"></div>
                        <div class="vessel-content">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-2">
                                    <div
                                        class="type-badge {getTypeColor(
                                            log.type,
                                        )}"
                                    >
                                        {#if log.type.includes("ZK")}
                                            <Shield size={10} strokeWidth={3} />
                                        {:else if log.type.includes("TX")}
                                            <Zap size={10} strokeWidth={3} />
                                        {:else if log.type.includes("PROTOCOL")}
                                            <Cpu size={10} strokeWidth={3} />
                                        {:else}
                                            <Terminal
                                                size={10}
                                                strokeWidth={3}
                                            />
                                        {/if}
                                        <span>{log.type}</span>
                                    </div>
                                    <span class="vessel-hash"
                                        >ID_{log.id
                                            .split("-")[0]
                                            .toUpperCase()}</span
                                    >
                                </div>
                                <div class="time-stamp">
                                    <Clock size={8} />
                                    <span>{formatTime(log.timestamp)}</span>
                                </div>
                            </div>
                            <p class="vessel-msg">{log.msg}</p>
                        </div>
                        <div class="vessel-glimmer"></div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>

    <!-- Footer Controls -->
    <footer class="manifold-footer">
        <div class="flex items-center justify-between w-full">
            <div class="flex items-center gap-3">
                <Activity size={12} class="text-white/20" />
                <span class="footer-label"
                    >Institutional_Bus_Monitoring_v4.8</span
                >
            </div>
            <div class="flex gap-4">
                <div class="footer-stat">
                    <span class="s-label">ERRORS</span>
                    <span class="s-value text-rose-400">0</span>
                </div>
                <div class="footer-stat">
                    <span class="s-label">VERIFIED</span>
                    <span class="s-value text-emerald-400">ALL</span>
                </div>
            </div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill shadow-cyan"></div>
        </div>
    </footer>
</div>

<style>
    .trace-manifold {
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
            rgba(34, 211, 238, 0.02),
            transparent
        );
        pointer-events: none;
    }
    .manifold-aura {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 200px;
        background: radial-gradient(
            circle at 0% 100%,
            rgba(34, 211, 238, 0.05),
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
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.2);
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
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    .header-telemetry {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 2px;
    }
    .tel-label {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .tel-value {
        font-size: 11px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }

    .manifold-body {
        flex: 1;
        padding: 2.5rem;
        overflow-y: auto;
        position: relative;
    }

    .event-stream {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .event-vessel {
        position: relative;
        padding-left: 2rem;
        transition: all 0.3s;
    }
    .vessel-line {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 1px;
        background: rgba(255, 255, 255, 0.05);
    }
    .event-vessel:hover .vessel-line {
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
    }

    .vessel-content {
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        transition: all 0.3s;
    }
    .event-vessel:hover .vessel-content {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(34, 211, 238, 0.2);
        transform: translateX(4px);
    }

    .type-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .vessel-hash {
        font-size: 8px;
        font-family: "JetBrains Mono", monospace;
        color: rgba(255, 255, 255, 0.2);
    }
    .time-stamp {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.1);
    }
    .vessel-msg {
        font-size: 11px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.5;
        margin-top: 0.5rem;
    }

    .vessel-glimmer {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(34, 211, 238, 0.05),
            transparent
        );
        transform: translateX(-100%);
        transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        pointer-events: none;
    }
    .event-vessel:hover .vessel-glimmer {
        transform: translateX(100%);
    }

    .manifold-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
    }
    .footer-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .footer-stat {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .s-label {
        font-size: 6px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
    }
    .s-value {
        font-size: 9px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .progress-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
    }
    .progress-fill {
        height: 100%;
        width: 100%;
        background: #22d3ee;
        animation: bar-pulse 4s infinite;
    }

    .empty-state {
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        opacity: 0.2;
    }
    .glimmer-circle {
        width: 40px;
        height: 40px;
        border: 2px solid #22d3ee;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    .empty-state p {
        font-size: 10px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.1);
        }
    }
    @keyframes bar-pulse {
        0%,
        100% {
            opacity: 0.4;
        }
        50% {
            opacity: 1;
        }
    }
    .shadow-cyan {
        box-shadow: 0 0 10px #22d3ee;
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
