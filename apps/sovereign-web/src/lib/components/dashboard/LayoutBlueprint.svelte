<script lang="ts">
    import {
        ChevronRight,
        Eye,
        Layout,
        Grid3X3,
        Layers,
        Boxes,
    } from "lucide-svelte";

    let activeLayer = $state("Root_Grid");
    let showColorCoding = $state(true);

    const hierarchy = [
        {
            id: "root",
            label: "Root_Grid",
            color: "bg-red-500/20",
            borderColor: "border-red-500",
            icon: Layout,
            desc: "Primary application manifold container.",
        },
        {
            id: "secondary",
            label: "Secondary_Sidebar",
            color: "bg-emerald-500/20",
            borderColor: "border-emerald-500",
            icon: Layout,
            desc: "Navigation and context-switching vessels.",
        },
        {
            id: "primary",
            label: "Primary_Content_Area",
            color: "bg-blue-500/20",
            borderColor: "border-blue-500",
            icon: Grid3X3,
            desc: "The manifest logic and viewport shards.",
        },
        {
            id: "inner",
            label: "Inner_Stack_Flow",
            color: "bg-yellow-500/20",
            borderColor: "border-yellow-500",
            icon: Layers,
            desc: "Sequential logic or repetitive component shards.",
        },
    ];

    const currentLayer = $derived(
        hierarchy.find((h) => h.label === activeLayer) || hierarchy[0],
    );
</script>

<div
    class="layout-blueprint-audit bg-black/60 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-6 relative overflow-hidden group"
>
    <!-- Header -->
    <header class="flex justify-between items-start z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-red-500/10 rounded-2xl text-red-500 border border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.1)]"
            >
                <Boxes size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Layout_Blueprint_Audit
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Nested_Box_Architecture // Hierarchical_Decomposition
                </p>
            </div>
        </div>
        <button
            onclick={() => (showColorCoding = !showColorCoding)}
            class="px-3 py-1.5 rounded-full text-[8px] font-black uppercase tracking-widest border transition-all flex items-center gap-2 {showColorCoding
                ? 'bg-white/10 border-white/20 text-white'
                : 'text-white/40 border-white/5'}"
        >
            <Eye size={10} />
            VISUAL_AUDIT_{showColorCoding ? "ON" : "OFF"}
        </button>
    </header>

    <!-- Visual Decomposition Area -->
    <div class="flex-1 flex gap-6 z-10">
        <!-- The "Mock" Blueprint Visualization -->
        <div
            class="flex-[1.5] bg-white/5 border border-white/10 rounded-3xl p-4 relative overflow-hidden backdrop-blur-sm"
        >
            <div
                class="w-full h-full border-2 border-dashed border-white/10 rounded-2xl p-4 flex gap-4 transition-all {showColorCoding &&
                activeLayer === 'Root_Grid'
                    ? 'border-red-500'
                    : ''}"
            >
                <!-- Sidebar Representation (Green) -->
                <div
                    class="w-20 h-full border-2 border-white/5 rounded-xl transition-all {showColorCoding
                        ? 'bg-emerald-500/20 border-emerald-500'
                        : ''}"
                    role="presentation"
                    onmouseenter={() => (activeLayer = "Secondary_Sidebar")}
                ></div>

                <!-- Content Area Representation (Blue) -->
                <div
                    class="flex-1 flex flex-col gap-4 border-2 border-white/5 rounded-xl transition-all {showColorCoding
                        ? 'bg-blue-500/20 border-blue-500'
                        : ''}"
                    role="presentation"
                    onmouseenter={() => (activeLayer = "Primary_Content_Area")}
                >
                    <!-- Inner Elements (Yellow) -->
                    <div
                        class="h-20 w-full border-2 border-white/5 rounded-lg transition-all {showColorCoding
                            ? 'bg-yellow-500/20 border-yellow-500'
                            : ''}"
                        role="presentation"
                        onmouseenter={(e) => {
                            e.stopPropagation();
                            activeLayer = "Inner_Stack_Flow";
                        }}
                    ></div>
                </div>
            </div>

            <!-- Absolute Labels -->
            {#if showColorCoding}
                <div
                    class="absolute top-6 left-6 text-[7px] font-black text-red-500 uppercase tracking-widest bg-black/40 px-2 py-1 rounded"
                >
                    ROOT
                </div>
                <div
                    class="absolute top-10 left-10 text-[7px] font-black text-emerald-500 uppercase tracking-widest bg-black/40 px-2 py-1 rounded"
                >
                    SIDEBAR
                </div>
                <div
                    class="absolute top-10 right-10 text-[7px] font-black text-blue-500 uppercase tracking-widest bg-black/40 px-2 py-1 rounded"
                >
                    CONTENT
                </div>
            {/if}
        </div>

        <!-- Metadata & Rules -->
        <div class="flex-1 flex flex-col gap-4">
            <h3
                class="text-[10px] font-black text-white/60 uppercase tracking-widest mb-2 flex items-center gap-2"
            >
                <Layout size={12} />
                Selected_Container
            </h3>

            <div
                class="p-4 rounded-3xl border transition-all duration-500 {currentLayer.borderColor} bg-white/5"
            >
                <div class="flex items-center gap-3 mb-3">
                    <currentLayer.icon size={16} class="text-white" />
                    <span class="text-xs font-bold text-white uppercase"
                        >{currentLayer.label}</span
                    >
                </div>
                <p class="text-[9px] text-white/40 leading-relaxed italic">
                    {currentLayer.desc}
                </p>
            </div>

            <div
                class="flex-1 bg-white/5 border border-white/10 rounded-3xl p-4 space-y-3"
            >
                <span
                    class="text-[8px] font-black text-white/20 uppercase tracking-widest block mb-1"
                    >Structural_Axioms</span
                >
                {#each ["Every complex UI is nested boxes.", " Mastery of the Grid is sovereignty.", "Stack Panels for sequential flows."] as rule}
                    <div class="flex items-center gap-2">
                        <ChevronRight size={10} class="text-red-500" />
                        <span class="text-[9px] font-medium text-white/60"
                            >{rule}</span
                        >
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Background Decoration -->
    <div
        class="absolute inset-0 opacity-[0.03] pointer-events-none"
        style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 30px 30px;"
    ></div>
</div>
