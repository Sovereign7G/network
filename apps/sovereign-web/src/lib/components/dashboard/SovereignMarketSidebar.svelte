<script lang="ts">
    import {
        QrCode,
        ArrowRight,
        Gift,
        ShieldCheck,
        ChevronDown,
        Package,
        List,
        Bot,
        Eye,
        Wrench,
        Sparkles,
        Zap,
    } from "lucide-svelte";
    import { scale } from "svelte/transition";
    import SovereignWellbeing from "./SovereignWellbeing.svelte";

    interface Props {
        marketplaceItems: any[];
        onSelect: (id: string) => void;
    }

    let { marketplaceItems, onSelect }: Props = $props();

    let showMyQR = $state(false);
    let envelopeStatus = $state<"IDLE" | "GIFTING" | "SENT">("IDLE");

    async function giftMerit() {
        envelopeStatus = "GIFTING";
        await new Promise((r) => setTimeout(r, 1500));
        envelopeStatus = "SENT";
        setTimeout(() => (envelopeStatus = "IDLE"), 3000);
    }
</script>

<div class="space-y-8">
    <!-- Buy-Box Experience -->
    <section
        class="glass-panel p-10 bg-black/40 border-white/[0.03] space-y-8 relative overflow-hidden"
    >
        <div class="absolute top-0 right-0 p-4">
            <div
                class="px-2 py-1 bg-amber-400 text-black text-[7px] font-black uppercase rounded"
            >
                SOVEREIGN PRIME
            </div>
        </div>

        <div class="space-y-2">
            <h3 class="text-lg font-black italic tracking-tighter uppercase">
                SUBSTRATE_BUY_BOX
            </h3>
            <p
                class="text-[9px] mono-font text-white/40 uppercase tracking-widest"
            >
                Optimize for scaling velocity.
            </p>
        </div>

        <div class="space-y-6">
            <div class="space-y-3 pb-6 border-b border-white/5">
                <button
                    onclick={() => (showMyQR = !showMyQR)}
                    class="w-full flex items-center justify-between p-4 {showMyQR
                        ? 'bg-neon-cyan text-black'
                        : 'bg-white/5 text-white/40'} border border-white/10 rounded-2xl hover:bg-white/10 transition-all group"
                >
                    <div class="flex items-center gap-3">
                        <QrCode
                            size={18}
                            class={showMyQR ? "text-black" : "text-neon-cyan"}
                        />
                        <div class="text-left">
                            <p
                                class="text-[8px] font-black uppercase tracking-widest"
                            >
                                CITIZEN_QR_ID
                            </p>
                            <p
                                class="text-[6px] {showMyQR
                                    ? 'text-black/60'
                                    : 'text-white/40'} uppercase"
                            >
                                {showMyQR
                                    ? "SCANNING_ACTIVE"
                                    : "Instant Peer_Anchoring"}
                            </p>
                        </div>
                    </div>
                    <ArrowRight
                        size={14}
                        class="opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all"
                    />
                </button>

                {#if showMyQR}
                    <div
                        class="p-6 bg-white rounded-3xl flex flex-col items-center gap-4 shadow-[0_0_30px_rgba(255,255,255,0.1)]"
                        transition:scale
                    >
                        <div
                            class="w-40 h-40 bg-black rounded-2xl flex items-center justify-center p-4"
                        >
                            <QrCode size={120} class="text-white" />
                        </div>
                        <p
                            class="text-[8px] font-black text-black uppercase tracking-widest"
                        >
                            ryjl3-tyaaa-...-cai
                        </p>
                    </div>
                {/if}

                <button
                    onclick={giftMerit}
                    disabled={envelopeStatus !== "IDLE"}
                    class="w-full flex items-center justify-between p-4 {envelopeStatus ===
                    'SENT'
                        ? 'bg-green-500/20 border-green-500/40'
                        : 'bg-red-500/5 border-red-500/10'} rounded-2xl hover:bg-red-500/10 transition-all group"
                >
                    <div class="flex items-center gap-3">
                        <Gift
                            size={18}
                            class={envelopeStatus === "SENT"
                                ? "text-green-400"
                                : "text-red-400"}
                        />
                        <div class="text-left">
                            <p
                                class="text-[8px] font-black uppercase tracking-widest {envelopeStatus ===
                                'SENT'
                                    ? 'text-green-400'
                                    : 'text-red-400'}"
                            >
                                {envelopeStatus === "IDLE"
                                    ? "MERIT_ENVELOPE"
                                    : envelopeStatus === "GIFTING"
                                      ? "GIFTING..."
                                      : "MERIT_GIFT_SENT"}
                            </p>
                            <p
                                class="text-[6px] {envelopeStatus === 'SENT'
                                    ? 'text-green-500/40'
                                    : 'text-red-500/40'} uppercase"
                            >
                                {envelopeStatus === "SENT"
                                    ? "CAUSAL_SETTLEMENT_COMPLETE"
                                    : "Social Gifting Logic"}
                            </p>
                        </div>
                    </div>
                    {#if envelopeStatus === "IDLE"}
                        <ArrowRight
                            size={14}
                            class="text-red-400 opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all"
                        />
                    {:else if envelopeStatus === "SENT"}
                        <ShieldCheck size={14} class="text-green-400" />
                    {/if}
                </button>
            </div>

            <div
                class="p-6 bg-neon-cyan/5 border border-neon-cyan/10 rounded-3xl space-y-4"
            >
                <div class="flex justify-between items-center">
                    <span class="text-[9px] font-black text-white/40 uppercase"
                        >PRIME_ANCHOR_EST</span
                    >
                    <span class="text-sm font-black text-neon-cyan italic"
                        >SUB-10MS</span
                    >
                </div>
                <div
                    class="h-0.5 w-full bg-white/5 rounded-full overflow-hidden"
                >
                    <div class="h-full w-2/3 bg-neon-cyan animate-pulse"></div>
                </div>
                <button
                    class="w-full py-4 bg-neon-cyan text-black rounded-2xl text-[10px] font-black uppercase tracking-widest hover:scale-105 transition-all"
                >
                    SET_DEFAULT_ONE_CLICK
                </button>
            </div>

            <div class="space-y-4">
                <div
                    class="flex items-center justify-between text-[10px] font-black uppercase text-white/40"
                >
                    <span>Ship_to_Shard</span>
                    <span class="text-white"
                        >Block_7782 <ChevronDown
                            size={14}
                            class="inline"
                        /></span
                    >
                </div>
                <div
                    class="flex items-center justify-between text-[10px] font-black uppercase text-white/40"
                >
                    <span>Security_Level</span>
                    <span class="text-[#24AE7C]">AAL3_VERIFIED</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Sovereign Channels -->
    <section
        class="glass-panel p-10 bg-[#FAE100]/5 border-[#FAE100]/20 space-y-8"
    >
        <div class="flex items-center justify-between">
            <h3
                class="text-[10px] font-black uppercase tracking-[0.2em] text-[#3C1E1E]"
            >
                SOVEREIGN_CHANNELS
            </h3>
            <div
                class="px-2 py-0.5 bg-[#FAE100] text-[#3C1E1E] text-[7px] font-black rounded"
            >
                ALIM_TALK
            </div>
        </div>
        <div class="space-y-4">
            {#each [{ name: "Age_Protocol_Official", lastMsg: "Your Merit consensus has been anchored.", time: "2m", color: "text-blue-400" }, { name: "Agora_Brand_Drops", lastMsg: "New high-fidelity stickers available! 🌸", time: "1h", color: "text-pink-400" }, { name: "Liquid_Vault_Support", lastMsg: "Handshake successful with Shard_07.", time: "5h", color: "text-green-400" }] as channel}
                <button
                    class="w-full flex items-center gap-4 p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/10 transition-all text-left group"
                >
                    <div
                        class="w-12 h-12 rounded-2xl bg-white flex items-center justify-center text-[#3C1E1E] shadow-sm flex-shrink-0 group-hover:scale-110 transition-all"
                    >
                        <Bot size={20} />
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex justify-between">
                            <p
                                class="text-[9px] font-black uppercase {channel.color}"
                            >
                                {channel.name}
                            </p>
                            <span
                                class="text-[7px] font-bold text-white/20 capitalize"
                                >{channel.time}</span
                            >
                        </div>
                        <p
                            class="text-[8px] font-medium text-white/60 truncate mt-1"
                        >
                            {channel.lastMsg}
                        </p>
                    </div>
                </button>
            {/each}
        </div>
        <button
            class="w-full py-4 bg-[#FAE100] text-[#3C1E1E] rounded-xl text-[8px] font-black uppercase tracking-widest hover:scale-105 active:scale-95 transition-all shadow-lg shadow-yellow-500/10"
        >
            FIND_MORE_CHANNELS
        </button>
    </section>

    <!-- Institutional Q&A -->
    <section class="glass-panel p-10 bg-black/40 border-white/[0.03] space-y-6">
        <h3
            class="text-[10px] font-black uppercase tracking-[0.2em] text-white"
        >
            INSTITUTIONAL_Q&A
        </h3>
        <div class="space-y-6">
            {#each Array(2) as _, i}
                <div class="space-y-2">
                    <div class="flex items-start gap-3">
                        <span class="text-neon-cyan font-black text-xs">Q:</span
                        >
                        <p
                            class="text-[10px] font-bold text-white leading-relaxed uppercase"
                        >
                            HOW_DOES_ALPHA_7_HANDLE_LATENCY_SPIKES?
                        </p>
                    </div>
                    <div class="flex items-start gap-3 pl-4">
                        <span class="text-[#24AE7C] font-black text-xs">A:</span
                        >
                        <p
                            class="text-[9px] text-white/40 leading-relaxed uppercase tracking-widest"
                        >
                            THE_STRATEGY_DEPLOYS_CASCADE_FALLBACKS_ON_QUANTUM_DISSONANCE_SHARDS.
                        </p>
                    </div>
                </div>
            {/each}
        </div>
        <button
            class="w-full py-4 border border-white/5 bg-white/[0.02] hover:bg-white/5 rounded-xl text-[8px] font-black uppercase tracking-widest text-white/40"
        >
            ASK_THE_COUNCIL
        </button>
    </section>

    <!-- Recently Viewed -->
    <section class="glass-panel p-10 bg-black/40 border-white/[0.03] space-y-6">
        <div class="flex items-center justify-between">
            <h3
                class="text-[10px] font-black uppercase tracking-[0.2em] text-white"
            >
                RECENTLY_VIEWED
            </h3>
            <Eye size={14} class="text-white/20" />
        </div>
        <div class="space-y-4">
            {#each marketplaceItems.slice(0, 2) as item}
                {@const HistIcon = item.icon}
                <button
                    class="w-full p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/10 transition-all flex items-center gap-4 text-left group"
                >
                    <div
                        class="w-10 h-10 rounded-xl {item.bg} flex items-center justify-center {item.color} group-hover:scale-110 transition-transform"
                    >
                        <HistIcon size={18} />
                    </div>
                    <div class="flex-1 min-w-0">
                        <p
                            class="text-[9px] font-black uppercase truncate tracking-tighter"
                        >
                            {item.title}
                        </p>
                        <p
                            class="text-[7px] font-bold text-neon-cyan/60 uppercase tracking-widest"
                        >
                            {item.reward} AGE
                        </p>
                    </div>
                </button>
            {/each}
        </div>
    </section>

    <!-- Pending Handshakes -->
    <section class="glass-panel p-10 bg-black/40 border-neon-cyan/20 space-y-6">
        <div class="flex items-center justify-between">
            <h3
                class="text-[10px] font-black uppercase tracking-[0.2em] text-neon-cyan"
            >
                PENDING_HANDSHAKES
            </h3>
            <div
                class="px-2 py-0.5 bg-neon-cyan text-black text-[7px] font-black rounded italic"
            >
                1_ACTIVE
            </div>
        </div>
        <div
            class="p-6 bg-neon-cyan/5 border border-neon-cyan/10 rounded-3xl space-y-3"
        >
            <div class="flex items-center gap-3">
                <Package size={16} class="text-neon-cyan" />
                <span class="text-[9px] font-black uppercase tracking-tight"
                    >Strategy_Teleport_Alpha_7</span
                >
            </div>
            <div
                class="flex justify-between items-center text-[7px] font-bold text-white/40 uppercase"
            >
                <span>EST_ANCHOR</span>
                <span class="text-white">12:45:00Z</span>
            </div>
            <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div class="h-full w-3/4 bg-neon-cyan animate-pulse"></div>
            </div>
        </div>
        <button
            class="w-full py-4 border border-white/10 bg-white/5 hover:bg-white/10 rounded-xl text-[8px] font-black uppercase tracking-widest text-white/60 flex items-center justify-center gap-2"
        >
            <List size={12} /> VIEW_FULL_LOG
        </button>
    </section>

    <SovereignWellbeing />
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }
</style>
