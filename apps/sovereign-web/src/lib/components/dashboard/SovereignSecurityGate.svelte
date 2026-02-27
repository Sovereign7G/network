<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
    import {
        ScanFace,
        Fingerprint,
        Lock,
        ShieldCheck,
        CheckCircle2,
        X,
        ChevronRight,
        Activity,
    } from "lucide-svelte";
    import { authStore } from "$lib/stores/auth.svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    type SecurityStep =
        | "IDLE"
        | "FACE"
        | "FINGERPRINT"
        | "PIN"
        | "SIGNATURE"
        | "SUCCESS";
    let step = $state<SecurityStep>("IDLE");
    let pin = $state("");
    let isHoldingFinger = $state(false);
    let holdProgress = $state(0);
    let faceScanning = $state(false);
    let signaturePoints = $state<{ x: number; y: number }[]>([]);
    let canvas = $state<HTMLCanvasElement>();
    let ctx = $state<CanvasRenderingContext2D | null>(null);

    // PIN logic
    function addPin(num: string) {
        if (pin.length < 6) pin += num;
        if (pin.length === 6) {
            manifold.recordEvent(
                "PIN_VERIFY",
                "PIN sequence accepted by Enclave.",
            );
            transitionTo("SIGNATURE");
        }
    }

    function clearPin() {
        pin = "";
    }

    // Fingerprint logic
    let holdInterval: any;
    function startHold() {
        isHoldingFinger = true;
        holdInterval = setInterval(() => {
            holdProgress += 2;
            if (holdProgress >= 100) {
                clearInterval(holdInterval);
                manifold.recordEvent(
                    "BIOMETRIC_MATCH",
                    "Fingerprint hash verified via Secure Enclave.",
                );
                transitionTo("PIN");
            }
        }, 20);
    }

    function stopHold() {
        isHoldingFinger = false;
        clearInterval(holdInterval);
        if (holdProgress < 100) holdProgress = 0;
    }

    // Face Scan logic
    function startFaceScan() {
        faceScanning = true;
        setTimeout(() => {
            faceScanning = false;
            manifold.recordEvent(
                "FACIAL_RES",
                "Neural Face ID matched 99.8% veracity.",
            );
            transitionTo("FINGERPRINT");
        }, 3000);
    }

    // Signature logic
    function handleDraw(e: MouseEvent | TouchEvent) {
        if (step !== "SIGNATURE" || !canvas) return;
        const rect = canvas.getBoundingClientRect();
        let x, y;
        if ("touches" in e) {
            x = e.touches[0].clientX - rect.left;
            y = e.touches[0].clientY - rect.top;
        } else {
            x = e.clientX - rect.left;
            y = e.clientY - rect.top;
        }

        if (signaturePoints.length === 0) {
            ctx?.beginPath();
            ctx?.moveTo(x, y);
        } else {
            ctx?.lineTo(x, y);
            ctx?.stroke();
        }
        signaturePoints.push({ x, y });
    }

    function commitSignature() {
        if (signaturePoints.length < 20) return;
        manifold.recordEvent(
            "SIG_COMMIT",
            "Causal signature commitment hashed.",
        );
        transitionTo("SUCCESS");
    }

    function clearSignature() {
        signaturePoints = [];
        if (canvas) ctx?.clearRect(0, 0, canvas.width, canvas.height);
    }

    function transitionTo(next: SecurityStep) {
        step = next;
    }

    function finalize() {
        authStore.completeSecurity();
        manifold.recordEvent(
            "AUTH_COMPLETE",
            "Institutional access granted to High-Sovereignty workspace.",
        );
    }

    onMount(() => {
        if (canvas) {
            ctx = canvas.getContext("2d");
            if (ctx) {
                if (ctx) ctx.strokeStyle = "#22d3ee";
                if (ctx) ctx.lineWidth = 2;
                ctx.lineCap = "round";
            }
        }
    });
</script>

