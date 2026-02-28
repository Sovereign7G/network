<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, slide, scale } from "svelte/transition";
    import { 
        CreditCard, 
        Send, 
        ShieldCheck, 
        Smartphone, 
        QrCode, 
        Calendar, 
        Repeat, 
        Ban,
        Zap,
        Clock,
        CheckCircle2,
        Info
    } from "lucide-svelte";

    // --- WEAVE-INSPIRED SOVEREIGN STATES ---
    type Mode = "IDLE" | "SCAN" | "TAP" | "TEXT" | "RESIDENCE" | "SUCCESS";
    let mode: Mode = $state("IDLE");
    let amount = $state(0);
    let recipient = $state("");
    let isProcessing = $state(false);
    let logs = $state<string[]>([]);
    let progress = $state(0);

    const LOGS = {
        TEXT: ["Detecting intention weave...", "Gossip Mesh handshake active...", "Decrypting payment intent..."],
        TAP: ["Resonating near-field frequency...", "WASM handshake established...", "Emitting sovereign signature..."],
        SCAN: ["Synthesizing local QR geometry...", "Topological scan in progress...", "Matched peer manifest."]
    };

    function startProcess(newMode: Mode) {
        mode = newMode;
        if (newMode !== "IDLE" && newMode !== "SUCCESS") {
            logs = LOGS[newMode as keyof typeof LOGS] || ["Initializing..."];
            isProcessing = true;
            progress = 0;
            
            const timer = setInterval(() => {
                progress += 5;
                if (progress >= 100) {
                    clearInterval(timer);
                    finalize();
                }
            }, 100);
        }
    }

    function finalize() {
        isProcessing = false;
        manifold.processPayment(recipient || "PEER-0x88", amount || 100, `Weave Synthesis: ${mode}`);
        mode = "SUCCESS";
        setTimeout(() => { mode = "IDLE"; amount = 0; }, 3000);
    }
</script>

<div
    class="flex flex-col h-full bg-slate-950/90 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-[0_0_50px_rgba(30,58,138,0.3)] relative group transition-all"
