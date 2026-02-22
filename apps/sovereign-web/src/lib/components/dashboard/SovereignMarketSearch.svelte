<script lang="ts">
    import { Search, Mic, User, Filter, ChevronDown } from "lucide-svelte";
    import { slide } from "svelte/transition";

    interface Props {
        searchQuery: string;
        isAAL3Verified: boolean;
        onToggleAnchored: () => void;
        suggestions: string[];
    }

    let {
        searchQuery = $bindable(),
        isAAL3Verified,
        onToggleAnchored,
        suggestions,
    }: Props = $props();
    let isSpeaking = $state(false);
    let showSuggestions = $state(false);
</script>

<div
    class="flex flex-col md:flex-row justify-between items-center gap-6 bg-black/40 backdrop-blur-3xl p-8 rounded-[3rem] border border-white/[0.03]"
>
    <div class="flex-1 w-full max-w-3xl relative">
        <Search
            class="absolute left-6 top-1/2 -translate-y-1/2 text-white/20"
            size={20}
        />
        <input
            type="text"
            placeholder="Search Agora (Recognition over Recall)..."
            bind:value={searchQuery}
            onfocus={() => (showSuggestions = true)}
            onblur={() => setTimeout(() => (showSuggestions = false), 200)}
            class="w-full bg-white/5 border border-white/10 rounded-[2rem] py-5 pl-16 pr-24 text-sm focus:outline-none focus:border-neon-cyan/40 transition-all font-medium placeholder:text-white/10"
        />

        {#if showSuggestions && searchQuery}
            <div
                class="absolute top-full left-0 w-full mt-2 bg-black border border-white/10 rounded-2xl overflow-hidden z-50 shadow-2xl"
                in:slide
            >
                {#each suggestions.filter((s) => s
                        .toLowerCase()
                        .includes(searchQuery.toLowerCase())) as suggestion}
                    <button
                        class="w-full px-6 py-4 text-left text-sm text-white/60 hover:bg-white/5 hover:text-neon-cyan transition-all flex items-center gap-3"
                        onclick={() => (searchQuery = suggestion)}
                    >
                        <Search size={14} class="opacity-20" />
                        {suggestion}
                    </button>
                {/each}
            </div>
        {/if}
        <button
            onclick={() => (isSpeaking = !isSpeaking)}
            class="absolute right-6 top-1/2 -translate-y-1/2 p-2 rounded-full {isSpeaking
                ? 'bg-red-500 text-white animate-pulse'
                : 'text-white/20 hover:text-white'} transition-all"
        >
            <Mic size={18} />
        </button>
    </div>
    <div class="flex items-center gap-3 ml-4 pl-4 border-l border-white/10">
        <button
            onclick={onToggleAnchored}
            class="flex items-center gap-2 px-4 py-2 rounded-full transition-all {isAAL3Verified
                ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/40 shadow-[0_0_15px_rgba(0,242,255,0.2)]'
                : 'bg-white/5 text-white/40 hover:text-white'}"
        >
            <User size={14} />
            <span class="text-[8px] font-black uppercase tracking-widest"
                >{isAAL3Verified ? "AAL3_ANCHORED" : "GUEST_SESSION"}</span
            >
        </button>
    </div>
    <div class="flex gap-4 ml-auto">
        <button
            class="flex items-center gap-2 px-8 py-5 bg-white/5 rounded-2xl border border-white/10 text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all"
        >
            <Filter size={14} />
            DYNAMIC_FILTERS
            <ChevronDown size={14} class="opacity-30" />
        </button>
        <button
            class="flex items-center gap-2 px-10 py-5 {!isAAL3Verified
                ? 'bg-white/10 text-white/20 cursor-not-allowed'
                : 'bg-neon-cyan text-black hover:scale-105 active:scale-95'} rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all shadow-lg shadow-neon-cyan/20"
        >
            {!isAAL3Verified ? "SIGN_IN_TO_POST" : "POST_TASK_ORDER"}
        </button>
    </div>
</div>
