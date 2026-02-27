// ==================== CORE TYPES ====================

// Sovereign Identity Types
export interface SovereignProfile {
    displayName: string;
    avatar: string | null;
    bio: string;
    location: string | null;
}

export interface SovereignPreferences {
    theme: 'dark' | 'light' | 'system';
    quietMode: boolean;
    autoPilot: boolean;
    notifications: boolean;
}

export interface SovereignState {
    id: string | null;
    did: string | null;
    handle: string | null;
    profile: SovereignProfile;
    verificationLevel: number;
    createdAt: string | null;
    lastActive: string;
    preferences: SovereignPreferences;
}

// ==================== HEARTH TYPES ====================

export interface MemoryType {
    id: string;
    label: string;
    resonance: number;
    icon: string;
    color: string;
    description: string;
}

export interface MemoryReflection {
    id: string;
    content: string;
    timestamp: Date;
}

export interface Memory {
    id: string;
    type: string;
    title?: string | null;
    content: string;
    timestamp: Date;
    resonance: number;
    reflections: MemoryReflection[];
    tags: string[];
}

export interface Insight {
    id: string;
    type: 'pattern' | 'opportunity' | 'achievement' | 'conversation';
    title: string;
    description: string;
    confidence: number;
    timestamp: Date;
    actionable: boolean;
    action?: string;
    actioned?: boolean;
    icon?: string;
}

export interface Achievement {
    id: string;
    title: string;
    description: string;
    earned: boolean;
    icon: string;
    earnedAt: Date | null;
    progress?: number;
    target?: number;
}

export interface ResonanceHistoryEntry {
    date: Date;
    value: number;
}

export interface HearthFilters {
    type: string;
    search: string;
    dateRange: 'all' | 'week' | 'month' | 'year';
}

export interface HearthState {
    memories: Memory[];
    streak: number;
    lastEntryDate: string | null;
    totalResonance: number;
    lifetimeResonance: number;
    filters: HearthFilters;
    insights: Insight[];
    achievements: Achievement[];
    resonanceHistory: ResonanceHistoryEntry[];
}

// ==================== VAULT TYPES ====================

export interface Transaction {
    id: string;
    type: 'receive' | 'send' | 'stake' | 'unstake' | 'swap';
    amount: number;
    asset: string;
    from?: string;
    to?: string;
    timestamp: Date;
    status: 'pending' | 'confirmed' | 'failed';
    hash?: string;
    memo?: string;
}

export interface AssetPrice {
    [key: string]: number;
}

export interface PriceHistoryEntry {
    date: Date;
    price: number;
}

export interface VaultState {
    balances: Record<string, number>;
    transactions: Transaction[];
    totalValue: number;
    totalValueChange: string;
    allocation: {
        liquid: number;
        staked: number;
        vested: number;
    };
    assetPrices: AssetPrice;
    priceHistory: Record<string, PriceHistoryEntry[]>;
}

// ==================== GOVERNANCE TYPES ====================

export interface ProposalType {
    id: string;
    label: string;
    icon: string;
    color: string;
}

export interface ProposalStatus {
    id: string;
    label: string;
    icon: string;
    color: string;
}

export interface ProposalDetails {
    parameter?: string;
    currentValue?: string;
    proposedValue?: string;
    amount?: number;
    recipient?: string;
    rationale: string;
}

export interface Proposal {
    id: string;
    title: string;
    description: string;
    type: string;
    status: string;
    proposer: string;
    proposerName: string;
    votesFor: number;
    votesAgainst: number;
    votesAbstain: number;
    quorum: number;
    startTime: Date;
    endTime: Date;
    executedAt?: Date;
    discussion?: string;
    details: ProposalDetails;
}

export interface CouncilMember {
    id: string;
    address: string;
    name: string;
    role: string;
    avatar: string | null;
    votingPower: number;
    proposalsCreated: number;
    participationRate: number;
}

export interface GovernanceStats {
    totalProposals: number;
    activeProposals: number;
    passRate: number;
    averageParticipation: number;
    totalVoters: number;
    totalDelegators: number;
}

export interface ActivityFeedItem {
    id: string;
    type: 'vote' | 'proposal' | 'delegate';
    user: string;
    action: string;
    timestamp: Date;
    resonance?: number;
}

export interface GovernanceState {
    proposals: Proposal[];
    userVotes: Record<string, string>;
    userDelegates: string | null;
    participationScore: number;
    votingPower: number;
    delegate: string | null;
    delegationHistory: Array<{
        to: string;
        timestamp: Date;
        amount: number;
    }>;
    councilMembers: CouncilMember[];
    governanceStats: GovernanceStats;
    activityFeed: ActivityFeedItem[];
}

// ==================== TELEMETRY TYPES ====================

export interface TelemetryLog {
    id: string;
    level: 'info' | 'warn' | 'error' | 'debug';
    module: string;
    message: string;
    timestamp: Date;
    data?: Record<string, unknown>;
}

export interface SystemVitals {
    cpu: number;
    memory: number;
    networkLatency: number;
    syncStatus: 'synced' | 'syncing' | 'degraded' | 'error';
    activeConnections: number;
    resonance: number;
}

export interface SystemicData {
    sofr: number;
    treasury10y: number;
    spread: number;
    oatBund: number;
    eurChf: number;
    wti: number;
    gold: number;
    xmr: number;
    xmrVolume: number;
    tao: number;
    render: number;
}

export interface TelemetryState {
    logs: TelemetryLog[];
    vitals: SystemVitals;
    resonance: number;
    layersActive: number;
    alerts: Array<{
        id: string;
        level: 'info' | 'warn' | 'error';
        message: string;
        timestamp: Date;
    }>;
    systemic?: SystemicData;
}

// ==================== CONCIERGE TYPES ====================

