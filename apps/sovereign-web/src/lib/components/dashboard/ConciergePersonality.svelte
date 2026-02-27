<script lang="ts">
    import { llmService } from "$lib/services/llm-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { scale } from "svelte/transition";
    import {
        Brain,
        Wind,
        Sparkles,
        Settings,
        Cpu,
        Fingerprint,
        Activity,
        Zap as ZapIcon,
        Sparkles as SparklesIcon,
        TrendingUp,
        Compass,
    } from "lucide-svelte";
    import { suggestionEngine } from "$lib/services/suggestion-engine.svelte";

    let config = $state(llmService?.getConfig() || { provider: "openai" });
    let activePersonality = $state("Institutional / Precise");

    const personalities = [
        {
            name: "Institutional / Precise",
            icon: ZapIcon,
            desc: "Systemic veracity & protocol-level precision.",
        },
        {
            name: "Sovereign / Tribal",
            icon: Wind,
            desc: "Community resonance & pluralistic values.",
        },
        {
            name: "Ethereal / Oracle",
            icon: Sparkles,
            desc: "Future drift synthesis & pattern mapping.",
        },
    ];

    function updateProvider(provider: "openai" | "anthropic") {
        if (!llmService) return;
        llmService.updateConfig({
            provider,
            model:
                provider === "openai"
                    ? "gpt-4-turbo-preview"
                    : "claude-3-opus-20240229",
        });
        config = llmService.getConfig();
        manifold.recordEvent(
            "AI_SYNC",
            `Neural bridge established via ${provider.toUpperCase()}`,
        );
    }
</script>

