<script lang="ts">
    import { onMount } from "svelte";
    import { createSonicSovereignty } from "../../../../../../packages/age-sensory/src/index";
    import { telemetryStore } from "$lib/stores/telemetry-store";

    let resonance = 0;
    let latency = 0;
    let alerts = 0;
    let saves: any[] = [];

    const sonic = createSonicSovereignty();

    onMount(() => {
        const unsubscribe = telemetryStore.subscribe((t) => {
            // Assuming telemetryStore might need these fields added
            resonance = (t as any).resonance || 0;
            latency = t.vitals.networkLatency;
            alerts = t.alerts.length;

            sonic.update(resonance, latency, alerts);

            if (alerts > 0) {
                sonic.triggerWarning("MEDIUM");
            }
        });

        // Listen for extraction-saved events dispatch from other components
        const handleSave = (event: any) => {
            const saveEntry = {
                amount: event.detail.amount,
                timestamp: Date.now(),
            };
            saves = [saveEntry, ...saves].slice(0, 50);
            sonic.playSaveChime(event.detail.amount);
        };

        window.addEventListener("extraction-saved", handleSave as any);

        return () => {
            unsubscribe();
            window.removeEventListener("extraction-saved", handleSave as any);
            sonic.stop();
        };
    });
</script>

<div class="sonic-indicator" class:alert={alerts > 0}>
    <div class="hum-indicator">
        <div
            class="hum-meter"
            style="height: {Math.max(4, resonance / 5)}px"
        ></div>
        <span class="label">🏛️ Resonance Hum</span>
    </div>

    <div class="chimes-counter">
        <div class="stat">
            <span class="muted">🔔 Today's Saves</span>
            <span class="count">{saves.length}</span>
        </div>
        <div class="stat">
            <span class="muted">Total</span>
            <span class="total"
                >${saves.reduce((sum, s) => sum + s.amount, 0).toFixed(2)}</span
            >
        </div>
    </div>

    {#if alerts > 0}
        <div class="discordance-warning">⚠️ SECURITY ALERT ACTIVE</div>
    {/if}
</div>

<style>
    .sonic-indicator {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(10px);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.8rem;
        z-index: 1000;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #00ffcc;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        min-width: 220px;
    }

    .sonic-indicator.alert {
        border-left-color: #ff3e00;
    }

    .hum-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }

    .hum-meter {
        width: 3px;
        background: #00ffcc;
        border-radius: 2px;
        transition:
            height 0.3s ease,
            background 0.3s;
    }

    .alert .hum-meter {
        background: #ff3e00;
    }

    .label {
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    .chimes-counter {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .muted {
        color: rgba(255, 255, 255, 0.4);
    }

    .count {
        color: #00ffcc;
        font-weight: bold;
    }

    .total {
        color: #ffd700;
        font-weight: bold;
    }

    .discordance-warning {
        margin-top: 0.75rem;
        padding: 0.4rem;
        background: rgba(255, 62, 0, 0.2);
        color: #ff3e00;
        border: 1px solid #ff3e00;
        border-radius: 4px;
        animation: pulse 1.5s infinite;
        text-align: center;
        font-weight: bold;
        font-size: 0.7rem;
    }

    @keyframes pulse {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.8;
            transform: scale(0.98);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>
