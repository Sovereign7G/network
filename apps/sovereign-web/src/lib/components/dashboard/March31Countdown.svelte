<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    // ⚫ PILLAR VI: MARCH 31 HARD RESET (v1.0)
    let daysLeft = 0;

    function calculateDays() {
        const resetDate = new Date("2026-03-31T00:00:00Z");
        const now = new Date();
        const diff = resetDate.getTime() - now.getTime();
        daysLeft = Math.ceil(diff / (1000 * 60 * 60 * 24));
    }

    onMount(() => {
        calculateDays();
        const timer = setInterval(calculateDays, 3600000); // Check every hour
        return () => clearInterval(timer);
    });

    const vectors = [
        { name: "Banks", impact: "13% write-downs" },
        { name: "Hedge Funds", impact: "$10.8M gap/500M" },
        { name: "Basis Trade", impact: "Liquidation speedup" },
        { name: "Intelligence", impact: "Active Readiness 100%" },
    ];
</script>

<div class="hard-reset-card" in:fly={{ y: 20 }}>
    <div class="header">
        <h3>⏳ MARCH 31 HARD RESET</h3>
        <span class="countdown">{daysLeft} DAYS</span>
    </div>

    <div class="timeline-visual">
        <div class="bar">
            <div
                class="fill"
                style="width: {Math.max(0, 100 - (daysLeft / 40) * 100)}%"
            ></div>
        </div>
        <div class="labels">
            <span>Feb 20 (Tariff)</span>
            <span>Mar 31 (Reset)</span>
        </div>
    </div>

    <div class="vector-list">
        {#each vectors as vector}
            <div class="vector-item">
                <span class="name">{vector.name}</span>
                <span class="impact">{vector.impact}</span>
            </div>
        {/each}
    </div>

    <div class="danger-zone">System Convergence Imminent</div>
</div>

<style>
    .hard-reset-card {
        background: linear-gradient(
            180deg,
            rgba(255, 62, 62, 0.05) 0%,
            rgba(13, 13, 15, 0.9) 100%
        );
        border: 1px solid rgba(255, 62, 62, 0.2);
        border-radius: 1.5rem;
        padding: 1.5rem;
        font-family: "Inter", sans-serif;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .header h3 {
        margin: 0;
        font-size: 1rem;
        color: #ff3e3e;
    }
    .countdown {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ff3e3e;
    }

    .timeline-visual {
        margin-bottom: 1.5rem;
    }
    .bar {
        height: 6px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }
    .fill {
        height: 100%;
        background: #ff3e3e;
        box-shadow: 0 0 10px #ff3e3e;
    }
    .labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.3);
    }

    .vector-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .vector-item {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0.5rem;
    }
    .impact {
        color: #ff3e3e;
        font-weight: 600;
    }

    .danger-zone {
        text-align: center;
        padding: 0.75rem;
        background: rgba(255, 62, 62, 0.1);
        border-radius: 0.75rem;
        font-size: 0.8rem;
        font-weight: 700;
        color: #ff3e3e;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.6;
        }
    }
</style>
