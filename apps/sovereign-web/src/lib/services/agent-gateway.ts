// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN AGENT GATEWAY
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]: agent-request, sovereign-policy-engine, ephemeral-runner, otel-tracer
// [OUT]: AgentGateway, gatewayInstance, AgentGatewayEvent
// [POS]: Least-Privilege AI Agent Gateway for AGE Protocol.
//        Applies lessons from InfoQ (Debnath 2026): Policy-as-Code, Least Privilege,
//        Ephemeral Execution, Observability by Default, Versioning & Auditability.
// Protocol: When updating me, sync this header + parent folder's .folder.md
// ═══════════════════════════════════════════════════════════════════════════════

import { browser } from '$app/environment';
import type {
    AgentCapability, RiskTier, AgentTrust, AgentRequest,
    PolicyDecision, GatewayJob, GatewayTraceSpan, GatewayMetrics,
    AgentGatewayEvent, PolicyRule, PolicyContext
} from '../types/agent-gateway.types';
import { CAPABILITY_RISK_MAP } from '../types/agent-gateway.types';
import { BUILTIN_POLICIES } from './agent-gateway-registry';
import { auditEngine } from './audit-engine.svelte';



export { CAPABILITY_RISK_MAP };

// BUILT-IN POLICIES are now imported from ./agent-gateway-registry.ts

// BUILT-IN POLICIES are now imported from ./agent-gateway-registry.ts


// ─── UTILITY ─────────────────────────────────────────────────────────────────

function uuid(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
}

function sha256Hex(input: string): string {
    // Browser-native SHA-256 is async; for synchronous plan hashing, use a fast hash
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
        const ch = input.charCodeAt(i);
        hash = ((hash << 5) - hash + ch) | 0;
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
}

// ─── THE GATEWAY ─────────────────────────────────────────────────────────────

/**
 * 🏛️ SOVEREIGN AGENT GATEWAY
 *
 * The mediation layer between AI agents and AGE Protocol infrastructure.
 * No agent interacts with infrastructure directly.
 *
 * Flow: Discovery → Request → Validation → Policy → Execution → Observability
 *
 * Architectural invariant:
 *   "Trust in agents is not a belief — it is something you observe, measure, and enforce."
 */
class AgentGateway {
    // ── State ──
    private policies: PolicyRule[] = [...BUILTIN_POLICIES];
    private jobs: Map<string, GatewayJob> = new Map();
    private seenIdempotencyKeys: Set<string> = new Set();
    private eventLog: AgentGatewayEvent[] = [];
    private static readonly MAX_EVENT_LOG = 1000;
    private static readonly MAX_COMPLETED_JOBS = 200;
    private static readonly RATE_LIMIT_WINDOW_MS = 60_000;
    private static readonly RATE_LIMIT_MAX = 50;
    private _metrics: GatewayMetrics = {
        totalRequests: 0,
        totalApproved: 0,
        totalDenied: 0,
        totalExecuted: 0,
        totalFailed: 0,
        avgPolicyLatencyMs: 0,
        avgExecutionLatencyMs: 0,
        avgSandboxTeardownMs: 0,
        denialRate: 0,
        activeJobs: 0,
        sandboxesCreated: 0,
        sandboxesDestroyed: 0,
    };
    private policyLatencies: number[] = [];
    private executionLatencies: number[] = [];
    private sandboxTeardownLatencies: number[] = [];

    /** Per-agent request timestamps for sliding-window rate limiting. */
    private _agentRequestTimestamps: Map<string, number[]> = new Map();

    /** External context resolver — provided by the manifold. */
    private contextResolver: (() => PolicyContext) | null = null;

    /** Subscribers for real-time event streaming. */
    private subscribers: ((event: AgentGatewayEvent) => void)[] = [];

    constructor() {
        if (browser) {
        }
    }

    // ─── PHASE 1: DISCOVERY (MCP-style) ──────────────────────────────────────
    // Agents discover what they CAN do. They cannot invent or guess.

