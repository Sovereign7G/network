import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import type {
    ConciergeState,
    Conversation,
    Insight,
            // @ts-ignore
    MessageInteraction,
    UserContext,
    Personality,
    ConversationMessage
} from '$lib/types';
import { llmService } from '$lib/services/llm-service.svelte';

const CONCIERGE_PERSONALITIES = {
    WISE: {
        id: 'wise',
        name: 'The Sovereign Architect',
        description: 'Analytical, deep, and focused on long-term systemic architecture.',
        traits: ['analytical', 'formal', 'strategic']
    },
    DIRECT: {
        id: 'direct',
        name: 'The Executor',
        description: 'Action-oriented, brief, and uncompromisingly efficient.',
        traits: ['concise', 'action-oriented', 'blunt']
    },
    ADAPTIVE: {
        id: 'adaptive',
        name: 'The Flow State',
        description: 'Empathetic, nuanced, adjusting to your cognitive rhythm.',
        traits: ['empathetic', 'nuanced', 'flexible']
    }
};

const initialState: ConciergeState = {
    initialized: true,
    personality: 'wise',
    capabilities: {},
    conversations: [
        {
            id: 'conv1',
            title: 'Sovereign Manifestation Guidance',
            lastMessage: 'Let us coordinate your next strategic maneuver.',
            timestamp: new Date(),
            messages: [
                {
                    id: 'msg1',
                    role: 'assistant',
                    content: 'System fully initialized. Operating under Sovereign ruleset.',
                    timestamp: new Date(Date.now() - 86400000)
                },
                {
                    id: 'msg2',
                    role: 'assistant',
                    content: 'Greetings. The manifold is stable. How can I assist in orchestrating your resources today?',
                    timestamp: new Date(Date.now() - 3600000)
                }
            ],
            context: {
                activeModule: 'dashboard',
                resonance: 92
            }
        }
    ],
    currentConversationId: 'conv1',
    insights: [
        {
            id: 'ins1',
            title: 'Opportunity: Liquidity Optimization',
            description: 'Your treasury is over-allocated in stable assets based on your risk profile.',
            type: 'opportunity',
            confidence: 0.88,
            timestamp: new Date(),
            actionable: true,
            action: 'Rebalance Vault'
        },
        {
            id: 'ins2',
            title: 'Governance Alert: Shard Proposal',
            description: 'A critical vote on protocol parameters requires your input within 48h.',
            type: 'pattern',
            confidence: 0.95,
            timestamp: new Date(Date.now() - 7200000),
            actionable: true,
            action: 'View Proposal'
        }
    ],
    suggestions: [
        {
            id: 'sugg1',
            text: 'Write about today\'s insights',
            context: 'hearth',
            priority: 0.9
        }
    ],
    isProcessing: false
};

class ConciergeEngine {
    state = $state<ConciergeState>(initialState);

    constructor() {
        if (browser) {
            const stored = loadFromStorage<Partial<ConciergeState>>('concierge', {});
            // Rehydrate dates
            if (stored.conversations) {
                stored.conversations = stored.conversations.map(c => ({
                    ...c,
                    timestamp: new Date(c.timestamp),
                    messages: c.messages.map(m => ({ ...m, timestamp: new Date(m.timestamp) }))
                }));
            }
            if (stored.insights) {
                stored.insights = stored.insights.map(i => ({ ...i, timestamp: new Date(i.timestamp) }));
            }
            this.state = { ...initialState, ...stored };
        }
    }

    private persist() {
        if (browser) {
            saveToStorage('concierge', $state.snapshot(this.state));
        }
    }

