<script lang="ts">
    import { naiEngine } from "./engine.svelte";
    import type { VisualOverlayComponent } from "./types";
    import { fade } from "svelte/transition";

    let overlays = $derived(
        naiEngine.getComponents<VisualOverlayComponent>("visual_overlay"),
    );
</script>

{#each overlays as ov}
    {#if ov.targetRegion}
        <div
            class="fixed z-[99] pointer-events-none transition-all duration-500"
            style="
                left: {ov.targetRegion.x}px; 
                top: {ov.targetRegion.y}px; 
                width: {ov.targetRegion.width}px; 
                height: {ov.targetRegion.height}px;
                border: 2px solid {ov.color};
                box-shadow: 0 0 20px {ov.color}33;
                border-radius: {ov.shape === 'circle' ? '50%' : '12px'};
            "
            transition:fade
        >
            {#if ov.shape === "pulse"}
                <div
                    class="absolute inset-0 animate-ping opacity-20"
                    style="background-color: {ov.color}"
                ></div>
            {/if}
        </div>
    {/if}
{/each}
