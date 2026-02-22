import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { loadFromStorage, saveToStorage } from '$lib/utils/storage';
import { PROPOSAL_TYPES, PROPOSAL_STATUS } from './constants';
import type {
    GovernanceState,
    Proposal,
    CouncilMember,
    GovernanceStats,
    ActivityFeedItem,
    ProposalStatus
} from '$lib/types';

const initialState: GovernanceState = {
    proposals: [
        {
            id: '1',
            title: 'Increase Hearth Resonance Rewards',
            description: 'Proposal to increase resonance rewards for daily Hearth entries by 20% to encourage more active participation.',
            type: PROPOSAL_TYPES.PARAMETER.id,
            status: PROPOSAL_STATUS.ACTIVE.id,
            proposer: '0x1234...5678',
            proposerName: 'Sovereign #1234',
            votesFor: 1247,
            votesAgainst: 382,
            votesAbstain: 45,
            quorum: 2000,
            startTime: new Date(Date.now() - 86400000 * 2),
            endTime: new Date(Date.now() + 86400000 * 3),
            discussion: 'https://forum.ageprotocol.com/proposal/1',
            details: {
                parameter: 'hearth.resonance.multiplier',
                currentValue: '1.0',
                proposedValue: '1.2',
                rationale: 'Increasing rewards will boost engagement and strengthen community bonds.'
            }
        },
        {
            id: '2',
            title: 'Add New Memory Type: "Achievement"',
            description: 'Introduce a new memory type for personal achievements worth 25 resonance to celebrate milestones.',
            type: PROPOSAL_TYPES.PARAMETER.id,
            status: PROPOSAL_STATUS.ACTIVE.id,
            proposer: '0x8765...4321',
            proposerName: 'Sovereign #8765',
            votesFor: 892,
            votesAgainst: 156,
            votesAbstain: 23,
            quorum: 2000,
            startTime: new Date(Date.now() - 86400000 * 4),
            endTime: new Date(Date.now() + 86400000),
            details: {
                parameter: 'hearth.memory.achievement',
                currentValue: 'null',
                proposedValue: '25 resonance',
                rationale: 'Celebrating achievements adds depth to the Hearth experience.'
            }
        },
        {
            id: '3',
            title: 'Reduce Governance Quorum',
            description: 'Lower minimum participation requirement from 10% to 7% to make governance more accessible.',
            type: PROPOSAL_TYPES.PARAMETER.id,
            status: PROPOSAL_STATUS.PASSED.id,
            proposer: '0x2468...1357',
            proposerName: 'Sovereign #2468',
            votesFor: 2156,
            votesAgainst: 843,
            votesAbstain: 67,
            quorum: 2000,
            startTime: new Date(Date.now() - 86400000 * 7),
            endTime: new Date(Date.now() - 86400000),
            executedAt: new Date(Date.now() - 86400000 * 0.5),
            details: {
                parameter: 'governance.quorum',
                currentValue: '10%',
                proposedValue: '7%',
                rationale: 'Lower quorum enables faster decision-making while maintaining security.'
            }
        }
    ],
    userVotes: {
        '1': 'for',
        '3': 'for'
    },
    userDelegates: null,
    participationScore: 78,
    votingPower: 1247,
    delegate: null,
    delegationHistory: [],
    councilMembers: [
        {
            id: 'council1',
            address: '0x1111...2222',
            name: 'Sovereign Council Member 1',
            role: 'Lead Steward',
            avatar: null,
            votingPower: 15000,
            proposalsCreated: 12,
            participationRate: 98
        },
        {
            id: 'council2',
            address: '0x3333...4444',
            name: 'Sovereign Council Member 2',
            role: 'Technical Steward',
            avatar: null,
            votingPower: 12000,
            proposalsCreated: 8,
            participationRate: 95
        }
    ],
    governanceStats: {
        totalProposals: 47,
        activeProposals: 2,
        passRate: 76,
        averageParticipation: 64,
        totalVoters: 892,
        totalDelegators: 234
    },
    activityFeed: [
        {
            id: '1',
            type: 'vote',
            user: 'Sovereign #1234',
            action: 'voted For on Proposal #1',
            timestamp: new Date(Date.now() - 3600000),
            resonance: 50
        },
        {
            id: '2',
            type: 'proposal',
            user: 'Sovereign #8765',
            action: 'created Proposal #2',
            timestamp: new Date(Date.now() - 86400000),
            resonance: 100
        },
        {
            id: '3',
            type: 'delegate',
            user: 'Sovereign #2468',
            action: 'delegated to Council Member',
            timestamp: new Date(Date.now() - 172800000),
            resonance: 25
        }
    ]
};

