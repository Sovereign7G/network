<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { fade, fly } from "svelte/transition";

    export let type: "SEND" | "PAY" | "FUND" | "APPROVE" = "SEND";
    export let asset: string = "AGE";
    export let balance: number = 0;
    export let recipient: string = "";
    export let amount: number = 0;
    export let description: string = "";

    const dispatch = createEventDispatcher();

    const CONFIG = {
        SEND: {
            title: "Send Assets",
            icon: "📤",
            verb: "Send",
            color: "#4CAF50",
        },
        PAY: {
            title: "Pay for Service",
            icon: "💳",
            verb: "Pay",
            color: "#2196F3",
        },
        FUND: {
            title: "Fund Proposal",
            icon: "🗳️",
            verb: "Fund",
            color: "#9C27B0",
        },
        APPROVE: {
            title: "Approve Request",
            icon: "✅",
            verb: "Approve",
            color: "#FF9800",
        },
    };

    let isProcessing = false;

    function handleAction() {
        isProcessing = true;
        setTimeout(() => {
            dispatch("confirm", { type, asset, amount, recipient });
            isProcessing = false;
        }, 1500);
    }
</script>

<div
    class="intent-modal"
    in:fly={{ y: 20, duration: 200 }}
    out:fade={{ duration: 150 }}
>
    <div class="intent-header">
        <h2>{CONFIG[type].icon} {CONFIG[type].title}</h2>
        <button class="close-btn" on:click={() => dispatch("close")}>✕</button>
    </div>

    <div class="intent-body">
        <div class="asset-preview">
            <div
                class="asset-orb"
                style="background: {CONFIG[type].color}"
            ></div>
            <div class="asset-details">
                <strong>{amount} {asset}</strong>
                <span>Balance: {balance} {asset}</span>
            </div>
        </div>

        <div class="intent-fields">
            {#if type === "SEND" || type === "PAY"}
                <div class="field">
                    <label for="recipient">Recipient</label>
                    <input
                        id="recipient"
                        type="text"
                        bind:value={recipient}
                        placeholder="Address or Alias"
                    />
                </div>
            {/if}

            <div class="field">
                <label for="amount">Amount</label>
                <input
                    id="amount"
                    type="number"
                    bind:value={amount}
                    placeholder="0.00"
                />
            </div>

            <div class="field">
                <label for="description">Context / Memo</label>
                <textarea
                    id="description"
                    bind:value={description}
                    placeholder="Optional context..."
                ></textarea>
            </div>
        </div>

        <button
            class="action-btn"
            style="background: {CONFIG[type].color}; --intent-color: {CONFIG[
                type
            ].color};"
            on:click={handleAction}
            disabled={isProcessing}
        >
            {#if isProcessing}
                <span class="spinner"></span>
            {:else}
                {CONFIG[type].verb} {asset}
            {/if}
        </button>
    </div>
</div>

<style>
    .intent-modal {
        background: #121212;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        width: 100%;
        max-width: 450px;
        overflow: hidden;
        color: white;
    }

    .intent-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.03);
    }

    .intent-body {
        padding: 2rem;
    }

    .asset-preview {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 1rem;
    }

    .asset-orb {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        filter: blur(10px);
        opacity: 0.6;
    }

    .intent-fields {
        display: grid;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .field label {
        display: block;
        font-size: 0.8rem;
        opacity: 0.6;
        margin-bottom: 0.5rem;
    }

    input,
    textarea {
        width: 100%;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        padding: 0.75rem;
        color: white;
        box-sizing: border-box;
    }

    .action-btn {
        width: 100%;
        padding: 1.25rem;
        border: none;
        border-radius: 1rem;
        color: white;
        font-weight: 700;
        cursor: pointer;
        transition:
            transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
            box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .action-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px var(--intent-color, rgba(255, 255, 255, 0.2));
    }

    .spinner {
        width: 20px;
        height: 20px;
        border: 2px solid white;
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        display: inline-block;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
