<script lang="ts">
    import { fade } from "svelte/transition";
    import { icpService } from "$lib/services/icp-service.svelte";
    import { credentialService } from "$lib/services/credential-service";
    import { neuralSensor } from "$lib/services/neural-sensor-service.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";
    import {
        ShieldCheck,
        Database,
        AlertCircle,
        Award,
        BrainCircuit,
        Fingerprint,
        Lock,
        Activity,
    } from "lucide-svelte";

    import SovereignPassport from "./SovereignPassport.svelte";

    let profile = $state<any>(null);
    let sensor = $derived(neuralSensor.state);
    let isSyncing = $state(false);
    let manifestingPassport = $state<any>(null);

    async function loadProfile() {
        if (!icpService.state.isAuthenticated) return;
        try {
            const res = await icpService.getBioProfile();
            profile = res[0] || null;
        } catch (e) {
            console.error("Failed to load BioProfile", e);
        }
    }

    async function syncResonance() {
        isSyncing = true;
        try {
            const res = await icpService.recordCoherence(
                sensor.coherence,
                "THETA_9.5HZ",
                "Synthetic Neural Graft V2",
            );
            if ("ok" in res) {
                profile = res.ok;
                manifold.recordEvent(
                    "BIO_RESONANCE_SYNCED",
                    "Neural coherence anchored to ICP BioVault.",
                );
            }
        } catch (e) {
            console.error("Sync failed", e);
        } finally {
            isSyncing = false;
        }
    }

    async function claimPassport() {
        try {
            const vc = await credentialService.claimSovereignPassport();
            if (vc) {
                manifestingPassport = vc;
                manifold.recordEvent(
                    "PASSPORT_MANIFESTED",
                    "Sovereign Passport VC manifested.",
                );
            }
        } catch (e: any) {
            alert(e.message);
        }
    }

    $effect(() => {
        if (icpService.state.isAuthenticated) {
            loadProfile();
        }
    });
</script>

