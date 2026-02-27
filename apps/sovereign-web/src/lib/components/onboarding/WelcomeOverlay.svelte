<script lang="ts">
//     import { fade, fly } from "svelte/transition";
    import { backOut } from "svelte/easing";
    import { Fingerprint, Wallet, Vote, ChevronRight } from "lucide-svelte";
    import { sovereignStore } from "$lib/stores/sovereign-store.svelte";

    // Show if the user hasn't completed their first visit and has no active ID
    let showWelcome = $derived(
        !sovereignStore.state.onboarding.firstVisit && !sovereignStore.state.id,

    );
    let closing = $state(false);

    function startJourney() {
        closing = true;
        setTimeout(() => {
            sovereignStore.markEventComplete("firstVisit");
            // Mock identity creation prompt or let the interface guide them
            sovereignStore.initialize({
                id: `did:v1:${Math.random().toString(36).substring(2, 10)}`,
            });
        }, 400);
    }

    function exploreAsGuest() {
        closing = true;
        setTimeout(() => {
            sovereignStore.markEventComplete("firstVisit");
        }, 400);
    }
</script>

{#if showWelcome && !closing}
    <div
        class="fixed inset-0 z-[200] flex items-center justify-center p-6 bg-black/80 backdrop-blur-md"
        transitionfade={{ duration: 400 }}
    >
        <!-- Atmospheric Background Glow -->
        <div
            class="absolute inset-0 pointer-events-none overflow-hidden flex items-center justify-center opacity-30"
        >
            <div
                class="w-[80vw] h-[80vw] max-w-[800px] max-h-[800px] bg-amber-500/20 rounded-full blur-[120px]"
            ></div>
        </div>

        <div
            class="max-w-2xl w-full welcome-panel relative overflow-hidden"
            in:fly={{ y: -40, duration: 800, easing: backOut }}
            out:fly={{ y: 20, duration: 400 }}
        >
            <div class="px-10 pt-12 pb-10 space-y-10 relative z-10">
                <div class="text-center space-y-4">
                    <span
                        class="text-[10px] font-black uppercase tracking-[0.4em] text-amber-400"
                        >Initiation Sequence</span
                    >
                    <h2
                        class="text-4xl font-black italic tracking-tighter text-white"
                    >
                        Welcome to Sovereign DaVinci
                    </h2>
                    <p
                        class="text-white/60 text-sm max-w-md mx-auto leading-relaxed"
                    >
                        You have entered the Cathedral. Here, complexity is
                        commanded through elegance, and your autonomy is
                        mathematically guaranteed.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="pillar-card">
                        <div class="icon-wrapper">
                            <Fingerprint size={28} class="text-emerald-400" />
                        </div>
                        <h3
                            class="text-sm font-black text-white uppercase tracking-wider mb-2"
                        >
                            Your Identity
                        </h3>
                        <p class="text-xs text-white/50 leading-relaxed">
                            Mint a self-sovereign DID. Your data stays with you,
                            protected by Zero-Knowledge proofs.
                        </p>
                    </div>

                    <div class="pillar-card">
                        <div class="icon-wrapper">
                            <Wallet size={28} class="text-amber-400" />
                        </div>
                        <h3
                            class="text-sm font-black text-white uppercase tracking-wider mb-2"
                        >
                            Your Wealth
                        </h3>
                        <p class="text-xs text-white/50 leading-relaxed">
                            Secure your assets in a permissionless vault. Move
                            value instantly without intermediaries.
                        </p>
                    </div>

                    <div class="pillar-card">
                        <div class="icon-wrapper">
                            <Vote size={28} class="text-purple-400" />
                        </div>
                        <h3
                            class="text-sm font-black text-white uppercase tracking-wider mb-2"
                        >
                            Your Voice
                        </h3>
                        <p class="text-xs text-white/50 leading-relaxed">
                            Shape the network through fractal democracy. Cast
                            your vote and watch it ripple across the mesh.
                        </p>
                    </div>
                </div>

                <div class="flex flex-col items-center gap-4 pt-4">
                    <button class="start-btn pulse-glow" onclick={startJourney}>
                        <span>Begin the Journey</span>
                        <ChevronRight size={18} />
                    </button>
                    <button
                        class="text-[10px] font-bold text-white/30 hover:text-white/60 uppercase tracking-widest transition-colors"
                        onclick={exploreAsGuest}
                    >
                        Explore as Guest
                    </button>
                </div>
            </div>

            <!-- Subtle edge highlight -->
            <div
                class="absolute inset-0 pointer-events-none border border-white/10 rounded-[2.5rem] mix-blend-overlay"
            ></div>
        </div>
    </div>
{/if}

<style>
    .welcome-panel {
        background: linear-gradient(
            180deg,
            rgba(20, 20, 25, 0.95) 0%,
            rgba(10, 10, 15, 0.98) 100%
        );
        border-radius: 2.5rem;
        box-shadow:
            0 40px 100px -20px rgba(0, 0, 0, 0.8),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .pillar-card {
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .pillar-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .icon-wrapper {
        width: 64px;
        height: 64px;
        border-radius: 1rem;
        background: rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .start-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem 3rem;
        background: linear-gradient(135deg, #1e1e24 0%, #111115 100%);
        color: white;
        border: 1px solid rgba(251, 191, 36, 0.4); /* amber tint */
        border-radius: 2rem;
        font-size: 0.85rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.2s;
        cursor: pointer;
        position: relative;
    }

    .pulse-glow::after {
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: 2rem;
        background: linear-gradient(
            135deg,
            rgba(251, 191, 36, 0.5),
            rgba(251, 191, 36, 0.1)
        );
        z-index: -1;
        opacity: 0.5;
        animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse-ring {
        0%,
        100% {
            opacity: 0.2;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.02);
        }
    }

    .start-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(251, 191, 36, 0.15);
        border-color: rgba(251, 191, 36, 0.8);
    }

    .start-btn:active {
        transform: translateY(0);
        scale: 0.98;
    }
</style>
