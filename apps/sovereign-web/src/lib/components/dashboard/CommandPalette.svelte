<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";

    import {
        ShieldAlert,
        Sparkles,
        Brain,
        Search,
        Command,
        Zap,
        Lock,
        Activity,
        Globe,
    } from "lucide-svelte";

    let { onExecute } = $props<{
        onExecute: (cmd: string, args?: any) => void;
    }>();

    let isOpen = $state(false);
    let query = $state("");
    let selectedIndex = $state(0);
    let isAnalyzing = $state(false);
    let aiSuggestion = $state<string | null>(null);

    async function analyzeIntent() {
        if (!query || query.length < 3) {
            aiSuggestion = null;
            return;
        }

        isAnalyzing = true;
        try {
            const q = query.toLowerCase();
            if (
                q.includes("harden") ||
                q.includes("secure") ||
                q.includes("lock")
            ) {
                aiSuggestion = "ENGAGE_NIST_AAL3_DEFENSE_LOOP";
            } else if (
                q.includes("money") ||
                q.includes("vault") ||
                q.includes("wealth")
            ) {
                aiSuggestion = "MANIFEST_TREASURY_INTELLIGENCE";
            } else if (q.includes("reset") || q.includes("clear")) {
                aiSuggestion = "INITIATE_MULTIVERSAL_SYNC";
            } else if (q.includes("zk") || q.includes("proof")) {
                aiSuggestion = "BATCH_VERIFY_ZK_ATTESTATIONS";
            } else {
                aiSuggestion = null;
            }
        } finally {
            isAnalyzing = false;
        }
    }

    $effect(() => {
        const timeout = setTimeout(analyzeIntent, 300);
        return () => clearTimeout(timeout);
    });

    const commands = [
        {
            id: "protocol:harden",
            label: "Harden Manifold",
            desc: "Engage NIST AAL3 institutional defenses",
            icon: ShieldAlert,
            color: "text-rose-400",
        },
        {
            id: "protocol:soften",
            label: "Standard Baseline",
            desc: "Return to nominal operational state",
            icon: Globe,
            color: "text-emerald-400",
        },
        {
            id: "protocol:zkAttest",
            label: "zkEVM Attestation",
            desc: "Verify batch Proofs via multi-prover set",
            icon: Lock,
            color: "text-cyan-400",
        },
        {
            id: "protocol:stress",
            label: "Mesh Stress Test",
            desc: "Simulate high-load causal replication",
            icon: Activity,
            color: "text-purple-400",
        },
        {
            id: "manifold:sync",
            label: "Reconcile State",
            desc: "Force immediate manifold-wide sync",
            icon: Command,
            color: "text-white/60",
        },
        {
            id: "sim:citizen",
            label: "Forge Citizen",
            desc: "Manifest high-resonance synthetic identity",
            icon: Sparkles,
            color: "text-amber-400",
        },
    ];

    let filteredCommands = $derived(
        commands.filter((c) => {
            const search = query.toLowerCase();
            return (
                c.label.toLowerCase().includes(search) ||
                c.id.toLowerCase().includes(search)
            );
        }),
    );

    function toggle() {
        isOpen = !isOpen;
        if (isOpen) {
            query = "";
            selectedIndex = 0;
            setTimeout(
                () => document.getElementById("intent-input")?.focus(),
                50,
            );
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
            e.preventDefault();
            toggle();
        }

        if (!isOpen) return;

        if (e.key === "Escape") {
            isOpen = false;
        } else if (e.key === "ArrowDown") {
            e.preventDefault();
            selectedIndex =
                (selectedIndex + 1) % (filteredCommands.length || 1);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            selectedIndex =
                (selectedIndex - 1 + (filteredCommands.length || 1)) %
                (filteredCommands.length || 1);
        } else if (e.key === "Enter") {
            e.preventDefault();
            const cmd = filteredCommands[selectedIndex];
            if (cmd) execute(cmd.id);
        }
    }

    function execute(id: string) {
        onExecute(id);
        isOpen = false;
    }

    onMount(() => {
        window.addEventListener("keydown", handleKeydown);
        return () => window.removeEventListener("keydown", handleKeydown);
    });
</script>

