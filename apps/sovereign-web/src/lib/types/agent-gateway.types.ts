// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ AGENT GATEWAY TYPE DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  None (pure type definitions)
// [OUT]: All gateway types — capabilities, trust, policies, jobs, traces, events
// [POS]: Separated from agent-gateway.ts per Ousterhout's principle:
//        "Different layer, different abstraction."
//        Types define the WHAT. The gateway module defines the HOW.
// Protocol: When updating me, sync this header + parent folder's .folder.md
// ═══════════════════════════════════════════════════════════════════════════════

// ─── CAPABILITY TYPES ────────────────────────────────────────────────────────

/** Every known capability an agent can invoke. Closed set — agents cannot invent actions. */
export type AgentCapability =
    | 'vault:rebalance'
    | 'vault:withdraw'
    | 'vault:deposit'
    | 'governance:propose'
    | 'governance:vote'
    | 'governance:branch'
    | 'kernel:harden'
    | 'kernel:soft_reset'
    | 'kernel:hard_reset'
    | 'stable:repeg'
    | 'zk:verify'
    | 'zk:batch_verify'
    | 'mesh:stress_drill'
    | 'identity:onboard'
    | 'ledger:transfer'
    | 'oracle:fetch'
    | 'llm:query'
    | 'infra:deploy'
    | 'infra:teardown'
    // FastCode-inspired Code Intelligence capabilities
    | 'code_intel:search'
    | 'code_intel:impact'
    | 'code_intel:graph_query';

// ─── RISK & TRUST TYPES ─────────────────────────────────────────────────────

/** Risk tiers that determine policy strictness. */
export type RiskTier = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

/** Trust levels for requesters — mirrors AGE permissionLevel but for agents. */
export type AgentTrust = 'UNTRUSTED' | 'REGISTERED' | 'VERIFIED' | 'SOVEREIGN';

// ─── JOB TYPES ──────────────────────────────────────────────────────────────

/** Status of a gateway job. */
export type JobStatus =
    | 'PENDING_POLICY'
    | 'POLICY_DENIED'
    | 'QUEUED'
    | 'EXECUTING'
    | 'COMPLETED'
    | 'FAILED'
    | 'SANDBOX_TEARDOWN';

// ─── REQUEST TYPES ──────────────────────────────────────────────────────────

/** Structured intent for any agent-initiated action. */
export interface AgentRequest {
    /** Unique request identifier (UUID) */
    requestId: string;
    /** The capability being invoked */
    capability: AgentCapability;
    /** Agent identity — never trusted implicitly */
    actor: {
        id: string;
        trust: AgentTrust;
        provider?: string;   // 'openai' | 'anthropic' | 'local' | 'icp_canister' etc.
        sessionId?: string;
    };
    /** Payload for the action — schema-validated per capability */
    params: Record<string, unknown>;
    /** Content-addressable hash of the action plan */
    planHash: string;
    /** Idempotency key to prevent duplicate execution */
    idempotencyKey: string;
    /** ISO timestamp of the request */
    timestamp: string;
    /** Optional: human approval token for CRITICAL tier */
    approvalToken?: string;
}

// ─── POLICY TYPES ───────────────────────────────────────────────────────────

/** Result of policy evaluation — externalized, not embedded in app code. */
export interface PolicyDecision {
    allowed: boolean;
    reason: string;
    appliedRules: string[];
    riskTier: RiskTier;
    requiresApproval: boolean;
    evaluatedAt: string;
    evaluationMs: number;
}

/** A single policy rule — declarative, composable, and auditable. */
export interface PolicyRule {
    id: string;
    name: string;
    description: string;
    /** Which capabilities this rule applies to */
    capabilities: AgentCapability[] | '*';
    /** Evaluation function — pure, with no side effects */
    evaluate: (request: AgentRequest, context: PolicyContext) => PolicyRuleResult;
    /** Priority: higher = evaluated first */
    priority: number;
    /** If true, a deny from this rule is final (no override). */
    isFinal: boolean;
}

