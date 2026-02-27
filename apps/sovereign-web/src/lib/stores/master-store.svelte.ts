// [IN]: svelte, vault-store, telemetry-store, governance-store, concierge-store, web3-service, icp-service
// [OUT]: SovereignManifold, manifold, systemHealth
// [POS]: The Central Intelligence Layer and state management for the Sovereign Web Manifold. / Sovereign Web Manifold \u7684\u4e2d\u592e\u667a\u80fd\u5c42\u548c\u72b6\u6001\u7ba1\u7406\u3022
// Protocol: When updating me, sync this header + parent folder's .folder.md

import { browser } from '$app/environment';
import { sovereignOpenCode } from '$lib/services/opencode-engine.svelte';
import { sovereignMolecule } from '$lib/services/mol-engine.svelte';
import { sovereignPicoClaw } from '$lib/services/picoclaw-engine.svelte';
import { sovereignZVec } from '$lib/services/zvec-engine.svelte';
import { sovereignSDD } from '$lib/services/sdd-engine.svelte';
import { sovereignEdgeScaler } from '$lib/services/edge-scaler.svelte';
import { sovereignRouteAgent } from '$lib/services/route-agent.svelte';
import { sovereignPhilosophy } from '$lib/services/philosophy-engine.svelte';
import { simulationEngine } from '$lib/services/simulation-engine.svelte';
import { sovereignStore } from './sovereign-store.svelte';
import { hearthStore } from './hearth-store.svelte';
import { vaultStore } from './vault-store.svelte';
import { governanceStore } from './governance-store.svelte';
import { conciergeStore } from './concierge-store.svelte';
import { telemetryStore } from './telemetry-store.svelte';
import { dashboardStore } from './dashboard-store.svelte';
import { onboardingStore } from './onboarding-store.svelte';
import { authStore } from './auth.svelte';
import { web3Service } from '$lib/services/web3-service.svelte';
import { icpService } from '$lib/services/icp-service.svelte';
            // @ts-ignore
import { agentGateway, type AgentGatewayEvent } from '$lib/services/agent-gateway';
import { notaryService } from '$lib/services/notary-service';
import { tokenomicsEngine } from '$lib/services/tokenomics-engine.svelte';
import { meshStressEngine } from '$lib/services/mesh-stress-engine.svelte';
import { zkAttesterEngine } from '$lib/services/zk-attester-engine.svelte';
import { metabolicEngine } from '$lib/services/metabolic-engine.svelte';
import { validatorEngine } from '$lib/services/validator-engine.svelte';
import { computeEngine } from '$lib/services/compute-engine.svelte';



import type { CognitiveEpoch, LLLState, BusinessState, EconomicEvent, CircularState, ForensicYieldState, OrderSide } from '$lib/types';



// 🏛️ SOVEREIGN MANIFOLD: The Central Intelligence Layer
export class SovereignManifold {
    // --- SYSTEM STATUS ---
    status = $state<'COHERENT' | 'STALLED' | 'DEGRADED'>('COHERENT');
    get resonance() { return telemetryStore.vitals.resonance; }
    set resonance(v: number) { telemetryStore.vitals.resonance = v; }

    get activeLayers() { return telemetryStore.vitals.activeConnections; } // Mapping active connections to layers for now
    set activeLayers(v: number) { telemetryStore.vitals.activeConnections = v; }

    lastHeartbeat = $state(Date.now());

    // --- FINANCIAL STATE ---
    get totalWealth() { return vaultStore.totalValue; }
    // totalWealth is usually derived, so no setter needed unless we want to force it

    ageCredits = $state(25400);
    ownedPlans = $state<string[]>([]);

    get isSynced() { return telemetryStore.vitals.syncStatus === 'synced'; }
    set isSynced(v: boolean) { telemetryStore.vitals.syncStatus = v ? 'synced' : 'degraded'; }

    // --- SECURITY & MODES ---
    isMoatActive = $state(false);
    turbulence = $state(false);
    isMeshConnected = $state(false);
    isZenMode = $state(false);
    isSpatialMode = $state(false);
    isSimulating = $state(false);
    isDesignMode = $state(false);

    // --- CORE MODULE STATES ---
    kernelState = $state<any>({});
    governanceState = $state<any>({});
    photonicGlow = $state({ intensity: 0, color: '#22d3ee' });
    multiversalState = $state<any>({});
    spectralBourse = $state<any>({});
    get validatorState() { return validatorEngine.state; }

