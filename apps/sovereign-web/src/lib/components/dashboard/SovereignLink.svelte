<script lang="ts">
    import {
        Link2,
        ShieldCheck,

        Globe,
        Lock,
        AlertCircle,
        ExternalLink,

        Check,
    } from "lucide-svelte";
    import { fade, fly, scale } from "svelte/transition";

    type Institution = {
        id: string;
        name: string;
        type: string;
        status: "READY" | "CONNECTED" | "VERIFYING";
        logo: string;
    };

    let institutions: Institution[] = $state([
        {
            id: "inst-882",
            name: "Sovereign Gold Reserve",
            type: "Asset Custodian",
            status: "READY",
            logo: "🏛️",
        },
        {
            id: "inst-991",
            name: "Alpha Merit Exchange",
            type: "Liquidity Node",
            status: "CONNECTED",
            logo: "📈",
        },
        {
            id: "inst-114",
            name: "Nexus Identity Shard",
            type: "Verification Protocol",
            status: "VERIFYING",
            logo: "🆔",
        },
        {
            id: "inst-005",
            name: "DeepWealth Canister",
            type: "Yield Aggregator",
            status: "READY",
            logo: "🤖",
        },
    ]);

    let step = $state(1);
    let selectedId = $state<string | null>(null);

    function handleLink() {
        if (!selectedId) return;
        step = 2;
        setTimeout(() => {
            step = 3;
        }, 2000);
    }
</script>

