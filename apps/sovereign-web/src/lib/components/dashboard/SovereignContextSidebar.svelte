<script lang="ts">
    import { fade } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { Plus, Settings2, ShieldAlert } from "lucide-svelte";
    import Tooltip from "$lib/components/ui/Tooltip.svelte";

    interface Props {
        onContextChange: (columns: any[]) => void;
        currentColumns: any[];
    }

    let { onContextChange, currentColumns }: Props = $props();
    let hoveredAnchor = $state("");
    let tooltipText = $state("");

    function handleSwitch(id: string) {
        if (id === manifold.activeContextId) return;
        const nextColumns = manifold.switchContext(id, currentColumns);
        onContextChange(nextColumns);
    }

    function showTooltip(anchor: string, text: string) {
        hoveredAnchor = anchor;
        tooltipText = text;
    }

    function hideTooltip() {
        hoveredAnchor = "";
        tooltipText = "";
    }
</script>

<aside
    class="w-20 h-screen fixed left-0 top-0 flex flex-col items-center py-8 z-[60] border-r border-white/5 bg-black/20 backdrop-blur-3xl"
    in:fade
>
    <!-- Protocol Logo / Identity -->
    <div
        class="mb-12 relative group cursor-pointer"
        role="button"
        tabindex="0"
        style="anchor-name: --anchor-logo"
        onmouseenter={() => showTooltip("--anchor-logo", "Sovereign Core")}
        onmouseleave={hideTooltip}
        onkeydown={(e: KeyboardEvent) =>
            e.key === "Enter" && showTooltip("--anchor-logo", "Sovereign Core")}
    >
        <div
            class="w-12 h-12 rounded-2xl bg-white flex items-center justify-center shadow-[0_0_30px_rgba(255,255,255,0.2)] group-hover:scale-110 transition-all"
        >
            <span class="text-black font-black text-xl italic uppercase">A</span
            >
        </div>
    </div>

    <!-- Project Boxes (Contexts) -->
    <nav class="flex-1 flex flex-col gap-6 w-full items-center">
        {#each manifold.contexts as ctx}
            <button
                onclick={() => handleSwitch(ctx.id)}
                onmouseenter={() => showTooltip(`--anchor-${ctx.id}`, ctx.name)}
                onmouseleave={hideTooltip}
                style="anchor-name: --anchor-{ctx.id}"
                class="relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500
                       {manifold.activeContextId === ctx.id
                    ? 'bg-white/10 border-white/20 shadow-[0_0_20px_rgba(255,255,255,0.05)]'
                    : 'bg-transparent border border-white/5 hover:border-white/20'}"
            >
                <span
                    class="text-2xl filter group-hover:grayscale-0 transition-all {manifold.activeContextId ===
                    ctx.id
                        ? 'grayscale-0'
                        : 'grayscale opacity-40'}"
                >
                    {ctx.icon}
                </span>

                {#if ctx.badge}
                    <div
                        class="absolute -top-1 -right-1 flex items-center justify-center"
                    >
                        <div
                            class="w-3 h-3 bg-rose-500 rounded-full animate-ping absolute"
                        ></div>
                        <div
                            class="w-3 h-3 bg-rose-500 rounded-full border-2 border-black z-10"
                        ></div>
                    </div>
                {/if}

                <!-- Active Indicator -->
                <div
                    class="absolute -left-6 w-1 h-8 bg-white rounded-r-full transition-all duration-500
                            {manifold.activeContextId === ctx.id
                        ? 'opacity-100 scale-100'
                        : 'opacity-0 scale-50'}"
                ></div>
            </button>
        {/each}

        <button
            style="anchor-name: --anchor-instantiate"
            onmouseenter={() =>
                showTooltip("--anchor-instantiate", "Instantiate New Box")}
            onmouseleave={hideTooltip}
            class="w-12 h-12 rounded-2xl border border-dashed border-white/10 flex items-center justify-center text-white/20 hover:text-white hover:border-white/30 transition-all group"
        >
            <Plus size={20} />
        </button>
    </nav>

    <!-- Bottom Actions -->
    <div class="mt-auto flex flex-col gap-6 items-center">
        <button
            style="anchor-name: --anchor-settings"
            onmouseenter={() =>
                showTooltip("--anchor-settings", "Global Configuration")}
            onmouseleave={hideTooltip}
            class="text-white/20 hover:text-cyan-400 transition-colors relative group"
        >
            <Settings2 size={20} />
        </button>
        <button
            style="anchor-name: --anchor-hardstop"
            onmouseenter={() =>
                showTooltip("--anchor-hardstop", "Hard Stop Protocol")}
            onmouseleave={hideTooltip}
            class="w-10 h-10 rounded-xl bg-rose-950/20 border border-rose-500/20 flex items-center justify-center text-rose-500 hover:bg-rose-500 hover:text-white transition-all group"
        >
            <ShieldAlert size={18} />
        </button>
    </div>

    <!-- ⚓ THE ANCHORED MANIFOLD TIP -->
    <Tooltip
        visible={!!hoveredAnchor}
        text={tooltipText}
        anchorName={hoveredAnchor}
    />
</aside>
