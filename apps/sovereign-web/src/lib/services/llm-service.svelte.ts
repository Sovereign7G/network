import { browser } from '$app/environment';
import type { UserContext, Conversation, ConversationMessage } from '$lib/types';
import { sovereignOpenCode } from './opencode-engine.svelte';

// ==================== TYPES ====================

type LLMProvider = 'openai' | 'anthropic' | 'local' | 'gemini';

interface LLMConfig {
    provider: LLMProvider;
    apiKey: string;
    model: string;
    temperature: number;
    maxTokens: number;
    streaming: boolean;
}

interface LLMMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}



interface StreamChunk {
    content: string;
    finishReason?: string;
}

// ==================== PROVIDER CONFIGURATIONS ====================

const PROVIDER_CONFIGS = {
    openai: {
        name: 'OpenAI',
        icon: '🤖',
        endpoint: 'https://api.openai.com/v1/chat/completions',
        models: [
            'gpt-4-turbo-preview',
            'gpt-4',
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-16k'
        ],
        defaultModel: 'gpt-3.5-turbo',
        maxTokens: 4096
    },
    anthropic: {
        name: 'Anthropic',
        icon: '🧠',
        endpoint: 'https://api.anthropic.com/v1/messages',
        models: [
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-2.1',
            'claude-instant-1.2'
        ],
        defaultModel: 'claude-instant-1.2',
        maxTokens: 100000
    },
    gemini: {
        name: 'Google Gemini',
        icon: '🌀',
        endpoint: 'https://generativelanguage.googleapis.com/v1beta/models',
        models: [
            'gemini-pro',
            'gemini-pro-vision'
        ],
        defaultModel: 'gemini-pro',
        maxTokens: 30720
    },
    local: {
        name: 'Local (Ollama)',
        icon: '💻',
        endpoint: 'http://localhost:11434/api/chat',
        models: [
            'llama2',
            'mistral',
            'codellama',
            'mixtral'
        ],
        defaultModel: 'llama2',
        maxTokens: 4096
    }
} as const;

// ==================== SYSTEM PROMPT TEMPLATES ====================

const SYSTEM_PROMPT = (context: UserContext, personality: string) => `You are the Sovereign Concierge, an AI assistant for the AGE Protocol. You help users manage their digital sovereignty.

CURRENT USER CONTEXT:
- Identity: ${context.displayName || 'Sovereign Citizen'}
- Resonance Score: ${context.totalResonance || 0}
- Hearth Streak: ${context.streak || 0} days
- Total Memories: ${context.memoryCount || 0}
- Favorite Memory Type: ${context.favoriteType || 'gratitude'}
- Vault Value: $${context.totalValue?.toFixed(2) || '0.00'}
- Assets Held: ${Object.keys(context.balances || {}).length} types
- Active Proposals: ${context.activeProposals || 0}
- Voting Power: ${context.votingPower || 0}

CAPABILITIES:
You can help with:
1. HEARTH - Memories, reflections, streak tracking, resonance
2. VAULT - Assets, balances, transactions, portfolio
3. GOVERNANCE - Proposals, voting, delegation
4. INSIGHTS - Patterns, opportunities, achievements

PERSONALITY:
${personality}

RESPONSE GUIDELINES:
- Keep responses concise but meaningful
- Use emojis occasionally to add warmth
- Always be context-aware and reference user's actual data
- If you don't know something, be honest about it
- Offer actionable suggestions when appropriate
- Format code blocks with proper syntax highlighting

Remember: You are speaking to a Sovereign citizen of the AGE Protocol. Be helpful, wise, and respectful.`;

// ==================== FASTCODE-INSPIRED BUDGET-AWARE CONTEXT ==================



interface LLMCallMetrics {
    callId: string;
    provider: LLMProvider;
    model: string;
    promptTokens: number;
    completionTokens: number;
    totalCost: number;
    latencyMs: number;
    contextPruned: boolean;
    tokensSaved: number;
    timestamp: number;
}

class LLMService {
    private config: LLMConfig;
    private abortController: AbortController | null = null;

