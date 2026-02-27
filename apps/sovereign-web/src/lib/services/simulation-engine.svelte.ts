import { browser } from '$app/environment';
import { manifold } from '$lib/stores/master-store.svelte';
import { metabolicEngine } from './metabolic-engine.svelte';
import { tokenomicsEngine } from './tokenomics-engine.svelte';
import { auditEngine } from './audit-engine.svelte';
import { sovereignFluxer } from './fluxer-engine.svelte';
import { sovereignEdgeScaler } from './edge-scaler.svelte';
import { computeEngine } from './compute-engine.svelte';
import { validatorEngine } from './validator-engine.svelte';
import { tradingEngine } from './sovereign-trading-engine.svelte';
import { neuralSensor } from './neural-sensor-service.svelte';

// ═══════════════════════════════════════════════════════════════════════════════
// 💓 SOVEREIGN SIMULATION ENGINE (Single Tick Orchestrator)
// ═══════════════════════════════════════════════════════════════════════════════
// [IN]:  manifold, metabolicEngine, tokenomicsEngine
// [OUT]: simulationEngine (singleton)
// [POS]: The ONE place all metabolic drift, resonance, kernel lane traffic,
//        and tokenomics epoch ticks originate. Eliminates dual-timer race
//        conditions between metabolic-engine.svelte.ts and master-store.
//        Also provides persistence sync scaffolding for cross-device state.
// ═══════════════════════════════════════════════════════════════════════════════

interface SimulationSnapshot {
    timestamp: number;
    resonance: number;
    tvlUsd: number;
    stablecoinParity: number;
    hilbertIndex: number;
    computeDemand: number;
}

const TICK_INTERVAL_MS = 3000;
const SNAPSHOT_INTERVAL_TICKS = 20; // Every ~60 seconds
const MAX_SNAPSHOTS = 100;

class SimulationEngine {
    private _interval: ReturnType<typeof setInterval> | null = null;
    private _isRunning = $state(false);
    private _tickCount = $state(0);
    private _snapshots = $state<SimulationSnapshot[]>([]);

    get isRunning() { return this._isRunning; }
    get tickCount() { return this._tickCount; }
    get snapshots() { return this._snapshots; }

    /** The latest metabolic vitals at a glance. */
    get vitals() {
        return {
            resonance: manifold.resonance,
            tvl: metabolicEngine.vault.totalValueLockedUsd,
            parity: metabolicEngine.stablecoin.parity,
            parityStatus: metabolicEngine.stablecoin.status,
            hilbert: manifold.hilbertState.index,
            compute: manifold.computeMarket.demandIndex,
            epoch: this._tickCount,
        };
    }

    start() {
        if (!browser || this._isRunning) return;

        this._isRunning = true;
        this._interval = setInterval(() => this._tick(), TICK_INTERVAL_MS);
    }

    stop() {
        if (this._interval) {
            clearInterval(this._interval);
            this._interval = null;
        }
        this._isRunning = false;
    }

    /** Force an immediate tick (for testing or UI trigger). */
    pulse() {
        this._tick();
    }

