<script lang="ts">
    import { markTutorialSeen } from "../stores/auth.js";
    import { fade, fly } from "svelte/transition";
    import { LayoutGrid, Globe, ShoppingBag, Vote } from "lucide-svelte";

    let step = $state(0);
    const steps = [
        {
            title: "REGISTRY STATUS",
            description:
                "Your real-time handshake with the sovereign mesh. Monitor your sync status and citizen rank here.",
            label: "NETWORK SYNC",
            icon: LayoutGrid,
            pos: "top-24 left-8",
        },
        {
            title: "GLOBAL SUBSTRATE",
            description:
                "An interactive visualization of the planetary compute mesh. Watch as data shards move across jurisdictions.",
            label: "LIVING MAP",
            icon: Globe,
            pos: "top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2",
        },
        {
            title: "SOVEREIGN MARKET",
            description:
                "Access the global trade protocol. Shard assets, fund missions, and participate in the generative economy.",
            label: "MARKET ACCESS",
            icon: ShoppingBag,
            pos: "bottom-24 left-8",
        },
        {
            title: "GOVERNANCE CORE",
            description:
                "Cast your vote on protocol upgrades and community relief funds. Your voice is hardcoded.",
            label: "DECISION MESH",
            icon: Vote,
            pos: "bottom-24 right-8",
        },
    ];

    function next() {
        if (step < steps.length - 1) {
            step++;
        } else {
            markTutorialSeen();
        }
    }
</script>

<div class="fixed inset-0 z-[100] bg-black/90 backdrop-blur-md" transition:fade>
    {#key step}
        <div
            class="absolute {steps[step]
                .pos} w-96 p-8 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-3xl shadow-[0_0_50px_rgba(0,0,0,0.5)]"
            in:fly={{ y: 20, duration: 600 }}
            out:fade={{ duration: 300 }}
        >
            <div
                class="w-12 h-12 mb-6 flex items-center justify-center rounded-2xl bg-cyan-400/10 border border-cyan-400/20"
            >
                <svelte:component
                    this={steps[step].icon}
                    class="w-6 h-6 text-cyan-400"
                />
            </div>

            <div
                class="mb-2 text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase"
            >
                {steps[step].title}
            </div>

            <h3
                class="mb-4 text-2xl font-black tracking-tighter text-white italic uppercase leading-none"
            >
                {steps[step].label}
            </h3>

            <p class="mb-8 text-white/50 text-sm leading-relaxed italic">
                {steps[step].description}
            </p>

            <div class="flex items-center justify-between">
                <button
                    onclick={markTutorialSeen}
                    class="text-[10px] font-black tracking-widest text-white/20 hover:text-white/40 transition-colors uppercase italic"
                >
                    Skip Tour
                </button>
                <button
                    onclick={next}
                    class="px-8 h-12 rounded-xl bg-cyan-400 text-[#050505] text-[11px] font-black tracking-widest hover:scale-105 transition-all uppercase italic shadow-[0_0_20px_rgba(0,242,255,0.3)]"
                >
                    {step === steps.length - 1
                        ? "Complete Boot"
                        : "Next Protocol"}
                </button>
            </div>
        </div>
    {/key}
</div>
