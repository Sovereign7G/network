<script lang="ts">
    import { onMount } from "svelte";
    import { fade, blur } from "svelte/transition";

    export let targetId: string;
    export let text: string;
    export let type: "logical" | "strategic" | "tactical" = "logical";

    let visible = false;
    let targetRect: DOMRect | null = null;

    onMount(() => {
        const el = document.getElementById(targetId);
        if (el) {
            targetRect = el.getBoundingClientRect();
            // Offset logic for institutional alignment
            visible = true;
        }
    });

    const colors = {
        logical: "text-cyan-400 border-cyan-400/20 bg-cyan-400/5",
        strategic: "text-amber-400 border-amber-400/20 bg-amber-400/5",
        tactical: "text-emerald-400 border-emerald-400/20 bg-emerald-400/5",
    };
</script>

{#if visible && targetRect}
    <div
        class="fixed z-[1000] pointer-events-none"
        style="
            left: {targetRect.left}px;
            top: {targetRect.bottom + 8}px;
            width: {targetRect.width}px;
        "
        transition:blur={{ duration: 400 }}
    >
        <!-- Annotation Stem -->
        <div
            class="w-px h-8 bg-gradient-to-b from-white/20 to-transparent mx-auto"
        ></div>

        <!-- Annotation Box -->
        <div
            class="px-3 py-2 border rounded-sm {colors[type]} backdrop-blur-md"
        >
            <div class="flex items-center gap-2 mb-1">
                <div
                    class="w-1.5 h-1.5 rounded-full bg-current animate-pulse"
                ></div>
                <span
                    class="text-[8px] font-black uppercase tracking-widest opacity-60"
                    >System_Annotation</span
                >
            </div>
            <p
                class="text-[10px] font-bold leading-tight uppercase italic tracking-tighter"
            >
                // {text}
            </p>
        </div>
    </div>
{/if}
