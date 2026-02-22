<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let asset;
    export let balance;
    export let price;
    export let icon = "🪙";

    const dispatch = createEventDispatcher();

    $: value = balance * price;
    $: formattedBalance = balance.toFixed(4);
    $: formattedValue = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
    }).format(value);
</script>

<div class="asset-card">
    <div class="asset-icon">
        <span class="icon">{icon}</span>
    </div>

    <div class="asset-info">
        <div class="asset-header">
            <span class="asset-name">{asset}</span>
            <span class="asset-price">${price?.toFixed(2) || "0.00"}</span>
        </div>

        <div class="asset-balance">
            <span class="balance-amount">{formattedBalance} {asset}</span>
            <span class="balance-value">{formattedValue}</span>
        </div>
    </div>

    <div class="asset-actions">
        <button
            class="action-btn send"
            on:click={() => dispatch("send")}
            aria-label="Send {asset}"
        >
            <span class="btn-glow"></span>
            📤
        </button>
        <button
            class="action-btn receive"
            on:click={() => dispatch("receive")}
            aria-label="Receive {asset}"
        >
            <span class="btn-glow"></span>
            📥
        </button>
        <button
            class="action-btn stake"
            on:click={() => dispatch("stake")}
            aria-label="Stake {asset}"
        >
            <span class="btn-glow"></span>
            💎
        </button>
        <button
            class="action-btn swap"
            on:click={() => dispatch("swap")}
            aria-label="Swap {asset}"
        >
            <span class="btn-glow"></span>
            🔄
        </button>
    </div>
</div>

<style>
    .asset-card {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    /* Inner Crystal Texture */
    .asset-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.05),
            transparent
        );
        pointer-events: none;
    }

    .asset-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.3);
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .asset-icon {
        width: 3.5rem;
        height: 3.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.05);
    }

    .icon {
        font-size: 1.75rem;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
    }

    .asset-info {
        flex: 1;
    }

    .asset-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .asset-name {
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: -0.025em;
        color: white;
    }

    .asset-price {
        font-size: 0.85rem;
        font-family: "JetBrains Mono", monospace;
        opacity: 0.6;
    }

    .asset-balance {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.95rem;
    }

    .balance-amount {
        color: #a78bfa;
        font-weight: 600;
    }

    .balance-value {
        opacity: 0.5;
        font-size: 0.85rem;
    }

    .asset-actions {
        display: flex;
        gap: 0.75rem;
    }

    .action-btn {
        width: 2.5rem;
        height: 2.5rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }

    .action-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: white;
        transform: scale(1.05);
    }

    .action-btn:active {
        transform: scale(0.95);
    }

    .btn-glow {
        position: absolute;
        inset: 0;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
    }

    /* specific glows */
    .action-btn.send:hover .btn-glow {
        background: radial-gradient(
            circle at center bottom,
            rgba(76, 175, 80, 0.4) 0%,
            transparent 60%
        );
        opacity: 1;
        animation: pulse-up 1.5s infinite;
    }

    .action-btn.receive:hover .btn-glow {
        background: radial-gradient(
            circle at center top,
            rgba(33, 150, 243, 0.4) 0%,
            transparent 60%
        );
        opacity: 1;
        animation: pulse-down 1.5s infinite;
    }

    .action-btn.stake:hover .btn-glow {
        background: radial-gradient(
            circle at center,
            rgba(156, 39, 176, 0.4) 0%,
            transparent 70%
        );
        opacity: 1;
        animation: orbit-glow 2s infinite linear;
    }

    .action-btn.swap:hover .btn-glow {
        background: linear-gradient(
            90deg,
            rgba(255, 152, 0, 0.2) 0%,
            rgba(255, 152, 0, 0.5) 50%,
            rgba(255, 152, 0, 0.2) 100%
        );
        opacity: 1;
        animation: bidirectional-flow 2s infinite linear;
    }

    @keyframes pulse-up {
        0% {
            transform: translateY(10px);
            opacity: 0.5;
        }
        50% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-10px);
            opacity: 0;
        }
    }

    @keyframes pulse-down {
        0% {
            transform: translateY(-10px);
            opacity: 0.5;
        }
        50% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(10px);
            opacity: 0;
        }
    }

    @keyframes orbit-glow {
        0% {
            transform: rotate(0deg) scale(1);
        }
        50% {
            transform: rotate(180deg) scale(1.2);
        }
        100% {
            transform: rotate(360deg) scale(1);
        }
    }

    @keyframes bidirectional-flow {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
</style>
