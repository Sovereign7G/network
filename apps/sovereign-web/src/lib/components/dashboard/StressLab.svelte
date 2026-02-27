<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly } from "svelte/transition";
    import { FlaskConical, ShieldAlert, Activity, Power } from "lucide-svelte";

    // 🧪 STRESS LAB: ChaosFuzz Control Panel
    const state = $derived(manifold.stressLabState);

    function toggleStress() {
        if (state.fuzzing) {
            manifold.stopStress();
        } else {
            manifold.chaosFuzzStress();
        }
    }
</script>

<div
    class="flex flex-col h-full bg-black/80 rounded-[2.5rem] border-2 border-white/10 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl relative"
>
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="p-3 bg-amber-500 text-black rounded-2xl shadow-[0_0_20px_rgba(245,158,11,0.3)]"
            >
                <FlaskConical size={20} />
            </div>
            <div>
                <h2
                    class="text-sm font-black uppercase tracking-tighter text-white"
                >
                    Stress_Lab
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="w-1.5 h-1.5 rounded-full {state.fuzzing
                            ? 'bg-amber-400 animate-ping'
                            : 'bg-white/20'}"
                    ></span>
                    <span
                        class="text-[8px] font-black text-amber-500/60 uppercase tracking-widest"
                        >ChaosFuzz // ABI_0x20</span
                    >
                </div>
            </div>
        </div>
        <button
            onclick={toggleStress}
            class="p-2 rounded-xl {state.fuzzing
                ? 'bg-rose-500 text-white'
                : 'bg-white/5 text-white/40'} hover:scale-105 transition-all"
        >
            <Power size={18} />
        </button>
    </div>

    <!-- Active Vectors -->
    <div class="flex-1 space-y-4">
        <p
            class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
        >
            Active_Stress_Vectors
        </p>
        <div class="grid grid-cols-1 gap-2">
            {#each state.activeVectors as vector}
                <div
                    class="px-4 py-3 bg-amber-500/10 border border-amber-500/20 rounded-xl flex items-center justify-between"
                    in:fly={{ y: 10 }}
                >
                    <span class="text-[9px] font-black text-amber-500 uppercase"
                        >{vector}</span
                    >
                    <Activity size={12} class="text-amber-500 animate-pulse" />
                </div>
            {:else}
                <div
                    class="h-24 flex items-center justify-center border border-dashed border-white/10 rounded-2xl"
                >
                    <span
                        class="text-[8px] font-black text-white/10 uppercase tracking-widest italic"
                        >Awaiting Stress Initiation</span
                    >
                </div>
            {/each}
        </div>
    </div>

    <!-- Strain HUD -->
    <div class="bg-black/40 p-5 rounded-3xl border border-white/5 space-y-4">
        <div>
            <div class="flex justify-between items-center mb-1">
                <span class="text-[7px] font-black text-white/20 uppercase"
                    >Manifold_Strain</span
                >
                <span
                    class="text-[10px] font-black {state.manifoldStrain > 70
                        ? 'text-rose-500'
                        : 'text-amber-500'}"
                    >{state.manifoldStrain.toFixed(1)}%</span
                >
            </div>
            <div class="h-1 bg-white/5 rounded-full overflow-hidden">
                <div
                    class="h-full {state.manifoldStrain > 70
                        ? 'bg-rose-500'
                        : 'bg-amber-500'} transition-all duration-300"
                    style:width="{state.manifoldStrain}%"
                ></div>
            </div>
        </div>

        {#if state.lastPanic}
            <div
                class="flex items-center gap-2 text-[8px] font-black text-rose-500 uppercase italic animate-pulse"
            >
                <ShieldAlert size={12} />
                <span
                    >Last Panic: {new Date(
                        state.lastPanic,
                    ).toLocaleTimeString()}</span
                >
            </div>
        {/if}
    </div>

    <div
        class="text-[7px] font-black text-white/20 uppercase text-center border-t border-white/5 pt-4 tracking-widest"
    >
        Invariant Protection: REINFORCED
    </div>
</div>
