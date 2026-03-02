<script lang="ts">
    import { fade } from "svelte/transition";
    import {
        Radio,
        SignalHigh,
        SignalMedium,
        SignalLow,
        Activity,
        ShieldCheck,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    let isScanning = $state(true);
    let selectedProfile = $state("bootstrap"); // 'bootstrap', 'helium', 'age-mesh'
    let isSwitching = $state(false);

    // Mock local shard network topology
    const localNetworks = [
        {
            id: "helium",
            name: "Helium 5G Mobile",
            type: "DePIN 1.0",
            merit: 0.85,
            fee: "0.01 AGE/GB",
            strength: 92,
            lat: 42,
            active: false,
        },
        {
            id: "age-mesh",
            name: "Sovereign Guardian @cipher",
            type: "AGE Dabba",
            merit: 0.98,
            fee: "0.005 SLC/GB",
            strength: 100,
            lat: 14,
            active: true,
        },
        {
            id: "world-mobile",
            name: "World Mobile AirNode",
            type: "DePIN 1.0",
            merit: 0.75,
            fee: "0.02 AGE/GB",
            strength: 65,
            lat: 55,
            active: false,
        },
    ];

    setTimeout(() => {
        isScanning = false;
    }, 1500);

    async function switchProfile(networkId: string) {
        if (selectedProfile === networkId || isSwitching) return;

        isSwitching = true;
        const net = localNetworks.find((n) => n.id === networkId);

        // Haptic feedback for interaction
        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate(50);
        }

        manifold.recordEvent(
            "ESIM_NEGOTIATION",
            `Initiating reverse-auction with ${net?.name}...`,
        );

        // Simulating eSIM Profile provisioning
        await new Promise((r) => setTimeout(r, 1200));

        // ZK-Zap Payment for Bootstrap
        manifold.walletState.resBalance -= 0.05; // tiny zap cost
        manifold.recordEvent(
            "ESIM_PROVISIONED",
            `Profile downloaded. Bound to Passport via ZK-Nullifier. Connecting...`,
        );

        await new Promise((r) => setTimeout(r, 800));

        selectedProfile = networkId;
        isSwitching = false;

        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate([100, 50, 100]); // Switch success
        }
    }
</script>

