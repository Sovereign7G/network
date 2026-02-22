<script lang="ts" context="module">
    import { Music, BookOpen } from "lucide-svelte";
</script>

<script lang="ts">
    import {
        Camera,
        Shield,
        Cpu,
        Smartphone,
        Zap,
        Globe,
        Lock,
        ArrowLeft,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    const protocols = [
        {
            id: "HOLLY-1",
            title: "Production Mesh",
            description:
                "Orchestrating high-throughput creative workflows across the sovereign substrate. Geographic neutrality ensures production resilience.",
            icon: Camera,
            color: "text-neon-amber",
            bg: "bg-neon-amber/5",
            border: "border-neon-amber/20",
        },
        {
            id: "CINEMA-1",
            title: "Ritual Integrity",
            description:
                "Measuring intentional communal viewing indices. Restoring the social value of cinema through verifiable ritual signatures.",
            icon: Zap,
            color: "text-neon-amber",
            bg: "bg-neon-amber/5",
            border: "border-neon-amber/20",
        },
        {
            id: "VOX-1",
            title: "Vocal Authenticity",
            description:
                "Protecting the lineage of performers. Preventing unauthorized AI replication of vocal DNA with VoidAuth signatures.",
            icon: Music,
            color: "text-neon-amber",
            bg: "bg-neon-amber/5",
            border: "border-neon-amber/20",
        },
        {
            id: "DRAMA-1",
            title: "Narrative Governance",
            description:
                "On-chain script vaults and creator participation metrics. Ensuring sovereign storytelling in an age of generative commodification.",
            icon: BookOpen,
            color: "text-neon-amber",
            bg: "bg-neon-amber/5",
            border: "border-neon-amber/20",
        },
        {
            id: "ESIM-1",
            title: "Connectivity Shell",
            description:
                "Decentralized DePIN marketplace for sovereign connectivity. Peer-to-peer eSIM orchestration for a borderless internet.",
            icon: Smartphone,
            color: "text-blue-400",
            bg: "bg-blue-400/5",
            border: "border-blue-400/20",
        },
    ];

    // Note: BookOpen and Music imports were missing in the list above, let's fix that in reality
</script>

<div class="min-h-screen bg-[#020408] text-white p-6 lg:p-20 font-sans">
    <div class="max-w-5xl mx-auto">
        <a
            href="/"
            class="inline-flex items-center space-x-2 text-[10px] font-black mono-font tracking-widest text-white/40 hover:text-neon-cyan transition-colors mb-20 group"
        >
            <ArrowLeft
                size={12}
                class="group-hover:-translate-x-1 transition-transform"
            />
            <span>BACK TO DISCOVERY</span>
        </a>

        <header class="mb-32">
            <h1
                class="text-6xl md:text-8xl font-black italic tracking-tighter uppercase leading-none mb-8"
            >
                THE CORE<br />
                <span class="neon-text">PROTOCOLS</span>
            </h1>
            <p class="text-xl text-white/60 max-w-2xl leading-relaxed">
                The AGE Protocol is defined by a series of specialized
                governance modules, each designed to ensure institutional
                resilience and individual sovereignty.
            </p>
        </header>

        <div class="space-y-12">
            {#each protocols as protocol, i}
                <div
                    class="glass-panel p-10 flex flex-col md:flex-row gap-10 items-start md:items-center hover:border-white/20 transition-all card-glow {protocol.border}"
                    in:fly={{ y: 30, delay: i * 100 }}
                >
                    <div
                        class="p-6 rounded-3xl {protocol.bg} {protocol.color} border {protocol.border}"
                    >
                        <protocol.icon size={40} />
                    </div>
                    <div class="flex-grow">
                        <div class="flex items-center space-x-4 mb-2">
                            <span
                                class="text-xs font-black mono-font tracking-[0.3em] opacity-30"
                                >{protocol.id}</span
                            >
                            <div class="h-px flex-grow bg-white/5"></div>
                        </div>
                        <h2
                            class="text-3xl font-black italic uppercase tracking-tight mb-4"
                        >
                            {protocol.title}
                        </h2>
                        <p class="text-white/40 text-lg leading-relaxed">
                            {protocol.description}
                        </p>
                    </div>
                </div>
            {/each}
        </div>

        <section class="mt-40 pt-20 border-t border-white/5">
            <div
                class="glass-panel p-12 bg-neon-cyan/5 border-neon-cyan/20 text-center"
            >
                <h3 class="text-2xl font-black italic uppercase mb-6">
                    Contribute to the Substrate
                </h3>
                <p class="text-white/60 mb-10 max-w-xl mx-auto italic">
                    All protocols are open for institutional hardening and peer
                    review. Join the sovereign network today.
                </p>
                <div class="flex flex-col md:flex-row justify-center gap-6">
                    <button
                        class="px-8 py-4 bg-neon-cyan text-black font-black italic rounded-xl hover:scale-105 active:scale-95 transition-all"
                        >HARDEN PROTOCOL</button
                    >
                    <button
                        class="px-8 py-4 border border-white/10 text-white/60 font-black italic rounded-xl hover:bg-white/5"
                        >VIEW WHITE SHEETS</button
                    >
                </div>
            </div>
        </section>
    </div>
</div>

<style>
    h1,
    h2,
    h3,
    button {
        font-family: var(--font-display);
    }
</style>
