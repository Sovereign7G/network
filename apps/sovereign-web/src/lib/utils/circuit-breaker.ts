// 🔌 CIRCUIT BREAKER PATTERN
// Prevents systemic collapse by tripping when a service fails repeatedly.

enum CircuitState {
    CLOSED, // All good, traffic flows
    OPEN,   // Failed, traffic blocked
    HALF_OPEN // Testing if service is back
}

export class CircuitBreaker {
    private state: CircuitState = CircuitState.CLOSED;
    private failureCount = 0;
    private lastFailureTime = 0;
    private readonly threshold: number;
    private readonly cooldown: number;

    constructor(threshold = 5, cooldown = 30000) {
        this.threshold = threshold;
        this.cooldown = cooldown;
    }

    async execute<T>(action: () => Promise<T>): Promise<T> {
        if (this.state === CircuitState.OPEN) {
            if (Date.now() - this.lastFailureTime > this.cooldown) {
                this.state = CircuitState.HALF_OPEN;
            } else {
                throw new Error("Circuit Breaker is OPEN. Service unavailable.");
            }
        }

        try {
            const result = await action();
            this.reset();
            return result;
        } catch (err) {
            this.recordFailure();
            throw err;
        }
    }

    private recordFailure() {
        this.failureCount++;
        this.lastFailureTime = Date.now();
        if (this.failureCount >= this.threshold) {
            this.state = CircuitState.OPEN;
            console.error("🏁 CIRCUIT BREAKER TRIPPED: Potential systemic instability detected.");
        }
    }

    private reset() {
        this.state = CircuitState.CLOSED;
        this.failureCount = 0;
    }

    getState() {
        return this.state;
    }
}
