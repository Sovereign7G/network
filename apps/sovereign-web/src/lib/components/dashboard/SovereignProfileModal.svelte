<script lang="ts">
    import { X, ShoppingBag, Wallet, Star } from "lucide-svelte";
    import { fade, scale } from "svelte/transition";

    interface Props {
        showProfile: boolean;
        profileName: string;
        profileStatus: string;
        profileBg: string;
        onClose: () => void;
    }

    let {
        showProfile = $bindable(),
        profileName,
        profileStatus,
        profileBg,
        onClose,
    }: Props = $props();
</script>

{#if showProfile}
    <div
        class="fixed inset-0 z-[120] bg-black/40 backdrop-blur-md flex items-center justify-center p-6"
        transition:fade
    >
        <div
            class="max-w-md w-full bg-white rounded-[3rem] overflow-hidden shadow-2xl flex flex-col"
            in:scale={{ duration: 400, start: 0.9 }}
        >
            <!-- Profile Cover -->
            <div class="h-64 {profileBg} relative">
                <button
                    onclick={onClose}
                    class="absolute top-6 right-6 p-2 bg-black/10 rounded-full text-white/60 hover:text-white"
                >
                    <X size={24} />
                </button>
            </div>

            <!-- Profile Content -->
            <div
                class="px-10 pb-12 -mt-20 flex flex-col items-center text-center space-y-6"
            >
                <div
                    class="w-32 h-32 rounded-[2.5rem] bg-black border-8 border-white shadow-xl overflow-hidden flex items-center justify-center text-white font-black italic text-4xl"
                >
                    {profileName[0]}
                </div>

                <div class="space-y-2">
                    <h3
                        class="text-2xl font-black italic text-[#3C1E1E] uppercase tracking-tighter"
                    >
                        {profileName}
                    </h3>
                    <p
                        class="text-[10px] font-medium text-[#3C1E1E]/40 uppercase tracking-widest"
                    >
                        {profileStatus}
                    </p>
                </div>

                <div class="grid grid-cols-2 gap-4 w-full">
                    <button
                        class="py-4 bg-[#F2F2F2] rounded-2xl text-[8px] font-black uppercase text-[#3C1E1E]/60 hover:bg-black/5"
                        >Edit Profile</button
                    >
                    <button
                        class="py-4 bg-[#FAE100] rounded-2xl text-[8px] font-black uppercase text-[#3C1E1E] shadow-lg shadow-yellow-500/20"
                        >Sovereign Talk</button
                    >
                </div>

                <div
                    class="w-full border-t border-black/5 pt-8 grid grid-cols-3 gap-6"
                >
                    <div class="flex flex-col items-center gap-2">
                        <div
                            class="w-10 h-10 rounded-xl bg-orange-500/10 text-orange-500 flex items-center justify-center"
                        >
                            <ShoppingBag size={18} />
                        </div>
                        <span
                            class="text-[7px] font-black text-black/40 uppercase"
                            >Orders</span
                        >
                    </div>
                    <div class="flex flex-col items-center gap-2">
                        <div
                            class="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center"
                        >
                            <Wallet size={18} />
                        </div>
                        <span
                            class="text-[7px] font-black text-black/40 uppercase"
                            >Pay</span
                        >
                    </div>
                    <div class="flex flex-col items-center gap-2">
                        <div
                            class="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center"
                        >
                            <Star size={18} />
                        </div>
                        <span
                            class="text-[7px] font-black text-black/40 uppercase"
                            >Gifts</span
                        >
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}
