
// 🚀 SOVEREIGN EDGE SCALER — PROACTIVE RESOURCE MANIFOLD
// ═══════════════════════════════════════════════════════════════════════════════
// Inspired by InfoQ's "Proactive Autoscaling for Edge Applications in Kubernetes"
// Incorporating Sovereign Calculus Governance (Extrema & Concavity Analysis).
// ═══════════════════════════════════════════════════════════════════════════════

type EdgeNodeStatus = 'healthy' | 'starting' | 'scaling_down' | 'exhausted';

interface EdgeReplica {
    id: string;
    region: string;
    status: EdgeNodeStatus;
    cpuUsage: number;
    latencyP95: number;
    uptime: number;
    startupCompletion: number; // 0 to 100
}

interface ScalerMetrics {
    activeReplicas: number;
    targetReplicas: number;
    avgLatencyMs: number;
    cpuHeadroom: number;
    predictionAccuracy: number;
    uptime: number;
    concavity: 'up' | 'down' | 'flat';
}

interface ScalingEvent {
    timestamp: number;
    type: 'SCALE_UP' | 'SCALE_DOWN';
    reason: string;
    signalValue: number;
}

// ─── INITIAL SYSTEM STATE ────────────────────────────────────────────────────

const INITIAL_REPLICAS: EdgeReplica[] = [
    {
        id: 'edge-tokyo-01',
        region: 'JP-EAST',
        status: 'healthy',
        cpuUsage: 42,
        latencyP95: 12.5,
        uptime: 86400,
        startupCompletion: 100
    },
    {
        id: 'edge-tokyo-02',
        region: 'JP-EAST',
        status: 'healthy',
        cpuUsage: 38,
        latencyP95: 14.1,
        uptime: 72000,
        startupCompletion: 100
    }
];

// ─── ENGINE IMPLEMENTATION ───────────────────────────────────────────────────

class SovereignEdgeScaler {
    private replicas = $state<EdgeReplica[]>([]);
    private events = $state<ScalingEvent[]>([]);
    private loadHistory = $state<number[]>([]);
    private _metrics = $state<ScalerMetrics>({
        activeReplicas: 0,
        targetReplicas: 2,
        avgLatencyMs: 13.3,
        cpuHeadroom: 62,
        predictionAccuracy: 94.5,
        uptime: Date.now(),
        concavity: 'flat'
    });

    private cooldownActive = false;
    private startupTimeMs = 3000;

    constructor() {
        this.replicas = [...INITIAL_REPLICAS];
        this.updateMetrics();
    }

    // ═══ SOVEREIGN CALCULUS GOVERNANCE ═══════════════════════════════════════

    /**
     * Inflection Point Detection (Second Derivative)
     * Detects if the rate of load increase is itself increasing (Concave Up).
     */
    private analyzeConcavity(): 'up' | 'down' | 'flat' {
        if (this.loadHistory.length < 3) return 'flat';

        const h = this.loadHistory;
        const last = h[h.length - 1]!;
        const prev = h[h.length - 2]!;
        const prev2 = h[h.length - 3]!;

        const velocity1 = last - prev;
        const velocity2 = prev - prev2;
        const acceleration = velocity1 - velocity2;

        if (acceleration > 0.5) return 'up';
        if (acceleration < -0.5) return 'down';
        return 'flat';
    }

    // ═══ SCALING LOGIC ═══════════════════════════════════════════════════════

    get allReplicas(): EdgeReplica[] { return this.replicas; }
    get allEvents(): ScalingEvent[] { return this.events; }

    proactiveCheck() {
        if (this.cooldownActive) return;

        const healthyNodes = this.replicas.filter(r => r.status === 'healthy');
        if (healthyNodes.length === 0) return;

        const avgLatency = healthyNodes.reduce((acc, r) => acc + r.latencyP95, 0) / healthyNodes.length;
        const avgCpu = healthyNodes.reduce((acc, r) => acc + r.cpuUsage, 0) / healthyNodes.length;

        const concavity = this.analyzeConcavity();
        this._metrics.concavity = concavity;

        // Optimized Trigger: Absolute Extrema Defense
        // If concave up (accelerating), scale up sooner (70% instead of 80%)
        const threshold = concavity === 'up' ? 70 : 80;

        if (avgLatency > 25 || avgCpu > threshold) {
            const reason = concavity === 'up'
                ? `Preemptive Inflection Response (Accelerating Load)`
                : `Proactive SLO Breach Prevention (Load: ${avgCpu.toFixed(1)}%)`;
            this.scaleUp(reason);
        } else if (avgCpu < 30 && this.replicas.length > 2 && concavity !== 'up') {
            this.scaleDown(`Efficiency Optimization (Low Load: ${avgCpu.toFixed(1)}%)`);
        }
    }