    get ledgerState() { return metabolicEngine.ledger; }

    logisticsState = $state<any>({});
    get tokenomicsState() { return tokenomicsEngine.state; }
    singularityState = $state<any>({});
    fediverseState = $state<any>({});
    localEconomyState = $state<any>({});

    get vaultState() { return metabolicEngine.vault; }
    get stablecoinState() { return metabolicEngine.stablecoin; }
    get financialIntelligence() { return metabolicEngine.intelligence; }

    bridgeStatus = $state<any>({});
    hilbertState = $state<any>({});
    get computeMarket() { return computeEngine.state; }

    veAgeState = $state<any>({});


    // --- SUB-STATES ---
    branchingState = $state({ active: false, branchId: null as string | null, parentBranch: 'v1.2', progress: 0, economicMoodShift: 'NEUTRAL' as 'NEUTRAL' | 'BULLISH' | 'BEARISH', proofGenerated: false });
    auditState = $state({ isAuditing: false, lastResults: [] as { timestamp: number, status: string, type: string, msg: string }[], health: 100 });
    stressLabState = $state({ fuzzing: false, activeVectors: [] as string[], manifoldStrain: 0, lastPanic: null as number | null });

    // Delegated to MeshStressEngine
    get meshStressState() { return meshStressEngine.state; }

    // Delegated to ZkAttesterEngine
    get zkAttesterState() { return zkAttesterEngine.state; }

    walletState = $state({ moralCredits: 4200.5, merits: 850, reputationScore: 0.92, manifoldDistance: 0.05, compliance: 'BASEL_IV' });
    businessState = $state<BusinessState>({ activeJobs: [], completedJobsCount: 142, rewardMultiplier: 1.0 });
    lllState = $state<LLLState>({
        activeGrids: 12,
        peakDissonance: 0.14,
        resolutionAlgorithm: 'TENNIS_MATCH',
        avgRoundsToConvergence: 3.2,
        status: 'OPERATIONAL'
    });
    circularState = $state<CircularState>({ ownershipModel: 'DABBA_COMMUNAL', status: 'STEADY' });
    forensicYieldState = $state<ForensicYieldState>({
        total: 12.4,
        status: 'VERIFIED',
        components: [
            { name: "Liquidity_Mining", contribution: 4.2, source: "DEX_MESH", color: "#22d3ee" },
            { name: "Validator_Rewards", contribution: 3.8, source: "Validator_Set", color: "#10b981" },
            { name: "Sovereign_Fee_Rebate", contribution: 2.1, source: "Kernel_Router", color: "#6366f1" },
            { name: "Proof_Generation_Mint", contribution: 2.3, source: "Pantheon_Forge", color: "#a855f7" }
        ],
        historicalYields: [],
        currentYield: 12.4,
        projectedYield: 13.2,
        volatility: 0.023,
        sharpeRatio: 1.8,
        maxDrawdown: 0.057,
        recoveryTime: 14,
        anomalies: []
    });
    foreignProtocols = $state([
        { id: 'fp-fediverse', name: 'Fediverse Bridge', status: 'ACTIVE', health: 0.98 },
        { id: 'fp-zk', name: 'JADE Verifier', status: 'OPTIMIZING', health: 0.85 }
    ]);
    trustMatrix = $state([
        { id: 'tm-01', source: 'Nagano', target: 'Zug', trust: 0.98, alignment: 0.95 },
        { id: 'tm-02', source: 'London', target: 'Tokyo', trust: 0.85, alignment: 0.92 }
    ]);

    // --- HISTORY & LOGS ---
    cognitiveHistory = $state<CognitiveEpoch[]>([]);
    causalLog = $state<EconomicEvent[]>([]);
    visualFX = $state({ glitchActive: false, panicOverlay: false });
    designPatches = $state<{ blockId: string, field: string, value: unknown }[]>([]);

