<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { fade, fly, scale } from "svelte/transition";
    import {
        ShoppingBag,
        Truck,
        Cpu,
        Map,
        Clock,
        Package,
        Zap,
        ShieldCheck,
        Star,
        Navigation,
        Search,
        Layers,
        Coffee,
        Server,
        Bot,
        BrainCircuit,
        Banknote,
        Sparkles,
        TrendingUp,
        Microscope,
        CircuitBoard,
        Gavel,
        ArrowRightLeft,
        Coins,
        Receipt,
        Globe,
        Sun,
        Database,
        Palette,
        Stethoscope,
        GraduationCap,
        ShieldAlert,
        Fingerprint,
        Radar,
        Activity,
        Waypoints,
        Link,
        Leaf,
        Atom,
        Container,
        Code,
    } from "lucide-svelte";

    type AgoraService = {
        id: string;
        type:
            | "STUFF"
            | "MOBILITY"
            | "GIG"
            | "COMPUTE"
            | "SPACE"
            | "CAPITAL"
            | "ASSET"
            | "NFT"
            | "TOKEN"
            | "AGENT"
            | "FINANCE"
            | "INDUSTRIAL"
            | "CONTRACT"
            | "CHIP"
            | "SUPPLY"
            | "LIFE"
            | "GOV"
            | "ENERGY"
            | "DATA"
            | "CRAFT"
            | "PREDICT"
            | "RISK"
            | "IP"
            | "FRONTIER"
            | "SOCIAL"
            | "SYNTH"
            | "REGEN"
            | "QUANTUM";
        title: string;
        provider: string;
        price: number;
        currency:
            | "AGE"
            | "RES"
            | "ETH"
            | "UCT"
            | "SOL"
            | "USD"
            | "JPY"
            | "YES"
            | "NO"
            | "SYN";
        rating: number;
        eta: string;
        icon: any;
        tags: string[];
    };

    let activeTab = $state("market"); // 'market' | 'logistics' | 'bounties' | 'tokenize'
    let searchQuery = $state("");

    const services: AgoraService[] = [
        // Synthetic Assets & Derivatives
        {
            id: "srv-039",
            type: "SYNTH",
            title: "Hyper-Inverse S&P 500",
            provider: "Spectral_Synths",
            price: 45,
            currency: "SYN",
            rating: 5.0,
            eta: "Drift_Adjusted",
            icon: Link,
            tags: ["Synth", "Short", "Derivative"],
        },

        // Regen & Ecological Credits
        {
            id: "srv-040",
            type: "REGEN",
            title: "Regen-Soil Credit v1",
            provider: "Gaia_Registry",
            price: 12,
            currency: "RES",
            rating: 5.0,
            eta: "Oracled_Sync",
            icon: Leaf,
            tags: ["Carbon", "Ecological", "RWA"],
        },

        // Quantum & Advanced Security
        {
            id: "srv-041",
            type: "QUANTUM",
            title: "Quantum-Safe Tunnel",
            provider: "Hilbert_Security",
            price: 50,
            currency: "UCT",
            rating: 5.0,
            eta: "Instant_Entangle",
            icon: Atom,
            tags: ["Security", "Post_Quantum", "AAL5"],
        },

        // Prediction Markets (Polymarket Equivalent)
        {
            id: "srv-034",
            type: "PREDICT",
            title: "Fed Pivot by Q4 2026",
            provider: "Spectral_Oracle",
            price: 0.65,
            currency: "YES",
            rating: 5.0,
            eta: "Market_Live",
            icon: Activity,
            tags: ["Truth_Market", "Finance", "Predict"],
        },

        // Risk & Insurance
        {
            id: "srv-035",
            type: "RISK",
            title: "Vault Settlement Insurance",
            provider: "Sovereign_Surety",
            price: 120,
            currency: "UCT",
            rating: 4.9,
            eta: "Active_Policy",
            icon: ShieldAlert,
            tags: ["Insurance", "Risk", "Institutional"],
        },

        // Intellectual Property (IP Shards)
        {
            id: "srv-036",
            type: "IP",
            title: "Patent Shard: ZK-Silicon",
            provider: "Lex_Sovereign",
            price: 2500,
            currency: "UCT",
            rating: 5.0,
            eta: "License_Verified",
            icon: Fingerprint,
            tags: ["IP", "Silicon", "Royalty_Bearing"],
        },

        // Frontier Tech (Space/Satellite)
        {
            id: "srv-037",
            type: "FRONTIER",
            title: "Satellite Bandwidth Bridge",
            provider: "Orbital_Mesh",
            price: 5,
            currency: "RES",
            rating: 5.0,
            eta: "Low_Orbit_Link",
            icon: Radar,
            tags: ["Space", "Telecom", "Low_Lat"],
        },

        // Social & Human Capital
        {
            id: "srv-038",
            type: "SOCIAL",
            title: "Reputation Bond (AAL4)",
            provider: "Citizen_Registry",
            price: 500,
            currency: "AGE",
            rating: 5.0,
            eta: "Soulbound_Link",
            icon: Waypoints,
            tags: ["SocialFi", "Human_Capital", "Trust"],
        },

        // Life & Academy (Longevity, Health, Learning)
        {
            id: "srv-028",
            type: "LIFE",
            title: "Longevity Protocol v2",
            provider: "BioFlow_Labs",
            price: 2500,
            currency: "UCT",
            rating: 5.0,
            eta: "Bio-Sync_Session",
            icon: Stethoscope,
            tags: ["Health", "Science", "Bio"],
        },
        {
            id: "srv-029",
            type: "LIFE",
            title: "Advanced ZK-Cryptography",
            provider: "AGE_Academy",
            price: 500,
            currency: "AGE",
            rating: 4.9,
            eta: "Self_Paced",
            icon: GraduationCap,
            tags: ["Education", "Pro", "Learning"],
        },

        // Energy & Infrastructure
        {
            id: "srv-030",
            type: "ENERGY",
            title: "Solar Microgrid Shard",
            provider: "Nagano_SunMesh",
            price: 15,
            currency: "RES",
            rating: 5.0,
            eta: "Instant_Grid_Link",
            icon: Sun,
            tags: ["Energy", "Green", "Utility"],
        },

        // Governance & Citizenship
        {
            id: "srv-031",
            type: "GOV",
            title: "Governance Weight (1k)",
            provider: "Sovereign_Council",
            price: 1000,
            currency: "AGE",
            rating: 4.8,
            eta: "Voter_Sync",
            icon: Globe,
            tags: ["Gov", "Voting", "Citizenship"],
        },

        // Data & Personal Graph
        {
            id: "srv-032",
            type: "DATA",
            title: "Personal Data License",
            provider: "Self_Sovereign_Data",
            price: 50,
            currency: "RES",
            rating: 5.0,
            eta: "Audit_Ready",
            icon: Database,
            tags: ["Data", "Monetization", "Privacy"],
        },

        // High-end Craft & Curated Art
        {
            id: "srv-033",
            type: "CRAFT",
            title: "Bespoke Neural Synth",
            provider: "Void_Artisan_Pool",
            price: 5.5,
            currency: "ETH",
            rating: 5.0,
            eta: "Mint_on_Demand",
            icon: Palette,
            tags: ["Art", "Custom", "High_End"],
        },

        // Supply Chain Finance & Credit
        {
            id: "srv-025",
            type: "SUPPLY",
            title: "Dynamic Invoice Factoring",
            provider: "TradeFlow_DAO",
            price: 0.15,
            currency: "UCT",
            rating: 5.0,
            eta: "Instant_Payout",
            icon: Receipt,
            tags: ["Finance", "Supply_Chain", "Credit"],
        },
        {
            id: "srv-026",
            type: "SUPPLY",
            title: "Inventory-Linked Credit",
            provider: "Logistics_Registry",
            price: 1500,
            currency: "UCT",
            rating: 4.8,
            eta: "Approved_by_AAL3",
            icon: Container,
            tags: ["Lending", "Asset_Backed", "Industrial"],
        },
        {
            id: "srv-027",
            type: "SUPPLY",
            title: "Pre-Shipment Capital",
            provider: "Nagano_Silicon_Fab",
            price: 5000,
            currency: "AGE",
            rating: 4.9,
            eta: "Production_Sync",
            icon: Banknote,
            tags: ["Manufacturing", "Credit", "B2B"],
        },

        // AI Agents & Autonomous Skills
        {
            id: "srv-016",
            type: "AGENT",
            title: "Quant-Alpha Trading Bot",
            provider: "Spectral_Bourse",
            price: 85,
            currency: "AGE",
            rating: 5.0,
            eta: "Instant_Deploy",
            icon: Bot,
            tags: ["AI_Agent", "Finance", "Bot_Store"],
        },
        {
            id: "srv-017",
            type: "AGENT",
            title: "Concierge: Real Estate Skill",
            provider: "Neural_Foundry",
            price: 120,
            currency: "RES",
            rating: 4.9,
            eta: "Module_Load",
            icon: BrainCircuit,
            tags: ["Skill", "Automation", "Agent_Skill"],
        },

        // Semiconductor Industry (Industrial/Chips)
        {
            id: "srv-022",
            type: "INDUSTRIAL",
            title: "5nm Wafer Capacity (Lot)",
            provider: "Fujitsu_Foundry_Nagano",
            price: 150000,
            currency: "JPY",
            rating: 5.0,
            eta: "Q3_2026",
            icon: Microscope,
            tags: ["Semiconductor", "Foundry", "Industrial"],
        },
        {
            id: "srv-023",
            type: "CHIP",
            title: "Sovereign GPU: Neon-8",
            provider: "Nagano_Silicon_Fab",
            price: 2400,
            currency: "UCT",
            rating: 4.9,
            eta: "2 weeks",
            icon: CircuitBoard,
            tags: ["Hardware", "GPU", "AI_Training"],
        },

        // Finance: Yield, Loans, & Credit
        {
            id: "srv-019",
            type: "FINANCE",
            title: "Yield Booster: Photonic Pool",
            provider: "Economic_Manifold",
            price: 0,
            currency: "UCT",
            rating: 4.9,
            eta: "12.2% APY",
            icon: TrendingUp,
            tags: ["DeFi", "Staking", "Yield"],
        },
        {
            id: "srv-020",
            type: "FINANCE",
            title: "Hyper-Collateralized Loan",
            provider: "Hilbert_Capital",
            price: 50000,
            currency: "UCT",
            rating: 5.0,
            eta: "Instant_Approval",
            icon: Coins,
            tags: ["Credit", "Loan", "Institutional"],
        },

        // Contracts & Smart Legal
        {
            id: "srv-018",
            type: "CONTRACT",
            title: "Smart Lease Agreement",
            provider: "Lex_Sovereign",
            price: 25,
            currency: "UCT",
            rating: 5.0,
            eta: "ZK_Verified",
            icon: Gavel,
            tags: ["Legal", "Contract", "Automation"],
        },
        {
            id: "srv-024",
            type: "CONTRACT",
            title: "Cross-Border Settlement",
            provider: "Global_Clearing_DAO",
            price: 0.1,
            currency: "ETH",
            rating: 4.8,
            eta: "Instant",
            icon: ArrowRightLeft,
            tags: ["Settlement", "SWIFT_Alternative", "Crypto"],
        },

        // Physical / Delivery
        {
            id: "srv-001",
            type: "STUFF",
            title: "Sovereign Lens v4",
            provider: "Void_Fab_09",
            price: 450,
            currency: "AGE",
            rating: 4.9,
            eta: "2 hours",
            icon: Package,
            tags: ["Hardware", "Verified"],
        },

        // Space / Airbnb / Real Estate
        {
            id: "srv-008",
            type: "SPACE",
            title: "Nagano Zen Suite (Private)",
            provider: "Citizen_Host_88",
            price: 85,
            currency: "RES",
            rating: 4.9,
            eta: "Instant_Book",
            icon: Map,
            tags: ["Short_Term", "Airbnb_Equivalent"],
        },
        {
            id: "srv-009",
            type: "ASSET",
            title: "Fractional: Luxury Condo SF",
            provider: "Real_Estate_Oracle",
            price: 1200,
            currency: "UCT",
            rating: 5.0,
            eta: "Deed_Verified",
            icon: ShieldCheck,
            tags: ["Real_Estate", "Yield_Bearing", "RWA"],
        },
        {
            id: "srv-011",
            type: "ASSET",
            title: "Commercial: Node-Z Headquarters",
            provider: "Sovereign_REIT",
            price: 45000,
            currency: "UCT",
            rating: 5.0,
            eta: "Institutional",
            icon: Server,
            tags: ["Commercial", "High_Cap"],
        },

        // NFTs / Digital Collectibles
        {
            id: "srv-013",
            type: "NFT",
            title: "Cyber-Fragment #402",
            provider: "Art_Minter_DAO",
            price: 2.5,
            currency: "ETH",
            rating: 4.9,
            eta: "Mint_Now",
            icon: Sparkles,
            tags: ["NFT", "Collective", "OpenSea_Equivalent"],
        },

        // Capital / Stocks
        {
            id: "srv-010",
            type: "CAPITAL",
            title: "NexaAI Equity (Pre-IPO)",
            provider: "Spectral_Bourse",
            price: 12.5,
            currency: "AGE",
            rating: 5.0,
            eta: "Market_Order",
            icon: Zap,
            tags: ["Stocks", "Robinhood", "Equity"],
        },
        {
            id: "srv-012",
            type: "CAPITAL",
            title: "BioFlow Labs Shard",
            provider: "Ventures_DAO",
            price: 0.85,
            currency: "AGE",
            rating: 4.8,
            eta: "Liquid",
            icon: Zap, // Changed from Heart
            tags: ["Biotech", "Growth"],
        },
        {
            id: "srv-021",
            type: "CAPITAL",
            title: "Tokenized S&P 500 Shard",
            provider: "Spectral_Capital",
            price: 450,
            currency: "USD",
            rating: 5.0,
            eta: "Market_Hours",
            icon: Banknote,
            tags: ["Stocks", "Institutional", "Robinhood"],
        },

        // Tokenization / Exchange (Coinbase/Kraken equivalent)
        {
            id: "srv-014",
            type: "TOKEN",
            title: "Tokenize Physical Gold",
            provider: "Sovereign_Vaults",
            price: 1,
            currency: "UCT",
            rating: 5.0,
            eta: "Audit_Required",
            icon: Cpu,
            tags: ["Tokenization", "RWA", "Safe"],
        },
        {
            id: "srv-015",
            type: "TOKEN",
            title: "Swap ETH for AGE",
            provider: "Spectral_Bourse",
            price: 0,
            currency: "AGE",
            rating: 5.0,
            eta: "Instant",
            icon: Layers,
            tags: ["Exchange", "Coinbase_Equivalent", "DEX"],
        },

        // Gig / Work (Fiverr/Upwork equivalent)
        {
            id: "srv-003",
            type: "GIG",
            title: "ZK-Circuit Audit",
            provider: "Math_Wizards_DA",
            price: 1200,
            currency: "AGE",
            rating: 5.0,
            eta: "2 days",
            icon: Code,
            tags: ["Audit", "Upwork_Equivalent", "Pro"],
        },

        // Mobility (Uber/DoorDash)
        {
            id: "srv-002",
            type: "MOBILITY",
            title: "Drone Delivery: Express",
            provider: "SkyMesh_Logistics",
            price: 5,
            currency: "RES",
            rating: 5.0,
            eta: "8 min",
            icon: Truck,
            tags: ["Speed", "Autonomous", "DoorDash"],
        },
        {
            id: "srv-005",
            type: "MOBILITY",
            title: "Human Transit: Premium",
            provider: "Civic_Rides",
            price: 25,
            currency: "AGE",
            rating: 4.8,
            eta: "4 min",
            icon: Navigation,
            tags: ["Comfort", "Secure", "Uber_Equivalent"],
        },

        // Compute
        {
            id: "srv-004",
            type: "COMPUTE",
            title: "H100 Cluster Access",
            provider: "Nagano_Compute_PoR",
            price: 0.045,
            currency: "AGE",
            rating: 4.9,
            eta: "Instant",
            icon: Server,
            tags: ["GPU", "Cloud", "AWS"],
        },

        // Food
        {
            id: "srv-006",
            type: "STUFF",
            title: "Organic Bio-Fuel Bowl",
            provider: "Hearth_Kitchens",
            price: 15,
            currency: "RES",
            rating: 4.7,
            eta: "12 min",
            icon: Coffee,
            tags: ["Food", "Delivery", "Health"],
        },
    ];

    let myOrders = $state([
        {
            id: "ord-881",
            title: "Sovereign Lens v4",
            status: "IN_TRANSIT",
            progress: 65,
            carrier: "Drone_AX-9",
        },
        {
            id: "ord-992",
            title: "ZK-Circuit Audit",
            status: "PROCESSING",
            progress: 15,
            carrier: "Agent_Zero",
        },
    ]);

    function placeOrder(service: AgoraService) {
        manifold.recordEvent(
            "AGORA_ORDER_PLACED",
            `Fulfillment for ${service.title} initiated via ${service.provider}`, // Changed message
        );
        myOrders = [
            {
                id: `ord-${Date.now()}`,
                title: service.title,
                status: "PENDING",
                progress: 0,
                carrier: service.provider,
            },
            ...myOrders,
        ];
        // In a real app, this would deduct credits and talk to a backend
    }

    const filteredServices = $derived(
        services.filter(
            (s) =>
                s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                s.tags.some((t) =>
                    t.toLowerCase().includes(searchQuery.toLowerCase()),
                ),
        ),
    );