export interface Personality {
    id: string;
    name: string;
    icon: string;
    description: string;
    color: string;
}

export interface Capability {
    id: string;
    name: string;
    icon: string;
    enabled: boolean;
}

export interface ConversationMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    context?: {
        type?: string;
        sentiment?: string;
    };
    suggestions?: Array<{
        text: string;
        context: string;
        priority: number;
    }>;
    streaming?: boolean;
    isError?: boolean;
}

export interface Conversation {
    id: string;
    title: string;
    lastMessage: string;
    timestamp: Date;
    unread: boolean;
    messages: ConversationMessage[];
}

export interface ScheduledReminder {
    id: string;
    title: string;
    description: string;
    cron: string;
    enabled: boolean;
    lastTriggered: Date | null;
    nextTrigger: Date | null;
}

export interface KnowledgeBase {
    userPreferences: {
        favoriteMemoryTypes: string[];
        peakActivityHours: number[];
        votingTopics: string[];
        assetPreferences: string[];
    };
    learnedPatterns: {
        resonanceVelocity: number;
        votingConsistency: number;
        reflectionDepth: number;
    };
}

export interface Suggestion {
    id: string;
    text: string;
    context: 'hearth' | 'vault' | 'governance' | 'general';
    priority: number;
}

export interface ConciergeState {
    initialized: boolean;
    personality: string;
    capabilities: Record<string, Capability>;
    conversations: Conversation[];
    currentConversationId: string | null;
    insights: Insight[];
    scheduledReminders: ScheduledReminder[];
    autonomousTasks: any[];
    knowledgeBase: KnowledgeBase;
    suggestions: Suggestion[];
    isProcessing: boolean;
}

// ==================== USER CONTEXT TYPES ====================

export interface UserContext {
    displayName: string;
    totalResonance: number;
    streak: number;
    memoryCount: number;
    favoriteType: string;
    resonanceTier?: string;
    balances: Record<string, number>;
    totalValue: number;
    activeProposals: number;
    votingPower: number;
    votingPattern: string;
    bestDay: string;
    depthIncrease: number;
    personality?: string;
}

// ==================== STORE TYPES ====================

export type StoreUpdater<T> = (value: T) => T;

export interface SovereignStore {
    subscribe: (run: (value: SovereignState) => void) => () => void;
    initialize: (data: Partial<SovereignState>) => void;
    updateProfile: (profile: Partial<SovereignProfile>) => void;
    setVerificationLevel: (level: number) => void;
    updatePreferences: (prefs: Partial<SovereignPreferences>) => void;
    toggleQuietMode: () => void;
    updateLastActive: () => void;
}

export interface HearthStore {
    subscribe: (run: (value: HearthState) => void) => () => void;
    addMemory: (memory: Omit<Memory, 'id' | 'timestamp' | 'resonance' | 'reflections'>) => void;
    addReflection: (memoryId: string, reflection: string) => void;
    deleteMemory: (id: string) => void;
    setFilter: <K extends keyof HearthFilters>(filterType: K, value: HearthFilters[K]) => void;
    getResonanceTier: (resonance: number) => { level: number; threshold: number; title: string; icon: string };
    getFilteredMemories: (state: HearthState) => Memory[];
    exportMemories: () => any;
}

export interface VaultStore {
    subscribe: (run: (value: VaultState) => void) => () => void;
    addTransaction: (tx: Omit<Transaction, 'id' | 'timestamp' | 'status'>) => void;
    updateBalance: (asset: string, amount: number) => void;
    updatePrice: (asset: string, price: number) => void;
    confirmTransaction: (id: string) => void;
}

export interface GovernanceStore {
    subscribe: (run: (value: GovernanceState) => void) => () => void;
    castVote: (proposalId: string, support: 'for' | 'against' | 'abstain') => void;
    createProposal: (proposal: Omit<Proposal, 'id' | 'status' | 'proposer' | 'proposerName' | 'votesFor' | 'votesAgainst' | 'votesAbstain' | 'quorum' | 'startTime' | 'endTime' | 'createdAt'>) => void;
    delegateVotes: (delegateAddress: string) => void;
    getProposalStatus: (proposal: Proposal) => ProposalStatus;
    getUserVotingPower: (state: GovernanceState, resonance: number, holdings: number) => number;
    getTimeRemaining: (endTime: Date) => string;
}

export interface TelemetryStore {
    subscribe: (run: (value: TelemetryState) => void) => () => void;
    addLog: (log: Omit<TelemetryLog, 'id' | 'timestamp'>) => void;
    updateVitals: (vitals: Partial<SystemVitals>) => void;
}

export interface ConciergeStore {
    subscribe: (run: (value: ConciergeState) => void) => () => void;
    sendMessage: (content: string, userContext: UserContext) => Promise<void>;
    newConversation: () => void;
    switchConversation: (conversationId: string) => void;
    deleteConversation: (conversationId: string) => void;
    setPersonality: (personalityId: string) => void;
    toggleCapability: (capabilityId: string) => void;
    addReminder: (reminder: Omit<ScheduledReminder, 'id' | 'enabled' | 'lastTriggered' | 'nextTrigger'>) => void;
    dismissInsight: (insightId: string) => void;
    executeInsightAction: (insightId: string) => void;
    generateUserContext: (
        sovereign: SovereignState,
        hearth: HearthState,
        vault: VaultState,
        governance: GovernanceState
    ) => UserContext;
}

// ==================== WORKER TYPES ====================

export type WorkerMessageType = 'STANDARDIZE_LAYOUT' | 'PROCESS_DATA' | 'QUERY_VECTOR' | 'ERROR';

export interface WorkerMessage<T = any> {
    id: string;
    type: WorkerMessageType;
    payload: T;
    timestamp: number;
    error?: string;
}

