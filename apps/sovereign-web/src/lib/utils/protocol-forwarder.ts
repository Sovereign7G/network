/**
 * Objective‑C inspired safe‑call helper.
 * If `fn` is undefined or throws, returns `fallback`.
 */
function safeCall<T>(fn: (() => T) | undefined, fallback: T): T {
    try {
        return fn ? fn() : fallback;
    } catch {
        return fallback;
    }
}

/**
 * Simple protocol forwarder – mimics Objective‑C message forwarding.
 * Allows registration of handlers for legacy/foreign protocols.
 */
class ProtocolForwarder {
    private handlers: Record<string, (blockId: string, args: any) => any> = {};

    register(name: string, handler: (blockId: string, args: any) => any) {
        this.handlers[name] = handler;
    }

    forward(name: string, blockId: string, args: any) {
        const handler = this.handlers[name];
        return safeCall(() => handler?.(blockId, args), undefined);
    }
}

// Export a singleton forwarder for the app to use.
const forwarder = new ProtocolForwarder();