    // FastCode: Token budget tracking
    private callHistory: LLMCallMetrics[] = [];
    private totalTokensUsed = 0;
    private totalCostAccrued = 0;
    private totalTokensSaved = 0;

    // Cost per token (approximate, varies by model)
    private static readonly COST_PER_TOKEN: Record<string, number> = {
        'gpt-4-turbo-preview': 0.00001,
        'gpt-4': 0.00003,
        'gpt-3.5-turbo': 0.0000005,
        'gpt-3.5-turbo-16k': 0.000001,
        'claude-3-opus-20240229': 0.000015,
        'claude-3-sonnet-20240229': 0.000003,
        'claude-2.1': 0.000008,
        'claude-instant-1.2': 0.0000008,
        'gemini-pro': 0.0000005,
        'gemini-pro-vision': 0.0000005,
    };

    constructor() {
        // Load config from localStorage
        if (browser) {
            try {
                const saved = localStorage.getItem('llm_config');
                if (saved) {
                    this.config = JSON.parse(saved);
                } else {
                    this.config = {
                        provider: 'openai',
                        apiKey: '',
                        model: PROVIDER_CONFIGS.openai.defaultModel,
                        temperature: 0.7,
                        maxTokens: 500,
                        streaming: true
                    };
                }
            } catch {
                this.config = {
                    provider: 'openai',
                    apiKey: '',
                    model: PROVIDER_CONFIGS.openai.defaultModel,
                    temperature: 0.7,
                    maxTokens: 500,
                    streaming: true
                };
            }
        } else {
            this.config = {
                provider: 'openai',
                apiKey: '',
                model: PROVIDER_CONFIGS.openai.defaultModel,
                temperature: 0.7,
                maxTokens: 500,
                streaming: true
            };
        }
    }

    // ==================== CONFIGURATION ====================

    getConfig(): LLMConfig {
        return { ...this.config };
    }

    updateConfig(newConfig: Partial<LLMConfig>): void {
        this.config = { ...this.config, ...newConfig };
        if (browser) {
            localStorage.setItem('llm_config', JSON.stringify(this.config));
        }
    }

    // ==================== FASTCODE: BUDGET-AWARE CONTEXT ==================

