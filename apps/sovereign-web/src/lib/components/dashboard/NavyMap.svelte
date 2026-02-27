<script lang="ts">
//     import { onMount, onDestroy } from "svelte";
    import { NavyMap } from "../../../../../../packages/age-navy/src/three/NavyMap";
    import { telemetryStore } from "$lib/stores/telemetry-store.svelte";

    let container: HTMLElement;
    let navyMap: NavyMap;
    let unsubscribe: () => void;

    onMount(() => {
        if (container) {
            navyMap = new NavyMap(container);


            unsubscribe = telemetryStore.subscribe((data) => {
                navyMap.updateTelemetry(data);
            });

            const resizeObserver = new ResizeObserver((entries) => {
                for (let entry of entries) {
                    const { width, height } = entry.contentRect;
                    navyMap.resize(width, height);
                }
            });

            resizeObserver.observe(container);

            return () => {
                resizeObserver.disconnect();
                if (unsubscribe) unsubscribe();
                navyMap.destroy();
            };
        }
    });
</script>

<div class="navy-container">
    <div class="navy-header">
        <h3>🚢 OCEANIC LOGISTICS (NAVY MAP)</h3>
        <span class="status">LIVE • SECTOR 7</span>
    </div>
    <div bind:this={container} class="map-viewport"></div>
</div>

<style>
    .navy-container {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        overflow: hidden;
        height: 400px;
        display: flex;
        flex-direction: column;
    }

    .navy-header {
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .navy-header h3 {
        margin: 0;
        font-size: 0.9rem;
        color: #4ecdc4;
        letter-spacing: 1px;
    }

    .status {
        font-size: 0.7rem;
        background: rgba(78, 205, 196, 0.1);
        color: #4ecdc4;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
    }

    .map-viewport {
        flex: 1;
        position: relative;
        cursor: move;
    }
</style>
