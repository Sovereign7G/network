// Chain configurations
export interface ChainConfig {
    id: number;
    name: string;
    shortName: string;
    currency: string;
    rpcUrl: string;
    explorerUrl: string;
    icon: string;
    color: string;
    bridgeAddress?: string;
}

export const SUPPORTED_CHAINS: Record<string, ChainConfig> = {
    ETHEREUM: {
        id: 1,
        name: 'Ethereum',
        shortName: 'ETH',
        currency: 'ETH',
        rpcUrl: 'https://mainnet.infura.io/v3/',
        explorerUrl: 'https://etherscan.io',
        icon: 'Ξ',
        color: '#627EEA',
        bridgeAddress: '0x...' // Will be populated
    },
    POLYGON: {
        id: 137,
        name: 'Polygon',
        shortName: 'MATIC',
        currency: 'MATIC',
        rpcUrl: 'https://polygon-rpc.com',
        explorerUrl: 'https://polygonscan.com',
        icon: '⬡',
        color: '#8247E5',
        bridgeAddress: '0x...'
    },
    ARBITRUM: {
        id: 42161,
        name: 'Arbitrum',
        shortName: 'ARB',
        currency: 'ETH',
        rpcUrl: 'https://arb1.arbitrum.io/rpc',
        explorerUrl: 'https://arbiscan.io',
        icon: '🔷',
        color: '#28A0F0',
        bridgeAddress: '0x...'
    },
    OPTIMISM: {
        id: 10,
        name: 'Optimism',
        shortName: 'OP',
        currency: 'ETH',
        rpcUrl: 'https://mainnet.optimism.io',
        explorerUrl: 'https://optimistic.etherscan.io',
        icon: '✨',
        color: '#FF0420',
        bridgeAddress: '0x...'
    }
};

export interface BridgeTransaction {
    id: string;
    fromChain: string;
    toChain: string;
    fromAddress: string;
    toAddress: string;
    asset: string;
    amount: number;
    status: 'pending' | 'completed' | 'failed';
    txHash?: string;
    timestamp: Date;
    completedAt?: Date;
}

export interface BridgeQuote {
    fromChain: string;
    toChain: string;
    asset: string;
    amount: number;
    fee: number;
    estimatedTime: number; // in minutes
    guaranteedPrice?: number;
}

export interface CrossChainBalance {
    chain: string;
    asset: string;
    balance: number;
    usdValue: number;
    lastUpdated: Date;
}
