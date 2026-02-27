<script lang="ts">
    import { PROPOSAL_TYPES } from "$lib/stores/constants";

    interface Props {
        onClose: () => void;
        onCreate: (proposal: any) => void;
    }

    let { onClose, onCreate }: Props = $props();

    let step = $state(1);
    let proposal = $state({
        title: "",
        description: "",
        type: PROPOSAL_TYPES.PARAMETER.id,
        details: {} as any,
        discussion: "",
    });

    let errors = $state({} as any);
    let isSubmitting = $state(false);

    function validateStep1() {
        errors = {};

        if (!proposal.title.trim()) {
            errors.title = "Title is required";
        }

        if (!proposal.description.trim()) {
            errors.description = "Description is required";
        }

        return Object.keys(errors).length === 0;
    }

    function nextStep() {
        if (validateStep1()) {
            step = 2;
        }
    }

    function handleSubmit() {
        isSubmitting = true;

        // Simulate blockchain transaction
        setTimeout(() => {
            onCreate(proposal);
            isSubmitting = false;
        }, 1500);
    }
</script>

<div class="create-proposal-modal">
    <div class="modal-header">
        <h2 class="modal-title">
            <span class="title-icon">📝</span>
            Create Proposal
        </h2>
        <button class="close-btn" onclick={onClose}>✕</button>
    </div>

    <div class="modal-body">
        <!-- Progress steps -->
        <div class="progress-steps">
            <div
                class="step"
                class:active={step === 1}
                class:completed={step > 1}
            >
                <span class="step-number">1</span>
                <span class="step-label">Details</span>
            </div>
            <div class="step-line" class:active={step > 1}></div>
            <div class="step" class:active={step === 2}>
                <span class="step-number">2</span>
                <span class="step-label">Parameters</span>
            </div>
        </div>

        {#if step === 1}
            <div class="step-content">
                <div class="form-group">
                    <label for="proposal-type" class="form-label"
                        >Proposal Type</label
                    >
                    <select
                        id="proposal-type"
                        class="form-select"
                        bind:value={proposal.type}
                    >
                        {#each Object.values(PROPOSAL_TYPES) as type}
                            <option value={type.id}>
                                {type.icon}
                                {type.label}
                            </option>
                        {/each}
                    </select>
                </div>

                <div class="form-group">
                    <label for="proposal-title" class="form-label">
                        Title <span class="required">*</span>
                    </label>
                    <input
                        type="text"
                        id="proposal-title"
                        class="form-input"
                        class:error={errors.title}
                        bind:value={proposal.title}
                        placeholder="Brief, descriptive title"
                    />
                    {#if errors.title}
                        <span class="error-message">{errors.title}</span>
                    {/if}
                </div>

                <div class="form-group">
                    <label for="proposal-description" class="form-label">
                        Description <span class="required">*</span>
                    </label>
                    <textarea
                        id="proposal-description"
                        class="form-textarea"
                        class:error={errors.description}
                        bind:value={proposal.description}
                        placeholder="Explain your proposal in detail..."
                        rows="4"
                    ></textarea>
                    {#if errors.description}
                        <span class="error-message">{errors.description}</span>
                    {/if}
                </div>
            </div>
        {:else if step === 2}
            <div class="step-content">
                {#if proposal.type === PROPOSAL_TYPES.PARAMETER.id}
                    <div class="form-group">
                        <label for="parameter-name" class="form-label"
                            >Parameter Name</label
                        >
                        <input
                            type="text"
                            id="parameter-name"
                            class="form-input"
                            bind:value={proposal.details.parameter}
                            placeholder="e.g., hearth.resonance.multiplier"
                        />
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="current-value" class="form-label"
                                >Current Value</label
                            >
                            <input
                                type="text"
                                id="current-value"
                                class="form-input"
                                bind:value={proposal.details.currentValue}
                                placeholder="1.0"
                            />
                        </div>

                        <div class="form-group">
                            <label for="proposed-value" class="form-label"
                                >Proposed Value</label
                            >
                            <input
                                type="text"
                                id="proposed-value"
                                class="form-input"
                                bind:value={proposal.details.proposedValue}
                                placeholder="1.2"
                            />
                        </div>
                    </div>
                {:else if proposal.type === PROPOSAL_TYPES.TREASURY.id}
                    <div class="form-group">
                        <label for="amount" class="form-label"
                            >Amount (AGE)</label
                        >
                        <input
                            type="number"
                            id="amount"
                            class="form-input"
                            bind:value={proposal.details.amount}
                            placeholder="50000"
                        />
                    </div>

                    <div class="form-group">
                        <label for="recipient" class="form-label"
                            >Recipient</label
                        >
                        <input
                            type="text"
                            id="recipient"
                            class="form-input"
                            bind:value={proposal.details.recipient}
                            placeholder="Address or description"
                        />
                    </div>
                {/if}

                <div class="form-group">
                    <label for="rationale" class="form-label">Rationale</label>
                    <textarea
                        id="rationale"
                        class="form-textarea"
                        bind:value={proposal.details.rationale}
                        placeholder="Explain why this change is needed..."
                        rows="3"
                    ></textarea>
                </div>

                <div class="form-group">
                    <label for="discussion" class="form-label"
                        >Discussion Link (Optional)</label
                    >
                    <input
                        type="url"
                        id="discussion"
                        class="form-input"
                        bind:value={proposal.discussion}
                        placeholder="https://forum.ageprotocol.com/..."
                    />
                </div>
            </div>
        {/if}

        <div class="fee-info">
            <span>Proposal Creation Fee</span>
            <span>100 AGE</span>
        </div>

        <div class="modal-actions">
            {#if step === 1}
                <button class="cancel-btn" onclick={onClose}> Cancel </button>
                <button class="next-btn" onclick={nextStep}> Next → </button>
            {:else}
                <button class="cancel-btn" onclick={onClose}> Cancel </button>
                <button class="back-btn" onclick={() => (step = 1)}>
                    ← Back
                </button>
                <button
                    class="submit-btn"
                    onclick={handleSubmit}
                    disabled={isSubmitting}
                >
                    {#if isSubmitting}
                        <span class="spinner"></span>
                        <span>Creating...</span>
                    {:else}
                        <span>Submit Proposal</span>
                    {/if}
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    .create-proposal-modal {
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

    .progress-steps {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }

    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .step-number {
        width: 2rem;
        height: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .step.active .step-number {
        background: #9370db;
        border-color: #9370db;
    }

    .step.completed .step-number {
        background: #4caf50;
        border-color: #4caf50;
    }

    .step-label {
        font-size: 0.9rem;
    }

    .step-line {
        flex: 1;
        height: 2px;
        background: rgba(255, 255, 255, 0.1);
        margin: 0 1rem;
        transition: background 0.2s;
    }

    .step-line.active {
        background: #9370db;
    }

    .step-content {
        margin-bottom: 1.5rem;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .required {
        color: #ff6b6b;
    }

    .form-input,
    .form-textarea,
    .form-select {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: inherit;
    }

    .form-input:focus,
    .form-textarea:focus,
    .form-select:focus {
        outline: none;
        border-color: #9370db;
    }

    .form-input.error {
        border-color: #ff6b6b;
    }

    .error-message {
        display: block;
        margin-top: 0.25rem;
        color: #ff6b6b;
        font-size: 0.8rem;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .fee-info {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
    }

    .cancel-btn,
    .back-btn,
    .next-btn,
    .submit-btn {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .cancel-btn,
    .back-btn {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .cancel-btn:hover,
    .back-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .next-btn,
    .submit-btn {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
    }

    .next-btn:hover,
    .submit-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .submit-btn:disabled {
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
        display: inline-block;
        margin-right: 0.5rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
