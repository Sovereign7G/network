<script lang="ts">
    import { Languages, X } from "lucide-svelte";
    import { fade, scale } from "svelte/transition";

    interface Props {
        show: boolean;
        onClose: () => void;
    }

    let { show = $bindable(), onClose }: Props = $props();
</script>

{#if show}
    <div
        class="fixed inset-0 bg-black/40 backdrop-blur-md z-[55] flex items-center justify-center p-6"
        transition:fade
    >
        <div
            class="max-w-xl w-full glass-panel bg-black border border-white/10 p-10 space-y-8"
            in:scale={{ duration: 400, start: 0.9 }}
        >
            <div class="flex justify-between items-center">
                <div class="flex items-center gap-4">
                    <div
                        class="w-12 h-12 rounded-2xl bg-white text-black flex items-center justify-center"
                    >
                        <Languages size={24} />
                    </div>
                    <div>
                        <h3
                            class="text-xl font-black italic tracking-tighter uppercase"
                        >
                            ISOMORPHIC_HUB
                        </h3>
                        <p
                            class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                        >
                            Real-time Substrate Translation
                        </p>
                    </div>
                </div>
                <button
                    onclick={onClose}
                    class="p-2 text-white/20 hover:text-white transition-all"
                >
                    <X size={24} />
                </button>
            </div>

            <div class="grid grid-cols-2 gap-4">
                {#each ["EN_US", "ZH_CN", "JA_JP", "DE_DE", "FR_FR", "ES_ES"] as lang}
                    <button
                        class="px-6 py-4 bg-white/5 border border-white/5 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-neon-cyan hover:text-black transition-all"
                    >
                        {lang}
                    </button>
                {/each}
            </div>

            <div
                class="p-6 bg-neon-cyan/5 border border-neon-cyan/10 rounded-2xl space-y-2"
            >
                <p
                    class="text-[8px] font-black text-white/40 uppercase tracking-widest"
                >
                    Active_Node_Context
                </p>
                <p
                    class="text-[11px] font-bold text-neon-cyan uppercase tracking-tight"
                >
                    TRANSLATING TERTIARY SHARDS VIA CAUSAL INFERENCE...
                </p>
            </div>
        </div>
    </div>
{/if}

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
