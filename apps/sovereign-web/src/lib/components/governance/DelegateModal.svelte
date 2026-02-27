<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let currentDelegate = null;
    export let councilMembers: any[] = [];
    export let votingPower = 0;

    const dispatch = createEventDispatcher();


    let delegateAddress = currentDelegate || "";
    let customAddress = "";
    let delegateType = currentDelegate ? "council" : "custom";
    let selectedCouncilMember = currentDelegate || "";

    function handleDelegate() {
        let address =
            delegateType === "council" ? selectedCouncilMember : customAddress;
        if (address) {
            dispatch("delegate", address);
        }
    }
</script>

<div class="delegate-modal">
    <div class="modal-header">
        <h2 class="modal-title">
            <span class="title-icon">🤝</span>
            Delegate Voting Power
        </h2>
        <button class="close-btn" onclick={() => dispatch("close")}>✕</button>
    </div>

    <div class="modal-body">
        <div class="voting-power-info">
            <span class="info-label">Your Voting Power</span>
            <span class="info-value">{votingPower}</span>
        </div>

        <div class="delegate-options">
            <label class="option-label">
                <input
                    type="radio"
                    bind:group={delegateType}
                    value="council"
                    checked={delegateType === "council"}
                />
                <span>Delegate to Council Member</span>
            </label>

            {#if delegateType === "council"}
                <select
                    class="council-select"
                    bind:value={selectedCouncilMember}
                >
                    <option value="">Select a council member...</option>
                    {#each councilMembers as member}
                        <option value={member.address}>
                            {member.name} ({member.votingPower} power)
                        </option>
                    {/each}
                </select>
            {/if}

            <label class="option-label">
                <input type="radio" bind:group={delegateType} value="custom" />
                <span>Delegate to Custom Address</span>
            </label>

            {#if delegateType === "custom"}
                <input
                    type="text"
                    class="custom-address"
                    bind:value={customAddress}
                    placeholder="0x... or did:age:..."
                />
            {/if}
        </div>

        <div class="delegate-info">
            <p class="info-text">
                Delegating your voting power allows someone else to vote on your
                behalf. You can change or revoke your delegation at any time.
            </p>
        </div>

        <div class="modal-actions">
            <button class="cancel-btn" onclick={() => dispatch("close")}>
                Cancel
            </button>
            <button
                class="delegate-btn"
                onclick={handleDelegate}
                disabled={delegateType === "council"
                    ? !selectedCouncilMember
                    : !customAddress}
            >
                Delegate Power
            </button>
        </div>
    </div>
</div>

<style>
    .delegate-modal {
        background: #1a1a1a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        overflow: hidden;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .modal-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 1.3rem;
    }

    .title-icon {
        font-size: 1.5rem;
    }

    .close-btn {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        font-size: 1.2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .modal-body {
        padding: 1.5rem;
    }

    .voting-power-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid rgba(147, 112, 219, 0.2);
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .info-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .info-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #9370db;
    }

    .delegate-options {
        margin-bottom: 1.5rem;
    }

    .option-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        cursor: pointer;
    }

    .council-select,
    .custom-address {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }

    .council-select:focus,
    .custom-address:focus {
        outline: none;
        border-color: #9370db;
    }

    .delegate-info {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0.5rem;
    }

    .info-text {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.7;
        line-height: 1.5;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
    }

    .cancel-btn,
    .delegate-btn {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .cancel-btn {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .cancel-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .delegate-btn {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
    }

    .delegate-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .delegate-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
