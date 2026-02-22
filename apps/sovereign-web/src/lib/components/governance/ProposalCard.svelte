<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import {
        governanceStore,
        PROPOSAL_TYPES,
        PROPOSAL_STATUS,
    } from "$lib/stores/master-store";

    export let proposal;
    export let userVote = null;
    export let votingPower = 0;
    export let status;
    export let timeRemaining;

    const dispatch = createEventDispatcher();

    let showDetails = false;
    let isVoting = false;

    const proposalType =
        PROPOSAL_TYPES[proposal.type.toUpperCase()] || PROPOSAL_TYPES.PARAMETER;
    const proposalStatus = status;

    $: totalVotes =
        proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
    $: forPercentage =
        totalVotes > 0 ? (proposal.votesFor / totalVotes) * 100 : 0;
    $: againstPercentage =
        totalVotes > 0 ? (proposal.votesAgainst / totalVotes) * 100 : 0;
    $: quorumPercentage = (totalVotes / proposal.quorum) * 100;

    function handleVote(support) {
        if (userVote) return;
        isVoting = true;

        // Simulate blockchain delay
        setTimeout(() => {
            dispatch("vote", { proposalId: proposal.id, support });
            isVoting = false;
        }, 500);
    }
</script>

<div class="proposal-card" class:expanded={showDetails}>
    <div class="proposal-header">
        <div class="proposal-type" style="--type-color: {proposalType.color};">
            <span class="type-icon">{proposalType.icon}</span>
            <span class="type-label">{proposalType.label}</span>
        </div>

        <div
            class="proposal-status"
            style="--status-color: {proposalStatus.color};"
        >
            <span class="status-icon">{proposalStatus.icon}</span>
            <span class="status-label">{proposalStatus.label}</span>
        </div>
    </div>

    <div class="proposal-content">
        <h3 class="proposal-title">{proposal.title}</h3>
        <p class="proposal-description">{proposal.description}</p>

        <div class="proposal-meta">
            <span class="meta-item">
                <span class="meta-icon">👤</span>
                {proposal.proposerName}
            </span>
            <span class="meta-item">
                <span class="meta-icon">⏰</span>
                {timeRemaining}
            </span>
            {#if proposalStatus.id === PROPOSAL_STATUS.ACTIVE.id}
                <span class="meta-item quorum">
                    <span class="meta-icon">📊</span>
                    Quorum: {Math.min(100, Math.round(quorumPercentage))}%
                </span>
            {/if}
        </div>

        {#if proposalStatus.id === PROPOSAL_STATUS.ACTIVE.id}
            <div class="vote-bars">
                <div class="vote-bar for" style="width: {forPercentage}%;">
                    <span class="vote-label">For {proposal.votesFor}</span>
                </div>
                <div
                    class="vote-bar against"
                    style="width: {againstPercentage}%;"
                >
                    <span class="vote-label"
                        >Against {proposal.votesAgainst}</span
                    >
                </div>
            </div>
        {/if}

        {#if showDetails}
            <div class="proposal-details">
                <h4 class="details-title">Details</h4>
                {#if proposal.details.parameter}
                    <div class="detail-item">
                        <span class="detail-label">Parameter:</span>
                        <code class="detail-value"
                            >{proposal.details.parameter}</code
                        >
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Current:</span>
                        <span class="detail-value"
                            >{proposal.details.currentValue}</span
                        >
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Proposed:</span>
                        <span class="detail-value"
                            >{proposal.details.proposedValue}</span
                        >
                    </div>
                {/if}

                {#if proposal.details.amount}
                    <div class="detail-item">
                        <span class="detail-label">Amount:</span>
                        <span class="detail-value"
                            >{proposal.details.amount} AGE</span
                        >
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Recipient:</span>
                        <span class="detail-value"
                            >{proposal.details.recipient}</span
                        >
                    </div>
                {/if}

                <div class="detail-item rationale">
                    <span class="detail-label">Rationale:</span>
                    <p class="detail-text">{proposal.details.rationale}</p>
                </div>

                {#if proposal.discussion}
                    <a
                        href={proposal.discussion}
                        target="_blank"
                        class="discussion-link"
                    >
                        💬 Join Discussion →
                    </a>
                {/if}
            </div>
        {/if}
    </div>

    <div class="proposal-footer">
        {#if proposalStatus.id === PROPOSAL_STATUS.ACTIVE.id}
            <div class="voting-section">
                {#if userVote}
                    <div class="voted-badge">
                        <span>✓ You voted {userVote}</span>
                    </div>
                {:else}
                    <div class="voting-buttons">
                        <button
                            class="vote-btn for"
                            on:click={() => handleVote("for")}
                            disabled={isVoting}
                        >
                            {#if isVoting}
                                <span class="spinner"></span>
                            {:else}
                                <span>✓ For</span>
                            {/if}
                        </button>
                        <button
                            class="vote-btn against"
                            on:click={() => handleVote("against")}
                            disabled={isVoting}
                        >
                            {#if isVoting}
                                <span class="spinner"></span>
                            {:else}
                                <span>✗ Against</span>
                            {/if}
                        </button>
                        <button
                            class="vote-btn abstain"
                            on:click={() => handleVote("abstain")}
                            disabled={isVoting}
                        >
                            <span>○ Abstain</span>
                        </button>
                    </div>
                    <span class="power-hint">Voting power: {votingPower}</span>
                {/if}
            </div>
        {:else if proposalStatus.id === PROPOSAL_STATUS.PASSED.id}
            <div class="result-badge passed">
                <span>✓ Passed</span>
                {#if proposal.executedAt}
                    <span>
                        · Executed {new Date(
                            proposal.executedAt,
                        ).toLocaleDateString()}</span
                    >
                {/if}
            </div>
        {:else if proposalStatus.id === PROPOSAL_STATUS.REJECTED.id}
            <div class="result-badge rejected">
                <span>✗ Rejected</span>
            </div>
        {:else if proposalStatus.id === PROPOSAL_STATUS.EXECUTED.id}
            <div class="result-badge executed">
                <span>⚡ Executed</span>
            </div>
        {/if}

        <button
            class="expand-btn"
            on:click={() => (showDetails = !showDetails)}
        >
            {showDetails ? "Show less" : "Show details"}
        </button>
    </div>
</div>

<style>
    .proposal-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        overflow: hidden;
        transition: all 0.2s;
    }

    .proposal-card:hover {
        border-color: #9370db;
        transform: translateX(4px);
    }

    .proposal-card.expanded {
        background: rgba(255, 255, 255, 0.04);
        border-color: #9370db;
    }

    .proposal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .proposal-type {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--type-color);
    }

    .type-icon {
        font-size: 1.1rem;
    }

    .type-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .proposal-status {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.5rem;
        background: var(--status-color);
        border-radius: 1rem;
        font-size: 0.7rem;
        color: white;
    }

    .proposal-content {
        padding: 1rem;
    }

    .proposal-title {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }

    .proposal-description {
        margin: 0 0 0.75rem 0;
        font-size: 0.9rem;
        opacity: 0.8;
        line-height: 1.5;
    }

    .proposal-meta {
        display: flex;
        gap: 1rem;
        margin-bottom: 0.75rem;
        font-size: 0.8rem;
        flex-wrap: wrap;
    }

    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        opacity: 0.7;
    }

    .meta-icon {
        font-size: 0.9rem;
    }

    .meta-item.quorum {
        color: #4ecdc4;
    }

    .vote-bars {
        display: flex;
        height: 24px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }

    .vote-bar {
        position: relative;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: width 0.3s;
    }

    .vote-bar.for {
        background: linear-gradient(90deg, #4caf50, #45b7d1);
    }

    .vote-bar.against {
        background: linear-gradient(90deg, #ff6b6b, #ff8e8e);
    }

    .vote-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    .proposal-details {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 0.5rem;
    }

    .details-title {
        margin: 0 0 0.75rem 0;
        font-size: 0.9rem;
        color: #9370db;
    }

    .detail-item {
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    .detail-label {
        display: block;
        margin-bottom: 0.25rem;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .detail-value {
        font-family: monospace;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
    }

    .detail-item.rationale {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .detail-text {
        margin: 0;
        line-height: 1.5;
        font-size: 0.9rem;
    }

    .discussion-link {
        display: inline-block;
        margin-top: 0.75rem;
        color: #4ecdc4;
        text-decoration: none;
        font-size: 0.9rem;
    }

    .discussion-link:hover {
        text-decoration: underline;
    }

    .proposal-footer {
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .voting-section {
        margin-bottom: 0.75rem;
    }

    .voting-buttons {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .vote-btn {
        flex: 1;
        padding: 0.5rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .vote-btn.for {
        background: #4caf50;
        color: white;
    }

    .vote-btn.for:hover:not(:disabled) {
        background: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 2px 10px #4caf50;
    }

    .vote-btn.against {
        background: #ff6b6b;
        color: white;
    }

    .vote-btn.against:hover:not(:disabled) {
        background: #ff5252;
        transform: translateY(-2px);
        box-shadow: 0 2px 10px #ff6b6b;
    }

    .vote-btn.abstain {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .vote-btn.abstain:hover:not(:disabled) {
        background: rgba(255, 255, 255, 0.2);
    }

    .vote-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .spinner {
        width: 1rem;
        height: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .power-hint {
        display: block;
        font-size: 0.7rem;
        opacity: 0.5;
        text-align: center;
    }

    .voted-badge {
        padding: 0.5rem;
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        border-radius: 0.5rem;
        text-align: center;
        color: #4caf50;
    }

    .result-badge {
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 0.75rem;
    }

    .result-badge.passed {
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        color: #4caf50;
    }

    .result-badge.rejected {
        background: rgba(255, 107, 107, 0.2);
        border: 1px solid #ff6b6b;
        color: #ff6b6b;
    }

    .result-badge.executed {
        background: rgba(147, 112, 219, 0.2);
        border: 1px solid #9370db;
        color: #9370db;
    }

    .expand-btn {
        width: 100%;
        padding: 0.5rem;
        background: none;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s;
    }

    .expand-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #9370db;
    }
</style>
