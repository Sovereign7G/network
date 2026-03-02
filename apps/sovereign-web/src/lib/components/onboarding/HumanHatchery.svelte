<script lang="ts">
    // @ts-nocheck
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
    import { elasticOut } from "svelte/easing";
    import LaborOrb from "./LaborOrb.svelte";
    import LogicSandbox from "./LogicSandbox.svelte";
    import BurnAltar from "./BurnAltar.svelte";
    import { passkeyService } from "../../services/passkey.svelte";
    import { onboardingStore } from "../../stores/onboarding-store.svelte";

    // Ritual State
    let currentGate = $state(1); // 1: Labor, 2: Logic, 3: Sacrifice, 4: Born
    let laborProgress = $state(0);
    let logicVerified = $state(false);
    let sacrificeConfirmed = $state(false);
    let cpuIntensity = $state(0); // Simulated CPU load for VDF
    let isSoulBinding = $state(false); // New: Passkey Phase

    /**
     * Anchor the crystallized labor to a human biometric touch.
     * Completes the 'Human-to-Node' link.
     */
    async function performSoulBinding() {
        if (laborProgress < 100) return;

        isSoulBinding = true;
        const result = await passkeyService.anchorIdentity(
            "Guardian-Alpha-" + Math.floor(Math.random() * 999),
            "0xVDF-PROOF-" + Date.now(),
        );

        if (result) {
            console.log("🧬 [HATCHERY] Soul-Binding Successful:", result.id);
            currentGate = 2;
        } else {
            console.error("❌ [HATCHERY] Soul-Binding Rejected.");
        }
        isSoulBinding = false;
    }

    // VDF Simulation
    function startLabor() {
        cpuIntensity = 0.85;
        const interval = setInterval(() => {
            if (laborProgress < 100) {
                laborProgress += 1.0; // Faster for UX
            } else {
                clearInterval(interval);
                cpuIntensity = 0.1;
                // Move to Soul Binding instead of auto-transitioning to Gate 2
            }
        }, 50);
    }

    // Final Burn
    function confirmSacrifice() {
        sacrificeConfirmed = true;

        // Finalize state transition with First Breath telemetry
        setTimeout(() => {
            currentGate = 4;

            // 📡 THE FIRST BREATH TELEMETRY
            manifold.recordEvent(
                "GENESIS_EVENT",
                "First Citizen ALPHA-001 has entered the manifold.",
            );

            // 1. Connectivity: First autonomous eSIM Data-Zap
            setTimeout(() => {
                manifold.recordEvent(
                    "ESIM_PROVISIONED",
                    "Autonomous Aether-Zap fired. Local data profile active. Latency: 12ms.",
                );
            }, 500);

            // 2. Silbo: Broadcast arrival to the shard
            setTimeout(() => {
                manifold.recordEvent(
                    "SILBO_BROADCAST",
                    "MESSAGE: 'Guardian 001 has Anchored.' Routing via P2P Mesh.",
                );
            }, 1000);

            // 3. Agora: Inscribe Talent Profile
            setTimeout(() => {
                manifold.recordEvent(
                    "AGORA_PROFILE_ACTIVE",
                    "Citizen ALPHA-001 listed in Talent Nexus. Base Merit: 1.00 M.",
                );
                onboardingStore.completeOnboarding();
            }, 1500);
        }, 2000);
    }

    onMount(() => {
        // Initialization ritual
    });
</script>

<div
    class="hatchery-portal fixed inset-0 z-[100] bg-[#030303] text-white flex flex-col items-center justify-center p-8 overflow-hidden"
