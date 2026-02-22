<script lang="ts">
    import {
        Grid,
        Smartphone,
        Utensils,
        ShoppingBag,
        Bike,
        Car,
        Plane,
        Train,
        Zap,
        Globe,
        ChevronRight,
        Star,
        Apple,
        Coffee,
        Ticket,
        Droplets,
        PhoneCall,
        Plus,
        Lock,
        Eye,
        MousePointer2,
        ShieldCheck,
        Building2,
        Vote,
        Stethoscope,
        Scale,
        Activity,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";

    import Tokenomics from "./Tokenomics.svelte";

    let activeTab = $state("EVENTS"); // "EVENTS", "MINI-PROGRAMS", "X-ROAD", "TOKENOMICS"
    let signingAction = $state<string | null>(null);
    let isVerifying = $state(false);
    let devMode = $state(false);
    let testUrl = $state("");
    let devTaps = $state(0);

    const miniApps = [
        {
            name: "Mesh Pay",
            category: "Finance",
            icon: Zap,
            status: "Official",
        },
        {
            name: "Bio-Scan",
            category: "Health",
            icon: Activity,
            status: "Verified",
        },
        {
            name: "Void Food",
            category: "Utility",
            icon: Utensils,
            status: "Verified",
        },
        {
            name: "Tube-Ex",
            category: "Transit",
            icon: Car,
            status: "Third-Party",
        },
        {
            name: "Soul-Bind",
            category: "Ritual",
            icon: Ticket,
            status: "Official",
        },
        {
            name: "L-Koffee",
            category: "Social",
            icon: Coffee,
            status: "Third-Party",
        },
    ];

    function handleDevTap() {
        devTaps++;
        if (devTaps >= 7 && !devMode) {
            devMode = true;
        }
    }

    function initiateSignature(action: string) {
        signingAction = action;
        isVerifying = false;
    }

    async function authorizeSignature() {
        isVerifying = true;
        await new Promise((r) => setTimeout(r, 2000));
        signingAction = null;
        isVerifying = false;
        // Show success toast/alert would be good here
        alert("QUALIFIED SIGNATURE GENERATED // ACTION SECURED");
    }

    const lifeEvents = [
        {
            label: "Entrepreneurship",
            meta: "Start Business in 15m",
            icon: Building2,
            color: "text-cyan-400",
            desc: "Secure company formation with legal EU/Global recognition.",
        },
        {
            label: "Civic Duty",
            meta: "i-Voting / Digital Signature",
            icon: Vote,
            color: "text-emerald-400",
            desc: "Participate in governance with end-to-end verifiability.",
        },
        {
            label: "Healthcare",
            meta: "e-Prescriptions / Records",
            icon: Stethoscope,
            color: "text-red-400",
            desc: "Manage medical heritage and proactive prescriptions.",
        },
        {
            label: "Sovereign Justice",
            meta: "Verified Legal Signing",
            icon: Scale,
            color: "text-purple-400",
            desc: "Sign high-ticket contracts with QES certified identity.",
        },
    ];

    const logisticEvents = [
        {
            label: "Mobility",
            meta: "Digital License / Permits",
            icon: Car,
            color: "text-amber-400",
        },
        {
            label: "Global Logistics",
            meta: "Parcel Flow / Air Sync",
            icon: Plane,
            color: "text-blue-400",
        },
    ];

    const xRoadLogs = [
        {
            entity: "Population Registry",
            action: "Address Update",
            time: "12m ago",
            status: "AUTHORIZED",
            color: "bg-emerald-500",
        },
        {
            entity: "Revenue Service",
            action: "Income Data Pull",
            time: "2h ago",
            status: "SYNCED",
            color: "bg-cyan-500",
        },
        {
            entity: "Health Mesh",
            action: "Heritage Access",
            time: "1d ago",
            status: "AUTHORIZED",
            color: "bg-purple-500",
        },
    ];
</script>

<div class="px-8 py-12 max-w-7xl mx-auto" in:fade>
    <!-- Sovereign Hub Header -->
    <div class="mb-16 flex justify-between items-end">
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
            >
                X-Road Federated Mesh // L0
            </div>
            <h1
                class="text-6xl font-black italic uppercase tracking-tighter mb-4"
            >
                Citizen <span class="text-white">Life</span>
            </h1>
            <p
                class="text-lg text-white/40 font-bold max-w-2xl italic flex items-center gap-3"
            >
                <ShieldCheck size={20} class="text-emerald-500" />
                State-certified e-ID active with Qualified Electronic Signature (QES)
            </p>
        </div>
        <div class="flex gap-4">
            {#each ["EVENTS", "MINI-PROGRAMS", "X-ROAD", "TOKENOMICS"] as tab}
                <button
                    onclick={() => (activeTab = tab)}
                    class="px-8 py-3 rounded-xl text-[10px] font-black tracking-widest uppercase transition-all {activeTab ===
                    tab
                        ? 'bg-white text-black'
                        : 'bg-white/5 text-white/40 hover:bg-white/10'}"
                >
                    {tab}
                </button>
            {/each}
        </div>
    </div>

    <!-- Stats Ribbon -->
    <div class="grid grid-cols-4 gap-6 mb-16">
        {#each [{ label: "X-ROAD NODES", val: "0014", color: "text-cyan-400" }, { label: "FEDERATED LATENCY", val: "14ms", color: "text-emerald-400" }, { label: "CITIZEN TRUST RANK", val: "AAA+", color: "text-amber-400" }, { label: "DATA REQUESTS (24H)", val: "18", color: "text-white" }] as stat}
            <div class="glass-panel p-6 border-white/5">
                <div
                    class="text-[10px] font-black text-white/20 uppercase tracking-widest mb-2"
                >
                    {stat.label}
                </div>
                <div
                    class="text-2xl font-black tabular-nums {stat.color} font-mono"
                >
                    {stat.val}
                </div>
            </div>
        {/each}
    </div>

    {#if activeTab === "EVENTS"}
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8" in:fade>
            {#each lifeEvents as e}
                {@const Icon = e.icon}
                <div
                    class="glass-panel p-12 group hover:border-white/10 transition-all cursor-pointer relative overflow-hidden"
                    onclick={() => initiateSignature(e.label)}
                >
                    <div
                        class="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity"
                    >
                        <Icon size={120} />
                    </div>
                    <div class="relative z-10 flex flex-col h-full">
                        <div class="flex items-center gap-4 mb-8">
                            <div
                                class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center {e.color} border border-white/5"
                            >
                                <Icon size={28} />
                            </div>
                            <div>
                                <h3
                                    class="text-2xl font-black italic uppercase tracking-tighter"
                                >
                                    {e.label}
                                </h3>
                                <div
                                    class="text-[10px] font-black text-white/40 tracking-widest uppercase"
                                >
                                    {e.meta}
                                </div>
                            </div>
                        </div>
                        <p
                            class="text-white/40 text-sm font-bold mb-12 max-w-sm italic leading-relaxed"
                        >
                            {e.desc}
                        </p>
                        <button
                            class="w-fit mt-auto px-8 py-3 rounded-lg border border-white/10 text-[10px] font-black tracking-widest uppercase hover:bg-white hover:text-black transition-all"
                        >
                            Initiate Life Event // QES
                        </button>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Signature Overlay -->
        {#if signingAction}
            <div
                class="fixed inset-0 z-[2000] flex items-center justify-center p-8 bg-black/80 backdrop-blur-3xl"
                transition:fade
            >
                <div
                    class="max-w-xl w-full glass-panel p-16 border-white/10 relative overflow-hidden text-center"
                    in:fly={{ y: 100 }}
                >
                    <div
                        class="absolute top-0 left-0 w-full h-1 bg-emerald-500/20"
                    >
                        <div
                            class="h-full bg-emerald-500 transition-all duration-300"
                            style="width: {isVerifying ? '100%' : '0%'}"
                        ></div>
                    </div>

                    <div class="mb-12">
                        <div
                            class="w-24 h-24 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-8"
                        >
                            <ShieldCheck size={48} class="text-emerald-500" />
                        </div>
                        <div
                            class="text-[10px] font-black text-white/20 uppercase tracking-[0.4em] mb-4"
                        >
                            Qualified Electronic Signature
                        </div>
                        <h2
                            class="text-4xl font-black italic uppercase tracking-tighter mb-4"
                        >
                            {signingAction}
                        </h2>
                        <p
                            class="text-white/40 text-xs font-bold font-mono leading-relaxed"
                        >
                            ACTION COMPLIANT WITH eIDAS 2.0 REGULATION. YOUR
                            PRIVATE SPLIT-KEY WILL BE RECONSTRUCTED VIA
                            BIOMETRIC AUTHENTICATION.
                        </p>
                    </div>

                    {#if isVerifying}
                        <div class="space-y-6" in:fade>
                            <div class="flex justify-center gap-2">
                                <div
                                    class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce"
                                    style="animation-delay: 0s"
                                ></div>
                                <div
                                    class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce"
                                    style="animation-delay: 0.1s"
                                ></div>
                                <div
                                    class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce"
                                    style="animation-delay: 0.2s"
                                ></div>
                            </div>
                            <div
                                class="text-[10px] font-black text-emerald-500 tracking-[0.2em] uppercase"
                            >
                                Checking Liveness // Secure Channel Open
                            </div>
                        </div>
                    {:else}
                        <div class="flex flex-col gap-4">
                            <button
                                onclick={authorizeSignature}
                                class="w-full h-20 rounded-2xl bg-emerald-500 text-black font-black italic tracking-[0.2em] text-lg hover:scale-[1.02] transition-all shadow-[0_0_50px_rgba(16,185,129,0.3)] flex items-center justify-center gap-4"
                            >
                                <Smartphone size={24} />
                                AUTHORIZE WITH BIOMETRIC
                            </button>
                            <button
                                onclick={() => (signingAction = null)}
                                class="w-full h-16 rounded-2xl border border-white/10 text-white/40 font-black tracking-widest uppercase text-xs hover:bg-white/5 transition-all"
                            >
                                Abort Transaction
                            </button>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}

        <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
            {#each logisticEvents as e}
                {@const Icon = e.icon}
                <div
                    class="glass-panel p-8 flex items-center justify-between group border-white/5 hover:border-white/10 transition-all cursor-pointer"
                >
                    <div class="flex items-center gap-6">
                        <div
                            class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center {e.color}"
                        >
                            <Icon size={20} />
                        </div>
                        <div>
                            <div
                                class="text-lg font-black italic uppercase tracking-tighter"
                            >
                                {e.label}
                            </div>
                            <div
                                class="text-[8px] font-black text-white/20 tracking-widest uppercase"
                            >
                                {e.meta}
                            </div>
                        </div>
                    </div>
                    <ChevronRight
                        size={20}
                        class="text-white/10 group-hover:text-white/40 group-hover:translate-x-2 transition-all"
                    />
                </div>
            {/each}
        </div>
    {:else if activeTab === "X-ROAD"}
        <div class="space-y-6" in:fade>
            <div class="flex items-center justify-between px-4">
                <div
                    class="text-[10px] font-black text-white/20 uppercase tracking-widest italic flex items-center gap-3"
                >
                    <Eye size={14} />
                    Data Sovereignty Transparency Log
                </div>
                <button
                    class="text-[10px] font-black text-white/40 hover:text-white transition-colors underline decoration-white/20"
                    >Download Full Audit Ledger</button
                >
            </div>

            {#each xRoadLogs as log}
                <div
                    class="glass-panel p-8 flex items-center gap-8 border-white/5 hover:border-white/10 transition-all"
                >
                    <div class="w-1 h-12 {log.color} rounded-full"></div>
                    <div class="flex-1">
                        <div
                            class="text-lg font-black italic uppercase tracking-tighter"
                        >
                            {log.entity}
                        </div>
                        <div
                            class="text-[10px] font-black text-white/20 tracking-widest uppercase"
                        >
                            {log.action}
                        </div>
                    </div>
                    <div class="text-right">
                        <div
                            class="text-xs font-mono font-black text-white/60 mb-2"
                        >
                            {log.time}
                        </div>
                        <div
                            class="px-3 py-1 rounded bg-white/5 text-[8px] font-black text-white/40 italic tracking-widest uppercase border border-white/5"
                        >
                            {log.status}
                        </div>
                    </div>
                    <button
                        class="p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-all group"
                    >
                        <Lock
                            size={16}
                            class="text-white/20 group-hover:text-cyan-400 transition-colors"
                        />
                    </button>
                </div>
            {/each}

            <div
                class="p-12 border-2 border-dashed border-white/5 rounded-3xl flex flex-col items-center justify-center gap-6"
            >
                <div
                    class="p-6 rounded-full bg-cyan-400/5 text-cyan-400 border border-cyan-400/10"
                >
                    <MousePointer2 size={32} />
                </div>
                <div class="text-center">
                    <h3
                        class="text-xl font-black italic uppercase tracking-tighter mb-2"
                    >
                        No Unauthorized Access Detected
                    </h3>
                    <p class="text-white/30 text-xs font-bold font-mono">
                        X-ROAD NODE SHIELD ACTIVE // 100% TRANSPARENCY
                    </p>
                </div>
            </div>
        </div>
    {:else if activeTab === "MINI-PROGRAMS"}
        <div class="space-y-12" in:fade>
            <!-- Discovery Header -->
            <div class="flex items-end justify-between">
                <div>
                    <h2
                        class="text-3xl font-black italic tracking-tighter uppercase mb-2"
                    >
                        Mesh Discovery
                    </h2>
                    <button
                        class="text-[10px] font-black text-neon-cyan uppercase tracking-widest leading-none bg-transparent border-none p-0 cursor-default outline-none"
                        onclick={handleDevTap}
                    >
                        {devMode
                            ? "// DEVELOPER MESH ACTIVE //"
                            : "Curated Sovereignty Directory"}
                    </button>
                </div>
                {#if devMode}
                    <div
                        class="flex items-center gap-4 bg-white/5 border border-white/10 rounded-2xl px-6 py-3"
                        in:fly={{ y: 10 }}
                    >
                        <div class="flex flex-col">
                            <span
                                class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                                >Test Capsule URL</span
                            >
                            <input
                                type="text"
                                bind:value={testUrl}
                                placeholder="http://localhost:3000"
                                class="bg-transparent border-none outline-none text-xs text-white p-0 focus:ring-0 w-48 placeholder:text-white/10"
                            />
                        </div>
                        <button
                            class="bg-neon-cyan text-black text-[10px] font-black px-4 py-2 rounded-lg hover:scale-105 transition-all"
                            >LOAD</button
                        >
                    </div>
                {/if}
            </div>

            <!-- Categories -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {#each ["FEATURED", "BILLS & UTILITY", "IDENTITY & SEC"] as cat}
                    <div class="space-y-6">
                        <div class="flex items-center gap-3">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-white/20"
                            ></div>
                            <span
                                class="text-[10px] font-black text-white/40 uppercase tracking-widest"
                                >{cat}</span
                            >
                        </div>

                        <div class="space-y-4">
                            {#each miniApps.filter((a) => cat === "FEATURED" || a.category.toUpperCase() === cat.split(" ")[0]) as app}
                                {@const AppIcon = app.icon}
                                <button
                                    class="w-full glass-panel p-6 flex items-center justify-between group border-white/5 hover:border-neon-cyan/20 transition-all hover:bg-white/[0.05]"
                                >
                                    <div class="flex items-center gap-5">
                                        <div
                                            class="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform"
                                        >
                                            <AppIcon
                                                size={24}
                                                class="text-white/40 group-hover:text-neon-cyan transition-colors"
                                            />
                                        </div>
                                        <div class="text-left">
                                            <div
                                                class="font-black italic uppercase text-lg leading-tight"
                                            >
                                                {app.name}
                                            </div>
                                            <div
                                                class="text-[9px] font-black text-white/20 uppercase tracking-wider"
                                            >
                                                {app.status} // {app.category}
                                            </div>
                                        </div>
                                    </div>
                                    <ChevronRight
                                        size={18}
                                        class="text-white/10 group-hover:text-white group-hover:translate-x-1 transition-all"
                                    />
                                </button>
                            {/each}
                        </div>
                    </div>
                {/each}
            </div>

            <!-- Community Submission Banner -->
            <div
                class="glass-panel p-12 bg-gradient-to-r from-neon-cyan/5 to-transparent border-neon-cyan/10 flex flex-col md:flex-row items-center justify-between gap-8 mt-12"
            >
                <div class="max-w-xl">
                    <h3
                        class="text-2xl font-black italic uppercase tracking-tighter mb-4"
                    >
                        Want to list your Capsule?
                    </h3>
                    <p
                        class="text-sm text-white/60 leading-relaxed font-medium"
                    >
                        Join the 1,200+ developers building on the sovereign
                        mesh. All submissions undergo a 24-hour verification
                        block by the Citizen Governance Core.
                    </p>
                </div>
                <button
                    class="bg-neon-cyan text-black font-black px-10 py-5 italic uppercase tracking-tighter rounded-2xl hover:scale-105 active:scale-95 transition-all shadow-[0_0_40px_rgba(0,243,255,0.2)]"
                    >Submit Proposal</button
                >
            </div>
        </div>
    {:else if activeTab === "TOKENOMICS"}
        <div in:fade>
            <Tokenomics />
        </div>
    {/if}
</div>

<style>
    :global(.glass-panel) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
    }
</style>
