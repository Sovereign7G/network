import { browser } from '$app/environment';

export const TILES = [
    {
        id: 'wallet',
        title: 'Wallet',
        icon: '💰',
        route: '/dashboard/wallet',
        color: '#4ECDC4',
        description: 'Your digital assets',
        module: 'vault',
        priority: 1
    },
    {
        id: 'ledger',
        title: 'Ledger',
        icon: '📒',
        route: '/dashboard/ledger',
        color: '#FFD700',
        description: 'Transaction history',
        module: 'vault',
        priority: 2
    },
    {
        id: 'hearth',
        title: 'Hearth',
        icon: '🔥',
        route: '/dashboard/hearth',
        color: '#FF6B6B',
        description: 'Memory log',
        module: 'hearth',
        priority: 1,
        badge: 'New'
    },
    {
        id: 'metrics',
        title: 'Metrics',
        icon: '📊',
        route: '/dashboard/metrics',
        color: '#9370DB',
        description: 'Your resonance score',
        module: 'metrics',
        priority: 2
    },
    {
        id: 'command',
        title: 'Command',
        icon: '⌨️',
        route: '/dashboard/command',
        color: '#45B7D1',
        description: 'Terminal interface',
        module: 'command',
        priority: 3
    },
    {
        id: 'concierge',
        title: 'Concierge',
        icon: '🤵',
        route: '/dashboard/concierge',
        color: '#96CEB4',
        description: 'AI assistant',
        module: 'agent',
        priority: 3
    },
    {
        id: 'governance',
        title: 'Council',
        icon: '⚖️',
        route: '/dashboard/governance',
        color: '#D4A5A5',
        description: 'Vote and govern',
        module: 'governance',
        priority: 2
    },
    {
        id: 'growth',
        title: 'Growth',
        icon: '🌱',
        route: '/dashboard/growth',
        color: '#88B04B',
        description: 'Autonomous compounding',
        module: 'growth',
        priority: 3
    },
    {
        id: 'telemetry',
        title: 'Telemetry',
        icon: '📡',
        route: '/dashboard/telemetry',
        color: '#9B59B6',
        description: 'System logs',
        module: 'telemetry',
        priority: 4
    },
    {
        id: 'forensics',
        title: 'Forensics',
        icon: '🔍',
        route: '/dashboard/forensics',
        color: '#E67E22',
        description: 'Deep analysis',
        module: 'forensics',
        priority: 4
    },
    {
        id: 'strategy',
        title: 'Strategy',
        icon: '🎯',
        route: '/dashboard/strategy',
        color: '#2C3E50',
        description: 'AI recommendations',
        module: 'strategy',
        priority: 3
    },
    {
        id: 'wellbeing',
        title: 'Wellbeing',
        icon: '🧘',
        route: '/dashboard/wellbeing',
        color: '#A8E6CF',
        description: 'Health tracking',
        module: 'wellbeing',
        priority: 2
    }
];

export interface DashboardLayout {
    pinnedTiles: string[];
    hiddenTiles: string[];
    tileOrder: string[];
}

export interface DashboardState {
    layout: DashboardLayout;
    selectedTile: string | null;
    hoveredTile: string | null;
    resonanceScore: number;
    lastUpdated: string;
}

const defaultLayout: DashboardLayout = {
    pinnedTiles: ['wallet', 'hearth', 'metrics'],
    hiddenTiles: [],
    tileOrder: TILES.map(t => t.id)
};

class DashboardEngine {
    state = $state<DashboardState>({
        layout: defaultLayout,
        selectedTile: null,
        hoveredTile: null,
        resonanceScore: 1247,
        lastUpdated: new Date().toISOString()
    });

    constructor() {
        if (browser) {
            try {
                const saved = localStorage.getItem('dashboard_layout');
                if (saved) {
                    this.state.layout = JSON.parse(saved);
                }
            } catch (e) {
                console.error('Failed to load dashboard layout:', e);
            }
        }
    }

    private persist() {
        if (browser) {
            try {
                localStorage.setItem('dashboard_layout', JSON.stringify($state.snapshot(this.state.layout)));
            } catch (e) {
                console.error('Failed to save dashboard layout:', e);
            }
        }
    }

    selectTile(tileId: string | null) {
        this.state.selectedTile = tileId;
    }

    hoverTile(tileId: string | null) {
        this.state.hoveredTile = tileId;
    }

    pinTile(tileId: string) {
        this.state.layout.pinnedTiles = [...new Set([...this.state.layout.pinnedTiles, tileId])];
        this.persist();
    }

    unpinTile(tileId: string) {
        this.state.layout.pinnedTiles = this.state.layout.pinnedTiles.filter(id => id !== tileId);
        this.persist();
    }

    hideTile(tileId: string) {
        this.state.layout.hiddenTiles = [...new Set([...this.state.layout.hiddenTiles, tileId])];
        this.persist();
    }

    showTile(tileId: string) {
        this.state.layout.hiddenTiles = this.state.layout.hiddenTiles.filter(id => id !== tileId);
        this.persist();
    }

    reorderTiles(newOrder: string[]) {
        this.state.layout.tileOrder = newOrder;
        this.persist();
    }

    resetLayout() {
        this.state.layout = {
            pinnedTiles: ['wallet', 'hearth', 'metrics'],
            hiddenTiles: [],
            tileOrder: TILES.map(t => t.id)
        };
        this.persist();
    }
}

export const dashboardStore = new DashboardEngine();
