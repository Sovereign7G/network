<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { api } from "$lib/services/api";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        Fingerprint,
        ShieldCheck,
        Globe,
        Crown,
        QrCode,
        Copy,
        CheckCircle2,
        Zap,
        Lock,
        Flame,
    } from "lucide-svelte";

    let identity: any = $state(null);
    let isLoading = $state(true);
    let copied = $state(false);

    onMount(async () => {
        try {
            identity = await api.request("/identity/verify");
        } catch (error) {
            console.error("Failed to load sovereign identity", error);
            // Fallback for demo
            identity = manifold.identity;
        } finally {
            isLoading = false;
        }
    });

    function copyDID() {
        if (!identity) return;
        navigator.clipboard.writeText(identity.did);
        copied = true;
        setTimeout(() => (copied = false), 2000);
    }
</script>

<div class="passport-manifold" in:fade>
    <div class="manifold-glass"></div>
    <div class="manifold-aura"></div>

    <!-- Institutional Header -->
    <header class="manifold-header">
        <div class="header-brand">
            <div class="icon-vessel shadow-blue">
                <Fingerprint size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Passport</h2>
                <div class="flex items-center gap-2">
                    <span class="subtitle">VERACITY_HIGH // PHASE_7</span>
                    <div class="status-pulse"></div>
                </div>
            </div>
        </div>
        <div class="header-badge">
            <ShieldCheck size={12} class="text-emerald-400" />
            <span>ZK_VERIFIED</span>
        </div>
    </header>

    <div class="manifold-body scrollbar-hide">
        {#if isLoading}
            <div class="manifesting-state">
                <div class="glimmer-circle"></div>
                <span class="manifesting-text"
                    >Manifesting_Sovereign_Identity...</span
                >
            </div>
        {:else if identity}
            <section class="identity-profile" in:fly={{ y: 20 }}>
                <div class="avatar-altar">
                    <div class="altar-orbit"></div>
                    <div class="altar-rings"></div>
                    <div class="avatar-vessel">
                        <Crown size={48} class="text-white/20" />
                    </div>
                </div>

                <div class="profile-meta">
                    <h2 class="display-name">{identity.profile.displayName}</h2>
                    <div class="region-tag">
                        <Globe size={10} class="text-cyan-400" />
                        <span>Nagano_Manifold // SHARD_01</span>
                    </div>
                </div>
            </section>

            <div class="telemetry-stack">
                <!-- DID Manifold -->
                <div class="tele-vessel group">
                    <header class="vessel-header">
                        <span class="v-label">Decentralized_Identifier</span>
                        <button onclick={copyDID} class="v-btn">
                            {#if copied}
                                <CheckCircle2
                                    size={12}
                                    class="text-emerald-400"
                                />
                            {:else}
                                <Copy
                                    size={12}
                                    class="group-hover:text-white transition-colors"
                                />
                            {/if}
                        </button>
                    </header>
                    <div class="v-content">
                        <code class="did-string">{identity.did}</code>
                    </div>
                </div>

                <!-- Resonance Level -->
                <div class="tele-vessel">
                    <header class="vessel-header">
                        <span class="v-label">Verification_Tier</span>
                        <span class="v-value"
                            >LEVEL_{identity.verificationLevel}</span
                        >
                    </header>
                    <div class="resonance-vitals">
                        <div class="vitals-track">
                            <div
                                class="vitals-fill"
                                style:width="{(identity.verificationLevel /
                                    10) *
                                    100}%"
                            ></div>
                        </div>
                        <div class="vitals-meta">
                            <span>REPUTATION_STABLE</span>
                            <span>PROG_82%</span>
                        </div>
                    </div>
                </div>

                <!-- Capabilities Matrix -->
                <div class="capability-matrix">
                    <div class="cap-card blue">
                        <header>
                            <Lock size={12} />
                            <span>ZK_ACCESS</span>
                        </header>
                        <p>Proof-verified entry active</p>
                    </div>
                    <div class="cap-card purple">
                        <header>
                            <QrCode size={12} />
                            <span>OFFLINE_GEN</span>
                        </header>
                        <p>Cold-start capability enabled</p>
                    </div>
                    <div class="cap-card gold">
                        <header>
                            <Flame size={12} />
                            <span>ARI_MULTIPLIER</span>
                        </header>
                        <p>Reputation-based scaling: 1.2x</p>
                    </div>
                </div>
            </div>

            <footer class="manifold-footer">
                <div class="flex items-center gap-3 justify-center mb-4">
                    <Zap size={10} class="text-white/20" />
                    <span class="footer-msg"
                        >"Causal integrity verified against Sovereign Mesh"</span
                    >
                </div>
                <div class="audit-link">
                    <span>Audit_Hash: 0xA7B2...F91E</span>
                </div>
            </footer>
        {/if}
    </div>
