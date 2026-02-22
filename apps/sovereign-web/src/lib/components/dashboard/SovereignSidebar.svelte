<script lang="ts">
    import { coreTabs, ecosystemTabs } from "$lib/constants/navigation";

    interface Props {
        activeTab: string;
        onSelect: (id: string) => void;
    }

    let { activeTab, onSelect }: Props = $props();

    const sections = [
        { title: "Core Journeys", tabs: coreTabs },
        { title: "Ecosystem Services", tabs: ecosystemTabs },
    ];
</script>

<aside
    class="fixed inset-y-0 left-0 w-80 bg-black/40 border-r border-white/5 backdrop-blur-3xl z-40 hidden xl:flex flex-col p-10 space-y-12"
>
    <div class="flex items-center space-x-3">
        <div
            class="w-10 h-10 bg-neon-cyan/20 border border-neon-cyan/40 flex items-center justify-center rounded-xl"
        >
            <div class="w-4 h-4 bg-neon-cyan rounded-sm animate-pulse"></div>
        </div>
        <span class="text-2xl font-black tracking-tightest uppercase italic"
            >AGE<span class="neon-text"> OS</span></span
        >
    </div>

    <nav class="flex-1 space-y-10 overflow-y-auto pr-2 custom-scrollbar">
        {#each sections as section}
            <div class="space-y-4">
                <div
                    class="text-[9px] font-black tracking-widest text-white/20 uppercase mb-4 ml-6"
                >
                    {section.title}
                </div>
                {#each section.tabs as tab}
                    <button
                        onclick={() => onSelect(tab.id)}
                        class="w-full px-6 py-4 rounded-2xl transition-all flex items-center gap-4 group
                    {activeTab === tab.id
                            ? 'bg-neon-cyan/10 border border-neon-cyan/30 text-neon-cyan shadow-[0_0_20px_rgba(0,242,255,0.1)]'
                            : 'text-white/40 hover:text-white/80 hover:bg-white/5'}"
                    >
                        <tab.icon
                            size={18}
                            class="group-hover:scale-110 transition-transform"
                        />
                        <span
                            class="text-xs font-bold tracking-widest uppercase"
                            >{tab.name}</span
                        >
                    </button>
                {/each}
            </div>
        {/each}
    </nav>

    <div class="pt-8 border-t border-white/5">
        <div
            class="glass-panel p-6 space-y-4 bg-neon-cyan/5 border-neon-cyan/10"
        >
            <div
                class="flex justify-between items-center text-[8px] font-black uppercase tracking-widest text-neon-cyan"
            >
                <span>Substrate Health</span>
                <span>99.8%</span>
            </div>
            <div class="h-1 bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-neon-cyan" style="width: 98.2%"></div>
            </div>
        </div>
    </div>
</aside>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 242, 255, 0.2);
    }
</style>
