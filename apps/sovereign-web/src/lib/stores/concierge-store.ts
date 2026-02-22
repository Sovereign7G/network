import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { CONCIERGE_PERSONALITIES, CONCIERGE_CAPABILITIES } from './constants';
import { sovereignStore } from './sovereign-store';
import { hearthStore } from './hearth-store';
import { vaultStore } from './vault-store';
import { governanceStore } from './governance-store';
import { llmService } from '$lib/services/llm-service';
import type {
    ConciergeState,
    Conversation,
    ConversationMessage,
    Insight,
    ScheduledReminder,
    KnowledgeBase,
    Suggestion,
    UserContext,
    Personality,
    Capability,
    SovereignState,
    HearthState,
    VaultState,
    GovernanceState
} from '$lib/types';

const initialState: ConciergeState = {
    initialized: true,
    personality: CONCIERGE_PERSONALITIES.WISE.id,
    capabilities: { ...CONCIERGE_CAPABILITIES },
    conversations: [
        {
            id: '1',
            title: 'Welcome to AGE',
            lastMessage: 'How can I assist you today?',
            timestamp: new Date(),
            unread: false,
            messages: [
                {
                    id: 'welcome1',
                    role: 'assistant',
                    content: 'Welcome, Sovereign. I am your Concierge, an intelligence designed to understand your journey through the AGE Protocol. How may I assist you today?',
                    timestamp: new Date(Date.now() - 86400000),
                    context: {
                        type: 'greeting',
                        sentiment: 'warm'
                    }
                }
            ]
        }
    ],
    currentConversationId: '1',
    insights: [
        {
            id: 'insight1',
            type: 'pattern',
            title: 'Evening Reflection Pattern',
            description: 'You tend to write most deeply in your Hearth between 8-10 PM',
            confidence: 0.85,
            timestamp: new Date(Date.now() - 3600000),
            actionable: true,
            action: 'Set evening reminder'
        },
        {
            id: 'insight2',
            type: 'opportunity',
            title: 'Unused Voting Power',
            description: 'You haven\'t voted on 3 active proposals that align with your interests',
            confidence: 0.92,
            timestamp: new Date(Date.now() - 7200000),
            actionable: true,
            action: 'View proposals'
        },
        {
            id: 'insight3',
            type: 'achievement',
            title: 'Almost There!',
            description: 'You\'re 3 days away from a 30-day Hearth streak',
            confidence: 1.0,
            timestamp: new Date(Date.now() - 1800000),
            actionable: true,
            action: 'Write today\'s entry'
        }
    ],
    scheduledReminders: [
        {
            id: 'remind1',
            title: 'Evening Reflection',
            description: 'Time to write in your Hearth',
            cron: '0 21 * * *',
            enabled: true,
            lastTriggered: new Date(Date.now() - 86400000),
            nextTrigger: new Date(Date.now() + 3600000)
        }
    ],
    autonomousTasks: [],
    knowledgeBase: {
        userPreferences: {
            favoriteMemoryTypes: ['gratitude', 'insight'],
            peakActivityHours: [20, 21, 22],
            votingTopics: ['parameter', 'treasury'],
            assetPreferences: ['AGE', 'RES']
        },
        learnedPatterns: {
            resonanceVelocity: 12.5,
            votingConsistency: 0.75,
            reflectionDepth: 0.8
        }
    },
    suggestions: [
        {
            id: 'sugg1',
            text: 'Write about today\'s insights',
            context: 'hearth',
            priority: 0.9
        },
        {
            id: 'sugg2',
            text: 'Review the new governance proposal',
            context: 'governance',
            priority: 0.7
        },
        {
            id: 'sugg3',
            text: 'Check your asset allocation',
            context: 'vault',
            priority: 0.5
        }
    ],
    isProcessing: false
};