>
    <!-- Header -->
    <div class="flex items-center justify-between z-10">
        <div class="flex items-center gap-3">
            <div class="p-3 bg-blue-500/10 rounded-2xl text-blue-400 border border-blue-500/20">
                <Zap size={20} class="animate-pulse" />
            </div>
            <div>
                <h2 class="text-xs font-black uppercase tracking-widest text-white">Value_Weaver</h2>
                <span class="text-[8px] font-black text-blue-400/60 uppercase tracking-widest">Avenue 4 Synthesis</span>
            </div>
        </div>
        <div class="flex gap-2">
            <div class="px-3 py-1 bg-emerald-400/10 border border-emerald-400/20 rounded-full flex items-center gap-2">
                <ShieldCheck size={12} class="text-emerald-400" />
                <span class="text-[8px] font-black text-emerald-400 uppercase tracking-widest">NODAL SETTLED</span>
            </div>
        </div>
    </div>

    <!-- Main Stack -->
    <div class="flex-1 relative">
        {#if mode === "IDLE"}
            <div class="grid grid-cols-2 gap-4 h-full" in:fade>
                <div class="space-y-4">
                    <div class="space-y-1">
                        <label class="text-[8px] font-black text-white/30 uppercase tracking-widest ml-1">Engagement_Volume</label>
                        <input type="number" bind:value={amount} class="w-full bg-black/40 border border-white/5 rounded-xl p-3 text-sm font-bold text-white outline-none focus:border-blue-500/40 transition-all" placeholder="0.00 CR"/>
                    </div>
                    
                    <button class="w-full p-4 bg-white/[0.03] border border-white/5 rounded-2xl flex flex-col items-center gap-2 hover:bg-blue-500/10 hover:border-blue-500/30 transition-all group" onclick={() => startProcess('TEXT')}>
                        <Send size={18} class="text-blue-400 group-hover:scale-110 transition-transform" />
                        <span class="text-[9px] font-black uppercase tracking-widest text-white/60">Text_to_Pay</span>
                    </button>
                    
                    <button class="w-full p-4 bg-white/[0.03] border border-white/5 rounded-2xl flex flex-col items-center gap-2 hover:bg-blue-500/10 hover:border-blue-500/30 transition-all group" onclick={() => startProcess('SCAN')}>
                        <QrCode size={18} class="text-blue-400 group-hover:scale-110 transition-transform" />
                        <span class="text-[9px] font-black uppercase tracking-widest text-white/60">Scan_to_Pay</span>
                    </button>
                </div>
                
                <div class="space-y-4">
                     <button class="h-[calc(50%-8px)] w-full bg-white/[0.03] border border-white/5 rounded-2xl flex flex-col justify-center items-center gap-2 hover:bg-blue-500/10 hover:border-blue-500/30 transition-all group" onclick={() => startProcess('TAP')}>
                        <Smartphone size={24} class="text-blue-400 group-hover:-translate-y-1 transition-transform" />
                        <span class="text-[9px] font-black uppercase tracking-widest text-white/60">Tap_to_Pay</span>
                    </button>
                    
                    <div class="h-[calc(50%-8px)] w-full bg-blue-500/5 border border-blue-500/10 rounded-2xl p-4 flex flex-col justify-between">
                        <div class="flex items-center justify-between">
                            <Repeat size={14} class="text-blue-400" />
                            <span class="text-[8px] font-black uppercase text-blue-400/60">Temporal Plans</span>
                        </div>
                        <p class="text-[8px] text-white/40 leading-relaxed font-bold uppercase tracking-tighter">Automate monthly value streams with direct nodal debit.</p>
                        <div class="h-1 bg-white/5 rounded-full overflow-hidden">
                            <div class="h-full bg-blue-400 w-1/3"></div>
                        </div>
                    </div>
                </div>
            </div>
        {:else if mode === "SUCCESS"}
            <div class="absolute inset-0 flex flex-col items-center justify-center gap-4" in:scale>
                <div class="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30 shadow-[0_0_30px_rgba(16,185,129,0.2)]">
                    <CheckCircle2 size={32} class="text-emerald-400" />
                </div>
                <h3 class="text-sm font-black text-white uppercase tracking-widest">Transaction_Invariant</h3>
                <p class="text-[8px] text-emerald-400/60 font-black uppercase">Confirmed by 3/3 Peer Shards</p>
            </div>
        {:else}
            <div class="flex flex-col h-full gap-4" in:fade>
                <div class="flex-1 bg-black/40 rounded-3xl border border-white/5 p-4 font-mono text-[9px] flex flex-col gap-2 overflow-hidden">
                    {#each logs as logMsg}
                        <div class="text-blue-300 transition-opacity">
                            <span class="opacity-40">>></span> {logMsg}
                        </div>
                    {/each}
                    <div class="mt-auto h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div class="h-full bg-blue-400 transition-all duration-100" style="width: {progress}%"></div>
                    </div>
                </div>
                
                <div class="p-4 bg-white/[0.02] border border-white/5 rounded-2xl flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <Clock size={16} class="text-blue-400 animate-spin-slow" />
                        <span class="text-[9px] font-black uppercase text-white/50 tracking-widest">Settling in Manifold...</span>
                    </div>
                    <span class="text-[10px] font-black text-white tabular-nums">{progress}%</span>
                </div>
            </div>
        {/if}
    </div>

    <!-- Footer Stats -->
    <div class="mt-auto pt-4 border-t border-white/5 flex items-center justify-between text-[8px] font-black uppercase tracking-widest text-white/20">
        <div class="flex items-center gap-2">
            <ShieldCheck size={10} />
            <span>PCI_COMPLIANT_SIM</span>
        </div>
        <div class="flex items-center gap-2">
            <Info size={10} />
            <span>NO_FEES_SOVEREIGN</span>
        </div>
    </div>
</div>

<style>
    .animate-spin-slow {
        animation: spin 4s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
