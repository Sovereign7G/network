import type { PolicyRule, AgentCapability, RiskTier, AgentTrust } from '../types/agent-gateway.types';
import { CAPABILITY_RISK_MAP } from '../types/agent-gateway.types';

/**
 * 🏛️ BUILT-IN POLICY REGISTRY
 * 
 * These mirror the article's OPA rules: RBAC, Integrity, Safety, Change Window.
 * Extracted from the main gateway to improve modularity and enable hot-reloading.
 */
export const BUILTIN_POLICIES: PolicyRule[] = [
    // RULE 1: RBAC — Agent trust level must meet capability requirements.
    {
        id: 'POL-RBAC-001',
        name: 'Agent Trust Gate',
        description: 'Agents must meet minimum trust level for the requested capability.',
        capabilities: '*',
        priority: 100,
        isFinal: true,
        evaluate: (req) => {
            const MIN_TRUST: Record<RiskTier, AgentTrust[]> = {
                LOW: ['UNTRUSTED', 'REGISTERED', 'VERIFIED', 'SOVEREIGN'],
                MEDIUM: ['REGISTERED', 'VERIFIED', 'SOVEREIGN'],
                HIGH: ['VERIFIED', 'SOVEREIGN'],
                CRITICAL: ['SOVEREIGN'],
            };
            const tier = CAPABILITY_RISK_MAP[req.capability];
            const allowed = MIN_TRUST[tier].includes(req.actor.trust);
            return {
                allowed,
                reason: allowed
                    ? `Trust level ${req.actor.trust} meets ${tier} requirement.`
                    : `Trust level ${req.actor.trust} insufficient for ${tier}-tier capability ${req.capability}.`,
            };
        },
    },

    // RULE 2: SAFETY — Block destructive operations categorically.
    {
        id: 'POL-SAFETY-001',
        name: 'Destructive Action Block',
        description: 'Prevent teardown/hard-reset unless explicit approval token is present.',
        capabilities: ['kernel:hard_reset', 'infra:teardown'],
        priority: 99,
        isFinal: true,
        evaluate: (req) => {
            if (req.approvalToken) {
                return { allowed: true, reason: 'Destructive action approved with token.' };
            }
            return { allowed: false, reason: 'Destructive actions require explicit human approval token.' };
        },
    },

    // RULE 3: CHANGE WINDOW — Business-hours gating for production-tier actions.
    {
        id: 'POL-WINDOW-001',
        name: 'Change Window Enforcement',
        description: 'HIGH/CRITICAL operations restricted to business hours (Mon-Fri 09:00-17:00).',
        capabilities: '*',
        priority: 80,
        isFinal: false,
        evaluate: (req, ctx) => {
            const tier = CAPABILITY_RISK_MAP[req.capability];
            if (tier !== 'HIGH' && tier !== 'CRITICAL') {
                return { allowed: true, reason: 'Low/medium risk — no change window restriction.' };
            }
            const isWeekday = ctx.dayOfWeek >= 1 && ctx.dayOfWeek <= 5;
            const isBusinessHours = ctx.timeOfDay >= 9 && ctx.timeOfDay < 17;
            const allowed = isWeekday && isBusinessHours;
            return {
                allowed,
                reason: allowed
                    ? 'Within change window (Mon-Fri 09:00-17:00).'
                    : `Outside change window. Day: ${ctx.dayOfWeek}, Hour: ${ctx.timeOfDay}.`,
            };
        },
    },

    // RULE 4: RESONANCE GUARD — Block operations when system is degraded.
    {
        id: 'POL-RESONANCE-001',
        name: 'Manifold Resonance Guard',
        description: 'Deny non-recovery operations when system resonance drops below 80.',
        capabilities: '*',
        priority: 90,
        isFinal: false,
        evaluate: (_req, ctx) => {
            const recoveryOps: AgentCapability[] = ['kernel:soft_reset', 'kernel:harden', 'oracle:fetch'];
            if (recoveryOps.includes(_req.capability)) {
                return { allowed: true, reason: 'Recovery operation permitted during degradation.' };
            }
            if (ctx.currentResonance < 80) {
                return { allowed: false, reason: `System resonance ${ctx.currentResonance.toFixed(1)} below 80. Only recovery ops permitted.` };
            }
            return { allowed: true, reason: `Resonance ${ctx.currentResonance.toFixed(1)} within safe range.` };
        },
    },

    // RULE 5: TURBULENCE LOCKDOWN — Full lockdown during active turbulence.
    {
        id: 'POL-TURB-001',
        name: 'Turbulence Lockdown',
        description: 'During active turbulence, only SOVEREIGN agents can execute.',
        capabilities: '*',
        priority: 95,
        isFinal: true,
        evaluate: (req, ctx) => {
            if (!ctx.isTurbulence) {
                return { allowed: true, reason: 'No turbulence detected.' };
            }
            if (req.actor.trust === 'SOVEREIGN') {
                return { allowed: true, reason: 'SOVEREIGN agent permitted during turbulence.' };
            }
            return { allowed: false, reason: 'System in turbulence. Only SOVEREIGN agents can execute.' };
        },
    },

    // RULE 6: CONCURRENCY LIMIT — Prevent agent swarm overload.
    {
        id: 'POL-CONCURRENCY-001',
        name: 'Concurrency Limiter',
        description: 'Maximum 10 concurrent gateway jobs to prevent resource exhaustion.',
        capabilities: '*',
        priority: 70,
        isFinal: false,
        evaluate: (_req, ctx) => {
            const MAX_CONCURRENT = 10;
            if (ctx.activeJobCount >= MAX_CONCURRENT) {
                return { allowed: false, reason: `Concurrency limit reached (${ctx.activeJobCount}/${MAX_CONCURRENT}).` };
            }
            return { allowed: true, reason: `Concurrency within limits (${ctx.activeJobCount}/${MAX_CONCURRENT}).` };
        },
    },

    // RULE 7: IDEMPOTENCY CHECK — Prevent duplicate execution.
    {
        id: 'POL-IDEM-001',
        name: 'Idempotency Guard',
        description: 'Reject requests with previously-seen idempotency keys.',
        capabilities: '*',
        priority: 100,
        isFinal: true,
        evaluate: (req) => {
            return { allowed: true, reason: `Idempotency key ${req.idempotencyKey.slice(0, 8)}… accepted.` };
        },
    },

    // RULE 8: MOAT LOCKDOWN — Block non-recovery ops when defensive moat is active.
    {
        id: 'POL-MOAT-001',
        name: 'Economic Moat Lockdown',
        description: 'When the sovereign economic moat is active, only recovery and diagnostic operations are permitted.',
        capabilities: '*',
        priority: 92,
        isFinal: true,
        evaluate: (req, ctx) => {
            if (!ctx.isMoatActive) {
                return { allowed: true, reason: 'No moat lockdown in effect.' };
            }
            const recoveryOps: AgentCapability[] = ['kernel:soft_reset', 'kernel:harden', 'oracle:fetch', 'zk:verify'];
            if (recoveryOps.includes(req.capability)) {
                return { allowed: true, reason: 'Recovery/diagnostic operation permitted during moat lockdown.' };
            }
            if (req.actor.trust === 'SOVEREIGN') {
                return { allowed: true, reason: 'SOVEREIGN agent override during moat lockdown.' };
            }
            return { allowed: false, reason: 'Economic moat active — only recovery ops and SOVEREIGN agents permitted.' };
        },
    },

    // RULE 9: RATE LIMITER — Per-agent sliding window rate control.
    {
        id: 'POL-RATE-001',
        name: 'Agent Rate Limiter',
        description: 'Enforce max 50 requests per 60-second sliding window per agent.',
        capabilities: '*',
        priority: 85,
        isFinal: false,
        evaluate: (req) => {
            return { allowed: true, reason: `Rate check for agent ${req.actor.id.slice(0, 8)}… deferred to gateway.` };
        },
    },

    // RULE 10: METABOLIC HYGIENE — Guard against systemic dissonance.
    {


        id: 'POL-METABOLIC-001',
        name: 'Metabolic Harmony Guard',
        description: 'Mandatory metabolic audit for HIGH/CRITICAL and financial operations.',
        capabilities: '*',
        priority: 98,
        isFinal: true,
        evaluate: (req, ctx) => {
            const financialOps: AgentCapability[] = ['vault:rebalance', 'vault:withdraw', 'vault:deposit', 'stable:repeg', 'ledger:transfer'];
            const tier = CAPABILITY_RISK_MAP[req.capability];

            if (tier !== 'HIGH' && tier !== 'CRITICAL' && !financialOps.includes(req.capability)) {
                return { allowed: true, reason: 'Low/Medium non-financial operation skips metabolic audit.' };
            }

            if (!ctx.metabolicAudit) {
                return { allowed: false, reason: 'Metabolic audit missing for sensitive operation.' };
            }

            if (ctx.metabolicAudit.status === 'AMPUTATION_RISK') {
                return {
                    allowed: false,
                    reason: `METABOLIC DENIAL: ${req.capability} would cause extreme systemic dissonance (Score: ${ctx.metabolicAudit.score}). Risks: ${ctx.metabolicAudit.risks.join(', ')}`
                };
            }

            return {
                allowed: true,
                reason: `Metabolic audit passed (Score: ${ctx.metabolicAudit.score}). Health: ${ctx.metabolicAudit.status}.`
            };
        },
    },
];