    // --- DEEP INTELLIGENCE MANIFOLD (Ousterhout Deep Module Pattern) ---
    // Using a getter instead of $derived to break circular dependency at module load time
    get intelligence() {
        return {
            opencode: { metrics: sovereignOpenCode?.metrics, stats: sovereignOpenCode?.stats },
            molecule: { metrics: sovereignMolecule?.metrics, stats: sovereignMolecule?.stats },
            picoclaw: { metrics: sovereignPicoClaw?.metrics, stats: sovereignPicoClaw?.stats },
            zvec: { metrics: sovereignZVec?.metrics, stats: sovereignZVec?.stats },
            sdd: { metrics: sovereignSDD?.metrics, stats: sovereignSDD?.stats },
            edge: { metrics: sovereignEdgeScaler?.metrics, stats: sovereignEdgeScaler?.stats },
            route: { metrics: sovereignRouteAgent?.metrics, stats: sovereignRouteAgent?.stats },
            philosophy: { metrics: sovereignPhilosophy?.metrics, stats: sovereignPhilosophy?.stats },
            stance: (sovereignPhilosophy?.metrics?.strategicInvestment ?? 0) > 70 ? 'strategic' : 'tactical'
        };
    }

    // --- AGENT GATEWAY STATE (InfoQ Least-Privilege AI Gateway) ---
    get gatewayMetrics() { return agentGateway?.metrics; }
    get gatewayEvents() { return this._gatewayEvents; }
    private _gatewayEvents = $state<AgentGatewayEvent[]>([]);
    gatewayPolicyCount = $state(0);

    // --- CONTEXTS ---
    contexts = $state<{ id: string, name: string, icon: string, badge: boolean }[]>([]);
    activeContextId = $state('ctx-core');
    causalSnapshots = $state<{ id: string, timestamp: number, label: string, columns: unknown[] }[]>([]);
    focusedBlockId = $state<string | null>(null);

    setFocus(id: string | null) {
        this.focusedBlockId = id;
    }

    getDesignPatch(blockId: string, field: string) {
        return this.designPatches.find(p => p.blockId === blockId && p.field === field)?.value;
    }

    applyDesignPatch(blockId: string, field: string, value: any) {
        const existing = this.designPatches.find(p => p.blockId === blockId && p.field === field);
        if (existing) {
            existing.value = value;
        } else {
            this.designPatches.push({ blockId, field, value });
        }
    }

    // --- WEB3 STATE (Runes) ---
    web3 = web3Service.state;
    icp = icpService.state;

    // --- SOVEREIGN IDENTITY (Unified) ---
    identity = $derived({
        evm: this.web3.address,
        icp: this.icp.principal,
        isFullyManifested: this.web3.isConnected && this.icp.isAuthenticated,
        label: this.web3.isConnected
            ? `${this.web3.address?.slice(0, 6)}...`
            : (this.icp.isAuthenticated ? `Principal ${this.icp.principal?.slice(0, 4)}...` : 'GUEST')
    });

    // --- PERMISSIONS (Gated by BioVault) ---
    permissionLevel = $derived(
        !this.icp.isAuthenticated ? 'GUEST' :
            this.resonance > 95 ? 'SOVEREIGN_OVERSEER' :
                this.resonance > 85 ? 'VERIFIED_CITIZEN' :
                    'REGISTERED_PROSPECT'
    );

    constructor() {
        if (browser) {
            this._initAgentGateway();
            this._wireEngines();
            this._syncManifold();

            // Start the simulation engine to provide metabolic life
            simulationEngine.start();
        }
    }

    private _wireEngines() {
        meshStressEngine.setCallbacks({
            onEvent: (type: string, msg: string) => this.recordEvent(type, msg),
            onGlitch: (active: boolean) => { this.visualFX.glitchActive = active; }
        });
        zkAttesterEngine.setEventCallback((type: string, msg: string) => this.recordEvent(type, msg));
    }


    private _syncManifold() {
        this.recordEvent('MANIFOLD_INIT', 'Sovereign synchronization sequence engaged.');
        // Initial data pull
        Promise.allSettled([
            vaultStore.loadVaultData(),
            sovereignStore.loadSovereignData()
        ]);

        this.contexts = [
            { id: 'ctx-mesh', name: 'The Mesh', icon: '🕸️', badge: false },
            { id: 'ctx-vault', name: 'The Vault', icon: '🏦', badge: true },
            { id: 'ctx-kernel', name: 'The Kernel', icon: '🧠', badge: false }
        ];
        this.activeContextId = 'ctx-mesh';
    }

    switchContext(id: string, currentColumns: any[]) {
        this.activeContextId = id;
        this.recordEvent('CONTEXT_SWITCH', `Manifold reconfigured for: ${id}`);
        // Strategy: Return re-verified columns for the new context
        return currentColumns.map(c => ({ ...c, active: Math.random() > 0.2 }));
    }



