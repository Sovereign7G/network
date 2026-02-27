<script lang="ts">
    import {
        Fingerprint,
        ShieldCheck,
        Lock,
        Activity,
        Globe,

        QrCode,
        TrendingUp,
        Plus,

    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    const zkArtifacts = [

        {
            label: "PLANETARY PASSPORT",
            status: "ACTIVE",
            color: "text-cyan-400",
        },
        {
            label: "PROPERTY DEED",
            status: "VERIFIED",
            color: "text-emerald-400",
        },
    ];

    const securitySettings = [
        {
            label: "Two-Factor Auth",
            status: "ENABLED",
            color: "text-amber-400",
            icon: Lock,
        },
        {
            label: "Biometric Key",
            status: "READY",
            color: "text-emerald-400",
            icon: Fingerprint,
        },
    ];
</script>

<div class="px-8 py-12 max-w-6xl mx-auto" in:fade>
    <!-- Briefing Header -->
    <div class="mb-12 flex items-end justify-between">
        <div>
            <div
                class="flex items-center gap-3 text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
            >
                <div
                    class="w-1.5 h-1.5 rounded-full bg-cyan-400 radiant-aura"
                ></div>
                Q-Lattice Synced
            </div>
            <h1
                class="text-6xl font-black italic uppercase tracking-tighter premium-gradient-text"
            >
                Sovereign <span class="text-cyan-400">ID</span>
            </h1>
        </div>
        <div class="flex items-center gap-4 mb-2">
            <div
                class="px-4 py-2 rounded-lg bg-white/5 border border-white/5 flex items-center gap-2"
            >
                <span
                    class="text-[10px] font-black text-white/40 tracking-widest italic uppercase premium-shimmer px-3 py-1 rounded-md"
                    >Trust Resonance: 100%</span
                >
            </div>
        </div>
    </div>

    <!-- Main Operational Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Identity Body -->
        <div class="lg:col-span-2 space-y-8">
            <!-- Dynamic ID Card -->
            <div
                class="glass-panel p-12 relative overflow-hidden group border-cyan-400/20 premium-shimmer"
            >
                <div
                    class="absolute -top-32 -right-32 w-96 h-96 bg-cyan-400/10 blur-[120px] rounded-full"
                ></div>

                <div class="relative z-10">
                    <div class="flex justify-between items-start mb-12">
                        <div>
                            <h2
                                class="text-5xl font-black italic uppercase tracking-tighter mb-2 leading-none premium-gradient-text"
                            >
                                Citizen Zero
                            </h2>
                            <div
                                class="font-mono text-[10px] text-white/20 tracking-widest uppercase"
                            >
                                DID:0xF8E2...D244
                            </div>
                        </div>
                        <div
                            class="px-3 py-1 rounded bg-emerald-500/10 border border-emerald-500/10 text-emerald-400 text-[10px] font-black italic uppercase"
                        >
                            Verified
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-8 mb-12">
                        <div>
                            <div
                                class="text-[8px] font-black text-white/20 tracking-widest uppercase mb-2"
                            >
                                Trust Rank
                            </div>
                            <div
                                class="text-3xl font-black text-cyan-400 italic premium-shimmer inline-block"
                            >
                                A++
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[8px] font-black text-white/20 tracking-widest uppercase mb-2"
                            >
                                Access
                            </div>
                            <div
                                class="text-3xl font-black text-emerald-400 italic"
                            >
                                L4
                            </div>
                        </div>
                        <div class="flex justify-end items-end">
                            <button
                                onclick={() => {}}
                                class="premium-scale w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-cyan-400 transition-all shadow-[0_0_20px_rgba(34,211,238,0.1)]"
                            >
                                <QrCode size={24} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ZK Proof Inventory -->
            <div class="space-y-4">
                <div
                    class="text-[10px] font-black tracking-widest text-white/20 uppercase italic px-2"
                >
                    Credential Inventory
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {#each zkArtifacts as artifact}
                        <div
                            class="premium-scale glass-panel p-6 flex items-center justify-between border-white/5 hover:border-cyan-400/20 transition-all cursor-pointer"
                        >
                            <div class="flex items-center gap-4">
                                <div
                                    class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center"
                                >
                                    <ShieldCheck
                                        size={18}
                                        class="text-cyan-400"
                                    />
                                </div>
                                <div
                                    class="font-black italic uppercase text-sm tracking-tight"
                                >
                                    {artifact.label}
                                </div>
                            </div>
                            <div
                                class="text-[8px] font-black {artifact.color} uppercase tracking-widest"
                            >
                                {artifact.status}
                            </div>
                        </div>
                    {/each}
                    <button
                        class="glass-panel p-6 border-dashed border-white/10 flex items-center justify-center gap-3 text-white/20 hover:text-white/40 hover:border-white/20 transition-all"
                    >
                        <Plus size={16} />
                        <span
                            class="text-[10px] font-black tracking-widest uppercase"
                            >Import Credential</span
                        >
                    </button>
                </div>
            </div>
        </div>

        <!-- Sidebar: Security Intelligence -->
        <div class="space-y-8">
            <div class="glass-panel p-8 space-y-8 border-white/5">
                <div>
                    <div class="flex items-center gap-4 mb-6">
                        <Activity size={16} class="text-cyan-400" />
                        <div
                            class="text-[10px] font-black tracking-widest text-white/40 uppercase"
                        >
                            Operational Security
                        </div>
                    </div>

                    <div class="space-y-6">
                        {#each securitySettings as setting}
                            {@const Icon = setting.icon}
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-3">
                                    <Icon size={16} class="text-white/20" />
                                    <div
                                        class="text-xs font-black italic uppercase text-white/60"
                                    >
                                        {setting.label}
                                    </div>
                                </div>
                                <div
                                    class="text-[8px] font-black {setting.color} uppercase"
                                >
                                    {setting.status}
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <div class="h-px bg-white/5"></div>

                <div>
                    <div
                        class="text-[10px] font-black tracking-widest text-white/20 uppercase mb-4 px-1"
                    >
                        Integrity Log
                    </div>
                    <div
                        class="p-6 rounded-2xl bg-white/[0.02] border border-white/5"
                    >
                        <div
                            class="text-[10px] text-white/40 font-bold leading-relaxed italic mb-4"
                        >
                            Last sync performed 12m ago. No biometric deviations
                            detected in current sector.
                        </div>
                        <div class="flex items-center gap-2">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-emerald-400"
                            ></div>
                            <span
                                class="text-[8px] font-black text-emerald-400 tracking-widest uppercase"
                                >Lattice Synced</span
                            >
                        </div>
                    </div>
                </div>
            </div>

            <button
                class="w-full py-4 rounded-xl bg-white/5 border border-white/5 text-[10px] font-black tracking-widest text-white/30 hover:bg-white/10 hover:text-white transition-all uppercase italic"
            >
                Revoke All Sessions
            </button>
        </div>
    </div>
</div>
