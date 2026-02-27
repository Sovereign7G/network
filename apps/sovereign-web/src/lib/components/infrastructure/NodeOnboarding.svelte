<script lang="ts">
    import { onMount } from "svelte";
    import { fade, slide } from "svelte/transition";
    import { sovereignComputeManager } from "../../../../../../packages/age-cloud/src/compute/compute-manager";
    import { cloudStore, hearthStore } from "../../stores/master-store";

    let activated = false;
    let detecting = false;
    let hardware = {
        cpu: { cores: 8, speed: 3.2 },
        memory: 16,
        storage: 512,
        gpu: { model: "RTX 4090 (Virtual Mesh)" },
    };
    let nodeId = "";
    let stats = {
        uptime: 0,
        load: 12,
        earnings: 0,
        resonance: 0,
    };

    onMount(async () => {
        detecting = true;
        // Simulate hardware detection
        await new Promise((r) => setTimeout(r, 1500));
        detecting = false;
    });

    async function activateNode() {
        detecting = true;

        const node = await sovereignComputeManager.registerComputeNode({
            owner: "@citizen.zero",
            type: "S-NODE",
            hardware: {
                cpu: {
                    cores: hardware.cpu.cores,
                    architecture: "x86_64",
                    speed: hardware.cpu.speed,
                },
                memory: hardware.memory,
                storage: hardware.storage,
            },
        });

        nodeId = node.id;
        cloudStore.addComputeNode(node);

        // Award resonance & memory
        hearthStore.addMemory({
            type: "TASK",
            content: `Activated S-Node ${nodeId.slice(0, 8)} · Contributed ${hardware.cpu.cores} vCPU to the Mesh`,
            tags: ["infrastructure", "v27", "activation"],
        });

        activated = true;
        detecting = false;
        startStatsTracking();
    }

    function startStatsTracking() {
        setInterval(() => {
            stats.uptime += 5;
            stats.load = 10 + Math.random() * 15;
            stats.earnings += 0.0001;
            stats.resonance = Math.floor(stats.uptime / 60);
        }, 5000);
    }
</script>

