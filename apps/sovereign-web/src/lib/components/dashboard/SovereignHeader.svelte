<script lang="ts">
    import {
        ArrowRight,
        Bookmark,
        Package,
        Sparkles,
        Lock,
        Info,
        User,
        Activity,
    } from "lucide-svelte";
    import { fly } from "svelte/transition";

    interface Props {
        activeTab: string;
        userId: string | null;
        isSweeping: boolean;
        isZenMode: boolean;
        showWisdom: boolean;
        showProfile: boolean;
        onTabSelect: (id: string) => void;
        onToggleSweeping: () => void;
        onToggleZen: () => void;
        onToggleWisdom: () => void;
        onToggleProfile: () => void;
    }

    let {
        activeTab,
        userId,
        isSweeping,
        isZenMode,
        showWisdom,
        showProfile,
        onTabSelect,
        onToggleSweeping,
        onToggleZen,
        onToggleWisdom,
        onToggleProfile,
    }: Props = $props();
</script>

<header
    class="flex justify-between items-end mb-20 pb-8 border-b {isZenMode
        ? 'border-black/5'
        : 'border-white/[0.03]'}"
>
    <div in:fly={{ x: -20, duration: 1000 }}>
        <div class="flex items-center gap-4 mb-3">
            <div
                class="flex items-center gap-1.5 text-[7px] font-black {isZenMode
                    ? 'text-black/30'
                    : 'text-white/30'} uppercase tracking-[0.2em]"
            >
                <span>SOVEREIGN</span>
                <ArrowRight size={8} class="opacity-20" />
                <span>DASHBOARD</span>
                <ArrowRight size={8} class="opacity-20" />
                <span class={isZenMode ? "text-[#00B900]" : "text-neon-cyan"}
                    >{activeTab.toUpperCase()}</span
                >
            </div>
            <div
                class="h-1 w-1 rounded-full {isZenMode
                    ? 'bg-black/10'
                    : 'bg-white/10'}"
            ></div>
            <div class="flex items-center gap-2">
                <div
                    class="w-2 h-2 rounded-full {isZenMode
                        ? 'bg-[#00B900]'
                        : 'bg-neon-cyan'} resonance-pulse"
                ></div>
                <span
                    class="text-[8px] font-black uppercase tracking-[0.4em] {isZenMode
                        ? 'text-[#00B900]'
                        : 'text-neon-cyan'}">SUBSTRATE LIVE</span
                >
            </div>
        </div>
        <h1
            class="text-5xl font-black tracking-tighter uppercase italic leading-none {isZenMode
                ? 'text-[#3C1E1E]'
                : 'text-white'}"
        >
            {activeTab.replace("_", " ")}
            <span class="opacity-20 text-4xl">COMMAND</span>
        </h1>
        <div class="flex items-center gap-4 mt-4">
            <p
                class="{isZenMode
                    ? 'text-black/30 bg-black/[0.02] border-black/5'
                    : 'text-white/30 bg-white/[0.02] border-white/5'} text-[9px] mono-font uppercase tracking-[0.2em] px-2 py-1 border rounded"
            >
                ID: {userId || "NOT_ASSIGNED"}
            </p>
            <p
                class="text-[9px] mono-font {isZenMode
                    ? 'text-[#00B900]/60'
                    : 'text-neon-cyan/60'} uppercase tracking-[0.2em]"
            >
                // CLEARANCE: AAL3_ALPHA
            </p>
        </div>
    </div>
    <div class="flex items-center space-x-8" in:fly={{ x: 20, duration: 1000 }}>
        <div class="flex flex-col items-end space-y-1">
            <span
                class="text-[7px] font-black opacity-20 uppercase tracking-[0.3em]"
                >TEMPORAL_ANCHOR</span
            >
            <span
                class="text-xs mono-font font-bold {isZenMode
                    ? 'text-[#3C1E1E]'
                    : 'text-white'}"
                >23:45:01 <span class="opacity-30">UTC</span></span
            >
        </div>
        <button
            onclick={onToggleSweeping}
            class="px-5 py-2.5 bg-[#24AE7C]/10 border border-[#24AE7C]/20 text-[#24AE7C] font-black uppercase tracking-widest text-[8px] rounded-xl hover:bg-[#24AE7C] hover:text-black transition-all flex items-center gap-2 active:scale-95"
        >
            <Activity size={12} class={isSweeping ? "animate-spin" : ""} />
            {isSweeping ? "SWEEPING..." : "CLEARANCE_SWEEP"}
        </button>

        <div
            class="{isZenMode ? 'bg-black/5' : 'bg-white/[0.03]'} h-10 w-px"
        ></div>

        <button
            class="w-12 h-12 rounded-2xl border {isZenMode
                ? 'border-black/5 bg-black/[0.02] text-black/30'
                : 'border-white/10 bg-white/[0.02] text-white/30'} hover:bg-black/5 transition-all flex flex-col items-center justify-center gap-1 relative group"
        >
            <Bookmark size={16} />
            <span
                class="text-[6px] font-black uppercase tracking-widest leading-none"
                >WISHLIST</span
            >
            <div
                class="absolute -top-1 -right-1 w-4 h-4 {isZenMode
                    ? 'bg-[#00B900]'
                    : 'bg-neon-cyan'} text-black text-[8px] font-black rounded-full border-2 {isZenMode
                    ? 'border-white'
                    : 'border-[#020408]'} flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
                2
            </div>
        </button>

        <button
            class="w-12 h-12 rounded-2xl border {isZenMode
                ? 'border-black/5 bg-black/[0.02] text-black/30'
                : 'border-white/10 bg-white/[0.02] text-white/30'} hover:bg-black/5 transition-all flex flex-col items-center justify-center gap-1 relative group"
        >
            <Package size={16} />
            <span
                class="text-[6px] font-black uppercase tracking-widest leading-none"
                >ORDERS</span
            >
            <div
                class="absolute -top-1 -right-1 w-4 h-4 bg-amber-400 text-black text-[8px] font-black rounded-full border-2 {isZenMode
                    ? 'border-white'
                    : 'border-[#020408]'} flex items-center justify-center"
            >
                1
            </div>
        </button>

        <div
            class="{isZenMode ? 'bg-black/5' : 'bg-white/[0.03]'} h-10 w-px"
        ></div>

        <button
            onclick={() => onTabSelect("evolve")}
            class="relative w-12 h-12 rounded-2xl border border-amber-400/20 bg-amber-400/5 text-amber-400 flex flex-col items-center justify-center gap-1 hover:bg-amber-400/10 transition-all active:scale-95"
        >
            <Sparkles size={16} />
            <span
                class="text-[6px] font-black uppercase tracking-widest leading-none"
                >PATCH</span
            >
            <div
                class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 {isZenMode
                    ? 'border-white'
                    : 'border-[#020408]'} animate-pulse"
            ></div>
        </button>

        <div
            class="{isZenMode ? 'bg-black/5' : 'bg-white/[0.03]'} h-10 w-px"
        ></div>

        <div
            class="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/20 rounded-full"
        >
            <Lock size={10} class="text-green-500" />
            <span
                class="text-[7px] font-black text-green-500 uppercase tracking-widest leading-none"
                >E2EE</span
            >
        </div>

        <button
            onclick={onToggleZen}
            class="px-3 py-2 rounded-xl border {isZenMode
                ? 'bg-[#00B900] border-[#00B900] text-white'
                : 'bg-white/5 border-white/10 text-white/40'} text-[8px] font-black uppercase tracking-widest transition-all hover:scale-105 active:scale-95"
        >
            {isZenMode ? "Obsidian" : "Zen"}
        </button>

        <div
            class="{isZenMode ? 'bg-black/5' : 'bg-white/[0.03]'} h-10 w-px"
        ></div>
        <button
            onclick={onToggleWisdom}
            class="w-12 h-12 rounded-2xl border transition-all flex flex-col items-center justify-center gap-1 {showWisdom
                ? isZenMode
                    ? 'border-[#00B900] bg-[#00B900]/10 text-[#00B900]'
                    : 'border-neon-cyan bg-neon-cyan/10 text-neon-cyan shadow-[0_0_20px_rgba(0,242,255,0.1)]'
                : isZenMode
                  ? 'border-black/5 bg-black/[0.02] text-black/30'
                  : 'border-white/10 bg-white/[0.02] text-white/30 hover:bg-white/5'}"
        >
            <Info size={16} />
            <span
                class="text-[6px] font-black uppercase tracking-widest leading-none"
                >WISDOM</span
            >
        </button>
        <button
            onclick={onToggleProfile}
            class="w-12 h-12 rounded-2xl border {showProfile
                ? isZenMode
                    ? 'border-[#00B900]'
                    : 'border-neon-cyan'
                : isZenMode
                  ? 'border-black/5'
                  : 'border-white/10'} {isZenMode
                ? 'bg-black/[0.02]'
                : 'bg-white/[0.02]'} flex items-center justify-center group hover:border-white/20 transition-all cursor-pointer relative"
        >
            <User
                size={18}
                class={showProfile
                    ? isZenMode
                        ? "text-[#00B900]"
                        : "text-neon-cyan"
                    : isZenMode
                      ? "text-black/20 group-hover:text-black/60"
                      : "opacity-20 group-hover:opacity-60 transition-opacity"}
            />
            <div
                class="absolute -top-1 -right-1 w-3 h-3 bg-[#24AE7C] rounded-full border-2 {isZenMode
                    ? 'border-white'
                    : 'border-[#04060b]'}"
            ></div>
        </button>
    </div>
</header>
