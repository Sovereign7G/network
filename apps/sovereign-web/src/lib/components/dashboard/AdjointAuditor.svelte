<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import { manifold } from "$lib/stores/master-store.svelte";

    let isAuditing = $derived(manifold.auditState.isAuditing);
    let results = $derived(manifold.auditState.lastResults);

    function triggerAudit() {
        manifold.runFullAudit();
    }
</script>

<div class="auditor-panel glass-panel p-6 space-y-4" in:fade>
    <div class="flex justify-between items-center mb-4">
        <h3
            class="text-xs font-black uppercase tracking-[0.2em] text-white/40 flex items-center gap-2"
        >
            <span
                class="w-2 h-2 rounded-full {isAuditing
                    ? 'bg-cyan-400 animate-pulse'
                    : 'bg-white/20'}"
            ></span>
            Adjoint Auditor // State Plane Verification
        </h3>
        {#if !isAuditing}
            <button
                onclick={triggerAudit}
                class="text-[10px] uppercase font-bold text-cyan-400 hover:text-white transition-colors"
            >
                RUN FULL AUDIT
            </button>
        {:else}
            <span class="text-[10px] uppercase font-black text-cyan-400/60"
                >AUDIT IN PROGRESS...</span
            >
        {/if}
    </div>

    {#if results.length === 0 && !isAuditing}
        <div
            class="py-8 flex flex-col items-center justify-center text-center space-y-3"
        >
            <div class="text-3xl opacity-20">🛡️</div>
            <p
                class="text-[10px] text-white/30 tracking-tight leading-relaxed max-w-[200px]"
            >
                No active audit record found. Initiate a scan to verify
                institutional integrity.
            </p>
        </div>
    {:else}
        <div class="space-y-3" in:slide>
            {#each results as result}
                <div
                    class="p-3 bg-white/5 border border-white/5 rounded-xl flex items-center justify-between group hover:bg-white/10 transition-all"
                >
                    <div class="space-y-1">
                        <div class="flex items-center gap-2">
                            <span
                                class="text-[8px] font-black uppercase tracking-tighter {result.status ===
                                'PASS'
                                    ? 'text-emerald-400'
                                    : 'text-amber-400'}"
                            >
                                {result.status}
                            </span>
                            <span class="text-[10px] mono-font text-white/80"
                                >{result.type}</span
                            >
                        </div>
                        <p class="text-[9px] text-white/40 leading-snug">
                            {result.msg}
                        </p>
                    </div>
                    <div
                        class="text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        {#if result.status === "PASS"}
                            <span class="text-emerald-400">✓</span>
                        {:else}
                            <span class="text-amber-400">!</span>
                        {/if}
                    </div>
                </div>
            {/each}

            {#if !isAuditing}
                <div
                    class="pt-4 border-t border-white/5 flex justify-between items-center"
                >
                    <span class="text-[9px] font-black uppercase text-white/20"
                        >Institutional Health Score</span
                    >
                    <span class="text-[11px] font-bold text-emerald-400"
                        >{manifold.auditState.health}%</span
                    >
                </div>
            {/if}
        </div>
    {/if}

    {#if isAuditing}
        <div
            class="p-4 bg-cyan-400/5 border border-dashed border-cyan-400/20 rounded-xl flex items-center justify-center gap-3"
            in:fade
        >
            <div
                class="w-3 h-3 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin"
            ></div>
            <span class="text-[9px] font-black uppercase text-cyan-400/60"
                >Executing fractal_lint.py --state-plane...</span
            >
        </div>
    {/if}
</div>

<style>
    .auditor-panel {
        background: rgba(10, 15, 20, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(34, 211, 238, 0.1);
        border-radius: 24px;
        transition: all 0.5s var(--ease-sovereign);
    }
</style>
