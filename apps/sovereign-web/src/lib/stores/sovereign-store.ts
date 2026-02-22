import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { SovereignState, SovereignProfile, SovereignPreferences } from '$lib/types';

const initialState: SovereignState = {
    id: null,
    did: null,
    handle: null,
    profile: {
        displayName: 'Citizen',
        avatar: null,
        bio: '',
        location: null
    },
    verificationLevel: 0,
    createdAt: null,
    lastActive: new Date().toISOString(),
    preferences: {
        theme: 'dark',
        quietMode: false,
        autoPilot: false,
        notifications: true
    }
};

function loadFromStorage(): SovereignState {
    if (!browser) return initialState;

    try {
        const saved = localStorage.getItem('sovereign');
        if (saved) {
            const parsed = JSON.parse(saved);
            return { ...initialState, ...parsed };
        }
    } catch (e) {
        console.error('Failed to load sovereign data:', e);
    }

    return initialState;
}

function createSovereignStore() {
    const { subscribe, set, update } = writable<SovereignState>(loadFromStorage());

    return {
        subscribe,

        initialize: (data: Partial<SovereignState>) => update((state: SovereignState) => {
            const newState = {
                ...state,
                ...data,
                createdAt: new Date().toISOString()
            };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        updateProfile: (profile: Partial<SovereignProfile>) => update((state: SovereignState) => {
            const newState = {
                ...state,
                profile: { ...state.profile, ...profile }
            };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        setVerificationLevel: (level: number) => update((state: SovereignState) => {
            const newState = { ...state, verificationLevel: level };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        updatePreferences: (prefs: Partial<SovereignPreferences>) => update((state: SovereignState) => {
            const newState = {
                ...state,
                preferences: { ...state.preferences, ...prefs }
            };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        toggleQuietMode: () => update((state: SovereignState) => {
            const newState = {
                ...state,
                preferences: { ...state.preferences, quietMode: !state.preferences.quietMode }
            };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        updateLastActive: () => update((state: SovereignState) => {
            const newState = { ...state, lastActive: new Date().toISOString() };
            if (browser) localStorage.setItem('sovereign', JSON.stringify(newState));
            return newState;
        }),

        // 🏛️ SOVEREIGN BRIDGE: Backend integration
        createDID: async () => {
            // In a real system, this would generate a cryptographic keypair
            const id = Math.random().toString(36).substring(2, 15);
            return `did:age:${id}`;
        },

        registerIdentity: async (identity: Partial<SovereignState>) => {
            try {
                const { api } = await import('$lib/services/api');
                const response = await api.registerIdentity(identity);
                console.log('[SovereignStore] Identity registered on backend:', response);
                return response;
            } catch (error) {
                console.error('[SovereignStore] Failed to register identity on backend:', error);
                throw error;
            }
        },

        loadSovereignData: async () => {
            try {
                const { api } = await import('$lib/services/api');
                const data = await api.request('/identity');
                update(state => ({ ...state, ...data }));
            } catch (error) {
                console.error('[SovereignStore] Failed to load identity data:', error);
            }
        }
    };
}

export const sovereignStore = createSovereignStore();