<div class="node-onboarding {activated ? 'active' : ''}">
    <div class="card-header">
        <div class="icon-orb">
            {#if activated}
                <div class="pulse-ring"></div>
            {/if}
            <span class="icon">⚡</span>
        </div>
        <div class="title-area">
            <h3>Sovereign Node Activation</h3>
            <p>
                {activated
                    ? "Infrastructure Online"
                    : "Contribute your idle hardware"}
            </p>
        </div>
        {#if !activated}
            <span class="badge" in:fade>+250 RESONANCE</span>
        {/if}
    </div>

    <div class="card-content">
        {#if detecting}
            <div class="detecting" in:fade>
                <div class="spinner"></div>
                <p>Analyzing Hardware Tiers...</p>
            </div>
        {:else if !activated}
            <div class="hardware-specs" in:slide>
                <div class="spec">
                    <span class="label">vCPU</span>
                    <span class="value">{hardware.cpu.cores} Cores</span>
                </div>
                <div class="spec">
                    <span class="label">RAM</span>
                    <span class="value">{hardware.memory} GB</span>
                </div>
                <div class="spec">
                    <span class="label">Storage</span>
                    <span class="value">{hardware.storage} GB</span>
                </div>
                <div class="spec">
                    <span class="label">GPU</span>
                    <span class="value">{hardware.gpu.model}</span>
                </div>
            </div>

            <div class="projected-earnings">
                <h4>Monthly Projection</h4>
                <div class="earnings-grid">
                    <div class="earning-item">
                        <span>Mesh Yield</span>
                        <span class="amount">$24.40</span>
                    </div>
                    <div class="earning-item total">
                        <span>Total Value</span>
                        <span class="amount">$24.40 / mo</span>
                    </div>
                </div>
            </div>

            <button class="activate-btn" onclick={activateNode}>
                Launch S-Node Activation
            </button>
        {:else}
            <div class="active-node" in:slide>
                <div class="success-row">
                    <div class="success-badge">✓ MESH ACTIVATED</div>
                    <span class="node-hash">{nodeId.slice(0, 16)}...</span>
                </div>

                <div class="node-stats">
                    <div class="stat">
                        <span class="label">Uptime</span>
                        <span class="value"
                            >{Math.floor(stats.uptime / 60)}m {stats.uptime %
                                60}s</span
                        >
                    </div>
                    <div class="stat">
                        <span class="label">Mesh Load</span>
                        <span class="value">{stats.load.toFixed(1)}%</span>
                    </div>
                    <div class="stat">
                        <span class="label">Earnings</span>
                        <span class="value highlight"
                            >${stats.earnings.toFixed(4)}</span
                        >
                    </div>
                    <div class="stat">
                        <span class="label">Resonance</span>
                        <span class="value">+{stats.resonance}</span>
                    </div>
                </div>

                <div class="contribution-viz">
                    <div class="viz-header">
                        <span>Cathedral Backbone Contribution</span>
                        <span>{stats.load.toFixed(0)}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="fill" style="width: {stats.load}%"></div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .node-onboarding {
        background: #0d110d;
        border: 1px solid #1a2a1a;
        border-radius: 20px;
        color: white;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .node-onboarding.active {
        border-color: #4caf50;
        box-shadow: 0 0 40px rgba(76, 175, 80, 0.05);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        padding: 1.5rem;
        background: rgba(76, 175, 80, 0.03);
        border-bottom: 1px solid #1a2a1a;
    }

    .icon-orb {
        width: 48px;
        height: 48px;
        background: #1a1a1a;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        position: relative;
    }

    .pulse-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 2px solid #4caf50;
        border-radius: 12px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 0.8;
        }
        100% {
            transform: scale(1.5);
            opacity: 0;
        }
    }

    .title-area h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
    }
    .title-area p {
        margin: 0;
        font-size: 0.8rem;
        color: #666;
    }

    .badge {
        margin-left: auto;
        background: #4caf50;
        color: #000;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 800;
    }

    .card-content {
        padding: 1.5rem;
    }

    .detecting {
        text-align: center;
        padding: 2rem;
    }

    .spinner {
        width: 32px;
        height: 32px;
        border: 2px solid #1a2a1a;
        border-top-color: #4caf50;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .hardware-specs {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .spec {
        background: #141414;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #222;
    }

    .spec .label {
        display: block;
        font-size: 0.7rem;
        color: #555;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .spec .value {
        font-size: 1rem;
        font-weight: 700;
        color: #fff;
    }

    .projected-earnings h4 {
        font-size: 0.8rem;
        color: #555;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .earnings-grid {
        background: #0a0e0a;
        border-radius: 12px;
        padding: 1rem;
    }

    .earning-item {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        padding: 0.25rem 0;
    }
    .earning-item.total {
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #1a2a1a;
        font-weight: 700;
    }
    .amount {
        color: #4caf50;
    }

    .activate-btn {
        width: 100%;
        margin-top: 1.5rem;
        padding: 1.25rem;
        background: #4caf50;
        color: #000;
        border: none;
        border-radius: 12px;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s;
    }

    .activate-btn:hover {
        background: #66bb6a;
        transform: translateY(-2px);
    }

    .success-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }
    .success-badge {
        background: rgba(76, 175, 80, 0.1);
        color: #4caf50;
        padding: 0.4rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .node-hash {
        font-family: monospace;
        font-size: 0.75rem;
        color: #444;
    }

    .node-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .stat {
        background: #141414;
        padding: 1rem;
        border-radius: 12px;
    }
    .stat .label {
        display: block;
        font-size: 0.7rem;
        color: #555;
        text-transform: uppercase;
    }
    .stat .value {
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0.25rem;
        display: block;
    }
    .stat .value.highlight {
        color: #4caf50;
    }

    .contribution-viz {
        background: #141414;
        padding: 1.25rem;
        border-radius: 12px;
    }
    .viz-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #555;
        margin-bottom: 0.75rem;
    }
    .progress-bar {
        height: 6px;
        background: #000;
        border-radius: 3px;
        overflow: hidden;
    }
    .fill {
        height: 100%;
        background: #4caf50;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        transition: width 0.5s;
    }
</style>
