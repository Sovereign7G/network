// Sovereign DaVinci Constants

export const MEMORY_TYPES = {
    GRATITUDE: { id: 'gratitude', label: 'Gratitude', name: 'Gratitude', color: '#FFD700', icon: '🙏', resonance: 10 },
    INSIGHT: { id: 'insight', label: 'Insight', name: 'Insight', color: '#4CAF50', icon: '💡', resonance: 15 },
    MILESTONE: { id: 'milestone', label: 'Milestone', name: 'Milestone', color: '#2196F3', icon: '🎯', resonance: 25 },
    RECOVERY: { id: 'recovery', label: 'Recovery', name: 'Recovery', color: '#FF9800', icon: '🔨', resonance: 20 },
    ACHIEVEMENT: { id: 'achievement', label: 'Achievement', name: 'Achievement', color: '#9C27B0', icon: '🏆', resonance: 30 }
} as const;

export const RESONANCE_TIERS_DATA = {
    AWAKENING: { threshold: 0, color: '#666666', name: 'Awakening', title: 'Awakening', icon: '✨' },
    EMERGENT: { threshold: 100, color: '#4CAF50', name: 'Emergent', title: 'Emergent', icon: '🌱' },
    COHERENT: { threshold: 500, color: '#2196F3', name: 'Coherent', title: 'Coherent', icon: '🌊' },
    SOVEREIGN: { threshold: 1000, color: '#FFD700', name: 'Sovereign', title: 'Sovereign', icon: '👑' },
    TRANSCENDENT: { threshold: 5000, color: '#9C27B0', name: 'Transcendent', title: 'Transcendent', icon: '🌌' }
} as const;

// Keep an array version for backward compatibility where needed
export const RESONANCE_TIERS = Object.values(RESONANCE_TIERS_DATA);

export const CONCIERGE_PERSONALITIES = [
    { id: 'wise', name: 'Wise Sage', description: 'Thoughtful, measured advice', icon: '🧙', color: '#9370DB' },
    { id: 'dynamic', name: 'Dynamic Strategist', description: 'Bold, action-oriented', icon: '⚡', color: '#FFD700' },
    { id: 'nurturing', name: 'Nurturing Guide', description: 'Supportive, encouraging', icon: '🧘', color: '#FF6B6B' },
    { id: 'analytical', name: 'Analytical Mind', description: 'Data-driven, precise', icon: '📊', color: '#4ECDC4' }
] as const;

export const PROPOSAL_TYPES = {
    TREASURY: { id: 'treasury', label: 'Treasury Allocation', name: 'Treasury', icon: '💰', color: '#FFD700' },
    PARAMETER: { id: 'parameter', label: 'Parameter Change', name: 'Parameter', icon: '⚙️', color: '#4ECDC4' },
    UPGRADE: { id: 'upgrade', label: 'Protocol Upgrade', name: 'Upgrade', icon: '🚀', color: '#9370DB' },
    SOCIAL: { id: 'social', label: 'Social Contract', name: 'Social', icon: '🤝', color: '#FF6B6B' },
    EMERGENCY: { id: 'emergency', label: 'Emergency Action', name: 'Emergency', icon: '⚠️', color: '#FF4444' }
} as const;

export const PROPOSAL_STATUS = {
    PENDING: { id: 'pending', label: 'Pending', name: 'Pending', icon: '⏳', color: '#666666' },
    ACTIVE: { id: 'active', label: 'Active', name: 'Active', icon: '🗳️', color: '#4ECDC4' },
    PASSED: { id: 'passed', label: 'Passed', name: 'Passed', icon: '✅', color: '#4CAF50' },
    FAILED: { id: 'failed', label: 'Failed', name: 'Failed', icon: '❌', color: '#FF6B6B' },
    EXECUTED: { id: 'executed', label: 'Executed', name: 'Executed', icon: '⚡', color: '#9370DB' }
} as const;
