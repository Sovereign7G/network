<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly } from "svelte/transition";
    import { Sparkles, Plus, Search, Layers } from "lucide-svelte";

    // 🎇 DISCOVERY PORTAL: Proactive exploration of the planetary mesh
    let query = $state("");
    let recommendations = $state([
        {
            id: "rec-1",
            title: "Adjoint Validator",
            resonance: 99,
            type: "audit",
        },
        {
            id: "rec-2",
            title: "Lunar Substrate",
            resonance: 94,
            type: "manifold",
        },
        { id: "rec-3", title: "Mesh Relay", resonance: 88, type: "trace" },
    ]);

    async function searchDiscover() {
        // In a real scenario, this calls manifold.searchSimilar
        manifold.recordEvent(
            "DISCOVERY_QUERY",
            `Searching for nodes similar to: ${query}`,
        );
    }
</script>

<div
    class="flex flex-col h-full bg-cyan-400/5 rounded-2xl p-4 border border-cyan-400/10 backdrop-blur-md"
>
    <div class="flex items-center gap-2 mb-4">
        <Sparkles size={14} class="text-cyan-400 animate-pulse" />
        <h3
            class="text-[10px] font-black uppercase tracking-widest text-cyan-400"
        >
            Discovery_Portal
        </h3>
    </div>

    <!-- Search Input -->
    <div class="relative mb-6">
        <Search
            size={12}
            class="absolute left-3 top-1/2 -translate-y-1/2 text-white/20"
        />
        <input
            type="text"
            bind:value={query}
            placeholder="Search Protocol Mesh..."
            class="w-full bg-black/40 border border-white/10 rounded-xl pl-9 pr-4 py-2 text-[10px] font-bold text-white placeholder:text-white/10 outline-none focus:border-cyan-400/40 transition-all"
            onkeydown={(e) => e.key === "Enter" && searchDiscover()}
        />
    </div>

    <!-- Recommendations -->
    <div class="flex-1 space-y-3 overflow-y-auto custom-scrollbar pr-1">
        <p
            class="text-[7px] font-black text-white/20 uppercase tracking-tighter mb-2"
        >
            Epoch_Suggestions // High_Resonance
        </p>

        {#each recommendations as rec}
            <div
                class="group bg-white/5 border border-white/5 rounded-xl p-3 flex items-center justify-between hover:bg-cyan-400/10 hover:border-cyan-400/30 transition-all cursor-pointer"
                transitionfly={{ x: -10 }}
            >
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-black/40 flex items-center justify-center text-white/40 group-hover:text-cyan-400 transition-colors"
                    >
                        <Layers size={14} />
                    </div>
                    <div>
                        <p
                            class="text-[9px] font-black text-white/80 group-hover:text-white transition-colors"
                        >
                            {rec.title}
                        </p>
                        <p
                            class="text-[7px] font-bold text-white/20 uppercase tracking-tighter"
                        >
                            Resonance: {rec.resonance}%
                        </p>
                    </div>
                </div>
                <button
                    class="w-6 h-6 rounded-lg bg-cyan-400/10 flex items-center justify-center text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-cyan-400 hover:text-black"
                >
                    <Plus size={12} />
                </button>
            </div>
        {/each}
    </div>

    <!-- Status Footer -->
    <div
        class="mt-4 pt-4 border-t border-white/5 flex items-center justify-between"
    >
        <div class="flex items-center gap-2">
            <div
                class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"
            ></div>
            <span class="text-[7px] font-black text-white/20 uppercase"
                >Mesh_Explorer_Active</span
            >
        </div>
        <span class="text-[7px] font-black text-cyan-400/40 italic"
            >A2UI_v2</span
        >
    </div>
</div>

<style>
    /* Custom scrollbar for discovery nodes */
</style>
