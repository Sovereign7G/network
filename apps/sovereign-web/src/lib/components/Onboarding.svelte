<script lang="ts">
    import { authStore } from "../stores/auth.svelte";
    import {
        Shield,
        Zap,

        Globe,
        ArrowRight,
        Fingerprint,
        Lock,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    let phase = $state("choice"); // 'choice', 'intro', 'security', 'import'
    let step = $state(0);

    const steps = [
        {
            title: "WELCOME TO AGE",
            subtitle: "The Sovereign Protocol for a New Economic Era.",
            desc: "Take full control of your digital identity and capital in a decentralized planetary network.",
            icon: Zap,
        },
        {
            title: "SYSTEM PRECISION",
            subtitle: "Premium Architecture for Institutional Trust.",
            desc: "Your assets are protected by zero-knowledge proofs and professional-grade security protocols.",
            icon: Shield,
        },
    ];

    const seedWords = [
        "chaos",
        "ritual",
        "axiom",
        "mesh",
        "pixel",
        "logic",
        "draco",
        "void",
        "cyan",
        "aurora",
        "plasma",
        "solar",
    ];

    function next() {
        if (phase === "intro") {
            if (step < steps.length - 1) {
                step++;
            } else {
                phase = "security";
            }
        } else if (phase === "security") {
            authStore.completeOnboarding();
        }
    }

    function startNew() {
        phase = "intro";
        step = 0;
    }

    function startImport() {
        phase = "import";
    }
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center bg-[#050505] overflow-hidden"
    transition:fade
>
    <!-- Background Effects -->
    <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-500/5 blur-[120px] rounded-full animate-pulse"
    ></div>
    <div
        class="absolute bottom-0 right-0 w-[400px] h-[400px] bg-amber-500/5 blur-[120px] rounded-full"
    ></div>

    <div class="relative w-full max-w-2xl px-8">
        {#if phase === "choice"}
            <div in:fly={{ y: 20, duration: 600 }} class="text-center">
                <div
                    class="mx-auto w-20 h-20 mb-12 flex items-center justify-center rounded-full border border-cyan-400/50 bg-cyan-400/10 shadow-[0_0_20px_rgba(0,242,255,0.2)]"
                >
                    <Fingerprint class="w-10 h-10 text-cyan-400" />
                </div>
                <div
                    class="text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
                >
                    Protocol Entry
                </div>
                <h1
                    class="text-5xl font-black tracking-tighter text-white mb-6 italic uppercase"
                >
                    Sovereign <span class="text-cyan-400">Initialize</span>
                </h1>
                <p class="text-white/50 mb-12 max-w-md mx-auto leading-relaxed">
                    Securely initialize a new Citizen ID or import your existing
                    sovereign identity from the mesh.
                </p>

                <div class="flex flex-col gap-4">
                    <button
                        onclick={startNew}
                        class="h-16 w-full rounded-2xl bg-cyan-400 text-black font-black italic tracking-widest text-sm hover:scale-[1.02] transition-transform"
                    >
                        INITIALIZE NEW IDENTITY
                    </button>
                    <button
                        onclick={startImport}
                        class="h-16 w-full rounded-2xl border border-white/10 bg-white/5 text-white font-black italic tracking-widest text-sm hover:bg-white/10 transition-all"
                    >
                        IMPORT FROM MESH
                    </button>
                </div>
            </div>
        {:else if phase === "intro"}
            {@const Icon = steps[step].icon}
            <div in:fly={{ y: 20, duration: 600 }} class="text-center">
                <div
                    class="mx-auto w-24 h-24 mb-12 flex items-center justify-center rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl"
                >
                    <Icon class="w-10 h-10 text-cyan-400" />
                </div>
                <div
                    class="text-[10px] font-black tracking-[0.4em] text-white/40 uppercase mb-4"
                >
                    {steps[step].title}
                </div>
                <h2
                    class="text-4xl font-black tracking-tighter text-white mb-6 leading-tight italic uppercase"
                >
                    {steps[step].subtitle}
                </h2>
                <p
                    class="text-lg text-white/50 mb-12 max-w-lg mx-auto leading-relaxed"
                >
                    {steps[step].desc}
                </p>

                <div class="flex flex-col items-center gap-8">
                    <div class="flex gap-2">
                        {#each steps as _, i}
                            <div
                                class="h-1 rounded-full transition-all duration-500 {step ===
                                i
                                    ? 'w-8 bg-cyan-400'
                                    : 'w-2 bg-white/10'}"
                            ></div>
                        {/each}
                    </div>
                    <button
                        onclick={next}
                        class="h-16 w-full rounded-2xl border border-cyan-400/30 bg-white/5 text-white font-black italic tracking-widest text-sm hover:bg-white/10 transition-all flex items-center justify-center gap-2"
                    >
                        CONTINUE <ArrowRight class="w-4 h-4" />
                    </button>
                </div>
            </div>
        {:else if phase === "security"}
            <div in:fly={{ y: 20, duration: 600 }} class="text-center">
                <div
                    class="mx-auto w-20 h-20 mb-12 flex items-center justify-center rounded-full border border-aurora-green/50 bg-aurora-green/10"
                >
                    <Lock class="w-10 h-10 text-aurora-green" />
                </div>
                <div
                    class="text-[10px] font-black tracking-[0.4em] text-aurora-green uppercase mb-4"
                >
                    Secure Your Identity
                </div>
                <h1
                    class="text-4xl font-black tracking-tighter text-white mb-8 italic uppercase"
                >
                    Recovery <span class="text-aurora-green">Seed</span>
                </h1>

                <div
                    class="grid grid-cols-3 gap-3 mb-12 p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md"
                >
                    {#each seedWords as word}
                        <div
                            class="py-2 px-3 rounded-lg bg-white/5 text-white/70 font-mono text-sm border border-white/5"
                        >
                            {word}
                        </div>
                    {/each}
                </div>

                <p class="text-sm text-white/30 mb-12">
                    Write this seed down. It is the only way to recover your
                    Citizen ID if your device is compromised.
                </p>

                <button
                    onclick={next}
                    class="h-16 w-full rounded-2xl bg-aurora-green text-black font-black italic tracking-widest text-sm hover:scale-[1.02] transition-all"
                >
                    I HAVE SECURED MY SEED
                </button>
            </div>
        {:else if phase === "import"}
            <div in:fly={{ y: 20, duration: 600 }} class="text-center">
                <div
                    class="text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
                >
                    Import Identity
                </div>
                <h1
                    class="text-4xl font-black tracking-tighter text-white mb-8 italic uppercase"
                >
                    Enter <span class="text-cyan-400">Seed</span>
                </h1>

                <textarea
                    placeholder="word1 word2 word3..."
                    class="w-full h-40 p-6 rounded-2xl bg-white/5 border border-white/10 text-white font-mono mb-12 focus:border-cyan-400/50 transition-all outline-none resize-none"
                ></textarea>

                <div class="flex flex-col gap-4">
                    <button
                        onclick={() => authStore.completeOnboarding()}
                        class="h-16 w-full rounded-2xl bg-cyan-400 text-black font-black italic tracking-widest text-sm"
                    >
                        INITIALIZE IMPORT
                    </button>
                    <button
                        onclick={() => (phase = "choice")}
                        class="text-white/30 text-[10px] font-black tracking-widest uppercase hover:text-white transition-colors"
                    >
                        CANCEL
                    </button>
                </div>
            </div>
        {/if}
    </div>
</div>
