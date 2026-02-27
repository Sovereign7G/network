<script lang="ts">
    import { manifold } from "$lib/stores/master-store.svelte";
    import { slide } from "svelte/transition";
    import { Briefcase, Target, Zap, Trophy, Play } from "lucide-svelte";

    const business = $derived(manifold.businessState);

    function startJob(id: string) {

        const job = business.activeJobs.find((j) => j.id === id);
        if (job) job.status = "RUNNING";
    }
</script>

<div
    class="flex flex-col h-full bg-slate-900/60 rounded-[3rem] border border-white/10 backdrop-blur-3xl overflow-hidden p-8 gap-8 shadow-2xl relative group"
>
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="p-4 bg-white/5 rounded-2xl text-amber-400">
                <Briefcase size={24} />
            </div>
            <div>
                <h2
                    class="text-xs font-black uppercase tracking-widest text-white"
                >
                    Business_Ops
                </h2>
                <span
                    class="text-[9px] font-black text-white/30 uppercase tracking-widest"
                    >Active_Missions: {business.activeJobs.length}</span
                >
            </div>
        </div>
        <div class="text-right">
            <div class="text-[8px] font-black text-white/20 uppercase mb-1">
                Missions_Finalized
            </div>
            <div class="flex items-center gap-2 justify-end">
                <Trophy size={14} class="text-amber-400" />
                <span class="text-lg font-black text-white"
                    >{business.completedJobsCount}</span
                >
            </div>
        </div>
    </div>

    <!-- Job List -->
    <div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
        {#each business.activeJobs as job (job.id)}
            <div
                class="bg-white/5 border border-white/5 p-5 rounded-[2rem] hover:border-amber-400/20 transition-all flex flex-col gap-4 relative overflow-hidden group/job"
                transition:slide
            >
                <div class="flex justify-between items-start">
                    <div class="flex items-start gap-3">
                        <div
                            class="p-2 bg-black/40 rounded-xl {job.status ===
                            'RUNNING'
                                ? 'text-cyan-400 animate-pulse'
                                : 'text-white/20'}"
                        >
                            <Target size={16} />
                        </div>
                        <div>
                            <h4
                                class="text-[11px] font-black text-white uppercase group-hover/job:text-amber-400 transition-colors"
                            >
                                {job.title}
                            </h4>
                            <span class="text-[8px] font-mono text-white/20"
                                >{job.id}</span
                            >
                        </div>
                    </div>
                    <div class="flex flex-col items-end gap-1">
                        <span
                            class="text-[10px] font-black text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full"
                            >{(job.reward * business.rewardMultiplier).toFixed(
                                0,
                            )} CR</span
                        >
                        {#if business.rewardMultiplier > 1}
                            <span
                                class="text-[7px] font-black text-cyan-400 uppercase italic animate-bounce"
                                >Escalated x{business.rewardMultiplier}</span
                            >
                        {/if}
                    </div>
                </div>

                <!-- Progress -->
                <div class="space-y-2">
                    <div
                        class="flex justify-between text-[8px] font-black text-white/20 uppercase tracking-widest"
                    >
                        <span>Calibration_Status</span>
                        <span>{(job.progress * 100).toFixed(0)}%</span>
                    </div>
                    <div
                        class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden"
                    >
                        <div
                            class="h-full {job.status === 'RUNNING'
                                ? 'bg-cyan-400'
                                : 'bg-white/10'} transition-all duration-1000"
                            style:width="{job.progress * 100}%"
                        ></div>
                    </div>
                </div>

                {#if job.status === "PENDING"}
                    <button
                        class="w-full py-2 bg-white text-black text-[9px] font-black uppercase tracking-widest rounded-xl hover:bg-amber-400 transition-all flex items-center justify-center gap-2"
                        onclick={() => startJob(job.id)}
                    >
                        <Play size={10} fill="currentColor" />
                        <span>INITIALIZE_TASK</span>
                    </button>
                {:else if job.status === "RUNNING"}
                    <button
                        class="w-full py-2 bg-cyan-500 text-white text-[9px] font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-all flex items-center justify-center gap-2 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
                        onclick={() => manifold.finishJob(job.id)}
                    >
                        <Zap size={10} fill="currentColor" />
                        <span>FINALIZE_MISSION</span>
                    </button>
                {/if}
            </div>
        {/each}

        <button
            class="w-full py-4 border-2 border-dashed border-white/5 rounded-[2rem] text-[9px] font-black text-white/20 uppercase hover:border-amber-400/20 hover:text-amber-400 transition-all"
            onclick={() =>
                manifold.createJob("Regional_Node_Telemetry", 400)}
        >
            + Initiate New Mission
        </button>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-2 gap-4 mt-auto">
        <div
            class="p-4 bg-white/5 rounded-2xl border border-white/5 text-center"
        >
            <div class="text-[7px] font-black text-white/20 uppercase mb-1">
                Compute_Yield
            </div>
            <div class="text-sm font-black text-cyan-400 tracking-tighter">
                8.4 TFLOPS
            </div>
        </div>
        <div
            class="p-4 bg-white/5 rounded-2xl border border-white/5 text-center"
        >
            <div class="text-[7px] font-black text-white/20 uppercase mb-1">
                System_Trust
            </div>
            <div class="text-sm font-black text-emerald-400 tracking-tighter">
                COHERENT
            </div>
        </div>
    </div>
</div>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
