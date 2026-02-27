<script lang="ts">
    import { fly, slide } from "svelte/transition";
    import {
        Handshake,
        Globe,
        Anchor,
        Heart,
        FileText,
        ChevronRight,
        Scale,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type Treaty = {
        id: string;
        parties: [string, string];
        title: string;
        status: "ACTIVE" | "PROPOSED" | "NEGOTIATING";
        trustScore: number;
        type: "PEACE_ACCORD" | "RESOURCE_SHARE" | "DATA_MAPPING";
        timestamp: string;
    };

    let treaties = $state<Treaty[]>([
        {
            id: "TR-2026-NAG-ZUG",
            parties: ["Nagano_PoR", "Zug_SwissVault"],
            title: "Global Liquid State Accord",
            status: "ACTIVE",
            trustScore: 98,
            type: "PEACE_ACCORD",
            timestamp: "2026-02-15",
        },
        {
            id: "TR-2026-LON-BRL",
            parties: ["London_Shades", "Berlin_Luminance"],
            title: "Hyper-Regional Resource Mesh",
            status: "NEGOTIATING",
            trustScore: 72,
            type: "RESOURCE_SHARE",
            timestamp: "2026-02-21",
        },
    ]);

    let activeParties = $state([
        { name: "Nagano", connectivity: 98, load: 45 },
        { name: "Zug", connectivity: 99, load: 12 },
        { name: "London", connectivity: 88, load: 78 },
        { name: "Berlin", connectivity: 92, load: 34 },
        { name: "Tokyo", connectivity: 99, load: 67 },
        { name: "Singapore", connectivity: 96, load: 22 },
    ]);

    let hoverJurisdiction = $state<(typeof activeParties)[0] | null>(null);

    function proposeTreaty() {
        manifold.recordEvent(
            "TREATY_PROPOSE",
            "New Peace Accord proposed between regional nodes.",
        );
    }
</script>

<div class="diplomacy-shell">
    <!-- Institutional Header -->
    <header class="diplomacy-header">
        <div class="header-brand">
            <div class="logo-box">
                <Handshake size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Diplomacy_Forge</h2>
                <div class="flex items-center gap-2">
                    <span class="fabric-label">Fabric_Status: Harmonious</span>
                    <div class="fabric-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">GLOBAL_ACCORDS</span>
                <span class="tel-value">{treaties.length}_ACTIVE</span>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block">
                <span class="tel-label">TRUST_INDEX</span>
                <span class="tel-value text-rose-400">0.96_PF</span>
            </div>
        </div>
    </header>

    <div class="diplomacy-body">
        <!-- Topology Viewport -->
        <main class="topology-viewport">
            <div class="topo-background">
                <div class="orbit ob-1"></div>
                <div class="orbit ob-2"></div>
                <div class="orbit ob-3"></div>
                <div class="topo-grid"></div>
            </div>

            <!-- Jurisdictional Spheres -->
            {#each activeParties as party, i}
                {@const angle = (i / activeParties.length) * Math.PI * 2}
                {@const x = Math.cos(angle) * 180}
                {@const y = Math.sin(angle) * 180}
                <button
                    class="node-sphere"
                    style="transform: translate({x}px, {y}px)"
                    onmouseenter={() => (hoverJurisdiction = party)}
                    onmouseleave={() => (hoverJurisdiction = null)}
                >
                    <div class="sphere-core">
                        <Anchor size={14} />
                        <div class="sphere-ping"></div>
                    </div>
                    <span class="sphere-label">{party.name}</span>
                </button>
            {/each}

            <!-- Central Authority -->
            <div class="topology-core">
                <Globe size={48} class="text-rose-400 animate-pulse" />
                <div class="core-aura"></div>
            </div>

            <!-- Intel Overlay -->
            {#if hoverJurisdiction}
                <div class="intel-overlay" in:fly={{ y: 20, duration: 400 }}>
                    <div class="intel-header">
                        <div class="intel-dot"></div>
                        <h3>{hoverJurisdiction.name}_Jurisdiction</h3>
                    </div>
                    <div class="intel-grid">
                        <div class="intel-item">
                            <span class="i-label">Connectivity</span>
                            <span class="i-value text-emerald-400"
                                >{hoverJurisdiction.connectivity}%</span
                            >
                        </div>
                        <div class="intel-item">
                            <span class="i-label">Shard_Load</span>
                            <span class="i-value"
                                >{hoverJurisdiction.load}%</span
                            >
                        </div>
                    </div>
                </div>
            {/if}
        </main>

        <!-- Accord Fabric -->
        <aside class="accord-sidebar scrollbar-hide">
            <header class="sidebar-header">
                <h3 class="sidebar-title">Treaty_Fabric</h3>
                <button class="scale-btn"><Scale size={14} /></button>
            </header>

            <div class="treaty-stack">
                {#each treaties as treaty}
                    <div
                        class="treaty-card"
                        class:active={treaty.status === "ACTIVE"}
                        transition:slide
                    >
                        <div class="card-meta">
                            <span class="c-id">{treaty.id}</span>
                            <div class="c-status">
                                <div
                                    class="status-pip"
                                    class:on={treaty.status === "ACTIVE"}
                                ></div>
                                <span>{treaty.status}</span>
                            </div>
                        </div>

                        <h4 class="card-title">{treaty.title}</h4>

                        <div class="card-parties">
                            <span class="p-tag">{treaty.parties[0]}</span>
                            <ChevronRight size={10} class="text-white/20" />
                            <span class="p-tag">{treaty.parties[1]}</span>
                        </div>

                        <footer class="card-footer">
                            <div class="trust-metric">
                                <Heart size={10} class="text-rose-400" />
                                <span>{treaty.trustScore}% Trust_PF</span>
                            </div>
                            <button class="terms-btn">View_Terms</button>
                        </footer>
                    </div>
                {/each}
            </div>

            <div class="footer-action">
                <button onclick={proposeTreaty} class="forge-btn">
                    <FileText size={14} />
                    <span>Forge_New_Accord</span>
                </button>
            </div>
        </aside>
    </div>
</div>

<style>
    .diplomacy-shell {
        height: 100%;
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        font-family: "Outfit", sans-serif;
        overflow: hidden;
    }

    .diplomacy-header {
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }

    .logo-box {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #f43f5e, #fb7185);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(244, 63, 94, 0.2);
    }

    .title {
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
        margin: 0;
    }

    .fabric-label {
        font-size: 8px;
        font-weight: 800;
        color: #fb7185;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-style: italic;
    }

    .fabric-pulsar {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #f43f5e;
        box-shadow: 0 0 10px #f43f5e;
        animation: pulse 1s infinite;
    }

    .header-telemetry {
        display: flex;
        gap: 2rem;
    }

    .tel-block {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .tel-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
        margin-bottom: 2px;
    }

    .tel-value {
        font-size: 14px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .tel-divider {
        width: 1px;
        height: 24px;
        background: rgba(255, 255, 255, 0.05);
    }

    .diplomacy-body {
        flex: 1;
        display: flex;
        overflow: hidden;
    }

    .topology-viewport {
        flex: 1;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .topo-background {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .topo-grid {
        position: absolute;
        inset: 0;
        background-image: radial-gradient(
            rgba(255, 255, 255, 0.03) 1px,
            transparent 1px
        );
        background-size: 40px 40px;
        opacity: 0.5;
    }

    .orbit {
        position: absolute;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 50%;
    }

    .ob-1 {
        width: 300px;
        height: 300px;
    }
    .ob-2 {
        width: 450px;
        height: 450px;
    }
    .ob-3 {
        width: 600px;
        height: 600px;
    }

    .node-sphere {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        background: none;
        border: none;
        cursor: pointer;
        z-index: 10;
    }

    .node-sphere:hover {
        transform: scale(1.1) !important;
    }

    .sphere-core {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.4);
        position: relative;
        transition: all 0.3s;
    }

    .node-sphere:hover .sphere-core {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.3);
        color: white;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }

    .sphere-ping {
        position: absolute;
        inset: 0;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: ping 2s infinite;
        opacity: 0;
    }

    .sphere-label {
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }

    .topology-core {
        width: 100px;
        height: 100px;
        background: rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.2);
        border-radius: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 5;
    }

    .core-aura {
        position: absolute;
        inset: -20px;
        background: radial-gradient(
            circle,
            rgba(244, 63, 94, 0.1),
            transparent 70%
        );
        filter: blur(20px);
        animation: pulse 2s infinite;
    }

    .intel-overlay {
        position: absolute;
        bottom: 2.5rem;
        left: 2.5rem;
        background: rgba(10, 15, 25, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 1.5rem;
        min-width: 240px;
    }

    .intel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .intel-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
    }

    .intel-header h3 {
        font-size: 10px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .intel-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
    }

    .intel-item {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .i-label {
        font-size: 7px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
    }

    .i-value {
        font-size: 12px;
        font-weight: 950;
        font-family: "JetBrains Mono", monospace;
        color: white;
    }

    .accord-sidebar {
        width: 380px;
        border-left: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(0, 0, 0, 0.2);
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
    }

    .sidebar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .sidebar-title {
        font-size: 10px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .scale-btn {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.4);
        padding: 0.5rem;
        border-radius: 10px;
        cursor: pointer;
    }

    .treaty-stack {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        overflow-y: auto;
    }

    .treaty-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.5rem;
        transition: all 0.3s;
    }

    .treaty-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .treaty-card.active {
        border-color: rgba(16, 185, 129, 0.1);
        background: rgba(16, 185, 129, 0.02);
    }

    .card-meta {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .c-id {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.15);
    }

    .c-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 7px;
        font-weight: 950;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
    }

    .status-pip {
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #f59e0b;
    }
    .status-pip.on {
        background: #10b981;
    }

    .card-title {
        font-size: 12px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        margin-bottom: 1.25rem;
    }

    .card-parties {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .p-tag {
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.5);
        background: rgba(255, 255, 255, 0.03);
        padding: 4px 10px;
        border-radius: 8px;
    }

    .card-footer {
        padding-top: 1.25rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .trust-metric {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 9px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.3);
    }

    .terms-btn {
        background: none;
        border: none;
        font-size: 8px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.2);
        text-decoration: underline;
        cursor: pointer;
    }

    .footer-action {
        padding-top: 2rem;
    }

    .forge-btn {
        width: 100%;
        padding: 1.25rem;
        background: #f43f5e;
        border: none;
        border-radius: 20px;
        color: white;
        font-size: 11px;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 10px 20px rgba(244, 63, 94, 0.2);
    }

    .forge-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(244, 63, 94, 0.3);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.05);
        }
    }
    @keyframes ping {
        0% {
            opacity: 0.8;
            transform: scale(1);
        }
        100% {
            opacity: 0;
            transform: scale(1.5);
        }
    }

    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