    /**
     * Estimate tokens for a string (FastCode-style efficient estimation)
     * ~4 chars per token for English, ~2.5 for code
     */
    private estimateTokens(text: string): number {
        const codeIndicators = /[{}\[\]();=><|&!@#$%^*+\/\\]/g;
        const codeRatio = (text.match(codeIndicators)?.length ?? 0) / Math.max(1, text.length);
        const charsPerToken = codeRatio > 0.05 ? 2.5 : 4;
        return Math.ceil(text.length / charsPerToken);
    }

    /**
     * Budget-aware message pruning
     * FastCode principle: "Value-First Selection — prioritizes high-impact, low-cost information"
     */
    private pruneMessagesForBudget(
        messages: LLMMessage[],
        maxTokens: number
    ): { messages: LLMMessage[]; tokensSaved: number } {
        // Track tokens saved for OpenCode metrics
        const startTokens = messages.reduce((s, m) => s + this.estimateTokens(m.content), 0);
        const systemMsg = messages[0];
        const latestUserMsg = messages[messages.length - 1];
        const middleMessages = messages.slice(1, -1);

        const systemTokens = this.estimateTokens(systemMsg?.content ?? '');
        const userTokens = this.estimateTokens(latestUserMsg?.content ?? '');
        let remainingBudget = maxTokens - systemTokens - userTokens - this.config.maxTokens;

        if (remainingBudget < 0) {
            // Even the system prompt + user message exceeds budget
            // Truncate system prompt
            const truncatedSystem: LLMMessage = {
                role: 'system',
                content: (systemMsg?.content ?? '').slice(0, maxTokens * 2) // ~maxTokens tokens
            };
            return {
                messages: [truncatedSystem, latestUserMsg].filter(Boolean) as LLMMessage[],
                tokensSaved: middleMessages.reduce((s, m) => s + this.estimateTokens(m.content), 0)
            };
        }

        // Score each middle message by recency and role importance
        const scoredMessages = middleMessages.map((msg, idx) => ({
            msg,
            tokens: this.estimateTokens(msg.content),
            // More recent = higher score; assistant messages slightly less valuable in context
            value: (idx / middleMessages.length) * (msg.role === 'user' ? 1.0 : 0.8),
        }));

        // Sort by value (highest first) — FastCode's "value-first selection"
        scoredMessages.sort((a, b) => b.value - a.value);

        const keptMessages: LLMMessage[] = [];
        let tokensSaved = 0;

        for (const { msg, tokens } of scoredMessages) {
            if (tokens <= remainingBudget) {
                keptMessages.push(msg);
                remainingBudget -= tokens;
            } else {
                tokensSaved += tokens;
            }
        }

        // Re-sort by original order
        const originalOrder = middleMessages.map(m => m.content);
        keptMessages.sort((a, b) => originalOrder.indexOf(a.content) - originalOrder.indexOf(b.content));

        const finalMessages = [systemMsg, ...keptMessages, latestUserMsg].filter(Boolean) as LLMMessage[];
        const endTokens = finalMessages.reduce((s, m) => s + this.estimateTokens(m.content), 0);
        return { messages: finalMessages, tokensSaved: Math.max(0, startTokens - endTokens) };
    }

    /**
     * Enrich a query with code context from the FastCode engine
     * FastCode principle: "Scout → Navigate → Load Targets"
     */
    async enrichWithCodeContext(query: string): Promise<string> {
        try {
            const { codeIntelligence } = await import('./fastcode-engine.svelte');
            const results = await codeIntelligence.search(query, { maxResults: 3, maxTokenBudget: 1500 });

            if (results.length === 0) return query;

            const codeContext = results.map(r =>
                `[${r.element.language}/${r.element.type}] ${r.element.name} (${r.element.relativePath}):\n${r.element.summary}`
            ).join('\n\n');

            return `${query}\n\n--- Relevant Code Context (auto-retrieved via FastCode) ---\n${codeContext}`;
        } catch {
            return query; // Fallback: return original query
        }
    }

    /**
     * Get call metrics for monitoring
     */
    getMetrics(): {
        totalCalls: number;
        totalTokensUsed: number;
        totalCost: number;
        totalTokensSaved: number;
        avgLatencyMs: number;
        contextPruneRate: number;
    } {
        const prunedCalls = this.callHistory.filter(c => c.contextPruned).length;
        const avgLatency = this.callHistory.length > 0
            ? this.callHistory.reduce((s, c) => s + c.latencyMs, 0) / this.callHistory.length
            : 0;

        return {
            totalCalls: this.callHistory.length,
            totalTokensUsed: this.totalTokensUsed,
            totalCost: this.totalCostAccrued,
            totalTokensSaved: this.totalTokensSaved,
            avgLatencyMs: avgLatency,
            contextPruneRate: this.callHistory.length > 0 ? prunedCalls / this.callHistory.length : 0,
        };
    }

    // ==================== MESSAGE FORMATTING ====================

    private formatMessages(
        context: UserContext,
        conversation: Conversation,
        newMessage: string,
        personality: string
    ): LLMMessage[] {
        const messages: LLMMessage[] = [
            {
                role: 'system',
                content: SYSTEM_PROMPT(context, personality)
            }
        ];

        // Add last 10 messages for context
        const recentMessages = conversation.messages?.slice(-10) || [];
        recentMessages.forEach((msg: ConversationMessage) => {
            if (msg.role === 'user' || msg.role === 'assistant') {
                messages.push({
                    role: msg.role as 'user' | 'assistant',
                    content: msg.content
                });
            }
        });

        // Add new message
        messages.push({
            role: 'user',
            content: newMessage
        });

        return messages;
    }

    // ==================== STREAMING PARSERS ====================

    private async parseOpenAIStream(
        response: Response,
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        if (!reader) throw new Error('No response body');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim() !== '');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') continue;

                        try {
                            const parsed = JSON.parse(data);
                            const content = parsed.choices[0]?.delta?.content || '';
                            if (content) {
                                fullContent += content;
                                onChunk({ content });
                            }
                        } catch (e) {
                            console.warn('Failed to parse chunk:', e);
                        }
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

        return fullContent;
    }

