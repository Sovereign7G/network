<script lang="ts">
//     import { onMount, onDestroy } from "svelte";
    import { web3Service } from "$lib/services/web3-service";
    import { SUPPORTED_CHAINS } from "$lib/types/blockchain";
    import type { WalletState } from "$lib/services/web3-service";

    let walletState: WalletState = {
        isConnected: false,
        address: null,
        chainId: null,
        provider: null,
        signer: null,
        balance: {},
        error: null,
    };

    let showChainSelector = false;
    let isConnecting = false;

    const unsubscribe = web3Service.subscribe((state) => {
        walletState = state;
    });

    onDestroy(unsubscribe);

    async function connect(
        provider: "metamask" | "walletconnect" | "coinbase",
    ) {
        isConnecting = true;
        await web3Service.connect(provider);
        isConnecting = false;
    }

    async function disconnect() {
        await web3Service.disconnect();
    }

    async function switchChain(chainId: string) {
        const chain = SUPPORTED_CHAINS[chainId];
        if (chain) {
            await web3Service.switchChain(chain);
            showChainSelector = false;
        }
    }

    function formatAddress(address: string): string {
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }

    function getCurrentChain() {
        if (!walletState.chainId) return null;
        return Object.values(SUPPORTED_CHAINS).find(
            (c) => c.id === walletState.chainId,
        );
    }
</script>

<div class="wallet-connector">
    {#if !walletState.isConnected}
        <div class="connect-panel">
            <h3 class="panel-title">Connect Wallet</h3>
            <p class="panel-subtitle">Connect to start cross-chain transfers</p>

            <div class="wallet-grid">
                <button
                    class="wallet-option metamask"
                    onclick={() => connect("metamask")}
                    disabled={isConnecting}
                >
                    <span class="wallet-icon">🦊</span>
                    <span class="wallet-name">MetaMask</span>
                </button>

                <button
                    class="wallet-option walletconnect"
                    onclick={() => connect("walletconnect")}
                    disabled={isConnecting}
                >
                    <span class="wallet-icon">🔗</span>
                    <span class="wallet-name">WalletConnect</span>
                    <span class="coming-soon">Soon</span>
                </button>

                <button
                    class="wallet-option coinbase"
                    onclick={() => connect("coinbase")}
                    disabled={isConnecting}
                >
                    <span class="wallet-icon">📱</span>
                    <span class="wallet-name">Coinbase</span>
                    <span class="coming-soon">Soon</span>
                </button>
            </div>

            {#if walletState.error}
                <div class="error-message">
                    ⚠️ {walletState.error}
                </div>
            {/if}
        </div>
    {:else}
        <div class="connected-panel">
            <div class="wallet-header">
                <div class="wallet-status">
                    <span class="status-dot connected"></span>
                    <span class="status-text">Connected</span>
                </div>

                <button class="disconnect-btn" onclick={disconnect}>
                    Disconnect
                </button>
            </div>

            <div class="wallet-info">
                <div class="info-row">
                    <span class="info-label">Address</span>
                    <span class="info-value address"
                        >{formatAddress(walletState.address!)}</span
                    >
                    <button
                        class="copy-btn"
                        onclick={() =>
                            navigator.clipboard.writeText(walletState.address!)}
                        title="Copy address"
                    >
                        📋
                    </button>
                </div>

                <div class="info-row">
                    <span class="info-label">Network</span>
                    <div class="network-selector">
                        <button
                            class="network-btn"
                            onclick={() =>
                                (showChainSelector = !showChainSelector)}
                            style="--chain-color: {getCurrentChain()?.color ||
                                '#9370DB'}"
                        >
                            <span class="chain-icon"
                                >{getCurrentChain()?.icon || "🌐"}</span
                            >
                            <span class="chain-name"
                                >{getCurrentChain()?.name || "Unknown"}</span
                            >
                            <span class="dropdown-arrow"
                                >{showChainSelector ? "▲" : "▼"}</span
                            >
                        </button>

                        {#if showChainSelector}
                            <div class="chain-dropdown">
                                {#each Object.entries(SUPPORTED_CHAINS) as [id, chain]}
                                    <button
                                        class="chain-option"
                                        class:active={chain.id ===
                                            walletState.chainId}
                                        onclick={() => switchChain(id)}
                                        style="--chain-color: {chain.color}"
                                    >
                                        <span class="chain-icon"
                                            >{chain.icon}</span
                                        >
                                        <span class="chain-name"
                                            >{chain.name}</span
                                        >
                                    </button>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>

                <div class="info-row">
                    <span class="info-label">Balance</span>
                    <span class="info-value balance">
                        {parseFloat(walletState.balance.native || "0").toFixed(
                            4,
                        )}
                        {getCurrentChain()?.currency || "ETH"}
                    </span>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .wallet-connector {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1.5rem;
    }

    .connect-panel {
        text-align: center;
    }

    .panel-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }

    .panel-subtitle {
        margin: 0 0 1.5rem 0;
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .wallet-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .wallet-option {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.75rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
        position: relative;
    }

    .wallet-option:hover:not(:disabled) {
        background: rgba(147, 112, 219, 0.1);
        border-color: #9370db;
        transform: translateY(-2px);
    }

    .wallet-option:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .wallet-option.metamask:hover {
        background: rgba(246, 133, 27, 0.1);
        border-color: #f6851b;
    }

    .wallet-icon {
        font-size: 2rem;
    }

    .wallet-name {
        font-size: 0.9rem;
    }

    .coming-soon {
        position: absolute;
        top: -0.5rem;
        right: -0.5rem;
        padding: 0.2rem 0.4rem;
        background: #ff6b6b;
        border-radius: 1rem;
        font-size: 0.6rem;
        color: white;
    }

    .connected-panel {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .wallet-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .wallet-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
    }

    .status-dot.connected {
        background: #4caf50;
        box-shadow: 0 0 10px #4caf50;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .disconnect-btn {
        padding: 0.5rem 1rem;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 2rem;
        color: #ff6b6b;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .disconnect-btn:hover {
        background: #ff6b6b;
        color: white;
    }

    .wallet-info {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0.75rem;
    }

    .info-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .info-label {
        width: 80px;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .info-value {
        flex: 1;
        font-size: 0.9rem;
    }

    .info-value.address {
        font-family: monospace;
    }

    .copy-btn {
        padding: 0.25rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        font-size: 1rem;
        transition: all 0.2s;
    }

    .copy-btn:hover {
        color: white;
        transform: scale(1.1);
    }

    .info-value.balance {
        color: #4ecdc4;
        font-weight: 600;
    }

    .network-selector {
        position: relative;
        flex: 1;
    }

    .network-btn {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--chain-color);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .network-btn:hover {
        background: rgba(var(--chain-color), 0.1);
    }

    .chain-icon {
        font-size: 1.1rem;
    }

    .chain-name {
        flex: 1;
        text-align: left;
        font-size: 0.9rem;
    }

    .dropdown-arrow {
        font-size: 0.7rem;
        opacity: 0.7;
    }

    .chain-dropdown {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        margin-top: 0.25rem;
        background: #1a1a1a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        padding: 0.25rem;
        z-index: 100;
        max-height: 200px;
        overflow-y: auto;
    }

    .chain-option {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        border-radius: 0.25rem;
        transition: all 0.2s;
    }

    .chain-option:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .chain-option.active {
        background: rgba(var(--chain-color), 0.2);
        border-left: 3px solid var(--chain-color);
    }

    .error-message {
        padding: 0.75rem;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 0.5rem;
        color: #ff6b6b;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
</style>
