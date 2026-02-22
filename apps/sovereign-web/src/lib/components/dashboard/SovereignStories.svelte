<script lang="ts">
    import { fade, fly, scale } from "svelte/transition";
    import { onMount } from "svelte";

    const stories = [
        {
            id: 1,
            type: "NODES",
            user: "Foundation_Alpha",
            preview:
                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=200&h=300&auto=format&fit=crop",
            viewed: false,
        },
        {
            id: 2,
            type: "GIFT",
            user: "Merit_Giver_0x",
            preview:
                "https://images.unsplash.com/photo-1513151233558-d860c5398176?q=80&w=200&h=300&auto=format&fit=crop",
            viewed: false,
        },
        {
            id: 3,
            type: "SHARD",
            user: "Agora_Merchant",
            preview:
                "https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=200&h=300&auto=format&fit=crop",
            viewed: true,
        },
        {
            id: 4,
            type: "COUNCIL",
            user: "Agentic_Bureau",
            preview:
                "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=200&h=300&auto=format&fit=crop",
            viewed: false,
        },
    ];

    let activeStory = $state<any>(null);

    function viewStory(story: any) {
        activeStory = story;
    }
</script>

<section class="space-y-4">
    <div class="flex items-center justify-between px-2">
        <h4
            class="text-[10px] font-black uppercase tracking-[0.3em] text-white/40"
        >
            Sovereign_Moments
        </h4>
        <button class="text-[8px] font-black text-neon-cyan uppercase"
            >View All</button
        >
    </div>

    <div class="flex gap-4 overflow-x-auto pb-4 px-2 no-scrollbar">
        <!-- My Story Add -->
        <button
            class="flex-shrink-0 w-20 flex flex-col items-center gap-2 group"
        >
            <div
                class="w-20 h-20 rounded-[2rem] border-2 border-dashed border-white/10 flex items-center justify-center group-hover:border-neon-cyan/40 transition-all"
            >
                <div
                    class="w-16 h-16 rounded-[1.5rem] bg-white/5 flex items-center justify-center text-white/40 group-hover:text-white"
                >
                    <span class="text-2xl">+</span>
                </div>
            </div>
            <span
                class="text-[8px] font-bold text-white/20 uppercase tracking-widest"
                >Post</span
            >
        </button>

        {#each stories as story}
            <button
                onclick={() => viewStory(story)}
                class="flex-shrink-0 w-20 flex flex-col items-center gap-2 group"
            >
                <div
                    class="w-20 h-20 rounded-[2rem] p-1 {story.viewed
                        ? 'bg-white/5'
                        : 'bg-gradient-to-tr from-[#FAE100] via-[#FFD1DC] to-[#24AE7C]'} transition-all group-hover:scale-105"
                >
                    <div
                        class="w-full h-full rounded-[1.8rem] overflow-hidden border-2 border-[#04060b] bg-black"
                    >
                        <img
                            src={story.preview}
                            alt={story.user}
                            class="w-full h-full object-crop grayscale group-hover:grayscale-0 transition-all duration-500"
                        />
                    </div>
                </div>
                <span
                    class="text-[8px] font-bold {story.viewed
                        ? 'text-white/20'
                        : 'text-white'} uppercase tracking-tight truncate w-full text-center"
                    >{story.user}</span
                >
            </button>
        {/each}
    </div>
</section>

{#if activeStory}
    <div
        class="fixed inset-0 z-[100] bg-black backdrop-blur-3xl flex items-center justify-center"
        transition:fade
    >
        <button
            onclick={() => (activeStory = null)}
            class="absolute top-10 right-10 text-white/40 hover:text-white z-[110]"
        >
            <span class="text-4xl">×</span>
        </button>

        <div
            class="relative w-full max-w-lg aspect-[9/16] bg-[#04060b] rounded-[3rem] overflow-hidden shadow-[0_0_100px_rgba(36,174,124,0.2)]"
            in:scale
        >
            <img
                src={activeStory.preview}
                alt="Story content"
                class="w-full h-full object-cover"
            />

            <div
                class="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/80 p-10 flex flex-col justify-between"
            >
                <div class="flex items-center gap-4">
                    <div
                        class="w-12 h-12 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 overflow-hidden"
                    >
                        <div
                            class="w-full h-full flex items-center justify-center text-white font-black italic"
                        >
                            {activeStory.user[0]}
                        </div>
                    </div>
                    <div>
                        <p
                            class="font-black italic text-white uppercase tracking-tighter"
                        >
                            {activeStory.user}
                        </p>
                        <p
                            class="text-[8px] font-black text-white/40 uppercase tracking-widest"
                        >
                            {activeStory.type}
                        </p>
                    </div>
                </div>

                <div class="space-y-4">
                    <div
                        class="p-6 bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl"
                    >
                        <p
                            class="text-xs font-medium text-white/90 leading-relaxed"
                        >
                            High-fidelity moment captured in Shard_07 during the
                            Genesis Ritual ceremony. 💎✨
                        </p>
                    </div>
                    <div class="flex gap-4">
                        <input
                            type="text"
                            placeholder="Send an expression..."
                            class="flex-1 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-xs focus:outline-none"
                        />
                        <button
                            class="w-12 h-12 bg-[#FAE100] text-[#3C1E1E] rounded-2xl flex items-center justify-center font-black"
                            >🤍</button
                        >
                    </div>
                </div>
            </div>

            <!-- Progress Bar -->
            <div class="absolute top-4 left-4 right-4 flex gap-1 h-1">
                <div class="flex-1 bg-white rounded-full overflow-hidden">
                    <div class="h-full bg-white/40 animate-progress"></div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }

    @keyframes progress {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }
    .animate-progress {
        animation: progress 5s linear forwards;
    }
</style>