    /**
     * Returns the list of available capabilities with their schemas and risk tiers.
     * This is the MCP `tools/list` equivalent.
     */
    discoverCapabilities(actorTrust: AgentTrust): {
        capability: AgentCapability;
        riskTier: RiskTier;
        accessible: boolean;
        description: string;
    }[] {
        const MIN_TRUST_ORDER: AgentTrust[] = ['UNTRUSTED', 'REGISTERED', 'VERIFIED', 'SOVEREIGN'];
        const actorLevel = MIN_TRUST_ORDER.indexOf(actorTrust);

        return (Object.entries(CAPABILITY_RISK_MAP) as [AgentCapability, RiskTier][]).map(
            ([capability, riskTier]) => {
                const minTrustForTier: Record<RiskTier, number> = {
                    LOW: 0,
                    MEDIUM: 1,
                    HIGH: 2,
                    CRITICAL: 3,
                };
                const accessible = actorLevel >= minTrustForTier[riskTier];
                return {
                    capability,
                    riskTier,
                    accessible,
                    description: `${capability} [${riskTier}]`,
                };
            },
        );
    }

    // ─── PHASE 2: REQUEST & VALIDATION ───────────────────────────────────────

    /**
     * Submit an agent request. This is the MCP `tools/call` equivalent.
     * Returns a job handle — never executes inline.
     */
    async submitRequest(request: AgentRequest): Promise<{
        accepted: boolean;
        jobId?: string;
        denial?: PolicyDecision;
        requiresApproval?: boolean;
    }> {
        this._metrics.totalRequests++;

        const traceId = uuid();

        // 1. Schema Validation
        if (!this.validateSchema(request)) {
            this.emitEvent({
                eventId: uuid(),
                type: 'REQUEST_RECEIVED',
                payload: { requestId: request.requestId, valid: false },
                timestamp: Date.now(),
                traceId,
            });
            return { accepted: false, denial: { allowed: false, reason: 'Schema validation failed.', appliedRules: [], riskTier: 'LOW', requiresApproval: false, evaluatedAt: new Date().toISOString(), evaluationMs: 0 } };
        }

        // 2. Idempotency Check
        if (this.seenIdempotencyKeys.has(request.idempotencyKey)) {
            // Return existing job if found
            const existingJob = [...this.jobs.values()].find(j => j.request.idempotencyKey === request.idempotencyKey);
            if (existingJob) {
                return { accepted: true, jobId: existingJob.jobId };
            }
            return { accepted: false, denial: { allowed: false, reason: 'Duplicate idempotency key.', appliedRules: ['POL-IDEM-001'], riskTier: 'LOW', requiresApproval: false, evaluatedAt: new Date().toISOString(), evaluationMs: 0 } };
        }

        // 2b. Per-Agent Rate Limiting (sliding window)
        const agentId = request.actor.id;
        const now = Date.now();
        const agentTimestamps = this._agentRequestTimestamps.get(agentId) || [];
        const windowStart = now - AgentGateway.RATE_LIMIT_WINDOW_MS;
        const recentTimestamps = agentTimestamps.filter(t => t > windowStart);
        if (recentTimestamps.length >= AgentGateway.RATE_LIMIT_MAX) {
            this._metrics.totalDenied++;
            this._metrics.denialRate = this._metrics.totalDenied / this._metrics.totalRequests;
            return {
                accepted: false,
                denial: {
                    allowed: false,
                    reason: `Agent ${agentId.slice(0, 8)}… exceeded rate limit (${AgentGateway.RATE_LIMIT_MAX} req/${AgentGateway.RATE_LIMIT_WINDOW_MS / 1000}s).`,
                    appliedRules: ['POL-RATE-001'],
                    riskTier: 'LOW',
                    requiresApproval: false,
                    evaluatedAt: new Date().toISOString(),
                    evaluationMs: 0,
                },
            };
        }
        recentTimestamps.push(now);
        this._agentRequestTimestamps.set(agentId, recentTimestamps);

        this.emitEvent({
            eventId: uuid(),
            type: 'REQUEST_RECEIVED',
            payload: { requestId: request.requestId, capability: request.capability, actor: request.actor.id },
            timestamp: Date.now(),
            traceId,
        });

        // 3. Policy Evaluation
        const policyStart = performance.now();
        const decision = this.evaluatePolicy(request);
        const policyMs = performance.now() - policyStart;

        this.policyLatencies.push(policyMs);
        this._metrics.avgPolicyLatencyMs = this.policyLatencies.reduce((a, b) => a + b, 0) / this.policyLatencies.length;

        // SLO check: Policy decision < 100ms
        if (policyMs > 100) {
            this.emitEvent({
                eventId: uuid(),
                type: 'SLO_VIOLATION',
                payload: { slo: 'POLICY_DECISION_LATENCY', limit: 100, actual: Math.round(policyMs) },
                timestamp: Date.now(),
                traceId,
            });
        }

        this.emitEvent({
            eventId: uuid(),
            type: decision.allowed ? 'POLICY_EVALUATED' : 'POLICY_DENIED',
            payload: { decision, requestId: request.requestId },
            timestamp: Date.now(),
            traceId,
        });

        if (!decision.allowed) {
            this._metrics.totalDenied++;
            this._metrics.denialRate = this._metrics.totalDenied / this._metrics.totalRequests;
            return { accepted: false, denial: decision };
        }

        // Check if human approval is required
        if (decision.requiresApproval && !request.approvalToken) {
            this.emitEvent({
                eventId: uuid(),
                type: 'APPROVAL_REQUIRED',
                payload: { requestId: request.requestId, capability: request.capability },
                timestamp: Date.now(),
                traceId,
            });
            return { accepted: false, requiresApproval: true, denial: { ...decision, allowed: false, reason: 'Human approval required for this action.' } };
        }

        this._metrics.totalApproved++;

        // 4. Enqueue Job
        this.seenIdempotencyKeys.add(request.idempotencyKey);

        const job: GatewayJob = {
            jobId: uuid(),
            request,
            policy: decision,
            status: 'QUEUED',
            sandboxId: null,
            result: null,
            error: null,
            trace: [],
            createdAt: Date.now(),
            completedAt: null,
        };

        this.jobs.set(job.jobId, job);
        this._metrics.activeJobs++;

        this.emitEvent({
            eventId: uuid(),
            type: 'JOB_QUEUED',
            payload: { jobId: job.jobId, capability: request.capability },
            timestamp: Date.now(),
            traceId,
        });

        // 5. Execute asynchronously in sandbox
        this.executeInSandbox(job, traceId);

        return { accepted: true, jobId: job.jobId };
    }

