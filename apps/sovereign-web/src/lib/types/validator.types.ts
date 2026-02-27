export interface Validator {
    id: string;
    name: string;
    stake: number;
    commission: number;
    uptime: number;
    status: 'VALIDATING' | 'IDLE' | 'SUSPENDED' | 'jailed' | 'inactive';
    location: string;
    nodes: number;
    neuralLiquidity: number;
    consensusParticipation: number;
    votingPower: number;
    delegators: number;
    apy: number;
    rank: number;
}

export interface ValidatorState {
    totalNodes: number;
    activeValidators: number;
    totalStakedAge: number;
    computeYieldTflops: number;
    neuralLiquidity: number;
    nodes: ValidatorNode[];
    validators: Validator[];
    totalStake: number;
    avgCommission: number;
    avgUptime: number;
    totalNeuralLiquidity: number;
    lastUpdated: number;
}

export interface ValidatorMetrics {
    neuralEfficiency: number;
    consensusHealth: number;
    decentralizationScore: number;
}

export type NeuralLiquidityScore = number;

export interface ValidatorNode {
    id: string;
    stake: number;
    uptime: number;
    reputation: number;
    status: 'VALIDATING' | 'IDLE' | 'SUSPENDED';
}
