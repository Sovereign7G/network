// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SOVEREIGN AUDIT ENGINE (Ousterhout Deep Module)
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  manifold-state, proposed-actions
// [OUT]: auditAction(), MetabolicStatus, AuditReport
// [POS]: Implements "Metabolic Auditioning" (0x5C-RE). Analyzes trade-offs
//        between protocol stability, economic depth, and social resonance.
//        Prevents "Economic Amputation" by blocking dissonant interventions.
// ═══════════════════════════════════════════════════════════════════════════════

// ─── UTILITY ─────────────────────────────────────────────────────────────────

type MetabolicStatus = 'HEALTHY' | 'DISSONANT' | 'AMPUTATION_RISK';

interface AuditReport {
    status: MetabolicStatus;
    score: number;           // 0-100 (100 = Perfect Harmony)
    delta: number;           // Metabolic Delta (Divergence from homeostasis)
    recommendation: string;
    risks: string[];
    reasoningTrace: string[]; // Step-by-step reasoning for the score
}

// Use a lazy getter to break circular dependency with master-store
async function getManifold() {
    const { manifold } = await import('../stores/master-store.svelte');
    return manifold;
}

class SovereignAuditEngine {
    private _lastAudit = $state<AuditReport | null>(null);
    private _anomalyCount = $state(0);

    get lastAudit() { return this._lastAudit; }
    get anomalies() { return this._anomalyCount; }

    /**
     * Audit a proposed protocol intervention.
     * Applies heuristic weights to predict the impact on Manifold Resonance.
     */
    auditAction(actionType: string, _params: Record<string, any> = {}, manifoldContext?: any): AuditReport {

        let score = 100;
        const risks: string[] = [];
        const trace: string[] = ['Initiating Metabolic Auditioning...'];

        // Use provided context or fall back to global manifold if available
        const currentResonance = manifoldContext?.resonance ?? 98;

        trace.push(`Current System Resonance: ${currentResonance.toFixed(1)}%`);

        // 1. Resonance Guard
        if (currentResonance < 80) {
            const penalty = (80 - currentResonance) * 2;
            score -= penalty;
            risks.push('LOW_RESONANCE_VULNERABILITY');
            trace.push(`[PENALTY] Low Resonance: -${penalty.toFixed(1)} points. System below 80% homeostasis.`);
        } else {
            trace.push(`[PASS] Resonance within safe bounds. (Score: ${score})`);
        }

        // 2. Action-Specific Logic
        trace.push(`Evaluating action: ${actionType}`);

        // We handle action-specific checks with the provided context
        const turbulence = manifoldContext?.turbulence ?? false;
        const vaultTVL = manifoldContext?.vaultState?.totalValueLockedUsd ?? 0;
        const stableParity = manifoldContext?.stablecoinState?.parity ?? 1.0;

        switch (actionType) {
            case 'HARDEN':
                if (turbulence) {
                    score -= 10;
                    risks.push('REDUNDANT_HARDENING');
                    trace.push(`[PENALTY] REDUNDANT_HARDENING: -10 points. Operation during turbulence is suboptimal.`);
                }
                break;

            case 'SOFT_RESET':
                if (currentResonance > 95) {
                    score -= 30;
                    risks.push('OPTIMAL_STATE_INTERFERENCE');
                    trace.push(`[PENALTY] OPTIMAL_STATE_INTERFERENCE: -30 points. System already at near-perfect coherence.`);
                }
                break;

            case 'VAULT_REBALANCE':
                if (vaultTVL > 100_000_000) {
                    score -= 15;
                    risks.push('HIGH_TVL_SLIPPAGE_RISK');
                    trace.push(`[PENALTY] HIGH_TVL_SLIPPAGE_RISK: -15 points. Liquidity depth insufficient for zero-impact rebalance.`);
                }
                break;

            case 'STABLE_REPEG':
                const drift = Math.abs(stableParity - 1.0);
                if (drift < 0.005) {
                    score -= 20;
                    risks.push('PREMATURE_PEGGING_FRICTION');
                    trace.push(`[PENALTY] PREMATURE_PEGGING_FRICTION: -20 points. Drift of ${(drift * 100).toFixed(4)}% is within biological jitter tolerance.`);
                }
                break;
        }

        // 3. Compute Final Status
        const delta = 100 - score;
        const status: MetabolicStatus =
            delta > 40 ? 'AMPUTATION_RISK' :
                delta > 15 ? 'DISSONANT' : 'HEALTHY';

        trace.push(`Audition complete. Final Score: ${score}/100. Status: ${status}.`);

        const report: AuditReport = {
            status,
            score,
            delta,
            risks,
            reasoningTrace: trace,
            recommendation: this._generateRecommendation(status, actionType)
        };


        this._lastAudit = report;
        if (status !== 'HEALTHY') this._anomalyCount++;

        return report;
    }

    private _generateRecommendation(status: MetabolicStatus, action: string): string {
        switch (status) {
            case 'AMPUTATION_RISK': return `CRITICAL: Block ${action}. Systemic dissonance exceeds safety threshold.`;
            case 'DISSONANT': return `WARNING: Proceed with caution. ${action} may cause resonance decay.`;
            case 'HEALTHY': return `RATIFY: ${action} is metabolically sound.`;
        }
    }

    async tick() {
        // Late bind manifold to check resonance
        const manifold = await getManifold();
        const resonance = manifold.resonance;
        if (resonance < 70) {
            this._anomalyCount++;
            manifold.recordEvent('AUDIT_ANOMALY', `Low resonance (${resonance.toFixed(1)}) detected by Sovereign Steward.`);
        }
    }
}


export const auditEngine = new SovereignAuditEngine();