<div class="max-w-4xl mx-auto space-y-8" in:fade>
    <div class="text-center space-y-4">
        <div
            class="inline-flex items-center gap-3 px-4 py-2 bg-neon-cyan/10 border border-neon-cyan/20 rounded-full text-neon-cyan"
        >
            <Link2 size={16} />
            <span class="text-[9px] font-black uppercase tracking-widest"
                >SOVEREIGN_LINK_HANDSHAKE_v1.0</span
            >
        </div>
        <h2 class="text-5xl font-black italic tracking-tighter uppercase">
            ESTABLISH_HANDSHAKE
        </h2>
        <p
            class="text-[12px] mono-font text-white/40 uppercase tracking-[0.4em]"
        >
            Securely link external institutional nodes to your substrate.
        </p>
    </div>

    {#if step === 1}
        <div
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
            in:fly={{ y: 20, duration: 800 }}
        >
            {#each institutions as inst}
                <button
                    onclick={() => (selectedId = inst.id)}
                    class="glass-panel p-8 text-left transition-all group relative overflow-hidden
                    {selectedId === inst.id
                        ? 'border-neon-cyan/50 bg-neon-cyan/[0.03]'
                        : 'border-white/[0.03] bg-black/40 hover:border-white/10'}"
                >
                    <div class="flex justify-between items-start mb-6">
                        <div
                            class="w-14 h-14 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform"
                        >
                            {inst.logo}
                        </div>
                        {#if inst.status === "CONNECTED"}
                            <div
                                class="px-2 py-1 bg-[#24AE7C]/10 border border-[#24AE7C]/20 rounded text-[#24AE7C] text-[7px] font-black uppercase tracking-widest"
                            >
                                ALREADY_CONNECTED
                            </div>
                        {/if}
                    </div>
                    <h3 class="text-lg font-black tracking-tight">
                        {inst.name}
                    </h3>
                    <p
                        class="text-[8px] mono-font text-white/30 uppercase tracking-widest mt-1"
                    >
                        {inst.type}
                    </p>

                    {#if selectedId === inst.id}
                        <div class="absolute bottom-4 right-4" in:scale>
                            <div
                                class="w-6 h-6 rounded-full bg-neon-cyan flex items-center justify-center text-black"
                            >
                                <Check size={14} strokeWidth={4} />
                            </div>
                        </div>
                    {/if}
                </button>
            {/each}
        </div>

        <div class="flex justify-center pt-8">
            <button
                onclick={handleLink}
                disabled={!selectedId}
                class="px-12 py-5 bg-neon-cyan text-black font-black uppercase tracking-tighter text-lg rounded-2xl shadow-[0_0_30px_rgba(0,242,255,0.3)] hover:scale-105 active:scale-95 disabled:opacity-20 disabled:grayscale transition-all"
            >
                INITIATE_HANDSHAKE_PROTOCOL
            </button>
        </div>
    {:else if step === 2}
        <div
            class="glass-panel p-20 flex flex-col items-center text-center space-y-10"
            in:scale
        >
            <div class="relative">
                <div
                    class="w-32 h-32 border-4 border-neon-cyan/20 border-t-neon-cyan rounded-full animate-spin"
                ></div>
                <div class="absolute inset-0 flex items-center justify-center">
                    <ShieldCheck
                        size={40}
                        class="text-neon-cyan animate-pulse"
                    />
                </div>
            </div>
            <div>
                <h3
                    class="text-2xl font-black italic tracking-tighter uppercase"
                >
                    VERIFYING_CAUSAL_ORIGIN...
                </h3>
                <p
                    class="text-[10px] mono-font text-white/30 uppercase tracking-[0.3em] mt-4"
                >
                    Establishing secure AAL3 tunnel to {institutions.find(
                        (i) => i.id === selectedId,
                    )?.name}
                </p>
            </div>

            <div
                class="w-full max-w-xs h-1 bg-white/5 rounded-full overflow-hidden"
            >
                <div
                    class="h-full bg-neon-cyan animate-[progress_2s_ease-in-out]"
                ></div>
            </div>
        </div>
    {:else if step === 3}
        <div
            class="glass-panel p-20 flex flex-col items-center text-center space-y-8"
            in:fly={{ y: -20 }}
        >
            <div
                class="w-24 h-24 bg-[#24AE7C]/20 border-2 border-[#24AE7C] rounded-full flex items-center justify-center text-[#24AE7C] animate-bounce"
            >
                <Check size={48} strokeWidth={4} />
            </div>
            <div>
                <h3
                    class="text-4xl font-black italic tracking-tighter uppercase text-[#24AE7C]"
                >
                    HANDSHAKE_COMPLETE
                </h3>
                <p
                    class="text-[12px] mono-font text-white/40 uppercase tracking-[0.4em] mt-4"
                >
                    Node successfully integrated into your Sovereign Substrate.
                </p>
            </div>
            <div
                class="p-6 bg-white/5 border border-white/10 rounded-2xl flex items-center gap-4 text-left"
            >
                <div
                    class="w-12 h-12 bg-white/5 border border-white/10 rounded-xl flex items-center justify-center text-white/40"
                >
                    <Lock size={20} />
                </div>
                <div>
                    <span
                        class="text-[7px] font-black text-white/20 uppercase tracking-widest block mb-1"
                        >NODE_AUTHENTICATION_KEY</span
                    >
                    <span class="text-xs mono-font font-bold"
                        >AGE_LINK_TXN_8829_XXXX_4421</span
                    >
                </div>
            </div>
            <button
                onclick={() => (step = 1)}
                class="px-8 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all"
            >
                RETURN_TO_OVERVIEW
            </button>
        </div>
    {/if}

    <div
        class="glass-panel p-6 bg-black/40 border-white/[0.03] flex items-center gap-6"
    >
        <div class="p-3 bg-amber-400/10 rounded-xl text-amber-400">
            <AlertCircle size={24} />
        </div>
        <div>
            <span
                class="text-[8px] font-black uppercase tracking-[0.2em] text-white/60 block"
                >Sovereign_Security_Notice</span
            >
            <p class="text-[10px] text-white/30 leading-relaxed max-w-lg mt-1">
                Linking an institutional node grants the AGE Protocol permission
                to monitor and execute agentic intent on your behalf. Ensure
                that you have reviewed the **Protocol Spec Sheet** for each
                institution before proceeding.
            </p>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 2.5rem;
    }

    @keyframes progress {
        0% {
            width: 0;
        }
        100% {
            width: 100%;
        }
    }
</style>
