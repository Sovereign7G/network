<script lang="ts">
    import { fade, slide, scale } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import {
        Compass,
        Layers,
        MessageSquareCode,
        Hexagon,
        Zap,
        ShieldCheck,
    } from "lucide-svelte";
    import { sovereignPhilosophy } from "$lib/services/philosophy-engine.svelte";
    import { designEngineering } from "$lib/services/design-engineering-engine.svelte";

    const tabs = ["manifold", "modules", "decisions"] as const;
    type TabType = (typeof tabs)[number];
    let activeTab = $state<TabType>("manifold");

    function getStanceColor(stance: string) {
        switch (stance) {
            case "strategic":
                return "#10b981";
            case "tactical":
                return "#f59e0b";
            case "emergency":
                return "#ef4444";
            default:
                return "#94a3b8";
        }
    }
</script>

<div class="philosophy-shell">
    <!-- Institutional Header -->
    <header class="phi-header">
        <div class="phi-brand">
            <div class="phi-logo">
                <Compass size={18} class="text-white" />
            </div>
            <div class="phi-title">
                <h3>Sovereign_Logic_Manifold</h3>
                <span class="phi-subtitle">Cognitive_Architecture_v4.0</span>
            </div>
        </div>

        <div class="phi-metrics-core">
            <div class="phi-stat">
                <span class="phi-label">COHESION_INDEX</span>
                <span class="phi-value text-emerald-400"
                    >{sovereignPhilosophy.stats.cohesion}</span
                >
            </div>
            <div class="phi-stat">
                <span class="phi-label">COMPLEXITY_RADIUS</span>
                <span
                    class="phi-value"
                    class:text-rose-400={sovereignPhilosophy.metrics
                        .globalComplexity > 20}
                >
                    {sovereignPhilosophy.stats.complexity}
                </span>
            </div>
        </div>
    </header>

    <!-- Navigation Tab System -->
    <nav class="phi-tabs">
        {#each tabs as tab}
            <button
                class="phi-tab-btn"
                class:active={activeTab === tab}
                onclick={() => (activeTab = tab)}
            >
                <span class="tab-label">{tab}</span>
                {#if activeTab === tab}
                    <div
                        class="tab-active-indicator"
                        in:scale={{
                            duration: 400,
                            easing: cubicOut,
                        }}
                    ></div>
                {/if}
            </button>
        {/each}
    </nav>

    <!-- Content Engine -->
    <div class="phi-content-viewport">
        {#if activeTab === "manifold"}
            <div class="phi-manifold-view" in:fade={{ duration: 400 }}>
                <div class="phi-hero-grid">
                    <div class="phi-hero-card">
                        <Layers size={18} class="text-indigo-400 mb-4" />
                        <span class="phi-hero-val"
                            >{designEngineering.foundationIntegrity}%</span
                        >
                        <span class="phi-hero-label">Foundation_Integrity</span>
                        <div class="phi-progress-track">
                            <div
                                class="phi-progress-fill"
                                style="width: {designEngineering.foundationIntegrity}%"
                            ></div>
                        </div>
                    </div>
                    <div class="phi-hero-card">
                        <ShieldCheck size={18} class="text-emerald-400 mb-4" />
                        <span class="phi-hero-val text-emerald-400"
                            >{designEngineering.eniScore}</span
                        >
                        <span class="phi-hero-label"
                            >Experience_Nuance_Index</span
                        >
                        <p class="phi-hero-desc">
                            Targeting Product Mastery via metabolic resonance
                            and high-fidelity delighters.
                        </p>
                    </div>
                </div>

                <div class="phi-manifesto-block">
                    <div class="flex items-center gap-2 mb-6">
                        <Hexagon size={12} class="text-indigo-400" />
                        <h4
                            class="text-[10px] font-black uppercase tracking-[0.2em] text-white/40"
                        >
                            Sovereign_Principles
                        </h4>
                    </div>

                    <div class="phi-principle-list">
                        <div class="phi-principle">
                            <div class="phi-dot-box">
                                <div class="phi-dot bg-emerald-400"></div>
                            </div>
                            <div class="phi-p-content">
                                <strong>Strategic_Stance_Primacy</strong>
                                <p>
                                    Mandatory 20% investment in long-term design
                                    health. Resist tactical tornadoes.
                                </p>
                            </div>
                        </div>
                        <div class="phi-principle">
                            <div class="phi-dot-box">
                                <div class="phi-dot bg-indigo-400"></div>
                            </div>
                            <div class="phi-p-content">
                                <strong>Extreme_Information_Hiding</strong>
                                <p>
                                    Powerful internal logic masked behind
                                    minimalist, high-assurance interfaces.
                                </p>
                            </div>
                        </div>
                        <div class="phi-principle">
                            <div class="phi-dot-box">
                                <div class="phi-dot bg-fuchsia-400"></div>
                            </div>
                            <div class="phi-p-content">
                                <strong>Strategy-First_Implementation</strong>
                                <p>
                                    The "Anti-Jump Directive": No UI is forged
                                    without a documented foundation (IA/Flow).
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <button
                    class="phi-action-btn"
                    onclick={() => sovereignPhilosophy.runDesignReview()}
                >
                    <Zap size={14} />
                    <span>Initiate_Strategic_Refactor_Loop</span>
                </button>
            </div>
        {:else if activeTab === "modules"}
            <div class="phi-modules-grid" in:fade={{ duration: 400 }}>
                {#each sovereignPhilosophy.allModules as mod (mod.id)}
                    <div class="phi-mod-card">
                        <div class="flex items-center justify-between mb-2">
                            <div class="flex items-center gap-2">
                                <div
                                    class="w-1.5 h-1.5 rounded-full"
                                    style="background: {getStanceColor(
                                        mod.stance,
                                    )}"
                                ></div>
                                <span class="text-[11px] font-black text-white"
                                    >{mod.id}</span
                                >
                            </div>
                            <span
                                class="text-[7px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full border"
                                style="color: {getStanceColor(
                                    mod.stance,
                                )}; border-color: {getStanceColor(
                                    mod.stance,
                                )}40"
                            >
                                {mod.stance}
                            </span>
                        </div>
                        <span
                            class="text-[8px] font-mono text-white/20 block truncate mb-4"
                            >{mod.path}</span
                        >

                        <div
                            class="grid grid-cols-3 gap-4 pt-4 border-t border-white/5"
                        >
                            <div class="flex flex-col">
                                <span
                                    class="text-[6px] font-black text-white/20 uppercase mb-1"
                                    >Depth</span
                                >
                                <span
                                    class="text-[13px] font-black font-mono transition-colors"
                                    class:text-emerald-400={mod.depth > 7}
                                    >{mod.depth.toFixed(1)}</span
                                >
                            </div>
                            <div class="flex flex-col">
                                <span
                                    class="text-[6px] font-black text-white/20 uppercase mb-1"
                                    >Hiding</span
                                >
                                <span
                                    class="text-[13px] font-black font-mono text-indigo-400"
                                    >{mod.hidingScore}%</span
                                >
                            </div>
                            <div class="flex flex-col">
                                <span
                                    class="text-[6px] font-black text-white/20 uppercase mb-1"
                                    >Obscurity</span
                                >
                                <span
                                    class="text-[13px] font-black font-mono text-rose-400"
                                    >{mod.obscurity}%</span
                                >
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {:else if activeTab === "decisions"}
            <div class="phi-decisions-scroll" in:fade={{ duration: 400 }}>
                {#each sovereignPhilosophy.allDecisions as dec}
                    <div class="phi-dec-item" transition:slide>
                        <div
                            class="phi-dec-impact"
                            class:positive={dec.impact === "positive"}
                            class:negative={dec.impact === "negative"}
                        ></div>
                        <div class="flex-1">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-3">
                                    <span
                                        class="text-[10px] font-black text-white"
                                        >{dec.decision}</span
                                    >
                                    <span class="phi-dec-tag">{dec.pillar}</span
                                    >
                                </div>
                                <span class="text-[8px] font-mono text-white/20"
                                    >{new Date(
                                        dec.timestamp,
                                    ).toLocaleTimeString()}</span
                                >
                            </div>
                            <div class="flex items-start gap-2">
                                <MessageSquareCode
                                    size={10}
                                    class="text-white/20 mt-1"
                                />
                                <p
                                    class="text-[9px] text-white/40 font-bold italic leading-relaxed"
                                >
                                    {dec.rationale}
                                </p>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>

<style>
    .philosophy-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        backdrop-filter: blur(40px);
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        position: relative;
        overflow: hidden;
    }

    .phi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2.5rem;
    }

    .phi-logo {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.2);
    }

    .phi-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .phi-title h3 {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.05em;
        margin: 0;
    }

    .phi-subtitle {
        font-size: 8px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .phi-metrics-core {
        display: flex;
        gap: 2rem;
    }

    .phi-stat {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .phi-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
        margin-bottom: 2px;
    }

    .phi-value {
        font-size: 16px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
    }

    .phi-tabs {
        display: flex;
        gap: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
    }

    .phi-tab-btn {
        padding: 0.75rem 0.5rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.3);
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        position: relative;
        cursor: pointer;
        transition: color 0.3s;
    }

    .phi-tab-btn.active {
        color: white;
    }

    .tab-active-indicator {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #6366f1;
        border-radius: 100px;
    }

    .phi-content-viewport {
        flex: 1;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .phi-hero-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .phi-hero-card {
        padding: 1.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        display: flex;
        flex-direction: column;
    }

    .phi-hero-val {
        font-size: 28px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        margin-bottom: 0.25rem;
    }

    .phi-hero-label {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .phi-progress-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 100px;
        margin-top: 1rem;
        overflow: hidden;
    }

    .phi-progress-fill {
        height: 100%;
        background: linear-gradient(to right, #6366f1, #a855f7);
        border-radius: 100px;
    }

    .phi-hero-desc {
        font-size: 9px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.2);
        margin-top: 0.75rem;
        line-height: 1.5;
    }

    .phi-manifesto-block {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .phi-principle {
        display: flex;
        gap: 1.25rem;
        margin-bottom: 1.5rem;
    }

    .phi-dot-box {
        padding-top: 0.25rem;
    }

    .phi-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    }

    .phi-p-content strong {
        display: block;
        font-size: 11px;
        font-weight: 900;
        color: white;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .phi-p-content p {
        font-size: 9px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.4);
        line-height: 1.6;
        margin: 0;
    }

    .phi-action-btn {
        width: 100%;
        padding: 1.25rem;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 18px;
        color: #818cf8;
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
    }

    .phi-action-btn:hover {
        background: rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
    }

    .phi-mod-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .phi-dec-item {
        display: flex;
        gap: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        padding: 1.25rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        border-left: 2px solid rgba(255, 255, 255, 0.05);
    }

    .phi-dec-impact.positive {
        border-left-color: #10b981;
    }
    .phi-dec-impact.negative {
        border-left-color: #ef4444;
    }

    .phi-dec-tag {
        font-size: 7px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #818cf8;
        background: rgba(99, 102, 241, 0.1);
        padding: 2px 8px;
        border-radius: 100px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }

    .phi-content-viewport::-webkit-scrollbar {
        width: 4px;
    }
    .phi-content-viewport::-webkit-scrollbar-track {
        background: transparent;
    }
    .phi-content-viewport::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
