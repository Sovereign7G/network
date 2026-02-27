export type CausalEventType =
    | 'transaction:created'
    | 'transaction:confirmed'
    | 'transaction:failed'
    | 'vote:cast'
    | 'vote:changed'
    | 'identity:created'
    | 'identity:verified'
    | 'node:activated'
    | 'node:deactivated'
    | 'stake:created'
    | 'stake:withdrawn'
    | 'bridge:initiated'
    | 'bridge:completed'
    | 'bridge:failed';

export interface CausalEvent<T = unknown> {
    id: string;
    type: CausalEventType;
    timestamp: number;
    actor: string;
    target: string;
    payload: T;
    previous?: string; // previous event ID for causality
    signature?: string;
}

export interface TransactionCausalPayload {
    txId: string;
    amount: number;
    asset: string;
    from: string;
    to: string;
    fee: number;
}

export interface VoteCausalPayload {
    proposalId: string;
    vote: 'for' | 'against' | 'abstain';
    power: number;
}
