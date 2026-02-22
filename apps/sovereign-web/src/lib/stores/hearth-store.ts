import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { MEMORY_TYPES, RESONANCE_TIERS } from './constants';
import type {
    HearthState,
    Memory,
    MemoryReflection,
    Insight,
    Achievement,
    ResonanceHistoryEntry,
    HearthFilters,
    StoreUpdater
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
            target: 1000
        }
    ],
    resonanceHistory: Array.from({ length: 30 }, (_, i) => ({
        date: new Date(Date.now() - (29 - i) * 86400000),
        value: Math.floor(Math.random() * 50) + 20
    }))
};

function createHearthStore() {
    const stored = loadFromStorage<HearthState>('hearth', initialState);

    // Restore dates
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

    const { subscribe, set, update } = writable<HearthState>(stored);

    return {
        subscribe,

        addMemory: (memory: Omit<Memory, 'id' | 'timestamp' | 'resonance' | 'reflections'>) =>
            update((state: HearthState) => {
                const type = MEMORY_TYPES[memory.type.toUpperCase()] || MEMORY_TYPES.GRATITUDE;
                const resonanceValue = type.resonance;

                const newMemory: Memory = {
                    ...memory,
                    id: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(),
                    timestamp: new Date(),
                    resonance: resonanceValue,
                    reflections: [],
                    tags: memory.tags || []
                };

                // Update streak
                const today = new Date().toDateString();
                const lastDate = state.lastEntryDate ? new Date(state.lastEntryDate).toDateString() : null;
                let newStreak = state.streak;

                if (lastDate !== today) {
                    const yesterday = new Date();
                    yesterday.setDate(yesterday.getDate() - 1);
                    if (lastDate === yesterday.toDateString()) {
                        newStreak += 1;
                    } else {
                        newStreak = 1;
                    }
                }

                // Update resonance history
                const today_history = state.resonanceHistory.find(
                    r => r.date.toDateString() === today
                );

                let newHistory = [...state.resonanceHistory];
                if (today_history) {
                    newHistory = newHistory.map(r =>
                        r.date.toDateString() === today
                            ? { ...r, value: r.value + resonanceValue }
                            : r
                    );
                } else {
                    newHistory.push({
                        date: new Date(),
                        value: resonanceValue
                    });
                    newHistory = newHistory.slice(-90);
                }

                const newState: HearthState = {
                    ...state,
                    memories: [newMemory, ...state.memories],
                    streak: newStreak,
                    lastEntryDate: today,
                    totalResonance: state.totalResonance + resonanceValue,
                    lifetimeResonance: state.lifetimeResonance + resonanceValue,
                    resonanceHistory: newHistory
                };

                // Check for new achievements
                if (state.memories.length === 0) {
                    newState.achievements = newState.achievements.map(a =>
                        a.id === '1' ? { ...a, earned: true, earnedAt: new Date() } : a
                    );
                }

                if (newStreak >= 7 && !state.achievements.find(a => a.id === '2')?.earned) {
                    newState.achievements = newState.achievements.map(a =>
                        a.id === '2' ? { ...a, earned: true, earnedAt: new Date() } : a
                    );
                }

                saveToStorage('hearth', newState);
                return newState;
            }),

        addReflection: (memoryId: string, reflection: string) =>
            update((state: HearthState) => {
                const newReflection: MemoryReflection = {
                    id: crypto.randomUUID(),
                    content: reflection,
                    timestamp: new Date()
                };

                const newState: HearthState = {
                    ...state,
                    memories: state.memories.map(m =>
                        m.id === memoryId
                            ? {
                                ...m,
                                reflections: [...(m.reflections || []), newReflection]
                            }
                            : m
                    )
                };

                saveToStorage('hearth', newState);
                return newState;
            }),

        deleteMemory: (id: string) => update((state: HearthState) => {
            const memory = state.memories.find(m => m.id === id);
            if (!memory) return state;

            const newState: HearthState = {
                ...state,
                memories: state.memories.filter(m => m.id !== id),
                totalResonance: Math.max(0, state.totalResonance - (memory.resonance || 0))
            };

            saveToStorage('hearth', newState);
            return newState;
        }),

        setFilter: <K extends keyof HearthFilters>(filterType: K, value: HearthFilters[K]) =>
            update((state: HearthState) => {
                const newState: HearthState = {
                    ...state,
                    filters: { ...state.filters, [filterType]: value }
                };
                saveToStorage('hearth', newState);
                return newState;
            }),

        getResonanceTier: (resonance: number) => {
            for (let i = RESONANCE_TIERS.length - 1; i >= 0; i--) {
                const tier = RESONANCE_TIERS[i];
                if (resonance >= tier.threshold) {
                    return tier;
                }
            }
            return RESONANCE_TIERS[0];
        },

        getFilteredMemories: (state: HearthState): Memory[] => {
            return state.memories.filter(memory => {
                const matchesType = state.filters.type === 'all' || memory.type === state.filters.type;
                const matchesSearch = state.filters.search === '' ||
                    memory.content.toLowerCase().includes(state.filters.search.toLowerCase()) ||
                    (memory.title && memory.title.toLowerCase().includes(state.filters.search.toLowerCase()));

                let matchesDate = true;
                const now = new Date();
                if (state.filters.dateRange === 'week') {
                    const weekAgo = new Date(now.setDate(now.getDate() - 7));
                    matchesDate = new Date(memory.timestamp) >= weekAgo;
                } else if (state.filters.dateRange === 'month') {
                    const monthAgo = new Date(now.setMonth(now.getMonth() - 1));
                    matchesDate = new Date(memory.timestamp) >= monthAgo;
                } else if (state.filters.dateRange === 'year') {
                    const yearAgo = new Date(now.setFullYear(now.getFullYear() - 1));
                    matchesDate = new Date(memory.timestamp) >= yearAgo;
                }

                return matchesType && matchesSearch && matchesDate;
            });
        },

        exportMemories: () => {
            let state: HearthState | undefined;
            subscribe(s => state = s)();
            if (!state) return null;
            return {
                memories: state.memories,
                totalResonance: state.totalResonance,
                streak: state.streak,
                exportDate: new Date().toISOString(),
                version: '1.0'
            };
        }
    };
}

export const hearthStore = createHearthStore();