>
    <!-- Atmospheric Background -->
    <div class="absolute inset-0 z-0 pointer-events-none">
        <div
            class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[120px] animate-pulse"
        ></div>
        <div
            class="absolute bottom-0 w-full h-px bg-gradient-to-r from-transparent via-amber-500/20 to-transparent"
        ></div>
    </div>

    {#if currentGate < 4}
        <header class="relative z-10 text-center mb-16" in:fade>
            <h1 class="text-4xl font-black tracking-tighter text-premium">
                RITUAL OF <span class="text-amber-500 italic">ALIGNMENT</span>
            </h1>
            <p
                class="text-[10px] uppercase tracking-[0.5em] text-white/30 mt-4"
            >
                PARAGON SHARD - GENESIS COHORT v21.2
            </p>
        </header>

        <!-- Progress Track -->
        <div class="relative z-10 w-full max-w-2xl mb-24">
            <div class="flex justify-between items-center mb-4">
                {#each [1, 2, 3] as gate}
                    <div class="flex flex-col items-center gap-2">
                        <div
                            class="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold transition-all duration-500 {currentGate >=
                            gate
                                ? 'bg-amber-500 text-black shadow-[0_0_15px_rgba(245,158,11,0.4)]'
                                : 'bg-white/5 text-white/20 border border-white/10'}"
                        >
                            {gate}
                        </div>
                        <span
                            class="text-[8px] uppercase tracking-widest {currentGate ===
                            gate
                                ? 'text-amber-500'
                                : 'text-white/20'}"
                        >
                            {gate === 1
                                ? "Labor"
                                : gate === 2
                                  ? "Logic"
                                  : "Sacrifice"}
                        </span>
                    </div>
                {/each}
            </div>
            <div class="h-0.5 bg-white/5 rounded-full overflow-hidden">
                <div
                    class="h-full bg-amber-500 transition-all duration-500"
                    style:width="{(currentGate - 1) * 50}%"
                ></div>
            </div>
        </div>

        <main class="relative z-10 w-full max-w-4xl grid grid-cols-1 gap-12">
            {#if currentGate === 1}
                <section
                    class="gate-container p-12 glass-panel rounded-[40px] text-center"
                    in:fly={{ y: 20, duration: 800 }}
                >
                    <div class="mb-8 p-12">
                        <LaborOrb
                            progress={laborProgress}
                            intensity={cpuIntensity}
                        />
                    </div>

                    <h2 class="text-2xl font-bold mb-4">The Gate of Labor</h2>
                    <p class="text-sm text-white/50 mb-12 max-w-md mx-auto">
                        In the AGE Protocol, citizenship requires physical work.
                        Prove your infrastructure's integrity by computing the
                        2,160,000 VDF iterations.
                    </p>

                    {#if laborProgress === 0}
                        <button
                            onclick={startLabor}
                            class="px-12 py-4 bg-white text-black text-xs font-black uppercase tracking-[0.3em] rounded-full hover:bg-amber-500 transition-all active:scale-95 shadow-xl"
                        >
                            Initiate VDF Computation
                        </button>
                    {:else if laborProgress < 100}
                        <div
                            class="flex items-center justify-center gap-6 mt-8 font-mono text-[10px] text-amber-500/60 uppercase tracking-widest"
                        >
                            <span class="animate-pulse"
                                >CPU_LOAD: {(cpuIntensity * 100).toFixed(
                                    0,
                                )}%</span
                            >
                            <span>•</span>
                            <span class="animate-pulse"
                                >SHARD_GROWTH_ACTIVE</span
                            >
                        </div>
                    {:else}
                        <button
                            onclick={performSoulBinding}
                            disabled={isSoulBinding}
                            class="px-12 py-5 bg-amber-500 text-black text-xs font-black uppercase tracking-[0.3em] rounded-full hover:scale-110 hover:shadow-[0_0_50px_rgba(245,158,11,0.5)] transition-all active:scale-95 shadow-xl flex items-center gap-4 mx-auto"
                        >
                            {#if isSoulBinding}
                                <div
                                    class="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin"
                                ></div>
                                ANCHORING...
                            {:else}
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="3"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="lucide lucide-fingerprint"
                                    ><path
                                        d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.02-.26 3"
                                    /><path
                                        d="M2.7 13.5a10.8 10.8 0 0 1 1.3-6.1C5.1 4.9 8 3 12 3s6.9 1.9 8 4.4a10.8 10.8 0 0 1 1.3 6.1"
                                    /><path
                                        d="M16 18c0-1.1-1-2.2-2.2-2.2a2.1 2.1 0 0 0-1.07.3L11 17l-1.3-1.3a2.1 2.1 0 0 0-3-.3C5.7 16.3 5 17.5 5 18.8c0 1.4.6 2.7 1.5 3.6"
                                    /><path
                                        d="M11 11.5c0-.8.7-1.5 1.5-1.5s1.5.7 1.5 1.5V13c0 .8-.7 1.5-1.5 1.5s-1.5-.7-1.5-1.5"
                                    /><path
                                        d="M11 5.3c-.6 0-1.2.2-1.7.5"
                                    /><path
                                        d="M19 13.2a11.5 11.5 0 0 1-.3 2.1"
                                    /><path
                                        d="M9.1 12.3c-.6 0-1.2.2-1.7.6"
                                    /><path
                                        d="M14.7 5.7a4 4 0 0 1 1.6.8"
                                    /></svg
                                >
                                ANCHOR HUMAN IDENTITY
                            {/if}
                        </button>
                    {/if}
                </section>
            {:else if currentGate === 2}
                <section
                    class="gate-container p-12 glass-panel rounded-[40px] text-center"
                    in:fly={{ y: 20, duration: 800 }}
                >
                    <h2 class="text-2xl font-bold mb-4">The Gate of Logic</h2>
                    <p class="text-sm text-white/50 mb-12 max-w-md mx-auto">
                        Complete the Merit-Decay circuit to prove your
                        comprehension of the Liquid Influence manifold.
                    </p>

                    <div class="mb-8 w-full">
                        <LogicSandbox
                            onsuccess={() => {
                                logicVerified = true;
                                setTimeout(() => (currentGate = 3), 1500);
                            }}
                        />
                    </div>
                </section>
            {:else if currentGate === 3}
                <section
                    class="gate-container p-12 glass-panel rounded-[40px] text-center"
                    in:fly={{ y: 20, duration: 800 }}
                >
                    <h2 class="text-2xl font-bold mb-4">
                        The Gate of Sacrifice
                    </h2>
                    <p class="text-sm text-white/50 mb-12 max-w-md mx-auto">
                        Finalize your commitment. The 10,000 $AGE Crow-Burn is
                        permanent and irrevocable.
                    </p>

                    <BurnAltar onsuccess={confirmSacrifice} />
                </section>
            {/if}
        </main>
    {:else}
        <!-- BORN -->
        <div
            class="text-center"
            in:scale={{ duration: 2000, start: 0.8, easing: elasticOut }}
        >
            <h1 class="text-8xl font-black tracking-tighter text-premium mb-8">
                BORN TO <span class="text-amber-500">PARAGON</span>
            </h1>
            <div
                class="text-[10px] uppercase tracking-[0.5em] text-white/40 mb-12"
            >
                Guardian S-ID: ALPHA-{Math.floor(Math.random() * 1000)
                    .toString()
                    .padStart(3, "0")}
            </div>

            <button
                onclick={() => onboardingStore.nextStep()}
                class="px-16 py-4 bg-white text-black text-xs font-black uppercase tracking-[0.4em] rounded-full hover:bg-amber-500 transition-all shadow-xl"
            >
                Enter the Mesh
            </button>
        </div>
    {/if}
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.5);
    }

    .text-premium {
        background: linear-gradient(
            to bottom,
            #fff 0%,
            rgba(255, 255, 255, 0.4) 100%
        );
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .gate-container {
        animation: portal-float 6s ease-in-out infinite;
    }

    @keyframes portal-float {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
</style>
