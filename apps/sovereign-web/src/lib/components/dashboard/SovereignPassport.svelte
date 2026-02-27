<!--
[IN]: icpService, manifold
[OUT]: SovereignPassport Component
[POS]: Layer 1 Sovereign Identity and Passport manifestation interface. / Layer 1 Sovereign Identity \u548c Passport \u663e\u5316\u63a5\u53e3\u3022
Protocol: When updating me, sync this header + parent folder's .folder.md
-->
<script lang="ts">
    import { fade, scale } from "svelte/transition";
    import {
        ShieldCheck,
        Fingerprint,
        Globe,
        Download,
        Share2,
        UserCheck,
    } from "lucide-svelte";
    import {
        credentialService,
        type SovereignCredential,
    } from "$lib/services/credential-service";

    interface Props {
        credential: SovereignCredential;
        onClose?: () => void;
    }

    let { credential, onClose }: Props = $props();

    const formattedDate = $derived(
        new Date(credential.issuanceDate).toLocaleDateString(undefined, {
            year: "numeric",
            month: "long",
            day: "numeric",
        }),
    );

    const shortId = $derived(
        credential.credentialSubject.id.split(":").pop() || "",
    );
</script>

<div
    class="passport-overlay fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-xl bg-black/80"
    in:fade
>
    <div
        class="passport-container relative w-full max-w-md aspect-[1/1.5] bg-[#0c0c0e] rounded-[3rem] border border-white/10 shadow-[0_0_100px_rgba(34,211,238,0.2)] overflow-hidden flex flex-col"
        in:scale={{ start: 0.9 }}
    >
        <!-- Holographic Top Wave -->
        <div
            class="absolute top-0 inset-x-0 h-32 bg-gradient-to-b from-cyan-500/20 to-transparent blur-3xl -z-10 animate-pulse"
        ></div>

        <!-- Header -->
        <div class="p-8 pt-10 text-center space-y-2">
            <div class="flex justify-center mb-4">
                <div class="p-4 bg-white/5 border border-white/10 rounded-full">
                    <Globe size={40} class="text-cyan-400" />
                </div>
            </div>
            <h1
                class="text-2xl font-black text-white tracking-widest uppercase"
            >
                Sovereign Passport
            </h1>
            <p
                class="text-[8px] font-black text-cyan-400 uppercase tracking-[0.4em]"
            >
                Decentralized Institutional Identity
            </p>
        </div>

        <!-- ID Card Body -->
        <div class="flex-1 px-8 space-y-8">
            <!-- Avatar / Biometric Placeholder -->
            <div class="flex justify-center">
                <div class="relative w-40 h-40">
                    <div
                        class="absolute inset-0 border-2 border-cyan-400/20 border-dashed rounded-3xl animate-spin-slow"
                    ></div>
                    <div
                        class="absolute inset-4 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 backdrop-blur-md overflow-hidden group"
                    >
                        <Fingerprint
                            size={60}
                            class="text-white/20 group-hover:text-cyan-400 transition-colors duration-500"
                        />
                        <div
                            class="absolute bottom-2 inset-x-2 h-0.5 bg-cyan-400/40 animate-scan"
                        ></div>
                    </div>
                    <!-- Status Badge -->
                    <div
                        class="absolute -bottom-2 -right-2 bg-emerald-500 text-black px-3 py-1 rounded-full text-[7px] font-black uppercase flex items-center gap-1 shadow-lg shadow-emerald-500/20"
                    >
                        <ShieldCheck size={10} />
                        Active
                    </div>
                </div>
            </div>

            <!-- Identity Details -->
            <div class="space-y-4 pt-4">
                <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-1">
                        <span
                            class="text-[7px] font-black uppercase text-white/20 tracking-widest"
                            >Principal_ID</span
                        >
                        <p class="text-[10px] font-mono text-white/80 truncate">
                            {shortId}
                        </p>
                    </div>
                    <div class="space-y-1">
                        <span
                            class="text-[7px] font-black uppercase text-white/20 tracking-widest"
                            >Issued_Date</span
                        >
                        <p class="text-[10px] font-mono text-white/80">
                            {formattedDate}
                        </p>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-1">
                        <span
                            class="text-[7px] font-black uppercase text-white/20 tracking-widest"
                            >Resonance_Tier</span
                        >
                        <div class="flex items-center gap-2">
                            <div
                                class="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.5)]"
                            ></div>
                            <p
                                class="text-[10px] font-black text-cyan-400 uppercase tracking-tighter"
                            >
                                {credential.credentialSubject.status}
                            </p>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <span
                            class="text-[7px] font-black uppercase text-white/20 tracking-widest"
                            >Manifestation_Index</span
                        >
                        <p class="text-[10px] font-mono text-white/80">
                            {(
                                credential.credentialSubject.resonanceScore *
                                100
                            ).toFixed(2)}%
                        </p>
                    </div>
                </div>
            </div>

            <!-- Cryptographic Proof Footer -->
            <div
                class="mt-8 p-4 bg-white/5 border border-white/5 rounded-2xl space-y-2"
            >
                <div
                    class="flex justify-between items-center text-[6px] font-black uppercase text-white/30 tracking-widest"
                >
                    <span>ECC_Threshold_Signature</span>
                    <span>Verified_by_BioVault</span>
                </div>
                <p
                    class="text-[7px] font-mono text-white/10 break-all leading-tight"
                >
                    {credential.proof.jws}
                </p>
            </div>
        </div>

        <!-- Actions -->
        <div
            class="p-8 grid grid-cols-3 gap-3 border-t border-white/5 bg-black/40"
        >
            <button
                onclick={() => credentialService.downloadCredential(credential)}
                class="flex flex-col items-center gap-2 p-3 bg-white/5 hover:bg-white/10 rounded-2xl transition-all border border-white/5"
            >
                <Download size={16} class="text-white/40" />
                <span class="text-[7px] font-black uppercase text-white/40"
                    >Archive</span
                >
            </button>
            <button
                class="flex flex-col items-center gap-2 p-3 bg-cyan-500/10 hover:bg-cyan-500/20 rounded-2xl transition-all border border-cyan-500/20"
                onclick={onClose}
            >
                <UserCheck size={16} class="text-cyan-400" />
                <span class="text-[7px] font-black uppercase text-cyan-400"
                    >Complete</span
                >
            </button>
            <button
                class="flex flex-col items-center gap-2 p-3 bg-white/5 hover:bg-white/10 rounded-2xl transition-all border border-white/5"
            >
                <Share2 size={16} class="text-white/40" />
                <span class="text-[7px] font-black uppercase text-white/40"
                    >Attest</span
                >
            </button>
        </div>
    </div>
</div>

<style>
    .passport-container {
        background: linear-gradient(180deg, #0c0c0e 0%, #060608 100%);
    }

    .animate-spin-slow {
        animation: spin 8s linear infinite;
    }

    .animate-scan {
        animation: scan 2s ease-in-out infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes scan {
        0%,
        100% {
            transform: translateY(-30px);
            opacity: 0;
        }
        50% {
            transform: translateY(120px);
            opacity: 1;
        }
    }
</style>
