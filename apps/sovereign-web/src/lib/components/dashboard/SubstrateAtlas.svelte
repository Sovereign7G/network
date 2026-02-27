<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly } from "svelte/transition";
    import { MapPin, Zap, Layers, Activity, Crosshair } from "lucide-svelte";
    import type { PointStatus } from "$lib/types";

    // 🗺️ SUBSTRATE ATLAS: Global Industrial Choke Points
    const points = $derived(manifold.substrateAtlas.points);

    function getStatusColor(status: PointStatus | string) {
        switch (status) {
            case "PROLONGED":
                return "text-amber-400";
            case "INITIATED":
                return "text-cyan-400";
            case "STABLE":
                return "text-emerald-400";
            default:
                return "text-white/40";
        }
    }
</script>

<div class="atlas-manifold" in:fade>
    <div class="manifold-glass"></div>
    <div class="manifold-aura"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="header-brand">
            <div class="icon-vessel shadow-indigo">
                <MapPin size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Substrate_Atlas</h2>
                <div class="flex items-center gap-2">
                    <span class="subtitle">Industrial_Choke_Point_Registry</span
                    >
                    <div class="status-pulse"></div>
                </div>
            </div>
        </div>
        <div class="header-telemetry flex flex-col items-end gap-2">
            <button
                onclick={() => {
                    throw new Error(
                        "Structural Integrity Compromised: Borel-Stable violation.",
                    );
                }}
                class="px-2 py-1 bg-rose-500/10 border border-rose-500/20 rounded text-[7px] font-black uppercase text-rose-500 hover:bg-rose-500 hover:text-white transition-all"
            >
                Stress_Kernel
            </button>
            <div class="flex flex-col items-end">
                <span class="tel-label">MESH_SYNC</span>
                <span class="tel-value">92%_OPTIMIZED</span>
            </div>
        </div>
    </header>

    <div class="manifold-body scrollbar-hide">
        <div class="atlas-grid">
            {#each points as point}
                <div class="choke-vessel group" in:fly={{ y: 20 }}>
                    <div class="vessel-aura"></div>
                    <div class="vessel-header">
                        <div class="flex flex-col gap-1">
                            <div class="top-meta">
                                <span class="region-badge">{point.region}</span>
                                <div class="id-wrapper">
                                    <Crosshair
                                        size={10}
                                        class="text-white/20 group-hover:text-indigo-400 transition-colors"
                                    />
                                    <h4 class="vessel-id">{point.id}</h4>
                                </div>
                            </div>
                            <span class="scarcity-label"
                                >Scarcity: {point.scarcity}</span
                            >
                        </div>
                        <div class="status-box">
                            <span
                                class="status-tag {getStatusColor(
                                    point.status,
                                )}">{point.status}</span
                            >
                            <div class="tps-meter">
                                <Zap size={8} class="text-cyan-400" />
                                <span class="tps-value"
                                    >{(point.tps / 1000).toFixed(0)}k
                                    <small>TPS</small></span
                                >
                            </div>
                        </div>
                    </div>

                    <div class="vessel-telemetry">
                        <div class="tel-track">
                            <div
                                class="tel-fill"
                                style:width="{(point.tps / 100000) * 100}%"
                            ></div>
                        </div>
                        <div class="tel-audit">
                            <Activity size={8} class="text-white/20" />
                            <span>Propagation_Active</span>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    </div>

    <!-- Footer Control Stratum -->
    <footer class="manifold-footer">
        <div class="footer-content">
            <div class="flex items-center gap-3">
                <Layers size={12} class="text-indigo-400/60" />
                <span class="footer-label"
                    >Substrate_Refinement: CONTINUOUS_LOOP</span
                >
            </div>
            <div class="footer-hash">
                <span>COORD_SYMMETRY: L-42</span>
            </div>
        </div>
        <div class="ambient-pulse"></div>
    </footer>
</div>

<style>
    .atlas-manifold {
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
            rgba(99, 102, 241, 0.05),
            transparent
        );
        pointer-events: none;
    }
    .manifold-aura {
        position: absolute;
        inset: -100px;
        background: radial-gradient(
            circle at top right,
            rgba(99, 102, 241, 0.05),
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
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
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
        background: #6366f1;
        box-shadow: 0 0 10px #6366f1;
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
        color: #6366f1;
        font-family: "JetBrains Mono", monospace;
    }

    .manifold-body {
        flex: 1;
        padding: 2.5rem;
        overflow-y: auto;
        position: relative;
    }
    .atlas-grid {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .choke-vessel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 28px;
        padding: 1.75rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .choke-vessel:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
    }

    .vessel-aura {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 100% 0%,
            rgba(99, 102, 241, 0.05),
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.4s;
    }
    .choke-vessel:hover .vessel-aura {
        opacity: 1;
    }

    .vessel-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
        position: relative;
        z-index: 10;
    }
    .top-meta {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }
    .region-badge {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.05);
        padding: 4px 8px;
        border-radius: 100px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .id-wrapper {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .vessel-id {
        font-size: 13px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    .scarcity-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .status-box {
        text-align: right;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .status-tag {
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .tps-meter {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: flex-end;
    }
    .tps-value {
        font-size: 11px;
        font-weight: 950;
        color: white;
        font-family: "JetBrains Mono", monospace;
    }
    .tps-value small {
        font-size: 7px;
        opacity: 0.4;
    }

    .vessel-telemetry {
        position: relative;
        z-index: 10;
    }
    .tel-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 100px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }
    .tel-fill {
        height: 100%;
        background: #6366f1;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
        border-radius: 100px;
        transition: width 1.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .tel-audit {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }

    .manifold-footer {
        padding: 1.5rem 2.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .footer-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(99, 102, 241, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .footer-hash {
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.1);
    }

    .ambient-pulse {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(
            to right,
            transparent,
            #6366f1,
            transparent
        );
        opacity: 0.2;
        animation: move 4s linear infinite;
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
    @keyframes move {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(100%);
        }
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
