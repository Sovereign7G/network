<script lang="ts">
    import {
        Paintbrush,
        Palette,
        Type,
        Space,
        Zap,
        ShieldCheck,
    } from "lucide-svelte";

    const colors = [
        {
            name: "Cyan_Resonance",
            hex: "#22d3ee",
            usage: "Primary Action / Data Flow",
        },
        {
            name: "Amber_Coherence",
            hex: "#fbbf24",
            usage: "Strategic Warning / Simulation",
        },
        {
            name: "Rose_Crisis",
            hex: "#f43f5e",
            usage: "Node Failure / Critical Error",
        },
        {
            name: "Aether_Indigo",
            hex: "#6366f1",
            usage: "Wasm Execution / Ephemeral Shards",
        },
        {
            name: "Deep_Manifold",
            hex: "#0a0514",
            usage: "Institutional Background / Glass",
        },
    ];

    const typography = [
        {
            name: "Headline_Prime",
            font: "Outfit",
            weight: "950",
            tracking: "-0.02em",
        },
        {
            name: "Terminal_Mono",
            font: "JetBrains Mono",
            weight: "700",
            tracking: "0.1em",
        },
        {
            name: "Body_Systemic",
            font: "Inter",
            weight: "400",
            tracking: "normal",
        },
    ];

    const spacing = [
        { label: "Atomic", value: "4px", desc: "Micro-alignment" },
        { label: "Molecular", value: "16px", desc: "Component Gaps" },
        { label: "Planetary", value: "48px", desc: "Section Buffers" },
    ];
</script>

<div
    class="design-substrate-manifold bg-black/80 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group"
>
    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-3 bg-cyan-400/10 rounded-2xl text-cyan-400 border border-cyan-400/20"
            >
                <Paintbrush size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.3em] text-white"
                >
                    Design_Substrate_v1
                </h2>
                <span
                    class="text-[8px] font-black text-white/30 uppercase italic"
                    >Clean Futurism // Context Engineering Step 2</span
                >
            </div>
        </div>
        <div class="flex items-center gap-2">
            <ShieldCheck size={12} class="text-white/20" />
            <span class="text-[8px] font-black text-white/20 uppercase"
                >AAL3_Design_Governance</span
            >
        </div>
    </header>

    <div
        class="flex-1 grid grid-cols-2 gap-8 z-10 custom-scrollbar overflow-y-auto pr-4"
    >
        <!-- Color Palette -->
        <section class="space-y-4">
            <div class="flex items-center gap-3 mb-2">
                <Palette size={14} class="text-cyan-400" />
                <h3
                    class="text-[10px] font-black text-white uppercase tracking-widest"
                >
                    Spectral_Palette
                </h3>
            </div>
            <div class="grid gap-3">
                {#each colors as color}
                    <div
                        class="flex items-center gap-4 p-3 bg-white/5 border border-white/10 rounded-2xl hover:border-cyan-400/40 transition-all"
                    >
                        <div
                            class="w-10 h-10 rounded-xl shadow-lg border border-white/10"
                            style:background={color.hex}
                        ></div>
                        <div class="flex flex-col">
                            <span
                                class="text-[10px] font-bold text-white uppercase"
                                >{color.name}</span
                            >
                            <span class="text-[8px] font-black text-white/20"
                                >{color.hex} // {color.usage}</span
                            >
                        </div>
                    </div>
                {/each}
            </div>
        </section>

        <!-- Typography & Spacing -->
        <div class="space-y-8">
            <!-- Typography -->
            <section class="space-y-4">
                <div class="flex items-center gap-3 mb-2">
                    <Type size={14} class="text-amber-400" />
                    <h3
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                    >
                        Type_Hierarchy
                    </h3>
                </div>
                <div class="space-y-3">
                    {#each typography as type}
                        <div
                            class="p-4 bg-white/5 border border-white/10 rounded-2xl"
                        >
                            <span
                                class="text-[8px] font-black text-white/20 uppercase block mb-2"
                                >{type.name}</span
                            >
                            <p
                                style:font-family={type.font}
                                style:font-weight={type.weight}
                                style:letter-spacing={type.tracking}
                                class="text-white text-lg"
                            >
                                Sovereign_Logic_0xAA
                            </p>
                        </div>
                    {/each}
                </div>
            </section>

            <!-- Spacing -->
            <section class="space-y-4">
                <div class="flex items-center gap-3 mb-2">
                    <Space size={14} class="text-emerald-400" />
                    <h3
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                    >
                        Geometric_Spacing
                    </h3>
                </div>
                <div class="grid grid-cols-3 gap-2">
                    {#each spacing as s}
                        <div
                            class="p-3 bg-white/5 border border-white/10 rounded-xl text-center"
                        >
                            <span class="text-lg font-black text-white"
                                >{s.value}</span
                            >
                            <span
                                class="text-[7px] font-black text-white/20 uppercase block mt-1"
                                >{s.label}</span
                            >
                        </div>
                    {/each}
                </div>
            </section>
        </div>
    </div>

    <!-- Footer Meta -->
    <footer
        class="mt-auto pt-6 border-t border-white/5 flex justify-between items-center z-10"
    >
        <div class="flex items-center gap-2">
            <Zap size={10} class="text-cyan-400" />
            <span class="text-[8px] font-black text-white/40 uppercase"
                >Aesthetic_Coherence_Score: 99.8%</span
            >
        </div>
        <div class="flex gap-2">
            <div
                class="w-3 h-3 rounded-sm bg-white/5 border border-white/10"
            ></div>
            <div
                class="w-3 h-3 rounded-sm bg-white/10 border border-white/20"
            ></div>
            <div class="w-3 h-3 rounded-sm bg-cyan-400"></div>
        </div>
    </footer>

    <!-- Background Decoration -->
    <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_0%_0%,rgba(34,211,238,0.05),transparent_50%)] pointer-events-none"
    ></div>
</div>
