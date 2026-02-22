<script lang="ts">
    interface Props {
        isZenMode?: boolean;
    }

    let { isZenMode = false }: Props = $props();

    const posts = [
        {
            user: "Alpha_Shard",
            content: "Protocol update successful. Stability at 99.9%. 🟢",
            type: "Status",
        },
        {
            user: "Citizen_07",
            content: "Incredible speed on the new AstroTransfer paths!",
            type: "Video",
        },
        {
            user: "Market_Watch",
            content: "Agora volume hits 2M MERIT. 📈",
            type: "News",
        },
    ];
</script>

<section
    class="glass-panel p-8 {isZenMode
        ? 'bg-white border-black/5'
        : 'bg-white/5 border-white/5'} space-y-6"
>
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
            <span class="w-1.5 h-6 bg-[#00B900] rounded-full"></span>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] {isZenMode
                    ? 'text-[#3C1E1E]'
                    : 'text-white'}"
            >
                SOVEREIGN_VOOM
            </h3>
        </div>
        <span class="text-[7px] font-bold text-[#00B900] uppercase"
            >Trending_Now</span
        >
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {#each posts as post}
            <div
                class="p-5 {isZenMode
                    ? 'bg-[#F9FAFB] border-black/5'
                    : 'bg-white/5 border-white/5'} border rounded-2xl space-y-3 hover:scale-[1.02] transition-all cursor-pointer"
            >
                <div class="flex items-center gap-2">
                    <div
                        class="w-6 h-6 rounded-full bg-gradient-to-br from-green-400 to-blue-500"
                    ></div>
                    <span
                        class="text-[8px] font-black uppercase {isZenMode
                            ? 'text-[#3C1E1E]'
                            : 'text-white'}">{post.user}</span
                    >
                </div>
                <p
                    class="text-[10px] {isZenMode
                        ? 'text-[#3C1E1E]/60'
                        : 'text-white/60'} leading-relaxed"
                >
                    {post.content}
                </p>
                <div class="flex items-center gap-3">
                    <span class="text-[6px] font-bold text-[#00B900] uppercase"
                        >{post.type}</span
                    >
                </div>
            </div>
        {/each}
    </div>
</section>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