</script>

<div
    class="h-full bg-zinc-950/60 rounded-[3rem] border border-white/5 backdrop-blur-3xl overflow-hidden flex flex-col shadow-2xl relative group"
>
    <!-- Header: Search & Navigation -->
    <div class="p-8 border-b border-white/5 space-y-6 bg-white/[0.02]">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="p-3 bg-cyan-400/20 rounded-2xl text-cyan-400">
                    <ShoppingBag size={20} />
                </div>
                <div>
                    <h2
                        class="text-xs font-black uppercase tracking-widest text-white"
                    >
                        Agora_Omni
                    </h2>
                    <span
                        class="text-[8px] font-black text-white/30 uppercase tracking-widest italic"
                        >Universal_Fulfillment_Network</span
                    >
                </div>
            </div>

            <div
                class="flex gap-1.5 p-1 bg-white/5 rounded-xl border border-white/5"
            >
                {#each ["market", "logistics", "tokenize", "bounties"] as tab}
                    <button
                        onclick={() => (activeTab = tab)}
                        class="px-4 py-1.5 text-[8px] font-black uppercase tracking-widest rounded-lg transition-all {activeTab ===
                        tab
                            ? 'bg-white text-black'
                            : 'text-white/40 hover:text-white'}"
                    >
                        {tab}
                    </button>
                {/each}
            </div>
        </div>

        <div class="relative group/search">
            <Search
                size={14}
                class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20 group-hover/search:text-cyan-400 transition-colors"
            />
            <input
                type="text"
                placeholder="Search rentals, synths, predictions, regen, or compute..."
                bind:value={searchQuery}
                class="w-full bg-black/40 border border-white/5 rounded-2xl py-3 pl-12 pr-4 text-xs font-bold text-white placeholder:text-white/10 focus:border-cyan-400/50 outline-none transition-all"
            />
        </div>
    </div>

    <!-- Active Content Area -->
    <div class="flex-1 overflow-y-auto p-6 no-scrollbar">
        {#if activeTab === "market"}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4" in:fade>
                {#each filteredServices as service}
                    <button
                        onclick={() => placeOrder(service)}
                        class="text-left bg-white/[0.03] border border-white/5 rounded-[2rem] p-5 hover:border-cyan-400/30 hover:bg-white/[0.05] transition-all group/card relative overflow-hidden"
                    >
                        <!-- Category Accent -->
                        <div
                            class="absolute top-0 right-0 p-3 opacity-10 group-hover/card:opacity-30 transition-opacity"
                        >
                            <span class="text-[40px] font-black italic"
                                >{service.type[0]}</span
                            >
                        </div>

                        <div class="flex justify-between items-start mb-4">
                            <div
                                class="p-3 bg-white/5 rounded-2xl group-hover/card:scale-110 transition-transform"
                            >
                                <service.icon
                                    size={20}
                                    class="text-white/60 group-hover/card:text-cyan-400"
                                />
                            </div>
                            <div class="flex flex-col items-end">
                                <div
                                    class="flex items-center gap-1 text-amber-400"
                                >
                                    <Star size={10} fill="currentColor" />
                                    <span class="text-[10px] font-black"
                                        >{service.rating}</span
                                    >
                                </div>
                                <span
                                    class="text-[8px] font-black text-white/20 uppercase tracking-widest mt-1"
                                    >{service.eta}</span
                                >
                            </div>
                        </div>

                        <div class="space-y-1">
                            <h4
                                class="text-sm font-black text-white group-hover/card:text-cyan-400 transition-colors"
                            >
                                {service.title}
                            </h4>
                            <p
                                class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                            >
                                via {service.provider}
                            </p>
                        </div>

                        <div
                            class="mt-6 flex items-center justify-between pt-4 border-t border-white/5"
                        >
                            <div class="flex gap-1.5 overflow-hidden">
                                {#each service.tags as tag}
                                    <span
                                        class="text-[7px] font-black text-white/20 uppercase px-2 py-0.5 bg-white/5 rounded border border-white/5"
                                        >{tag}</span
                                    >
                                {/each}
                            </div>
                            <span
                                class="text-lg font-black text-white tracking-tighter italic"
                                >{service.price}
                                <span
                                    class="text-[10px] text-zinc-500 font-bold"
                                    >{service.currency}</span
                                ></span
                            >
                        </div>
                    </button>
                {/each}
            </div>
        {:else if activeTab === "logistics"}
            <div class="space-y-6" in:fly={{ y: 20 }}>
                <!-- Interactive Fulfillment Map -->
                <div
                    class="aspect-[2/1] bg-black/40 rounded-3xl border border-white/10 relative overflow-hidden group/map"
                >
                    <div
                        class="absolute inset-0 opacity-20 perspective-grid"
                    ></div>
                    <div
                        class="absolute inset-0 flex items-center justify-center"
                    >
                        <Navigation
                            size={40}
                            class="text-cyan-400/20 animate-pulse"
                        />
                        <div
                            class="absolute w-2 h-2 bg-emerald-400 rounded-full shadow-[0_0_10px_#10b981] animate-ping"
                            style="top: 30%; left: 40%;"
                        ></div>
                        <div
                            class="absolute w-2 h-2 bg-cyan-400 rounded-full shadow-[0_0_10px_#22d3ee] animate-bounce"
                            style="top: 60%; left: 70%;"
                        ></div>
                    </div>
                    <div
                        class="absolute bottom-4 left-4 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10"
                    >
                        <span
                            class="text-[8px] font-black text-cyan-400 uppercase tracking-widest"
                            >Active_Drift: Tracking_Live</span
                        >
                    </div>
                </div>

                <div class="space-y-3">
                    <h3
                        class="text-[10px] font-black text-white/20 uppercase tracking-widest px-2"
                    >
                        Transit_Protocol
                    </h3>
                    {#each myOrders as order}
                        <div
                            class="p-5 bg-white/[0.03] border border-white/5 rounded-3xl space-y-4"
                        >
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-3">
                                    <div
                                        class="w-10 h-10 rounded-xl bg-cyan-400/10 flex items-center justify-center text-cyan-400"
                                    >
                                        {#if order.status === "IN_TRANSIT"}
                                            <Truck size={18} />
                                        {:else}
                                            <Clock size={18} />
                                        {/if}
                                    </div>
                                    <div>
                                        <h5
                                            class="text-xs font-black text-white uppercase"
                                        >
                                            {order.title}
                                        </h5>
                                        <span
                                            class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                                            >{order.carrier}</span
                                        >
                                    </div>
                                </div>
                                <span
                                    class="text-[8px] font-black text-cyan-400 uppercase tracking-[0.2em]"
                                    >{order.status}</span
                                >
                            </div>
                            <div class="space-y-2">
                                <div
                                    class="h-1 bg-white/5 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="h-full bg-cyan-400 shadow-[0_0_10px_rgba(34,211,238,0.5)] transition-all duration-1000"
                                        style="width: {order.progress}%"
                                    ></div>
                                </div>
                                <div
                                    class="flex justify-between text-[7px] font-black text-white/20 uppercase"
                                >
                                    <span>Origin_Fab</span>
                                    <span>Citizen_Drop</span>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeTab === "tokenize"}
            <div
                class="h-full flex flex-col items-center justify-center text-center p-8 space-y-8"
                in:fade
            >
                <div
                    class="w-24 h-24 bg-cyan-400/10 rounded-[2.5rem] border border-cyan-400/30 flex items-center justify-center text-cyan-400 animate-pulse"
                >
                    <Cpu size={48} />
                </div>
                <div class="space-y-4">
                    <h3
                        class="text-2xl font-black italic uppercase tracking-tighter text-white"
                    >
                        Tokenize_Reality
                    </h3>
                    <p
                        class="text-[10px] font-black text-white/30 uppercase max-w-xs leading-relaxed tracking-widest"
                    >
                        Convert physical real estate, private equity, or digital
                        art into tradeable sovereign shards.
                    </p>
                </div>
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full">
                    <button
                        class="p-4 bg-white/5 border border-white/10 rounded-3xl hover:border-cyan-400/50 transition-all group text-center"
                    >
                        <Map
                            size={20}
                            class="mx-auto mb-2 text-white/20 group-hover:text-cyan-400"
                        />
                        <span
                            class="text-[7px] font-black uppercase text-white/40 group-hover:text-white"
                            >Real_Estate</span
                        >
                    </button>
                    <button
                        class="p-4 bg-white/5 border border-white/10 rounded-3xl hover:border-cyan-400/50 transition-all group text-center"
                    >
                        <Sparkles
                            size={20}
                            class="mx-auto mb-2 text-white/20 group-hover:text-cyan-400"
                        />
                        <span
                            class="text-[7px] font-black uppercase text-white/40 group-hover:text-white"
                            >Digital_Art</span
                        >
                    </button>
                    <button
                        class="p-4 bg-white/5 border border-white/10 rounded-3xl hover:border-cyan-400/50 transition-all group text-center"
                    >
                        <Fingerprint
                            size={20}
                            class="mx-auto mb-2 text-white/20 group-hover:text-cyan-400"
                        />
                        <span
                            class="text-[7px] font-black uppercase text-white/40 group-hover:text-white"
                            >Patent/IP</span
                        >
                    </button>
                    <button
                        class="p-4 bg-white/5 border border-white/10 rounded-3xl hover:border-cyan-400/50 transition-all group text-center"
                    >
                        <Waypoints
                            size={20}
                            class="mx-auto mb-2 text-white/20 group-hover:text-cyan-400"
                        />
                        <span
                            class="text-[7px] font-black uppercase text-white/40 group-hover:text-white"
                            >Human_Capital</span
                        >
                    </button>
                </div>
                <button
                    class="w-full py-4 bg-cyan-400 text-black text-[10px] font-black uppercase tracking-widest rounded-2xl hover:scale-105 transition-all shadow-xl shadow-cyan-400/20"
                >
                    Initialize_Shard_Protocol
                </button>
            </div>
        {:else if activeTab === "bounties"}
            <div
                class="flex flex-col items-center justify-center h-full text-center space-y-6 py-12"
                in:scale
            >
                <div
                    class="p-6 bg-purple-500/10 rounded-full border border-purple-500/20"
                >
                    <Zap size={40} class="text-purple-400 animate-pulse" />
                </div>
                <div class="space-y-2 max-w-xs">
                    <h3
                        class="text-xl font-black italic tracking-tighter uppercase text-purple-400"
                    >
                        GIG_RESONANCE
                    </h3>
                    <p
                        class="text-[10px] font-black text-white/20 uppercase leading-relaxed tracking-widest"
                    >
                        Post or complete institutional tasks. Zero-Trust
                        verification (AAL3) mandatory.
                    </p>
                </div>
                <button
                    class="px-8 py-3 bg-purple-500 text-white text-[10px] font-black uppercase tracking-widest rounded-xl hover:scale-105 transition-all shadow-xl shadow-purple-500/20"
                >
                    Host_a_Bounty
                </button>
            </div>
        {/if}
    </div>

    <!-- System Status Bar -->
    <div
        class="p-6 border-t border-white/5 bg-black/40 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <ShieldCheck size={14} class="text-emerald-400" />
            <span
                class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                >Liquidity: Institutional</span
            >
        </div>
        <div
            class="flex items-center gap-4 text-white/40 text-[9px] font-black uppercase italic"
        >
            <span>24h Vol: 1.4B AGE</span>
            <div class="h-4 w-[1px] bg-white/10"></div>
            <span>Global_Sync: 99.8%</span>
        </div>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }

    .perspective-grid {
        background-image: linear-gradient(
                rgba(255, 255, 255, 0.05) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.05) 1px,
                transparent 1px
            );
        background-size: 50px 50px;
        transform: rotateX(60deg) translateY(-20%);
    }
</style>