{#if isOpen}
    <div
        class="intent-overlay"
        in:fade={{ duration: 150 }}
        onclick={toggle}
        onkeydown={(e: KeyboardEvent) => e.key === "Escape" && toggle()}
        role="button"
        tabindex="0"
    >
        <div
            class="intent-modal-container"
            onclick={(e: MouseEvent) => e.stopPropagation()}
            role="presentation"
        >
            <div class="intent-modal" in:fly={{ y: -10, duration: 400 }}>
                <!-- Header / Input -->
                <div class="intent-header">
                    <div class="intent-icon-shell">
                        {#if isAnalyzing}
                            <Brain
                                size={20}
                                class="text-purple-400 animate-pulse"
                            />
                        {:else}
                            <Search size={20} class="text-white/20" />
                        {/if}
                    </div>
                    <input
                        bind:value={query}
                        placeholder="State your intent... (e.g. 'harden protocol')"
                        id="intent-input"
                        autocomplete="off"
                        spellcheck="false"
                    />
                    <div class="shortcut-tag">⌘K</div>
                </div>

                <!-- AI Suggestion Layer -->
                {#if aiSuggestion}
                    <button
                        onclick={() => {
                            query = aiSuggestion!;
                            execute(
                                filteredCommands[0]?.id || "protocol:harden",
                            );
                        }}
                        class="suggestion-bar"
                        in:scale={{ start: 0.98, duration: 400 }}
                    >
                        <Zap size={12} class="text-amber-400" />
                        <span
                            class="text-[10px] font-black uppercase tracking-widest"
                            >{aiSuggestion}</span
                        >
                        <span
                            class="text-[8px] font-bold text-white/20 ml-auto italic"
                            >RESONANCE SUGGESTION</span
                        >
                    </button>
                {/if}

                <!-- Command List -->
                <div class="intent-results overflow-auto max-h-[480px]">
                    {#if filteredCommands.length > 0}
                        <div class="section-label">
                            Institutional_Directives
                        </div>
                        {#each filteredCommands as cmd, i}
                            <button
                                class="intent-item"
                                class:active={i === selectedIndex}
                                onmousemove={() => (selectedIndex = i)}
                                onclick={() => execute(cmd.id)}
                            >
                                <div
                                    class="icon-box"
                                    class:active={i === selectedIndex}
                                >
                                    <cmd.icon size={18} class={cmd.color} />
                                </div>
                                <div class="flex flex-col text-left">
                                    <span class="cmd-label">{cmd.label}</span>
                                    <span class="cmd-desc">{cmd.desc}</span>
                                </div>
                                {#if i === selectedIndex}
                                    <div class="enter-hint" in:fade>ENTER</div>
                                {/if}
                            </button>
                        {/each}
                    {:else}
                        <div
                            class="p-12 text-center text-white/10 uppercase font-black text-xs tracking-widest"
                        >
                            No matching intents found in manifest
                        </div>
                    {/if}
                </div>

                <!-- Footer -->
                <div class="intent-footer">
                    <span
                        class="text-[7px] font-black tracking-widest text-white/10 italic"
                        >SOVEREIGN_INTENT_ENGINE_v2.0</span
                    >
                    <div class="flex gap-4">
                        <div class="flex items-center gap-1">
                            <span class="key-pill">↑↓</span>
                            <span class="text-[8px] font-bold text-white/20"
                                >NAVIGATE</span
                            >
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="key-pill text-emerald-400">⏎</span>
                            <span class="text-[8px] font-bold text-white/20"
                                >EXECUTE</span
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .intent-overlay {
        position: fixed;
        inset: 0;
        background: rgba(2, 4, 8, 0.4);
        backdrop-filter: blur(20px);
        z-index: 10000;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        padding-top: 12vh;
        font-family: "Outfit", sans-serif;
    }

    .intent-modal-container {
        width: 100%;
        max-width: 600px;
        filter: drop-shadow(0 25px 50px rgba(0, 0, 0, 0.5));
    }

    .intent-modal {
        background: rgba(10, 15, 25, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        overflow: hidden;
        backdrop-filter: blur(40px);
    }

    .intent-header {
        display: flex;
        align-items: center;
        padding: 1.5rem;
        gap: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }

    .intent-icon-shell {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }

    input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 1.125rem;
        font-weight: 500;
        outline: none;
        letter-spacing: -0.01em;
    }

    input::placeholder {
        color: rgba(255, 255, 255, 0.15);
    }

    .shortcut-tag {
        font-size: 9px;
        font-weight: 900;
        padding: 4px 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        color: rgba(255, 255, 255, 0.2);
    }

    .suggestion-bar {
        display: flex;
        align-items: center;
        width: calc(100% - 2rem);
        margin: 0 1rem 1rem 1rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(
            90deg,
            rgba(168, 85, 247, 0.1),
            transparent
        );
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 12px;
        color: #e879f9;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .suggestion-bar:hover {
        background: linear-gradient(
            90deg,
            rgba(168, 85, 247, 0.15),
            rgba(168, 85, 247, 0.05)
        );
    }

    .intent-results {
        padding: 0.5rem;
    }

    .section-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        padding: 0.75rem 1rem;
    }

    .intent-item {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 1.25rem;
        padding: 1rem;
        border: none;
        background: transparent;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }

    .intent-item.active {
        background: rgba(255, 255, 255, 0.04);
        transform: scale(0.99);
    }

    .icon-box {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        transition: all 0.2s;
    }

    .icon-box.active {
        background: rgba(255, 255, 255, 0.05);
        transform: rotate(-5deg);
    }

    .cmd-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .cmd-desc {
        color: rgba(255, 255, 255, 0.3);
        font-size: 11px;
        font-weight: 500;
    }

    .enter-hint {
        margin-left: auto;
        font-size: 8px;
        font-weight: 900;
        color: #10b981;
        padding: 4px 8px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.05);
    }

    .intent-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.03);
    }

    .key-pill {
        font-size: 10px;
        font-weight: 900;
        opacity: 0.6;
    }
</style>