function createGovernanceStore() {
    const stored = loadFromStorage<GovernanceState>('governance', initialState);

    // Restore dates
    if (stored.proposals) {
        stored.proposals = stored.proposals.map(p => ({
            ...p,
            startTime: new Date(p.startTime),
            endTime: new Date(p.endTime),
            executedAt: p.executedAt ? new Date(p.executedAt) : undefined
        }));
    }

    if (stored.activityFeed) {
        stored.activityFeed = stored.activityFeed.map(a => ({
            ...a,
            timestamp: new Date(a.timestamp)
        }));
    }

    if (stored.delegationHistory) {
        stored.delegationHistory = stored.delegationHistory.map(d => ({
            ...d,
            timestamp: new Date(d.timestamp)
        }));
    }

    const { subscribe, set, update } = writable<GovernanceState>(stored);

    return {
        subscribe,

        castVote: (proposalId: string, support: 'for' | 'against' | 'abstain') =>
            update((state: GovernanceState) => {
                const proposal = state.proposals.find(p => p.id === proposalId);
                if (!proposal) return state;

                if (state.userVotes[proposalId]) return state;

                const updatedProposals = state.proposals.map(p => {
                    if (p.id === proposalId) {
                        return {
                            ...p,
                            votesFor: support === 'for' ? p.votesFor + 1 : p.votesFor,
                            votesAgainst: support === 'against' ? p.votesAgainst + 1 : p.votesAgainst,
                            votesAbstain: support === 'abstain' ? p.votesAbstain + 1 : p.votesAbstain
                        };
                    }
                    return p;
                });

                const newActivity: ActivityFeedItem = {
                    id: crypto.randomUUID(),
                    type: 'vote',
                    user: 'You',
                    action: `voted ${support} on Proposal #${proposalId}`,
                    timestamp: new Date(),
                    resonance: 10
                };

                const newState: GovernanceState = {
                    ...state,
                    proposals: updatedProposals,
                    userVotes: { ...state.userVotes, [proposalId]: support },
                    participationScore: Math.min(100, state.participationScore + 1),
                    activityFeed: [newActivity, ...state.activityFeed].slice(0, 50)
                };

                saveToStorage('governance', newState);
                return newState;
            }),

        createProposal: (proposal: Omit<Proposal, 'id' | 'status' | 'proposer' | 'proposerName' | 'votesFor' | 'votesAgainst' | 'votesAbstain' | 'quorum' | 'startTime' | 'endTime' | 'createdAt'>) =>
            update((state: GovernanceState) => {
                const newProposal: Proposal = {
                    ...proposal,
                    id: (state.proposals.length + 1).toString(),
                    status: PROPOSAL_STATUS.DISCUSSION.id,
                    proposer: '0xabcd...efgh',
                    proposerName: 'You',
                    votesFor: 0,
                    votesAgainst: 0,
                    votesAbstain: 0,
                    quorum: 2000,
                    startTime: new Date(Date.now() + 86400000 * 2),
                    endTime: new Date(Date.now() + 86400000 * 9)
                };

                const newActivity: ActivityFeedItem = {
                    id: crypto.randomUUID(),
                    type: 'proposal',
                    user: 'You',
                    action: `created Proposal #${newProposal.id}: ${newProposal.title}`,
                    timestamp: new Date(),
                    resonance: 100
                };

                const newState: GovernanceState = {
                    ...state,
                    proposals: [newProposal, ...state.proposals],
                    participationScore: Math.min(100, state.participationScore + 5),
                    activityFeed: [newActivity, ...state.activityFeed].slice(0, 50),
                    governanceStats: {
                        ...state.governanceStats,
                        totalProposals: state.governanceStats.totalProposals + 1
                    }
                };

                saveToStorage('governance', newState);
                return newState;
            }),

        delegateVotes: (delegateAddress: string) =>
            update((state: GovernanceState) => {
                const newActivity: ActivityFeedItem = {
                    id: crypto.randomUUID(),
                    type: 'delegate',
                    user: 'You',
                    action: `delegated to ${delegateAddress}`,
                    timestamp: new Date(),
                    resonance: 25
                };

                const newState: GovernanceState = {
                    ...state,
                    userDelegates: delegateAddress,
                    delegationHistory: [
                        ...state.delegationHistory,
                        {
                            to: delegateAddress,
                            timestamp: new Date(),
                            amount: state.votingPower
                        }
                    ],
                    activityFeed: [newActivity, ...state.activityFeed].slice(0, 50)
                };

                saveToStorage('governance', newState);
                return newState;
            }),

        getProposalStatus: (proposal: Proposal): ProposalStatus => {
            const now = new Date();
            if (proposal.status === PROPOSAL_STATUS.EXECUTED.id) return PROPOSAL_STATUS.EXECUTED;
            if (proposal.status === PROPOSAL_STATUS.PASSED.id) return PROPOSAL_STATUS.PASSED;
            if (proposal.status === PROPOSAL_STATUS.REJECTED.id) return PROPOSAL_STATUS.REJECTED;

            if (now < proposal.startTime) return PROPOSAL_STATUS.DISCUSSION;
            if (now > proposal.endTime) {
                if (proposal.votesFor > proposal.votesAgainst &&
                    proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain >= proposal.quorum) {
                    return PROPOSAL_STATUS.PASSED;
                } else {
                    return PROPOSAL_STATUS.REJECTED;
                }
            }
            return PROPOSAL_STATUS.ACTIVE;
        },

        getUserVotingPower: (state: GovernanceState, resonance: number, holdings: number): number => {
            return Math.floor(resonance + (holdings / 10));
        },

        getTimeRemaining: (endTime: Date): string => {
            const now = new Date();
            const diff = endTime.getTime() - now.getTime();

            if (diff <= 0) return 'Ended';

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

            if (days > 0) return `${days}d ${hours}h remaining`;
            if (hours > 0) return `${hours}h remaining`;
            return 'Less than an hour';
        }
    };
}

export const governanceStore = createGovernanceStore();