    // ─── PHASE 3: POLICY EVALUATION ──────────────────────────────────────────

    private evaluatePolicy(request: AgentRequest): PolicyDecision {
        const startMs = performance.now();
        const audit = auditEngine.auditAction(request.capability, request.params);
        const context = this.getContext(audit);
        const appliedRules: string[] = [];

        let finalAllowed = true;
        let denyReason = '';

        // Sort by priority (higher first)
        const sortedPolicies = [...this.policies].sort((a, b) => b.priority - a.priority);

        for (const rule of sortedPolicies) {
            // Check if rule applies to this capability
            if (rule.capabilities !== '*' && !rule.capabilities.includes(request.capability)) {
                continue;
            }

            const result = rule.evaluate(request, context);
            appliedRules.push(`${rule.id}: ${result.allowed ? '✓' : '✗'} ${result.reason}`);

            if (!result.allowed) {
                finalAllowed = false;
                denyReason = result.reason;
                if (rule.isFinal) break; // Final rules halt evaluation immediately
            }
        }

        const riskTier = CAPABILITY_RISK_MAP[request.capability];
        const requiresApproval = riskTier === 'CRITICAL';

        return {
            allowed: finalAllowed,
            reason: finalAllowed ? 'All policy rules passed.' : denyReason,
            appliedRules,
            riskTier,
            requiresApproval,
            evaluatedAt: new Date().toISOString(),
            evaluationMs: Math.round(performance.now() - startMs),
        };
    }

    // ─── PHASE 4: EPHEMERAL SANDBOX EXECUTION ────────────────────────────────
    // Lesson: "Every action runs in a short-lived, isolated environment
    //          that is destroyed immediately after execution."

