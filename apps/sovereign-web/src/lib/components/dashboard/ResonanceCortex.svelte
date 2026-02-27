<script lang="ts">
    import { fade, slide, fly } from "svelte/transition";

    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Shield,
        Lock,
        Unlock,
        AlertTriangle,
        Fingerprint,
        ShieldAlert,
        Terminal,
        Cpu,
    } from "lucide-svelte";

    let permissionLevel = $derived(manifold.permissionLevel);

    const levelMetadata: Record<
        string,
        { label: string; color: string; icon: any; desc: string; tone: string }
    > = {
        GUEST: {
            label: "GUEST_UNAUTHENTICATED",
            color: "text-white/40",
            icon: Lock,
            desc: "Manifest through Internet Identity to begin.",
            tone: "rgba(255, 255, 255, 0.05)",
        },
        REGISTERED_PROSPECT: {
            label: "REGISTERED_PROSPECT",
            color: "text-blue-400",
            icon: Fingerprint,
            desc: "Initial resonance established. Limited manifold access.",
            tone: "rgba(59, 130, 246, 0.1)",
        },
        VERIFIED_CITIZEN: {
            label: "VERIFIED_CITIZEN",
            color: "text-emerald-400",
            icon: Shield,
            desc: "Institutional trust verified. Core rails unlocked.",
            tone: "rgba(16, 185, 129, 0.1)",
        },
        SOVEREIGN_OVERSEER: {
            label: "SOVEREIGN_OVERSEER",
            color: "text-purple-400",
            icon: Unlock,
            desc: "Maximum coherence achieved. Full protocol instantiation permitted.",
            tone: "rgba(168, 85, 247, 0.1)",
        },
    };

    let meta = $derived(levelMetadata[permissionLevel] || levelMetadata.GUEST);

    const gatingRules = [
        { name: "Core_Transfer", level: "REGISTERED_PROSPECT" },
        { name: "Policy_Vote", level: "VERIFIED_CITIZEN" },
        { name: "Singularity_Init", level: "SOVEREIGN_OVERSEER" },
        { name: "Shard_Mutation", level: "SOVEREIGN_OVERSEER" },
    ];

    function isUnlocked(ruleLevel: string) {
        if (ruleLevel === "SOVEREIGN_OVERSEER") return manifold.resonance > 95;
        if (ruleLevel === "VERIFIED_CITIZEN") return manifold.resonance > 85;
        return manifold.resonance > 0;
    }
</script>

