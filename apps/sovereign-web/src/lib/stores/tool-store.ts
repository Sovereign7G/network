import { writable } from 'svelte/store';

export interface Tool {
    name: string;
    icon: string;
    action: string;
    desc: string;
    component?: any;
}

export interface Capability {
    name: string;
    icon: string;
    status: 'active' | 'beta' | 'coming';
    desc: string;
}

function createToolStore() {
    const { subscribe, set, update } = writable({
        activeTool: null as Tool | null,
        toolPanelOpen: false,
        quickStats: {
            resonance: 98,
            tps: 1247,
            nodes: 389000,
            blocks: 47
        }
    });

    return {
        subscribe,

        activateTool(tool: Tool) {
            update(state => ({ ...state, activeTool: tool, toolPanelOpen: true }));
        },

        deactivateTool() {
            update(state => ({ ...state, activeTool: null, toolPanelOpen: false }));
        },

        toggleToolPanel() {
            update(state => ({ ...state, toolPanelOpen: !state.toolPanelOpen }));
        },

        updateQuickStats(stats: any) {
            update(state => ({ ...state, quickStats: { ...state.quickStats, ...stats } }));
        }
    };
}

export const toolStore = createToolStore();
