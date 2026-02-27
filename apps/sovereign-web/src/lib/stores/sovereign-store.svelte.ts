import { browser } from '$app/environment';
import type { SovereignState, SovereignProfile, SovereignPreferences } from '$lib/types';

// ─── INITIAL STATE ──────────────────────────────────────────────────────────

const INITIAL_SOVEREIGN: SovereignState = {
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
        notifications: true,
        advancedMode: false
    },
    onboarding: {
        firstVisit: false,
        firstTransaction: false,
        firstZkProof: false,
        firstVote: false,
        firstHearthMemory: false
    }
};

// ─── THE SOVEREIGN IDENTITY ENGINE ───────────────────────────────────────────

class SovereignIdentityEngine {
    state = $state<SovereignState>(INITIAL_SOVEREIGN);

    constructor() {
        if (browser) {
            try {
                const saved = localStorage.getItem('sovereign');
                if (saved) {
                    this.state = { ...INITIAL_SOVEREIGN, ...JSON.parse(saved) };
                }
            } catch (e) {
                console.error('🛰️ [Identity] Manifest corruption detected. Re-initializing core defaults.');
            }
        }
    }

    // ─── ACTIONS ─────────────────────────────────────────────────────────────

            // @ts-ignore
    markEventComplete(event: keyof SovereignState['onboarding']) {
        if (this.state.onboarding[event]) return false;
        this.state.onboarding[event] = true;
            // @ts-ignore
        this.persist();
        return true;
    }

    initialize(data: Partial<SovereignState>) {
        Object.assign(this.state, data, { createdAt: new Date().toISOString() });
        this.persist();
    }

    updateProfile(profile: Partial<SovereignProfile>) {
        Object.assign(this.state.profile, profile);
        this.persist();
    }

    setVerificationLevel(level: number) {
        this.state.verificationLevel = level;
        this.persist();
    }

    updatePreferences(prefs: Partial<SovereignPreferences>) {
        Object.assign(this.state.preferences, prefs);
        this.persist();
    }

    toggleQuietMode() {
        this.state.preferences.quietMode = !this.state.preferences.quietMode;
        this.persist();
    }

    toggleAdvancedMode() {
        this.state.preferences.advancedMode = !this.state.preferences.advancedMode;
        this.persist();
    }

    updateLastActive() {
        this.state.lastActive = new Date().toISOString();
        this.persist();
    }

    // ─── BRIDGE METHODS ──────────────────────────────────────────────────────

    async createDID() {
        try {
            const { api } = await import('$lib/services/api');
            const response = await api.request('/identity/generate', { method: 'POST' });
            return response.did || `did:age:${Math.random().toString(36).substring(2, 12)}`;
        } catch (error) {
            return `did:age:${Math.random().toString(36).substring(2, 12)}`;
        }
    }

    async registerIdentity(data: Partial<SovereignState>) {
        if (!browser) return;
        try {
            const { api } = await import('$lib/services/api');
            const response = await api.request('/identity/register', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            if (response.success) {
            }
        } catch (error) {
            // Silence and allow offline-first onboarding
            throw error;
        }
    }

    async loadSovereignData() {
        if (!browser) return;
        try {
            const { api } = await import('$lib/services/api');
            const data = await api.request('/identity');
            if (data) {
                Object.assign(this.state, data);
                this.persist();
            }
        } catch (error) {
            console.warn('🛰️ [Identity] Core backplane unreachable. Using local sovereign cache.');
        }
    }

    private persist() {
        if (browser) {
            localStorage.setItem('sovereign', JSON.stringify($state.snapshot(this.state)));
        }
    }
}

const instance = new SovereignIdentityEngine();
export const sovereignStore = instance;