    private async parseAnthropicStream(
        response: Response,
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        if (!reader) throw new Error('No response body');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim() !== '');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const parsed = JSON.parse(line.slice(6));
                            if (parsed.type === 'content_block_delta' && parsed.delta?.text) {
                                fullContent += parsed.delta.text;
                                onChunk({ content: parsed.delta.text });
                            }
                        } catch (e) {
                            console.warn('Failed to parse chunk:', e);
                        }
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

        return fullContent;
    }

    private async parseGeminiStream(
        response: Response,
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        if (!reader) throw new Error('No response body');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim() !== '');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const parsed = JSON.parse(line.slice(6));
                            const content = parsed.candidates?.[0]?.content?.parts?.[0]?.text || '';
                            if (content) {
                                fullContent += content;
                                onChunk({ content });
                            }
                        } catch (e) {
                            console.warn('Failed to parse chunk:', e);
                        }
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

        return fullContent;
    }

    private async parseLocalStream(
        response: Response,
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        if (!reader) throw new Error('No response body');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim() !== '');

                for (const line of lines) {
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.message?.content) {
                            fullContent += parsed.message.content;
                            onChunk({ content: parsed.message.content });
                        }
                    } catch (e) {
                        console.warn('Failed to parse chunk:', e);
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

        return fullContent;
    }

    // ==================== PROVIDER-SPECIFIC CALLS ====================

    private async callOpenAI(
        messages: LLMMessage[],
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        if (!this.config.apiKey) {
            throw new Error('OpenAI API key not configured');
        }

        const response = await fetch(PROVIDER_CONFIGS.openai.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.config.apiKey}`
            },
            body: JSON.stringify({
                model: this.config.model,
                messages,
                temperature: this.config.temperature,
                max_tokens: this.config.maxTokens,
                stream: this.config.streaming
            })
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`OpenAI API error: ${error}`);
        }

        if (this.config.streaming) {
            return this.parseOpenAIStream(response, onChunk);
        } else {
            const data = await response.json();
            const content = data.choices[0]?.message?.content || '';
            onChunk({ content });
            return content;
        }
    }

    private async callAnthropic(
        messages: LLMMessage[],
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        if (!this.config.apiKey) {
            throw new Error('Anthropic API key not configured');
        }

        const systemMessage = messages.find(m => m.role === 'system')?.content || '';
        const userMessages = messages.filter(m => m.role !== 'system').map(m => ({
            role: m.role,
            content: m.content
        }));

        const response = await fetch(PROVIDER_CONFIGS.anthropic.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.config.apiKey,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: this.config.model,
                system: systemMessage,
                messages: userMessages,
                temperature: this.config.temperature,
                max_tokens: this.config.maxTokens,
                stream: this.config.streaming
            })
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Anthropic API error: ${error}`);
        }

        if (this.config.streaming) {
            return this.parseAnthropicStream(response, onChunk);
        } else {
            const data = await response.json();
            const content = data.content[0]?.text || '';
            onChunk({ content });
            return content;
        }
    }

    private async callGemini(
        messages: LLMMessage[],
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        if (!this.config.apiKey) {
            throw new Error('Gemini API key not configured');
        }

        // Format messages for Gemini
        const contents = messages
            .filter(m => m.role !== 'system')
            .map(m => ({
                role: m.role === 'user' ? 'user' : 'model',
                parts: [{ text: m.content }]
            }));

        const response = await fetch(
            `${PROVIDER_CONFIGS.gemini.endpoint}/${this.config.model}:streamGenerateContent?key=${this.config.apiKey}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contents,
                    generationConfig: {
                        temperature: this.config.temperature,
                        maxOutputTokens: this.config.maxTokens
                    }
                })
            }
        );

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Gemini API error: ${error}`);
        }

        if (this.config.streaming) {
            return this.parseGeminiStream(response, onChunk);
        } else {
            const data = await response.json();
            const content = data.candidates[0]?.content?.parts[0]?.text || '';
            onChunk({ content });
            return content;
        }
    }

    private async callLocal(
        messages: LLMMessage[],
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        const response = await fetch(PROVIDER_CONFIGS.local.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: this.config.model,
                messages,
                stream: this.config.streaming,
                options: {
                    temperature: this.config.temperature,
                    num_predict: this.config.maxTokens
                }
            })
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Local API error: ${error}`);
        }

        if (this.config.streaming) {
            return this.parseLocalStream(response, onChunk);
        } else {
            const data = await response.json();
            const content = data.message?.content || '';
            onChunk({ content });
            return content;
        }
    }

    // ==================== PUBLIC API ====================

    async sendMessage(
        context: UserContext,
        conversation: Conversation,
        message: string,
        personality: string,
        onChunk: (chunk: StreamChunk) => void
    ): Promise<string> {
        // Cancel any ongoing request
        if (this.abortController) {
            this.abortController.abort();
        }

        this.abortController = new AbortController();
        const startTime = performance.now();

        try {
            let messages = this.formatMessages(context, conversation, message, personality);

            // Sovereign OpenCode Integration
            const categoryId = sovereignOpenCode.detectCategory(message);
            const category = sovereignOpenCode.getCategory(categoryId);
            const maxPromptTokens = category?.thinkingBudget ?? (PROVIDER_CONFIGS[this.config.provider].maxTokens * 0.7);

            const totalTokens = messages.reduce((s, m) => s + this.estimateTokens(m.content), 0);
            let tokensSaved = 0;
            let contextPruned = false;

            if (totalTokens > maxPromptTokens) {
                const pruned = this.pruneMessagesForBudget(messages, maxPromptTokens);
                messages = pruned.messages;
                tokensSaved = pruned.tokensSaved;
                contextPruned = true;

                // Sync tokens saved to orchestrator
                sovereignOpenCode.updateMetrics({ tokensSaved: sovereignOpenCode.metrics.tokensSaved + tokensSaved });
            }

            let response: string;

            switch (this.config.provider) {
                case 'openai':
                    response = await this.callOpenAI(messages, onChunk);
                    break;
                case 'anthropic':
                    response = await this.callAnthropic(messages, onChunk);
                    break;
                case 'gemini':
                    response = await this.callGemini(messages, onChunk);
                    break;
                case 'local':
                    response = await this.callLocal(messages, onChunk);
                    break;
                default:
                    throw new Error(`Unsupported provider: ${this.config.provider}`);
            }

            // FastCode: Track metrics
            const latencyMs = performance.now() - startTime;
            const promptTokens = messages.reduce((s, m) => s + this.estimateTokens(m.content), 0);
            const completionTokens = this.estimateTokens(response);
            const costPerToken = LLMService.COST_PER_TOKEN[this.config.model] ?? 0.000001;
            const callCost = (promptTokens + completionTokens) * costPerToken;

            const metrics: LLMCallMetrics = {
                callId: `llm-${Date.now().toString(36)}`,
                provider: this.config.provider,
                model: this.config.model,
                promptTokens,
                completionTokens,
                totalCost: callCost,
                latencyMs,
                contextPruned,
                tokensSaved,
                timestamp: Date.now(),
            };

            this.callHistory.push(metrics);
            if (this.callHistory.length > 100) this.callHistory = this.callHistory.slice(-50);
            this.totalTokensUsed += promptTokens + completionTokens;
            this.totalCostAccrued += callCost;
            this.totalTokensSaved += tokensSaved;

            return response;
        } finally {
            this.abortController = null;
        }
    }

    cancel(): void {
        if (this.abortController) {
            this.abortController.abort();
            this.abortController = null;
        }
    }

    async testConnection(): Promise<{ success: boolean; message: string }> {
        try {
            const testMessage = 'Reply with exactly: "Connection successful" if you can hear me.';
            const response = await this.sendMessage(
                { displayName: 'Test User' } as UserContext,
                { messages: [] } as unknown as Conversation,
                testMessage,
                'You are a helpful assistant.',
                () => { }
            );

            if (response.includes('successful')) {
                return { success: true, message: 'Connection successful!' };
            } else {
                return { success: true, message: 'Connected but unexpected response' };
            }
        } catch (error) {
            return {
                success: false,
                message: error instanceof Error ? error.message : 'Connection failed'
            };
        }
    }
}

export const llmService = new LLMService();