    async recordEvent(type: string, msg: string) {
        const event = await notaryService.notarize(type, msg);
        this.causalLog = [event, ...this.causalLog].slice(0, 50);
    }

    triggerEscalation(_shardId: string) {
        this.multiversalState.escalationLevel = Math.min(100, this.multiversalState.escalationLevel + 20);
        this.multiversalState.syncStatus = 'ESCALATED';
        this.resonance -= 5;
    }

    archiveManifoldState() {
        const snap = { id: `ARCHIVE-0x${Date.now().toString(16).toUpperCase()}`, timestamp: Date.now(), resonance: this.resonance };
        this.multiversalState.archives.unshift(snap);
        this.resonance = Math.min(100, this.resonance + 5);
        this.recordEvent('MANIFOLD_ARCHIVED', `State sealed: ${snap.id}`);
    }

    finishJob(id: string) {
        const idx = this.businessState.activeJobs.findIndex(j => j.id === id);
            // @ts-ignore
        if (idx !== -1) {
            const job = this.businessState.activeJobs[idx];
            this.ageCredits += job.reward;
            this.businessState.activeJobs.splice(idx, 1);
            this.recordEvent('JOB_COMPLETED', `Mission ${id} finalized.`);
            this.mineCognitiveEpoch(job.title || id);
        }
    }

    mineCognitiveEpoch(jobTitle: string) {
        const id = `LOG-0x${Math.floor(Math.random() * 0xFFFF).toString(16).toUpperCase()}`;
        const moods: CognitiveEpoch['mood'][] = ['ZEN', 'ANALYTICAL', 'TRANSCENDENT', 'RESOLVED'];
        const mood = moods[Math.floor(Math.random() * moods.length)] as CognitiveEpoch['mood'];

        this.cognitiveHistory.unshift({
            id,
            epoch: 'Adaptive_Convergence',
            mood,
            thought: `Cognitive synthesis of '${jobTitle || 'Unknown Mission'}' completed.`
        });
        this.cognitiveHistory = this.cognitiveHistory.slice(0, 20);
        this.resonance = Math.min(100, this.resonance + 2);
        this.recordEvent('COGNITIVE_MINED', `Sophia epoch mined from job: ${jobTitle || 'Unknown'}`);
    }


    initiateBranch(id: string) {
        this.recordEvent('GOV_BRANCH_INITIATED', `Copy-on-Write branch ${id} spawned sequence.`);
        this.branchingState.active = true;
        this.branchingState.branchId = id;
        this.branchingState.progress = 0;
        this.branchingState.proofGenerated = false;

        const interval = setInterval(() => {
            if (this.branchingState.progress < 100) {
                this.branchingState.progress += 2;
                if (this.branchingState.progress === 50) this.branchingState.economicMoodShift = 'BULLISH';
            } else {
                this.branchingState.proofGenerated = true;
                this.recordEvent('GOV_BRANCH_COHERENT', `Branch ${id} successfully synchronized with Cow Instance.`);
                clearInterval(interval);
            }
        }, 300);
    }

    async triggerYieldEscalation() {
        this.forensicYieldState.status = 'AUDITING';
        this.recordEvent('FORENSIC_AUDIT_INIT', 'Initiating high-assurance audit loop across all yield layers.');

        await new Promise(r => setTimeout(r, 2000));

        this.forensicYieldState.total += (Math.random() * 0.1);
        this.forensicYieldState.status = 'VERIFIED';
        this.recordEvent('FORENSIC_AUDIT_COMPLETE', 'Audit finalized. 0xDEAD_RECKONING avoided. Yield verified.');
    }

    async onboardSyntheticCitizen() {
        this.recordEvent('SYNTHETIC_ONBOARD_INIT', 'Initializing high-assurance synthetic citizen manifest.');
        await icpService.simulateSyntheticCitizen();
        this.resonance = 98.4;
        this.recordEvent('PASSPORT_ELGIBILITY_CONFIRMED', 'Resonance profile met Overseer standards. Passport manifestation unlocked.');
    }

    async runMeshStressDrill() {
        return meshStressEngine.runDrill();
    }


    get ambientMood() {
        return this.resonance < 85 ? 'VIGILANT' : 'STABLE';
    }

