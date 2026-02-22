<script lang="ts">
    import { goto } from "$app/navigation";
</script>

<div class="stake-page">
    <h1 class="glow-text">Stake Assets</h1>
    <p class="subtitle">Secure the Cathedral</p>

    <div class="stake-card glass">
        <p>Staking functionality coming soon.</p>
        <button
            on:click={() => goto("/dashboard/sovereign")}
            class="stake-button">Return to Dashboard</button
        >
    </div>
</div>

<style>
    .stake-page {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        text-align: center;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #9c27b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 2rem;
    }

    .stake-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
    }
    p {
        color: white;
        margin-bottom: 2rem;
    }

    .stake-button {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #9c27b0, #7b1fa2);
        border: none;
        border-radius: 12px;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .stake-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(156, 39, 176, 0.3);
    }
</style>
