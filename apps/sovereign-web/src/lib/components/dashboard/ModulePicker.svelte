<script lang="ts">
    import { fade, fly } from "svelte/transition";
    import {
        Search,
        X,
        Package,
        Shield,
        Zap,
        Coins,
        Activity,
        Globe,
        Scale,
        Layers,
        Cpu,
        Terminal,
        Box,
        Boxes,
        Smartphone,
        Palette,
        Type,
        Sparkles,
        Anchor,
        Wind,
        HardDrive,
        ArrowUpRight,
        Eye,
        Database,
        TrendingUp,
    } from "lucide-svelte";

    let { isOpen = $bindable(), onAdd } = $props<{
        isOpen: boolean;
        onAdd: (id: string) => void;
    }>();

    let searchQuery = $state("");

    const categories = [
        {
            id: "core",
            label: "Intelligence_Baselines",
            icon: Zap,
            color: "text-cyan-400",
        },
        {
            id: "finance",
            label: "Economic_Manifolds",
            icon: Coins,
            color: "text-amber-400",
        },
        {
            id: "governance",
            label: "Institutional_Justice",
            icon: Scale,
            color: "text-purple-400",
        },
        {
            id: "security",
            label: "Cybernetic_Trust",
            icon: Shield,
            color: "text-rose-400",
        },
        {
            id: "discovery",
            label: "Sovereign_Discovery",
            icon: Globe,
            color: "text-emerald-400",
        },
        {
            id: "biometrics",
            label: "Biological_State",
            icon: Activity,
            color: "text-blue-400",
        },
    ];

    const allModules = [
        // CORE
        {
            id: "code_intel",
            label: "Code_Intelligence",
            icon: Cpu,
            category: "core",
            desc: "Neuro-Causal code analysis",
        },
        {
            id: "opencode",
            label: "OpenCode_Matrix",
            icon: Terminal,
            category: "core",
            desc: "Autonomous source refinement",
        },
        {
            id: "research",
            label: "Mission_Control",
            icon: Globe,
            category: "core",
            desc: "Strategic autonomous research",
        },
        {
            id: "icp_console",
            label: "Canister_Console",
            icon: Box,
            category: "core",
            desc: "Direct Substrate interaction",
        },
        {
            id: "decoded",
            label: "Spectral_Decryption",
            icon: Eye,
            category: "core",
            desc: "Speculative Last Supper decoder",
        },
        {
            id: "containment",
            label: "Aether_Hydra_Hub",
            icon: Box,
            category: "core",
            desc: "Wasm + Docker runtime synergy",
        },
        {
            id: "substrate_design",
            label: "Design_Substrate",
            icon: Palette,
            category: "core",
            desc: "System style guide & tokens",
        },
        {
            id: "typo_spec",
            label: "Typographic_Spec",
            icon: Type,
            category: "core",
            desc: "Invisible engineering audit",
        },
        {
            id: "mobile_audit",
            label: "Sovereign_Mobile",
            icon: Smartphone,
            category: "core",
            desc: "Privacy & Convergence audit",
        },
        {
            id: "layout_blueprint",
            label: "Layout_Blueprint",
            icon: Boxes,
            category: "core",
            desc: "Hierarchical box audit",
        },
        {
            id: "redis_engine",
            label: "Redis_Sovereignty",
            icon: Database,
            category: "core",
            desc: "In-memory atomic manifest",
        },
        {
            id: "taste_audit",
            label: "Taste_Audit",
            icon: Sparkles,
            category: "core",
            desc: "Design engineering polish",
        },
        {
            id: "vintage_soul",
            label: "Vintage_Soul",
            icon: Anchor,
            category: "core",
            desc: "Individual vision audit",
        },
        {
            id: "kinetic_audit",
            label: "Kinetic_Audit",
            icon: Wind,
            category: "core",
            desc: "CSS keyframe motion audit",
        },
        {
            id: "storage_audit",
            label: "Storage_Sovereignty",
            icon: HardDrive,
            category: "core",
            desc: "Local-first CRDT audit",
        },

        // FINANCE
        {
            id: "economy",
            label: "Economic_Manifold",
            icon: TrendingUp,
            category: "finance",
            desc: "Real-time protocol state",
        },
        {
            id: "banking",
            label: "Sovereign_Banking",
            icon: Coins,
            category: "finance",
            desc: "Institutional capital rails",
        },
        {
            id: "tokenomics",
            label: "Asset_Plane",
            icon: Layers,
            category: "finance",
            desc: "Aggregated systemic supply",
        },

        // GOVERNANCE
        {
            id: "governance",
            label: "Governance_Court",
            icon: Scale,
            category: "governance",
            desc: "Judicial policy arbitration",
        },
        {
            id: "policy",
            label: "Policy_Fabricator",
            icon: Terminal,
            category: "governance",
            desc: "Algorithmic law weaving",
        },
        {
            id: "diplomacy",
            label: "Diplomacy_Forge",
            icon: Globe,
            category: "governance",
            desc: "Cross-chain trust topology",
        },

        // SECURITY
        {
            id: "gate",
            label: "Security_Gate",
            icon: Shield,
            category: "security",
            desc: "NIST AAL3 access control",
        },
        {
            id: "resonance_cortex",
            label: "Resonance_Cortex",
            icon: Activity,
            category: "security",
            desc: "Systemic coherence monitoring",
        },
        {
            id: "audit",
            label: "Adjoint_Auditor",
            icon: Search,
            category: "security",
            desc: "Continuous formal verification",
        },
    ];

    let filteredModules = $derived(
        allModules.filter(
            (m) =>
                m.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
                m.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
                m.desc.toLowerCase().includes(searchQuery.toLowerCase()),
        ),
    );
