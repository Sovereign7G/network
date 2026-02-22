<script lang="ts">
    import { X, Bot } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    interface Props {
        url: string | null;
        onClose: () => void;
    }

    let { url, onClose }: Props = $props();
</script>

{#if url}
    <div
        class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-3xl flex flex-col p-4 md:p-12"
        transition:fade
    >
        <div
            class="flex-1 bg-white rounded-[3rem] overflow-hidden flex flex-col shadow-2xl relative"
            in:fly={{ y: 100 }}
        >
            <!-- WebView Top Bar -->
            <div
                class="h-16 bg-[#F2F2F2] border-b border-black/5 flex items-center justify-between px-8"
            >
                <div class="flex items-center gap-4">
                    <button
                        onclick={onClose}
                        class="p-2 text-black/40 hover:text-black"
                    >
                        <X size={24} />
                    </button>
                    <div class="flex flex-col">
                        <span
                            class="text-[10px] font-black text-black uppercase tracking-tighter"
                            >Partner_Web_Shard</span
                        >
                        <span class="text-[8px] text-black/40 truncate w-48"
                            >{url}</span
                        >
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <div
                        class="px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-lg flex items-center gap-1.5"
                    >
                        <div
                            class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"
                        ></div>
                        <span
                            class="text-[6px] font-black text-green-600 uppercase"
                            >AAL3_AUTO_LOGIN_ACTIVE</span
                        >
                    </div>
                    <button class="p-2 text-black/40"><Bot size={20} /></button>
                </div>
            </div>

            <!-- Virtual Content Area -->
            <div
                class="flex-1 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] p-20 flex flex-col items-center justify-center text-center space-y-10"
            >
                <div
                    class="w-32 h-32 rounded-[2.5rem] bg-black flex items-center justify-center animate-pulse"
                >
                    <Bot size={64} class="text-neon-cyan" />
                </div>
                <div class="max-w-md space-y-4">
                    <h2
                        class="text-3xl font-black italic text-[#3C1E1E] uppercase"
                    >
                        Age_Protocol Gateway
                    </h2>
                    <p
                        class="text-xs font-medium text-[#3C1E1E]/60 leading-relaxed"
                    >
                        Establishing persistent connection to partner substrate.
                        Your UserAgent has been set to <code
                            class="bg-black/5 px-2 py-1 rounded"
                            >SOVEREIGN_OS_V1.20</code
                        > for seamless interaction.
                    </p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div
                        class="p-6 bg-[#FAE100]/10 border border-[#FAE100]/30 rounded-3xl"
                    >
                        <p
                            class="text-[8px] font-black text-[#3C1E1E]/40 uppercase mb-2"
                        >
                            Principal_Identity
                        </p>
                        <p class="text-xs font-bold text-[#3C1E1E]">
                            ryjl3-tyaaa-...-cai
                        </p>
                    </div>
                    <div
                        class="p-6 bg-[#24AE7C]/10 border border-[#24AE7C]/30 rounded-3xl"
                    >
                        <p
                            class="text-[8px] font-black text-[#3C1E1E]/40 uppercase mb-2"
                        >
                            Auth_Status
                        </p>
                        <p class="text-xs font-bold text-[#24AE7C]">
                            SUCCESSFULL_SSO
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}
