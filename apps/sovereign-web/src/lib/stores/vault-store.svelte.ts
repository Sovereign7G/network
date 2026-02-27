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

class VaultEngine {
    state = $state<VaultState>(initialState);

    constructor() {
        if (browser) {
            const stored = loadFromStorage<VaultState>('vault', initialState);
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
            this.state = stored;
        }
    }

    private persist() {
        if (browser) saveToStorage('vault', $state.snapshot(this.state));
    }

    private generateUUID() {
        return browser && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString();
    }

    get totalValue() {
        return this.state.totalValue;
    }

    async loadVaultData() {
        try {
            const { api } = await import('$lib/services/api');
            const data = await api.request('/vault');
            if (data) Object.assign(this.state, data);
            this.persist();
        } catch { }
    }

    addTransaction(tx: Omit<Transaction, 'id' | 'timestamp' | 'status'>) {
        const newTx: Transaction = {
            ...tx,
            id: this.generateUUID(),
            timestamp: new Date(),
            status: 'pending'
        };

        if (tx.type === 'receive') {
            this.state.balances[tx.asset] = (this.state.balances[tx.asset] || 0) + tx.amount;
        } else if (tx.type === 'send') {
            this.state.balances[tx.asset] = (this.state.balances[tx.asset] || 0) - tx.amount;
        }

        this.state.transactions = [newTx, ...this.state.transactions];
        this.recalculateTotalValue();
        this.persist();
    }

    updateBalance(asset: string, amount: number) {
        this.state.balances[asset] = amount;
        this.recalculateTotalValue();
        this.persist();
    }

    updatePrice(asset: string, price: number) {
        this.state.assetPrices[asset] = price;
        this.recalculateTotalValue();
        this.persist();
    }

    recalculateTotalValue() {
        this.state.totalValue = Object.entries(this.state.balances).reduce(
            (sum, [asset, amount]) => sum + amount * (this.state.assetPrices[asset] || 0),
            0
        );
    }
}

export const vaultStore = new VaultEngine();
