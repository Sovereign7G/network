import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { SUPPORTED_CHAINS } from '$lib/types/blockchain';
import type { BridgeTransaction, BridgeQuote, CrossChainBalance } from '$lib/types/blockchain';

interface BridgeState {
    connectedChains: string[];
    balances: CrossChainBalance[];
    transactions: BridgeTransaction[];
    pendingQuotes: BridgeQuote[];
    isConnecting: boolean;
    error: string | null;
}

const initialState: BridgeState = {
    connectedChains: [],
    balances: [],
    transactions: [],
    pendingQuotes: [],
    isConnecting: false,
    error: null
};

function createBridgeStore() {
    const stored = loadFromStorage<BridgeState>('bridge', initialState);
    const { subscribe, set, update } = writable<BridgeState>(stored);

    return {
        subscribe,

        connectChain: async (chainId: string) => {
            update(state => ({ ...state, isConnecting: true, error: null }));

            try {
                // Simulate connection - replace with actual Web3 connection
                await new Promise(resolve => setTimeout(resolve, 1000));

                update(state => ({
                    ...state,
                    connectedChains: [...state.connectedChains, chainId],
                    isConnecting: false
                }));
            } catch (error) {
                update(state => ({
                    ...state,
                    isConnecting: false,
                    error: error instanceof Error ? error.message : 'Failed to connect'
                }));
            }
        },

        disconnectChain: (chainId: string) => {
            update(state => ({
                ...state,
                connectedChains: state.connectedChains.filter(c => c !== chainId),
                balances: state.balances.filter(b => b.chain !== chainId)
            }));
            saveToStorage('bridge', get({ subscribe }));
        },

        getQuote: async (fromChain: string, toChain: string, asset: string, amount: number): Promise<BridgeQuote | null> => {
            // Simulate quote - replace with actual bridge API call
            const quote: BridgeQuote = {
                fromChain,
                toChain,
                asset,
                amount,
                fee: amount * 0.001, // 0.1% fee
                estimatedTime: 15, // 15 minutes
                guaranteedPrice: amount * 0.999
            };

            update(state => ({
                ...state,
                pendingQuotes: [quote, ...state.pendingQuotes].slice(0, 10)
            }));

            return quote;
        },

        executeBridge: async (quote: BridgeQuote, fromAddress: string, toAddress: string) => {
            update(state => ({ ...state, isConnecting: true }));

            try {
                // Simulate bridge execution
                await new Promise(resolve => setTimeout(resolve, 3000));

                const transaction: BridgeTransaction = {
                    id: crypto.randomUUID(),
                    fromChain: quote.fromChain,
                    toChain: quote.toChain,
                    fromAddress,
                    toAddress,
                    asset: quote.asset,
                    amount: quote.amount,
                    status: 'pending',
                    timestamp: new Date()
                };

                update(state => ({
                    ...state,
                    transactions: [transaction, ...state.transactions],
                    pendingQuotes: state.pendingQuotes.filter(q =>
                        !(q.fromChain === quote.fromChain &&
                            q.toChain === quote.toChain &&
                            q.asset === quote.asset &&
                            q.amount === quote.amount)
                    ),
                    isConnecting: false
                }));

                // Simulate completion after 2 minutes
                setTimeout(() => {
                    update(state => ({
                        ...state,
                        transactions: state.transactions.map(tx =>
                            tx.id === transaction.id
                                ? { ...tx, status: 'completed', completedAt: new Date() }
                                : tx
                        )
                    }));
                }, 120000);

                saveToStorage('bridge', get({ subscribe }));
                return transaction;
            } catch (error) {
                update(state => ({
                    ...state,
                    isConnecting: false,
                    error: error instanceof Error ? error.message : 'Bridge failed'
                }));
                return null;
            }
        },

        updateBalances: (balances: CrossChainBalance[]) => {
            update(state => ({ ...state, balances }));
            saveToStorage('bridge', get({ subscribe }));
        }
    };
}

export const bridgeStore = createBridgeStore();
