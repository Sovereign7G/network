<script lang="ts">
    import { Briefcase, Zap } from "lucide-svelte";
//     import { fade, fly } from "svelte/transition";

    const roles = [
        { title: "Backplane Architect", yield: "12% NAI", match: 0.98 },
        { title: "Resonance Engineer", yield: "8% NAI", match: 0.85 },
        { title: "Protocol Steward", yield: "15% NAI", match: 0.92 },
    ];
</script>

<div class="space-y-4">
    <h3
        class="text-sm font-black italic text-neon-cyan uppercase tracking-widest"
    >
        Available Missions
    </h3>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {#each roles as role, i}
            <div
                class="glass-panel p-6 hover:border-neon-cyan/40 transition-all cursor-pointer group card-glow"
                in:fly={{ y: 20, delay: i * 100 }}
            >
                <div class="space-y-4">
                    <div class="flex justify-between items-start">
                        <Briefcase
                            size={20}
                            class="text-white/40 group-hover:text-neon-cyan transition-colors"
                        />
                        <div
                            class="px-2 py-0.5 rounded border border-neon-cyan/30 text-neon-cyan bg-neon-cyan/10 text-[10px] font-bold mono-font"
                        >
                            {(role.match * 100).toFixed(0)}% Match
                        </div>
                    </div>
                    <div>
                        <h4 class="font-bold text-white text-lg">
                            {role.title}
                        </h4>
                        <p
                            class="text-[10px] text-white/40 mt-1 uppercase mono-font"
                        >
                            Stewardship Pool
                        </p>
                    </div>
                    <div
                        class="pt-4 flex items-center justify-between border-t border-white/5"
                    >
                        <span
                            class="text-[10px] font-bold text-white/40 uppercase mono-font"
                            >Est. Yield</span
                        >
                        <span class="text-sm font-black text-white italic"
                            >{role.yield}</span
                        >
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
