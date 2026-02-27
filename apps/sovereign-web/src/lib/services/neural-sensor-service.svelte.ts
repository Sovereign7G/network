import { manifold } from '$lib/stores/master-store.svelte';

interface FrequencyBand {
    label: string;
    freq: number;
    magnitude: number;
}

interface NeuralSensorState {
    coherence: number;
    pulseRate: number;
    bands: FrequencyBand[];
    waveform: number[];
    isStressed: boolean;
}

class NeuralSensorService {
    state = $state<NeuralSensorState>({
        coherence: 0.95,
        pulseRate: 72,
        bands: [
            { label: 'DEL', freq: 2, magnitude: 0.1 },
            { label: 'THE', freq: 6, magnitude: 0.8 },
            { label: 'ALP', freq: 10, magnitude: 0.4 },
            { label: 'BET', freq: 20, magnitude: 0.2 },
            { label: 'GAM', freq: 40, magnitude: 0.05 }
        ],
        waveform: Array(50).fill(0),
        isStressed: false
    });

    private interval: ReturnType<typeof setInterval> | null = null;
    private _running = false;

    /**
     * NOTE: This service intentionally keeps its own 100ms interval.
     * The waveform animation requires 10fps minimum for visual fidelity;
     * delegating to SimEngine (3s ticks) would make it unusable.
     */
    start() {
        if (this._running) return;
        this._running = true;
        this.startSimulation();
    }

    private startSimulation() {
        this.interval = setInterval(() => {
            const manifoldResonance = manifold.resonance / 100;

            // Artificial drift with manifold influence
            this.state.coherence = Math.max(0, Math.min(1.0,
                this.state.coherence + (Math.random() - 0.48) * 0.02 + (manifoldResonance - 0.5) * 0.01
            ));

            this.state.pulseRate = Math.round(70 + (1 - this.state.coherence) * 40 + (Math.random() - 0.5) * 5);
            this.state.isStressed = this.state.coherence < 0.85;

            // Shift bands
            this.state.bands.forEach((b, i) => {
                b.magnitude = Math.max(0.05, Math.min(1.0,
                    0.5 + Math.sin(Date.now() / 1000 + i) * 0.4 + (Math.random() - 0.5) * 0.1
                ));
            });

            // Update waveform (circular buffer)
            const nextVal = Math.sin(Date.now() / 200) * 0.5 + (Math.random() - 0.5) * 0.2;
            this.state.waveform = [...this.state.waveform.slice(1), nextVal];
        }, 100);
    }

    getCoherenceGrade() {
        if (this.state.coherence > 0.95) return 'DIVINE';
        if (this.state.coherence > 0.85) return 'RESONANT';
        if (this.state.coherence > 0.70) return 'UNSTABLE';
        return 'GHOST_STATE';
    }

    stop() {
        if (this.interval) clearInterval(this.interval);
    }
}

const instance = new NeuralSensorService();
export const neuralSensor = instance;
