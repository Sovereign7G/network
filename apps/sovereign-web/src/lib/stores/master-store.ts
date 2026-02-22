import { derived } from 'svelte/store';
import { sovereignStore } from './sovereign-store';
import { telemetryStore } from './telemetry-store';

// Re-export constants
export * from './constants';

// Re-export stores
export { sovereignStore } from './sovereign-store';
export { hearthStore } from './hearth-store';
export { vaultStore } from './vault-store';
export { governanceStore } from './governance-store';
export { telemetryStore } from './telemetry-store';
export const resonanceStore = derived(telemetryStore, $t => ({ score: $t.resonance }));
export { conciergeStore } from './concierge-store';
export { bountyTheatre } from '../../../../../packages/age-commerce/src/store/bounty-store';
export { crmStore } from '../../../../../packages/age-crm/src/store/crm-store';
export { spatialStore } from '../../../../../packages/age-spatial/src/store/spatial-store';
export { telecomStore } from '../../../../../packages/age-telecom/src/store/telecom-store';
export { audioStore } from '../../../../../packages/age-audio/src/store/audio-store';
export { cloudStore } from '../../../../../packages/age-cloud/src/store/cloud-store';

// Derived System Health Store
export const systemHealth = derived(
    [sovereignStore, telemetryStore],
    ([$sovereign, $telemetry]) => ({
        status: $telemetry.vitals.syncStatus === 'synced' ? 'healthy' : 'degraded',
        quietMode: $sovereign.preferences.quietMode,
        resonance: $telemetry.resonance,
        layersActive: $telemetry.layersActive
    })
);

// Re-export types for convenience
export type * from '$lib/types';

