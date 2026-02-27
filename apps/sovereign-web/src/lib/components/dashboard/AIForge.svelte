<script lang="ts">
    import { agentService } from "$lib/services/agent-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { icpService } from "$lib/services/icp-service.svelte";
    import {
        Sparkles,
        Brain,
        AlertCircle,
        RefreshCw,
        MessageSquare,
    } from "lucide-svelte";

    let guidance = $state("");
    let sophia = agentService.sophia;
    let icp = icpService.state;

    async function synthesizeVision() {
        if (!guidance || !icp.isAuthenticated) return;
        try {
            const currentGuidance = guidance;
            guidance = "";
            await agentService.interact(currentGuidance);
            manifold.recordEvent(
                "VISION_SYNTHESIZED",
                `Sophia manifested a vision: ${currentGuidance.slice(0, 30)}`,
            );
        } catch (e) {
            console.error(e);
        }
    }

    const presets = [
        "Manifest a decentralized sovereign mesh strategy.",
        "Synthesize a roadmap for institutional resonance scaling.",
        "Forge a blueprint for autonomous shard recovery.",
    ];

    let scrollDiv = $state<HTMLDivElement | null>(null);
    $effect(() => {
        if (sophia.history.length && scrollDiv) {
            scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }
    });

    const clearHistory = () => {
        agentService.sophia.history = [];
    };
    function format(c: string) {
        return c.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    }
</script>

<div class="ai-forge-panel glass-panel h-full flex overflow-hidden">
    <!-- Sidebar -->
    <div
        class="w-48 border-r border-white/5 bg-black/20 flex flex-col hidden md:flex"
    >
        <div
            class="p-4 border-b border-white/5 flex items-center justify-between"
        >
            <span class="text-[8px] font-black uppercase text-white/40"
                >Chronicles</span
            >
            <button
                onclick={clearHistory}
                class="p-1 opacity-30 hover:opacity-100"
            >
                <RefreshCw size={10} />
            </button>
        </div>
        <div class="flex-1 overflow-y-auto p-2 space-y-1">

            {#each sophia.history.filter((m) => m.role === "user") as item}
                <button
                    onclick={() => (guidance = item.content)}
                    class="w-full text-left p-2 rounded hover:bg-white/5 truncate text-[8px] text-white/40"
                >
                    {item.content}
                </button>
            {/each}
        </div>
    </div>

    <!-- Main -->
    <div class="flex-1 flex flex-col p-6">
        <div class="flex items-center gap-3 mb-6">
            <div class="p-2 rounded bg-purple-500/20 text-purple-400">
                <Sparkles size={18} />
            </div>
            <div>
                <h3 class="text-[8px] font-black uppercase text-white/40 mb-1">
                    Pantheon Interface
                </h3>
                <h2 class="text-xl font-black text-white uppercase">
                    Sophia AI Forge
                </h2>
            </div>
        </div>

        <div
            bind:this={scrollDiv}
            class="flex-1 overflow-y-auto space-y-6 mb-6 pr-2"
        >
            {#if sophia.history.length === 0}
                <div
                    class="h-full flex flex-col items-center justify-center opacity-20 text-center px-8"
                >
                    <Brain size={48} class="mb-4 text-purple-500" />
                    <p class="text-[10px] font-black uppercase">
                        Awaiting Divine Direction
                    </p>
                </div>
            {/if}

            {#each sophia.history as msg (msg.id)}
                <div
                    class="flex flex-col gap-2 {msg.role === 'user'
                        ? 'items-end'
                        : 'items-start'}"
                >
                    <div class="max-w-[85%]">
                        <div
                            class="text-[6px] font-black uppercase text-white/20 mb-1"
                        >
                            {msg.role === "user" ? "Citizen" : "Sophia"} // {new Date(
                                msg.timestamp,
                            ).toLocaleTimeString()}
                        </div>
                        <div
                            class="p-4 rounded-2xl text-[11px] {msg.role ===
                            'user'
                                ? 'bg-white/5 text-white/80'
                                : 'bg-purple-500/5 text-purple-100'}"
                        >
                            {@html format(msg.content)}
                        </div>
                        {#if msg.payload && msg.payload.type === "STRATEGIC_ROADMAP"}
                            <div
                                class="mt-4 p-4 rounded-xl bg-black/40 border border-purple-500/30 text-[9px]"
                            >
                                <p
                                    class="font-black text-purple-300 uppercase mb-2"
                                >
                                    {msg.payload.data.title}
                                </p>
                                {#each msg.payload.data.steps as step}
                                    <div
                                        class="flex items-center gap-2 {step.status ===
                                        'active'
                                            ? 'text-white'
                                            : 'text-white/40'}"
                                    >
                                        <span
                                            >{step.status === "complete"
                                                ? "✓"
                                                : "○"}</span
                                        >
                                        <span>{step.label}</span>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}

            {#if sophia.lastStreamingDelta}
                <div class="flex flex-col gap-1 items-start">
                    <div
                        class="text-[6px] font-black uppercase text-purple-400 animate-pulse"
                    >
                        Sophia // Manifesting...
                    </div>
                    <div
                        class="max-w-[85%] p-3 rounded-2xl bg-purple-500/20 text-purple-300 text-[10px] italic"
                    >
                        {sophia.lastStreamingDelta}
                    </div>
                </div>
            {/if}
        </div>

        <!-- Input -->
        <div class="space-y-4">
            <div class="relative">
                <textarea
                    bind:value={guidance}
                    placeholder="DESCRIBE THE VISION..."
                    class="w-full h-24 bg-black/40 border border-white/10 rounded-2xl p-4 text-[10px] text-purple-300 focus:border-purple-500/50 outline-none resize-none"
                ></textarea>
                <button
                    onclick={synthesizeVision}
                    disabled={sophia.status !== "idle" ||
                        !guidance ||
                        !icp.isAuthenticated}
                    class="absolute bottom-4 right-4 p-2 bg-purple-600 rounded-lg text-white disabled:opacity-20 transition-all"
                >
                    <MessageSquare size={14} />
                </button>
            </div>
            <div class="flex flex-wrap gap-2">
                {#each presets as preset}
                    <button
                        onclick={() => (guidance = preset)}
                        class="px-2 py-1 bg-white/5 border border-white/10 rounded text-[7px] font-black uppercase text-white/40 hover:text-white/80 transition-all"
                    >
                        {preset.slice(0, 20)}...
                    </button>
                {/each}
            </div>
            {#if !icp.isAuthenticated}
                <div
                    class="flex gap-2 items-center justify-center p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl"
                >
                    <AlertCircle size={14} class="text-rose-400" />
                    <span class="text-[8px] text-rose-400 font-black uppercase"
                        >Identity Interface Required</span
                    >
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .ai-forge-panel {
        background: linear-gradient(
            135deg,
            rgba(147, 51, 234, 0.05) 0%,
            rgba(15, 23, 42, 0.4) 100%
        );
    }
    ::-webkit-scrollbar {
        width: 2px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(147, 51, 234, 0.2);
    }
</style>
