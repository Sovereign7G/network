/**
 * 🏛️ UNIVERSAL SOVEREIGN WORKER
 * Inspired by Cloudflare Vinext and Agents.
 * This entry point consolidates protocol logic, agent execution, and asset serving.
 */
import { SophiaAgent, type AgentMessage } from '@age-protocol/agents-sdk';

// Ambient types for Cloudflare environment if not globally defined
declare global {
    interface DurableObjectState {
        storage: DurableObjectStorage;
        blockCollision<T>(closure: () => Promise<T>): Promise<T>;
    }
    interface DurableObjectStorage {
        get<T>(key: string): Promise<T | undefined>;
        put<T>(key: string, value: T): Promise<void>;
    }
    interface DurableObjectNamespace {
        idFromName(name: string): DurableObjectId;
        get(id: DurableObjectId): DurableObjectStub;
    }
    interface DurableObjectId { }
    interface DurableObjectStub {
        fetch(request: Request): Promise<Response>;
    }
}

interface Env {
    // Cloudflare Bindings
    AI: any;
    SOPHIA_STORAGE: DurableObjectNamespace;
}

/**
 * 🧠 SOPHIA AGENT DURABLE OBJECT
 * Maintains stateful persistence for AI Forge interactions.
 */
export class SophiaAgentDO {
    private agent: SophiaAgent;
    private state: DurableObjectState;

    constructor(state: DurableObjectState, _env: Env) {
        this.state = state;
        this.agent = new SophiaAgent('SOPHIA-DO-01');

        // Restore history from storage on instantiation
        this.state.blockCollision(async () => {
            const savedHistory = await this.state.storage.get<AgentMessage[]>('history');
            if (savedHistory) {
                // @ts-ignore - Accessing protected for restoration
                this.agent.history = savedHistory;
            }
        });

        // Auto-save history on every state update
        this.agent.on('stateUpdate', async (agentState: any) => {
            await this.state.storage.put('history', agentState.history);
        });
    }

    async fetch(request: Request): Promise<Response> {
        const url = new URL(request.url);

        if (url.pathname === '/interact' && request.method === 'POST') {
            const { guidance } = await request.json() as { guidance: string };
            await this.agent.onMessage(guidance);
            return new Response(JSON.stringify({
                status: 'processed',
                history: this.agent.getState().history
            }), { headers: { 'Content-Type': 'application/json' } });
        }

        if (url.pathname === '/history') {
            return new Response(JSON.stringify(this.agent.getState().history), {
                headers: { 'Content-Type': 'application/json' }
            });
        }

        return new Response("Sophia Agent DO Online", { status: 200 });
    }
}

export default {
    async fetch(request: Request, env: Env): Promise<Response> {
        const url = new URL(request.url);

        // 1. Handle Agent RPC (Durable Object Routing)
        if (url.pathname.startsWith('/agent/sophia')) {
            const id = env.SOPHIA_STORAGE.idFromName('global-sophia');
            const obj = env.SOPHIA_STORAGE.get(id);

            // Rewrite path for DO internal routing
            const doPath = url.pathname.replace('/agent/sophia', '');
            const doUrl = new URL(doPath, 'http://agent.local');

            return obj.fetch(new Request(doUrl.toString(), request));
        }

        // 2. Handle API Routes
        if (url.pathname.startsWith('/api')) {
            return new Response(JSON.stringify({
                status: "AGE Protocol Intelligence Online",
                environment: "Universal_Worker_v1"
            }), {
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });
        }

        // 3. Asset Serving / Fallback
        return new Response("AGE Sovereign Dashboard (Universal Worker)", {
            headers: { 'Content-Type': 'text/html' }
        });
    }
};
