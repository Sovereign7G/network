<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import { icpService } from "$lib/services/icp-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import { Terminal, Activity, Globe, Lock } from "lucide-svelte";

    let icp = icpService.state;
    let healthStatus = $state("Awaiting Ping...");
    let isPinging = $state(false);
    let selectedCommand = $state("Sophia_SynthesizeVision");
    let commandResponse = $state<any>(null);

    async function pingCanister() {
        isPinging = true;
        try {
            healthStatus = await icpService.getHealth();
            manifold.recordEvent(
                "ICP_HEALTH_CHECK",
                "Canister PantheonConduit responded successfully.",
            );
        } catch (e) {
            healthStatus = "Error: Replica Unreachable";
        } finally {
            isPinging = false;
        }
    }

    async function executeCommand() {
        try {
            let cmd: any = {};
            if (selectedCommand === "Sophia_SynthesizeVision") {
                cmd = {
                    Sophia_SynthesizeVision: {
                        poetic_guidance: "Reflective harmony in silicon.",
                        roadmap_id: "RM-2026-ALPHA",
                    },
                };
            } else if (selectedCommand === "InitiateNeuralSymbiosis") {
                cmd = {
                    InitiateNeuralSymbiosis: {
                        frequency_band: "9.2 GHz",
                        coherence_threshold: 0.95,
                    },
                };
            }

            commandResponse = await icpService.executeDivineCommand(cmd);
            manifold.recordEvent(
                "DIVINE_COMMAND_EXECUTED",
                `Command ${selectedCommand} manifested.`,
            );
        } catch (e) {
            commandResponse = { success: false, error: "Manifestation Failed" };
        }
    }
</script>

<div class="canister-console glass-panel p-6 h-full flex flex-col" in:fade>
    <div class="flex justify-between items-start mb-6">
        <div>
            <h3
                class="text-xs font-black uppercase tracking-[0.3em] text-white/40 mb-1"
            >
                ICP Network Console
            </h3>
            <div class="flex items-center gap-2">
                <span class="text-2xl font-black text-white">PLAYGROUND</span>
                <div
                    class="px-2 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-[8px] font-black uppercase tracking-widest"
                >
                    Canister_Active
                </div>
            </div>
        </div>
        <div class="flex gap-2">
            {#if !icp.isAuthenticated}
                <button
                    onclick={() => icpService.login()}
                    class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-[10px] font-black uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(147,51,234,0.3)]"
                >
                    Link Identity
                </button>
            {:else}
                <div class="text-right">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase block"
                        >Linked Principal</span
                    >
                    <span class="text-[10px] font-mono text-purple-400"
                        >{icp.principal?.slice(0, 8)}...</span
                    >
                </div>
            {/if}
        </div>
    </div>

    <!-- Vitals -->
    <div class="grid grid-cols-2 gap-4 mb-6">
        <div class="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
            <span
                class="text-[8px] font-black text-white/20 uppercase tracking-widest block mb-1"
                >Heartbeat</span
            >
            <div class="flex items-center gap-2 text-emerald-400">
                <Activity size={12} class="animate-pulse" />
                <span class="text-xs font-black uppercase tracking-tighter"
                    >{healthStatus}</span
                >
            </div>
        </div>
        <button
            onclick={pingCanister}
            disabled={isPinging}
            class="bg-white/[0.05] border border-white/10 p-4 rounded-2xl hover:bg-white/10 transition-all flex flex-col items-center justify-center gap-1 group"
        >
            <Globe
                size={16}
                class="text-white/40 group-hover:text-cyan-400 transition-colors"
            />
            <span class="text-[8px] font-black text-white/20 uppercase"
                >Ping_Replica</span
            >
        </button>
    </div>

    <!-- Command Center -->
    <div
        class="flex-1 bg-black/40 rounded-2xl border border-white/5 p-4 flex flex-col gap-4"
    >
        <div class="flex items-center gap-2 mb-2">
            <Terminal size={14} class="text-purple-400" />
            <span
                class="text-[10px] font-black uppercase tracking-widest text-white/60"
                >Manifestation_Interface</span
            >
        </div>

        <select
            bind:value={selectedCommand}
            class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-[10px] font-black uppercase text-white outline-none focus:border-purple-500/50 transition-all"
        >
            <option value="Sophia_SynthesizeVision"
                >Sophia: Synthesize Vision</option
            >
            <option value="InitiateNeuralSymbiosis"
                >Sophia: Neural Symbiosis</option
            >
            <option value="Yaroslav_ForgeAgent">Yaroslav: Forge Agent</option>
        </select>

        <button
            onclick={executeCommand}
            disabled={!icp.isAuthenticated}
            class="w-full py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-lg hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-30 disabled:grayscale"
        >
            Manifest Command
        </button>

        {#if commandResponse}
            <div
                class="mt-4 p-3 bg-white/[0.03] border border-white/5 rounded-xl"
                in:slide
            >
                <div class="flex justify-between items-center mb-2">
                    <span class="text-[8px] font-black uppercase text-white/20"
                        >Response Status</span
                    >
                    <span
                        class="text-[8px] font-black uppercase {commandResponse.success
                            ? 'text-emerald-400'
                            : 'text-rose-400'}"
                    >
                        {commandResponse.success ? "SUCCESS" : "FAILED"}
                    </span>
                </div>
                <p
                    class="text-[10px] font-mono text-white/60 leading-relaxed italic"
                >
                    {commandResponse.data ||
                        commandResponse.error ||
                        "No data returned."}
                </p>
            </div>
        {/if}
    </div>

    <!-- Footnote -->
    <div
        class="mt-6 pt-4 border-t border-white/5 flex justify-between items-center"
    >
        <div class="flex items-center gap-2">
            <Lock size={10} class="text-purple-500" />
            <span
                class="text-[7px] font-black uppercase text-white/20 tracking-tighter italic"
                >Secured by Internet Identity // BLS12-381</span
            >
        </div>
        <div class="flex gap-1">
            <div class="w-1 h-3 bg-purple-500/40 rounded-full"></div>
            <div class="w-1 h-3 bg-purple-500/20 rounded-full"></div>
            <div class="w-1 h-3 bg-purple-500/10 rounded-full"></div>
        </div>
    </div>
</div>

<style>
    .canister-console {
        background: linear-gradient(
            135deg,
            rgba(88, 28, 135, 0.1) 0%,
            rgba(15, 23, 42, 0.4) 100%
        );
    }
</style>