</div>

<style>
    .passport-manifold {
        height: 100%;
        background: rgba(10, 7, 15, 0.4);
        backdrop-filter: blur(60px);
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
        inset: 0;
        background: radial-gradient(
            circle at 0% 0%,
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
        z-index: 10;
    }

    .icon-vessel {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 20px rgba(14, 165, 233, 0.2);
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
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }

    .header-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 100px;
        color: #10b981;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
    }

    .manifold-body {
        flex: 1;
        padding: 2.5rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2.5rem;
        position: relative;
    }

    .identity-profile {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
        text-align: center;
    }

    .avatar-altar {
        position: relative;
        width: 140px;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .altar-orbit {
        position: absolute;
        inset: -10px;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: spin 40s linear infinite;
    }
    .altar-rings {
        position: absolute;
        inset: 0;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.02);
    }
    .avatar-vessel {
        width: 100px;
        height: 100px;
        background: #0c0e12;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        z-index: 2;
        position: relative;
    }

    .display-name {
        font-size: 28px;
        font-weight: 950;
        color: white;
        letter-spacing: -0.02em;
    }
    .region-tag {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .telemetry-stack {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    .tele-vessel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
        transition: all 0.3s;
    }
    .tele-vessel:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .vessel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .v-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .v-btn {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.2s;
    }
    .v-value {
        font-size: 11px;
        font-weight: 950;
        color: #22d3ee;
        font-family: "JetBrains Mono", monospace;
    }

    .did-string {
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        color: #22d3ee;
        word-break: break-all;
        opacity: 0.8;
    }

    .resonance-vitals {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .vitals-track {
        height: 6px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 100px;
        overflow: hidden;
    }
    .vitals-fill {
        height: 100%;
        background: linear-gradient(to right, #22d3ee, #6366f1);
        box-shadow: 0 0 15px rgba(34, 211, 238, 0.4);
    }
    .vitals-meta {
        display: flex;
        justify-content: space-between;
        font-size: 7px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .capability-matrix {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }
    .cap-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        transition: all 0.3s;
    }
    .cap-card:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.05);
    }
    .cap-card header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 8px;
        font-weight: 950;
        text-transform: uppercase;
    }
    .cap-card p {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.3);
        font-weight: 500;
        line-height: 1.3;
    }

    .cap-card.blue header {
        color: #22d3ee;
    }
    .cap-card.purple header {
        color: #c084fc;
    }
    .cap-card.gold header {
        color: #fbbf24;
    }

    .manifold-footer {
        margin-top: auto;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
    }
    .footer-msg {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-style: italic;
    }
    .audit-link {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.05);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .manifesting-state {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }
    .glimmer-circle {
        width: 44px;
        height: 44px;
        border: 2px solid rgba(34, 211, 238, 0.1);
        border-top-color: #22d3ee;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    .manifesting-text {
        font-size: 10px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
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
            opacity: 0.6;
            transform: scale(1.1);
        }
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