export interface PolicyRuleResult {
    allowed: boolean;
    reason: string;
}

export interface PolicyContext {
    currentResonance: number;
    permissionLevel: string;
    isTurbulence: boolean;
    isMoatActive: boolean;
    timeOfDay: number; // 0-23
    dayOfWeek: number; // 0=Sun, 6=Sat
    activeJobCount: number;
    metabolicAudit?: {
        score: number;
        status: 'HEALTHY' | 'DISSONANT' | 'AMPUTATION_RISK';
        risks: string[];
    };
}


// ─── JOB & EXECUTION TYPES ─────────────────────────────────────────────────

/** An execution job created after policy approval. */
export interface GatewayJob {
    jobId: string;
    request: AgentRequest;
    policy: PolicyDecision;
    status: JobStatus;
    sandboxId: string | null;
    result: unknown;
    error: string | null;
    trace: GatewayTraceSpan[];
    createdAt: number;
    completedAt: number | null;
}

// ─── OBSERVABILITY TYPES ────────────────────────────────────────────────────

/** OpenTelemetry-style trace span for observability. */
export interface GatewayTraceSpan {
    spanId: string;
    name: string;
    startTime: number;
    endTime: number | null;
    status: 'OK' | 'ERROR' | 'IN_PROGRESS';
    attributes: Record<string, string | number | boolean>;
    parentSpanId?: string | undefined;
}

/** Aggregate gateway metrics. */
export interface GatewayMetrics {
    totalRequests: number;
    totalApproved: number;
    totalDenied: number;
    totalExecuted: number;
    totalFailed: number;
    avgPolicyLatencyMs: number;
    avgExecutionLatencyMs: number;
    avgSandboxTeardownMs: number;
    denialRate: number;
    activeJobs: number;
    sandboxesCreated: number;
    sandboxesDestroyed: number;
}

/** Event emitted for full audit trail. */
export interface AgentGatewayEvent {
    eventId: string;
    type:
    | 'REQUEST_RECEIVED'
    | 'POLICY_EVALUATED'
    | 'POLICY_DENIED'
    | 'JOB_QUEUED'
    | 'SANDBOX_CREATED'
    | 'EXECUTION_STARTED'
    | 'EXECUTION_COMPLETED'
    | 'EXECUTION_FAILED'
    | 'SANDBOX_DESTROYED'
    | 'APPROVAL_REQUIRED'
    | 'SLO_VIOLATION';
    payload: Record<string, unknown>;
    timestamp: number;
    traceId: string;
}

// ─── CAPABILITY RISK MAPPING ────────────────────────────────────────────────

/** Maps each capability to its risk tier. Centralized data, not logic. */
export const CAPABILITY_RISK_MAP: Record<AgentCapability, RiskTier> = {
    'oracle:fetch': 'LOW',
    'llm:query': 'LOW',
    'zk:verify': 'LOW',
    'zk:batch_verify': 'LOW',
    'vault:deposit': 'MEDIUM',
    'vault:rebalance': 'MEDIUM',
    'governance:vote': 'MEDIUM',
    'stable:repeg': 'MEDIUM',
    'mesh:stress_drill': 'MEDIUM',
    'identity:onboard': 'MEDIUM',
    'ledger:transfer': 'HIGH',
    'vault:withdraw': 'HIGH',
    'governance:propose': 'HIGH',
    'governance:branch': 'HIGH',
    'kernel:harden': 'HIGH',
    'infra:deploy': 'HIGH',
    'kernel:soft_reset': 'HIGH',
    'kernel:hard_reset': 'CRITICAL',
    'infra:teardown': 'CRITICAL',
    // FastCode Code Intelligence (read-only, no side effects)
    'code_intel:search': 'LOW',
    'code_intel:impact': 'LOW',
    'code_intel:graph_query': 'LOW',
};
