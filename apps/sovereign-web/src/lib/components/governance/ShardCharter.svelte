<script lang="ts">
    import { fade, fly, scale } from "svelte/transition";
    import { FileSignature, Scale, Zap, Users, Hexagon } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    let inscribeProgress = $state(0);
    let isSigning = $state(false);
    let isChartered = $state(false);

    // Initial Genesis Parameters for Shard 001
    let equalizationTax = $state(2.5); // 2.5% local tax, 0% platform fee
    let minVotingMerit = $state(0.75); // M threshold for governance
    let dataZapRate = $state(0.01); // SLC per MB
    let maxGuardians = $state(100);

    function startSigning() {
        if (isSigning || isChartered) return;
        isSigning = true;

        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate([10, 50, 10]);
        }

        let interval = setInterval(() => {
            inscribeProgress += 2;
            if (inscribeProgress >= 100) {
                clearInterval(interval);
                finalizeCharter();
            }
        }, 30);
    }

    function cancelSigning() {
        if (!isChartered) {
            isSigning = false;
            inscribeProgress = 0;
        }
    }

    function finalizeCharter() {
        isSigning = false;

        // Deep resonance haptic
        if (typeof navigator !== "undefined" && navigator.vibrate) {
            navigator.vibrate([200, 100, 500]);
        }

        manifold.recordEvent(
            "SHARD_CHARTERED",
            `Shard 001 Genesis parameters locked. Alpha-Nodes enabled.`,
        );

        setTimeout(() => {
            isChartered = true;
        }, 500);
    }
</script>

