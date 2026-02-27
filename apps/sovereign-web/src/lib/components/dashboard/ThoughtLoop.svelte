<script lang="ts">
    import { fade } from "svelte/transition";
    import { Search, ArrowRight, Sparkles, X, Quote } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { DAVINCI_QUOTES } from "../../registries/davinci-wisdom";
    import { onMount } from "svelte";

    interface Props {
        onExecute: (cmd: string) => void;
    }

    let { onExecute }: Props = $props();

    let query = $state("");
    let isFocused = $state(false);
    let quoteIndex = $state(0);
    const currentQuote = $derived(DAVINCI_QUOTES[quoteIndex]);

    onMount(() => {
        const interval = setInterval(() => {
            quoteIndex = (quoteIndex + 1) % DAVINCI_QUOTES.length;
        }, 8000);
        return () => clearInterval(interval);
    });

    const suggestions = $derived.by(() => {
        if (manifold.focusedBlockId) {
            return [
                "Fork this Module",
                "Generate Supply Chain",
                "Generate Financial Mesh",
                "Maximize Resonance",
                "Refine Metadata",
                "Adapt Legacy Protocol",
                "Bridge to Core DaVinci",
                "Optimize Block Logic",
                "Add Risk Heatmap",
                "Reveal Hidden Provenance",
                "Sync with Core ABI",
            ];
        }

        const activeCtx = manifold.contexts.find(
            (c) => c.id === manifold.activeContextId,
        );
        if (activeCtx?.id === "ctx-market") {
            return [
                "Audit Lunar Shipments",
                "Check Mars Demand",
                "Start Simulation",
                "Simulate Supply Breach",
            ];
        }
        if (activeCtx?.id === "ctx-social") {
            return [
                "Analyze Soul Trends",
                "Optimize Ad Vortex",
                "Check Influencer Payouts",
            ];
        }
        return ["Harden Protocols", "Run Fractal Audit", "Sync Sovereign Mesh"];
    });

    function handleSubmit(e?: Event) {
        e?.preventDefault();
        if (!query.trim()) return;

        // v0 Pattern: Map natural language to systemic commands
        let cmdId = "";
        const lowerQuery = query.toLowerCase();

        if (lowerQuery.includes("fork")) cmdId = "module:fork";
        else if (lowerQuery.includes("simulation")) cmdId = "simulation:start";
        else if (lowerQuery.includes("stop simulation"))
            cmdId = "simulation:stop";
        else if (lowerQuery.includes("audit")) cmdId = "protocol:audit";
        else if (lowerQuery.includes("generate supply chain"))
            cmdId = "epoch:generate:sc";
        else if (lowerQuery.includes("generate financial mesh"))
            cmdId = "epoch:generate:fm";
        else if (lowerQuery.includes("maximize resonance"))
            cmdId = "refine:resonance:100";
        else if (lowerQuery.includes("refine metadata"))
            cmdId = "refine:metadata:auto";
        else if (lowerQuery.includes("adapt legacy protocol"))
            cmdId = "protocol:adapt:legacy";
        else if (lowerQuery.includes("bridge to core"))
            cmdId = "bridge:context:ctx-core";
        else cmdId = lowerQuery.replace(/\s+/g, ":");

        onExecute(cmdId);
        query = "";
    }
</script>

<div
    class="thought-loop-container p-8 mt-12 mb-24 max-w-4xl mx-auto w-full"
    in:fade
>
    <div class="flex items-center gap-3 mb-6">
        <Sparkles size={16} class="text-cyan-400 animate-pulse" />
        <h3 class="text-xs font-black uppercase tracking-[0.3em] text-white/40">
            Sovereign Thought Loop // Next Iteration
        </h3>
        {#if manifold.focusedBlockId}
            <button
                onclick={() => manifold.setFocus(null)}
                class="flex items-center gap-2 px-2 py-1 bg-cyan-400/10 border border-cyan-400/20 rounded-md text-[8px] font-black text-cyan-400 hover:bg-cyan-400 hover:text-black transition-all"
            >
                <X size={8} />
                FOCUSED: 0x{manifold.focusedBlockId.slice(-6)}
            </button>
        {/if}
    </div>

    <form
        onsubmit={handleSubmit}
        class="relative group transition-all duration-500"
        class:is-focused={isFocused}
    >
        <div
            class="absolute inset-0 bg-white/5 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-all duration-700"
        ></div>

        <div
            class="relative bg-black/40 backdrop-blur-3xl border border-white/5 group-hover:border-white/20 rounded-2xl p-2 flex items-center gap-4 transition-all overflow-hidden h-16"
        >
            <div class="pl-4 text-white/20">
                <Search size={20} />
            </div>

            <input
                bind:value={query}
                onfocus={() => (isFocused = true)}
                onblur={() => (isFocused = false)}
                placeholder={manifold.focusedBlockId
                    ? `Iterate on focused module 0x${manifold.focusedBlockId.slice(-6)}...`
                    : "Iterate on the current canvas... (e.g., 'Audit Lunar Shipments')"}
                class="flex-1 bg-transparent border-none outline-none text-white font-medium placeholder:text-white/10"
            />

            <button
                type="submit"
                class="h-12 w-12 bg-white text-black rounded-xl flex items-center justify-center hover:bg-cyan-400 transition-all group/btn"
            >
                <ArrowRight
                    size={20}
                    class="group-hover/btn:translate-x-1 transition-transform"
                />
            </button>
        </div>
    </form>

    <div
        class="mt-4 px-4 flex items-start gap-3 opacity-40 hover:opacity-100 transition-opacity duration-500 min-h-[40px]"
    >
        <Quote size={12} class="text-cyan-400 mt-1 shrink-0" />
        {#key quoteIndex}
            <p
                class="text-[10px] leading-relaxed font-medium italic text-white/60 tracking-wide"
                in:fade={{ duration: 500 }}
            >
                "{currentQuote.text}"
            </p>
        {/key}
    </div>

    <div class="flex flex-wrap gap-2 mt-6">
        {#each suggestions as suggestion}
            <button
                onclick={() => {
                    query = suggestion;
                    handleSubmit();
                }}
                class="px-4 py-2 bg-white/5 border border-white/5 hover:border-white/10 rounded-lg text-[9px] font-black uppercase tracking-widest text-white/30 hover:text-white transition-all"
            >
                {suggestion}
            </button>
        {/each}
    </div>
</div>

<style>
    .thought-loop-container {
        position: relative;
    }

    .is-focused .relative {
        border-color: rgba(34, 211, 238, 0.4) !important;
        box-shadow: 0 0 40px rgba(34, 211, 238, 0.1);
    }
</style>
