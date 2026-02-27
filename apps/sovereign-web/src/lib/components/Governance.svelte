<script lang="ts">

    import {
        Shield,
        Globe,
        Target,
        AlertCircle,
        CheckCircle2,
        XCircle,
        Sparkles,
        EyeOff,
        RefreshCw,
        Smartphone,
        QrCode,
    } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
    import { naiEngine } from "$lib/nai/engine.svelte";
    import VisualOverlay from "$lib/nai/VisualOverlay.svelte";
    import SovereignAnnotation from "./SovereignAnnotation.svelte";
    import { spawnSparkles } from "$lib/utils/SparkleEmitter";
    import type {
        PrivacyComponent,
        InstructionComponent,
        AmbientComponent,
        ActionComponent,
    } from "$lib/nai/types";

    let activeCategory = $state("ALL");
    let showPairingQR = $state(false);
    const categories = ["ALL", "ECONOMY", "SECURITY", "INFRA"];

    // 🧠 NAI: Reactive State
    let isPeekerDetected = $derived(
        naiEngine
            .getComponents<PrivacyComponent>("privacy")
            .some((c) => c.peekerDetected),
    );
    let isMeshConnected = $derived(naiEngine.isMeshConnected);
    let isFlashCrash = $derived(
        naiEngine.currentFrame?.metadata?.condition === "flash_crash",
    );
    let isTotalBreach = $derived(
        naiEngine.currentFrame?.metadata?.condition === "total_breach",
    );

    let agentInstruction = $derived(
        naiEngine.getComponents<InstructionComponent>("instruction")[0],
    );
    let ambientMood = $derived(
        naiEngine.getComponents<AmbientComponent>("ambient")[0] || {
            mood: "STABLE",
            baseColor: "#22d3ee",
        },
    );

    let resonanceSync = $derived(
        naiEngine.getComponents<any>("verification")[0],
    );

    // 🧠 NAI: Action Reactor
    $effect(() => {
        const actions = naiEngine.getComponents<ActionComponent>("action");
        for (const action of actions) {
            if (action.actionName === "FOCUS_PROPOSAL") {
                const propId = action.params?.id;
                if (propId) {
                    const el = document.getElementById(propId);
                    el?.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            }
        }
    });

    let proposals = $state([
        {
            id: "PROP_014",
            title: "SHACKLETON RELIEF",
            description:
                "Allocation of 10M UCT to Sector 4 expansion to support 5,000 incoming citizens.",
            support: 0.84,
            type: "ECONOMY",
            color: "text-amber-400",
            timeRemaining: "URGENT",
        },
        {
            id: "PROP_015",
            title: "PROTOCOL STABILITY",
            description:
                "Hardening FFI Bridge via age_ffi_guard. Locked 120fps via Vulkan AOT Shaders.",
            support: 0.98,
            type: "SECURITY",
            color: "text-cyan-400",
            timeRemaining: "SECURING",
        },
        {
            id: "PROP_016",
            title: "IDENTITY SOVEREIGNTY",
            description:
                "Induction of NIST AAL3 Multi-Factor Handshake and 90-Day Hardware Rotation.",
            support: 0.95,
            type: "IDENTITY",
            color: "text-emerald-400",
            timeRemaining: "COMPLIANT",
        },
    ]);

    function castVote(propId: string) {
        const prop = proposals.find((p) => p.id === propId);
        if (prop) {
            prop.support = Math.min(1.0, prop.support + 0.01);
            const el = document.getElementById(propId + "_btn");
            if (el) {
                const rect = el.getBoundingClientRect();
                spawnSparkles(
                    rect.left + rect.width / 2,
                    rect.top + rect.height / 2,
                );
                el.classList.add("liquid-pulse");
                setTimeout(() => el.classList.remove("liquid-pulse"), 600);
            }
        }
    }

    const upgrades = [
        {
            name: "CYCLES_MGMT (ICP)",
            status: "LIVE",
            progress: 100,
            color: "text-cyan-400",
        },
        {
            name: "GOVERNANCE_C (ICP)",
            status: "LIVE",
            id: "72j4w-6qaaa-aaaab-qacxq-cai",
            progress: 100,
            color: "text-emerald-400",
        },
    ];

    function simulateAgentAnalysis() {
        naiEngine.pushFrame({
            agentId: "SOPHIA_GOV",
            sessionId: "gov_sess_001",
            components: [
                {
                    type: "instruction",
                    text: "ANALYSIS: PROP_015 IS CRITICAL. LATTICE EROSION DETECTED IN SECTOR 2. IMMEDIATE SUPPORT RECOMMENDED.",
                    severity: "critical",
                },
                {
                    type: "visual_overlay",
                    shape: "pulse",
                    color: "#f43f5e",
                    targetRegion: { x: 50, y: 400, width: 400, height: 100 },
                },
                {
                    type: "action",
                    actionName: "FOCUS_PROPOSAL",
                    params: { id: "PROP_015" },
                },
            ],
        });
    }

    function togglePrivacyMock() {
        const current =
            naiEngine.getComponents<PrivacyComponent>("privacy")[0]
                ?.peekerDetected || false;
        naiEngine.pushFrame({
            agentId: "SECURITY_BOT",
            sessionId: "sec_99",
            components: [
                {
                    type: "privacy",
                    peekerDetected: !current,
                    blurIntensity: 30,
                },
            ],
        });
    }

    function cycleAmbientMood() {
        const cur = ambientMood.mood;
        let next: "STABLE" | "BULLISH" | "CHAOTIC" = "STABLE";
        let color = "#22d3ee";

        if (cur === "STABLE") {
            next = "BULLISH";
            color = "#10b981";
        } else if (cur === "BULLISH") {
            next = "CHAOTIC";
            color = "#f43f5e";
        }

        naiEngine.pushFrame({
            agentId: "RESONANCE_BOT",
            sessionId: "ambient_99",
            components: [
                {
                    type: "ambient",
                    mood: next,
                    baseColor: color,
                },
            ],
        });
    }

    function tetherMesh() {
        showPairingQR = true;
        setTimeout(() => {
            showPairingQR = false;
            // 🧠 NAI: Mesh Bridge Handshake
            naiEngine.injectMeshFrame({
                agentId: "MESH_BRIDGE",
                sessionId: "tether_01",
                components: [
                    {
                        type: "instruction",
                        text: "MESH TETHER ACTIVE: Smartphone Sentinel connected. Cross-device resonance optimized.",
                        severity: "info",
                    },
                ],
            });
        }, 3000);
    }

    let isGlassCourtHosting = $state(false);
    function toggleGlassCourt() {
        isGlassCourtHosting = !isGlassCourtHosting;
        if (isGlassCourtHosting) {
            naiEngine.pushFrame({
                agentId: "COLOCATION_HUB",
                sessionId: "court_host_99",
                components: [
                    {
                        type: "ambient",
                        mood: "GOVERNANCE_SYNC",
                        baseColor: "#00ffff",
                        intensity: 0.8,
                    },
                ],
                metadata: {
                    type: "ANCHOR_BEACON",
                    anchor_id: "court_sim_2026_xyz",
                },
            });
        }
    }

    let isSurgicalActive = $state(false);
    function toggleSurgicalSentinel() {
        isSurgicalActive = !isSurgicalActive;
        naiEngine.pushFrame({
            agentId: "PRIVACY_SENTINEL",
            sessionId: "surgical_99",
            components: [
                {
                    type: "privacy",
                    peekerDetected: true,
                    maskingEffect: isSurgicalActive ? "digital_frost" : "blur",
                    blurIntensity: isSurgicalActive ? 0 : 40,
                },
            ],
        });
    }

    function clearNai() {
        naiEngine.clear();
        isSurgicalActive = false;
    }
</script>

<div class="px-8 py-12 max-w-7xl mx-auto min-h-screen relative" in:fade>
    <!-- 🕵️ NAI: Privacy Shield Alert -->
    {#if isPeekerDetected}
        <div
            class="fixed top-8 left-1/2 -translate-x-1/2 z-[100] bg-amber-400 text-black px-6 py-2 rounded-full font-black text-[10px] tracking-widest uppercase flex items-center gap-3 shadow-[0_0_30px_rgba(251,191,36,0.5)]"
            transitionfly={{ y: -50 }}
        >
            <EyeOff size={14} />
            Privacy Shield Active // {isMeshConnected
                ? "Remote Peer Detected Threat"
                : "Local Sensor Alert"}
        </div>
    {/if}

    <!-- 🚀 NAI: Flash Crash Alert -->
    {#if isFlashCrash}
        <div
            class="fixed top-20 left-1/2 -translate-x-1/2 z-[100] bg-rose-500 text-white px-8 py-3 rounded-full font-black text-[12px] tracking-widest uppercase flex items-center gap-3 shadow-[0_0_50px_rgba(244,63,94,0.6)] animate-pulse"
            transitionfly={{ y: -50 }}
        >
            <Sparkles size={16} class="animate-spin" />
            AGENTIC FLASH CRASH // THRESHOLD EXCEEDED // SCTP SATURATION
        </div>
    {/if}
    <!-- 🛡️ NAI: Resonance Sync / AAL3 Proximity (Identity Radiance) -->
    {#if resonanceSync}
        <div
            class="fixed top-8 right-8 z-[100] glass-panel border-cyan-400/50 px-6 py-4 flex items-center gap-4 shadow-[0_0_60px_rgba(34,211,238,0.5)] animate-[pulse_2s_infinite]"
            transitionfly={{ x: 50 }}
        >
            <div class="p-2 rounded-full bg-cyan-400/30 text-cyan-400 relative">
                <!-- Radiant Aura -->
                <div
                    class="absolute inset-0 rounded-full bg-cyan-400/20 blur-xl animate-ping"
                ></div>
                <Smartphone size={16} class="relative z-10" />
            </div>
            <div>
                <div
                    class="text-[10px] font-black tracking-widest text-cyan-400 uppercase premium-shimmer"
                >
                    Resonance Active
                </div>
                <div class="text-[8px] font-bold text-white/60 uppercase">
                    NIST AAL3 // IDENTITY RADIANCE
                </div>
            </div>
        </div>
    {/if}

    <!-- 🛡️ NAI: Total Breach Alert -->
    {#if isTotalBreach}
        <div
            class="fixed top-32 left-1/2 -translate-x-1/2 z-[100] bg-black text-rose-500 border-2 border-rose-500 px-10 py-4 rounded-xl font-black text-[14px] tracking-[0.3em] uppercase flex items-center gap-4 shadow-[0_0_100px_rgba(244,63,94,0.8)] animate-[pulse_0.2s_infinite]"
            transitionfly={{ y: -50 }}
        >
            <Shield size={20} />
            TOTAL BREACH SIMULATION // FAST-PATH RECOVERY ACTIVE // HARDENED MODE
        </div>
    {/if}

    <!-- 📱 NAI: Mesh Pairing QR -->
    {#if showPairingQR}
        <div
            class="fixed inset-0 z-[200] flex items-center justify-center bg-black/80 backdrop-blur-xl"
            transition:fade
        >
            <div
                class="glass-panel p-12 text-center space-y-8 border-cyan-400/20"
            >
                <div
                    class="mx-auto w-48 h-48 bg-white p-4 rounded-2xl flex items-center justify-center shadow-[0_0_50px_rgba(34,211,238,0.2)]"
                >
                    <QrCode size={120} class="text-black" />
                </div>
                <div>
                    <h2
                        class="text-xl font-black italic uppercase tracking-widest text-cyan-400 mb-2"
                    >
                        Tether Device
                    </h2>
                    <p
                        class="text-[10px] font-bold text-white/40 uppercase tracking-[0.2em]"
                    >
                        Scan to establish P2P Mesh link
                    </p>
                </div>
                <div
                    class="flex items-center justify-center gap-4 text-cyan-400"
                >
                    <RefreshCw size={16} class="animate-spin" />
                    <span
                        class="text-[8px] font-black uppercase tracking-widest"
                        >Waiting for Handshake...</span
                    >
                </div>
            </div>
        </div>
    {/if}

    <!-- 🧠 NAI: Agent Guidance Overlay -->
    {#if agentInstruction}
        <div
            class="fixed bottom-12 right-12 z-50 w-96 glass-panel p-8 border-cyan-400/30 shadow-[0_0_50px_rgba(34,211,238,0.1)]"
            transitionfly={{ x: 100, duration: 800 }}
        >
            <div class="flex items-center gap-3 mb-6">
                <div class="p-2 rounded-lg bg-cyan-400/10 text-cyan-400">
                    <Sparkles size={16} />
                </div>
                <div
                    class="text-[10px] font-black tracking-[0.2em] text-cyan-400 uppercase"
                >
                    Agent Intelligence Stream
                </div>
            </div>
            <p class="text-sm text-white font-bold leading-relaxed italic mb-8">
                "{agentInstruction.text}"
            </p>
            <div class="flex gap-4">
                <button
                    onclick={clearNai}
                    class="flex-1 py-3 rounded-xl bg-white/5 border border-white/10 text-[8px] font-black uppercase tracking-widest hover:bg-white/10 transition-all"
                >
                    Dismiss
                </button>
            </div>
        </div>
    {/if}

    <!-- Simplified Briefing Header -->
    <div class="mb-16 flex justify-between items-start">
        <div>
            <div
                class="flex items-center gap-3 text-[10px] font-black tracking-[0.4em] text-cyan-400 uppercase mb-4"
            >
                <AlertCircle size={14} />
                Immediate Action Required
            </div>
            <h1
                class="text-6xl font-black italic uppercase tracking-tighter mb-4 premium-gradient-text relative group"
            >
                <!-- Liquid Refraction Effect -->
                <div
                    class="absolute -inset-4 bg-cyan-400/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-1000"
                ></div>
                Protocol<span
                    style="color: {ambientMood.baseColor}"
                    class="transition-colors duration-1000 drop-shadow-[0_0_15px_rgba(34,211,238,0.4)]"
                    >Briefing</span
                >
            </h1>
            <p
                class="text-lg text-white/40 font-bold max-w-2xl transition-all duration-700"
                class:blur-2xl={isPeekerDetected || isTotalBreach}
                class:animate-pulse={isFlashCrash || isTotalBreach}
                style="filter: blur({isPeekerDetected
                    ? 24
                    : isTotalBreach
                      ? 8
                      : 0}px); transform: {isFlashCrash || isTotalBreach
                    ? `translate(${(Math.random() - 0.5) * (isTotalBreach ? 12 : 4)}px, ${(Math.random() - 0.5) * (isTotalBreach ? 12 : 4)}px)`
                    : 'none'}"
            >
                The sovereign mesh requires your resonance on 2 critical
                proposals. Your voting power is <span
                    class="text-white premium-shimmer px-2 rounded-md"
                    >12.5k Credits</span
                >.
            </p>
        </div>

        <!-- 🕵️ Simulation Controls -->
        <div class="flex flex-col gap-2">
            <button
                onclick={simulateAgentAnalysis}
                class="px-4 py-2 rounded-lg bg-cyan-400/10 border border-cyan-400/20 text-cyan-400 text-[8px] font-black uppercase tracking-widest flex items-center gap-2 hover:bg-cyan-400 hover:text-black transition-all"
            >
                <Sparkles size={12} />
                Simulate Agent Analysis
            </button>
            <button
                onclick={cycleAmbientMood}
                class="px-4 py-2 rounded-lg border text-[8px] font-black uppercase tracking-widest flex items-center gap-2 transition-all hover:bg-white hover:text-black"
                style="background: {ambientMood.baseColor}1a; border-color: {ambientMood.baseColor}33; color: {ambientMood.baseColor}"
            >
                <RefreshCw size={12} />
                Cycle Ambient: {ambientMood.mood}
            </button>
            <button
                onclick={togglePrivacyMock}
                class="px-4 py-2 rounded-lg bg-amber-400/10 border border-amber-400/20 text-amber-400 text-[8px] font-black uppercase tracking-widest flex items-center gap-2 hover:bg-amber-400 hover:text-black transition-all"
            >
                <EyeOff size={12} />
                Toggle Privacy Mock
            </button>
            <button
                onclick={tetherMesh}
                class="px-4 py-2 rounded-lg bg-emerald-400/10 border border-emerald-400/20 text-emerald-400 text-[8px] font-black uppercase tracking-widest flex items-center gap-2 hover:bg-emerald-400 hover:text-black transition-all"
            >
                <Smartphone size={12} />
                Tether Mobile Sentinel
            </button>
            <button
                onclick={toggleGlassCourt}
                class="px-4 py-2 rounded-lg border text-[8px] font-black uppercase tracking-widest flex items-center gap-2 transition-all {isGlassCourtHosting
                    ? 'bg-cyan-400 text-black border-cyan-400 shadow-[0_0_20px_rgba(34,211,238,0.5)]'
                    : 'bg-white/5 border-white/10 text-white/60 hover:bg-white/10'}"
            >
                <Globe
                    size={12}
                    class={isGlassCourtHosting ? "animate-pulse" : ""}
                />
                {isGlassCourtHosting ? "HOSTING COURT" : "JOIN GLASS COURT"}
            </button>
            <button
                onclick={toggleSurgicalSentinel}
                class="px-4 py-2 rounded-lg border text-[8px] font-black uppercase tracking-widest flex items-center gap-2 transition-all {isSurgicalActive
                    ? 'bg-cyan-400 text-black border-cyan-400'
                    : 'bg-white/5 border-white/10 text-white/60'}"
            >
                <Shield size={12} />
                SURGICAL SENTINEL: {isSurgicalActive ? "ACTIVE" : "OFF"}
            </button>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-12">
        <!-- Sidebar: Status -->
        <div class="space-y-8">
            <div class="glass-panel p-8 space-y-8 border-white/5">
                <div class="h-px bg-white/5"></div>

                <!-- UTILITY DATA VIZ: Quorum Progress -->
                <div>
                    <div
                        class="text-[10px] font-bold text-white/20 uppercase tracking-widest mb-6 italic"
                    >
                        Quorum Progress // 64% Required
                    </div>
                    <div class="space-y-4">
                        <div
                            class="relative h-2 bg-white/5 rounded-full overflow-hidden"
                        >
                            <div
                                class="absolute inset-0 bg-cyan-400 group-hover:bg-amber-400 transition-colors"
                                style="width: 78%"
                            ></div>
                        </div>
                        <div
                            class="flex justify-between text-[10px] font-black text-cyan-400"
                        >
                            <span>78% REACHED</span>
                            <span class="text-white/20">PASSED</span>
                        </div>
                    </div>
                </div>

                <div class="h-px bg-white/5"></div>

                <!-- UTILITY DATA VIZ: Participation Mesh -->
                <div>
                    <div
                        class="text-[10px] font-bold text-white/20 uppercase tracking-widest mb-6 italic"
                    >
                        7D Participation Mesh
                    </div>
                    <div class="h-16 w-full relative">
                        <svg
                            class="w-full h-full opacity-40"
                            viewBox="0 0 100 40"
                        >
                            <path
                                d="M0,38 L10,30 L20,35 L30,10 L40,15 L50,5 L60,12 L70,8 L80,20 L90,15 L100,5"
                                fill="none"
                                stroke="var(--color-accent)"
                                stroke-width="1"
                            />
                            <path
                                d="M0,38 L10,30 L20,35 L30,10 L40,15 L50,5 L60,12 L70,8 L80,20 L90,15 L100,5 V40 H0 Z"
                                fill="url(#mesh-gradient)"
                            />
                            <defs>
                                <linearGradient
                                    id="mesh-gradient"
                                    x1="0"
                                    y1="0"
                                    x2="0"
                                    y2="1"
                                >
                                    <stop
                                        offset="0%"
                                        stop-color="var(--color-accent)"
                                        stop-opacity="0.1"
                                    />
                                    <stop
                                        offset="100%"
                                        stop-color="var(--color-accent)"
                                        stop-opacity="0"
                                    />
                                </linearGradient>
                            </defs>
                        </svg>
                        <div
                            class="absolute inset-0 flex items-center justify-center"
                        >
                            <div
                                class="text-[18px] font-black italic text-white premium-shimmer"
                            >
                                12.4K NODES
                            </div>
                        </div>
                    </div>
                </div>

                <div class="h-px bg-white/5"></div>

                <div>
                    <div
                        class="text-[10px] font-black text-white/20 uppercase tracking-widest mb-4"
                    >
                        Upgrades
                    </div>
                    <div class="space-y-4">
                        {#each upgrades as upgrade}
                            <div class="space-y-2">
                                <div
                                    class="flex justify-between text-[8px] font-black uppercase"
                                >
                                    <span class="text-white/40"
                                        >{upgrade.name}</span
                                    >
                                    <span class={upgrade.color}
                                        >{upgrade.status}</span
                                    >
                                </div>
                                <div
                                    class="h-1 bg-white/5 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="h-full bg-cyan-400/50"
                                        style="width: {upgrade.progress}%"
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>

            <button
                class="w-full py-4 rounded-xl bg-cyan-400/10 border border-cyan-400/20 text-cyan-400 text-[10px] font-black tracking-widest uppercase hover:bg-cyan-400 hover:text-black transition-all"
            >
                Delegate Resonance
            </button>
        </div>

        <!-- Main Proposals Content -->
        <div class="lg:col-span-3 space-y-12">
            <!-- Category Chips -->
            <div class="flex gap-4">
                {#each categories as cat}
                    <button
                        onclick={() => (activeCategory = cat)}
                        class="premium-scale px-6 py-2 rounded-full text-[10px] font-black tracking-widest transition-all {activeCategory ===
                        cat
                            ? 'bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.2)]'
                            : 'bg-white/5 text-white/40 hover:bg-white/10'}"
                    >
                        {cat}
                    </button>
                {/each}
            </div>

            <!-- Proposals Grid -->
            <div class="space-y-6">
                {#each proposals as prop}
                    <div
                        class="glass-panel p-10 group hover:border-cyan-400/20 transition-all premium-scale"
                    >
                        <div class="flex flex-col md:flex-row gap-12">
                            <div class="flex-1">
                                <div class="flex items-center gap-4 mb-4">
                                    <span
                                        class="px-3 py-1 rounded-md bg-white/5 text-[8px] font-black tracking-widest text-white/40 uppercase"
                                        >{prop.type}</span
                                    >
                                    {#if prop.support > 0.9}
                                        <span
                                            class="px-3 py-1 rounded-md bg-amber-400/20 text-[8px] font-black tracking-widest text-amber-400 uppercase flex items-center gap-2"
                                        >
                                            <Sparkles size={10} />
                                            KINTSUGI LAW // HARDENED
                                        </span>
                                    {/if}
                                    <span
                                        class="text-[8px] font-black tracking-widest text-cyan-400 uppercase tabular-nums"
                                        >{prop.id} // {prop.timeRemaining}</span
                                    >
                                </div>
                                <h3
                                    class="text-3xl font-black italic uppercase tracking-tighter mb-4 group-hover:text-cyan-400 transition-colors {prop.support >
                                    0.9
                                        ? 'kintsugi-text'
                                        : ''}"
                                >
                                    {prop.title}
                                </h3>
                                <p
                                    class="text-white/40 font-bold leading-relaxed max-w-xl"
                                >
                                    {prop.description}
                                </p>
                            </div>

                            <div
                                class="w-full md:w-64 flex flex-col justify-center gap-4"
                            >
                                <button
                                    id={prop.id + "_btn"}
                                    onclick={() => castVote(prop.id)}
                                    class="premium-scale premium-shimmer w-full h-14 rounded-2xl bg-cyan-400 text-black font-black italic tracking-widest flex items-center justify-center gap-3 transition-all"
                                >
                                    <CheckCircle2 size={18} />
                                    SUPPORT
                                </button>
                                <button
                                    class="w-full h-14 rounded-2xl bg-white/5 border border-white/10 text-white/40 font-black italic tracking-widest flex items-center justify-center gap-3 hover:bg-white/10 hover:text-white transition-all"
                                >
                                    <XCircle size={18} />
                                    REJECT
                                </button>
                            </div>
                        </div>

                        <!-- Progress Bar Sub-detail -->
                        <div
                            class="mt-8 pt-8 border-t border-white/5 flex items-center gap-6"
                        >
                            <div
                                class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                            >
                                Global Consensus
                            </div>
                            <div
                                class="flex-1 h-1 bg-white/5 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-cyan-400/20 transition-all duration-700 ease-out"
                                    style="width: {prop.support * 100}%"
                                ></div>
                            </div>
                            <div
                                class="text-[10px] font-black text-cyan-400 italic"
                            >
                                {(prop.support * 100).toFixed(0)}%
                            </div>
                        </div>
                    </div>
                {/each}
            </div>

            <div
                class="p-10 rounded-[32px] bg-cyan-400/5 border border-cyan-400/10 flex items-start gap-8"
            >
                <Target class="text-cyan-400 shrink-0" size={32} />
                <div>
                    <h4
                        class="text-sm font-black italic uppercase tracking-widest mb-2 text-white/80"
                    >
                        Protocol Mission Alignment
                    </h4>
                    <p
                        class="text-xs text-white/40 font-bold leading-relaxed italic"
                    >
                        All active proposals are currently aligned with the AGE
                        Protocol 2026 Resilience Roadmap. No fragmentation risks
                        detected by Sophia-Services.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- STRATEGIC MANIFESTO: Phase 4 Expansion (Strategic Board Pattern) -->
    <div class="mt-24 space-y-12">
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-white/20 uppercase mb-4"
            >
                Command Intent
            </div>
            <h2
                class="text-4xl font-black italic uppercase tracking-tighter text-white"
            >
                Strategic <span class="text-amber-400">Manifesto</span>
            </h2>
        </div>

        <div
            class="strategic-board grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
        >
            <div class="strategic-panel">
                <h4>Core Objectives</h4>
                <ul class="space-y-2 list-none p-0">
                    <li>// L7 LATENCY: {"<"} 12ms</li>
                    <li>// VALIDATOR UPTIME: 99.999%</li>
                    <li>// SECR HARDENING: LEVEL 9</li>
                </ul>
            </div>
            <div class="strategic-panel border-amber-400">
                <h4>Phase 4 Milestones</h4>
                <ul class="space-y-2 list-none p-0">
                    <li>// LUNAR MESH INDUCTION</li>
                    <li>// SOPHIA ETHICS RATIFIED</li>
                    <li>// NEURAL BRIDGE V1</li>
                </ul>
            </div>
            <div class="strategic-panel">
                <h4>Protocol Needs</h4>
                <ul class="space-y-2 list-none p-0">
                    <li>// LIQUIDITY SATURATION</li>
                    <li>// PEER-TO-PEER TRUST</li>
                    <li>// ZERO-KNOWLEDGE PROOF</li>
                </ul>
            </div>
            <div class="strategic-panel">
                <h4>2026 Resilience</h4>
                <ul class="space-y-2 list-none p-0">
                    <li>// QUANTUM RESISTANCE</li>
                    <li>// ADAPTIVE GOVERNANCE</li>
                    <li>// SOVEREIGN IDENTITY</li>
                </ul>
            </div>
        </div>

        <!-- 🧙‍♂️ WIZARD OF OZ: Protocol Concierge Status -->
        <div
            class="mt-6 flex items-center gap-3 px-4 py-2 bg-amber-400/5 border border-amber-400/10 rounded"
        >
            <div class="relative">
                <div
                    class="w-2 h-2 bg-amber-400 rounded-full animate-pulse"
                ></div>
                <div
                    class="absolute inset-0 bg-amber-400 rounded-full animate-ping opacity-20"
                ></div>
            </div>
            <div class="flex flex-col">
                <span
                    class="text-[9px] font-black text-amber-400 uppercase tracking-widest"
                    >Protocol Concierge // Active</span
                >
                <span class="text-[8px] text-white/40 font-mono italic"
                    >NAI Engine (Sophia) is manually overseeing Level 9 state
                    transitions during induction.</span
                >
            </div>
        </div>
    </div>
    <!-- 💖 MLP: RESONANCE & SENTIMENT (Experience Strategy) -->
    <div
        id="manifold_resonance"
        class="mt-24 space-y-12 relative overflow-hidden"
    >
        <!-- Adaptive Mood Substrate -->
        <div
            class="absolute inset-0 resonance-pulse mood-adaptive-emerald pointer-events-none"
        ></div>

        <div
            class="relative z-10 flex flex-col md:flex-row items-end justify-between gap-8"
        >
            <div class="max-w-xl">
                <div
                    class="text-[10px] font-black tracking-[0.4em] text-white/20 uppercase mb-4"
                >
                    Experience Strategy
                </div>
                <h2
                    class="text-4xl font-black italic uppercase tracking-tighter text-white"
                >
                    Network <span class="text-emerald-400">Resonance</span>
                </h2>
                <p class="mt-4 text-white/40 text-sm leading-relaxed font-mono">
                    // Monitoring sub-perceptual feedback loops and
                    institutional sentiment. The protocol's 'lovability' is
                    currently rated at <span class="text-emerald-400">92%</span>
                    based on frictionless state transitions and validator affinity.
                </p>
            </div>

            <div class="grid grid-cols-2 gap-4 w-full md:w-auto">
                <div class="lovable-card p-6 flex flex-col items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-[0.2em]"
                        >Affinity</span
                    >
                    <span class="text-3xl font-black text-emerald-400"
                        >0.89</span
                    >
                </div>
                <div class="lovable-card p-6 flex flex-col items-center">
                    <span
                        class="text-[8px] font-black text-white/20 uppercase tracking-[0.2em]"
                        >Resonance</span
                    >
                    <span class="text-3xl font-black text-cyan-400">HIGH</span>
                </div>
            </div>
        </div>
    </div>

    <!-- INSTITUTIONAL DATA: Protocol Registry -->
    <div class="mt-24 space-y-12">
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-white/20 uppercase mb-4"
            >
                Historical Ledger
            </div>
            <h2
                class="text-4xl font-black italic uppercase tracking-tighter text-white"
            >
                Protocol <span class="text-cyan-400">Registry</span>
            </h2>
        </div>

        <div class="glass-panel overflow-hidden border-white/5">
            <table class="hardened-table">
                <thead>
                    <tr>
                        <th>Artifact ID</th>
                        <th>Law Title</th>
                        <th>Status</th>
                        <th>Hardening Power</th>
                        <th>Ratified</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="group hover:bg-white/[0.02] transition-colors">
                        <td class="font-black text-[10px] text-cyan-400"
                            >AGE-2025-09</td
                        >
                        <td class="font-bold text-white"
                            >OBLIVIOUS_ROUTING_V2</td
                        >
                        <td
                            ><span
                                class="px-2 py-0.5 rounded-full bg-emerald-400/10 text-emerald-400 text-[8px] font-black uppercase"
                                >HARDENED</span
                            ></td
                        >
                        <td class="font-black italic text-cyan-400">92.4%</td>
                        <td class="text-white/20 text-[10px] tabular-nums"
                            >12 JAN 2026</td
                        >
                    </tr>
                    <tr class="group hover:bg-white/[0.02] transition-colors">
                        <td class="font-black text-[10px] text-cyan-400"
                            >AGE-2025-04</td
                        >
                        <td class="font-bold text-white"
                            >SOPHIA_ETHICS_CONSTRAINT</td
                        >
                        <td
                            ><span
                                class="px-2 py-0.5 rounded-full bg-emerald-400/10 text-emerald-400 text-[8px] font-black uppercase"
                                >HARDENED</span
                            ></td
                        >
                        <td class="font-black italic text-cyan-400">98.1%</td>
                        <td class="text-white/20 text-[10px] tabular-nums"
                            >04 DEC 2025</td
                        >
                    </tr>
                    <tr class="group hover:bg-white/[0.02] transition-colors">
                        <td class="font-black text-[10px] text-cyan-400"
                            >AGE-2024-11</td
                        >
                        <td class="font-bold text-white"
                            >LIQUID_QUORUM_ADJUSTMENT</td
                        >
                        <td
                            ><span
                                class="px-2 py-0.5 rounded-full bg-white/5 text-white/40 text-[8px] font-black uppercase"
                                >LEGACY</span
                            ></td
                        >
                        <td class="font-black italic text-white/20">64.0%</td>
                        <td class="text-white/20 text-[10px] tabular-nums"
                            >28 OCT 2024</td
                        >
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <!-- 🏛️ PROTOCOL COMPONENT REGISTRY (High-Density View) -->
    <div id="manifold_registry" class="mt-24 space-y-12">
        <div>
            <div
                class="text-[10px] font-black tracking-[0.4em] text-white/20 uppercase mb-4"
            >
                Institutional Library
            </div>
            <h2
                class="text-4xl font-black italic uppercase tracking-tighter text-white"
            >
                Component <span class="text-cyan-400">Registry</span>
            </h2>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {#each Array(12) as _, i}
                <div
                    class="lovable-card p-4 flex flex-col items-center justify-center text-center space-y-3"
                >
                    <div
                        class="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center border border-white/10 hover:border-cyan-400 transition-colors"
                    >
                        <div class="w-2 h-2 rounded-full bg-cyan-400"></div>
                    </div>
                    <div class="flex flex-col">
                        <span
                            class="text-[8px] font-black text-white/20 uppercase tracking-widest"
                            >Module_{100 + i}</span
                        >
                        <span class="text-[10px] font-bold text-white/60"
                            >SECR_CORE_V{i}</span
                        >
                    </div>
                </div>
            {/each}
        </div>

        <div
            class="mt-8 p-6 lovable-card border-dashed border-white/10 flex items-center justify-center"
        >
            <button
                class="text-[10px] font-black tracking-[0.3em] text-white/30 hover:text-cyan-400 transition-colors uppercase"
            >
                // VIEW ALL SYSTEM ARTIFACTS
            </button>
        </div>
    </div>

    <SovereignAnnotation
        targetId="manifold_resonance"
        text="Affinity logic validated by Sophia. Resonance is HIGH."
        type="tactical"
    />
    <SovereignAnnotation
        targetId="manifold_registry"
        text="Index reflects 12 hardened law artifacts in Phase 4."
        type="strategic"
    />

    <VisualOverlay />
</div>