<div class="bio-vault-container">
    <!-- Header -->
    <div class="flex justify-between items-start mb-10">
        <div class="flex flex-col">
            <h3
                class="text-[9px] font-black uppercase tracking-[0.2em] text-emerald-400 mb-1"
            >
                Neural_Symbiosis_Node
            </h3>
            <h2
                class="text-2xl font-black text-white uppercase tracking-tighter"
            >
                Bio_Vault
            </h2>
        </div>
        <div class="security-chip">
            <ShieldCheck size={18} class="text-emerald-400" />
            <span class="text-[8px] font-black uppercase text-emerald-400/60"
                >AAL3</span
            >
        </div>
    </div>

    {#if !icpService.state.isAuthenticated}
        <div class="auth-required" in:fade>
            <div class="lock-icon-shell">
                <Lock size={32} class="text-white/10" />
            </div>
            <div class="text-center space-y-1">
                <p
                    class="text-[10px] font-black text-white uppercase tracking-widest"
                >
                    Sovereign_Identity_Required
                </p>
                <p class="text-[8px] text-white/30 font-medium">
                    Connect your Internet Identity to decrypt vault shards
                </p>
            </div>
            <button onclick={() => icpService.login()} class="auth-btn">
                <Fingerprint size={14} />
                <span>Authorize_Decrypt</span>
            </button>
        </div>
    {:else}
        <div
            class="vault-content overflow-auto scrollbar-hide flex-1 space-y-8"
        >
            <!-- Neural Spectrum -->
            <div class="sensor-card">
                <div class="flex justify-between items-center mb-4">
                    <div class="flex items-center gap-2">
                        <BrainCircuit size={14} class="text-cyan-400" />
                        <span
                            class="text-[9px] font-black uppercase text-white/40"
                            >Neural_Coherence</span
                        >
                    </div>
                    <div class="text-right flex flex-col">
                        <span class="text-xs font-black text-cyan-400"
                            >{(sensor.coherence * 100).toFixed(1)}%</span
                        >
                        <span
                            class="text-[7px] text-white/20 uppercase font-black tracking-widest"
                            >{neuralSensor.getCoherenceGrade()}</span
                        >
                    </div>
                </div>

                <!-- Waveform Visualizer -->
                <div class="waveform-box">
                    {#each sensor.waveform as val, i}
                        <div
                            class="wave-bar"
                            style="height: {40 + val * 60}%; opacity: {0.2 +
                                (i / sensor.waveform.length) * 0.8}"
                        ></div>
                    {/each}
                    <div class="scanline"></div>
                </div>

                <!-- Frequency Monitor -->
                <div class="grid grid-cols-5 gap-1.5 pt-4">
                    {#each sensor.bands as band}
                        <div class="flex flex-col items-center gap-1.5">
                            <div class="band-ruler">
                                <div
                                    class="band-fill"
                                    style="height: {band.magnitude * 100}%"
                                ></div>
                            </div>
                            <span
                                class="text-[6px] font-black text-white/20 uppercase"
                                >{band.label}</span
                            >
                        </div>
                    {/each}
                </div>

                <button
                    onclick={syncResonance}
                    disabled={isSyncing}
                    class="sync-btn"
                    class:syncing={isSyncing}
                >
                    {#if isSyncing}
                        <Activity size={12} class="animate-spin" />
                        <span>ANCHORING_CONSCIOUSNESS...</span>
                    {:else}
                        <Activity size={12} />
                        <span>ANCHOR_COHERENCE_TO_LXV</span>
                    {/if}
                </button>
            </div>

            <!-- Profile Stats -->
            <div class="grid grid-cols-2 gap-3">
                <div class="stat-box">
                    <span
                        class="text-[7px] font-black uppercase text-white/20 mb-2 block"
                        >Total_Resonance_Metric</span
                    >
                    <span class="text-sm font-black text-white"
                        >{profile
                            ? (profile.cumulative_coherence * 100).toFixed(2) +
                              "%"
                            : "0.00%"}</span
                    >
                </div>
                <div class="stat-box">
                    <span
                        class="text-[7px] font-black uppercase text-white/20 mb-2 block"
                        >Sovereign_Manifest</span
                    >
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-1.5">
                            {#if profile?.is_verified}
                                <Award size={10} class="text-emerald-400" />
                                <span
                                    class="text-[7px] font-black uppercase text-emerald-400"
                                    >CITIZEN_V1</span
                                >
                            {:else}
                                <AlertCircle size={10} class="text-rose-400" />
                                <span
                                    class="text-[7px] font-black uppercase text-rose-400"
                                    >GHOST_STATE</span
                                >
                            {/if}
                        </div>
                        {#if (profile?.cumulative_coherence || 0) >= 0.8}
                            <button onclick={claimPassport} class="claim-badge"
                                >MANIFEST_V2</button
                            >
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/if}

    <!-- Security Footer -->
    <div class="vault-footer">
        <div
            class="flex items-center gap-2 text-white/10 uppercase font-black text-[7px]"
        >
            <Database size={10} />
            <span>Encrypted @ ICP_Subnet_Nagano // ECC_Secp256k1</span>
        </div>
    </div>

    {#if manifestingPassport}
        <SovereignPassport
            credential={manifestingPassport}
            onClose={() => (manifestingPassport = null)}
        />
    {/if}
</div>

<style>
    .bio-vault-container {
        height: 100%;
        background: rgba(10, 15, 25, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        backdrop-filter: blur(40px);
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        position: relative;
        overflow: hidden;
    }

    .security-chip {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 12px;
    }

    .auth-required {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }

    .lock-icon-shell {
        width: 80px;
        height: 80px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .auth-btn {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        color: white;
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.2s;
    }

    .auth-btn:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(34, 211, 238, 0.3);
    }

    .sensor-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
    }

    .waveform-box {
        height: 80px;
        background: rgba(34, 211, 238, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(34, 211, 238, 0.1);
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        padding: 0.5rem;
        position: relative;
        overflow: hidden;
    }

    .wave-bar {
        width: 3px;
        background: #22d3ee;
        border-radius: 100px;
        transition: height 0.1s linear;
    }

    .scanline {
        position: absolute;
        width: 100%;
        height: 1px;
        background: rgba(34, 211, 238, 0.2);
        top: 0;
        left: 0;
        animation: scan 3s linear infinite;
    }

    @keyframes scan {
        from {
            transform: translateY(0);
        }
        to {
            transform: translateY(80px);
        }
    }

    .band-ruler {
        width: 100%;
        height: 48px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 4px;
        position: relative;
        overflow: hidden;
    }

    .band-fill {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
            to top,
            rgba(34, 211, 238, 0.3),
            rgba(34, 211, 238, 0.1)
        );
        transition: height 0.3s;
    }

    .sync-btn {
        width: 100%;
        margin-top: 1.5rem;
        padding: 0.85rem;
        background: #22d3ee;
        color: #05070a;
        border: none;
        border-radius: 14px;
        font-size: 9px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 8px 20px rgba(34, 211, 238, 0.2);
    }

    .sync-btn:hover {
        transform: translateY(-2px);
        background: #67e8f9;
        box-shadow: 0 12px 24px rgba(34, 211, 238, 0.3);
    }

    .sync-btn.syncing {
        opacity: 0.7;
        cursor: wait;
    }

    .stat-box {
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
    }

    .claim-badge {
        padding: 4px 10px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        color: #10b981;
        font-size: 7px;
        font-weight: 900;
        cursor: pointer;
        transition: all 0.2s;
    }

    .vault-footer {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
    }
</style>