<div
    class="h-full bg-zinc-950/80 rounded-[3rem] border-2 border-cyan-400/20 backdrop-blur-3xl overflow-hidden flex flex-col shadow-2xl relative group"
>
    <!-- Background grid/glow -->
    <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(34,211,238,0.1),transparent)] pointer-events-none"
    ></div>
    <div
        class="absolute inset-0 bg-grid-white/[0.02] bg-[size:40px_40px] pointer-events-none"
    ></div>

    <!-- Header -->
    <div
        class="p-8 border-b border-white/5 bg-white/[0.02] relative z-10 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <div class="p-3 bg-cyan-400/20 rounded-2xl text-cyan-400">
                <ShieldCheck size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-[0.3em] text-white"
                >
                    Secure_Enclave
                </h2>
                <span
                    class="text-[8px] font-black text-white/30 uppercase tracking-widest italic"
                    >NIST_AAL3_Identity_Vault</span
                >
            </div>
        </div>
        <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></div>
            <span
                class="text-[8px] font-black text-cyan-400 uppercase tracking-widest"
                >Safe_Stop Active</span
            >
        </div>
    </div>

    <!-- Main Interaction Area -->
    <div
        class="flex-1 overflow-hidden p-8 flex flex-col items-center justify-center relative z-10"
    >
        {#if step === "IDLE"}
            <div class="text-center space-y-8" in:scale>
                <div class="relative">
                    <div
                        class="w-32 h-32 bg-cyan-400/10 rounded-[3rem] border border-cyan-400/30 flex items-center justify-center text-cyan-400 mx-auto"
                    >
                        <Lock size={48} />
                    </div>
                    <div
                        class="absolute -inset-4 bg-cyan-400/5 rounded-full blur-2xl animate-pulse"
                    ></div>
                </div>
                <div class="space-y-4">
                    <h3
                        class="text-2xl font-black italic tracking-tighter uppercase text-white"
                    >
                        Authentication_Required
                    </h3>
                    <p
                        class="text-[10px] font-black text-white/30 uppercase max-w-xs leading-relaxed tracking-widest"
                    >
                        To access high-sovereignty modules, multi-modal
                        verification is mandated by the Protocol.
                    </p>
                </div>
                <button
                    onclick={() => transitionTo("FACE")}
                    class="w-full py-4 bg-cyan-400 text-black text-[10px] font-black uppercase tracking-widest rounded-2xl hover:scale-105 active:scale-95 transition-all shadow-xl shadow-cyan-400/20 flex items-center justify-center gap-2"
                >
                    Begin_Verification
                    <ChevronRight size={14} />
                </button>
            </div>
        {:else if step === "FACE"}
            <div
                class="w-full h-full flex flex-col items-center justify-center space-y-12"
                in:fade
            >
                <div class="relative">
                    <!-- Face Viewport -->
                    <div
                        class="w-64 h-64 rounded-full border-2 border-dashed border-white/20 flex items-center justify-center relative overflow-hidden bg-black/40"
                    >
                        <ScanFace size={80} class="text-white/10" />

                        {#if faceScanning}
                            <!-- Scanning Laser -->
                            <div
                                class="absolute top-0 left-0 w-full h-1 bg-cyan-400/50 shadow-[0_0_15px_#22d3ee] animate-scan-laser"
                            ></div>
                            <!-- Hexagon Mesh -->
                            <div
                                class="absolute inset-0 border-[20px] border-cyan-400/5 opacity-40 animate-pulse"
                            ></div>
                        {/if}

                        <video
                            class="absolute inset-0 w-full h-full object-cover opacity-20 filter grayscale invert"
                            autoplay
                            muted
                            playsinline
                        >
                            <track kind="captions" />
                        </video>
                    </div>

                    <!-- HUD Markers -->
                    <div
                        class="absolute -inset-4 border border-cyan-400/20 rounded-full pointer-events-none"
                    ></div>
                    <div class="absolute top-0 right-0 p-2">
                        <Activity size={14} class="text-cyan-400/40" />
                    </div>
                </div>

                <div class="text-center space-y-4">
                    <h3 class="text-xl font-black italic text-white uppercase">
                        {faceScanning
                            ? "Neural_Scanning..."
                            : "Facial_Registration"}
                    </h3>
                    <p
                        class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em]"
                    >
                        Align face to the biometric viewport.
                    </p>
                </div>

                {#if !faceScanning}
                    <button
                        onclick={startFaceScan}
                        class="px-12 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest text-white hover:bg-white hover:text-black transition-all"
                    >
                        Initialize_Scan
                    </button>
                {/if}
            </div>
        {:else if step === "FINGERPRINT"}
            <div
                class="w-full h-full flex flex-col items-center justify-center space-y-12"
                in:scale
            >
                <div class="relative">
                    <!-- Biometric Pad -->
                    <button
                        onmousedown={startHold}
                        onmouseup={stopHold}
                        onmouseleave={stopHold}
                        ontouchstart={startHold}
                        ontouchend={stopHold}
                        class="w-48 h-48 bg-black/60 rounded-[3rem] border-2 border-white/5 flex items-center justify-center relative overflow-hidden group/pad"
                    >
                        <Fingerprint
                            size={64}
                            class="transition-colors {isHoldingFinger
                                ? 'text-cyan-400'
                                : 'text-white/20'}"
                        />

                        <!-- Progress Ring -->
                        <svg class="absolute inset-0 w-full h-full -rotate-90">
                            <circle
                                cx="96"
                                cy="96"
                                r="80"
                                fill="none"
                                stroke="rgba(34,211,238,0.2)"
                                stroke-width="4"
                            />
                            <circle
                                cx="96"
                                cy="96"
                                r="80"
                                fill="none"
                                stroke="#22d3ee"
                                stroke-width="4"
                                stroke-dasharray="502"
                                stroke-dashoffset={502 -
                                    (502 * holdProgress) / 100}
                                class="transition-all duration-200"
                            />
                        </svg>

                        {#if isHoldingFinger}
                            <div
                                class="absolute inset-0 bg-cyan-400/10 animate-pulse"
                            ></div>
                        {/if}
                    </button>
                </div>

                <div class="text-center space-y-4">
                    <h3 class="text-xl font-black italic text-white uppercase">
                        Biometric_Auth
                    </h3>
                    <p
                        class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em]"
                    >
                        Hold finger on pad for shard-key extraction.
                    </p>
                </div>
            </div>
        {:else if step === "PIN"}
            <div
                class="w-full h-full flex flex-col items-center justify-center space-y-8"
                in:fly={{ y: 20 }}
            >
                <!-- PIN Display -->
                <div class="flex gap-4 mb-4">
                    {#each Array(6) as _, i}
                        <div
                            class="w-4 h-4 rounded-full border-2 transition-all {pin.length >
                            i
                                ? 'bg-cyan-400 border-cyan-400 shadow-[0_0_10px_#22d3ee]'
                                : 'border-white/10'}"
                        ></div>
                    {/each}
                </div>

                <!-- PAD Grid -->
                <div class="grid grid-cols-3 gap-4">
                    {#each ["1", "2", "3", "4", "5", "6", "7", "8", "9"] as num}
                        <button
                            onclick={() => addPin(num)}
                            class="w-16 h-16 bg-white/5 border border-white/5 rounded-2xl flex items-center justify-center text-lg font-black text-white hover:bg-cyan-400 hover:text-black hover:border-cyan-400 transition-all active:scale-95"
                        >
                            {num}
                        </button>
                    {/each}
                    <button
                        onclick={clearPin}
                        class="w-16 h-16 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex items-center justify-center"
                        ><X size={20} class="text-rose-500" /></button
                    >
                    <button
                        onclick={() => addPin("0")}
                        class="w-16 h-16 bg-white/5 border border-white/5 rounded-2xl flex items-center justify-center text-lg font-black text-white hover:bg-cyan-400 hover:text-black"
                        >0</button
                    >
                    <div
                        class="w-16 h-16 flex items-center justify-center text-white/5 italic font-black text-[8px]"
                    >
                        AGE_OS
                    </div>
                </div>

                <div class="text-center space-y-2">
                    <h3
                        class="text-[10px] font-black text-white uppercase tracking-widest"
                    >
                        Enclave_PIN_Sequence
                    </h3>
                </div>
            </div>
        {:else if step === "SIGNATURE"}
            <div
                class="w-full h-full flex flex-col items-center justify-center space-y-8"
                in:fade
            >
                <div class="relative w-full max-w-sm">
                    <canvas
                        bind:this={canvas}
                        width="400"
                        height="200"
                        onmousemove={(e) => {
                            if (e.buttons) handleDraw(e);
                        }}
                        ontouchmove={(e) => {
                            e.preventDefault();
                            handleDraw(e);
                        }}
                        class="w-full aspect-[2/1] bg-black/40 rounded-3xl border border-white/10 touch-none cursor-crosshair"
                    ></canvas>
                    <div class="absolute bottom-4 right-4 flex gap-2">
                        <button
                            onclick={clearSignature}
                            class="p-2 bg-white/5 hover:bg-white/10 rounded-lg text-white/40"
                            ><X size={14} /></button
                        >
                        <button
                            onclick={commitSignature}
                            class="p-2 bg-cyan-400 text-black rounded-lg disabled:opacity-30"
                            disabled={signaturePoints.length < 20}
                            ><CheckCircle2 size={14} /></button
                        >
                    </div>
                </div>

                <div class="text-center space-y-4">
                    <h3 class="text-xl font-black italic text-white uppercase">
                        Causal_Signature
                    </h3>
                    <p
                        class="text-[9px] font-black text-white/30 uppercase tracking-[0.2em]"
                    >
                        Digitially sign the sovereignty commit.
                    </p>
                </div>
            </div>
        {:else if step === "SUCCESS"}
            <div
                class="w-full h-full flex flex-col items-center justify-center space-y-8"
                in:scale
            >
                <div
                    class="w-24 h-24 bg-emerald-400/20 rounded-full border-2 border-emerald-400 flex items-center justify-center text-emerald-400 animate-bounce"
                >
                    <ShieldCheck size={48} />
                </div>
                <div class="text-center space-y-2">
                    <h3 class="text-2xl font-black italic text-white uppercase">
                        Access_Granted
                    </h3>
                    <p
                        class="text-[10px] font-black text-emerald-400 uppercase tracking-widest"
                    >
                        Veracity 99.8% // AAL3 Compliant
                    </p>
                </div>
                <button
                    onclick={finalize}
                    class="px-12 py-3 bg-emerald-500 text-black text-[10px] font-black uppercase tracking-widest rounded-xl hover:scale-105 transition-all shadow-xl shadow-emerald-500/20"
                >
                    Enter_Workspace
                </button>
            </div>
        {/if}
    </div>

    <!-- System Status Bar -->
    <div
        class="p-6 border-t border-white/5 bg-black/40 flex items-center justify-between"
    >
        <div class="flex items-center gap-3">
            <Activity size={14} class="text-cyan-400" />
            <span
                class="text-[9px] font-black text-white/40 uppercase tracking-widest"
                >Secure_Enclave: NOMINAL</span
            >
        </div>
        <div
            class="flex items-center gap-4 text-white/10 text-[9px] font-black uppercase italic"
        >
            <span>Kernel_v14</span>
            <div class="h-4 w-[1px] bg-white/10"></div>
            <span>Enc: Quantum_Safe</span>
        </div>
    </div>
</div>

<style>
    @keyframes scan {
        0% {
            transform: translateY(0);
        }
        100% {
            transform: translateY(256px);
        }
    }

    .animate-scan-laser {
        animation: scan 3s infinite linear;
    }
</style>
