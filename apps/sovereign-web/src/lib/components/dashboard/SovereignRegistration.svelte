<script lang="ts">
    import {
        User,
        Mail,
        Phone,
        ShieldCheck,
        Fingerprint,
        FileText,

        Calendar,
        Upload,
        Check,
        AlertCircle,
        ArrowRight,
        Zap,
        Lock,
    } from "lucide-svelte";
    import { fade, fly, slide, scale } from "svelte/transition";

    let step = $state(1);

    let formData = $state({
        fullName: "",
        email: "",
        phone: "",
        identityType: "AURA_KEY",
        identificationNumber: "",
        consent: false,
    });

    let isSubmitting = $state(false);

    function nextStep() {
        if (step < 3) step += 1;
    }

    async function handleSubmit() {
        isSubmitting = true;
        // Simulate AAL3 Handshake/Registration
        await new Promise((r) => setTimeout(r, 2500));
        step = 4;
        isSubmitting = false;
    }
</script>

<div class="max-w-3xl mx-auto py-12 px-6" in:fade>
    <!-- Logo/Header -->
    <div class="flex items-center gap-4 mb-20">
        <div
            class="w-12 h-12 rounded-xl bg-[#24AE7C]/20 border border-[#24AE7C]/40 flex items-center justify-center text-[#24AE7C]"
        >
            <Zap size={24} />
        </div>
        <div>
            <h1 class="text-3xl font-black italic tracking-tighter uppercase">
                CARE_PULSE // AGE_REG
            </h1>
            <p
                class="text-[10px] mono-font text-white/40 uppercase tracking-[0.4em] mt-1"
            >
                High-Trust Sovereign Onboarding Protocol
            </p>
        </div>
    </div>

    <!-- Progress Steps -->
    <div class="flex items-center justify-between mb-16 relative">
        <div
            class="absolute top-1/2 left-0 w-full h-0.5 bg-white/5 -translate-y-1/2 -z-10"
        ></div>
        <div
            class="absolute top-1/2 left-0 h-0.5 bg-[#24AE7C] -translate-y-1/2 -z-10 transition-all duration-700"
            style="width: {(step - 1) * 50}%"
        ></div>

        {#each [1, 2, 3] as s}
            <div
                class="w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500 border-2
                {step >= s
                    ? 'bg-[#24AE7C] border-[#24AE7C] text-black'
                    : 'bg-black border-white/10 text-white/20'}"
            >
                {#if step > s}
                    <Check size={20} strokeWidth={3} />
                {:else}
                    <span class="text-sm font-black italic">{s}</span>
                {/if}
            </div>
        {/each}
    </div>

    <div class="glass-panel p-12 bg-black/40 border-white/[0.03]">
        {#if step === 1}
            <div in:fly={{ x: 20, duration: 500 }} class="space-y-8">
                <div>
                    <h2
                        class="text-2xl font-black italic tracking-tighter uppercase"
                    >
                        CITIZEN_IDENTIFICATION
                    </h2>
                    <p
                        class="text-[10px] mono-font text-white/40 uppercase tracking-[0.2em] mt-2"
                    >
                        Personal details for protocol anchoring.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="space-y-3">
                        <label
                            class="text-[9px] font-black uppercase tracking-widest text-white/50 px-1"
                            >FULL_NAME</label
                        >
                        <div class="relative">
                            <User
                                size={16}
                                class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20"
                            />
                            <input
                                type="text"
                                bind:value={formData.fullName}
                                placeholder="ALEX_S_NOVAK"
                                class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 pl-12 pr-6 text-sm focus:border-neon-cyan/40 focus:outline-none transition-all"
                            />
                        </div>
                    </div>
                    <div class="space-y-3">
                        <label
                            class="text-[9px] font-black uppercase tracking-widest text-white/50 px-1"
                            >EMAIL_ADDRESS</label
                        >
                        <div class="relative">
                            <Mail
                                size={16}
                                class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20"
                            />
                            <input
                                type="email"
                                bind:value={formData.email}
                                placeholder="ALEX@PROTOCOL.SOV"
                                class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 pl-12 pr-6 text-sm focus:border-neon-cyan/40 focus:outline-none transition-all"
                            />
                        </div>
                    </div>
                </div>

                <div class="space-y-3">
                    <label
                        class="text-[9px] font-black uppercase tracking-widest text-white/50 px-1"
                        >SOVEREIGN_CONTACT (SMS_ALERTS)</label
                    >
                    <div class="relative">
                        <Phone
                            size={16}
                            class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20"
                        />
                        <input
                            type="tel"
                            bind:value={formData.phone}
                            placeholder="+1 (555) 000-0000"
                            class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 pl-12 pr-6 text-sm focus:border-neon-cyan/40 focus:outline-none transition-all"
                        />
                    </div>
                </div>

                <button
                    onclick={nextStep}
                    class="w-full py-5 bg-[#24AE7C] text-black font-black uppercase tracking-tighter text-lg rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3"
                >
                    PROCEED_TO_SECURITY <ArrowRight size={20} />
                </button>
            </div>
        {:else if step === 2}
            <div in:fly={{ x: 20, duration: 500 }} class="space-y-8">
                <div>
                    <h2
                        class="text-2xl font-black italic tracking-tighter uppercase"
                    >
                        SECURITY_ATTESTATION
                    </h2>
                    <p
                        class="text-[10px] mono-font text-white/40 uppercase tracking-[0.2em] mt-2"
                    >
                        Credential verification and AAL3 handshake.
                    </p>
                </div>

                <div class="space-y-3">
                    <label
                        class="text-[9px] font-black uppercase tracking-widest text-white/50 px-1"
                        >IDENTIFICATION_TYPE</label
                    >
                    <select
                        bind:value={formData.identityType}
                        class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 px-6 text-sm appearance-none focus:border-neon-cyan/40 focus:outline-none transition-all"
                    >
                        <option value="AURA_KEY">AURA_IDENTITY_KEY</option>
                        <option value="BIOMETRIC_SEED"
                            >BIOMETRIC_SEED_ANCHOR</option
                        >
                        <option value="GOV_ID">SOVEREIGN_INSTITUTION_ID</option>
                    </select>
                </div>

                <div class="space-y-3">
                    <label
                        class="text-[9px] font-black uppercase tracking-widest text-white/50 px-1"
                        >IDENTIFICATION_NUMBER / PIN</label
                    >
                    <div class="relative">
                        <Fingerprint
                            size={16}
                            class="absolute left-4 top-1/2 -translate-y-1/2 text-white/20"
                        />
                        <input
                            type="password"
                            bind:value={formData.identificationNumber}
                            placeholder="•••• •••• •••• ••••"
                            class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 pl-12 pr-6 text-sm focus:border-neon-cyan/40 focus:outline-none transition-all"
                        />
                    </div>
                </div>

                <div
                    class="p-8 rounded-3xl border border-dashed border-white/10 bg-white/[0.02] flex flex-col items-center justify-center text-center space-y-4 cursor-pointer hover:bg-white/[0.04] transition-all"
                >
                    <div
                        class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center text-white/30"
                    >
                        <Upload size={32} />
                    </div>
                    <div>
                        <span
                            class="text-xs font-black uppercase tracking-widest block"
                            >UPLOAD_CREDIENTIALS_STAMP</span
                        >
                        <span
                            class="text-[8px] mono-font text-white/20 uppercase tracking-[0.3em] mt-2"
                            >SVG_PNG_JPG (MAX_10MB)</span
                        >
                    </div>
                </div>

                <div class="flex gap-4">
                    <button
                        onclick={() => (step = 1)}
                        class="flex-1 py-5 bg-white/5 border border-white/10 text-white/40 font-black uppercase tracking-tighter text-lg rounded-2xl hover:bg-white/10 transition-all"
                    >
                        BACK
                    </button>
                    <button
                        onclick={nextStep}
                        class="flex-[2] py-5 bg-[#24AE7C] text-black font-black uppercase tracking-tighter text-lg rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3"
                    >
                        CONSENT_&_VERIFY <ArrowRight size={20} />
                    </button>
                </div>
            </div>
        {:else if step === 3}
            <div in:fly={{ x: 20, duration: 500 }} class="space-y-10">
                <div>
                    <h2
                        class="text-2xl font-black italic tracking-tighter uppercase"
                    >
                        PROTOCOL_CONSENT
                    </h2>
                    <p
                        class="text-[10px] mono-font text-white/40 uppercase tracking-[0.2em] mt-2"
                    >
                        Finalization of the Sovereign Handshake.
                    </p>
                </div>

                <div class="space-y-6">
                    <label
                        class="flex items-start gap-4 p-6 bg-white/[0.02] border border-white/5 rounded-3xl cursor-pointer hover:bg-white/[0.04] transition-all"
                    >
                        <input
                            type="checkbox"
                            bind:checked={formData.consent}
                            class="mt-1 w-5 h-5 accent-[#24AE7C]"
                        />
                        <div
                            class="text-[10px] text-white/40 leading-relaxed uppercase tracking-widest"
                        >
                            I CONSENT TO THE AUTOMATED COLLECTION AND PROCESSING
                            OF MY SOVEREIGN DATA AS DEFINED IN THE <span
                                class="text-[#24AE7C] underline"
                                >CITIZEN_RIGHTS_SUBSTRATE</span
                            >. I UNDERSTAND THIS ANCHOR IS IMMUTABLE.
                        </div>
                    </label>
                </div>

                <div
                    class="p-8 bg-amber-400/5 border border-amber-400/20 rounded-3xl flex items-start gap-4"
                >
                    <AlertCircle
                        size={20}
                        class="text-amber-400 shrink-0 mt-0.5"
                    />
                    <p
                        class="text-[9px] text-amber-400/80 leading-relaxed uppercase tracking-widest"
                    >
                        WARNING: ATTESTING TO FALSE CREDENTIALS WILL RESULT IN
                        IMMEDIATE JADE_MONOLITH LOCKDOWN AND RECOVERY PROTOCOL
                        INITIATION AS PER THE FOUNDATION SECURITY RULES.
                    </p>
                </div>

                <button
                    onclick={handleSubmit}
                    disabled={!formData.consent || isSubmitting}
                    class="w-full py-6 bg-[#24AE7C] text-black font-black uppercase tracking-tighter text-2xl rounded-[2rem] hover:scale-[1.02] active:scale-[0.98] disabled:opacity-20 disabled:grayscale transition-all flex items-center justify-center gap-4 shadow-[0_0_40px_rgba(36,174,124,0.3)]"
                >
                    {#if isSubmitting}
                        <div
                            class="w-6 h-6 border-4 border-black border-t-transparent rounded-full animate-spin"
                        ></div>
                        ANCHORING_IDENTITY...
                    {:else}
                        INITIALIZE_ANCHOR <ShieldCheck size={28} />
                    {/if}
                </button>
            </div>
        {:else if step === 4}
            <div
                in:scale={{ duration: 800 }}
                class="flex flex-col items-center py-10 space-y-10 text-center"
            >
                <div
                    class="w-32 h-32 rounded-full bg-[#24AE7C]/20 border-2 border-[#24AE7C] flex items-center justify-center text-[#24AE7C] animate-bounce"
                >
                    <Check size={60} strokeWidth={4} />
                </div>
                <div>
                    <h2
                        class="text-5xl font-black italic tracking-tighter uppercase text-[#24AE7C]"
                    >
                        CITIZEN_VERIFIED
                    </h2>
                    <p
                        class="text-[14px] mono-font text-white/40 uppercase tracking-[0.5em] mt-4"
                    >
                        Welcome to the Sovereign Substrate, Alex.
                    </p>
                </div>
                <div
                    class="p-8 bg-white/5 border border-white/10 rounded-[2.5rem] flex items-center gap-6 text-left w-full max-w-sm"
                >
                    <div
                        class="w-14 h-14 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center text-neon-cyan"
                    >
                        <Lock size={24} />
                    </div>
                    <div>
                        <span
                            class="text-[8px] font-black text-white/20 uppercase tracking-widest block mb-1"
                            >ALLOCATED_PIN_ID</span
                        >
                        <span
                            class="text-sm mono-font font-black tracking-widest italic"
                            >CP-AGE-8821-X99</span
                        >
                    </div>
                </div>
                <button
                    onclick={() => (step = 1)}
                    class="px-12 py-5 bg-white/10 border border-white/10 rounded-2xl text-sm font-black uppercase tracking-widest hover:bg-white/20 transition-all"
                >
                    ENTER_COMMAND_CENTER
                </button>
            </div>
        {/if}
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(80px);
        border-radius: 3rem;
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.8);
    }

    :global(body) {
        background: radial-gradient(
            circle at top right,
            #112c24 0%,
            #020408 50%
        );
    }

    select option {
        background: #0a0a0a;
        color: white;
    }
</style>