function createConciergeStore() {
    const stored = loadFromStorage<ConciergeState>('concierge', initialState);

    // Restore dates in conversations
    if (stored.conversations) {
        stored.conversations = stored.conversations.map(c => ({
            ...c,
            timestamp: new Date(c.timestamp),
            messages: c.messages?.map(m => ({
                ...m,
                timestamp: new Date(m.timestamp)
            })) || []
        }));
    }

    // Restore dates in insights
    if (stored.insights) {
        stored.insights = stored.insights.map(i => ({
            ...i,
            timestamp: new Date(i.timestamp)
        }));
    }

    // Restore dates in reminders
    if (stored.scheduledReminders) {
        stored.scheduledReminders = stored.scheduledReminders.map(r => ({
            ...r,
            lastTriggered: r.lastTriggered ? new Date(r.lastTriggered) : null,
            nextTrigger: r.nextTrigger ? new Date(r.nextTrigger) : null
        }));
    }

    const { subscribe, set, update } = writable<ConciergeState>(stored);

    return {
        subscribe,

        sendMessage: async (content: string, userContext: UserContext): Promise<void> => {
            // Add user message immediately
            update((state: ConciergeState) => {
                const newMessage: ConversationMessage = {
                    id: crypto.randomUUID(),
                    role: 'user',
                    content,
                    timestamp: new Date()
                };

                let conversations = [...state.conversations];
                const conversationIndex = conversations.findIndex(c => c.id === state.currentConversationId);

                if (conversationIndex >= 0) {
                    const conversation = conversations[conversationIndex];
                    conversations[conversationIndex] = {
                        ...conversation,
                        messages: [...(conversation.messages || []), newMessage],
                        lastMessage: content,
                        timestamp: new Date()
                    };
                }

                return {
                    ...state,
                    conversations,
                    isProcessing: true
                };
            });

            try {
                const state = get({ subscribe });
                const conversation = state.conversations.find(c => c.id === state.currentConversationId);
                const personality = CONCIERGE_PERSONALITIES[state.personality.toUpperCase()]?.description || 'wise';

                if (!conversation) return;

                let fullResponse = '';

                // Call LLM service with streaming
                await llmService.sendMessage(
                    userContext,
                    conversation,
                    content,
                    personality,
                    (chunk) => {
                        fullResponse += chunk.content;

                        // Update UI with streaming response
                        update((currentState: ConciergeState) => {
                            const conversations = [...currentState.conversations];
                            const convIdx = conversations.findIndex(c => c.id === currentState.currentConversationId);

                            if (convIdx >= 0) {
                                const messages = conversations[convIdx].messages;
                                const lastMessage = messages[messages.length - 1];

                                if (lastMessage && lastMessage.role === 'assistant' && lastMessage.streaming) {
                                    lastMessage.content = fullResponse;
                                } else {
                                    messages.push({
                                        id: crypto.randomUUID(),
                                        role: 'assistant',
                                        content: fullResponse,
                                        timestamp: new Date(),
                                        streaming: true
                                    });
                                }
                            }

                            return { ...currentState, conversations };
                        });
                    }
                );

                // Finalize response
                update((currentState: ConciergeState) => {
                    const conversations = [...currentState.conversations];
                    const convIdx = conversations.findIndex(c => c.id === currentState.currentConversationId);

                    if (convIdx >= 0) {
                        const messages = conversations[convIdx].messages;
                        const lastMessage = messages[messages.length - 1];

                        if (lastMessage && lastMessage.role === 'assistant') {
                            lastMessage.streaming = false;
                        }
                    }

                    // Generate insight based on conversation
                    const newInsight: Insight = {
                        id: crypto.randomUUID(),
                        type: 'conversation',
                        title: 'New conversation completed',
                        description: `You discussed "${content.substring(0, 50)}${content.length > 50 ? '...' : ''}"`,
                        confidence: 0.8,
                        timestamp: new Date(),
                        actionable: false
                    };

                    const newState = {
                        ...currentState,
                        conversations,
                        insights: [newInsight, ...currentState.insights].slice(0, 10),
                        isProcessing: false
                    };
                    saveToStorage('concierge', newState);
                    return newState;
                });

            } catch (error) {
                console.error('LLM API error:', error);

                // Add error message
                update((currentState: ConciergeState) => {
                    const conversations = [...currentState.conversations];
                    const convIdx = conversations.findIndex(c => c.id === currentState.currentConversationId);

                    if (convIdx >= 0) {
                        conversations[convIdx].messages.push({
                            id: crypto.randomUUID(),
                            role: 'assistant',
                            content: `I apologize, but I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please check your API configuration.`,
                            timestamp: new Date(),
                            isError: true
                        });
                    }

                    const newState = {
                        ...currentState,
                        conversations,
                        isProcessing: false
                    };
                    saveToStorage('concierge', newState);
                    return newState;
                });
            }
        },

        newConversation: () => update((state: ConciergeState) => {
            const newConversation: Conversation = {
                id: crypto.randomUUID(),
                title: 'New Conversation',
                lastMessage: 'How can I help?',
                timestamp: new Date(),
                unread: false,
                messages: [
                    {
                        id: crypto.randomUUID(),
                        role: 'assistant',
                        content: 'Hello again, Sovereign. What would you like to explore?',
                        timestamp: new Date(),
                        context: { type: 'greeting', sentiment: 'warm' }
                    }
                ]
            };

            const newState: ConciergeState = {
                ...state,
                conversations: [newConversation, ...state.conversations],
                currentConversationId: newConversation.id
            };

            saveToStorage('concierge', newState);
            return newState;
        }),

        switchConversation: (conversationId: string) => update((state: ConciergeState) => {
            const newState: ConciergeState = {
                ...state,
                currentConversationId: conversationId,
                conversations: state.conversations.map(c =>
                    c.id === conversationId ? { ...c, unread: false } : c
                )
            };
            saveToStorage('concierge', newState);
            return newState;
        }),

        deleteConversation: (conversationId: string) => update((state: ConciergeState) => {
            const conversations = state.conversations.filter(c => c.id !== conversationId);
            const currentConversationId = conversations.length > 0 ? conversations[0]?.id ?? null : null;

            const newState: ConciergeState = {
                ...state,
                conversations,
                currentConversationId
            };

            saveToStorage('concierge', newState);
            return newState;
        }),

        setPersonality: (personalityId: string) => update((state: ConciergeState) => {
            const newState: ConciergeState = {
                ...state,
                personality: personalityId
            };
            saveToStorage('concierge', newState);
            return newState;
        }),

        toggleCapability: (capabilityId: string) => update((state: ConciergeState) => {
            const capability = state.capabilities[capabilityId];
            if (!capability) return state;

            const newState: ConciergeState = {
                ...state,
                capabilities: {
                    ...state.capabilities,
                    [capabilityId]: {
                        ...capability,
                        enabled: !capability.enabled
                    }
                }
            };
            saveToStorage('concierge', newState);
            return newState;
        }),

        addReminder: (reminder: Omit<ScheduledReminder, 'id' | 'enabled' | 'lastTriggered' | 'nextTrigger'>) =>
            update((state: ConciergeState) => {
                const newReminder: ScheduledReminder = {
                    ...reminder,
                    id: crypto.randomUUID(),
                    enabled: true,
                    lastTriggered: null,
                    nextTrigger: new Date(Date.now() + 86400000) // Tomorrow
                };

                const newState: ConciergeState = {
                    ...state,
                    scheduledReminders: [...state.scheduledReminders, newReminder]
                };

                saveToStorage('concierge', newState);
                return newState;
            }),

        dismissInsight: (insightId: string) => update((state: ConciergeState) => {
            const newState: ConciergeState = {
                ...state,
                insights: state.insights.filter(i => i.id !== insightId)
            };
            saveToStorage('concierge', newState);
            return newState;
        }),

        executeInsightAction: (insightId: string) => update((state: ConciergeState) => {
            const newState: ConciergeState = {
                ...state,
                insights: state.insights.map(i =>
                    i.id === insightId ? { ...i, actioned: true } : i
                )
            };
            saveToStorage('concierge', newState);
            return newState;
        }),

        generateUserContext: (
            sovereign: SovereignState,
            hearth: HearthState,
            vault: VaultState,
            governance: GovernanceState
        ): UserContext => {
            // Calculate favorite memory type
            const typeCounts: Record<string, number> = {};
            hearth.memories.forEach(m => {
                typeCounts[m.type] = (typeCounts[m.type] || 0) + 1;
            });

            const favoriteType = Object.entries(typeCounts)
                .sort((a, b) => b[1] - a[1])[0]?.[0] || 'gratitude';

            // Calculate voting pattern
            const voteCount = Object.keys(governance.userVotes).length;
            const votingPattern = voteCount > 3 ? 'consistently' : voteCount > 0 ? 'selectively' : 'thoughtfully';

            return {
                displayName: sovereign?.profile?.displayName || 'Sovereign',
                totalResonance: hearth?.totalResonance || 0,
                streak: hearth?.streak || 0,
                memoryCount: hearth?.memories?.length || 0,
                favoriteType,
                balances: vault?.balances || {},
                totalValue: vault?.totalValue || 0,
                activeProposals: governance?.proposals?.filter(p => p.status === 'active').length || 0,
                votingPower: governance?.votingPower || 0,
                votingPattern,
                bestDay: 'Tuesday',
                depthIncrease: 15
            };
        },

        getCurrentPersonality: (state: ConciergeState): Personality => {
            return CONCIERGE_PERSONALITIES[state.personality.toUpperCase()] || CONCIERGE_PERSONALITIES.WISE;
        },

        getSuggestionsByContext: (state: ConciergeState, context: string): Suggestion[] => {
            return state.suggestions
                .filter(s => s.context === context)
                .sort((a, b) => b.priority - a.priority);
        }
    };
}

export const conciergeStore = createConciergeStore();
