import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import type {
    VaultState,
    Transaction,
    AssetPrice,
    PriceHistoryEntry
} from '$lib/types';

const initialState: VaultState = {
    balances: {
        AGE: 1247.32,
        RES: 892.5,
        USDC: 5000.0,
        BTC: 0.012,
        ETH: 0.15
    },
    transactions: [
        {
            id: '1',
            type: 'receive',
            amount: 100,
            asset: 'AGE',
            from: '0x1234...5678',
            to: '0xabcd...efgh',
            timestamp: new Date(Date.now() - 3600000),
            status: 'confirmed',
            hash: '0x' + Math.random().toString(36).substring(2, 15)
        },
        {
            id: '2',
            type: 'send',
            amount: 50,
            asset: 'RES',
            from: '0xabcd...efgh',
            to: '0x8765...4321',
            timestamp: new Date(Date.now() - 86400000),
            status: 'confirmed',
            hash: '0x' + Math.random().toString(36).substring(2, 15)
        },
        {
            id: '3',
            type: 'stake',
            amount: 500,
            asset: 'AGE',
            from: '0xabcd...efgh',
            to: 'staking_pool',
            timestamp: new Date(Date.now() - 172800000),
            status: 'confirmed',
            hash: '0x' + Math.random().toString(36).substring(2, 15)
        }
    ],
    totalValue: 7247.32,
    totalValueChange: '+12.3%',
    allocation: {
        liquid: 60,
        staked: 25,
        vested: 15
    },
    assetPrices: {
        AGE: 1.25,
        RES: 0.75,
        USDC: 1.00,
        BTC: 45000,
        ETH: 3200
    },
    priceHistory: {
        AGE: Array.from({ length: 30 }, (_, i) => ({
            date: new Date(Date.now() - (29 - i) * 86400000),
            price: 1.0 + Math.sin(i / 5) * 0.2 + Math.random() * 0.1
        })),
        RES: Array.from({ length: 30 }, (_, i) => ({
            date: new Date(Date.now() - (29 - i) * 86400000),
            price: 0.6 + Math.cos(i / 4) * 0.15 + Math.random() * 0.1
        }))
    }
};

function createVaultStore() {
    const stored = loadFromStorage<VaultState>('vault', initialState);

    // Restore dates
    if (stored.transactions) {
        stored.transactions = stored.transactions.map(tx => ({
            ...tx,
            timestamp: new Date(tx.timestamp)
        }));
    }

    if (stored.priceHistory) {
        Object.keys(stored.priceHistory).forEach(key => {
            const history = stored.priceHistory[key];
            if (history) {
                stored.priceHistory[key] = history.map(p => ({
                    ...p,
                    date: new Date(p.date)
                }));
            }
        });
    }

    const { subscribe, set, update } = writable<VaultState>(stored);

    return {
        subscribe,

        addTransaction: (tx: Omit<Transaction, 'id' | 'timestamp' | 'status'>) =>
            update((state: VaultState) => {
                const newTx: Transaction = {
                    ...tx,
                    id: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(),
                    timestamp: new Date(),
                    status: 'pending'
                };

                // Update balance based on transaction
                const newBalances = { ...state.balances };
                if (tx.type === 'receive') {
                    newBalances[tx.asset] = (newBalances[tx.asset] || 0) + tx.amount;
                } else if (tx.type === 'send') {
                    newBalances[tx.asset] = (newBalances[tx.asset] || 0) - tx.amount;
                }

                // Recalculate total value
                const newTotalValue = Object.entries(newBalances).reduce(
                    (sum, [asset, amount]) => sum + amount * (state.assetPrices[asset] || 0),
                    0
                );

                const newState: VaultState = {
                    ...state,
                    balances: newBalances,
                    transactions: [newTx, ...state.transactions],
                    totalValue: newTotalValue
                };

                saveToStorage('vault', newState);
                return newState;
            }),

        updateBalance: (asset: string, amount: number) =>
            update((state: VaultState) => {
                const newState: VaultState = {
                    ...state,
                    balances: { ...state.balances, [asset]: amount }
                };
                saveToStorage('vault', newState);
                return newState;
            }),

        updatePrice: (asset: string, price: number) =>
            update((state: VaultState) => {
                const newState: VaultState = {
                    ...state,
                    assetPrices: { ...state.assetPrices, [asset]: price }
                };
                saveToStorage('vault', newState);
                return newState;
            }),

        confirmTransaction: (id: string) =>
            update((state: VaultState) => {
                const newState: VaultState = {
                    ...state,
                    transactions: state.transactions.map(tx =>
                        tx.id === id ? { ...tx, status: 'confirmed' } : tx
                    )
                };
                saveToStorage('vault', newState);
                return newState;
            }),

        // 🏛️ SOVEREIGN BRIDGE: Load data from backend
        loadVaultData: async () => {
            try {
                const { api } = await import('$lib/services/api');
                const balances = await api.get('/vault/balance');
                const transactions = await api.get('/vault/transactions');

                update((state: VaultState) => {
                    const newState = {
                        ...state,
                        balances: { ...state.balances, ...balances },
                        transactions: transactions.length > 0 ? transactions : state.transactions
                    };
                    saveToStorage('vault', newState);
                    return newState;
                });
            } catch (error) {
                console.error('[VaultStore] Failed to load data from backend:', error);
            }
        }
    };
}

export const vaultStore = createVaultStore();
