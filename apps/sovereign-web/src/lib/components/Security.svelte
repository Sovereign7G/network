<script lang="ts">
    import { authStore } from "../stores/auth.svelte";

//     import { ShieldCheck, Fingerprint, Lock, ArrowRight } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    let phase = $state("pin"); // 'pin' or 'biometrics'
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center bg-[#050505]"
    transition:fade
>
    <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-500/10 blur-[120px] rounded-full"
    ></div>

    <div class="relative w-full max-w-xl px-8">
        <div
            class="mb-4 text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase"
        >
            Security Parameters
        </div>
        <h1 class="mb-12 text-5xl font-black tracking-tighter text-white">
            Secure your Profile.
        </h1>

        {#if phase === "pin"}
            <div in:fly={{ x: 20, duration: 600 }}>
                <p class="mb-12 text-white/40 text-sm leading-relaxed max-w-sm">
                    Set a 6-digit Security Code for local access and transaction
                    signing on the Sovereign Mesh.
                </p>

                <div class="grid grid-cols-3 gap-4 max-w-xs mb-12">
                    {#each Array(9) as _, i}
                        <button
                            onclick={() => {}}
                            class="h-16 flex items-center justify-center rounded-xl bg-white/5 border border-white/5 text-xl font-bold text-white hover:bg-white/10 hover:border-white/10 transition-all"
                        >
                            {i + 1}
                        </button>
                    {/each}
                    <div class="h-16"></div>
                    <button
                        onclick={() => (phase = "biometrics")}
                        class="h-16 flex items-center justify-center rounded-xl bg-white/5 border border-white/5 text-xl font-bold text-white hover:bg-white/10 hover:border-white/10 transition-all"
                        >0</button
                    >
                    <button
                        onclick={() => (phase = "biometrics")}
                        class="h-16 flex items-center justify-center rounded-xl bg-white/5 text-white/20 flex items-center justify-center"
                        ><ArrowRight class="w-6 h-6" /></button
                    >
                </div>
            </div>
        {:else}
            <div in:fly={{ x: 20, duration: 600 }}>
                <p class="mb-12 text-white/40 text-sm leading-relaxed max-w-sm">
                    Enable biometric authentication for instant access across
                    all authorized planetary nodes.
                </p>

                <div class="flex flex-col gap-6">
                    <button
                        onclick={() => authStore.completeSecurity()}
                        class="group h-16 w-full flex items-center justify-between px-8 rounded-2xl bg-cyan-400/10 border border-cyan-400/30 text-cyan-400 font-bold hover:bg-cyan-400/20 transition-all"
                    >
                        <div class="flex items-center gap-4">
                            <Fingerprint class="w-6 h-6" />
                            <span>LINK BIOMETRICS</span>
                        </div>
                        <ArrowRight class="w-4 h-4" />
                    </button>

                    <button
                        onclick={() => authStore.completeSecurity()}
                        class="h-16 w-full flex items-center justify-center text-xs font-black tracking-widest text-white/20 hover:text-white/40 transition-colors"
                    >
                        SKIP FOR NOW
                    </button>
                </div>
            </div>
        {/if}
    </div>
</div>
