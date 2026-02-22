export type A2UIComponent =
    | InstructionComponent
    | VisualOverlayComponent
    | ActionComponent
    | PrivacyComponent
    | AmbientComponent
    | VerificationComponent;

export interface InstructionComponent {
    type: 'instruction';
    text: string;
    voiceUrl?: string;
    severity?: 'info' | 'warning' | 'critical';
}

export interface VisualOverlayComponent {
    type: 'visual_overlay';
    targetRegion?: { x: number, y: number, width: number, height: number };
    shape: 'rect' | 'circle' | 'pulse';
    color: string; // hex
}

export interface ActionComponent {
    type: 'action';
    actionName: string;
    params?: Record<string, any>;
    hapticPattern?: number[];
}

export interface PrivacyComponent {
    type: 'privacy';
    peekerDetected: boolean;
    blurIntensity: number;
    maskingEffect?: 'blur' | 'digital_frost' | 'none';
}

export interface AmbientComponent {
    type: 'ambient';
    mood: 'STABLE' | 'CHAOTIC' | 'CALM' | 'BULLISH' | 'GOVERNANCE_SYNC' | 'HARDENED_LAW';
    baseColor: string;
    intensity?: number;
    turbulence?: number;
}

export interface VerificationComponent {
    type: 'verification';
    threshold: number;
    referenceImageBase64?: string;
    livenessRequired: boolean;
}

export interface A2UIFrame {
    agentId: string;
    sessionId: string;
    components: A2UIComponent[];
    metadata?: Record<string, any>;
    priority?: 'standard' | 'high' | 'critical';
}
