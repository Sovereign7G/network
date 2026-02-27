<script lang="ts">
    import {
        governanceStore,
        hearthStore,
        vaultStore,
    } from "$lib/stores/master-store";
    import { PROPOSAL_TYPES, PROPOSAL_STATUS } from "$lib/stores/constants";
    import ProposalCard from "$lib/components/governance/ProposalCard.svelte";
    import CreateProposalModal from "$lib/components/governance/CreateProposalModal.svelte";
    import DelegateModal from "$lib/components/governance/DelegateModal.svelte";
    import CouncilMembers from "$lib/components/governance/CouncilMembers.svelte";
    import GovernanceStats from "$lib/components/governance/GovernanceStats.svelte";
    import ActivityFeed from "$lib/components/governance/ActivityFeed.svelte";
    import { fade, fly, scale } from "svelte/transition";

    let showCreateModal = $state(false);
    let showDelegateModal = $state(false);
    let selectedFilter = $state("active");
    let selectedType = $state("all");
    let searchQuery = $state("");

    const filters = [
        { id: "all", label: "All Proposals", icon: "📋" },
        { id: "active", label: "Active", icon: "🗳️" },
        { id: "discussion", label: "Discussion", icon: "💬" },
        { id: "passed", label: "Passed", icon: "✅" },
        { id: "executed", label: "Executed", icon: "⚡" },
    ];

    // Calculate user voting power
    let votingPower = $derived(
        governanceStore.getUserVotingPower(
            hearthStore.state?.totalResonance || 0,
            vaultStore.state?.totalValue || 0,
        ),
    );

    // Filter proposals
    let filteredProposals = $derived(
        governanceStore.state.proposals.filter((proposal) => {
            const status = governanceStore.getProposalStatus(proposal);

            const matchesFilter =
                selectedFilter === "all" || status.id === selectedFilter;
            const matchesType =
                selectedType === "all" || proposal.type === selectedType;
            const matchesSearch =
                searchQuery === "" ||
                proposal.title
                    .toLowerCase()
                    .includes(searchQuery.toLowerCase()) ||
                proposal.description
                    .toLowerCase()
                    .includes(searchQuery.toLowerCase());

            return matchesFilter && matchesType && matchesSearch;
        }),
    );

    // Sort proposals: active first, then by end date
    let sortedProposals = $derived(
        [...filteredProposals].sort((a, b) => {
            const aStatus = governanceStore.getProposalStatus(a);
            const bStatus = governanceStore.getProposalStatus(b);

            if (
                aStatus.id === PROPOSAL_STATUS.ACTIVE.id &&
                bStatus.id !== PROPOSAL_STATUS.ACTIVE.id
            )
                return -1;
            if (
                aStatus.id !== PROPOSAL_STATUS.ACTIVE.id &&
                bStatus.id === PROPOSAL_STATUS.ACTIVE.id
            )
                return 1;

            return (
                new Date(b.endTime).getTime() - new Date(a.endTime).getTime()
            );
        }),
    );
</script>

<svelte:head>
    <title>Governance Council · AGE Protocol</title>
</svelte:head>

