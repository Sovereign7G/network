import { writable } from 'svelte/store';

export const authStatus = writable('onboarding'); // 'onboarding', 'security', 'authenticated'
export const hasSeenTutorial = writable(false);
export const aal3Status = writable(true); // NIST AAL3 Certified

export const completeOnboarding = () => authStatus.set('security');
export const completeSecurity = () => authStatus.set('authenticated');
export const markTutorialSeen = () => hasSeenTutorial.set(true);
