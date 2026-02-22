<script lang="ts">
    import { Zap } from "lucide-svelte";

    const activities = [
        {
            id: 1,
            title: "Merit Consensus Reached",
            canister: "vu5yx-...-cai",
            amount: "+450 ARI",
            time: "2m ago",
        },
        {
            id: 2,
            title: "Merit Consensus Reached",
            canister: "vu5yx-...-cai",
            amount: "+450 ARI",
            time: "2m ago",
        },
        {
            id: 3,
            title: "Merit Consensus Reached",
            canister: "vu5yx-...-cai",
            amount: "+450 ARI",
            time: "2m ago",
        },
        {
            id: 4,
            title: "Merit Consensus Reached",
            canister: "vu5yx-...-cai",
            amount: "+450 ARI",
            time: "2m ago",
        },
        {
            id: 5,
            title: "Merit Consensus Reached",
            canister: "vu5yx-...-cai",
            amount: "+450 ARI",
            time: "2m ago",
        },
    ];
</script>

<div class="space-y-4">
    {#each activities as activity}
        <div
            class="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5 hover:bg-white/10 transition-all cursor-pointer group"
        >
            <div class="flex items-center gap-4">
                <div
                    class="w-10 h-10 rounded-full bg-neon-cyan/10 flex items-center justify-center text-neon-cyan group-hover:scale-110 transition-transform"
                >
                    <Zap size={18} />
                </div>
                <div>
                    <div class="text-sm font-black">
                        {activity.title}
                    </div>
                    <div class="text-[10px] text-white/30 mono-font">
                        Canister: {activity.canister}
                    </div>
                </div>
            </div>
            <div class="text-right">
                <div class="text-sm font-black text-green-400">
                    {activity.amount}
                </div>
                <div class="text-[10px] text-white/30 uppercase">
                    {activity.time}
                </div>
            </div>
        </div>
    {/each}
</div>
