import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import type { TelemetryState, TelemetryLog, SystemVitals } from '$lib/types';

const initialState: TelemetryState = {
    logs: [
        {
            id: '1',
            level: 'info',
            module: 'system',
            message: 'Dashboard initialized',
            timestamp: new Date()
        }
    ],
    vitals: {
        cpu: 23,
        memory: 45,
        networkLatency: 187,
        syncStatus: 'synced',
        activeConnections: 3,
        resonance: 98 // Default resonance
    },
    resonance: 98,
    layersActive: 20,
    alerts: []
};

function createTelemetryStore() {
    const stored = loadFromStorage<TelemetryState>('telemetry', initialState);

    // Restore dates
    if (stored.logs) {
        stored.logs = stored.logs.map(l => ({
            ...l,
            timestamp: new Date(l.timestamp)
        }));
    }

    if (stored.alerts) {
        stored.alerts = stored.alerts.map(a => ({
            ...a,
            timestamp: new Date(a.timestamp)
        }));
    }

    const { subscribe, set, update } = writable<TelemetryState>(stored);

    return {
        subscribe,

        addLog: (log: Omit<TelemetryLog, 'id' | 'timestamp'>) =>
            update((state: TelemetryState) => {
                const newLog: TelemetryLog = {
                    ...log,
                    id: crypto.randomUUID(),
                    timestamp: new Date()
                };

                const newState: TelemetryState = {
                    ...state,
                    logs: [newLog, ...state.logs].slice(0, 100)
                };

                saveToStorage('telemetry', newState);
                return newState;
            }),

        updateVitals: (vitals: Partial<SystemVitals>) =>
            update((state: TelemetryState) => {
                const newState: TelemetryState = {
                    ...state,
                    vitals: { ...state.vitals, ...vitals }
                };
                saveToStorage('telemetry', newState);
                return newState;
            }),

        addAlert: (alert: Omit<TelemetryState['alerts'][0], 'id' | 'timestamp'>) =>
            update((state: TelemetryState) => {
                const newAlert = {
                    ...alert,
                    id: crypto.randomUUID(),
                    timestamp: new Date()
                };

                const newState: TelemetryState = {
                    ...state,
                    alerts: [newAlert, ...state.alerts].slice(0, 20)
                };

                saveToStorage('telemetry', newState);
                return newState;
            }),

        clearLogs: () => update((state: TelemetryState) => {
            const newState: TelemetryState = {
                ...state,
                logs: []
            };
            saveToStorage('telemetry', newState);
            return newState;
        }),
        update
    };
}

export const telemetryStore = createTelemetryStore();
