<script lang="ts">
    import { Zap, ChevronDown } from "lucide-svelte";
    import { slide } from "svelte/transition";

    let showDiscoveryTray = $state(false);
</script>

<div class="flex justify-center -mt-4 mb-4">
    <button
        onclick={() => (showDiscoveryTray = !showDiscoveryTray)}
        class="px-8 py-1.5 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition-all group"
    >
        <ChevronDown
            size={14}
            class="text-white/20 group-hover:text-neon-cyan transition-colors {showDiscoveryTray
                ? 'rotate-180'
                : ''}"
        />
    </button>
</div>

{#if showDiscoveryTray}
    <div
        class="bg-white/[0.02] border border-white/5 rounded-[2rem] p-8 mb-8"
        transition:slide
    >
        <h4
            class="text-[10px] font-black uppercase tracking-[0.3em] mb-6 text-white/40"
        >
            Recently_Anchored_Mini_Programs
        </h4>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            {#each Array(4) as _, i}
                <button
                    class="p-6 bg-black/40 border border-white/5 rounded-2xl flex items-center gap-4 hover:border-neon-cyan/40 transition-all"
                >
                    <div
                        class="w-10 h-10 rounded-xl bg-neon-cyan/10 flex items-center justify-center text-neon-cyan"
                    >
                        <Zap size={18} />
                    </div>
                    <div class="text-left">
                        <p class="text-[9px] font-black uppercase">
                            EPHEMERAL_SHARD_{i + 1}
                        </p>
                        <p
                            class="text-[7px] text-white/20 uppercase tracking-widest"
                        >
                            ZERO_INSTALL_UTILITY
                        </p>
                    </div>
                </button>
            {/each}
        </div>
    </div>
{/if}
