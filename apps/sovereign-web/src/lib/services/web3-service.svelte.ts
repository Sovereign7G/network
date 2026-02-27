import { browser } from '$app/environment';
import { ethers } from 'ethers';
import { SUPPORTED_CHAINS } from '$lib/types/blockchain';
import type { ChainConfig } from '$lib/types/blockchain';
import { bridgeStore } from '$lib/stores/bridge-store.svelte';
import { CircuitBreaker } from '$lib/utils/circuit-breaker';

// Provider types
type WalletProvider = 'metamask' | 'walletconnect' | 'coinbase' | 'injected';

interface WalletState {
    isConnected: boolean;
    address: string | null;
    chainId: number | null;
    provider: ethers.BrowserProvider | null;
    signer: ethers.Signer | null;
    balance: Record<string, string>;
    error: string | null;
}

class Web3Service {
    // Svelte 5 Rune for reactive state
    state = $state<WalletState>({
        isConnected: false,
        address: null,
        chainId: null,
        provider: null,
        signer: null,
        balance: {},
        error: null
    });

    private _listeners: (() => void)[] = [];
    private _breaker = new CircuitBreaker(3, 60000); // 3 failures, 1 min cooldown

    constructor() {
        if (browser) {
            this._setupListeners();
        }
    }

    /** Wire up wallet event listeners with proper cleanup tracking. */
    private _setupListeners() {
        if (!window.ethereum) return;

        const onAccounts = this.handleAccountsChanged.bind(this);
        const onChain = this.handleChainChanged.bind(this);
        const onDisconnect = this.handleDisconnect.bind(this);

        window.ethereum.on('accountsChanged', onAccounts);
        window.ethereum.on('chainChanged', onChain);
        window.ethereum.on('disconnect', onDisconnect);

        // Track for cleanup
        this._listeners.push(
            () => window.ethereum?.removeListener?.('accountsChanged', onAccounts),
            () => window.ethereum?.removeListener?.('chainChanged', onChain),
            () => window.ethereum?.removeListener?.('disconnect', onDisconnect),
        );
    }

    /** Clean up all listeners to prevent memory leaks. */
    destroy() {
        this._listeners.forEach(cleanup => cleanup());
        this._listeners = [];
    }

    private updateState(newState: Partial<WalletState>): void {
        Object.assign(this.state, newState);
    }

    // Handle account changes
    private async handleAccountsChanged(accounts: string[]): Promise<void> {
        if (accounts.length === 0) {
            // User disconnected
            await this.disconnect();
        } else {
            this.updateState({ address: accounts[0] || null });
            await this.updateBalance();
        }
    }

    // Handle chain changes
    private handleChainChanged(chainId: string): void {
        const newChainId = parseInt(chainId, 16);
        this.updateState({ chainId: newChainId });
        this.updateBalance();

        // Update bridge store with connected chain
        const chain = Object.values(SUPPORTED_CHAINS).find(c => c.id === newChainId);
        if (chain) {
            bridgeStore.connectChain(chain.shortName);
        }
    }

    // Handle disconnect
    private handleDisconnect(): void {
        this.disconnect();
    }

    // Connect to MetaMask or injected provider
    async connectMetaMask(): Promise<boolean> {
        if (!browser) return false;

        return this._breaker.execute(async () => {
            try {
                if (!window.ethereum) {
                    throw new Error('MetaMask not installed');
                }

                const provider = new ethers.BrowserProvider(window.ethereum);
                await provider.send('eth_requestAccounts', []);

                const signer = await provider.getSigner();
                const address = await signer.getAddress();
                const network = await provider.getNetwork();
                const chainId = Number(network.chainId);

                this.updateState({
                    isConnected: true,
                    address,
                    chainId,
                    provider,
                    signer,
                    error: null
                });

                await this.updateBalance();

                // Auto-connect supported chains
                const chain = Object.values(SUPPORTED_CHAINS).find(c => c.id === chainId);
                if (chain) {
                    bridgeStore.connectChain(chain.shortName);
                }

                return true;
            } catch (error) {
                this.updateState({
                    error: error instanceof Error ? error.message : 'Failed to connect'
                });
                throw error;
            }
        }).catch(() => false);
    }

