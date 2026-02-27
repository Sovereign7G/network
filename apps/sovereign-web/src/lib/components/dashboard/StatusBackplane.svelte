<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly } from "svelte/transition";
    import { Cpu, Globe, Activity, Zap, Shield } from "lucide-svelte";

    // Link to master state
    let protocols = $derived(manifold.foreignProtocols);
    let resonance = $derived(manifold.resonance);
    let photonic = $derived(manifold.photonicGlow);
</script>

<div class="status-backplane-manifold" transition:fade>
    <!-- Systemic Refinement Loop (Top Section) -->
    <div class="protocol-matrix">
        {#each protocols as protocol (protocol.id)}
            <div
                class="protocol-vessel"
                transitionfly={{ x: -20, delay: protocol.id.length * 10 }}
                class:optimizing={protocol.status === "OPTIMIZING"}
            >
                <div class="vessel-glow"></div>
                <div class="vessel-content">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-3">
                            <div
                                class="icon-shell"
                                class:pulse={protocol.status === "OPTIMIZING"}
                            >
                                <Cpu size={12} />
                            </div>
                            <div class="flex flex-col">
                                <h4 class="p-name">{protocol.name}</h4>
                                <span class="p-status uppercase"
                                    >{protocol.status}</span
                                >
                            </div>
                        </div>
                        <span
                            class="p-health {protocol.health < 80
                                ? 'text-rose-400'
                                : 'text-cyan-400'}">{protocol.health}%</span
                        >
                    </div>

                    <div class="health-track">
                        <div
                            class="health-fill"
                            style:width="{protocol.health}%"
                            style:background={protocol.health < 80
                                ? "#f43f5e"
                                : "#22d3ee"}
                        ></div>
                    </div>

                    {#if protocol.status === "OPTIMIZING"}
                        <div class="scan-line"></div>
                    {/if}
                </div>
            </div>
        {/each}
    </div>

    <!-- Global Resonance HUD (Bottom Section) -->
    <section class="resonance-manifold" in:fly={{ y: 20 }}>
        <div class="manifold-glass"></div>
        <div class="flex items-center gap-4 mb-5">
            <div class="globe-vessel">
                <Globe size={20} class="text-cyan-400 relative z-10" />
                <div class="globe-aura"></div>
                <div class="globe-ping"></div>
            </div>
            <div class="flex-1">
                <div class="flex justify-between items-center mb-2">
                    <span class="m-label">DaVinci_Resonance</span>
                    <span
                        class="m-value {resonance < 85
                            ? 'text-rose-400'
                            : 'text-cyan-400'}">{resonance.toFixed(1)}%</span
                    >
                </div>
                <div class="m-track">
                    <div
                        class="m-fill"
                        style:width="{resonance}%"
                        class:crisis={resonance < 85}
                    ></div>
                </div>
            </div>
        </div>

        <div class="telemetry-manifold">
            <div class="tel-item">
                <span class="t-label">Photonic_Cohesion</span>
                <div class="flex items-center gap-2">
                    <Zap size={10} class="text-amber-400" />
                    <span class="t-value"
                        >{(photonic.coherence * 100).toFixed(1)}%</span
                    >
                </div>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-item text-right">
                <span class="t-label">Trust_Matrix</span>
                <div class="flex items-center gap-2 justify-end">
                    <Shield size={10} class="text-emerald-400" />
                    <span class="t-value text-white"
                        >{manifold.trustMatrix.length}_ACTIVE</span
                    >
                </div>
            </div>
        </div>

        <div class="manifold-footer">
            <Activity size={10} class="text-white/20" />
            <span>Sfumato_Validated_v5.1 // Leonardo Pillar</span>
        </div>
    </section>
</div>

<style>
    .status-backplane-manifold {
        position: fixed;
        bottom: 2.5rem;
        left: 2.5rem;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        width: 320px;
        font-family: "Outfit", sans-serif;
    }

    .protocol-matrix {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .protocol-vessel {
        background: rgba(10, 5, 15, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .protocol-vessel:hover {
        transform: translateX(8px);
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(34, 211, 238, 0.2);
    }

    .vessel-glow {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 0% 50%,
            rgba(34, 211, 238, 0.05),
            transparent 70%
        );
        pointer-events: none;
    }

    .icon-shell {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.4);
        transition: all 0.3s;
    }

    .icon-shell.pulse {
        background: rgba(34, 211, 238, 0.1);
        border-color: rgba(34, 211, 238, 0.3);
        color: #22d3ee;
        animation: shell-pulse 2s infinite;
    }

    .p-name {
        font-size: 11px;
        font-weight: 950;
        color: white;
        letter-spacing: 0.02em;
    }
    .p-status {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
    }
    .p-health {
        font-size: 13px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .health-track {
        height: 3px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 100px;
        overflow: hidden;
    }
    .health-fill {
        height: 100%;
        transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 0 10px currentColor;
    }

    .scan-line {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to right,
            transparent,
            rgba(34, 211, 238, 0.05),
            transparent
        );
        animation: scan 2s linear infinite;
        pointer-events: none;
    }

    .resonance-manifold {
        background: rgba(10, 5, 25, 0.5);
        backdrop-filter: blur(60px);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 28px;
        padding: 1.75rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
    }

    .manifold-glass {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.05),
            transparent
        );
        pointer-events: none;
    }

    .globe-vessel {
        position: relative;
        width: 44px;
        height: 44px;
        background: rgba(34, 211, 238, 0.05);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(34, 211, 238, 0.1);
    }

    .globe-ping {
        position: absolute;
        inset: -2px;
        border: 1px solid #22d3ee;
        border-radius: 16px;
        animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
        opacity: 0;
    }

    .m-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .m-value {
        font-size: 16px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }
    .m-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        overflow: hidden;
    }
    .m-fill {
        height: 100%;
        background: linear-gradient(to right, #06b6d4, #6366f1);
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    }
    .m-fill.crisis {
        background: #f43f5e;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.4);
    }

    .telemetry-manifold {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        margin-top: 1.5rem;
        padding-top: 1.25rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .tel-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .t-label {
        font-size: 6px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .t-value {
        font-size: 11px;
        font-weight: 950;
        color: #22d3ee;
    }
    .tel-divider {
        width: 1px;
        height: 32px;
        background: rgba(255, 255, 255, 0.05);
        margin: 0 1.5rem;
    }

    .manifold-footer {
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    @keyframes scan {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(200%);
        }
    }
    @keyframes ping {
        75%,
        100% {
            transform: scale(1.6);
            opacity: 0;
        }
        0% {
            transform: scale(1);
            opacity: 0.6;
        }
    }
    @keyframes shell-pulse {
        0%,
        100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
</style>
