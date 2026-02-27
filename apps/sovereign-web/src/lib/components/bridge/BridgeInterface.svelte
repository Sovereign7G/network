<script lang="ts">
    import WalletConnector from "./WalletConnector.svelte";
    import { bridgeStore } from "$lib/stores/bridge-store.svelte";
    import { SUPPORTED_CHAINS } from "$lib/types/blockchain";
    import type { BridgeQuote } from "$lib/types/blockchain";

    let fromChain = "ETHEREUM";
    let toChain = "POLYGON";
    let asset = "AGE";
    let amount = 0;
    let quote: BridgeQuote | null = null;
    let isGettingQuote = false;

    const chains = Object.entries(SUPPORTED_CHAINS).map(
        ([chainId, config]) => ({
            id: chainId,
            ...config,
        }),
    );

    async function getQuote() {
        if (amount <= 0) return;

        isGettingQuote = true;
        quote = await bridgeStore.getQuote(fromChain, toChain, asset, amount);
        isGettingQuote = false;
    }

    async function executeBridge() {
        if (!quote) return;

        // Get from address from connected wallet
        const fromAddress = "0x..."; // Replace with actual wallet address
        const toAddress = fromAddress; // Same address on destination chain

        await bridgeStore.executeBridge(quote, fromAddress, toAddress);
        quote = null;
        amount = 0;
    }

    $: fromConfig = SUPPORTED_CHAINS[fromChain];
    $: toConfig = SUPPORTED_CHAINS[toChain];
</script>

<div class="bridge-interface">
    <WalletConnector />
    <h2 class="bridge-title">
        <span class="title-icon">🌉</span>
        Astro Bridge
    </h2>

    <div class="bridge-form">
        <div class="chain-selectors">
            <div class="chain-select">
<!-- svelte-ignore a11y_label_has_associated_control -->
                <label>From</label>
                <select bind:value={fromChain}>
                    {#each chains as chain}
                        <option value={chain.id}>
                            {chain.icon}
                            {chain.name}
                        </option>
                    {/each}
                </select>
                {#if fromConfig}
                    <div
                        class="chain-info"
                        style="--chain-color: {fromConfig.color}"
                    >
                        <span>Balance: 0 {fromConfig.currency}</span>
                    </div>
                {/if}
            </div>

            <div class="swap-arrow">→</div>

            <div class="chain-select">
<!-- svelte-ignore a11y_label_has_associated_control -->
                <label>To</label>
                <select bind:value={toChain}>
                    {#each chains as chain}
                        <option value={chain.id}>
                            {chain.icon}
                            {chain.name}
                        </option>
                    {/each}
                </select>
                {#if toConfig}
                    <div
                        class="chain-info"
                        style="--chain-color: {toConfig.color}"
                    >
                        <span>Destination: {toConfig.name}</span>
                    </div>
                {/if}
            </div>
        </div>

        <div class="amount-input">
<!-- svelte-ignore a11y_label_has_associated_control -->
            <label>Amount</label>
            <div class="input-wrapper">
                <input
                    type="number"
                    bind:value={amount}
                    min="0"
                    step="0.01"
                    placeholder="0.00"
                />
                <select bind:value={asset}>
                    <option value="AGE">AGE</option>
                    <option value="RES">RES</option>
                    <option value="USDC">USDC</option>
                </select>
            </div>
        </div>

        <button
            class="quote-btn"
            onclick={getQuote}
            disabled={amount <= 0 || isGettingQuote}
        >
            {#if isGettingQuote}
                <span class="spinner"></span>
                Getting Quote...
            {:else}
                Get Bridge Quote
            {/if}
        </button>

        {#if quote}
            <div class="quote-display">
                <h3>Bridge Quote</h3>
                <div class="quote-details">
                    <div class="quote-row">
                        <span>Amount:</span>
                        <span>{quote.amount} {quote.asset}</span>
                    </div>
                    <div class="quote-row">
                        <span>Fee:</span>
                        <span>{quote.fee.toFixed(4)} {quote.asset}</span>
                    </div>
                    <div class="quote-row">
                        <span>You'll receive:</span>
                        <span
                            >{(quote.amount - quote.fee).toFixed(4)}
                            {quote.asset}</span
                        >
                    </div>
                    <div class="quote-row">
                        <span>Estimated time:</span>
                        <span>{quote.estimatedTime} minutes</span>
                    </div>
                </div>

                <button class="execute-btn" onclick={executeBridge}>
                    Execute Bridge Transfer
                </button>
            </div>
        {/if}

        {#if bridgeStore.state.error}
            <div class="error-message">
                ⚠️ {bridgeStore.state.error}
            </div>
        {/if}
    </div>
</div>

<style>
    .bridge-interface {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        padding: 2rem;
    }

    .bridge-interface :global(.wallet-connector) {
        margin-bottom: 2rem;
    }

    .bridge-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 0 2rem 0;
        font-size: 1.8rem;
    }

    .title-icon {
        font-size: 2rem;
    }

    .bridge-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .chain-selectors {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .chain-select {
        flex: 1;
        min-width: 200px;
    }

    .chain-select label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .chain-select select {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-size: 1rem;
        cursor: pointer;
    }

    .chain-info {
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: rgba(var(--chain-color), 0.1);
        border-left: 3px solid var(--chain-color);
        border-radius: 0.25rem;
        font-size: 0.8rem;
    }

    .swap-arrow {
        font-size: 2rem;
        opacity: 0.5;
        padding: 0 0.5rem;
    }

    .amount-input label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .input-wrapper {
        display: flex;
        gap: 0.5rem;
    }

    .input-wrapper input {
        flex: 1;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-size: 1rem;
    }

    .input-wrapper select {
        width: 100px;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
    }

    .quote-btn,
    .execute-btn {
        padding: 1rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 0.5rem;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .quote-btn:hover:not(:disabled),
    .execute-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .quote-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .quote-display {
        margin-top: 1rem;
        padding: 1.5rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid #9370db;
        border-radius: 1rem;
    }

    .quote-display h3 {
        margin: 0 0 1rem 0;
        color: #9370db;
    }

    .quote-details {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .quote-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .error-message {
        padding: 1rem;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 0.5rem;
        color: #ff6b6b;
    }

    .spinner {
        display: inline-block;
        width: 1rem;
        height: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-right: 0.5rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
