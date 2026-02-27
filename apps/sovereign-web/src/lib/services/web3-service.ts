import { browser } from '$app/environment';
import { ethers } from 'ethers';
import { SUPPORTED_CHAINS } from '$lib/types/blockchain';
import type { ChainConfig } from '$lib/types/blockchain';
import { bridgeStore } from '$lib/stores/bridge-store';
// import { get } from 'svelte/store';

// Provider types
export type WalletProvider = 'metamask' | 'walletconnect' | 'coinbase' | 'injected';

export interface WalletState {
    isConnected: boolean;
    address: string | null;
    chainId: number | null;
            // @ts-ignore
    provider: ethers.providers.Web3Provider | null;
    signer: ethers.Signer | null;
    balance: Record<string, string>;
    error: string | null;
}

class Web3Service {
    private state: WalletState = {
        isConnected: false,
        address: null,
        chainId: null,
        provider: null,
        signer: null,
        balance: {},
        error: null
    };

    private listeners: Array<(state: WalletState) => void> = [];

    constructor() {
        if (browser) {
            // Listen for account changes
            if (window.ethereum) {
                window.ethereum.on('accountsChanged', this.handleAccountsChanged.bind(this));
                window.ethereum.on('chainChanged', this.handleChainChanged.bind(this));
                window.ethereum.on('disconnect', this.handleDisconnect.bind(this));
            }
        }
    }

    // Subscribe to state changes
    subscribe(callback: (state: WalletState) => void): () => void {
        this.listeners.push(callback);
        callback(this.state);
        return () => {
            this.listeners = this.listeners.filter(cb => cb !== callback);
        };
    }

    private notifyListeners(): void {
        this.listeners.forEach(cb => cb(this.state));
    }

    private updateState(newState: Partial<WalletState>): void {
        this.state = { ...this.state, ...newState };
        this.notifyListeners();
    }

    // Handle account changes
    private async handleAccountsChanged(accounts: string[]): Promise<void> {
        if (accounts.length === 0) {
            // User disconnected
            await this.disconnect();
        } else {
            this.updateState({ address: accounts[0] });
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

        try {
            if (!window.ethereum) {
                throw new Error('MetaMask not installed');
            }

            const provider = new ethers.providers.Web3Provider(window.ethereum);
            // @ts-ignore
            await provider.send('eth_requestAccounts', []);

            const signer = provider.getSigner();
            const address = await signer.getAddress();
            const network = await provider.getNetwork();
            const chainId = network.chainId;

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
            return false;
        }
    }

    // Connect to WalletConnect
    async connectWalletConnect(): Promise<boolean> {
        // We'll implement this when we add WalletConnect dependency
        this.updateState({ error: 'WalletConnect coming soon' });
        return false;
    }

    // Connect to Coinbase Wallet
    async connectCoinbase(): Promise<boolean> {
        // We'll implement this when we add Coinbase SDK
        this.updateState({ error: 'Coinbase Wallet coming soon' });
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
        // Disconnect from bridge store
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
            const balance: Record<string, string> = {};

            // Get native balance
            const nativeBalance = await this.state.provider.getBalance(this.state.address);
            balance.native = ethers.utils.formatEther(nativeBalance);

            // Get AGE token balance (example ERC20)
            // This would need the AGE token contract address
            // const ageContract = new ethers.Contract(AGE_TOKEN_ADDRESS, ERC20_ABI, this.state.provider);
            // const ageBalance = await ageContract.balanceOf(this.state.address);
            // balance.AGE = ethers.utils.formatUnits(ageBalance, 18);

            this.updateState({ balance });
        } catch (error) {
            console.error('Failed to update balance:', error);
        }
    }

    // Switch chain
    async switchChain(chain: ChainConfig): Promise<boolean> {
        if (!this.state.provider) return false;

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

        try {
            const tx = await this.state.signer.sendTransaction({
                to,
                value: ethers.utils.parseEther(value),
                data: data || '0x'
            // @ts-ignore
            });
            return tx.hash;
        } catch (error) {
            console.error('Failed to send transaction:', error);
            return null;
        }
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
