import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { MEMORY_TYPES, RESONANCE_TIERS } from './constants';
import type {
    HearthState,
    Memory,
    HearthFilters
} from '$lib/types';

const initialState: HearthState = {
    memories: Array.from({ length: 47 }, (_, i) => ({
        id: `memory-${i}`,
        title: `Memory Log #${47 - i}`,
        content: `Reflecting on the Sovereign Cathedral resonance at level ${90 + Math.floor(Math.random() * 10)}%`,
        timestamp: new Date(Date.now() - i * 3600000 * 12),
        type: 'gratitude',
        resonance: 25,
        reflections: [],
        tags: ['cathedral', 'sovereign']
    })),
    streak: 0,
    lastEntryDate: null,
    totalResonance: 1247,
    lifetimeResonance: 1247,
    filters: {
        type: 'all',
        search: '',
        dateRange: 'all'
    },
    insights: [
        {
            id: '1',
            title: 'Peak Resonance Times',
            description: 'You tend to write most deeply in the evening',
            type: 'pattern',
            icon: '🌙',
            confidence: 0.85,
            timestamp: new Date(Date.now() - 3600000),
            actionable: true,
            action: 'Set evening reminder'
        },
        {
            id: '2',
            title: 'Gratitude Champion',
            description: 'Gratitude is your most frequent memory type',
            type: 'achievement',
            icon: '🙏',
            confidence: 0.92,
            timestamp: new Date(Date.now() - 7200000),
            actionable: false
        }
    ],
    achievements: [
        {
            id: '1',
            title: 'First Flame',
            description: 'Created your first memory',
            earned: true,
            icon: '🔥',
            earnedAt: new Date(Date.now() - 86400000 * 7)
        },
        {
            id: '2',
            title: 'Week Warrior',
            description: '7-day streak',
            earned: true,
            icon: '📅',
            earnedAt: new Date(Date.now() - 86400000 * 3)
        },
        {
            id: '3',
            title: 'Resonance Master',
            description: 'Reach 1000 total resonance',
            earned: false,
            icon: '✨',
            progress: 1247,
            target: 1000,
            earnedAt: null
        }
    ],
    resonanceHistory: Array.from({ length: 30 }, (_, i) => ({
        date: new Date(Date.now() - (29 - i) * 86400000),
        value: Math.floor(Math.random() * 50) + 20
    }))
};

class HearthEngine {
    state = $state<HearthState>(initialState);

    constructor() {
        if (browser) {
            const stored = loadFromStorage<HearthState>('hearth', initialState);

            if (stored.memories) {
                stored.memories = stored.memories.map(m => ({
                    ...m,
                    timestamp: new Date(m.timestamp),
                    reflections: m.reflections?.map(r => ({
                        ...r,
                        timestamp: new Date(r.timestamp)
                    })) || []
                }));
            }
            if (stored.achievements) {
                stored.achievements = stored.achievements.map(a => ({
                    ...a,
                    earnedAt: a.earnedAt ? new Date(a.earnedAt) : null
                }));
            }
            if (stored.resonanceHistory) {
                stored.resonanceHistory = stored.resonanceHistory.map(r => ({
                    ...r,
                    date: new Date(r.date)
                }));
            }
            if (stored.insights) {
                stored.insights = stored.insights.map(i => ({
                    ...i,
                    timestamp: new Date(i.timestamp)
                }));
            }

            this.state = stored;
        }
    }

    private generateUUID() {
        return browser && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2);
    }

    addMemory(memory: Omit<Memory, 'id' | 'timestamp' | 'resonance' | 'reflections'>) {
        const typeMeta = (MEMORY_TYPES as Record<string, any>)[memory.type.toUpperCase()] || MEMORY_TYPES.GRATITUDE;
        const resonanceValue = typeMeta.resonance;

        const newMemory: Memory = {
            ...memory,
            id: this.generateUUID(),
            timestamp: new Date(),
            resonance: resonanceValue,
            reflections: [],
            tags: memory.tags || []
        };

        const today = new Date().toDateString();
        const lastDate = this.state.lastEntryDate ? new Date(this.state.lastEntryDate).toDateString() : null;

        if (lastDate !== today) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            if (lastDate === yesterday.toDateString()) {
                this.state.streak += 1;
            } else {
                this.state.streak = 1;
            }
            this.state.lastEntryDate = today;
        }

        const existingHistory = this.state.resonanceHistory.find(r => r.date.toDateString() === today);
        if (existingHistory) {
            existingHistory.value += resonanceValue;
        } else {
            this.state.resonanceHistory.push({ date: new Date(), value: resonanceValue });
            if (this.state.resonanceHistory.length > 90) this.state.resonanceHistory.shift();
        }

        this.state.memories = [newMemory, ...this.state.memories];
        this.state.totalResonance += resonanceValue;
        this.state.lifetimeResonance += resonanceValue;

        if (this.state.memories.length === 1) {
            const a = this.state.achievements.find(a => a.id === '1');
            if (a) { a.earned = true; a.earnedAt = new Date(); }
        }

        this.persist();
    }

    addReflection(memoryId: string, reflection: string) {
        const memory = this.state.memories.find(m => m.id === memoryId);
        if (memory) {
            memory.reflections.push({
                id: this.generateUUID(),
                content: reflection,
                timestamp: new Date()
            });
            this.persist();
        }
    }

    deleteMemory(id: string) {
        const memoryIndex = this.state.memories.findIndex(m => m.id === id);
        if (memoryIndex !== -1) {
            const memory = this.state.memories[memoryIndex];
            this.state.totalResonance = Math.max(0, this.state.totalResonance - (memory.resonance || 0));
            this.state.memories.splice(memoryIndex, 1);
            this.persist();
        }
    }

    setFilter<K extends keyof HearthFilters>(filterType: K, value: HearthFilters[K]) {
        this.state.filters[filterType] = value;
        this.persist();
    }

    getResonanceTier(resonance: number) {
        for (let i = RESONANCE_TIERS.length - 1; i >= 0; i--) {
            const tier = RESONANCE_TIERS[i];
            if (resonance >= tier.threshold) {
                return tier;
            }
        }
        return RESONANCE_TIERS[0];
    }

    private persist() {
        if (browser) {
            saveToStorage('hearth', $state.snapshot(this.state));
        }
    }
}

export const hearthStore = new HearthEngine();
