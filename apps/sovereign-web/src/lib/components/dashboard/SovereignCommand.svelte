<script lang="ts">
    import {
        Shield,
        Lock,
        Fingerprint,
        Eye,

        Zap,
        Activity,
        Key,

        ShieldCheck,
        Terminal,
        History,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    let authPinActive = $state(true);

    let signPinActive = $state(true);
    let biometricStatus = $state("VERIFIED");


    const auditLogs = [

        {
            time: "10:24:55",
            subject: "REVENUE SERVICE",
            action: "TAX_DATA_PULL",
            status: "ALLOWED",
        },
        {
            time: "09:12:10",
            subject: "AGE_BRIDGE_0xFD",
            action: "PKI_ATTESTATION",
            status: "SUCCESS",
        },
        {
            time: "Yesterday",
            subject: "CINEMA_PROTOCOL",
            action: "VOCAL_DNA_VERIFY",
            status: "ALLOWED",
        },
        {
            time: "2 days ago",
            subject: "MINISTRY_OF_TRUTH",
            action: "ID_RE_SYNC",
            status: "SUCCESS",
        },
    ];

    const eIdMetrics = [
        {
            label: "QES Level",
            value: "QUALIFIED (EIDAS)",
            color: "text-purple-400",
        },
        { label: "Trust Score", value: "99.8/100", color: "text-neon-cyan" },
        { label: "Data Residencies", value: "14 SHARDS", color: "text-white" },
    ];
</script>

<div class="grid grid-cols-1 lg:grid-cols-12 gap-8" in:fade>
    <!-- Left: Identity Overview -->
    <div class="lg:col-span-8 space-y-8">
        <section
            class="glass-panel p-10 relative overflow-hidden bg-gradient-to-br from-purple-500/10 to-transparent"
        >
            <div class="absolute top-0 right-0 p-10 opacity-5">
                <Shield size={200} />
            </div>

            <div
                class="flex flex-col md:flex-row gap-10 items-start md:items-center relative z-10"
            >
                <div class="relative">
                    <div
                        class="w-32 h-32 rounded-3xl border border-purple-500/30 bg-purple-500/5 flex items-center justify-center"
                    >
                        <Fingerprint size={64} class="text-purple-400" />
                    </div>
                    <div
                        class="absolute -bottom-2 -right-2 bg-green-500 w-8 h-8 rounded-full border-4 border-[#020408] flex items-center justify-center"
                    >
                        <ShieldCheck size={14} class="text-white" />
                    </div>
                </div>

                <div class="space-y-2">
                    <div class="flex items-center gap-3">
                        <h2
                            class="text-4xl font-black tracking-tighter uppercase italic"
                        >
                            Sovereign <span class="text-purple-400">eID</span>
                        </h2>
                        <span
                            class="px-3 py-1 bg-purple-500/20 border border-purple-500/40 rounded-full text-[10px] font-black uppercase text-purple-400 tracking-widest"
                            >v12.0 HARDENED</span
                        >
                    </div>
                    <p
                        class="text-white/40 text-sm mono-font uppercase tracking-widest"
                    >
                        Digital Resident ID: 0xFD_7782_99A1_22C0
                    </p>
                    <div class="flex gap-4 pt-4">
                        {#each eIdMetrics as metric}
                            <div class="flex flex-col gap-1">
                                <span
                                    class="text-[8px] font-black text-white/30 uppercase tracking-tighter"
                                    >{metric.label}</span
                                >
                                <span
                                    class="text-xs font-black mono-font {metric.color}"
                                    >{metric.value}</span
                                >
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </section>

        <!-- Security Controls -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="glass-panel p-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3
                        class="text-xs font-black uppercase tracking-[0.2em] text-white/40"
                    >
                        TWO-PIN ARCHITECTURE
                    </h3>
                    <Lock size={14} class="text-white/20" />
                </div>
                <div class="space-y-4">
                    <div
                        class="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5"
                    >
                        <div class="flex items-center gap-4">
                            <Key size={18} class="text-neon-cyan" />
                            <div class="flex flex-col">
                                <span class="text-[10px] font-black uppercase"
                                    >Authentication PIN</span
                                >
                                <span
                                    class="text-[8px] mono-font text-white/30 uppercase"
                                    >0xFD Login Active</span
                                >
                            </div>
                        </div>
                        <div
                            class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]"
                        ></div>
                    </div>
                    <div
                        class="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5"
                    >
                        <div class="flex items-center gap-4">
                            <Zap size={18} class="text-purple-400" />
                            <div class="flex flex-col">
                                <span class="text-[10px] font-black uppercase"
                                    >Signing PIN (QES)</span
                                >
                                <span
                                    class="text-[8px] mono-font text-white/30 uppercase"
                                    >Legal Signature Enabled</span
                                >
                            </div>
                        </div>
                        <div
                            class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]"
                        ></div>
                    </div>
                </div>
            </div>

            <div class="glass-panel p-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3
                        class="text-xs font-black uppercase tracking-[0.2em] text-white/40"
                    >
                        Hardware Attestation
                    </h3>
                    <Terminal size={14} class="text-white/20" />
                </div>
                <div
                    class="p-6 bg-black/40 border border-white/5 rounded-2xl space-y-4"
                >
                    <div
                        class="flex justify-between items-center text-[10px] mono-font"
                    >
                        <span class="text-white/40 uppercase"
                            >Root Authority</span
                        >
                        <span class="text-neon-cyan">AGE_SILICON_V3</span>
                    </div>
                    <div
                        class="flex justify-between items-center text-[10px] mono-font"
                    >
                        <span class="text-white/40 uppercase"
                            >Enclave Integrity</span
                        >
                        <span class="text-green-400 italic font-black"
                            >UNBROKEN</span
                        >
                    </div>
                    <div
                        class="flex justify-between items-center text-[10px] mono-font"
                    >
                        <span class="text-white/40 uppercase"
                            >Biometric Match</span
                        >
                        <span class="text-white">99.9% PROBABILITY</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Right: Audit Logs & Activity -->
    <div class="lg:col-span-4 space-y-8">
        <section class="glass-panel p-8 h-full flex flex-col">
            <div class="flex items-center justify-between mb-8">
                <h3
                    class="text-xs font-black uppercase tracking-[0.2em] text-white/40 flex items-center gap-2"
                >
                    <History size={14} />
                    Data Access Audit
                </h3>
            </div>

            <div class="space-y-6 flex-1">
                {#each auditLogs as log}
                    <div
                        class="relative pl-6 border-l border-white/5 pb-6 last:pb-0"
                    >
                        <div
                            class="absolute left-[-5px] top-0 w-2.5 h-2.5 rounded-full bg-white/10 border border-[#020408]"
                        ></div>
                        <div class="flex flex-col gap-1">
                            <div class="flex justify-between items-center">
                                <span
                                    class="text-[10px] font-black uppercase tracking-widest"
                                    >{log.subject}</span
                                >
                                <span class="text-[8px] mono-font text-white/30"
                                    >{log.time}</span
                                >
                            </div>
                            <span
                                class="text-[9px] mono-font text-white/50 uppercase"
                                >{log.action}</span
                            >
                            <span
                                class="text-[7px] font-bold text-green-400 mt-1 flex items-center gap-1 uppercase"
                            >
                                <ShieldCheck size={10} />
                                {log.status}
                            </span>
                        </div>
                    </div>
                {/each}
            </div>

            <button
                class="w-full mt-8 py-4 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/5 transition-all mb-auto"
            >
                VIEW FULL CAUSAL HISTORY
            </button>
        </section>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
    }
</style>
