<script lang="ts">
    import {
        Smartphone,
        Monitor,
        ShieldAlert,
        Zap,
        Globe,
        Lock,
        CheckCircle2,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let transmissionHealth = $state(98);
    let telemetryBlockedCount = $state(1420);
    let convergenceScale = $state(0.4); // 0.4 = mobile, 1.0 = desktop

    const auditLogs = [
        {
            id: 1,
            type: "Privacy",
            message: "Nexus_Telemetry_Intercepted",
            status: "Blocked",
        },
        {
            id: 2,
            type: "Scale",
            message: "Cinnamon_Mobile_Scaling_Applied",
            status: "Active",
        },
        {
            id: 3,
            type: "Kernel",
            message: "FOSS_Integrity_Verified",
            status: "Secure",
        },
        {
            id: 4,
            type: "Liability",
            message: "Fault_Sovereignty_Signed",
            status: "Acknowledged",
        },
    ];

    onMount(() => {
        const interval = setInterval(() => {
            transmissionHealth = Math.min(
                100,
                Math.max(90, transmissionHealth + (Math.random() - 0.5)),
            );
            telemetryBlockedCount += Math.floor(Math.random() * 3);
        }, 3000);
        return () => clearInterval(interval);
    });
</script>

<div
    class="sovereign-mobile-audit bg-black/70 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl p-8 h-full flex flex-col gap-8 relative overflow-hidden group"
>
    <!-- Header -->
    <header class="flex justify-between items-center z-10">
        <div class="flex gap-4">
            <div
                class="p-4 bg-emerald-400/10 rounded-2xl text-emerald-400 border border-emerald-400/20 shadow-[0_0_20px_rgba(52,211,153,0.1)]"
            >
                <Smartphone size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.4em] text-white"
                >
                    Sovereign_Mobile_Audit
                </h2>
                <p
                    class="text-[8px] font-black text-white/30 uppercase italic mt-1 tracking-widest"
                >
                    Fortress_OS // Mobile_Convergence_Manifold
                </p>
            </div>
        </div>
        <div class="flex items-center gap-3">
            <div
                class="h-1.5 w-1.5 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_10px_#34d399]"
            ></div>
            <span
                class="text-[9px] font-black text-emerald-400 uppercase tracking-widest"
                >SUBSTRATE_READY</span
            >
        </div>
    </header>

    <!-- Scaling Visualizer (Convergence) -->
    <div class="flex-1 flex flex-col gap-6 z-10">
        <div
            class="bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col gap-4"
        >
            <div class="flex justify-between items-center mb-2">
                <div class="flex items-center gap-2">
                    <Monitor size={14} class="text-white/40" />
                    <span
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                        >Convergence_Scale</span
                    >
                </div>
                <span class="text-[10px] font-mono text-cyan-400"
                    >{(convergenceScale * 100).toFixed(0)}%</span
                >
            </div>
            <input
                type="range"
                min="0.4"
                max="1.0"
                step="0.01"
                bind:value={convergenceScale}
                class="w-full h-1 bg-white/10 rounded-full appearance-none cursor-pointer accent-cyan-400"
            />
            <div
                class="flex justify-between text-[7px] font-black text-white/20 uppercase"
            >
                <span>Pocket_Mobile</span>
                <span>Workstation_Convergence</span>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-6">
            <!-- Telemetry Block stats -->
            <div
                class="bg-rose-500/5 border border-rose-500/10 rounded-3xl p-6 relative group/stat overflow-hidden"
            >
                <ShieldAlert size={14} class="text-rose-400 mb-4" />
                <span
                    class="text-[24px] font-black text-white block leading-none"
                    >{telemetryBlockedCount.toLocaleString()}</span
                >
                <span
                    class="text-[8px] font-black text-rose-400 uppercase tracking-widest mt-2 block"
                    >Telemetry_Intercepts</span
                >
                <div
                    class="absolute -right-4 -bottom-4 opacity-5 rotate-12 group-hover/stat:rotate-0 transition-transform duration-700"
                >
                    <Lock size={80} />
                </div>
            </div>

            <!-- Health/Sovereignty -->
            <div
                class="bg-indigo-500/5 border border-indigo-500/10 rounded-3xl p-6"
            >
                <Zap size={14} class="text-indigo-400 mb-4" />
                <span
                    class="text-[24px] font-black text-white block leading-none"
                    >{transmissionHealth.toFixed(1)}%</span
                >
                <span
                    class="text-[8px] font-black text-indigo-400 uppercase tracking-widest mt-2 block"
                    >Runtime_Independence</span
                >
            </div>
        </div>

        <!-- Real-time audit log -->
        <div
            class="flex-1 min-h-[120px] bg-white/[0.02] border border-white/5 rounded-3xl overflow-hidden flex flex-col"
        >
            <div
                class="px-6 py-3 border-b border-white/5 bg-white/[0.02] flex justify-between items-center"
            >
                <span
                    class="text-[8px] font-black text-white/40 uppercase tracking-widest"
                    >Real-Time_Audit_Loom</span
                >
                <Globe size={10} class="text-white/20" />
            </div>
            <div class="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-2">
                {#each auditLogs as log}
                    <div
                        class="flex items-center justify-between p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-transparent hover:border-white/10 group/log"
                    >
                        <div class="flex items-center gap-3">
                            <div
                                class="w-1.5 h-1.5 rounded-full {log.status ===
                                'Blocked'
                                    ? 'bg-rose-400'
                                    : 'bg-emerald-400'}"
                            ></div>
                            <div class="flex flex-col">
                                <span class="text-[9px] font-bold text-white/80"
                                    >{log.message}</span
                                >
                                <span
                                    class="text-[7px] font-black text-white/20 uppercase"
                                    >{log.type}</span
                                >
                            </div>
                        </div>
                        <CheckCircle2
                            size={12}
                            class="text-emerald-400 opacity-0 group-hover/log:opacity-100 transition-opacity"
                        />
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Background Blueprint -->
    <div
        class="absolute inset-0 opacity-[0.05] pointer-events-none"
        style="background-image: radial-gradient(circle, white 0.5px, transparent 0.5px); background-size: 30px 30px;"
    ></div>
</div>
