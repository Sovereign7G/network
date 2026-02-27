<script lang="ts">
    import { learningEngine } from "$lib/engines/learning-engine.svelte";
    import { fade } from "svelte/transition";
    import {
        BrainCircuit,
        ShieldCheck,
        Download,
        RefreshCw,
        Clock,
    } from "lucide-svelte";

    const profile = $derived(learningEngine.profile);

    // Derived stats for visualization
    const engagementScore = $derived.by(() => {
        const scores = Object.values(profile.preferences.typeScores);
        if (scores.length === 0) return 0;
        return (scores.reduce((a, b) => a + b, 0) / scores.length) * 100;
    });

    const activeHoursSorted = $derived.by(() => {
        return Object.entries(profile.preferences.activeHours)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3);
    });

    function resetLearning() {
        if (
            confirm(
                "Are you sure? This will wipe your local learning profile. This action cannot be undone.",
            )
        ) {
            learningEngine.reset();
        }
    }

    function exportProfile() {
        const data = JSON.stringify(profile, null, 2);
        const blob = new Blob([data], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `sovereign-learning-profile-${Date.now()}.json`;
        a.click();
    }
</script>

<div class="learning-insights">
    <!-- Journey Header -->
    <div class="insight-section mb-8" in:fade>
        <div class="flex items-center gap-3 mb-4">
            <div class="section-icon">
                <ShieldCheck size={18} />
            </div>
            <h3
                class="text-[12px] font-black uppercase tracking-widest text-white/80"
            >
                Sovereign Journey
            </h3>
        </div>

        <div class="grid grid-cols-2 gap-3">
            <div class="stat-card">
                <span class="label">Transactions</span>
                <span class="value">{profile.journey.transactionCount}</span>
            </div>
            <div class="stat-card">
                <span class="label">Votes Cast</span>
                <span class="value">{profile.journey.voteCount}</span>
            </div>
            <div class="stat-card">
                <span class="label">ZK Proofs</span>
                <span class="value">{profile.journey.zkCount}</span>
            </div>
            <div class="stat-card">
                <span class="label">Milestones</span>
                <span class="value">{profile.journey.milestones.length}</span>
            </div>
        </div>
    </div>

    <!-- Engagement & Preferences -->
    <div class="insight-section mb-8" in:fade={{ delay: 100 }}>
        <div class="flex items-center gap-3 mb-4">
            <div class="section-icon">
                <BrainCircuit size={18} />
            </div>
            <h3
                class="text-[12px] font-black uppercase tracking-widest text-white/80"
            >
                learned Preferences
            </h3>
        </div>

        <div class="p-4 bg-white/[0.03] border border-white/5 rounded-2xl mb-4">
            <div class="flex justify-between items-end mb-2">
                <span
                    class="text-[9px] font-black uppercase tracking-widest text-white/40"
                    >Engagement Resonance</span
                >
                <span class="text-xs font-black text-amber-400"
                    >{Math.round(engagementScore)}%</span
                >
            </div>
            <div class="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div
                    class="h-full bg-amber-400"
                    style="width: {engagementScore}%"
                ></div>
            </div>
        </div>

        <div class="space-y-3">
            {#each Object.entries(profile.preferences.typeScores) as [type, score]}
                <div class="preference-row">
                    <span
                        class="text-[9px] uppercase tracking-widest text-white/60"
                        >{type.replace("-", " ")}</span
                    >
                    <div
                        class="flex-1 h-[2px] bg-white/5 rounded-full mx-4 overflow-hidden"
                    >
                        <div
                            class="h-full bg-white/40"
                            style="width: {score * 100}%"
                        ></div>
                    </div>
                    <span class="text-[9px] font-black text-white/40"
                        >{Math.round(score * 100)}%</span
                    >
                </div>
            {/each}
            {#if Object.keys(profile.preferences.typeScores).length === 0}
                <p class="text-[10px] text-white/20 italic text-center py-4">
                    Observing your interaction patterns...
                </p>
            {/if}
        </div>
    </div>

    <!-- Temporal Patterns -->
    <div class="insight-section mb-8" in:fade={{ delay: 200 }}>
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
                <div class="section-icon">
                    <Clock size={18} />
                </div>
                <h3
                    class="text-[12px] font-black uppercase tracking-widest text-white/80"
                >
                    Temporal Fluidity
                </h3>
            </div>

            {#if activeHoursSorted.length > 0}
                <div
                    class="px-2 py-1 bg-amber-400/10 border border-amber-400/20 rounded text-[8px] font-black text-amber-400 uppercase tracking-widest"
                >
                    Peak: {activeHoursSorted[0][0]}:00
                </div>
            {/if}
        </div>

        <div class="hour-grid grid grid-cols-6 gap-2 mb-4">
            {#each Array(24) as _, h}
                {@const weight = profile.preferences.activeHours[h] ?? 0}
                <div
                    class="h-6 rounded-md border border-white/5 flex items-center justify-center text-[7px] transition-all"
                    style="background: rgba(147, 112, 219, {weight *
                        0.4}); border-color: rgba(147, 112, 219, {weight})"
                    title="{h}:00 - Activity: {Math.round(weight * 100)}%"
                >
                    {h}
                </div>
            {/each}
        </div>
    </div>

    <!-- Control Panel -->
    <div class="flex flex-col gap-2 mt-auto">
        <div class="flex gap-2">
            <button class="control-btn flex-1" onclick={exportProfile}>
                <Download size={14} />
                <span>Export Profile</span>
            </button>
            <button class="control-btn flex-1 danger" onclick={resetLearning}>
                <RefreshCw size={14} />
                <span>Reset Engine</span>
            </button>
        </div>
        <p
            class="text-[8px] text-white/20 text-center uppercase tracking-[0.2em] mt-4"
        >
            🔒 All learning stays on this device
        </p>
    </div>
</div>

<style>
    .learning-insights {
        padding: 1rem;
        display: flex;
        flex-direction: column;
        height: 100%;
        overflow-y: auto;
    }

    .section-icon {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.6);
    }

    .stat-card {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .stat-card .label {
        font-size: 8px;
        font-weight: black;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.3);
    }

    .stat-card .value {
        font-size: 14px;
        font-weight: black;
        color: white;
    }

    .preference-row {
        display: flex;
        align-items: center;
    }

    .control-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-size: 10px;
        font-weight: black;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.2s;
    }

    .control-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .control-btn.danger {
        color: #ef4444;
        border-color: rgba(239, 68, 68, 0.2);
    }

    .control-btn.danger:hover {
        background: rgba(239, 68, 68, 0.1);
    }

    /* Custom scrollbar */
    .learning-insights::-webkit-scrollbar {
        width: 4px;
    }
    .learning-insights::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