<div class="governance">
    <!-- Header -->
    <div class="governance-header" in:fade>
        <div class="header-left">
            <h1 class="governance-title">
                <span class="title-icon">⚖️</span>
                Sovereign Council
            </h1>
            <div class="voting-power">
                <span class="power-label">Your Voting Power</span>
                <span class="power-value">{votingPower}</span>
                <span class="power-badge">⚡ Active</span>
            </div>
        </div>

        <div class="header-actions">
            <button
                class="action-button"
                onclick={() => (showDelegateModal = true)}
            >
                <span class="action-icon">🤝</span>
                <span>Delegate</span>
            </button>
            <button
                class="action-button primary"
                onclick={() => (showCreateModal = true)}
            >
                <span class="action-icon">➕</span>
                <span>Create Proposal</span>
            </button>
        </div>
    </div>

    <!-- Stats Overview -->
    <div class="stats-row" in:fly={{ y: 20, duration: 500, delay: 100 }}>
        <GovernanceStats stats={governanceStore.state.governanceStats} />
    </div>

    <!-- Main Grid -->
    <div class="governance-grid">
        <!-- Left Column: Proposals -->
        <div class="proposals-column">
            <!-- Filters -->
            <div
                class="filters-bar"
                in:fly={{ y: 20, duration: 500, delay: 150 }}
            >
                <div class="filter-tabs">
                    {#each filters as filter}
                        <button
                            class="filter-tab"
                            class:active={selectedFilter === filter.id}
                            onclick={() => (selectedFilter = filter.id)}
                        >
                            <span class="tab-icon">{filter.icon}</span>
                            <span>{filter.label}</span>
                        </button>
                    {/each}
                </div>

                <div class="filter-controls">
                    <div class="search-wrapper">
                        <span class="search-icon">🔍</span>
                        <input
                            type="text"
                            class="search-input"
                            placeholder="Search proposals..."
                            bind:value={searchQuery}
                        />
                    </div>

                    <select class="type-filter" bind:value={selectedType}>
                        <option value="all">All Types</option>
                        {#each Object.values(PROPOSAL_TYPES) as type}
                            <option value={type.id}>
                                {type.icon}
                                {type.label}
                            </option>
                        {/each}
                    </select>
                </div>
            </div>

            <!-- Proposals List -->
            {#if sortedProposals.length === 0}
                <div class="empty-state" in:fade>
                    <span class="empty-icon">📭</span>
                    <h3>No proposals found</h3>
                    <p>Try adjusting your filters or create a new proposal.</p>
                    <button
                        class="create-first-btn"
                        onclick={() => (showCreateModal = true)}
                    >
                        Create First Proposal
                    </button>
                </div>
            {:else}
                <div class="proposals-list">
                    {#each sortedProposals as proposal (proposal.id)}
                        <div
                            in:fly={{
                                y: 20,
                                duration: 400,
                                delay:
                                    200 +
                                    sortedProposals.indexOf(proposal) * 50,
                            }}
                            out:fade
                        >
                            <ProposalCard
                                {proposal}
                                userVote={governanceStore.state.userVotes[
                                    proposal.id
                                ]}
                                {votingPower}
                                status={governanceStore.getProposalStatus(
                                    proposal,
                                )}
                                timeRemaining={governanceStore.getTimeRemaining(
                                    new Date(proposal.endTime),
                                )}
                            />
                        </div>
                    {/each}
                </div>
            {/if}
        </div>

        <!-- Right Column: Council & Activity -->
        <div class="sidebar-column">
            <!-- Council Members -->
            <div
                class="sidebar-card"
                in:fly={{ x: 20, duration: 500, delay: 200 }}
            >
                <h2 class="sidebar-title">
                    <span class="title-icon">👥</span>
                    Council Stewards
                </h2>
                <CouncilMembers
                    members={governanceStore.state.councilMembers}
                />
            </div>

            <!-- Activity Feed -->
            <div
                class="sidebar-card"
                in:fly={{ x: 20, duration: 500, delay: 250 }}
            >
                <h2 class="sidebar-title">
                    <span class="title-icon">📊</span>
                    Recent Activity
                </h2>
                <ActivityFeed activities={governanceStore.state.activityFeed} />
            </div>

            <!-- Quick Stats -->
            <div
                class="sidebar-card stats-card"
                in:fly={{ x: 20, duration: 500, delay: 300 }}
            >
                <h2 class="sidebar-title">
                    <span class="title-icon">📈</span>
                    Governance Health
                </h2>
                <div class="health-metrics">
                    <div class="health-item">
                        <span class="health-label">Participation</span>
                        <div class="health-bar">
                            <div
                                class="health-fill"
                                style="width: {governanceStore.state
                                    .participationScore}%;"
                            ></div>
                        </div>
                        <span class="health-value"
                            >{governanceStore.state.participationScore}%</span
                        >
                    </div>
                    <div class="health-item">
                        <span class="health-label">Delegation Rate</span>
                        <div class="health-bar">
                            <div
                                class="health-fill"
                                style="width: {(governanceStore.state
                                    .governanceStats.totalDelegators /
                                    governanceStore.state.governanceStats
                                        .totalVoters) *
                                    100}%;"
                            ></div>
                        </div>
                        <span class="health-value">
                            {Math.round(
                                (governanceStore.state.governanceStats
                                    .totalDelegators /
                                    governanceStore.state.governanceStats
                                        .totalVoters) *
                                    100,
                            )}%
                        </span>
                    </div>
                    <div class="health-item">
                        <span class="health-label">Pass Rate</span>
                        <div class="health-bar">
                            <div
                                class="health-fill"
                                style="width: {governanceStore.state
                                    .governanceStats.passRate}%;"
                            ></div>
                        </div>
                        <span class="health-value"
                            >{governanceStore.state.governanceStats
                                .passRate}%</span
                        >
                    </div>
                </div>

                <div class="delegation-info">
                    {#if governanceStore.state.userDelegates}
                        <div class="delegated-badge">
                            <span
                                >Delegated to: {governanceStore.state
                                    .userDelegates}</span
                            >
                            <button
                                class="change-delegate"
                                onclick={() => (showDelegateModal = true)}
                            >
                                Change
                            </button>
                        </div>
                    {:else}
                        <button
                            class="delegate-prompt"
                            onclick={() => (showDelegateModal = true)}
                        >
                            Delegate your voting power →
                        </button>
                    {/if}
                </div>
            </div>
        </div>
    </div>

    <!-- Modals -->
    {#if showCreateModal}
        <div
            class="modal-overlay"
            role="presentation"
            tabindex="-1"
            in:fade
            onclick={() => (showCreateModal = false)}
            onkeydown={(e: KeyboardEvent) => e.key === "Escape" && (showCreateModal = false)}
        >
            <div
                class="modal-content"
                role="dialog"
                tabindex="-1"
                aria-modal="true"
                aria-label="Create Proposal"
                in:scale
                onclick={(e: MouseEvent) => e.stopPropagation()}
                onkeydown={(e: KeyboardEvent) => e.stopPropagation()}
            >
                <CreateProposalModal
                    onClose={() => (showCreateModal = false)}
                    onCreate={(proposal: any) => {
                        governanceStore.createProposal(proposal);
                        showCreateModal = false;
                    }}
                />
            </div>
        </div>
    {/if}

    {#if showDelegateModal}
        <div
            class="modal-overlay"
            role="presentation"
            tabindex="-1"
            in:fade
            onclick={() => (showDelegateModal = false)}
            onkeydown={(e: KeyboardEvent) => e.key === "Escape" && (showDelegateModal = false)}
        >
            <div
                class="modal-content"
                role="dialog"
                tabindex="-1"
                aria-modal="true"
                aria-label="Delegate Votes"
                in:scale
                onclick={(e: MouseEvent) => e.stopPropagation()}
                onkeydown={(e: KeyboardEvent) => e.stopPropagation()}
            >
                <DelegateModal
                    currentDelegate={governanceStore.state.userDelegates}
                    councilMembers={governanceStore.state.councilMembers}
                    {votingPower}
                    onclose={() => (showDelegateModal = false)}

                    ondelegate={(e: Event) => {
                        governanceStore.delegateVotes(event.detail);
                        showDelegateModal = false;
                    }}
                />
            </div>
        </div>
    {/if}
</div>

<style>
    .governance {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }

    .governance-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .governance-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 2rem;
    }

    .title-icon {
        font-size: 2.5rem;
    }

    .voting-power {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid rgba(147, 112, 219, 0.2);
        border-radius: 2rem;
    }

    .power-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .power-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #9370db;
    }

    .power-badge {
        padding: 0.2rem 0.5rem;
        background: #4caf50;
        border-radius: 1rem;
        font-size: 0.7rem;
    }

    .header-actions {
        display: flex;
        gap: 1rem;
    }

    .action-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .action-button.primary {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
    }

    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.3);
    }

    .stats-row {
        margin-bottom: 2rem;
    }

    .governance-grid {
        display: grid;
        grid-template-columns: 1fr 350px;
        gap: 2rem;
    }

    .filters-bar {
        margin-bottom: 1.5rem;
    }

    .filter-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }

    .filter-tab {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s;
    }

    .filter-tab:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #9370db;
    }

    .filter-tab.active {
        background: #9370db;
        border-color: #9370db;
        color: white;
    }

    .tab-icon {
        font-size: 1rem;
    }

    .filter-controls {
        display: flex;
        gap: 1rem;
    }

    .search-wrapper {
        flex: 1;
        position: relative;
    }

    .search-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0.5;
    }

    .search-input {
        width: 100%;
        padding: 0.75rem 1rem 0.75rem 3rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
    }

    .search-input:focus {
        outline: none;
        border-color: #9370db;
    }

    .type-filter {
        padding: 0.75rem 2rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        cursor: pointer;
    }

    .proposals-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 2rem;
        border: 1px dashed rgba(255, 255, 255, 0.1);
    }

    .empty-icon {
        font-size: 4rem;
        display: block;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    .empty-state h3 {
        margin: 0 0 0.5rem 0;
    }

    .empty-state p {
        margin: 0 0 1.5rem 0;
        opacity: 0.7;
    }

    .create-first-btn {
        padding: 0.75rem 2rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .create-first-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 0 1rem 0;
        font-size: 1.1rem;
    }

    .title-icon {
        font-size: 1.3rem;
    }

    .stats-card {
        background: rgba(147, 112, 219, 0.05);
        border-color: rgba(147, 112, 219, 0.2);
    }

    .health-metrics {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .health-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .health-label {
        width: 100px;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .health-bar {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
    }

    .health-fill {
        height: 100%;
        background: linear-gradient(90deg, #9370db, #ff6b6b);
        transition: width 0.3s;
    }

    .health-value {
        width: 45px;
        font-size: 0.9rem;
        color: #9370db;
        text-align: right;
    }

    .delegation-info {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .delegated-badge {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem;
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid #4caf50;
        border-radius: 0.5rem;
        font-size: 0.9rem;
    }

    .change-delegate {
        padding: 0.25rem 0.5rem;
        background: none;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
    }

    .delegate-prompt {
        width: 100%;
        padding: 0.75rem;
        background: rgba(147, 112, 219, 0.2);
        border: 1px dashed #9370db;
        border-radius: 0.5rem;
        color: #9370db;
        cursor: pointer;
        transition: all 0.2s;
    }

    .delegate-prompt:hover {
        background: rgba(147, 112, 219, 0.3);
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal-content {
        width: 90%;
        max-width: 600px;
        max-height: 90vh;
        overflow-y: auto;
    }

    @media (max-width: 1024px) {
        .governance-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 768px) {
        .governance {
            padding: 1rem;
        }

        .filter-controls {
            flex-direction: column;
        }

        .filter-tabs {
            justify-content: center;
        }
    }
</style>