    private _tick() {
        this._tickCount++;

        // ──────────────────────────────────────────────────────────────────
        // 1. MANIFOLD RESONANCE DRIFT
        //    The core "health" signal. Biased slightly upward to represent
        //    the natural tendency of a healthy system toward equilibrium.
        // ──────────────────────────────────────────────────────────────────
        const resonanceDelta = (Math.random() - 0.48) * 2; // slight upward bias
        manifold.resonance = Math.max(70, Math.min(100, manifold.resonance + resonanceDelta));

        // ──────────────────────────────────────────────────────────────────
        // 2. KERNEL LANE TRAFFIC DRIFT
        //    Each lane gets independent jitter to simulate real network load.
        // ──────────────────────────────────────────────────────────────────
        if (manifold.kernelState?.lanes) {
            manifold.kernelState.lanes.forEach(l => {
                l.traffic = Math.max(0, Math.min(100, l.traffic + (Math.random() - 0.5) * 15));
            });
        }

        // ──────────────────────────────────────────────────────────────────
        // 3. METABOLIC DRIFT (Stablecoin & Vault)
        //    Parity drift is mean-reverting toward 1.0. TVL accrues slowly.
        // ──────────────────────────────────────────────────────────────────
        const metabolic = metabolicEngine.state;
        const parityDrift = (Math.random() - 0.5) * 0.002;
        metabolic.stablecoin.parity += parityDrift;

        // Mean-revert parity toward 1.0 with a 5% correction factor
        metabolic.stablecoin.parity += (1.0 - metabolic.stablecoin.parity) * 0.05;

        // Update parity status
        const parityDev = Math.abs(metabolic.stablecoin.parity - 1.0);
        metabolic.stablecoin.status = parityDev > 0.01 ? 'DEPEGGED' : parityDev > 0.005 ? 'DRIFTING' : 'PEGGED';

        // TVL accrual (yield)
        metabolic.vault.totalValueLockedUsd *= (1 + (Math.random() - 0.45) * 0.001);

        // ──────────────────────────────────────────────────────────────────
        // 4. HILBERT SPACE DRIFT (Sovereign Manifold Index)
        // ──────────────────────────────────────────────────────────────────
        manifold.hilbertState.index = Math.max(0.1, Math.min(1.0,
            manifold.hilbertState.index + (Math.random() - 0.5) * 0.001
        ));

        // ──────────────────────────────────────────────────────────────────
        // 5. COMPUTE MARKET DEMAND PULSE
        // ──────────────────────────────────────────────────────────────────
        manifold.computeMarket.demandIndex = Math.max(0.2, Math.min(1.0,
            manifold.computeMarket.demandIndex + (Math.random() - 0.5) * 0.08
        ));

        // ──────────────────────────────────────────────────────────────────
        // 6. TOKENOMICS ARI DECAY (micro-epoch)
        //    We handle the micro-epoch here so the tokenomicsEngine
        //    doesn't need its own timer.
        // ──────────────────────────────────────────────────────────────────
        // Handled by tokenomics engine's internal timer for now

        // ──────────────────────────────────────────────────────────────────
        // 7. FLUXER ENGINE TICK (real-time communication metrics)
        //    Replaces the Fluxer's orphan setInterval.
        // ──────────────────────────────────────────────────────────────────
        sovereignFluxer.tick();

        // ──────────────────────────────────────────────────────────────────
        // 8. AUDIT ENGINE TICK (every 10 ticks ≈ 30s)
        //    Replaces the AuditEngine's orphan setInterval.
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount % 10 === 0) {
            auditEngine.tick();
        }

        // ──────────────────────────────────────────────────────────────────
        // 9. TOKENOMICS ENGINE TICK (ARI decay + market cap drift)
        //    Runs every 5th tick (~15s). Was an orphan setInterval at 1h/24.
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount % 5 === 0) {
            tokenomicsEngine.tick();
        }

        // ──────────────────────────────────────────────────────────────────
        // 10. EDGE SCALER TICK (replica drift + proactive scaling)
        //    Replaces the EdgeScaler's orphan setInterval.
        // ──────────────────────────────────────────────────────────────────
        sovereignEdgeScaler.tick();

        // ──────────────────────────────────────────────────────────────────
        // 11. COMPUTE ENGINE TICK (job lifecycle)
        //     Every 5th tick (~15s) matches original job cadence.
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount % 5 === 0) {
            computeEngine.tick();
        }

        // ──────────────────────────────────────────────────────────────────
        // 12. VALIDATOR ENGINE TICK (network churn)
        //     Every 3rd tick (~9s ≈ 10s original).
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount % 3 === 0) {
            validatorEngine.tick();
        }

        // ──────────────────────────────────────────────────────────────────
        // 13. TRADING ENGINE TICK (market drift, prediction odds, agent P&L)
        //     Every tick for real-time market fidelity.
        // ──────────────────────────────────────────────────────────────────
        tradingEngine.tick();

        // ──────────────────────────────────────────────────────────────────
        // 14. NEURAL SENSOR LAZY START (100ms animation, self-managed)
        //     Boots its own fast loop on first heartbeat.
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount === 1) {
            neuralSensor.start();
        }

        // ──────────────────────────────────────────────────────────────────
        // 15. HEARTBEAT TIMESTAMP
        // ──────────────────────────────────────────────────────────────────
        manifold.lastHeartbeat = Date.now();

        // ──────────────────────────────────────────────────────────────────
        // 16. PERIODIC SNAPSHOT (for persistence/analytics)
        // ──────────────────────────────────────────────────────────────────
        if (this._tickCount % SNAPSHOT_INTERVAL_TICKS === 0) {
            this._captureSnapshot();
        }
    }

    private _captureSnapshot() {
        const snap: SimulationSnapshot = {
            timestamp: Date.now(),
            resonance: manifold.resonance,
            tvlUsd: metabolicEngine.vault.totalValueLockedUsd,
            stablecoinParity: metabolicEngine.stablecoin.parity,
            hilbertIndex: manifold.hilbertState.index,
            computeDemand: manifold.computeMarket.demandIndex,
        };
        this._snapshots = [snap, ...this._snapshots].slice(0, MAX_SNAPSHOTS);

        // 🔮 PERSISTENCE SYNC HOOK
        // In production, this is where we'd push to the Postgres/KV store
        // via the Elixir backplane for cross-device state synchronization:
        //   fetch('/api/manifold/snapshot', { method: 'POST', body: JSON.stringify(snap) });
    }
}

export const simulationEngine = new SimulationEngine();
