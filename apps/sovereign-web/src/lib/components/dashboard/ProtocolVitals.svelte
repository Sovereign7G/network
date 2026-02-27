<script lang="ts">
    import {
        HeartPulse,
        ShieldCheck,
        Zap,
        Activity,

        Thermometer,
        AlertCircle,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    type Vital = {
        label: string;
        value: string;
        unit: string;
        status: "OPTIMAL" | "STABLE" | "TRIAGE";
        trend: "UP" | "DOWN" | "FLAT";
        icon: any;
    };

    const vitals: Vital[] = $state([
        {
            label: "SUBSTRATE_COHERENCE",
            value: "99.98",
            unit: "%",
            status: "OPTIMAL",
            trend: "UP",
            icon: HeartPulse,
        },
        {
            label: "CAUSAL_INTEGRITY",
            value: "0.999",
            unit: "STP",
            status: "OPTIMAL",
            trend: "FLAT",
            icon: ShieldCheck,
        },
        {
            label: "TELEPORTATION_LATENCY",
            value: "12",
            unit: "MS",
            status: "STABLE",
            trend: "DOWN",
            icon: Zap,
        },
        {
            label: "MERIT_REALIZATION_RATE",
            value: "8.4",
            unit: "ARI",
            status: "OPTIMAL",
            trend: "UP",
            icon: Activity,
        },
    ]);

    const statusColors = {
        OPTIMAL: "text-[#24AE7C] bg-[#24AE7C]/10 border-[#24AE7C]/20",
        STABLE: "text-neon-cyan bg-neon-cyan/10 border-neon-cyan/20",
        TRIAGE: "text-red-400 bg-red-400/10 border-red-400/20",
    };
</script>

<div class="glass-panel p-8 space-y-8 bg-black/40 border-white/[0.03]">
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div
                class="w-10 h-10 rounded-xl bg-[#24AE7C]/10 flex items-center justify-center text-[#24AE7C]"
            >
                <Activity size={20} />
            </div>
            <div>
                <h3
                    class="text-[10px] font-black uppercase tracking-[0.3em] text-white/90"
                >
                    PROTOCOL_VITALS
                </h3>
                <p
                    class="text-[7px] mono-font text-white/30 uppercase tracking-widest mt-0.5"
                >
                    Clinical Substrate Monitoring
                </p>
            </div>
        </div>
        <div
            class="px-3 py-1 bg-[#24AE7C]/10 border border-[#24AE7C]/20 rounded-full flex items-center gap-2"
        >
            <div
                class="w-1.5 h-1.5 rounded-full bg-[#24AE7C] animate-pulse"
            ></div>
            <span
                class="text-[7px] font-black text-[#24AE7C] uppercase tracking-[0.1em]"
                >SECURE_AAL3</span
            >
        </div>
    </div>

    <div class="grid grid-cols-1 gap-4">
        {#each vitals as vital}
            {@const Icon = vital.icon}
            <div
                class="p-5 bg-white/[0.01] border border-white/[0.05] rounded-2xl group hover:border-white/10 transition-all relative overflow-hidden"
            >
                <div class="flex justify-between items-start mb-4">
                    <div
                        class="p-2 bg-white/5 rounded-lg text-white/40 group-hover:text-white/80 transition-colors"
                    >
                        <Icon size={16} />
                    </div>
                    <div
                        class="px-2 py-0.5 rounded text-[8px] font-black tracking-widest uppercase {statusColors[
                            vital.status
                        ]}"
                    >
                        {vital.status}
                    </div>
                </div>

                <div class="flex items-baseline gap-2">
                    <span
                        class="text-3xl font-black italic tracking-tighter text-white/90"
                        >{vital.value}</span
                    >
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                        >{vital.unit}</span
                    >
                </div>

                <p
                    class="text-[8px] mono-font text-white/30 uppercase tracking-[0.2em] mt-2"
                >
                    {vital.label}
                </p>

                <!-- Clinical Graph Shimmer (Background) -->
                <div
                    class="absolute bottom-0 right-0 w-32 h-12 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity"
                >
                    <svg viewBox="0 0 100 40" class="w-full h-full">
                        <path
                            d="M0,30 Q10,10 20,30 T40,30 T60,20 T80,35 T100,5"
                            fill="none"
                            class="stroke-[#24AE7C]"
                            stroke-width="2"
                        />
                    </svg>
                </div>
            </div>
        {/each}
    </div>

    <div class="pt-6 border-t border-white/[0.03] space-y-4">
        <div class="flex items-center gap-2 text-white/20">
            <AlertCircle size={10} />
            <span class="text-[7px] font-black uppercase tracking-widest"
                >Diagnostic: All sectors coherent.</span
            >
        </div>
        <button
            class="w-full py-4 border border-[#24AE7C]/20 bg-[#24AE7C]/5 hover:bg-[#24AE7C] hover:text-black transition-all rounded-xl text-[8px] font-black uppercase tracking-[0.4em] text-[#24AE7C]"
        >
            GENERATE_CLINICAL_REPORT
        </button>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(40px);
        border-radius: 2rem;
    }
</style>