    private async executeInSandbox(job: GatewayJob, traceId: string) {
        const sandboxId = `sandbox-${uuid().slice(0, 8)}`;
        job.sandboxId = sandboxId;
        job.status = 'EXECUTING';

        this._metrics.sandboxesCreated++;

        const rootSpan = this.startSpan(job, 'gateway.execute', { sandboxId, capability: job.request.capability });

        this.emitEvent({
            eventId: uuid(),
            type: 'SANDBOX_CREATED',
            payload: { jobId: job.jobId, sandboxId },
            timestamp: Date.now(),
            traceId,
        });

        try {
            // Create isolated execution context — no shared mutable state
            const executionSpan = this.startSpan(job, 'sandbox.run', { sandboxId }, rootSpan.spanId);

            const execStart = performance.now();
            const result = await this.runCapability(job.request);
            const execMs = performance.now() - execStart;

            this.executionLatencies.push(execMs);
            this._metrics.avgExecutionLatencyMs =
                this.executionLatencies.reduce((a, b) => a + b, 0) / this.executionLatencies.length;

            this.endSpan(executionSpan, 'OK');

            job.result = result;
            job.status = 'COMPLETED';
            job.completedAt = Date.now();
            this._metrics.totalExecuted++;

            this.emitEvent({
                eventId: uuid(),
                type: 'EXECUTION_COMPLETED',
                payload: { jobId: job.jobId, sandboxId, elapsedMs: Math.round(execMs) },
                timestamp: Date.now(),
                traceId,
            });
        } catch (err: unknown) {
            const errorMsg = err instanceof Error ? err.message : String(err);
            job.error = errorMsg;
            job.status = 'FAILED';
            job.completedAt = Date.now();
            this._metrics.totalFailed++;

            this.emitEvent({
                eventId: uuid(),
                type: 'EXECUTION_FAILED',
                payload: { jobId: job.jobId, sandboxId, error: errorMsg },
                timestamp: Date.now(),
                traceId,
            });
        } finally {
            // MANDATORY TEARDOWN — always clean up, even on failure
            const teardownSpan = this.startSpan(job, 'sandbox.teardown', { sandboxId }, rootSpan.spanId);
            const teardownStart = performance.now();

            job.status = job.error ? 'FAILED' : 'COMPLETED';
            job.sandboxId = null; // Sandbox no longer exists

            const teardownMs = performance.now() - teardownStart;
            this.sandboxTeardownLatencies.push(teardownMs);
            this._metrics.avgSandboxTeardownMs =
                this.sandboxTeardownLatencies.reduce((a, b) => a + b, 0) / this.sandboxTeardownLatencies.length;
            this._metrics.sandboxesDestroyed++;
            this._metrics.activeJobs = Math.max(0, this._metrics.activeJobs - 1);

            this.endSpan(teardownSpan, 'OK');
            this.endSpan(rootSpan, job.error ? 'ERROR' : 'OK');

            this.emitEvent({
                eventId: uuid(),
                type: 'SANDBOX_DESTROYED',
                payload: { jobId: job.jobId, sandboxId, teardownMs: Math.round(teardownMs) },
                timestamp: Date.now(),
                traceId,
            });
        }
    }

