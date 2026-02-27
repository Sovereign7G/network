import { browser } from '$app/environment';
import type { TelemetryMetric, TelemetryPoint, TelemetryBatch } from '../types/telemetry.types';

class RUMMonitor {
    private batch: TelemetryPoint[] = [];
    private readonly BATCH_SIZE = 100;
    private readonly FLUSH_INTERVAL = 30000; // 30 seconds

    private sessionId = Math.random().toString(36).substring(7).toUpperCase();
    private flushTimer: ReturnType<typeof setInterval>;

    constructor() {
        this.flushTimer = setInterval(() => this.flush(), this.FLUSH_INTERVAL);

        if (browser) {
            // Page unload flush
            window.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {
                    this.flush();
                }
            });

            this.init();
        }
    }

    private init() {
        this.trackTTFB();
        this.trackFCP();
        this.trackLCP();
        this.trackFID();
        this.trackCLS();

        window.addEventListener('error', (e) => {
            this.trackError(e.message, e.error?.stack);
        });

        window.addEventListener('unhandledrejection', (e) => {
            this.trackError(e.reason?.message || "Unhandled Promise Rejection", e.reason?.stack);
        });
    }

    public track(metric: TelemetryMetric, value: number, tags?: Record<string, string>): void {
        if (!browser) return;

        this.batch.push({
            metric,
            value,
            timestamp: Date.now(),
            tags
        });

        if (this.batch.length >= this.BATCH_SIZE) {
            this.flush();
        }
    }

    private trackTTFB() {
        try {
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntriesByType('navigation');
                if (entries.length > 0) {
                    const navEntry = entries[0] as PerformanceNavigationTiming;
                    this.track('ttfb', navEntry.responseStart);
                }
            }).observe({ type: 'navigation', buffered: true });
        } catch { /* Suppress on unsupported browsers */ }
    }

    private trackFCP() {
        try {
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntriesByName('first-contentful-paint');
                if (entries.length > 0) {
                    this.track('fcp', entries[0].startTime);
                }
            }).observe({ type: 'paint', buffered: true });
        } catch { }
    }

    public trackLCP(): void {
        try {
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                if (entries.length > 0) {
                    const lastEntry = entries[entries.length - 1];
                    if (lastEntry) {
                        this.track('lcp', lastEntry.startTime);
                    }
                }
            }).observe({ type: 'largest-contentful-paint', buffered: true });
        } catch { }
    }

    public trackFID(): void {
        try {
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                if (entries.length > 0) {
                    const firstInput = entries[0] as PerformanceEventTiming;
                    const delay = firstInput.processingStart - firstInput.startTime;
                    this.track('fid', delay);
                }
            }).observe({ type: 'first-input', buffered: true });
        } catch { }
    }

    private trackCLS() {
        try {
            let clsValue = 0;
            new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    const layoutShift = entry as any;
                    if (!layoutShift.hadRecentInput) {
                        clsValue += layoutShift.value;
                        this.track('cls', clsValue);
                    }
                }
            }).observe({ type: 'layout-shift', buffered: true });
        } catch { }
    }

    trackInteraction(name: string, duration: number) {
        if (!browser) return;
        this.track('interaction', duration, { name });
    }

    trackError(message: string, stack?: string, component?: string) {
        if (!browser) return;
        this.track('interaction', 0, { type: 'error', message, stack: stack || '', component: component || '' });
    }

    private async flush(): Promise<void> {
        if (this.batch.length === 0) return;

        const batch: TelemetryBatch = {
            id: Math.random().toString(36).substring(7).toUpperCase(),
            points: [...this.batch],
            sessionId: this.sessionId,
            timestamp: Date.now(),
            version: '5.42.0'
        };

        this.batch = [];

        // Send in background, don't block
        if (browser && navigator.onLine) {
            fetch('/api/telemetry', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(batch),
                keepalive: true
            }).catch(() => { /* silent fail */ });
        }
    }

    public destroy(): void {
        clearInterval(this.flushTimer);
        this.flush();
    }

    public getReport(): any {
        return {
            points: this.batch,
            sessionId: this.sessionId,
            timestamp: Date.now()
        };
    }
}

const rumMonitor = new RUMMonitor();