</script>

{#if isOpen}
    <div
        class="manifest-overlay"
        transitionfade={{ duration: 300 }}
        onclick={() => (isOpen = false)}
        onkeydown={(e) => e.key === "Escape" && (isOpen = false)}
        role="button"
        tabindex="0"
    >
        <div
            class="manifest-manifold"
            onclick={(e) => e.stopPropagation()}
            role="presentation"
            transitionfly={{ y: 40, duration: 600 }}
        >
            <div class="manifold-glass"></div>

            <!-- Header Section -->
            <header class="manifest-header">
                <div class="header-content">
                    <div class="header-glyph"></div>
                    <div>
                        <h2 class="manifest-title">
                            Instantiate_Manifold_Dimension
                        </h2>
                        <p class="manifest-subtitle">
                            PROTOCOL ACTIVE // SELECT COORDINATES TO MANIFEST
                        </p>
                    </div>
                </div>
                <button onclick={() => (isOpen = false)} class="close-btn">
                    <X size={20} />
                </button>
            </header>

            <!-- Search Stratum -->
            <div class="search-stratum">
                <div class="search-box">
                    <Search size={16} class="text-white/20" />
                    <input
                        bind:value={searchQuery}
                        placeholder="SEARCH PROTOCOL_DIMENSIONS..."
                        autocomplete="off"
                    />
                    <div class="search-indicator">SCANNING...</div>
                </div>
            </div>

            <!-- Dimensions Scroll -->
            <div class="manifest-body scrollbar-hide">
                {#each categories as cat}
                    {#if filteredModules.some((m) => m.category === cat.id)}
                        <section class="category-block">
                            <header class="category-header">
                                <cat.icon size={14} class={cat.color} />
                                <h3 class="cat-label">{cat.label}</h3>
                                <div class="cat-line"></div>
                            </header>

                            <div class="dimension-grid">
                                {#each filteredModules.filter((m) => m.category === cat.id) as mod}
                                    <button
                                        class="dimension-card group"
                                        onclick={() => {
                                            onAdd(mod.id);
                                            isOpen = false;
                                        }}
                                    >
                                        <div class="card-aura"></div>
                                        <div class="card-content">
                                            <div class="card-header">
                                                <div
                                                    class="icon-vessel {cat.color}"
                                                >
                                                    <mod.icon size={18} />
                                                </div>
                                                <ArrowUpRight
                                                    size={12}
                                                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                                                />
                                            </div>
                                            <span class="card-title"
                                                >{mod.label}</span
                                            >
                                            <p class="card-desc">{mod.desc}</p>
                                        </div>
                                    </button>
                                {/each}
                            </div>
                        </section>
                    {/if}
                {/each}

                {#if filteredModules.length === 0}
                    <div class="empty-manifest">
                        <Package size={48} class="opacity-10 mb-6" />
                        <span
                            >No matching dimensions found in protocol registry</span
                        >
                    </div>
                {/if}
            </div>

            <!-- Footer Stratum -->
            <footer class="manifest-footer">
                <div class="flex items-center gap-3">
                    <div class="pulse-dot"></div>
                    <span class="footer-label"
                        >Institutional_Orchestration_Layer_v4.8</span
                    >
                </div>
                <div class="footer-stats">
                    <span>CORES_AVAILABLE: 1,024</span>
                    <div class="h-4 w-px bg-white/10 mx-4"></div>
                    <span class="text-cyan-400">STATUS: READY</span>
                </div>
            </footer>
        </div>
    </div>
{/if}

<style>
    .manifest-overlay {
        position: fixed;
        inset: 0;
        z-index: 10000;
        background: rgba(2, 4, 8, 0.6);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        font-family: "Outfit", sans-serif;
    }

    .manifest-manifold {
        position: relative;
        width: 100%;
        max-width: 900px;
        max-height: 85vh;
        background: rgba(10, 5, 20, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 40px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.7);
    }

    .manifold-glass {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.02),
            transparent
        );
        pointer-events: none;
    }

    .manifest-header {
        padding: 2.5rem 3rem;
        background: rgba(255, 255, 255, 0.01);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-content {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .header-glyph {
        width: 12px;
        height: 12px;
        background: #22d3ee;
        transform: rotate(45deg);
        box-shadow: 0 0 15px #22d3ee;
    }
    .manifest-title {
        font-size: 18px;
        font-weight: 950;
        text-transform: uppercase;
        color: white;
        letter-spacing: -0.02em;
    }
    .manifest-subtitle {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-top: 4px;
    }

    .close-btn {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        width: 44px;
        height: 44px;
        color: white/40;
        cursor: pointer;
        transition: all 0.3s;
    }
    .close-btn:hover {
        background: rgba(244, 63, 94, 0.1);
        border-color: rgba(244, 63, 94, 0.3);
        color: #f43f5e;
    }

    .search-stratum {
        padding: 1.5rem 3rem;
        background: rgba(0, 0, 0, 0.2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .search-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 0 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        height: 56px;
    }

    .search-box input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        outline: none;
        letter-spacing: 0.1em;
    }
    .search-indicator {
        font-size: 7px;
        font-weight: 950;
        color: #10b981;
        animation: pulse 2s infinite;
    }

    .manifest-body {
        flex: 1;
        overflow-y: auto;
        padding: 3rem;
    }

    .category-block {
        margin-bottom: 3.5rem;
    }
    .category-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .cat-label {
        font-size: 10px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        white-space: nowrap;
    }
    .cat-line {
        height: 1px;
        flex: 1;
        background: linear-gradient(
            to right,
            rgba(255, 255, 255, 0.1),
            transparent
        );
    }

    .dimension-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1.5rem;
    }

    .dimension-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 1.75rem;
        text-align: left;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
    }

    .dimension-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .card-aura {
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 100% 0%,
            rgba(34, 211, 238, 0.03),
            transparent 70%
        );
        pointer-events: none;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .icon-vessel {
        width: 44px;
        height: 44px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }
    .dimension-card:hover .icon-vessel {
        transform: scale(1.1);
        background: rgba(255, 255, 255, 0.05);
    }

    .card-title {
        font-size: 12px;
        font-weight: 950;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        display: block;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.3);
        line-height: 1.6;
    }

    .manifest-footer {
        padding: 1.5rem 3rem;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        background: #22d3ee;
        border-radius: 50%;
        box-shadow: 0 0 10px #22d3ee;
        animation: pulse 2s infinite;
    }
    .footer-label {
        font-size: 8px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .footer-stats {
        display: flex;
        align-items: center;
        font-size: 8px;
        font-weight: 950;
        color: rgba(255, 255, 255, 0.3);
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
    }
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
</style>
