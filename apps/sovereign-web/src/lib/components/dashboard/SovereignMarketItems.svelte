<script lang="ts">
    import {
        Star,
        Bookmark,
        Zap,
        ShieldCheck,
        ArrowRight,
        Sparkles,
    } from "lucide-svelte";

    interface Props {
        items: any[];
        onSelect: (id: string) => void;
    }

    let { items, onSelect }: Props = $props();
</script>

<div class="space-y-6">
    {#each items as item}
        {@const Icon = item.icon}
        <div
            class="glass-panel p-8 group hover:bg-white/[0.03] transition-all border border-white/5 hover:border-white/20 cursor-pointer relative overflow-hidden"
        >
            <div class="flex flex-col md:flex-row gap-8 relative z-10">
                <!-- High-Quality Product Presentation (360 Proxy) -->
                <div
                    class="w-32 h-32 md:w-48 md:h-48 rounded-[2rem] bg-black border border-white/5 flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 shadow-2xl"
                >
                    <div
                        class="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent"
                    ></div>
                    <div class="relative z-10 {item.color}">
                        <Icon size={64} strokeWidth={1} />
                    </div>
                    <div
                        class="absolute bottom-3 right-3 text-[6px] font-black text-white/20 uppercase tracking-[0.4em] transform rotate-90 origin-right"
                    >
                        SPEC_360
                    </div>
                </div>

                <div class="flex-1 space-y-4">
                    <div class="flex items-start justify-between">
                        <div class="space-y-2">
                            <h4
                                class="text-3xl font-black italic tracking-tighter uppercase leading-none"
                            >
                                {item.title}
                            </h4>
                            <div class="flex items-center gap-3">
                                <span
                                    class="text-[9px] font-black text-neon-cyan uppercase tracking-widest"
                                    >{item.author}</span
                                >
                                <div class="h-3 w-px bg-white/10"></div>
                                <div class="flex items-center gap-1">
                                    {#each Array(5) as _, i}
                                        <Star
                                            size={10}
                                            class={i < Math.floor(item.rating)
                                                ? "text-amber-400"
                                                : "text-white/10"}
                                            fill={i < Math.floor(item.rating)
                                                ? "currentColor"
                                                : "none"}
                                        />
                                    {/each}
                                    <span
                                        class="text-[8px] font-bold text-white/40 uppercase ml-2"
                                        >{item.reviews} VERIFIED PURCHASES</span
                                    >
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button
                                class="p-3 bg-white/5 rounded-xl text-white/20 hover:text-white transition-all"
                            >
                                <Bookmark size={14} />
                            </button>
                        </div>
                    </div>

                    <div class="flex flex-col gap-1">
                        <div class="flex items-baseline gap-3">
                            <span
                                class="text-4xl font-black italic tracking-tighter text-white"
                                >{item.reward}</span
                            >
                            <span
                                class="text-sm font-bold text-white/20 line-through tracking-tighter"
                                >{item.listPrice}</span
                            >
                            <span
                                class="text-[10px] font-black text-neon-cyan uppercase tracking-widest"
                                >SAVE 20%</span
                            >
                        </div>
                        <p
                            class="text-[10px] font-black text-[#24AE7C] uppercase tracking-widest"
                        >
                            {item.delivery}
                        </p>
                    </div>

                    <!-- Causal Bundling (Amazon Style) -->
                    <div
                        class="bg-white/[0.02] border border-white/5 p-4 rounded-xl space-y-2"
                    >
                        <p
                            class="text-[7px] font-black text-white/40 uppercase tracking-[0.2em]"
                        >
                            FREQUENTLY_ANCHORED_TOGETHER
                        </p>
                        <div class="flex items-center gap-3">
                            <div class="flex -space-x-2">
                                <div
                                    class="w-6 h-6 rounded-full bg-neon-cyan/20 border border-neon-cyan/40 flex items-center justify-center"
                                >
                                    <Zap size={10} class="text-neon-cyan" />
                                </div>
                                <div
                                    class="w-6 h-6 rounded-full bg-amber-400/20 border border-amber-400/40 flex items-center justify-center text-amber-400"
                                >
                                    <ShieldCheck size={10} />
                                </div>
                            </div>
                            <span
                                class="text-[8px] font-bold text-white/60 uppercase"
                                >+ BUNDLE_SAVINGS: 15.00 AGE</span
                            >
                        </div>
                    </div>

                    <div
                        class="pt-4 flex items-center justify-between border-t border-white/5"
                    >
                        <div class="flex gap-4">
                            {#each item.badges as badge}
                                <div
                                    class="flex items-center gap-1.5 px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg"
                                >
                                    <ShieldCheck
                                        size={10}
                                        class="text-[#24AE7C]"
                                    />
                                    <span
                                        class="text-[7px] font-black text-white/60 uppercase tracking-widest"
                                        >{badge}</span
                                    >
                                </div>
                            {/each}
                        </div>
                        <div class="flex gap-4">
                            <button
                                onclick={() => onSelect("transfers")}
                                class="px-10 py-5 bg-white text-black rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-neon-cyan transition-all flex items-center gap-3 shadow-[0_0_40px_rgba(255,255,255,0.1)]"
                            >
                                ONE_CLICK_TELEPORT <ArrowRight size={14} />
                            </button>
                            <button
                                class="px-6 py-5 bg-white/[0.02] border border-white/10 rounded-2xl text-[8px] font-black uppercase tracking-widest hover:bg-white/5 transition-all text-white/40 flex items-center gap-2 group/sim"
                            >
                                <Sparkles
                                    size={12}
                                    class="group-hover/sim:text-neon-cyan transition-colors"
                                /> SIMULATE_OUTCOME
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
