// import { browser } from '$app/environment';

export const ONBOARDING_STEPS = {
    WELCOME: 'welcome',
    IDENTITY: 'identity',
    SEAL: 'seal'
} as const;

export type OnboardingStep = typeof ONBOARDING_STEPS[keyof typeof ONBOARDING_STEPS];

export interface OnboardingData {
    displayName: string;
    handle: string;
    bio: string;
    avatar: string | null;
    interests: string[];
    verificationLevel: number;
    acceptedTerms: boolean;
    acceptedProtocol: boolean;
}

export interface OnboardingState {
    currentStep: OnboardingStep;
    completed: boolean;
    data: OnboardingData;
    progress: number;
}

const initialState: OnboardingState = {
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

class OnboardingEngine {
    state = $state<OnboardingState>({
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
    });

    setStep(step: OnboardingStep) {
        const steps = Object.values(ONBOARDING_STEPS);
        const stepIndex = steps.indexOf(step);
        this.state.progress = ((stepIndex + 1) / steps.length) * 100;
        this.state.currentStep = step;
    }

    nextStep() {
        const steps = Object.values(ONBOARDING_STEPS);
        const currentIndex = steps.indexOf(this.state.currentStep);

        if (currentIndex < steps.length - 1) {
            this.state.currentStep = steps[currentIndex + 1];
            this.state.progress = ((currentIndex + 2) / steps.length) * 100;
        }
    }

    previousStep() {
        const steps = Object.values(ONBOARDING_STEPS);
        const currentIndex = steps.indexOf(this.state.currentStep);

        if (currentIndex > 0) {
            this.state.currentStep = steps[currentIndex - 1];
            this.state.progress = (currentIndex / steps.length) * 100;
        }
    }

    updateData(data: Partial<OnboardingData>) {
        this.state.data = { ...this.state.data, ...data };
    }

    completeOnboarding() {
        this.state.completed = true;
        this.state.progress = 100;
    }

    reset() {
        this.state = JSON.parse(JSON.stringify(initialState));
    }
}

export const onboardingStore = new OnboardingEngine();