<div class="cortex-shell" in:fade>
    <!-- Background Kinetic Aura -->
    <div
        class="cortex-aura"
        style:background="radial-gradient(circle at 0% 0%, {meta.tone} 0%, transparent
        70%)"
    ></div>

    <!-- Institutional Header -->
    <header class="cortex-header">
        <div class="header-brand">
            <div class="logo-box">
                <ShieldAlert size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Institutional_Cortex</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label">SECURITY_PLANE_ACTIVE</span>
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>
        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">RESONANCE</span>
                <span
                    class="tel-value {manifold.resonance < 85
                        ? 'text-rose-400'
                        : 'text-emerald-400'}">{manifold.resonance}%</span
                >
            </div>
        </div>
    </header>

    <div class="cortex-body scrollbar-hide">
        <!-- Permission Card -->
        <section class="identity-manifold" in:fly={{ y: 20, delay: 100 }}>
            <div class="id-icon-shell" style:color={meta.color.split("-")[1]}>
                <meta.icon size={24} />
            </div>
            <div class="id-content">
                <div class="flex items-center justify-between mb-1">
                    <span class="id-label">Clearance_Tier</span>
                    <span class="id-status {meta.color}">{permissionLevel}</span
                    >
                </div>
                <h3 class="id-title">{meta.label}</h3>
                <p class="id-desc">{meta.desc}</p>
            </div>
        </section>

        <!-- Gating Matrix -->
        <section class="matrix-viewport" in:fly={{ y: 20, delay: 200 }}>
            <header class="section-header">
                <Cpu size={12} class="text-white/40" />
                <h3>Protocol_Gating_Matrix</h3>
            </header>
            <div class="matrix-grid">
                {#each gatingRules as protocol}
                    <div
                        class="gate-card"
                        class:unlocked={isUnlocked(protocol.level)}
                    >
                        <div class="gate-info">
                            <span class="g-name">{protocol.name}</span>
                            <span class="g-req"
                                >REQ: {protocol.level.split("_").pop()}</span
                            >
                        </div>
                        <div class="gate-indicator">
                            {#if isUnlocked(protocol.level)}
                                <Unlock size={12} class="text-emerald-400" />
                            {:else}
                                <Lock size={12} class="text-rose-400/40" />
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        </section>

        <!-- Causal Log -->
        <section class="log-viewport" in:fly={{ y: 20, delay: 300 }}>
            <header class="section-header">
                <Terminal size={12} class="text-white/40" />
                <h3>High_Assurance_Log</h3>
            </header>
            <div class="log-vessel scrollbar-hide">
                {#each manifold.causalLog.slice(0, 8) as log}
                    <div class="log-entry" transition:slide>
                        <div class="log-meta">
                            <span class="l-type">{log.type}</span>
                            <span class="l-id"
                                >0x{(log.id || "").split("-")[0]}</span
                            >
                        </div>
                        <p class="l-msg">{log.msg}</p>
                        {#if log.signature}
                            <div class="l-sig">
                                SIGN: {log.signature.slice(0, 32)}...
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>
        </section>
    </div>

    <!-- Alarm Overlay -->
    {#if manifold.resonance < 85}
        <footer class="cortex-alert" in:fly={{ y: 100 }}>
            <AlertTriangle size={16} />
            <div class="alert-content">
                <span class="alert-title">Low_Resonance_Protocol_Active</span>
                <span class="alert-desc"
                    >Institutional gating engaged. Link Bio-Vault to restore
                    full coherence.</span
                >
            </div>
        </footer>
    {/if}
</div>

<style>
    .cortex-shell {
        height: 100%;
        background: rgba(10, 5, 15, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
        position: relative;
    }

    .cortex-aura {
        position: absolute;
        inset: 0;
        pointer-events: none;
        transition: background 1s ease;
    }

    .cortex-header {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logo-box {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(6, 182, 212, 0.2);
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
        color: #06b6d4;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .phase-pulsar {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #06b6d4;
        box-shadow: 0 0 10px #06b6d4;
        animation: pulse 2s infinite;
    }

    .header-telemetry .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: block;
        text-align: right;
    }

    .header-telemetry .tel-value {
        font-size: 18px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .cortex-body {
        flex: 1;
        padding: 2rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .identity-manifold {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }

    .id-icon-shell {
        width: 56px;
        height: 56px;
        background: currentColor;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .id-content {
        flex: 1;
    }
    .id-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }
    .id-status {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
    }
    .id-title {
        font-size: 14px;
        font-weight: 950;
        color: white;
        margin-bottom: 0.5rem;
    }
    .id-desc {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .section-header h3 {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .matrix-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
    }

    .gate-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .gate-card.unlocked {
        background: rgba(16, 185, 129, 0.05);
        border-color: rgba(16, 185, 129, 0.1);
    }

    .gate-info {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .g-name {
        font-size: 10px;
        font-weight: 900;
        color: white;
    }
    .g-req {
        font-size: 7px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
    }

    .log-vessel {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1rem;
        height: 200px;
        overflow-y: auto;
    }

    .log-entry {
        padding: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .log-entry:last-child {
        border-bottom: none;
    }

    .log-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .l-type {
        font-size: 8px;
        font-weight: 950;
        color: #06b6d4;
        text-transform: uppercase;
    }
    .l-id {
        font-size: 8px;
        font-family: "JetBrains Mono", monospace;
        color: rgba(255, 255, 255, 0.2);
    }
    .l-msg {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.6);
    }
    .l-sig {
        font-size: 7px;
        font-family: "JetBrains Mono", monospace;
        color: rgba(255, 255, 255, 0.1);
    }

    .cortex-alert {
        padding: 1.5rem 2rem;
        background: rgba(244, 63, 94, 0.1);
        border-top: 1px solid rgba(244, 63, 94, 0.2);
        display: flex;
        gap: 1rem;
        color: #f43f5e;
        align-items: center;
        animation: alert-pulse 2s infinite;
    }

    .alert-content {
        display: flex;
        flex-direction: column;
    }
    .alert-title {
        font-size: 10px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .alert-desc {
        font-size: 8px;
        font-weight: 800;
        opacity: 0.8;
    }

    @keyframes alert-pulse {
        0%,
        100% {
            background: rgba(244, 63, 94, 0.1);
        }
        50% {
            background: rgba(244, 63, 94, 0.2);
        }
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.2);
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