    // ═══════════════════════════════════════════════════════════════
    // AGENT GATEWAY INTEGRATION (InfoQ: Least-Privilege AI Gateway)
    // "Trust in agents is something you observe, measure, and enforce."
    // ═══════════════════════════════════════════════════════════════

    private _initAgentGateway() {
        // Wire the gateway's context resolver to live manifold state
        agentGateway.setContextResolver(() => ({
            currentResonance: this.resonance,
            permissionLevel: this.permissionLevel,
            isTurbulence: this.turbulence,
            isMoatActive: this.isMoatActive,
            timeOfDay: new Date().getHours(),
            dayOfWeek: new Date().getDay(),
            activeJobCount: agentGateway.metrics.activeJobs,
        }));

        // Subscribe to gateway events for manifold-level observability
        agentGateway.subscribe((event) => {
            this._gatewayEvents = [event, ...this._gatewayEvents].slice(0, 100);
            this.gatewayPolicyCount = agentGateway.getPolicies().length;

            // Auto-record critical gateway events into the causal log
            if (event.type === 'POLICY_DENIED' || event.type === 'EXECUTION_FAILED' || event.type === 'SLO_VIOLATION') {
                this.recordEvent(`GATEWAY_${event.type}`, JSON.stringify(event.payload));
            }
        });

        this.gatewayPolicyCount = agentGateway.getPolicies().length;
        this.recordEvent('GATEWAY_INIT', 'Sovereign Agent Gateway initialized with least-privilege controls.');
    }

    /** Get the gateway instance for submitting agent requests. */
    get gateway() {
        return agentGateway;
    }

    // ═══════════════════════════════════════════════════════════════
    // zkEVM ATTESTER METHODS (Ansgar Dietrichs — Bankless Feb 2026)
    // "Don't re-execute. Verify the proof."
    // ═══════════════════════════════════════════════════════════════

    verifyStateTransition(proofHash: string, backend: string, clientSide = true) {
        return zkAttesterEngine.verifyStateTransition(proofHash, backend, clientSide);
    }

    batchVerifyProofs(proofs: { hash: string; backend: string; clientSide: boolean }[]) {
        return zkAttesterEngine.batchVerifyProofs(proofs);
    }


    recordSnapshot(columns: any[], label: string) {
        const snap = {
            id: `SNAP-0x${Date.now().toString(16).toUpperCase()}`,
            timestamp: Date.now(),
            label,
            columns: JSON.parse(JSON.stringify(columns))
        };
        this.causalSnapshots = [snap, ...this.causalSnapshots].slice(0, 10);
        this.recordEvent('SNAPSHOT_CREATED', `Manifold state captured: ${label}`);
    }

    restoreSnapshot(id: string) {
        const snap = this.causalSnapshots.find(s => s.id === id);
        if (snap) {
            this.recordEvent('SNAPSHOT_RESTORED', `Reverting to: ${snap.label}`);
            return JSON.parse(JSON.stringify(snap.columns));
        }
    }

    startSimulation(objective: string) {
        this.isSimulating = true;
        simulationEngine.start();
        this.recordEvent('SIMULATION_STARTED', `Objective: ${objective}`);
    }

    stopSimulation() {
        this.isSimulating = false;
        simulationEngine.stop();
        this.recordEvent('SIMULATION_STOPPED', 'Experimental heartbeat disengaged.');
    }

    toggleDesignMode() {
        this.isDesignMode = !this.isDesignMode;
        if (this.isDesignMode) {
            this.designPatches = [];
        }
    }

    commitDesign(columns: any[]) {
        this.isDesignMode = false;
        this.designPatches = [];
        this.recordEvent('DESIGN_COMMITTED', 'Structural modifications finalized.');
        return columns;
    }

    // --- MANIFOLD ACTION METHODS ---
    voteCourtCase(caseId: string, vote: 'APPROVE' | 'DENY' | 'ABSTAIN') {
        const c = this.governanceState.courtCases.find((x) => x.id === caseId);
        if (c) c.status = vote === 'APPROVE' ? 'ALLOW' : (vote === 'DENY' ? 'DENY' : 'PENDING');
            // @ts-ignore
        this.recordEvent('VOTE_CAST', `Voted ${vote} on ${caseId}`);
    }

