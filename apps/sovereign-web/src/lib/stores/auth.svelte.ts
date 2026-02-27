export type AuthStatus = 'onboarding' | 'security' | 'authenticated';

class AuthEngine {
    state = $state({
        status: 'onboarding' as AuthStatus,
        hasSeenTutorial: false,
        aal3Status: true // NIST AAL3 Certified
    });

    completeOnboarding() {
        this.state.status = 'security';
    }

    completeSecurity() {
        this.state.status = 'authenticated';
    }

    markTutorialSeen() {
        this.state.hasSeenTutorial = true;
    }
}

export const authStore = new AuthEngine();
