import { SophiaAgent, type AgentMessage, type AgentStatus } from '@age-protocol/agents-sdk';

/**
 * 🏛️ AGENT SERVICE (Svelte Context)
 * Bridges the stateful Sovereign Agent to the Svelte reactive UI.
 */
class AgentService {
    public sophia = $state<{
        status: AgentStatus;
        history: AgentMessage[];
        lastStreamingDelta: string;
    }>({
        status: 'idle',
        history: [],
        lastStreamingDelta: ''
    });

    private agent: SophiaAgent;

    constructor() {
        this.agent = new SophiaAgent('SOPHIA-01');

        this.agent.on('statusChange', (status: AgentStatus) => {
            this.sophia.status = status;
            if (status === 'thinking') {
                this.sophia.lastStreamingDelta = '';
            }
        });

        this.agent.on('delta', (delta: string) => {
            this.sophia.lastStreamingDelta += delta;
        });

        this.agent.on('stateUpdate', (state: any) => {
            this.sophia.history = state.history;
        });
    }

    async interact(guidance: string) {
        await this.agent.onMessage(guidance);
    }
}

            // @ts-ignore
const agentService = new AgentService();
