import type { CausalEvent, CausalEventType } from '../types/causal.types';

class CausalLogService {
    private events = $state<CausalEvent[]>([]);
    private listeners = new Map<string, Set<(event: CausalEvent) => void>>();

    public recordEvent<T>(
        type: CausalEventType,
        actor: string,
        target: string,
        payload: T,
        previous?: string
    ): CausalEvent<T> {
        const id = Math.random().toString(36).substring(7).toUpperCase();
        const event: CausalEvent<T> = {
            id,
            type,
            timestamp: Date.now(),
            actor,
            target,
            payload,
            previous
        };

        this.events = [event, ...this.events].slice(0, 10000);
        this.notifyListeners(event);

        return event;
    }

    public getEventsForActor(actor: string, limit: number = 100): CausalEvent[] {
        return this.events
            .filter(e => e.actor === actor)
            .slice(0, limit);
    }

    public getEventsForTarget(target: string, limit: number = 100): CausalEvent[] {
        return this.events
            .filter(e => e.target === target)
            .slice(0, limit);
    }

    public getCausalChain(eventId: string): CausalEvent[] {
        const chain: CausalEvent[] = [];
        let current = this.events.find(e => e.id === eventId);

        while (current) {
            chain.unshift(current);
            current = this.events.find(e => e.id === current?.previous);
        }

        return chain;
    }

    private notifyListeners(event: CausalEvent): void {
        const typeListeners = this.listeners.get(event.type);
        if (typeListeners) {
            typeListeners.forEach(listener => listener(event));
        }
    }

    public on(type: CausalEventType, listener: (event: CausalEvent) => void): () => void {
        if (!this.listeners.has(type)) {
            this.listeners.set(type, new Set());
        }

        this.listeners.get(type)!.add(listener);

        return () => {
            this.listeners.get(type)?.delete(listener);
        };
    }
}

            // @ts-ignore
const causalLogService = new CausalLogService();
