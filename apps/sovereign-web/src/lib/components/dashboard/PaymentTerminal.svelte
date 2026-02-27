<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { slide } from "svelte/transition";
    import { CreditCard, Send, ShieldCheck, CheckCircle2 } from "lucide-svelte";

    let recipient = $state("");
    let amount = $state(0);
    let reason = $state("");
    let isProcessing = $state(false);
    let status: "IDLE" | "SUCCESS" | "ERROR" = $state("IDLE");

    async function handlePayment() {
        if (!recipient || amount <= 0) return;

        isProcessing = true;
        status = "IDLE";

        // Artificial latency for "Conserved Transfer" verification
        await new Promise((r) => setTimeout(r, 1500));

        const success = manifold.processPayment(
            recipient,
            amount,
            reason,
        );
        isProcessing = false;
        status = success ? "SUCCESS" : "ERROR";

        if (success) {
            recipient = "";
            amount = 0;
            reason = "";
            setTimeout(() => {
                status = "IDLE";
            }, 3000);
        }
    }
</script>

<div
    class="flex flex-col h-full bg-zinc-900/80 rounded-[2.5rem] border border-white/10 backdrop-blur-3xl overflow-hidden p-6 gap-6 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="p-3 bg-white/5 rounded-2xl text-cyan-400">
                <CreditCard size={20} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Payment_Terminal
                </h2>
                <span
                    class="text-[8px] font-black text-white/30 uppercase tracking-widest"
                    >SOVEREIGN PAY v2.4</span
                >
            </div>
        </div>
        <div
            class="px-3 py-1 bg-cyan-400/10 border border-cyan-400/20 rounded-full flex items-center gap-2"
        >
            <ShieldCheck size={12} class="text-cyan-400" />
            <span
                class="text-[8px] font-black text-cyan-400 uppercase tracking-widest"
                >ENCRYPTED</span
            >
        </div>
    </div>

    <!-- Interface -->
    <div class="flex-1 space-y-4">
        <div class="space-y-1.5">
            <label
                for="recipient"
                class="text-[8px] font-black text-white/20 uppercase px-2 mb-1 block"
                >Recipient_Address</label
            >
            <input
                id="recipient"
                type="text"
                bind:value={recipient}
                placeholder="0xADDR..."
                class="w-full bg-black/40 border border-white/5 rounded-2xl p-4 text-xs font-bold text-white placeholder:text-white/10 focus:border-cyan-400/50 outline-none transition-all"
            />
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
                <label
                    for="amount"
                    class="text-[8px] font-black text-white/20 uppercase px-2 mb-1 block"
                    >Amount_CR</label
                >
                <input
                    id="amount"
                    type="number"
                    bind:value={amount}
                    class="w-full bg-black/40 border border-white/5 rounded-2xl p-4 text-xs font-bold text-white focus:border-cyan-400/50 outline-none transition-all"
                />
            </div>
            <div class="space-y-1.5">
                <label
                    for="reason"
                    class="text-[8px] font-black text-white/20 uppercase px-2 mb-1 block"
                    >Reason_Tag</label
                >
                <input
                    id="reason"
                    type="text"
                    bind:value={reason}
                    placeholder="e.g. Services"
                    class="w-full bg-black/40 border border-white/5 rounded-2xl p-4 text-xs font-bold text-white placeholder:text-white/10 focus:border-cyan-400/50 outline-none transition-all"
                />
            </div>
        </div>

        {#if status === "SUCCESS"}
            <div
                class="p-4 bg-emerald-400/10 border border-emerald-400/20 rounded-2xl flex items-center gap-3 text-emerald-400"
                transition:slide
            >
                <CheckCircle2 size={16} />
                <span class="text-[10px] font-black uppercase tracking-widest"
                    >Transaction_Finalized</span
                >
            </div>
        {:else if status === "ERROR"}
            <div
                class="p-4 bg-rose-400/10 border border-rose-400/20 rounded-2xl flex items-center gap-3 text-rose-400"
                transition:slide
            >
                <ShieldCheck size={16} />
                <span class="text-[10px] font-black uppercase tracking-widest"
                    >Insufficient_Resonance</span
                >
            </div>
        {/if}
    </div>

    <!-- Action -->
    <button
        class="w-full py-5 {isProcessing
            ? 'bg-white/10 scale-[0.98]'
            : 'bg-white hover:bg-cyan-400 hover:scale-[1.02]'} text-black text-[11px] font-black uppercase tracking-[0.2em] rounded-[2rem] active:scale-95 transition-all shadow-xl flex items-center justify-center gap-3"
        onclick={handlePayment}
        disabled={isProcessing}
    >
        {#if isProcessing}
            <div
                class="w-4 h-4 border-2 border-black/20 border-t-black rounded-full animate-spin"
            ></div>
            <span>VERIFYING...</span>
        {:else}
            <Send size={16} />
            <span>AUTHORIZE_TRANSFER</span>
        {/if}
    </button>
</div>