<div class="intelligence-core">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
            <div class="core-icon-shell">
                <Brain size={18} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h3
                    class="text-[10px] font-black uppercase tracking-[0.2em] text-white"
                >
                    Neural_Concierge
                </h3>
                <span
                    class="text-[8px] font-bold text-white/20 uppercase tracking-[0.1em]"
                    >Intelligence_Manifest_v4.2</span
                >
            </div>
        </div>
        <div class="aal-tag">AAL3 Intelligence</div>
    </div>

    <!-- Provider Grid -->
    <div class="grid grid-cols-2 gap-3 mb-8">
        {#each ["openai", "anthropic"] as provider}
            <button
                onclick={() =>
                    updateProvider(provider as "openai" | "anthropic")}
                class="provider-btn"
                class:active={config.provider === provider}
            >
                {#if provider === "openai"}
                    <Cpu size={16} />
                {:else}
                    <Fingerprint size={16} />
                {/if}
                <span class="text-[9px] font-black uppercase tracking-widest"
                    >{provider}</span
                >
                {#if config.provider === provider}
                    <div class="indicator" in:scale></div>
                {/if}
            </button>
        {/each}
    </div>

    <!-- personality Matrix -->
    <div class="flex-1 space-y-6">
        <div class="flex items-center gap-2 px-1">
            <Activity size={10} class="text-white/20" />
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                >Behavioral_Vector_Matrix</span
            >
        </div>

        <div class="personality-list scrollbar-hide">
            {#each personalities as p}
                <button
                    onclick={() => (activePersonality = p.name)}
                    class="personality-card"
                    class:active={activePersonality === p.name}
                >
                    <div class="flex items-center gap-4">
                        <div
                            class="p-icon"
                            class:active={activePersonality === p.name}
                        >
                            <p.icon size={14} />
                        </div>
                        <div class="flex flex-col">
                            <span class="p-name">{p.name}</span>
                            <span class="p-desc">{p.desc}</span>
                        </div>
                    </div>
                </button>
            {/each}
        </div>
    </div>

    <!-- Smart Suggestions (Anticipatory Intelligence) -->
    <div class="suggestions-hub mt-8">
        <div class="flex items-center gap-2 px-1 mb-4">
            <TrendingUp size={10} class="text-white/20" />
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                >Anticipatory_Projections</span
            >
        </div>

        <div class="suggestions-grid">
            {#each suggestionEngine.suggestions as s (s.id)}
                <button
                    class="suggestion-pill group"
                    onclick={s.action?.handler}
                >
                    <div class="pill-icon">
                        {#if s.type === "ACTION"}<ZapIcon size={10} />
                        {:else if s.type === "OPTIMIZATION"}<SparklesIcon
                                size={10}
                            />
                        {:else if s.type === "INSIGHT"}<Activity size={10} />
                        {:else}<Compass size={10} />{/if}
                    </div>
                    <div class="pill-content">
                        <span class="pill-label">{s.title}</span>
                        <span class="pill-desc">{s.description}</span>
                    </div>
                </button>
            {/each}
        </div>
    </div>

    <!-- Live Neural Trace -->
    <div class="neural-trace">
        <div class="trace-bg">
            <svg viewBox="0 0 400 100" class="w-full h-full opacity-20">
                <path
                    d="M0 50 Q 50 20, 100 50 T 200 50 T 300 50 T 400 50"
                    fill="none"
                    stroke="#a855f7"
                    stroke-width="2"
                >
                    <animate
                        attributeName="d"
                        dur="5s"
                        repeatCount="indefinite"
                        values="M0 50 Q 50 20, 100 50 T 200 50 T 300 50 T 400 50; M0 50 Q 50 80, 100 50 T 200 50 T 300 50 T 400 50; M0 50 Q 50 20, 100 50 T 200 50 T 300 50 T 400 50"
                    />
                </path>
            </svg>
        </div>
        <div class="trace-overlay">
            <div class="flex flex-col">
                <span class="text-[7px] font-black text-white/20 uppercase mb-1"
                    >Neural_Drift_Rate</span
                >
                <span class="text-xs font-black text-white">0.0824_Hz</span>
            </div>
            <button class="settings-btn">
                <Settings size={14} />
            </button>
        </div>
    </div>
</div>

<style>
    .intelligence-core {
        height: 100%;
        background: rgba(10, 15, 25, 0.4);
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

    .core-icon-shell {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #a855f7, #6366f1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(168, 85, 247, 0.2);
    }

    .aal-tag {
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #a855f7;
        background: rgba(168, 85, 247, 0.1);
        padding: 6px 14px;
        border-radius: 100px;
        border: 1px solid rgba(168, 85, 247, 0.2);
    }

    .provider-btn {
        padding: 1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.2s;
        position: relative;
        cursor: pointer;
    }

    .provider-btn.active {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .indicator {
        position: absolute;
        top: 8px;
        right: 8px;
        width: 4px;
        height: 4px;
        background: #a855f7;
        border-radius: 50%;
        box-shadow: 0 0 10px #a855f7;
    }

    .personality-card {
        width: 100%;
        padding: 1.25rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: left;
    }

    .personality-card:hover {
        background: rgba(255, 255, 255, 0.04);
        transform: translateX(4px);
    }

    .personality-card.active {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(168, 85, 247, 0.3);
    }

    .p-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.2);
        transition: all 0.3s;
    }

    .p-icon.active {
        background: rgba(168, 85, 247, 0.15);
        color: #a855f7;
        transform: scale(1.1);
    }

    .p-name {
        display: block;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
        margin-bottom: 2px;
    }

    .p-desc {
        display: block;
        font-size: 9px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.3);
        line-height: 1.4;
    }

    /* Suggestions Hub */
    .suggestions-grid {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .suggestion-pill {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: left;
    }

    .suggestion-pill:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(168, 85, 247, 0.4);
        transform: translateY(-2px);
    }

    .pill-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(168, 85, 247, 0.1);
        color: #a855f7;
        border-radius: 8px;
        flex-shrink: 0;
    }

    .pill-content {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .pill-label {
        font-size: 10px;
        font-weight: 800;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .pill-desc {
        font-size: 8px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.4);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .neural-trace {
        margin-top: auto;
        height: 64px;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        position: relative;
        overflow: hidden;
    }

    .trace-bg {
        position: absolute;
        inset: 0;
    }

    .trace-overlay {
        position: relative;
        z-index: 10;
        padding: 0 1.25rem;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .settings-btn {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.2s;
    }

    .settings-btn:hover {
        background: rgba(255, 255, 255, 0.06);
        color: white;
    }
</style>
