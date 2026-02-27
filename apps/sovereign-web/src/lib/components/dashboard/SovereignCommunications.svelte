<script module>
    import { Plus } from "lucide-svelte";
</script>

<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
    import {
        Shield,
        Key,
        Zap,
        Cpu,
        Lock,
        Globe,
        Users,
        Send,
        Hash,
        EyeOff,
        Terminal,
        Activity,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type Channel = {
        id: string;
        name: string;
        type: "PUBLIC" | "ENCRYPTED" | "SHARD_LOCKED";
        unread: number;
        participants: number;
        anonymityStrength: number; // 0-100
    };

    type Message = {
        id: string;
        author: string;
        content: string;
        timestamp: string;
        isEncrypted: boolean;
        veracity: number;
    };

    let channels = $state<Channel[]>([
        {
            id: "1",
            name: "Global_Manifold",
            type: "PUBLIC",
            unread: 0,
            participants: 1250,
            anonymityStrength: 45,
        },
        {
            id: "2",
            name: "Silicon_Peace_Accords",
            type: "ENCRYPTED",
            unread: 4,
            participants: 12,
            anonymityStrength: 98,
        },
        {
            id: "3",
            name: "Void_Syndicate_Alpha",
            type: "SHARD_LOCKED",
            unread: 12,
            participants: 5,
            anonymityStrength: 99,
        },
        {
            id: "4",
            name: "Hyper_Regional_Node",
            type: "PUBLIC",
            unread: 0,
            participants: 450,
            anonymityStrength: 60,
        },
    ]);

    let activeChannelId = $state("1");
    let activeChannel = $derived(
        channels.find((c) => c.id === activeChannelId),
    );

    let messages = $state<Message[]>([
        {
            id: "m1",
            author: "did:age:node_88",
            content: "Kernel sync complete. Ready for dispatch.",
            timestamp: "20:30:05",
            isEncrypted: false,
            veracity: 99.9,
        },
        {
            id: "m2",
            author: "Anonymous_Shard",
            content: "Shifting laws to Nagano jurisdiction. All nodes confirm.",
            timestamp: "20:31:12",
            isEncrypted: true,
            veracity: 100,
        },
        {
            id: "m3",
            author: "Planetary_Relay",
            content:
                "High latency detected in the Pacific Shard. Switching to Satellite Link.",
            timestamp: "20:32:45",
            isEncrypted: false,
            veracity: 98.5,
        },
    ]);

    let newMessage = $state("");
    let isJoinModalOpen = $state(false);
    let secretKeyInput = $state("");
    let cpuUsage = $state(0.4); // Homage to Root (Low CPU)
    let memoryUsage = $state(64);

    function sendMessage() {
        if (!newMessage.trim()) return;

        const msg: Message = {
            id: Math.random().toString(36).substr(2, 9),
            author: "Local_Sovereign",
            content: newMessage,
            timestamp: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
            }),
            isEncrypted: activeChannel?.type !== "PUBLIC",
            veracity: 99.9,
        };

        messages = [...messages, msg];
        newMessage = "";
        manifold.recordEvent(
            "COMMS_SEND",
            `Message sharded to ${activeChannel?.name}`,
        );
    }

    function joinShardLockedChannel() {
        if (secretKeyInput.length > 8) {
            isJoinModalOpen = false;
            activeChannelId = "3";
            manifold.recordEvent(
                "SHARD_UNLOCK",
                "Secret key verified. Access granted to Kloak-style channel.",
            );
        }
    }

    onMount(() => {
        // Subtle resource jitter for realism
        const interval = setInterval(() => {
            cpuUsage = 0.35 + Math.random() * 0.1;
            memoryUsage = 60 + Math.floor(Math.random() * 10);
        }, 3000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="h-[600px] bg-zinc-950 rounded-[2.5rem] border border-white/5 overflow-hidden flex flex-col shadow-2xl relative"
>
    <!-- Top Meta HUD -->
    <div
        class="p-6 bg-white/[0.02] border-b border-white/5 flex items-center justify-between gap-4"
    >
        <div class="flex items-center gap-3">
            <div class="p-2 bg-indigo-500/20 rounded-xl text-indigo-400">
                <Globe size={18} />
            </div>
            <div>
                <h2
                    class="text-[10px] font-black uppercase tracking-[0.3em] text-white"
                >
                    Sovereign_Comms
                </h2>
                <div class="flex items-center gap-2">
                    <span
                        class="text-[8px] font-black text-indigo-400 uppercase tracking-widest"
                        >Kloak_Nodes: ACTIVE</span
                    >
                    <div
                        class="w-1 h-1 rounded-full bg-indigo-400 animate-pulse"
                    ></div>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-6">
            <!-- Resource Usage (ROOT Inspiration) -->
            <div class="flex items-center gap-4">
                <div class="text-right">
                    <p
                        class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
                    >
                        Sys_Load
                    </p>
                    <div class="flex items-center gap-2">
                        <Cpu size={10} class="text-emerald-400/40" />
                        <span class="text-[9px] font-mono text-emerald-400"
                            >{cpuUsage.toFixed(2)}%</span
                        >
                    </div>
                </div>
                <div class="text-right">
                    <p
                        class="text-[7px] font-black text-white/20 uppercase tracking-[0.2em]"
                    >
                        Mem_Footprint
                    </p>
                    <div class="flex items-center gap-2">
                        <Zap size={10} class="text-cyan-400/40" />
                        <span class="text-[9px] font-mono text-cyan-400"
                            >{memoryUsage}MB</span
                        >
                    </div>
                </div>
            </div>
            <div class="h-8 w-[1px] bg-white/5"></div>
            <div
                class="p-3 bg-white/5 rounded-2xl text-white/40 hover:text-white transition-colors cursor-pointer"
            >
                <Shield size={16} />
            </div>
        </div>
    </div>

    <div class="flex-1 flex overflow-hidden">
        <!-- Sidebar: Channels (STOAT Inspired Familiarity) -->
        <div class="w-64 border-r border-white/5 bg-black/40 flex flex-col">
            <div class="p-6">
                <h3
                    class="text-[8px] font-black text-white/30 uppercase tracking-[0.3em] mb-4"
                >
                    Jurisdictional_Rooms
                </h3>
                <div class="space-y-1">
                    {#each channels as channel}
                        <button
                            onclick={() => (activeChannelId = channel.id)}
                            class="w-full p-3 rounded-2xl flex items-center justify-between group transition-all {activeChannelId ===
                            channel.id
                                ? 'bg-indigo-500/10 border border-indigo-500/20'
                                : 'hover:bg-white/5 border border-transparent'}"
                        >
                            <div class="flex items-center gap-3">
                                {#if channel.type === "PUBLIC"}
                                    <Hash
                                        size={14}
                                        class={activeChannelId === channel.id
                                            ? "text-indigo-400"
                                            : "text-white/20"}
                                    />
                                {:else if channel.type === "ENCRYPTED"}
                                    <Lock size={14} class="text-emerald-400" />
                                {:else}
                                    <Key size={14} class="text-amber-400" />
                                {/if}
                                <span
                                    class="text-[10px] font-black lowercase tracking-wider {activeChannelId ===
                                    channel.id
                                        ? 'text-white'
                                        : 'text-white/40 group-hover:text-white/70'}"
                                >
                                    {channel.name}
                                </span>
                            </div>
                            {#if channel.unread > 0}
                                <div
                                    class="px-1.5 py-0.5 bg-indigo-500 rounded-md text-[8px] font-black text-white"
                                >
                                    {channel.unread}
                                </div>
                            {/if}
                        </button>
                    {/each}
                </div>
            </div>

            <div class="mt-auto p-6 border-t border-white/5">
                <button
                    onclick={() => (isJoinModalOpen = true)}
                    class="w-full p-3 bg-white/5 border border-white/10 rounded-2xl text-[9px] font-black uppercase tracking-widest text-white/60 hover:text-indigo-400 hover:border-indigo-400/40 transition-all flex items-center justify-center gap-2"
                >
                    <Plus size={14} />
                    Import_Secret_Key
                </button>
            </div>
        </div>

        <!-- Main Chat Area -->
        <div class="flex-1 flex flex-col bg-zinc-950 relative">
            <!-- Chat Header -->
            <div
                class="p-4 px-8 border-b border-white/5 flex items-center justify-between"
            >
                <div class="flex items-center gap-4">
                    <h2
                        class="text-lg font-black italic tracking-tighter text-white uppercase"
                    >
                        {activeChannel?.name}
                    </h2>
                    <div
                        class="flex items-center gap-2 px-2 py-0.5 bg-white/5 rounded-lg"
                    >
                        <Users size={10} class="text-white/20" />
                        <span class="text-[9px] font-mono text-white/40"
                            >{activeChannel?.participants}</span
                        >
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <div class="flex flex-col items-end">
                        <span
                            class="text-[7px] font-black text-white/20 uppercase tracking-widest"
                            >Anonymity_Level</span
                        >
                        <div class="flex items-center gap-2">
                            <div
                                class="w-16 h-1 bg-white/5 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-indigo-500"
                                    style="width: {activeChannel?.anonymityStrength}%"
                                ></div>
                            </div>
                            <span class="text-[9px] font-mono text-indigo-400"
                                >{activeChannel?.anonymityStrength}%</span
                            >
                        </div>
                    </div>
                </div>
            </div>

            <!-- Messages List -->
            <div class="flex-1 overflow-y-auto p-8 space-y-6 scrollbar-hide">
                {#each messages as msg}
                    <div class="flex flex-col gap-1 group" in:fly={{ y: 10 }}>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span
                                    class="text-[9px] font-black text-indigo-400/80 uppercase tracking-widest leading-none"
                                    >{msg.author}</span
                                >
                                <span class="text-[8px] font-mono text-white/10"
                                    >{msg.timestamp}</span
                                >
                            </div>
                            {#if msg.isEncrypted}
                                <div class="flex items-center gap-1">
                                    <EyeOff
                                        size={10}
                                        class="text-emerald-400/40"
                                    />
                                    <span
                                        class="text-[7px] font-black text-emerald-400/40 uppercase"
                                        >ZK_ENCRYPTED</span
                                    >
                                </div>
                            {/if}
                        </div>
                        <p
                            class="text-[11px] leading-relaxed text-white/70 max-w-2xl font-medium tracking-wide"
                        >
                            {msg.content}
                        </p>
                        <div
                            class="flex items-center gap-2 mt-1 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                            <div
                                class="flex items-center gap-1 px-1.5 py-0.5 bg-white/5 rounded-md border border-white/5"
                            >
                                <Activity size={8} class="text-cyan-400" />
                                <span class="text-[7px] font-mono text-white/30"
                                    >V: {msg.veracity}%</span
                                >
                            </div>
                        </div>
                    </div>
                {/each}
            </div>

            <!-- Message Input (KLOAK Style Security) -->
            <div class="p-6 bg-white/[0.02] border-t border-white/5">
                <div class="relative group">
                    <input
                        type="text"
                        bind:value={newMessage}
                        onkeydown={(e: KeyboardEvent) => e.key === "Enter" && sendMessage()}
                        placeholder="Encrypted transmission..."
                        class="w-full bg-black/60 border border-white/10 rounded-2xl py-4 pl-6 pr-24 text-[11px] text-white placeholder:text-white/20 focus:outline-none focus:border-indigo-500/50 transition-all font-medium"
                    />
                    <div
                        class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2"
                    >
                        <button
                            class="p-2 text-white/20 hover:text-white transition-colors"
                        >
                            <Terminal size={14} />
                        </button>
                        <button
                            onclick={sendMessage}
                            class="p-2 px-4 bg-indigo-500 text-white rounded-xl hover:scale-105 active:scale-95 transition-all shadow-xl shadow-indigo-500/20"
                        >
                            <Send size={14} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Secret Key Entry Overlay -->
    {#if isJoinModalOpen}
        <div
            class="absolute inset-0 z-50 flex items-center justify-center p-12"
            transition:fade
        >
            <div
                class="absolute inset-0 bg-black/80 backdrop-blur-md"
                onclick={() => (isJoinModalOpen = false)}
                onkeydown={(e: KeyboardEvent) =>
                    e.key === "Escape" && (isJoinModalOpen = false)}
                role="button"
                tabindex="0"
                aria-label="Close modal"
            ></div>
            <div
                class="relative w-full max-w-md bg-zinc-900 rounded-[2.5rem] border border-white/10 p-10 space-y-8 shadow-2xl"
                transition:scale
            >
                <div class="text-center space-y-4">
                    <div
                        class="w-20 h-20 bg-amber-500/10 rounded-[2rem] border border-amber-500/20 flex items-center justify-center text-amber-500 mx-auto"
                    >
                        <Key size={32} />
                    </div>
                    <h2
                        class="text-2xl font-black italic tracking-tighter uppercase text-white"
                    >
                        Unlock_Node_Shard
                    </h2>
                    <p
                        class="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] leading-relaxed"
                    >
                        To access decentralized comms, input your sharded secret
                        key. Access is sharded, peer-to-peer, and anonymous.
                    </p>
                </div>

                <div class="space-y-4">
                    <div class="relative">
                        <input
                            type="password"
                            bind:value={secretKeyInput}
                            placeholder="KEY_SHARD_ID_XXXXXXXX"
                            class="w-full bg-black/40 border border-white/5 rounded-2xl p-4 text-center font-mono text-sm tracking-[0.3em] text-amber-400 focus:outline-none focus:border-amber-500/50"
                        />
                    </div>
                    <button
                        onclick={joinShardLockedChannel}
                        disabled={secretKeyInput.length < 8}
                        class="w-full py-4 bg-amber-500 text-black text-[10px] font-black uppercase tracking-widest rounded-2xl hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-20 shadow-xl shadow-amber-500/10"
                    >
                        Initialize_Connection
                    </button>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
