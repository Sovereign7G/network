import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Define all available tiles with their properties
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

// User preferences for tile layout
const defaultLayout = {
    pinnedTiles: ['wallet', 'hearth', 'metrics'], // Always show these first
    hiddenTiles: [], // Tiles user has hidden
    tileOrder: TILES.map(t => t.id) // Default order
};

// Load from localStorage
function loadLayout() {
    if (!browser) return defaultLayout;

    try {
        const saved = localStorage.getItem('dashboard_layout');
        return saved ? JSON.parse(saved) : defaultLayout;
    } catch (e) {
        console.error('Failed to load dashboard layout:', e);
        return defaultLayout;
    }
}

// Create the store
function createDashboardStore() {
    const { subscribe, set, update } = writable({
        layout: loadLayout(),
        selectedTile: null,
        hoveredTile: null,
        resonanceScore: 1247, // Mock data - will come from user store
        lastUpdated: new Date().toISOString()
    });

    // Save layout to localStorage on changes
    if (browser) {
        subscribe(state => {
            try {
                localStorage.setItem('dashboard_layout', JSON.stringify(state.layout));
            } catch (e) {
                console.error('Failed to save dashboard layout:', e);
            }
        });
    }

    return {
        subscribe,

        // Tile interactions
        selectTile: (tileId) => update(state => ({
            ...state,
            selectedTile: tileId
        })),

        hoverTile: (tileId) => update(state => ({
            ...state,
            hoveredTile: tileId
        })),

        // Layout management
        pinTile: (tileId) => update(state => ({
            ...state,
            layout: {
                ...state.layout,
                pinnedTiles: [...new Set([...state.layout.pinnedTiles, tileId])]
            }
        })),

        unpinTile: (tileId) => update(state => ({
            ...state,
            layout: {
                ...state.layout,
                pinnedTiles: state.layout.pinnedTiles.filter(id => id !== tileId)
            }
        })),

        hideTile: (tileId) => update(state => ({
            ...state,
            layout: {
                ...state.layout,
                hiddenTiles: [...new Set([...state.layout.hiddenTiles, tileId])]
            }
        })),

        showTile: (tileId) => update(state => ({
            ...state,
            layout: {
                ...state.layout,
                hiddenTiles: state.layout.hiddenTiles.filter(id => id !== tileId)
            }
        })),

        // Reorder tiles
        reorderTiles: (newOrder) => update(state => ({
            ...state,
            layout: {
                ...state.layout,
                tileOrder: newOrder
            }
        })),

        // Reset to default
        resetLayout: () => update(state => ({
            ...state,
            layout: defaultLayout
        }))
    };
}

export const dashboardStore = createDashboardStore();