<div class="charter-container" in:fade={{ duration: 600 }}>
    <div
        class="absolute inset-0 grid-overlay opacity-10 pointer-events-none"
    ></div>

    <header class="text-center mb-10 relative z-10">
        <div
            class="inline-flex items-center justify-center p-4 bg-[#22d3ee]/10 rounded-full mb-4 ring-1 ring-[#22d3ee]/30"
        >
            <FileSignature size={32} class="text-[#22d3ee]" />
        </div>
        <h1 class="text-3xl font-black text-white tracking-widest uppercase">
            The Sovereign Charter
        </h1>
        <p
            class="text-[#22d3ee] font-mono text-sm tracking-widest opacity-80 mt-2"
        >
            SHARD 001 • GENESIS PARAMETERS
        </p>
    </header>

    {#if !isChartered}
        <div
            class="parameters-grid relative z-10"
            in:fly={{ y: 20, duration: 400 }}
        >
            <!-- Rule 1: The Tax -->
            <div class="rule-card group">
                <div class="rule-header">
                    <Scale class="text-amber-500" size={20} />
                    <h3>Equalization Tax</h3>
                </div>
                <div class="rule-body">
                    <div class="flex items-end gap-2 mb-2">
                        <span class="text-4xl font-black text-white"
                            >{equalizationTax.toFixed(1)}</span
                        >
                        <span class="text-xl text-[#22d3ee] mb-1">%</span>
                    </div>
                    <p class="text-xs text-white/50 leading-relaxed">
                        0% Platform Fee. 100% of this tax recirculates solely to
                        validators and local mesh hosts within Shard 001. No
                        external extraction.
                    </p>
                </div>
                <input
                    type="range"
                    bind:value={equalizationTax}
                    min="0.5"
                    max="5.0"
                    step="0.1"
                    class="sovereign-slider mt-4"
                    disabled={isSigning}
                />
            </div>

            <!-- Rule 2: Resonance -->
            <div class="rule-card group">
                <div class="rule-header">
                    <Hexagon class="text-amber-500" size={20} />
                    <h3>Governance Floor</h3>
                </div>
                <div class="rule-body">
                    <div class="flex items-end gap-2 mb-2">
                        <span class="text-4xl font-black text-white"
                            >{minVotingMerit.toFixed(2)}</span
                        >
                        <span class="text-xl text-[#22d3ee] mb-1">M</span>
                    </div>
                    <p class="text-xs text-white/50 leading-relaxed">
                        The minimum Merit standard required to vote on protocol
                        upgrades or alter this Charter. Merit cannot be bought;
                        it must be earned through resonance.
                    </p>
                </div>
                <input
                    type="range"
                    bind:value={minVotingMerit}
                    min="0.10"
                    max="1.00"
                    step="0.05"
                    class="sovereign-slider mt-4"
                    disabled={isSigning}
                />
            </div>

            <!-- Rule 3: Data -->
            <div class="rule-card group">
                <div class="rule-header">
                    <Zap class="text-amber-500" size={20} />
                    <h3>Aether-Zap Rate</h3>
                </div>
                <div class="rule-body">
                    <div class="flex items-end gap-2 mb-2">
                        <span class="text-4xl font-black text-white"
                            >{dataZapRate.toFixed(3)}</span
                        >
                        <span
                            class="text-xs text-[#22d3ee] mb-2 uppercase tracking-widest font-bold"
                            >SLC / MB</span
                        >
                    </div>
                    <p class="text-xs text-white/50 leading-relaxed">
                        The baseline peer-to-peer data routing cost for the eSIM
                        Mesh. Guardians hosting the network earn this directly
                        per Data Dabba.
                    </p>
                </div>
                <input
                    type="range"
                    bind:value={dataZapRate}
                    min="0.001"
                    max="0.050"
                    step="0.001"
                    class="sovereign-slider mt-4"
                    disabled={isSigning}
                />
            </div>

            <!-- Rule 4: Cap -->
            <div class="rule-card group">
                <div class="rule-header">
                    <Users class="text-amber-500" size={20} />
                    <h3>Pioneer Cap</h3>
                </div>
                <div class="rule-body">
                    <div class="flex items-end gap-2 mb-2">
                        <span class="text-4xl font-black text-white"
                            >{maxGuardians}</span
                        >
                        <span
                            class="text-xs text-[#22d3ee] mb-2 uppercase tracking-widest font-bold"
                            >NODES</span
                        >
                    </div>
                    <p class="text-xs text-white/50 leading-relaxed">
                        The hard limit for the Genesis Cohort. Hatchery
                        automatically seals once {maxGuardians} Passkeys are inscribed
                        into the Genesis Block.
                    </p>
                </div>
                <input
                    type="range"
                    bind:value={maxGuardians}
                    min="50"
                    max="500"
                    step="10"
                    class="sovereign-slider mt-4"
                    disabled={isSigning}
                />
            </div>
        </div>

        <!-- The Inscription Plate -->
        <div class="mt-12 text-center relative z-10 w-full max-w-sm mx-auto">
            <button
                class="signature-plate"
                onmousedown={startSigning}
                onmouseup={cancelSigning}
                onmouseleave={cancelSigning}
                ontouchstart={(e) => {
                    e.preventDefault();
                    startSigning();
                }}
                ontouchend={cancelSigning}
                ontouchcancel={cancelSigning}
            >
                <div class="plate-bg" style="width: {inscribeProgress}%"></div>
                <span
                    class="relative z-10 uppercase tracking-[0.3em] font-black text-xs {inscribeProgress >
                    50
                        ? 'text-black'
                        : 'text-[#22d3ee]'} transition-colors duration-200"
                >
                    {isSigning
                        ? `INSCRIBING... ${inscribeProgress}%`
                        : "HOLD TO INSCRIBE CHARTER"}
                </span>
            </button>
            <p class="text-[10px] text-white/30 uppercase tracking-widest mt-4">
                This action binds the Shard Cryptographically.
            </p>
        </div>
    {:else}
        <!-- Success State -->
        <div
            class="charter-sealed text-center relative z-10"
            in:scale={{ duration: 800, start: 0.9 }}
        >
            <div class="seal-ring mx-auto mb-8">
                <div class="seal-inner">
                    <Hexagon size={48} class="text-emerald-400" />
                </div>
            </div>

            <h2
                class="text-4xl font-black text-white tracking-[0.2em] uppercase mb-4"
            >
                Charter Inscribed
            </h2>
            <p class="text-[#22d3ee] font-mono mb-8 opacity-80">
                SHARD 001 IS NOW CONSTITUTIONAL
            </p>

            <div
                class="bg-black/40 border border-[#22d3ee]/20 rounded-2xl p-6 text-left max-w-lg mx-auto backdrop-blur-md"
            >
                <div
                    class="flex justify-between border-b border-white/5 pb-2 mb-2"
                >
                    <span
                        class="text-xs text-white/50 uppercase tracking-widest font-bold"
                        >Eq. Tax</span
                    >
                    <span class="font-mono text-emerald-400"
                        >{equalizationTax.toFixed(1)}%</span
                    >
                </div>
                <div
                    class="flex justify-between border-b border-white/5 pb-2 mb-2"
                >
                    <span
                        class="text-xs text-white/50 uppercase tracking-widest font-bold"
                        >Gov. Floor</span
                    >
                    <span class="font-mono text-emerald-400"
                        >{minVotingMerit.toFixed(2)} M</span
                    >
                </div>
                <div
                    class="flex justify-between border-b border-white/5 pb-2 mb-2"
                >
                    <span
                        class="text-xs text-white/50 uppercase tracking-widest font-bold"
                        >Zap Rate</span
                    >
                    <span class="font-mono text-emerald-400"
                        >{dataZapRate.toFixed(3)} SLC/MB</span
                    >
                </div>
                <div class="flex justify-between">
                    <span
                        class="text-xs text-white/50 uppercase tracking-widest font-bold"
                        >Guardians</span
                    >
                    <span class="font-mono text-emerald-400"
                        >0 / {maxGuardians}</span
                    >
                </div>
            </div>

            <div
                class="mt-8 text-[10px] font-mono text-emerald-500/50 uppercase tracking-widest"
            >
                [ GENESIS BLOCK 0x0000 GENERATED ]
            </div>
        </div>
    {/if}