    // Connect to WalletConnect (v2)
    async connectWalletConnect(): Promise<boolean> {
        // WalletConnect v2 requires a project ID from cloud.walletconnect.com
        // When ready, use: import { WalletConnectModal } from '@walletconnect/modal';
        console.warn('[Web3] WalletConnect integration pending projectId setup.');
        this.updateState({ error: 'WalletConnect requires project configuration. See cloud.walletconnect.com.' });
        return false;
    }

    // Connect to Coinbase Wallet
    async connectCoinbase(): Promise<boolean> {
        // Coinbase Wallet SDK: import CoinbaseWalletSDK from '@coinbase/wallet-sdk';
        console.warn('[Web3] Coinbase Wallet integration pending SDK setup.');
        this.updateState({ error: 'Coinbase Wallet requires SDK configuration.' });
        return false;
    }

    // Generic connect method
    async connect(provider: WalletProvider): Promise<boolean> {
        switch (provider) {
            case 'metamask':
                return this.connectMetaMask();
            case 'walletconnect':
                return this.connectWalletConnect();
            case 'coinbase':
                return this.connectCoinbase();
            default:
                return this.connectMetaMask();
        }
    }

    // Disconnect wallet
    async disconnect(): Promise<void> {
        if (this.state.chainId) {
            const chain = Object.values(SUPPORTED_CHAINS).find(c => c.id === this.state.chainId);
            if (chain) {
                bridgeStore.disconnectChain(chain.shortName);
            }
        }

        this.updateState({
            isConnected: false,
            address: null,
            chainId: null,
            provider: null,
            signer: null,
            balance: {},
            error: null
        });
    }

    // Update balances for all assets
    async updateBalance(): Promise<void> {
        if (!this.state.provider || !this.state.address) return;

        try {
            await this._breaker.execute(async () => {
                const balance: Record<string, string> = {};

                // Get native balance
                const nativeBalance = await this.state.provider!.getBalance(this.state.address!);
                balance.native = ethers.formatEther(nativeBalance);

                this.updateState({ balance });
            });
        } catch (error) {
            console.error('Failed to update balance:', error);
        }
    }

    // Switch chain
    async switchChain(chain: ChainConfig): Promise<boolean> {
        if (!browser || !window.ethereum) return false;

        try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: `0x${chain.id.toString(16)}` }]
            });
            return true;
        } catch (error: any) {
            // Chain not added to wallet
            if (error.code === 4902) {
                return this.addChain(chain);
            }
            return false;
        }
    }

    // Add new chain to wallet
    async addChain(chain: ChainConfig): Promise<boolean> {
        if (!window.ethereum) return false;

        try {
            await window.ethereum.request({
                method: 'wallet_addEthereumChain',
                params: [{
                    chainId: `0x${chain.id.toString(16)}`,
                    chainName: chain.name,
                    nativeCurrency: {
                        name: chain.currency,
                        symbol: chain.currency,
                        decimals: 18
                    },
                    rpcUrls: [chain.rpcUrl],
                    blockExplorerUrls: [chain.explorerUrl]
                }]
            });
            return true;
        } catch (error) {
            console.error('Failed to add chain:', error);
            return false;
        }
    }

    // Sign message
    async signMessage(message: string): Promise<string | null> {
        if (!this.state.signer) return null;

        try {
            const signature = await this.state.signer.signMessage(message);
            return signature;
        } catch (error) {
            console.error('Failed to sign message:', error);
            return null;
        }
    }

    // Send transaction
    async sendTransaction(to: string, value: string, data?: string): Promise<string | null> {
        if (!this.state.signer) return null;

        return this._breaker.execute(async () => {
            try {
                const tx = await this.state.signer!.sendTransaction({
                    to,
                    value: ethers.parseEther(value),
                    data: data || '0x'
                });
                return tx.hash;
            } catch (error) {
                console.error('Failed to send transaction:', error);
                throw error;
            }
        }).catch(() => null);
    }

    // Get explorer URL for transaction
    getExplorerUrl(txHash: string): string | null {
        if (!this.state.chainId) return null;

        const chain = Object.values(SUPPORTED_CHAINS).find(c => c.id === this.state.chainId);
        if (!chain) return null;

        return `${chain.explorerUrl}/tx/${txHash}`;
    }
}

// Add window.ethereum type
declare global {
    interface Window {
        ethereum?: any;
    }
}

export const web3Service = new Web3Service();
