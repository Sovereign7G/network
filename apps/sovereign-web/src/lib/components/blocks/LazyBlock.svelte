<script lang="ts">
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { Loader2 } from "lucide-svelte";

    let { importer, ...props } = $props<{
        importer: () => Promise<{ default: any }>;
        [key: string]: any;
    }>();

    let Component = $state<any>(null);
    let error = $state<string | null>(null);
    let loading = $state(true);

    onMount(async () => {
        try {
            const module = await importer();
            Component = module.default;
        } catch (e: any) {
            console.error("Failed to load lazy component", e);
            error = e.message || "Failed to load component";
        } finally {
            loading = false;
        }
    });
</script>

{#if loading}
    <div
        class="flex flex-col items-center justify-center p-12 min-h-[200px] bg-white/[0.02] border border-white/5 rounded-[2.5rem]"
        in:fade
    >
        <Loader2 class="text-white/20 animate-spin mb-4" size={24} />
        <span
            class="text-[10px] font-black uppercase tracking-widest text-white/10"
            >Assembling Module...</span
        >
    </div>
{:else if error}
    <div
        class="p-8 bg-red-500/10 border border-red-500/20 rounded-[2.5rem] text-center"
        in:fade
    >
        <p class="text-xs font-bold text-red-400">
            Structural integrity failure
        </p>
        <p class="text-[10px] text-red-400/60 mt-2 uppercase tracking-widest">
            {error}
        </p>
    </div>
{:else if Component}
    <div in:fade>
        <Component {...props} />
    </div>
{/if}
