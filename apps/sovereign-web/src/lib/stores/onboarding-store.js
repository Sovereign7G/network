import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const ONBOARDING_STEPS = {
    WELCOME: 'welcome',
    IDENTITY: 'identity',
    SEAL: 'seal'
};

const initialState = {
    currentStep: ONBOARDING_STEPS.WELCOME,
    completed: false,
    data: {
        displayName: '',
        handle: '',
        bio: '',
        avatar: null,
        interests: [],
        verificationLevel: 1,
        acceptedTerms: false,
        acceptedProtocol: false
    },
    progress: 0
};

function createOnboardingStore() {
    const { subscribe, set, update } = writable(initialState);

    return {
        subscribe,

        setStep: (step) => update(state => {
            const steps = Object.values(ONBOARDING_STEPS);
            const stepIndex = steps.indexOf(step);
            const progress = ((stepIndex + 1) / steps.length) * 100;

            return {
                ...state,
                currentStep: step,
                progress
            };
        }),

        nextStep: () => update(state => {
            const steps = Object.values(ONBOARDING_STEPS);
            const currentIndex = steps.indexOf(state.currentStep);

            if (currentIndex < steps.length - 1) {
                const nextStep = steps[currentIndex + 1];
                const progress = ((currentIndex + 2) / steps.length) * 100;

                return {
                    ...state,
                    currentStep: nextStep,
                    progress
                };
            }

            return state;
        }),

        previousStep: () => update(state => {
            const steps = Object.values(ONBOARDING_STEPS);
            const currentIndex = steps.indexOf(state.currentStep);

            if (currentIndex > 0) {
                const prevStep = steps[currentIndex - 1];
                const progress = (currentIndex / steps.length) * 100;

                return {
                    ...state,
                    currentStep: prevStep,
                    progress
                };
            }

            return state;
        }),

        updateData: (data) => update(state => ({
            ...state,
            data: { ...state.data, ...data }
        })),

        completeOnboarding: () => update(state => ({
            ...state,
            completed: true,
            progress: 100
        })),

        reset: () => set(initialState)
    };
}

export const onboardingStore = createOnboardingStore();
