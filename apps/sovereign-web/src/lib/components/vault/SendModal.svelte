<script lang="ts">
    import { cleanRoom } from "../../../../../../packages/age-cleanroom/src/store/clean-room-store";
    import ContextFlush from "../../../../../../packages/age-cleanroom/src/gestures/ContextFlush.svelte";
    import VerificationOverlay from "../../../../../../packages/age-cleanroom/src/components/VerificationOverlay.svelte";

    let { asset, balance, onsend, onclose } = $props();

    let amount = $state("");
    let recipient = $state("");
    let memo = $state("");
    let error = $state("");
    let isProcessing = $state(false);
    let showCleanRoom = $state(false);
    let pendingTransaction = $state(null as any);

    let flushTrigger = $state(null as any);

    function handleSend() {
        error = "";

        // Validation
        if (!recipient) {
            error = "Recipient address is required";
            return;
        }

        if (!amount || parseFloat(amount) <= 0) {
            error = "Please enter a valid amount";
            return;
        }

        if (parseFloat(amount) > balance) {
            error = "Insufficient balance";
            return;
        }

        // Trigger Clean Room for large transactions (using $1000 heuristic)
        // For simplicity, we assume 1 unit = $1 if not USDC/AGE
        const val = parseFloat(amount);
        if (val >= 1000) {
            flushTrigger?.startPress(val);
        } else {
            executeFinalSend();
        }
    }

    function handleFlush(event: CustomEvent) {
        pendingTransaction = {
            id: `tx-${Date.now()}`,
            type: "SEND",
            from: "0xabcd...efgh", // Mock current address
            to: recipient,
            amount: event.detail.amount,
            asset: asset,
            timestamp: Date.now(),
        };
        showCleanRoom = true;
    }

    function handleConfirmed() {
        showCleanRoom = false;
        executeFinalSend();
    }

    function handleCancelled() {
        showCleanRoom = false;
        pendingTransaction = null;
        cleanRoom.deactivate();
    }

    function executeFinalSend() {
        isProcessing = true;

        // Simulate blockchain transaction
        setTimeout(() => {
            if (onsend) {
                onsend({
                    type: "send",
                    asset,
                    amount: parseFloat(amount),
                    to: recipient,
                    memo,
                    from: "0xabcd...efgh",
                    status: "pending",
                });
            }
            isProcessing = false;
        }, 1500);
    }

    function setMaxAmount() {
        amount = balance.toString();
    }
</script>

<div class="send-modal">
    <div class="modal-header">
        <h2 class="modal-title">
            <span class="title-icon">📤</span>
            Send {asset}
        </h2>
        <button class="close-button" onclick={() => onclose && onclose()}
            >✕</button
        >
    </div>

    <div class="modal-body">
        <div class="balance-info">
            <span class="info-label">Available Balance</span>
            <span class="info-value">{balance.toFixed(4)} {asset}</span>
        </div>

        <form
            onsubmit={(e) => {
                e.preventDefault();
                handleSend();
            }}
        >
            <div class="form-group">
                <label for="recipient" class="form-label"
                    >Recipient Address</label
                >
                <input
                    type="text"
                    id="recipient"
                    class="form-input"
                    bind:value={recipient}
                    placeholder="0x... or did:age:..."
                    disabled={isProcessing}
                />
            </div>

            <div class="form-group">
                <label for="amount" class="form-label">Amount</label>
                <div class="amount-input-wrapper">
                    <input
                        type="number"
                        id="amount"
                        class="form-input amount-input"
                        bind:value={amount}
                        placeholder="0.00"
                        step="0.01"
                        min="0"
                        max={balance}
                        disabled={isProcessing}
                    />
                    <button
                        type="button"
                        class="max-button"
                        onclick={setMaxAmount}
                        disabled={isProcessing}
                    >
                        MAX
                    </button>
                </div>
                <span class="input-hint"
                    >≈ ${((parseFloat(amount) || 0) * 1.25).toFixed(2)} USD</span
                >
            </div>

            <div class="form-group">
                <label for="memo" class="form-label">Memo (Optional)</label>
                <input
                    type="text"
                    id="memo"
                    class="form-input"
                    bind:value={memo}
                    placeholder="What's this for?"
                    disabled={isProcessing}
                />
            </div>

            {#if error}
                <div class="error-message">
                    ⚠️ {error}
                </div>
            {/if}

            <div class="fee-info">
                <span>Network Fee</span>
                <span>≈ 0.001 {asset}</span>
            </div>

            <div class="modal-actions">
                <button
                    type="button"
                    class="cancel-button"
                    onclick={() => onclose && onclose()}
                    disabled={isProcessing}
                >
                    Cancel
                </button>

                <ContextFlush
                    threshold={2000}
                    targetAmount={1000}
                    onFlush={handleFlush}
                    bind:this={flushTrigger}
                >
                    <svelte:fragment slot="trigger" let:startPress>
                        <button
                            type="submit"
                            class="send-button"
                            disabled={isProcessing || !recipient || !amount}
                            class:processing={isProcessing}
                            class:high-value={parseFloat(amount) >= 1000}
                        >
                            {#if isProcessing}
                                <span class="spinner"></span>
                                <span>Processing...</span>
                            {:else}
                                <span>
                                    {parseFloat(amount) >= 1000 ? "🔒 " : ""}
                                    Send {asset}
                                </span>
                            {/if}
                        </button>
                    </svelte:fragment>
                </ContextFlush>
            </div>
        </form>
    </div>

    {#if showCleanRoom && pendingTransaction}
        <VerificationOverlay
            transaction={pendingTransaction}
            onConfirmed={handleConfirmed}
            onCancelled={handleCancelled}
        />
    {/if}
</div>

<style>
    .send-modal {
        background: #1a1a1a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        overflow: hidden;
        color: white;
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

    .close-button {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s;
    }

    .close-button:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .modal-body {
        padding: 1.5rem;
    }

    .balance-info {
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
        opacity: 0.7;
    }

    .info-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #9370db;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .form-input {
        width: 100%;
        box-sizing: border-box;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: inherit;
    }

    .form-input:focus {
        outline: none;
        border-color: #9370db;
    }

    .amount-input-wrapper {
        display: flex;
        gap: 0.5rem;
    }

    .amount-input {
        flex: 1;
    }

    .max-button {
        padding: 0.75rem 1rem;
        background: rgba(147, 112, 219, 0.2);
        border: 1px solid #9370db;
        border-radius: 0.5rem;
        color: #9370db;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .max-button:hover:not(:disabled) {
        background: #9370db;
        color: white;
    }

    .input-hint {
        display: block;
        margin-top: 0.25rem;
        font-size: 0.8rem;
        opacity: 0.5;
    }

    .error-message {
        padding: 0.75rem;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 0.5rem;
        color: #ff6b6b;
        margin-bottom: 1rem;
    }

    .fee-info {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
    }

    .cancel-button,
    .send-button {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        box-sizing: border-box;
    }

    .cancel-button {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .cancel-button:hover:not(:disabled) {
        background: rgba(255, 255, 255, 0.1);
    }

    .send-button {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .send-button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .send-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .send-button.processing {
        cursor: wait;
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
</style>