    fabricateWafer(region: string, template: string) {
        this.governanceState.lawWafers.push({ id: `WAFER-0x${Date.now()}`, template, region, status: 'FABRICATING', progress: 0.1 });
        this.recordEvent('FABRICATION_STARTED', `Wafer template ${template} for ${region}`);
    }

    get substrateAtlas() {
        return { points: [] as { id: string, label: string, region: string, scarcity: string, status: string, tps: number }[] };
    }

    claimDividend() {
        this.ageCredits += Math.random() * 100;
        this.recordEvent('DIVIDEND_CLAIMED', 'Moral dividend claimed');
    }

    createJob(title: string, reward: number) {
        this.businessState.activeJobs.push({ id: `JOB-${Date.now()}`, title, reward, status: 'QUEUED', progress: 0 });
        this.recordEvent('JOB_CREATED', `Job ${title} created`);
    }

    triggerMultiversalStressTest() {
        this.recordEvent('STRESS_TEST', 'Multiversal stress test triggered');
    }

    spawnMultiversalShard() {
        this.multiversalState.activeShards.push(`Shard-${Math.floor(Math.random() * 1000)}`);
        this.recordEvent('SHARD_SPAWNED', 'New shard spawned');
    }

    purchasePlan(id: string, price: number) {
        this.ageCredits -= price;
        this.ownedPlans.push(id);
        this.recordEvent('PLAN_PURCHASED', `Plan ${id} purchased`);
    }

    stakeCompute(pool: string) {
        this.recordEvent('COMPUTE_STAKED', `Compute staked in ${pool}`);
    }

    simulateAgoraVolitivity() {
        this.recordEvent('SIMULATION', 'Agora volitivity simulated');
    }

    stakeCognitiveEpoch(id: string) {
        this.recordEvent('EPOCH_STAKED', `Cognitive epoch ${id} staked`);
    }

    runLCLBreachSimulation() {
        this.recordEvent('SIMULATION', 'LCL Breach simulated');
    }

    rebalanceLocalEconomy() {
        this.recordEvent('ECONOMY_REBALANCED', 'Local economy rebalanced');
    }

    decayValidatorReputation() {
        this.recordEvent('REPUTATION_DECAY', 'Validator reputation decayed');
    }

    issueSyntheticMerits() {
        this.recordEvent('MERITS_ISSUED', 'Synthetic merits issued');
    }

    processPayment(_recipient: string, amount: number, _reason?: string) {
        this.ageCredits -= amount;
        this.recordEvent('PAYMENT_PROCESSED', `${amount} processed`);
        return true;
    }

    runFullAudit() {
        this.auditState.isAuditing = true;
        this.recordEvent('AUDIT_STARTED', 'Full audit started');
    }

    placeSpectralOrder(side: OrderSide, price: number, size: number) {
        this.recordEvent('ORDER_PLACED', `${side} order for ${size} @ ${price}`);
    }

    stopStress() {
        this.stressLabState.fuzzing = false;
        this.recordEvent('STRESS_STOPPED', 'Stress stopped');
    }

    chaosFuzzStress() {
        this.stressLabState.fuzzing = true;
        this.recordEvent('STRESS_STARTED', 'Chaos fuzz stress started');
    }

    boostConvergence() {
        this.singularityState.convergence += 0.1;
        this.recordEvent('CONVERGENCE_BOOSTED', 'Convergence boosted');
    }

    async hardReset() {
        if (browser) {
            localStorage.clear();
            window.location.reload();
        }
    }
}

// 🏛️ Sovereign Manifold implementation remains above...

// --- SINGLETON EXPORTS ---

// Always export an instance, but ensure it's safe for SSR by checking 'browser' inside methods and constructor.
const manifoldInstance = new SovereignManifold();
export const manifold = manifoldInstance;

export const systemHealth = {
    get resonance() { return manifold.resonance; },
    get status() { return (manifold.status === 'COHERENT') ? 'healthy' : 'degraded' },
    get layers() { return manifold.activeLayers; },
    get quietMode() { return sovereignStore?.state?.preferences?.quietMode ?? false; }
};

export { sovereignStore, telemetryStore, vaultStore, hearthStore, governanceStore, conciergeStore, dashboardStore, onboardingStore, authStore };

// Export constants from constants file
export {
    MEMORY_TYPES,
    RESONANCE_TIERS,
    CONCIERGE_PERSONALITIES,
    PROPOSAL_TYPES,
    PROPOSAL_STATUS
} from './constants';

export type * from '$lib/types';
