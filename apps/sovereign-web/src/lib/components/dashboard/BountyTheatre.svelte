<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
//     import { bountyTheatre } from "../../../../../../packages/age-commerce/src/store/bounty-store";

    let events: any[] = [];

    const unsubscribe = bountyTheatre.subscribe((state) => {
        events = state;
    });

    onMount(() => {
        return () => unsubscribe();
    });

    // Sample static agents for visual presence
    const agents = [
        { id: "AI-CORE-1", name: "Sovereign Arbiter", totalBounties: 47 },
        { id: "AI-LOG-4", name: "Logistics Prime", totalBounties: 128 },
        { id: "AI-SEC-9", name: "Watcher Prime", totalBounties: 847 },
    ];
</script>

<div class="bounty-theatre">
    <div class="theatre-header">
        <div class="header-left">
            <h3>🤖 BOUNTY THEATRE</h3>
            <span class="subtitle">MACHINE ECONOMY TRANSPARENCY</span>
        </div>
        <div class="economy-stats">
            <div class="stat">
                <span class="stat-label">ACTIVE AGENTS</span>
                <span class="stat-value">{agents.length}</span>
            </div>
            <div class="stat">
                <span class="stat-label">24H VOLUME</span>
                <span class="stat-value">1.4M AGE</span>
            </div>
        </div>
    </div>

    <div class="bounty-list">
        {#each events as event (event.timestamp)}
            <div class="bounty-card" in:fly={{ y: 20, duration: 500 }} out:fade>
                <div class="agent-info">
                    <div class="agent-avatar">
                        <span class="status-dot active"></span>
                        <div class="avatar-circles">
                            <div class="circle c1"></div>
                            <div class="circle c2"></div>
                        </div>
                    </div>
                    <div class="agent-meta">
                        <span class="agent-id">EVENT: {event.type}</span>
                        <span class="agent-name"
                            >{new Date(
                                event.timestamp,
                            ).toLocaleTimeString()}</span
                        >
                    </div>
                    <div class="bounty-status">LIVE</div>
                </div>

                <div class="task-info">
                    <p class="task-description">
                        {event.reason ||
                            event.service ||
                            (event.type === "LIFEBOAT_REBALANCE"
                                ? "Strategic Portfolio Rebalance"
                                : "Machine Activity")}
                    </p>
                    {#if event.amount}
                        <div class="reward-tag">
                            <span class="reward-amount">{event.amount}</span>
                            <span class="reward-asset">USDC</span>
                        </div>
                    {/if}
                </div>

                {#if event.type === "LIFEBOAT_REBALANCE"}
                    <div class="progress-section">
                        <div class="progress-header">
                            <span>SYSTEMIC PROTECTION</span>
                            <span>ACTIVE</span>
                        </div>
                        <div class="progress-bar">
                            <div
                                class="progress-fill"
                                style="width: 100%; background: #f44336;"
                            ></div>
                        </div>
                    </div>
                {/if}
            </div>
        {:else}
            <div class="empty-state">
                <p>📡 WAITING FOR MACHINE ACTIVITY...</p>
            </div>
        {/each}
    </div>
</div>

<style>
    .bounty-theatre {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        color: white;
    }

    .theatre-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
    }

    .theatre-header h3 {
        margin: 0;
        font-size: 1.1rem;
        letter-spacing: 2px;
        color: #4ecdc4;
    }

    .subtitle {
        font-size: 0.7rem;
        color: #666;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .economy-stats {
        display: flex;
        gap: 2rem;
    }

    .stat {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .stat-label {
        font-size: 0.6rem;
        color: #666;
    }

    .stat-value {
        font-weight: bold;
        font-size: 1rem;
        color: #4ecdc4;
    }

    .bounty-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .bounty-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.75rem;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s;
    }

    .bounty-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .agent-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .agent-avatar {
        position: relative;
        width: 40px;
        height: 40px;
    }

    .status-dot {
        position: absolute;
        top: 0;
        right: 0;
        width: 8px;
        height: 8px;
        background: #444;
        border-radius: 50%;
        z-index: 2;
    }

    .status-dot.active {
        background: #4ecdc4;
        box-shadow: 0 0 10px #4ecdc4;
    }

    .avatar-circles {
        position: relative;
        width: 100%;
        height: 100%;
        background: #111;
        border-radius: 50%;
        overflow: hidden;
    }

    .circle {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }

    .c1 {
        width: 80%;
        height: 80%;
    }
    .c2 {
        width: 50%;
        height: 50%;
        background: rgba(78, 205, 196, 0.1);
    }

    .agent-meta {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .agent-id {
        font-size: 0.6rem;
        font-family: monospace;
        color: #666;
    }

    .agent-name {
        font-weight: bold;
        font-size: 0.9rem;
    }

    .bounty-status {
        font-size: 0.6rem;
        padding: 0.2rem 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        color: #666;
    }

    .task-info {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .task-description {
        margin: 0;
        font-size: 0.85rem;
        color: #aaa;
        max-width: 70%;
    }

    .reward-tag {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .reward-amount {
        font-weight: bold;
        color: #fff;
    }

    .reward-asset {
        font-size: 0.6rem;
        color: #666;
    }

    .progress-section {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.65rem;
        color: #666;
        letter-spacing: 1px;
    }

    .progress-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4ecdc4, #9370db);
        transition: width 1s ease-in-out;
    }

    .empty-state {
        padding: 3rem;
        text-align: center;
        color: #444;
        border: 1px dashed rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        font-style: italic;
    }
</style>