</div>

<style>
    .charter-container {
        min-height: 80vh;
        width: 100%;
        background: radial-gradient(circle at 50% 0%, #08111a 0%, #03060a 100%);
        border-radius: 40px;
        padding: 4rem 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(34, 211, 238, 0.1);
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.8);
    }

    .grid-overlay {
        background-size: 40px 40px;
        background-image: linear-gradient(
                to right,
                rgba(34, 211, 238, 0.2) 1px,
                transparent 1px
            ),
            linear-gradient(
                to bottom,
                rgba(34, 211, 238, 0.2) 1px,
                transparent 1px
            );
    }

    .parameters-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .rule-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
    }

    .rule-card:hover {
        background: rgba(34, 211, 238, 0.05);
        border-color: rgba(34, 211, 238, 0.2);
        box-shadow:
            0 20px 40px rgba(0, 0, 0, 0.4),
            inset 0 0 20px rgba(34, 211, 238, 0.05);
        transform: translateY(-2px);
    }

    .rule-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .rule-header h3 {
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: white;
    }

    .rule-body {
        flex: 1;
    }

    /* Custom Sovereign Slider */
    .sovereign-slider {
        -webkit-appearance: none;
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        outline: none;
        transition: opacity 0.2s;
        cursor: pointer;
    }

    .sovereign-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #22d3ee;
        border: 2px solid black;
        cursor: pointer;
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
        transition: transform 0.1s;
    }

    .sovereign-slider::-webkit-slider-thumb:hover {
        transform: scale(1.2);
    }

    .sovereign-slider:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }

    /* Inscription Button */
    .signature-plate {
        width: 100%;
        height: 60px;
        background: rgba(34, 211, 238, 0.05);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        outline: none;
        transition: transform 0.1s;
        user-select: none;
        -webkit-user-select: none;
    }

    .signature-plate:active {
        transform: scale(0.98);
    }

    .plate-bg {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: #22d3ee;
        box-shadow: 0 0 30px rgba(34, 211, 238, 0.8);
        transition: width 0.05s linear;
    }

    /* Seal Animation */
    .seal-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 2px dashed rgba(52, 211, 153, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: spinSlow 20s linear infinite;
        position: relative;
    }

    .seal-inner {
        width: 90px;
        height: 90px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(52, 211, 153, 0.5);
        box-shadow:
            0 0 40px rgba(16, 185, 129, 0.3),
            inset 0 0 20px rgba(16, 185, 129, 0.2);
        animation: spinReverse 15s linear infinite;
    }

    @keyframes spinSlow {
        100% {
            transform: rotate(360deg);
        }
    }

    @keyframes spinReverse {
        0% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(0deg);
        }
    }
</style>
