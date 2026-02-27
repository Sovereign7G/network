<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fly, scale } from "svelte/transition";
    import {
        Fingerprint,
        QrCode,
        Cpu,
        CreditCard,
        ShieldCheck,
        Zap,
        Smartphone,
        Wifi,
        Lock,
        Globe,
    } from "lucide-svelte";

    let activeTab = $state("passport");
    let isNfcScanning = $state(false);
    let nfcSuccess = $state(false);

    function simulateNfc() {
        isNfcScanning = true;
        nfcSuccess = false;
        setTimeout(() => {
            isNfcScanning = false;
            nfcSuccess = true;
            manifold.recordEvent(
                "NFC_LINK_SUCCESS",
                "Physical AGE Key synchronized via NFC.",
            );
            setTimeout(() => (nfcSuccess = false), 3000);
        }, 2000);
    }

    const creditMetas = [
        { label: "Stability", value: 98, color: "text-emerald-400" },
        { label: "Velocity", value: 74, color: "text-cyan-400" },
        { label: "Heritage", value: 92, color: "text-purple-400" },
    ];
</script>

<div
    class="h-full bg-zinc-950/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden flex flex-col shadow-2xl relative group"
>
    <!-- Navigation Tabs -->
    <div class="flex border-b border-white/5 bg-white/[0.02]">
        {#each ["passport", "payments", "hardware"] as tab}
            <button
                onclick={() => (activeTab = tab)}
                class="flex-1 py-4 text-[9px] font-black uppercase tracking-[0.2em] transition-all relative {activeTab ===
                tab
                    ? 'text-cyan-400'
                    : 'text-white/20 hover:text-white/40'}"
            >
                {tab}
                {#if activeTab === tab}
                    <div
                        class="absolute bottom-0 left-0 w-full h-0.5 bg-cyan-400"
                        in:scale
                    ></div>
                {/if}
            </button>
        {/each}
    </div>

    <div class="flex-1 p-8 overflow-y-auto no-scrollbar">
        {#if activeTab === "passport"}
            <div class="space-y-8" in:fly={{ y: 10 }}>
                <!-- DID Identity Header -->
                <div class="flex items-center gap-6">
                    <div
                        class="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-400/20 to-blue-600/20 border border-cyan-400/30 flex items-center justify-center relative"
                    >
                        <Fingerprint size={32} class="text-cyan-400" />
                        <div
                            class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-zinc-950"
                        ></div>
                    </div>
                    <div>
                        <h3
                            class="text-lg font-black text-white leading-tight italic"
                        >
                            Sovereign_Passport
                        </h3>
                        <div class="flex items-center gap-2 mt-1">
                            <span
                                class="text-[8px] font-black text-emerald-400 uppercase tracking-widest"
                                >AAL3 Verified</span
                            >
                            <span class="text-white/10 text-[8px]">•</span>
                            <span
                                class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                                >Global Mobility: ACTIVE</span
                            >
                        </div>
                    </div>
                </div>

                <!-- Credit Resonance Gauge -->
                <div
                    class="p-6 bg-white/[0.03] rounded-[2rem] border border-white/5 space-y-4"
                >
                    <div class="flex justify-between items-center">
                        <span
                            class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                            >Credit_Resonance</span
                        >
                        <span
                            class="text-xl font-black text-cyan-400 tracking-tighter italic"
                            >842.1</span
                        >
                    </div>
                    <div
                        class="h-1.5 bg-white/5 rounded-full overflow-hidden flex gap-0.5"
                    >
                        <div
                            class="h-full bg-cyan-400 w-[84%]"
                            style="box-shadow: 0 0 15px rgba(34,211,238,0.4)"
                        ></div>
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        {#each creditMetas as meta}
                            <div class="flex flex-col items-center">
                                <span
                                    class="text-[7px] font-black text-white/20 uppercase mb-1"
                                    >{meta.label}</span
                                >
                                <span class="text-xs font-black {meta.color}"
                                    >{meta.value}%</span
                                >
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- DIDs & Credentials -->
                <div class="space-y-3">
                    <div
                        class="p-4 bg-black/40 rounded-2xl border border-white/5 flex items-center justify-between group/row"
                    >
                        <div class="flex items-center gap-3">
                            <ShieldCheck size={14} class="text-emerald-400" />
                            <span class="text-[10px] font-bold text-white/60"
                                >Biometric_Hash</span
                            >
                        </div>
                        <span class="text-xs font-mono text-white/20"
                            >0xfD...99E1</span
                        >
                    </div>
                    <div
                        class="p-4 bg-black/40 rounded-2xl border border-white/5 flex items-center justify-between group/row"
                    >
                        <div class="flex items-center gap-3">
                            <Globe size={14} class="text-purple-400" />
                            <span class="text-[10px] font-bold text-white/60"
                                >Causal_Visa</span
                            >
                        </div>
                        <span
                            class="text-[8px] font-black text-purple-400 uppercase tracking-widest px-2 py-1 bg-purple-400/5 rounded border border-purple-400/20"
                            >Priority_Pass</span
                        >
                    </div>
                </div>
            </div>
        {:else if activeTab === "payments"}
            <div
                class="space-y-8 h-full flex flex-col items-center justify-center text-center"
                in:fly={{ y: 10 }}
            >
                <!-- Dynamic QR -->
                <div class="relative group cursor-pointer">
                    <div
                        class="absolute -inset-8 bg-cyan-400/5 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity"
                    ></div>
                    <div class="w-48 h-48 bg-white p-4 rounded-3xl relative">
                        <QrCode size={160} class="text-black" />
                        <div
                            class="absolute inset-0 flex items-center justify-center"
                        >
                            <div
                                class="w-12 h-12 bg-zinc-950 rounded-xl border-4 border-white flex items-center justify-center"
                            >
                                <span
                                    class="text-[10px] font-black text-cyan-400"
                                    >AGE</span
                                >
                            </div>
                        </div>
                    </div>
                </div>

                <div class="space-y-2">
                    <h4
                        class="text-xl font-black italic tracking-tighter uppercase"
                    >
                        SCAN_TO_RECEIVE
                    </h4>
                    <p
                        class="text-[10px] font-black text-white/20 uppercase tracking-[0.3em]"
                    >
                        Resonance-Backed Instant Settlements
                    </p>
                </div>

                <div class="w-full grid grid-cols-2 gap-4">
                    <button
                        class="bg-white/5 hover:bg-white/10 border border-white/5 p-4 rounded-2xl transition-all group/btn"
                    >
                        <CreditCard
                            size={20}
                            class="text-cyan-400 mx-auto mb-2 transition-transform group-hover/btn:-translate-y-1"
                        />
                        <span
                            class="text-[8px] font-black text-white/40 uppercase block tracking-widest"
                            >Share_Link</span
                        >
                    </button>
                    <button
                        class="bg-white/5 hover:bg-white/10 border border-white/5 p-4 rounded-2xl transition-all group/btn"
                    >
                        <Smartphone
                            size={20}
                            class="text-purple-400 mx-auto mb-2 transition-transform group-hover/btn:-translate-y-1"
                        />
                        <span
                            class="text-[8px] font-black text-white/40 uppercase block tracking-widest"
                            >Request_Pay</span
                        >
                    </button>
                </div>
            </div>
        {:else if activeTab === "hardware"}
            <div class="space-y-8" in:fly={{ y: 10 }}>
                <!-- NFC Hub -->
                <div
                    class="p-10 bg-black/40 rounded-[2.5rem] border border-white/5 flex flex-col items-center justify-center relative overflow-hidden group/nfc"
                >
                    <div
                        class="absolute inset-0 bg-gradient-to-b from-cyan-400/5 to-transparent opacity-0 group-hover/nfc:opacity-100 transition-opacity"
                    ></div>

                    {#if isNfcScanning}
                        <div
                            class="space-y-6 flex flex-col items-center"
                            in:scale
                        >
                            <div class="relative">
                                <div
                                    class="w-24 h-24 border-4 border-cyan-400/20 border-t-cyan-400 rounded-full animate-spin"
                                ></div>
                                <div
                                    class="absolute inset-0 flex items-center justify-center"
                                >
                                    <Wifi
                                        size={32}
                                        class="text-cyan-400 animate-pulse"
                                    />
                                </div>
                            </div>
                            <span
                                class="text-[10px] font-black text-cyan-400 uppercase tracking-[0.4em]"
                                >Establishing_Link...</span
                            >
                        </div>
                    {:else if nfcSuccess}
                        <div
                            class="space-y-6 flex flex-col items-center"
                            in:scale
                        >
                            <div
                                class="w-24 h-24 bg-emerald-400/20 border-2 border-emerald-400 rounded-full flex items-center justify-center"
                            >
                                <ShieldCheck
                                    size={40}
                                    class="text-emerald-400"
                                />
                            </div>
                            <span
                                class="text-[10px] font-black text-emerald-400 uppercase tracking-[0.4em]"
                                >Hardware_Synced</span
                            >
                        </div>
                    {:else}
                        <div class="space-y-6 flex flex-col items-center">
                            <div
                                class="w-24 h-24 bg-white/5 border border-white/10 rounded-full flex items-center justify-center text-white/20 group-hover/nfc:text-cyan-400 transition-colors"
                            >
                                <Smartphone size={40} />
                            </div>
                            <button
                                onclick={simulateNfc}
                                class="px-8 py-3 bg-white text-black text-[10px] font-black uppercase tracking-widest rounded-xl hover:scale-105 active:scale-95 transition-all shadow-xl"
                            >
                                Scan_AGE_Key
                            </button>
                            <span
                                class="text-[8px] font-black text-white/20 uppercase tracking-[0.2em]"
                                >Hold device near NFC sensor</span
                            >
                        </div>
                    {/if}
                </div>

                <!-- hardware devices -->
                <div class="space-y-3">
                    <div
                        class="p-4 bg-white/[0.02] rounded-2xl border border-white/5 flex items-center justify-between opacity-60"
                    >
                        <div class="flex items-center gap-3">
                            <Cpu size={14} />
                            <span class="text-[10px] font-bold"
                                >Ledger Nano X</span
                            >
                        </div>
                        <div class="flex items-center gap-2">
                            <span
                                class="text-[7px] font-black text-white/40 uppercase"
                                >Offline</span
                            >
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-white/20"
                            ></div>
                        </div>
                    </div>
                    <div
                        class="p-4 bg-white/[0.02] rounded-2xl border border-white/5 flex items-center justify-between"
                    >
                        <div class="flex items-center gap-3">
                            <Lock size={14} class="text-cyan-400" />
                            <span class="text-[10px] font-bold"
                                >AGE_HARDWARE_NODE</span
                            >
                        </div>
                        <div class="flex items-center gap-2">
                            <span
                                class="text-[7px] font-black text-cyan-400 uppercase"
                                >Linked</span
                            >
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <!-- Quick Footer -->
    <div
        class="p-6 border-t border-white/5 bg-black/40 flex items-center justify-between"
    >
        <div class="flex items-center gap-2">
            <Zap size={14} class="text-amber-400" />
            <span
                class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                >Protocol Trust: NOMINAL</span
            >
        </div>
        <div class="flex -space-x-1">
            {#each Array(3) as _}
                <div
                    class="w-6 h-6 rounded-full border border-zinc-950 bg-white/10 backdrop-blur-md"
                ></div>
            {/each}
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
</style>
