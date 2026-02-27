<script lang="ts">
    import { fade } from "svelte/transition";
    import { AlertTriangle, RefreshCw } from "lucide-svelte";

    let { children, moduleName = "Unknown_Module" } = $props<{
        children: any;
        moduleName?: string;
    }>();

    let error = $state<any>(null);
</script>

{#if error}
    <div
        class="module-error-fallback p-8 bg-red-500/5 border border-red-500/20 rounded-[2.5rem] flex flex-col items-center justify-center text-center min-h-[200px]"
        in:fade
    >
        <div class="p-4 bg-red-500/10 rounded-full mb-4">
            <AlertTriangle class="text-red-500" size={32} />
        </div>
        <h3
            class="text-sm font-black text-red-500 uppercase tracking-widest mb-2"
        >
            {moduleName}_FAILURE
        </h3>
        <p
            class="text-[10px] text-red-400/60 uppercase tracking-tighter mb-6 max-w-[200px]"
        >
            {error.message ||
                "Unknown structural integrity violation detected in module runtime."}
        </p>
        <button
            onclick={() => (error = null)}
            class="px-6 py-2 bg-red-500 text-white text-[10px] font-black uppercase tracking-widest rounded-full hover:bg-red-400 transition-all flex items-center gap-2"
        >
            <RefreshCw size={12} />
            Reinitialize_Module
        </button>
    </div>
{:else}
    <div class="relative h-full">
        {@render children()}
    </div>
{/if}