<div class="connectivity-card" in:fade>
    <div class="header">
        <div class="title-group">
            <Radio class="text-[#22d3ee] animate-pulse" size={20} />
            <h2>Sovereign Connectivity</h2>
        </div>
        <div class="zk-badge">
            <ShieldCheck size={14} />
            <span>ZK-MASKED</span>
        </div>
    </div>

    <!-- Active Profile Data -->
    <div class="active-profile-box">
        <div class="flex justify-between items-center mb-4">
            <div>
                <span
                    class="text-[10px] text-white/50 uppercase tracking-widest font-bold"
                    >Active eSIM Profile</span
                >
                <div class="text-xl font-black mt-1 text-white">
                    {selectedProfile === "bootstrap"
                        ? "Bootstrap Carrier"
                        : localNetworks.find((n) => n.id === selectedProfile)
                              ?.name}
                </div>
            </div>
            <div class="signal-indicator" class:pulse={isSwitching}>
                <SignalHigh class="text-[#00e5ff]" size={32} />
            </div>
        </div>

        <div class="live-metrics">
            <div class="metric">
                <span class="label">Data Flow</span>
                <span class="value font-mono">1.2 MB/s</span>
            </div>
            <div class="metric text-right">
                <span class="label">Local Exposure</span>
                <span class="value text-emerald-400 font-mono">0.00 SLC</span>
            </div>
        </div>

        {#if isSwitching}
            <div class="progress-bar mt-4" in:fade>
                <div
                    class="fill animate-pulse w-full bg-[#00e5ff] h-1 rounded"
                ></div>
            </div>
        {/if}
    </div>

    <!-- The Manifold Radar -->
    <div class="radar-section">
        <div class="flex justify-between items-end mb-4">
            <h3 class="text-sm font-bold text-white/70">Local DePIN Mesh</h3>
            {#if isScanning}
                <span
                    class="text-[10px] text-[#22d3ee] animate-pulse uppercase tracking-widest font-black flex items-center gap-1"
                >
                    <Activity size={10} /> Scanning
                </span>
            {:else}
                <button
                    class="text-[10px] text-white/40 hover:text-white uppercase tracking-widest font-black transition-colors"
                    onclick={() => {
                        isScanning = true;
                        setTimeout(() => (isScanning = false), 1000);
                    }}
                >
                    Rescan
                </button>
            {/if}
        </div>

        <div class="network-list">
            {#each localNetworks as net}
                <button
                    class="network-row"
                    class:active={selectedProfile === net.id}
                    class:disabled={isSwitching}
                    onclick={() => switchProfile(net.id)}
                    disabled={isSwitching || selectedProfile === net.id}
                >
                    <div class="net-icon">
                        {#if net.strength > 90}
                            <SignalHigh
                                size={18}
                                class={selectedProfile === net.id
                                    ? "text-black"
                                    : "text-[#22d3ee]"}
                            />
                        {:else if net.strength > 70}
                            <SignalMedium
                                size={18}
                                class={selectedProfile === net.id
                                    ? "text-black"
                                    : "text-[#22d3ee]"}
                            />
                        {:else}
                            <SignalLow
                                size={18}
                                class={selectedProfile === net.id
                                    ? "text-black"
                                    : "text-amber-500"}
                            />
                        {/if}
                    </div>

                    <div class="net-info">
                        <div class="net-name">{net.name}</div>
                        <div class="net-tags">
                            <span class="quality">{net.lat}ms</span>
                            <span class="merit text-amber-500 font-bold"
                                >M {net.merit.toFixed(2)}</span
                            >
                            <span class="type opacity-50">{net.type}</span>
                        </div>
                    </div>

                    <div class="net-action">
                        {#if selectedProfile === net.id}
                            <span
                                class="status-active font-black text-xs tracking-wider"
                                >CONNECTED</span
                            >
                        {:else}
                            <div
                                class="zap-price text-right group-hover:block transition-all"
                            >
                                <span
                                    class="block text-[10px] opacity-50 leading-tight"
                                    >ZAP RATE</span
                                >
                                <span
                                    class="block text-xs font-bold font-mono text-emerald-400"
                                    >{net.fee}</span
                                >
                            </div>
                        {/if}
                    </div>
                </button>
            {/each}
        </div>
    </div>
</div>

<style>
    .connectivity-card {
        background: rgba(15, 15, 20, 0.4);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        padding: 1.5rem;
        color: white;
        font-family: inherit;
        position: relative;
        overflow: hidden;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .title-group {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .title-group h2 {
        font-size: 1.1rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .zk-badge {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        font-size: 0.6rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        padding: 0.4rem 0.8rem;
        border-radius: 100px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .active-profile-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(34, 211, 238, 0.2);
        box-shadow: inset 0 0 20px rgba(34, 211, 238, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .live-metrics {
        display: flex;
        justify-content: space-between;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .metric {
        display: flex;
        flex-direction: column;
    }

    .metric .label {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 0.2rem;
    }

    .metric .value {
        font-size: 1.1rem;
        font-weight: 900;
        letter-spacing: -0.05em;
    }

    .network-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .network-row {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        color: white;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
    }

    .network-row:hover:not(.disabled):not(.active) {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .network-row.active {
        background: #00e5ff;
        color: black;
        box-shadow: 0 10px 30px rgba(0, 229, 255, 0.2);
        cursor: default;
    }

    .net-icon {
        width: 36px;
        height: 36px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .network-row.active .net-icon {
        background: rgba(0, 0, 0, 0.1);
    }

    .net-info {
        flex: 1;
    }

    .net-name {
        font-size: 0.9rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .net-tags {
        display: flex;
        gap: 0.75rem;
        font-size: 0.65rem;
        font-weight: 700;
    }

    .status-active {
        color: black;
        opacity: 0.7;
    }
</style>
