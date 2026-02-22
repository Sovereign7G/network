<script lang="ts">
    import { MapPin, Car, Activity } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import LivingMap from "../map/LivingMap.svelte";

    let pickup = $state("");
    let destination = $state("");
    let calculating = $state(false);

    function calculateRoute() {
        calculating = true;
        setTimeout(() => {
            calculating = false;
        }, 2000);
    }
</script>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6" in:fade>
    <div class="glass-panel p-8 card-glow space-y-6">
        <h3
            class="text-xl font-black italic flex items-center gap-3 uppercase tracking-tighter"
        >
            <Car class="text-neon-cyan" size={24} />
            Mobility Intent
        </h3>

        <div class="space-y-4">
            <div class="space-y-2">
                <label
                    for="pickup-vector"
                    class="text-[10px] font-black text-white/40 uppercase mono-font tracking-widest"
                    >Pickup Vector</label
                >
                <div
                    class="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl px-4 py-2 focus-within:border-neon-cyan/50 transition-all"
                >
                    <MapPin size={18} class="text-neon-cyan" />
                    <input
                        id="pickup-vector"
                        type="text"
                        placeholder="Origin Coordinates"
                        bind:value={pickup}
                        class="bg-transparent border-none outline-none text-white text-sm w-full placeholder:text-white/20"
                    />
                </div>
            </div>

            <div class="space-y-2">
                <label
                    for="destination-vector"
                    class="text-[10px] font-black text-white/40 uppercase mono-font tracking-widest"
                    >Destination Vector</label
                >
                <div
                    class="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl px-4 py-2 focus-within:border-neon-cyan/50 transition-all"
                >
                    <MapPin size={18} class="text-purple-400" />
                    <input
                        id="destination-vector"
                        type="text"
                        placeholder="Target Coordinates"
                        bind:value={destination}
                        class="bg-transparent border-none outline-none text-white text-sm w-full placeholder:text-white/20"
                    />
                </div>
            </div>
        </div>

        <button
            onclick={calculateRoute}
            disabled={calculating}
            class="w-full bg-neon-cyan text-black font-black py-4 uppercase tracking-tighter italic text-lg hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
        >
            {calculating
                ? "CALCULATING PHASE SPACE..."
                : "CALCULATE METABOLIC ROUTE"}
        </button>
    </div>

    <div class="glass-panel overflow-hidden relative">
        <LivingMap />

        {#if calculating}
            <div
                class="absolute inset-0 bg-black/60 flex items-center justify-center backdrop-blur-sm"
                in:fade
            >
                <div class="text-center space-y-4">
                    <Activity
                        size={48}
                        class="mx-auto text-neon-cyan animate-pulse"
                    />
                    <p
                        class="text-[10px] font-black text-white/40 uppercase mono-font tracking-[0.2em]"
                    >
                        Mapping Real-time Phase Space...
                    </p>
                </div>
            </div>
        {/if}
    </div>
</div>