    /**
     * Execute a capability in its isolated context.
     * Each capability handler is a pure function operating on its own data.
     */
    private async runCapability(request: AgentRequest): Promise<unknown> {
        // Simulate capability execution latency (replace with real handlers)
        const simulatedLatency = 50 + Math.random() * 200;
        await new Promise((resolve) => setTimeout(resolve, simulatedLatency));

        switch (request.capability) {
            case 'vault:rebalance':
                return { rebalanced: true, optimizationPct: 0.1, timestamp: Date.now() };
            case 'vault:deposit':
                return { deposited: true, amount: request.params.amount, timestamp: Date.now() };
            case 'vault:withdraw':
                return { withdrawn: true, amount: request.params.amount, timestamp: Date.now() };
            case 'governance:propose':
                return { proposalId: `PROP-${uuid().slice(0, 8)}`, status: 'SUBMITTED' };
            case 'governance:vote':
                return { voted: true, proposalId: request.params.proposalId };
            case 'governance:branch':
                return { branchId: `BRANCH-${uuid().slice(0, 8)}`, status: 'INITIATED' };
            case 'kernel:harden':
                return { hardened: true, newResonance: 85 };
            case 'kernel:soft_reset':
                return { reset: true, resonance: 98, status: 'COHERENT' };
            case 'kernel:hard_reset':
                return { hardReset: true, warning: 'All state cleared.' };
            case 'stable:repeg':
                return { repegged: true, newParity: 1.0000 };
            case 'zk:verify':
                return { verified: true, proofHash: request.params.proofHash, backend: request.params.backend };
            case 'zk:batch_verify':
                return { batchVerified: true, count: (request.params.proofs as unknown[])?.length ?? 0 };
            case 'mesh:stress_drill':
                return { drillComplete: true, avgLatency: 12.4, errorRate: 0.001 };
            case 'identity:onboard':
                return { onboarded: true, passportGrade: 'SOVEREIGN' };
            case 'ledger:transfer':
                return { transferId: `TX-${uuid().slice(0, 8)}`, status: 'CONFIRMED' };
            case 'oracle:fetch':
                return { oracleData: { btc: 94500, eth: 3200, age: 1.42 }, freshness: Date.now() };
            case 'llm:query':
                return { response: 'Sovereign query processed.', model: request.params.model };
            case 'infra:deploy':
                return { deploymentId: `DEPLOY-${uuid().slice(0, 8)}`, status: 'ACTIVE' };
            case 'infra:teardown':
                return { tornDown: true, resourcesFreed: 12 };

            // FastCode Code Intelligence capabilities
            case 'code_intel:search': {
                const { codeIntelligence } = await import('./fastcode-engine.svelte');
                const results = await codeIntelligence.search(
                    (request.params.query as string) ?? '',
                    { maxResults: (request.params.maxResults as number) ?? 10 }
                );
                return {
                    results: results.map(r => ({
                        name: r.element.name,
                        type: r.element.type,
                        language: r.element.language,
                        path: r.element.relativePath,
                        score: r.score,
                        semanticScore: r.semanticScore,
                        keywordScore: r.keywordScore,
                        graphScore: r.graphScore,
                        summary: r.element.summary,
                    })),
                    budget: codeIntelligence.lastBudget,
                    scout: codeIntelligence.lastScout,
                };
            }

            case 'code_intel:impact': {
                const { codeIntelligence } = await import('./fastcode-engine.svelte');
                const elementId = (request.params.elementId as string) ?? '';
                const impact = codeIntelligence.analyzeImpact(elementId);
                return {
                    riskLevel: impact.riskLevel,
                    recommendation: impact.recommendation,
                    directlyAffected: impact.directlyAffected.map(e => ({ name: e.name, type: e.type, path: e.relativePath })),
                    transitivelyAffected: impact.transitivelyAffected.map(e => ({ name: e.name, type: e.type, path: e.relativePath })),
                };
            }

            case 'code_intel:graph_query': {
                const { codeIntelligence } = await import('./fastcode-engine.svelte');
                const graph = codeIntelligence.graph;
                return {
                    nodes: graph?.stats.totalNodes ?? 0,
                    edges: graph?.stats.totalEdges ?? 0,
                    density: graph?.stats.density ?? 0,
                    avgDegree: graph?.stats.avgDegree ?? 0,
                    callEdges: graph?.callGraph.length ?? 0,
                    depEdges: graph?.dependencyGraph.length ?? 0,
                    inheritEdges: graph?.inheritanceGraph.length ?? 0,
                };
            }

            default:
                throw new Error(`Unknown capability: ${request.capability}`);
        }
    }

    // ─── PHASE 5: OBSERVABILITY ──────────────────────────────────────────────
    // Lesson: "Trust in agents is something you observe, measure, and enforce."

    private startSpan(
        job: GatewayJob,
        name: string,
        attributes: Record<string, string | number | boolean>,
        parentSpanId?: string,
    ): GatewayTraceSpan {
        const span: GatewayTraceSpan = {
            spanId: uuid().slice(0, 8),
            name,
            startTime: performance.now(),
            endTime: null,
            status: 'IN_PROGRESS',
            attributes,
            parentSpanId,
        };
        job.trace.push(span);
        return span;
    }

    private endSpan(span: GatewayTraceSpan, status: 'OK' | 'ERROR') {
        span.endTime = performance.now();
        span.status = status;
    }

    // ─── EVENT SYSTEM ────────────────────────────────────────────────────────

