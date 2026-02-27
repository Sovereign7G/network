import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { API_CONFIG } from '$lib/config/api';
            // @ts-ignore
import type { TelemetryState, TelemetryLog, SystemVitals, TelemetryAlert } from '$lib/types';

// ─── TYPES & LOGIC ──────────────────────────────────────────────────────────

const INITIAL_VITALS: SystemVitals = {
    cpu: 23,
    memory: 45,
    networkLatency: 187,
    syncStatus: 'synced',
    activeConnections: 3,
    resonance: 98,
    systemic: {
        sofr: 5.31,
        treasury10y: 4.22,
        spread: 1.09,
        oatBund: 0.54,
        eurChf: 0.98,
        wti: 78.4,
        gold: 2024.5,
        xmr: 142.3,
        xmrVolume: 1200000,
        tao: 580.4,
        render: 7.2
    }
};

// ─── THE MANIFOLD TELEMETRY ENGINE ───────────────────────────────────────────

class TelemetryEngine {
    logs = $state<TelemetryLog[]>([]);
    vitals = $state<SystemVitals>(INITIAL_VITALS);
    alerts = $state<TelemetryAlert[]>([]);

    private socket: WebSocket | null = null;
    private retryCount = 0;
    private maxRetryDelay = 30000;
    private baseRetryDelay = 1000;

    constructor() {
        if (browser) {
            const stored = loadFromStorage<Partial<TelemetryState>>('telemetry', {});

            // Rehydrate logs and alerts
            this.logs = (stored.logs || []).map(l => ({ ...l, timestamp: new Date(l.timestamp) }));
            this.alerts = (stored.alerts || []).map(a => ({ ...a, timestamp: new Date(a.timestamp) }));

            this.connect();
        }
    }

    private connect() {
        if (!browser) return;

        try {
            this.socket = new WebSocket(API_CONFIG.wsURL);

            this.socket.onopen = () => {

                // Speak Phoenix Protocol
                this.socket?.send(JSON.stringify({
                    topic: "vitals:global",
                    event: "phx_join",
                    payload: {},
                    ref: "1"
                }));

                // Heartbeat to keep connection alive
                setInterval(() => {
                    if (this.socket?.readyState === WebSocket.OPEN) {
                        this.socket.send(JSON.stringify({
                            topic: "phoenix",
                            event: "heartbeat",
                            payload: {},
                            ref: "hb"
                        }));
                    }
                }, 30000);

                this.retryCount = 0;
                this.vitals.syncStatus = 'synced';
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    // Phoenix protocol wraps payload in a message
                    // incoming broadcast: { "topic": "vitals:global", "event": "effect", "payload": { "type": "vitals", "payload": { ... } } }
                    if (data.event === 'effect' && data.payload) {
                        this.handleInbound(data.payload);
                    } else if (data.payload?.status === 'ok') {
                        // Join or heartbeat success
                    }
                } catch (e) {
                    console.error('⚠️ [Telemetry] Packet Corruption Detected:', e);
                }
            };

            this.socket.onclose = (event) => {
                console.warn('🛰️ [Telemetry] Connection Closed:', event.code, event.reason);
                this.vitals.syncStatus = 'degraded';
                this.scheduleReconnect();
            };

            this.socket.onerror = () => {
                this.socket?.close();
            };
        } catch (e) {
            this.scheduleReconnect();
        }
    }

    private handleInbound(data: any) {
        if (data.type === 'vitals') {
            Object.assign(this.vitals, data.payload);
        } else if (data.type === 'log') {
            this.addLog(data.payload);
        }
    }

    private scheduleReconnect() {
        const delay = Math.min(this.maxRetryDelay, this.baseRetryDelay * Math.pow(2, this.retryCount));
        console.warn(`🛰️ [Telemetry] Signal Lost. Reacquiring in ${(delay / 1000).toFixed(1)}s...`);

        setTimeout(() => {
            this.retryCount++;
            this.connect();
        }, delay);
    }

    // ─── EXTERNAL INTERFACE ──────────────────────────────────────────────────

    addLog(log: Omit<TelemetryLog, 'id' | 'timestamp'>) {
        const newLog: TelemetryLog = {
            ...log,
            id: crypto.randomUUID(),
            timestamp: new Date()
        };

        this.logs = [newLog, ...this.logs].slice(0, 100);
        this.persist();
    }

    addAlert(alert: Omit<TelemetryAlert, 'id' | 'timestamp'>) {
        const newAlert: TelemetryAlert = {
            ...alert,
            id: crypto.randomUUID(),
            timestamp: new Date()
        };

        this.alerts = [newAlert, ...this.alerts].slice(0, 20);
        this.persist();
    }

    updateVitals(vitals: Partial<SystemVitals>) {
        Object.assign(this.vitals, vitals);
        // We rarely persist vitals to disk as they are ephemeral real-time stream
    }

    clearLogs() {
        this.logs = [];
        this.persist();
    }

    private persist() {
        if (browser) {
            saveToStorage('telemetry', {
                logs: this.logs,
                alerts: this.alerts
            });
        }
    }
}

// 🏛️ Export singleton engine
const instance = new TelemetryEngine();
export const telemetryStore = instance;
