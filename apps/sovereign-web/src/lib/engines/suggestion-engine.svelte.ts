import { browser } from "$app/environment";
import { manifold } from "$lib/stores/master-store.svelte";
import { sovereignStore } from "$lib/stores/sovereign-store.svelte";
import { learningEngine } from "./learning-engine.svelte";
import type { Suggestion } from "$lib/types";

// NOTE: Add imports to actual stores once they are robust enough:
// import { vaultStore } from "$lib/stores/vault-store.svelte";
// import { hearthStore } from "$lib/stores/hearth-store.svelte";

const ENGINE_INTERVAL = 30000;

class SuggestionEngine {
    suggestions = $state<Suggestion[]>([]);

    private timer: ReturnType<typeof setInterval> | null = null;

    constructor() {
        if (browser) {
            this.start();
        }
    }

    start() {
        if (this.timer) return;
        this.timer = setInterval(() => this.tick(), ENGINE_INTERVAL);
        // Initial tick after a short delay to allow stores to hydrate
        setTimeout(() => this.tick(), 2000);
    }

    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    private tick() {
        if (!browser) return;


        const newSuggestions = [
            ...this.detectIdleAssets(),
            ...this.detectGovernanceOpportunities(),
            ...this.detectBridgeOpportunities(),
            ...this.detectMilestones(),
            ...this.detectAnomalies()
        ];

        // Merge, prioritize, and deduplicate
        const merged = this.prioritizeAndMerge(newSuggestions);
        this.suggestions = merged;
    }

    private prioritizeAndMerge(newSuggestions: Suggestion[]): Suggestion[] {
        // Keep existing suggestions that haven't been dismissed
        // Merge in new ones if they don't already exist (by ID)

        const currentMap = new Map<string, Suggestion>();
        for (const s of this.suggestions) {
            // @ts-ignore
            if (!s.dismissed) {
                currentMap.set(s.id, s);
            }
        }

        for (const ns of newSuggestions) {
            // Update or add, unless dismissed
            const existing = currentMap.get(ns.id);
            if (!existing || (!existing.dismissed)) {
            // @ts-ignore
                // If it already exists, maybe retain 'seen' status
                const seenState = existing ? existing.seen : false;
                currentMap.set(ns.id, { ...ns, seen: seenState });
            }
        }

        // Filter expired
        const now = Date.now();
        const valid = Array.from(currentMap.values()).filter(s => {
            if (s.expiresAt && s.expiresAt < now) return false;
            return true;
        });

        // Apply Learning Engine personalization
        const personalized = learningEngine.personalize(valid);

        // Max cap
        return personalized.slice(0, 10);
    }

    // --- TRIGGERS ---

    private detectIdleAssets(): Suggestion[] {
        // Mock idle asset logic: if user has no staked balance but has overall balance
        // Replace with real vaultStore logic when available.
        // For demonstration, arbitrarily triggering if Math.random() < 0.2
        const suggestions: Suggestion[] = [];

        if (Math.random() < 0.2) {
            suggestions.push({
                id: 'idle-asset-usdc',
                type: 'idle-asset',
                title: 'Earn yield on idle assets',
                description: 'You have unstaked USDC. Stake now for 12.4% APY.',
                priority: 7,
                seen: false,
                dismissed: false,
                context: { source: 'vault' }
            });
        }
        return suggestions;
    }

    private detectGovernanceOpportunities(): Suggestion[] {
        const suggestions: Suggestion[] = [];
        if (Math.random() < 0.15) {
            suggestions.push({
                id: 'gov-proposal-1024',
                type: 'governance-proposal',
                title: 'High Priority Vote',
                description: 'A new network upgrade parameter vote is ending soon.',
                priority: 8,
                seen: false,
                dismissed: false,
                context: { source: 'council' }
            });
        }
        return suggestions;
    }

    private detectBridgeOpportunities(): Suggestion[] {
        const suggestions: Suggestion[] = [];
        if (Math.random() < 0.1) {
            suggestions.push({
                id: 'bridge-low-gas',
                type: 'bridge-opportunity',
                title: 'Optimal Bridge Timing',
                description: 'Ethereum gas is 20% below the weekly average. Perfect time to bridge.',
                priority: 6,
                seen: false,
                dismissed: false,
                expiresAt: Date.now() + 3600000,
                context: { source: 'bridge' }
            });
        }
        return suggestions;
    }

    private detectMilestones(): Suggestion[] {
        const suggestions: Suggestion[] = [];
        const state = sovereignStore.state;

        // E.g., remind to take the first transaction if they haven't yet
        if (!state.onboarding.firstTransaction) {
            suggestions.push({
                id: 'milestone-first-tx',
                type: 'milestone-completion',
            // @ts-ignore
                title: 'Complete your first transaction',
                description: 'Step into true sovereignty by initiating a peer-to-peer transfer.',
                priority: 5,
                seen: false,
                dismissed: false,
                context: { source: 'vault' }
            });
        }

        return suggestions;
    }

    private detectAnomalies(): Suggestion[] {
        const suggestions: Suggestion[] = [];

        // Use real manifold data to detect low resonance anomalies
        if (manifold.resonance < 50) {
            suggestions.push({
                id: 'anomaly-resonance-low',
                type: 'anomaly-detected',
                title: 'System Resonance Dropping',
                description: 'Network health is fluctuating. Shard-mesh may be stressed.',
                priority: 9,
                seen: false,
                dismissed: false,
                context: { source: 'manifold' }
            });
        }

        return suggestions;
    }

    // --- ACTIONS ---

    markSeen(id: string) {
        const sugg = this.suggestions.find(s => s.id === id);
        if (sugg && !sugg.seen) {
            sugg.seen = true;
            learningEngine.trackInteraction({
                suggestionId: sugg.id,
                type: sugg.type,
            // @ts-ignore
                action: 'seen',
            // @ts-ignore
                timestamp: Date.now(),
                source: sugg.context.source
            });
            // @ts-ignore
        }
    }

    dismiss(id: string) {
            // @ts-ignore
        const sugg = this.suggestions.find(s => s.id === id);
        if (sugg) {
            sugg.dismissed = true;
            learningEngine.trackInteraction({
                suggestionId: sugg.id,
                type: sugg.type,
                action: 'dismissed',
                timestamp: Date.now(),
                source: sugg.context.source
            });
            // @ts-ignore
            this.suggestions = this.suggestions.filter(s => s.id !== id);
        }
    }
}

const suggestionEngine = new SuggestionEngine();
