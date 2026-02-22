import type { MemoryType, ProposalType, ProposalStatus, Personality } from '$lib/types';

// ==================== MEMORY TYPES ====================
export const MEMORY_TYPES: Record<string, MemoryType> = {
    GRATITUDE: {
        id: 'gratitude',
        label: 'Gratitude',
        resonance: 5,
        icon: '🙏',
        color: '#FFD700',
        description: 'Moments of thankfulness and appreciation'
    },
    LESSON: {
        id: 'lesson',
        label: 'Lesson',
        resonance: 10,
        icon: '📚',
        color: '#9370DB',
        description: 'Wisdom gained from experience'
    },
    CONNECTION: {
        id: 'connection',
        label: 'Connection',
        resonance: 15,
        icon: '🤝',
        color: '#FF6B6B',
        description: 'Meaningful interactions with others'
    },
    MOMENT: {
        id: 'moment',
        label: 'Moment',
        resonance: 20,
        icon: '✨',
        color: '#4ECDC4',
        description: 'Precious instances worth remembering'
    },
    ACHIEVEMENT: {
        id: 'achievement',
        label: 'Achievement',
        resonance: 25,
        icon: '🏆',
        color: '#FFD700',
        description: 'Personal victories and milestones'
    },
    INSIGHT: {
        id: 'insight',
        label: 'Insight',
        resonance: 30,
        icon: '💡',
        color: '#45B7D1',
        description: 'Profound realizations and breakthroughs'
    }
};

// ==================== RESONANCE TIERS ====================
export const RESONANCE_TIERS = [
    { level: 1, threshold: 0, title: 'Spark', icon: '✨' },
    { level: 2, threshold: 100, title: 'Ember', icon: '🔥' },
    { level: 3, threshold: 500, title: 'Flame', icon: '🔥' },
    { level: 4, threshold: 1000, title: 'Bonfire', icon: '🔥' },
    { level: 5, threshold: 5000, title: 'Inferno', icon: '🔥' },
    { level: 6, threshold: 10000, title: 'Phoenix', icon: '🦅' }
] as const;

// ==================== PROPOSAL TYPES ====================
export const PROPOSAL_TYPES: Record<string, ProposalType> = {
    PARAMETER: { id: 'parameter', label: 'Parameter Change', icon: '⚙️', color: '#4ECDC4' },
    TREASURY: { id: 'treasury', label: 'Treasury Allocation', icon: '💰', color: '#FFD700' },
    UPGRADE: { id: 'upgrade', label: 'Protocol Upgrade', icon: '🚀', color: '#9370DB' },
    SOCIAL: { id: 'social', label: 'Social Contract', icon: '🤝', color: '#FF6B6B' },
    EMERGENCY: { id: 'emergency', label: 'Emergency', icon: '⚠️', color: '#FF4444' }
};

// ==================== PROPOSAL STATUSES ====================
export const PROPOSAL_STATUS: Record<string, ProposalStatus> = {
    DRAFT: { id: 'draft', label: 'Draft', icon: '📝', color: '#666666' },
    DISCUSSION: { id: 'discussion', label: 'Discussion', icon: '💬', color: '#45B7D1' },
    ACTIVE: { id: 'active', label: 'Active', icon: '🗳️', color: '#4ECDC4' },
    PASSED: { id: 'passed', label: 'Passed', icon: '✅', color: '#4CAF50' },
    REJECTED: { id: 'rejected', label: 'Rejected', icon: '❌', color: '#FF6B6B' },
    EXECUTED: { id: 'executed', label: 'Executed', icon: '⚡', color: '#9370DB' }
};

// ==================== CONCIERGE PERSONALITIES ====================
export const CONCIERGE_PERSONALITIES: Record<string, Personality> = {
    WISE: { id: 'wise', name: 'The Sage', icon: '🧙', description: 'Contemplative and philosophical', color: '#9370DB' },
    ANALYTICAL: { id: 'analytical', name: 'The Analyst', icon: '📊', description: 'Data-driven and precise', color: '#4ECDC4' },
    NURTURING: { id: 'nurturing', name: 'The Guide', icon: '🧘', description: 'Supportive and encouraging', color: '#FF6B6B' },
    DYNAMIC: { id: 'dynamic', name: 'The Catalyst', icon: '⚡', description: 'Energetic and action-oriented', color: '#FFD700' }
};

// ==================== CONCIERGE CAPABILITIES ====================
export const CONCIERGE_CAPABILITIES = {
    HEARTH: { id: 'hearth', name: 'Memory & Resonance', icon: '🔥', enabled: true },
    VAULT: { id: 'vault', name: 'Asset Management', icon: '💰', enabled: true },
    GOVERNANCE: { id: 'governance', name: 'Voting & Proposals', icon: '⚖️', enabled: true },
    INSIGHTS: { id: 'insights', name: 'Pattern Recognition', icon: '💡', enabled: true },
    REMINDERS: { id: 'reminders', name: 'Scheduled Actions', icon: '⏰', enabled: true },
    AUTOMATION: { id: 'automation', name: 'Autonomous Tasks', icon: '🤖', enabled: false }
} as const;
