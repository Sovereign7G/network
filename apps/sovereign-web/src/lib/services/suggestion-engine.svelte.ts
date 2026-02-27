
import { manifold } from '$lib/stores/master-store.svelte';
import { sovereignStore } from '$lib/stores/sovereign-store.svelte';
import { vaultStore } from '$lib/stores/vault-store.svelte';
import { hearthStore } from '$lib/stores/hearth-store.svelte';
import type { Suggestion, SuggestionEngineConfig } from '$lib/types';

class SuggestionEngine {
    private config: SuggestionEngineConfig;
    public suggestions = $state<Suggestion[]>([]);

    constructor(config: Partial<SuggestionEngineConfig> = {}) {
        this.config = {
            maxSuggestions: 10,
            pollingInterval: 30000,
            cooldownPeriods: {},
            ...config
        };
    }

    public activeSuggestions = $derived.by(() => {
        // 1. Resonance-based suggestions
        if (manifold.resonance < 50) {
            this.addUniqueSuggestion({
                type: 'ACTION',
                title: 'Sync Resonance',
                description: 'Your connection to the manifold is drifting. Re-sync to stabilize.',
                priority: 10,
                action: {
                    label: 'Sync',
                    handler: () => manifold.recordEvent('MANIFOLD_SYNC', 'Manual resonance re-alignment triggered.')
                },
                context: { source: 'manifold', data: {} },
                seen: false,
                dismissed: false
            });
        }

        // 2. Hearth-based suggestions
        if (hearthStore.state.streak === 0) {
            this.addUniqueSuggestion({
                type: 'ACTION',
                title: 'Morning Reflection',
                description: 'Maintain your sovereign presence with a brief reflection.',
                priority: 8,
                action: {
                    label: 'Reflect',
                    handler: () => { window.location.href = '/hearth'; }
                },
                context: { source: 'hearth', data: {} },
                seen: false,
                dismissed: false
            });
        }

        // 3. Vault-based suggestions
        const pendingTx = vaultStore.state.transactions.find((t: any) => t.status === 'pending');
        if (pendingTx) {
            this.addUniqueSuggestion({
                type: 'INSIGHT',
                title: 'Track Propagation',
                description: 'A transaction is traversing the substrate. Monitor its trail.',
                priority: 9,
                action: {
                    label: 'Track',
                    handler: () => { window.location.href = `/vault/${pendingTx.id}`; }
                },
                context: { source: 'vault', data: { txId: pendingTx.id } },
                seen: false,
                dismissed: false
            });
        }

        // 4. Advanced Mode discovery
        if (!sovereignStore.state.preferences.advancedMode && manifold.resonance > 95) {
            this.addUniqueSuggestion({
                type: 'OPTIMIZATION',
                title: 'Unleash Sovereign Tools',
                description: 'You are highly coherent. Advanced ZK-tools are now recommended.',
                priority: 5,
                action: {
                    label: 'Unleash',
                    handler: () => sovereignStore.toggleAdvancedMode()
                },
                context: { source: 'sovereign', data: {} },
                seen: false,
                dismissed: false
            });
        }

        return this.suggestions
            .filter(s => !s.dismissed && !s.seen)
            .sort((a, b) => (b.priority as number) - (a.priority as number))
            .slice(0, 3);
    });

    private addUniqueSuggestion(s: Omit<Suggestion, 'id'>): void {
        const exists = this.suggestions.find(existing => existing.title === s.title);
        if (!exists && this.suggestions.length < this.config.maxSuggestions) {
            this.suggestions.push({
                ...s,
                id: Math.random().toString(36).substring(7).toUpperCase()
            });
        }
    }

    public markSeen(id: string): void {
        const s = this.suggestions.find(s => s.id === id);
        if (s) s.seen = true;
    }

    public dismiss(id: string): void {
        const s = this.suggestions.find(s => s.id === id);
        if (s) s.dismissed = true;
    }
}

const suggestionEngine = new SuggestionEngine();
