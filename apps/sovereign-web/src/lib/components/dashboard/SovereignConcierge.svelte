<script lang="ts">
    import {
        MessageSquare,
        X,
        Send,
        Bot,
        User,

        Sparkles,
        Info,
        ShieldCheck,

        HelpCircle,
        Smile,
        Image as ImageIcon,
        Mic,
        Plus,

        Phone,
        Video,
    } from "lucide-svelte";
    import { fade, fly, slide, scale } from "svelte/transition";

    interface Props {
        isZenMode?: boolean;
    }

    let { isZenMode = false }: Props = $props();
    let isOpen = $state(false);
    let message = $state("");
    let showStickers = $state(false);

    // Kakao-style emotional colors
    const colors = {
        kakaoYellow: "#FAE100",
        kakaoBrown: "#3C1E1E",
        bubbleUser: "#FAE100",
        bubbleBot: "#ffffff",

        softPeach: "#FFD1DC",
        softYellow: "#FFF9C4",
    };

    let chatHistory = $state<
        {
            role: string;
            content: string;
            time: string;
            read: boolean;
            isSticker: boolean;
            type?: string;
        }[]
    >([
        {
            role: "assistant",
            content:
                "Greetings, Citizen! 🌸 I'm your Sovereign Concierge. Ready for some high-velocity coordination?",
            time: "10:00",
            read: true,
            isSticker: false,
        },
    ]);

    const stickers = [
        { id: "happy", emoji: "😊", label: "JOY" },
        { id: "love", emoji: "🥰", label: "LOVE" },
        { id: "zap", emoji: "⚡", label: "ZAP" },
        { id: "moon", emoji: "🌙", label: "MOON" },
        { id: "star", emoji: "✨", label: "STAR" },
        { id: "flower", emoji: "🌸", label: "BLOOM" },
        { id: "green", emoji: "🟢", label: "ZEN" },
    ];

    function sendTransaction(type: string) {
        chatHistory = [
            ...chatHistory,
            {
                role: "assistant",
                content:

                    type === "PAYMENT"
                        ? "AstroTransfer Summary: 125 AGE sent to Alpha_Shard."
                        : "Reservation Confirmed: Shard-Hailing at 14:00Z.",
                time: getCurrentTime(),
                read: true,
                isSticker: false,
                type: type,
            },
        ];
    }

    function sendSticker(sticker: any) {
        chatHistory = [
            ...chatHistory,
            {
                role: "user",
                content: sticker.emoji,
                time: getCurrentTime(),
                read: false,
                isSticker: true,
            },
        ];
        showStickers = false;
        simulateResponse();
    }

    function sendMessage() {
        if (!message) return;
        chatHistory = [
            ...chatHistory,
            {
                role: "user",
                content: message,
                time: getCurrentTime(),
                read: false,
                isSticker: false,
            },
        ];

        const userMsg = message.toLowerCase();
        message = "";
        simulateResponse(userMsg);
    }

    function getCurrentTime() {
        return new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    function simulateResponse(userMsg = "") {
        setTimeout(() => {
            let response = "I'm checking the council archives for you... 💎";
            if (userMsg.includes("transfer") || userMsg.includes("send")) {
                response =
                    "Telemetry indicates 12ms latency. AstroTransfer is green! 🚀";
            }

            chatHistory = [
                ...chatHistory,
                {
                    role: "assistant",
                    content: response,
                    time: getCurrentTime(),
                    read: true,
                    isSticker: false,
                },
            ];

            // Mark user messages as read
            chatHistory = chatHistory.map((m) => ({ ...m, read: true }));
        }, 1200);
    }
</script>

<!-- Concierge Trigger -->
{#if !isOpen}
    <button
        onclick={() => (isOpen = true)}
        in:scale={{ duration: 400 }}
        class="fixed bottom-32 right-12 w-16 h-16 rounded-full {isZenMode
            ? 'bg-[#00B900] text-white shadow-[0_15px_35px_rgba(0,185,0,0.3)]'
            : 'bg-[#FAE100] text-[#3C1E1E] shadow-[0_15px_35px_rgba(250,225,0,0.3)]'} flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-50 group hover:rotate-3"
    >
        <MessageSquare size={28} />
        <div
            class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full border-2 border-[#04060b] flex items-center justify-center text-[8px] text-white font-black animate-bounce"
        >
            1
        </div>
    </button>
{/if}

<!-- Concierge Panel (Kakao Style) -->
{#if isOpen}
    <div
        class="fixed bottom-32 right-12 w-[420px] h-[680px] glass-panel {isZenMode
            ? 'bg-[#F4F7F9] border-black/5 shadow-[0_50px_100px_rgba(0,0,0,0.1)]'
            : 'bg-[#BACEE0] border-white/20 shadow-[0_50px_100px_rgba(0,0,0,0.5)]'} flex flex-col z-50 overflow-hidden rounded-[3rem]"
        in:fly={{ y: 40, duration: 500 }}
        out:fly={{ y: 40, duration: 300 }}
    >
        <!-- Header (K-App Top Bar) -->
        <div
            class="p-6 {isZenMode
                ? 'bg-white/80'
                : 'bg-[#BACEE0]/80'} backdrop-blur-xl border-b border-black/5 flex items-center justify-between z-10"
        >
            <div class="flex items-center gap-4">
                <div
                    class="w-12 h-12 rounded-2xl bg-white border border-black/5 flex items-center justify-center text-[#3C1E1E] shadow-sm"
                >
                    <Bot size={24} />
                </div>
                <div>
                    <h3
                        class="text-sm font-black text-[#3C1E1E] uppercase tracking-tighter"
                    >
                        SOVEREIGN_CONCIERGE
                    </h3>
                    <div class="flex items-center gap-2">
                        <span
                            class="text-[8px] font-bold text-black/40 uppercase tracking-widest"
                            >Global Council Support</span
                        >
                        <div
                            class="px-2 py-0.5 bg-green-500/10 border border-green-500/20 rounded-full flex items-center gap-1"
                        >
                            <ShieldCheck size={8} class="text-green-500" />
                            <span
                                class="text-[6px] font-black text-green-600 uppercase"
                                >E2EE</span
                            >
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <button class="p-2 text-[#3C1E1E]/40 hover:text-[#3C1E1E]"
                    ><Phone size={18} /></button
                >
                <button class="p-2 text-[#3C1E1E]/40 hover:text-[#3C1E1E]"
                    ><Video size={18} /></button
                >
                <button
                    onclick={() => (isOpen = false)}
                    class="p-2 text-[#3C1E1E]/40 hover:text-[#3C1E1E] bg-black/5 rounded-full"
                >
                    <X size={20} />
                </button>
            </div>
        </div>

        <!-- Chat Area (Scrollable Message Plane) -->
        <div
            class="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed"
        >
            <div class="flex justify-center">
                <span
                    class="bg-black/10 text-white/60 text-[8px] font-black uppercase px-4 py-1.5 rounded-full backdrop-blur-sm"
                    >Causal Session: Today</span
                >
            </div>

            {#each chatHistory as msg}
                <div
                    class="flex {msg.role === 'user'
                        ? 'justify-end'
                        : 'justify-start'} group"
                >
                    <div
                        class="max-w-[80%] flex items-end gap-3 {msg.role ===
                        'user'
                            ? 'flex-row-reverse'
                            : ''}"
                    >
                        {#if msg.role === "assistant"}
                            <div
                                class="w-8 h-8 rounded-xl bg-white flex items-center justify-center text-[#3C1E1E] shadow-sm flex-shrink-0"
                            >
                                <Bot size={16} />
                            </div>
                        {/if}

                        <div class="space-y-1">
                            {#if msg.isSticker}
                                <div
                                    class="text-6xl animate-bounce-slow py-2 drop-shadow-lg"
                                >
                                    {msg.content}
                                </div>
                            {:else if msg.type === "PAYMENT"}
                                <div
                                    class="p-6 bg-[#00B900]/5 border border-[#00B900]/20 rounded-3xl space-y-3"
                                    in:scale
                                >
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="w-8 h-8 rounded-xl bg-[#00B900] text-white flex items-center justify-center"
                                        >
                                            <Send size={16} />
                                        </div>
                                        <p
                                            class="text-[10px] font-black text-[#3C1E1E] uppercase"
                                        >
                                            TRANSACTION_SUCCESS
                                        </p>
                                    </div>
                                    <p
                                        class="text-xs font-medium text-[#3C1E1E]/60"
                                    >
                                        {msg.content}
                                    </p>
                                    <button
                                        class="w-full py-2 bg-[#00B900] text-white rounded-lg text-[8px] font-black uppercase"
                                        >View Receipt</button
                                    >
                                </div>
                            {:else if msg.type === "RESERVATION"}
                                <div
                                    class="p-6 bg-blue-500/5 border border-blue-500/20 rounded-3xl space-y-3"
                                    in:scale
                                >
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="w-8 h-8 rounded-xl bg-blue-500 text-white flex items-center justify-center"
                                        >
                                            <Sparkles size={16} />
                                        </div>
                                        <p
                                            class="text-[10px] font-black text-[#3C1E1E] uppercase"
                                        >
                                            RESERVATION_ACTIVE
                                        </p>
                                    </div>
                                    <p
                                        class="text-xs font-medium text-[#3C1E1E]/60"
                                    >
                                        {msg.content}
                                    </p>
                                    <button
                                        class="w-full py-2 bg-blue-500 text-white rounded-lg text-[8px] font-black uppercase"
                                        >Manage</button
                                    >
                                </div>
                            {:else}
                                <div
                                    class="p-4 rounded-[1.5rem] text-[12px] leading-relaxed shadow-sm {msg.role ===
                                    'assistant'
                                        ? 'bg-white text-[#3C1E1E] rounded-tl-none border border-white'
                                        : 'bg-[#FAE100] text-[#3C1E1E] rounded-tr-none border border-yellow-400 font-medium'}"
                                >
                                    {msg.content}
                                </div>
                            {/if}
                        </div>

                        <div
                            class="flex flex-col items-center justify-end gap-1 mb-1 {msg.role ===
                            'user'
                                ? 'items-end'
                                : 'items-start'}"
                        >
                            {#if msg.role === "user"}
                                <span
                                    class="text-[8px] font-black text-white/60 {msg.read
                                        ? 'opacity-0'
                                        : 'opacity-100'}">1</span
                                >
                            {/if}
                            <span
                                class="text-[7px] font-bold text-black/20 uppercase whitespace-nowrap"
                                >{msg.time}</span
                            >
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Sticker Tray (Social Sovereignty) -->
        {#if showStickers}
            <div
                class="p-4 bg-white/90 backdrop-blur-md border-t border-black/5 grid grid-cols-4 gap-4 overflow-y-auto max-h-48"
                in:slide
            >
                {#each stickers as sticker}
                    <button
                        onclick={() => sendSticker(sticker)}
                        class="flex flex-col items-center gap-1 p-2 hover:bg-black/5 rounded-2xl transition-all"
                    >
                        <span class="text-3xl">{sticker.emoji}</span>
                        <span class="text-[6px] font-black text-black/40"
                            >{sticker.label}</span
                        >
                    </button>
                {/each}
            </div>
        {/if}

        <!-- Input Area (K-App Style) -->
        <div class="p-6 bg-white border-t border-black/5 space-y-4">
            <div class="flex items-center gap-3">
                <button class="text-black/30 hover:text-black transition-all"
                    ><Plus size={24} /></button
                >
                <div class="flex-1 relative">
                    <input
                        type="text"
                        placeholder="Express your protocol intent..."
                        bind:value={message}
                        onkeydown={(e: KeyboardEvent) => e.key === "Enter" && sendMessage()}
                        class="w-full bg-black/5 border-none rounded-2xl py-3.5 pl-5 pr-12 text-[12px] focus:outline-none focus:ring-2 focus:ring-[#FAE100]/50 transition-all font-medium text-[#3C1E1E]"
                    />
                    <button
                        onclick={() => (showStickers = !showStickers)}
                        class="absolute right-3 top-1/2 -translate-y-1/2 text-black/20 hover:text-[#3C1E1E] transition-all"
                    >
                        <Smile size={20} />
                    </button>
                </div>
                {#if message}
                    <button
                        onclick={sendMessage}
                        in:scale
                        class="w-11 h-11 bg-[#FAE100] text-[#3C1E1E] rounded-xl flex items-center justify-center hover:scale-105 active:scale-95 transition-all shadow-md"
                    >
                        <Send size={18} />
                    </button>
                {:else}
                    <button
                        class="text-black/30 hover:text-black transition-all"
                        ><Mic size={24} /></button
                    >
                {/if}
            </div>
        </div>
    </div>
{/if}

<style>
    .glass-panel {
        backdrop-filter: blur(80px);
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.05);
        border-radius: 10px;
    }

    @keyframes bounce-slow {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    .animate-bounce-slow {
        animation: bounce-slow 2s infinite ease-in-out;
    }
</style>
