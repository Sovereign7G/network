<script lang="ts" module>
    export interface FormContext {
        id: string;
        name: string;
        error?: string;
        description?: string;
    }
</script>

<script lang="ts">
    import { fly, fade } from "svelte/transition";
    import type { Snippet } from "svelte";

    interface Props {
        name: string;
        label?: string | undefined;
        description?: string | undefined;
        error?: string | undefined;
        children: Snippet;
    }

    let { name, label, description, error, children }: Props = $props();
    const id = $derived(
        `form-field-${name}-${Math.random().toString(36).slice(2, 9)}`,
    );
</script>

<div class="form-item space-y-2 mb-6 group">
    {#if label}
        <label
            for={id}
            class="block text-[10px] font-black uppercase tracking-[0.2em] text-white/40 group-hover:text-cyan-400 transition-colors"
        >
            {label}
        </label>
    {/if}

    <div class="form-control relative transition-all duration-300">
        {@render children()}

        {#if error}
            <div
                class="absolute right-3 top-1/2 -translate-y-1/2 text-[8px] font-black text-rose-500 uppercase tracking-widest bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20"
                in:fly={{ x: 10, duration: 200 }}
            >
                {error}
            </div>
        {/if}
    </div>

    {#if description && !error}
        <p
            class="text-[9px] font-medium text-white/20 italic leading-relaxed group-hover:text-white/40 transition-colors"
            in:fade
        >
            {description}
        </p>
    {/if}

    {#if error}
        <p
            class="text-[9px] font-black text-rose-500/80 uppercase tracking-tighter"
            in:fade
        >
            Validation Error // Systemic Integrity Compromised
        </p>
    {/if}
</div>

<style>
    .form-item {
        position: relative;
    }

    :global(.form-control input),
    :global(.form-control textarea),
    :global(.form-control select) {
        width: 100%;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: white;
        font-family: inherit;
        font-size: 13px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        outline: none;
    }

    :global(.form-control input:hover),
    :global(.form-control textarea:hover) {
        border-color: rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.05);
    }

    :global(.form-control input:focus),
    :global(.form-control textarea:focus) {
        border-color: rgba(34, 211, 238, 0.4);
        background: rgba(34, 211, 238, 0.02);
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.05);
    }

    :global(.form-control input[aria-invalid="true"]) {
        border-color: rgba(244, 63, 94, 0.4);
        background: rgba(244, 63, 94, 0.02);
    }
</style>
