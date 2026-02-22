<script lang="ts">
    import { fade, fly } from "svelte/transition";

    const tokens = [
        {
            name: "AGE Core",
            symbol: "AGE",
            img: "/images/tokens/age.png",
            desc: "The fundamental unit of governance and protocol sovereignty. Used for high-level constitutional voting.",
            color: "text-cyan-400",
            glow: "shadow-cyan-500/20",
        },
        {
            name: "Universal Credit",
            symbol: "UCT",
            img: "/images/tokens/uct.png",
            desc: "Optimized for global fiat-parity transactions and daily citizen commerce.",
            color: "text-white",
            glow: "shadow-white/20",
        },
        {
            name: "Artemis Resonance",
            symbol: "ARI",
            img: "/images/tokens/ari.png",
            desc: "Index of mesh resonance. Tracks extra-terrestrial node health and lunar consensus.",
            color: "text-blue-200",
            glow: "shadow-blue-200/20",
        },
        {
            name: "Bio-Liquid",
            symbol: "H2O",
            img: "/images/tokens/h2o.png",
            desc: "Direct representation of critical physical resources within the digital mesh.",
            color: "text-emerald-400",
            glow: "shadow-emerald-400/20",
        },
        {
            name: "Sovereign Bond",
            symbol: "BOND",
            img: "/images/tokens/bond.png",
            desc: "Long-term institutional debt instrument, yield-bearing and gold-backed.",
            color: "text-amber-400",
            glow: "shadow-amber-400/20",
        },
        {
            name: "Merit Identity",
            symbol: "MERITS",
            img: "/images/tokens/merits.png",
            desc: "Non-transferable reputation shards earned through verified civic contribution.",
            color: "text-purple-400",
            glow: "shadow-purple-400/20",
        },
        {
            name: "Moral Compass",
            symbol: "MORAL",
            img: "/images/tokens/moral.png",
            desc: "Ethical alignment verification token used for AI Control Plane interventions.",
            color: "text-green-600",
            glow: "shadow-green-600/20",
        },
    ];
</script>

<div class="px-8 py-24 max-w-7xl mx-auto" in:fade>
    <div class="mb-20">
        <div
            class="text-[10px] font-black tracking-[0.4em] text-white/40 uppercase mb-4 italic"
        >
            Economic Layer // Protocol Assets
        </div>
        <h1
            class="text-7xl font-black italic uppercase tracking-tighter mb-8 leading-none"
        >
            Sovereign <span class="text-white/20">Tokenomics</span>
        </h1>
        <p class="text-xl text-white/40 font-bold max-w-3xl italic">
            The multi-token architecture of the AGE Protocol ensures resilient
            resource allocation, reputation-based governance, and instant liquid
            settlement across extra-terrestrial mesh nodes.
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each tokens as token, i}
            <div
                class="glass-panel p-10 border-white/5 group hover:border-white/10 transition-all cursor-default"
                in:fly={{ y: 20, delay: i * 100 }}
            >
                <div
                    class="relative w-full aspect-square mb-10 flex items-center justify-center"
                >
                    <!-- Glow effect -->
                    <div
                        class="absolute inset-0 bg-white/5 blur-[80px] rounded-full scale-50 group-hover:scale-100 transition-transform duration-700"
                    ></div>

                    <img
                        src={token.img}
                        alt={token.name}
                        class="w-48 h-48 relative z-10 drop-shadow-2xl group-hover:scale-110 transition-transform duration-500"
                    />
                </div>

                <div class="text-center relative z-10">
                    <div
                        class="text-[9px] font-black tracking-[0.3em] text-white/20 uppercase mb-2"
                    >
                        Asset Type // {token.symbol}
                    </div>
                    <h3
                        class="text-3xl font-black italic uppercase tracking-tighter mb-4 {token.color}"
                    >
                        {token.name}
                    </h3>
                    <p
                        class="text-sm text-white/40 font-bold italic leading-relaxed"
                    >
                        {token.desc}
                    </p>
                </div>
            </div>
        {/each}
    </div>
</div>