    private scaleUp(reason: string) {
        const id = `edge-${Math.random().toString(36).slice(2, 6)}`;
        const newReplica: EdgeReplica = {
            id,
            region: 'JP-CENTRAL',
            status: 'starting',
            cpuUsage: 0,
            latencyP95: 0,
            uptime: 0,
            startupCompletion: 0
        };

        this.replicas.push(newReplica);
        this.events.unshift({ timestamp: Date.now(), type: 'SCALE_UP', reason, signalValue: 0 });
        this.cooldown(5000);

        const interval = setInterval(() => {
            newReplica.startupCompletion += 10;
            if (newReplica.startupCompletion >= 100) {
                newReplica.status = 'healthy';
                newReplica.cpuUsage = 20 + Math.random() * 20;
                newReplica.latencyP95 = 10 + Math.random() * 5;
                clearInterval(interval);
            }
        }, this.startupTimeMs / 10);
    }

    private scaleDown(reason: string) {
        const target = this.replicas.find(r => r.status === 'healthy');
        if (!target) return;

        target.status = 'scaling_down';
        this.events.unshift({ timestamp: Date.now(), type: 'SCALE_DOWN', reason, signalValue: 0 });
        this.cooldown(5000);

        setTimeout(() => {
            this.replicas = this.replicas.filter(r => r.id !== target.id);
        }, 2000);
    }

    private cooldown(ms: number) {
        this.cooldownActive = true;
        setTimeout(() => this.cooldownActive = false, ms);
    }

    // ═══ ANALYTICS & SIMULATION ══════════════════════════════════════════════

    /**
     * Called by SimulationEngine on each 3s tick.
     * Replaces the orphan setInterval — all timed state flows through the heartbeat.
     */
    tick() {
        this.replicas.forEach(r => {
            if (r.status === 'healthy') {
                r.cpuUsage = Math.max(10, Math.min(95, r.cpuUsage + (Math.random() * 12 - 5)));
                r.latencyP95 = Math.max(8, Math.min(50, r.latencyP95 + (Math.random() * 4 - 2)));
            }
        });

        // Record load for global calculus analysis
        const healthyNodes = this.replicas.filter(r => r.status === 'healthy');
        const avgLoad = healthyNodes.length > 0
            ? healthyNodes.reduce((acc, r) => acc + r.cpuUsage, 0) / healthyNodes.length
            : 0;

        this.loadHistory.push(avgLoad);
        if (this.loadHistory.length > 10) this.loadHistory.shift();

        this.updateMetrics();
        this.proactiveCheck();
    }

    private updateMetrics() {
        const healthy = this.replicas.filter(r => r.status === 'healthy');
        if (healthy.length === 0) return;

        this._metrics.activeReplicas = healthy.length;
        this._metrics.avgLatencyMs = healthy.reduce((acc, r) => acc + r.latencyP95, 0) / healthy.length;
        this._metrics.cpuHeadroom = 100 - (healthy.reduce((acc, r) => acc + r.cpuUsage, 0) / healthy.length);

        if (this.events.length > 20) this.events.pop();
    }

    get metrics() { return this._metrics; }
    get stats() {
        return {
            nodes: this.replicas.length,
            headroom: this._metrics.cpuHeadroom.toFixed(0) + '%',
            latency: this._metrics.avgLatencyMs.toFixed(1) + 'ms',
            accuracy: this._metrics.predictionAccuracy + '%',
            concavity: this._metrics.concavity
        };
    }
}

export const sovereignEdgeScaler = new SovereignEdgeScaler();