    private generateUUID() {
        return browser && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2);
    }

    generateUserContext(
        sovereignStore: any,
        hearthStore: any,
        vaultStore: any,
        governanceStore: any
            // @ts-ignore
    ): UserContext {
        return {
            profile: sovereignStore.profile,
            resonance: hearthStore.totalResonance,
            activeStreak: hearthStore.streak,
            portfolioValue: vaultStore.totalValue,
            recentActivity: [...hearthStore.memories.slice(0, 3)],
            systemStatus: 'healthy',
            currentTime: new Date().toISOString()
        };
    }

    async sendMessage(content: string, userContext: UserContext) {
        const conversationId = this.state.currentConversationId;
        const conversationIndex = this.state.conversations.findIndex(c => c.id === conversationId);
        if (conversationIndex === -1) return;

        const userMessage: ConversationMessage = {
            id: this.generateUUID(),
            role: 'user',
            content,
            timestamp: new Date()
        };

        this.state.conversations[conversationIndex].messages.push(userMessage);
        this.state.conversations[conversationIndex].lastMessage = content;
        this.state.conversations[conversationIndex].timestamp = new Date();

        this.state.isProcessing = true;
        this.persist();

        const responseId = this.generateUUID();
        const assistantMessage: ConversationMessage = {
            id: responseId,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            streaming: true
        };

        this.state.conversations[conversationIndex].messages.push(assistantMessage);

        try {
            const conversation = this.state.conversations[conversationIndex];
            const personality = this.getCurrentPersonality().description;

            let fullResponse = '';
            await llmService.sendMessage(
                userContext,
                conversation,
                content,
                personality,
                (chunk) => {
                    fullResponse += chunk.content;
                    const cIdx = this.state.conversations.findIndex(c => c.id === conversationId);
                    if (cIdx !== -1) {
                        const mIdx = this.state.conversations[cIdx].messages.findIndex(m => m.id === responseId);
                        if (mIdx !== -1) {
                            this.state.conversations[cIdx].messages[mIdx].content = fullResponse;
                        }
                    }
                }
            );

            const cIdxFinal = this.state.conversations.findIndex(c => c.id === conversationId);
            if (cIdxFinal !== -1) {
                const mIdxFinal = this.state.conversations[cIdxFinal].messages.findIndex(m => m.id === responseId);
                if (mIdxFinal !== -1) {
                    this.state.conversations[cIdxFinal].messages[mIdxFinal].streaming = false;
                }
            }

            const newInsight: Insight = {
                id: this.generateUUID(),
                type: 'conversation',
                title: 'New conversation completed',
                description: `You discussed "${content.substring(0, 50)}${content.length > 50 ? '...' : ''}"`,
                confidence: 0.8,
                timestamp: new Date(),
                actionable: false
            };

            this.state.insights = [newInsight, ...this.state.insights].slice(0, 10);
            this.state.isProcessing = false;
            this.persist();

        } catch (error) {
            console.error('LLM API error:', error);
            const cIdxErr = this.state.conversations.findIndex(c => c.id === conversationId);
            if (cIdxErr !== -1) {
                const mIdxErr = this.state.conversations[cIdxErr].messages.findIndex(m => m.id === responseId);
                if (mIdxErr !== -1) {
                    this.state.conversations[cIdxErr].messages[mIdxErr].content = `I apologize, but I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}.`;
                    this.state.conversations[cIdxErr].messages[mIdxErr].streaming = false;
                    this.state.conversations[cIdxErr].messages[mIdxErr].isError = true;
                }
            }
            this.state.isProcessing = false;
            this.persist();
        }
    }

    startNewConversation() {
        const newConversation: Conversation = {
            id: this.generateUUID(),
            title: 'New Integration Context',
            lastMessage: 'Initializing new thread...',
            timestamp: new Date(),
            messages: [{
                id: this.generateUUID(),
                role: 'assistant',
                content: 'System fully initialized. Operating under Sovereign ruleset.',
                timestamp: new Date()
            }, {
                id: this.generateUUID(),
                role: 'assistant',
                content: `I am ready. Tell me what needs orchestrating.`,
                timestamp: new Date()
            }],
            context: {}
        };
        this.state.conversations.unshift(newConversation);
        this.state.currentConversationId = newConversation.id;
        this.persist();
    }

    switchConversation(id: string) {
        if (this.state.conversations.find(c => c.id === id)) {
            this.state.currentConversationId = id;
            this.persist();
        }
    }

    setPersonality(personalityId: string) {
        if (CONCIERGE_PERSONALITIES[personalityId.toUpperCase() as keyof typeof CONCIERGE_PERSONALITIES]) {
            this.state.personality = personalityId;
            this.persist();
        }
    }

    getCurrentPersonality(): Personality {
        return (CONCIERGE_PERSONALITIES as any)[this.state.personality.toUpperCase()] || CONCIERGE_PERSONALITIES.WISE;
    }

    getSuggestionsByContext(context: string): any[] {
        return this.state.suggestions
            .filter(s => s.context === context)
            .sort((a, b) => b.priority - a.priority);
    }
}

export const conciergeStore = new ConciergeEngine();