    private emitEvent(event: AgentGatewayEvent) {
        this.eventLog.push(event);
        // Memory-bounded audit log — evict oldest entries when limit exceeded
        if (this.eventLog.length > AgentGateway.MAX_EVENT_LOG) {
            this.eventLog = this.eventLog.slice(-AgentGateway.MAX_EVENT_LOG);
        }
        // Evict completed jobs beyond retention limit to prevent memory leaks
        if (this.jobs.size > AgentGateway.MAX_COMPLETED_JOBS + 20) {
            const completedJobs = [...this.jobs.entries()]
                .filter(([, j]) => j.status === 'COMPLETED' || j.status === 'FAILED')
                .sort(([, a], [, b]) => a.createdAt - b.createdAt);
            const toEvict = completedJobs.length - AgentGateway.MAX_COMPLETED_JOBS;
            for (let i = 0; i < toEvict; i++) {
                const entry = completedJobs[i];
                if (entry) this.jobs.delete(entry[0]);
            }
        }
        // Notify subscribers
        for (const sub of this.subscribers) {
            try { sub(event); } catch { /* subscriber error — do not propagate */ }
        }
    }

    /** Subscribe to real-time gateway events. Returns unsubscribe function. */
    subscribe(callback: (event: AgentGatewayEvent) => void): () => void {
        this.subscribers.push(callback);
        return () => {
            this.subscribers = this.subscribers.filter((s) => s !== callback);
        };
    }

    // ─── SCHEMA VALIDATION ───────────────────────────────────────────────────

    private validateSchema(request: AgentRequest): boolean {
        if (!request.requestId || !request.capability || !request.actor?.id || !request.planHash || !request.idempotencyKey) {
            return false;
        }
        if (!(request.capability in CAPABILITY_RISK_MAP)) {
            return false;
        }
        return true;
    }

    // ─── PUBLIC API ──────────────────────────────────────────────────────────

    /** Set external context resolver (connected to SovereignManifold). */
    setContextResolver(resolver: () => PolicyContext) {
        this.contextResolver = resolver;
    }

    /** Add a custom policy rule (hot-reloadable, no redeploy). */
    addPolicy(rule: PolicyRule) {
        this.policies.push(rule);
        this.policies.sort((a, b) => b.priority - a.priority);
    }

    /** Remove a policy rule by ID. */
    removePolicy(ruleId: string) {
        this.policies = this.policies.filter((r) => r.id !== ruleId);
    }

    /** Get all registered policies. */
    getPolicies(): PolicyRule[] {
        return [...this.policies];
    }

    /** Get current gateway metrics. */
    get metrics(): GatewayMetrics {
        return { ...this._metrics };
    }

    /** Get the full audit log. */
    getAuditLog(): AgentGatewayEvent[] {
        return [...this.eventLog];
    }

    /** Get a specific job by ID. */
    getJob(jobId: string): GatewayJob | undefined {
        return this.jobs.get(jobId);
    }

    /** Get all jobs. */
    getAllJobs(): GatewayJob[] {
        return [...this.jobs.values()];
    }

    /** Get recent jobs (last N). */
    getRecentJobs(count: number = 20): GatewayJob[] {
        return [...this.jobs.values()].sort((a, b) => b.createdAt - a.createdAt).slice(0, count);
    }

    /** Build a valid AgentRequest helper. */
    buildRequest(
        capability: AgentCapability,
        actor: AgentRequest['actor'],
        params: Record<string, unknown> = {},
    ): AgentRequest {
        const planPayload = JSON.stringify({ capability, params, actor: actor.id });
        return {
            requestId: uuid(),
            capability,
            actor,
            params,
            planHash: sha256Hex(planPayload),
            idempotencyKey: uuid(),
            timestamp: new Date().toISOString(),
        };
    }

    private getContext(audit?: any): PolicyContext {
        if (this.contextResolver) {
            const ctx = this.contextResolver();
            if (audit) {
                ctx.metabolicAudit = {
                    score: audit.score,
                    status: audit.status,
                    risks: audit.risks
                };
            }
            return ctx;
        }

        // Default context
        const now = new Date();
        return {
            currentResonance: 98,
            permissionLevel: 'GUEST',
            isTurbulence: false,
            isMoatActive: false,
            timeOfDay: now.getHours(),
            dayOfWeek: now.getDay(),
            activeJobCount: this._metrics.activeJobs,
        };
    }

    /** Export the capability risk map for external use. */
    static get RISK_MAP(): Record<AgentCapability, RiskTier> {
        return { ...CAPABILITY_RISK_MAP };
    }
}

// ─── SINGLETON ───────────────────────────────────────────────────────────────

export const agentGateway = new AgentGateway();
