<script lang="ts">
    import { Search, Zap, AlertTriangle, ChevronRight } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
    import LivingMap from "$lib/components/map/LivingMap.svelte";
    import type { Snippet } from "svelte";

    interface Props {
        activeCanister: string | null;
        isScanning: boolean;
        causalNarrative: any;
        isZenMode: boolean;
        onFetchForensics: (id: string) => void;
        sidebar?: Snippet;
    }

    let {
        activeCanister,
        isScanning,
        causalNarrative,
        isZenMode,
        onFetchForensics,
        sidebar,
    }: Props = $props();

    const canisters = [
        {
            id: "ryjl3-tyaaa-aaaaa-aaaba-cai",
            name: "sophia_canister",
            status: "HEALTHY",
            type: "zap",
        },
        {
            id: "vu5yx-eh777-77774-qaaga-cai",
            name: "merit_canister",
            status: "ALERT",
            type: "alert",
        },
    ];
</script>

<div class="grid grid-cols-1 lg:grid-cols-12 gap-8" in:fade>
    <!-- Main Forensics Area -->
    <div class="lg:col-span-8 space-y-8">
        <section
            class="glass-panel p-8 card-glow relative overflow-hidden {isZenMode
                ? 'bg-white border-black/5'
                : ''}"
        >
            <div
                class="absolute -top-24 -right-24 w-64 h-64 {isZenMode
                    ? 'bg-[#00B900]/5'
                    : 'bg-[#00f2ff]/5'} rounded-full blur-3xl"
            ></div>
            <h2
                class="text-3xl font-black mb-8 flex items-center italic tracking-tight {isZenMode
                    ? 'text-[#3C1E1E]'
                    : 'text-white'}"
            >
                <Search
                    size={32}
                    class="mr-4 {isZenMode ? 'text-[#00B900]' : 'neon-text'}"
                />
                WITR CAUSAL FORENSICS
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                {#each canisters as canister}
                    <button
                        onclick={() => onFetchForensics(canister.id)}
                        class="w-full p-6 {isZenMode
                            ? 'bg-[#F9FAFB]'
                            : 'bg-white/5'} rounded-2xl border transition-all text-left group {activeCanister ===
                        canister.id
                            ? isZenMode
                                ? 'border-[#00B900] bg-[#00B900]/5'
                                : 'border-neon-cyan bg-neon-cyan/5 shadow-[0_0_20px_rgba(0,242,255,0.1)]'
                            : isZenMode
                              ? 'border-black/5 hover:border-black/20'
                              : 'border-white/5 hover:border-white/20'}"
                    >
                        <div class="flex justify-between items-start mb-4">
                            <div
                                class="w-10 h-10 rounded-xl flex items-center justify-center {canister.status ===
                                'HEALTHY'
                                    ? isZenMode
                                        ? 'bg-[#00B900]/10 text-[#00B900]'
                                        : 'bg-neon-cyan/10 text-neon-cyan'
                                    : 'bg-red-500/20 text-red-400'}"
                            >
                                {#if canister.type === "zap"}
                                    <Zap size={20} />
                                {:else}
                                    <AlertTriangle size={20} />
                                {/if}
                            </div>
                            <div
                                class="text-[9px] font-bold px-2 py-0.5 rounded border {canister.status ===
                                'HEALTHY'
                                    ? isZenMode
                                        ? 'border-[#00B900]/30 text-[#00B900] bg-[#00B900]/10'
                                        : 'border-neon-cyan/30 text-neon-cyan bg-neon-cyan/10'
                                    : 'border-red-500/30 text-red-500 bg-red-500/10'}"
                            >
                                {canister.status}
                            </div>
                        </div>
                        <h4
                            class="font-bold text-lg mb-1 {isZenMode
                                ? 'text-[#3C1E1E]'
                                : 'text-white'}"
                        >
                            {canister.name}
                        </h4>
                        <p
                            class="text-[10px] mono-font opacity-40 truncate {isZenMode
                                ? 'text-[#3C1E1E]'
                                : 'text-white'}"
                        >
                            {canister.id}
                        </p>
                    </button>
                {/each}
            </div>

            {#if isScanning}
                <div
                    class="h-64 flex flex-col items-center justify-center space-y-4"
                    in:fade
                >
                    <div
                        class="w-16 h-1 w-64 {isZenMode
                            ? 'bg-black/5'
                            : 'bg-white/5'} rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full {isZenMode
                                ? 'bg-[#00B900]'
                                : 'bg-neon-cyan animate-scan shadow-[0_0_15px_#00f2ff]'}"
                        ></div>
                    </div>
                    <p
                        class="text-[10px] font-bold {isZenMode
                            ? 'text-[#00B900]'
                            : 'neon-text'} mono-font animate-pulse uppercase tracking-[0.3em]"
                    >
                        Executing Causal Autopsy...
                    </p>
                </div>
            {:else if causalNarrative}
                <div class="space-y-6" in:fly={{ y: 20, duration: 500 }}>
                    <div
                        class="{isZenMode
                            ? 'bg-[#F9FAFB] border-black/5'
                            : 'bg-white/5 border border-white/10'} p-6 rounded-xl"
                    >
                        <div class="flex justify-between items-start mb-6">
                            <div>
                                <div
                                    class="text-[10px] mono-font opacity-50 uppercase tracking-[0.2em] mb-1 {isZenMode
                                        ? 'text-[#3C1E1E]'
                                        : 'text-white'}"
                                >
                                    Causal Narrative Target
                                </div>
                                <h3
                                    class="text-2xl font-bold flex items-center {isZenMode
                                        ? 'text-[#3C1E1E]'
                                        : 'text-white'}"
                                >
                                    {causalNarrative.target.name}
                                    <span
                                        class="ml-3 text-xs mono-font opacity-40 font-normal"
                                        >({causalNarrative.target.id})</span
                                    >
                                </h3>
                            </div>
                            <div
                                class="px-3 py-1 {isZenMode
                                    ? 'bg-[#00B900]/10 text-[#00B900] border-[#00B900]/20'
                                    : 'bg-neon-cyan/10 text-neon-cyan border-neon-cyan/20'} rounded text-[10px] font-bold mono-font border"
                            >
                                CONFIDENCE: {causalNarrative.source.confidence}%
                            </div>
                        </div>

                        <div class="space-y-4 mb-8">
                            <div
                                class="text-[10px] mono-font opacity-50 uppercase tracking-[0.2em] {isZenMode
                                    ? 'text-[#3C1E1E]'
                                    : 'text-white'}"
                            >
                                Why It Exists (Trace History)
                            </div>
                            <div class="space-y-3">
                                {#each causalNarrative.whyExists as step}
                                    <div class="flex items-center space-x-4">
                                        <div
                                            class="w-1.5 h-1.5 rounded-full {isZenMode
                                                ? 'bg-[#00B900]'
                                                : 'bg-neon-cyan shadow-[0_0_8px_#00f2ff]'}"
                                        ></div>
                                        <div
                                            class="text-sm {isZenMode
                                                ? 'text-[#3C1E1E]'
                                                : 'text-white'}"
                                        >
                                            <span class="opacity-40"
                                                >{step.from}</span
                                            >
                                            <ChevronRight
                                                size={12}
                                                class="inline mx-2 opacity-20"
                                            />
                                            <span class="font-bold"
                                                >{step.to}</span
                                            >
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                </div>
            {:else}
                <div
                    class="h-full min-h-[500px] relative overflow-hidden rounded-2xl"
                >
                    <LivingMap
                        title="SHARD TELEMETRY"
                        subtitle="Causal Trace Active"
                    />
                </div>
            {/if}
        </section>
    </div>

    <!-- Sidebar -->
    <div class="lg:col-span-4 space-y-8">
        {@render sidebar?.()}
    </div>
</div>
