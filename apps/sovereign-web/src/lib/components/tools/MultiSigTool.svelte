<script lang="ts">
    let requiredSignatures = 2;
    let totalSignatories = 3;
    let signatories = ["0xTreasury...", "0xCouncil...", ""];

    function addSignatory() {
        signatories = [...signatories, ""];
        totalSignatories = signatories.length;
    }

    function deployVault() {
        alert(
            `Deploying Multi-Sig Vault (${requiredSignatures}/${totalSignatories})`,
        );
    }
</script>

<div class="multisig-tool">
    <div class="header-info">
        <p>Configure an M-of-N sovereign vault for distributed authority.</p>
    </div>

    <div class="threshold-config">
        <div class="input-group">
            <label for="required-sigs">Required Signatures (M)</label>
            <input
                id="required-sigs"
                type="number"
                bind:value={requiredSignatures}
                min="1"
                max={totalSignatories}
            />
        </div>
        <div class="sync-symbol">/</div>
        <div class="input-group">
            <label for="total-signatories">Total Signatories (N)</label>
            <input
                id="total-signatories"
                type="number"
                bind:value={totalSignatories}
                disabled
            />
        </div>
    </div>

    <div
        class="signatories-list"
        role="group"
        aria-labelledby="signatories-title"
    >
        <span id="signatories-title" class="group-label"
            >Signatory Addresses</span
        >
        {#each signatories as sig, i}
            <input
                type="text"
                bind:value={signatories[i]}
                placeholder="0x..."
                aria-label="Signatory {i + 1}"
            />
        {/each}
        <button class="add-btn" onclick={addSignatory}>+ Add Signatory</button>
    </div>

    <button class="deploy-btn" onclick={deployVault}>
        Deploy Multi-Sig Vault
    </button>
</div>

<style>
    .multisig-tool {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .header-info p {
        margin: 0;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
    }

    .threshold-config {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }

    .input-group {
        flex: 1;
    }

    .input-group label {
        display: block;
        font-size: 0.75rem;
        color: rgba(255, 215, 0, 0.7);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    input {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 8px;
        color: white;
        box-sizing: border-box;
    }

    input:disabled {
        opacity: 0.5;
    }

    .sync-symbol {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.3);
        padding-top: 1rem;
    }

    .signatories-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .signatories-list .group-label {
        font-size: 0.75rem;
        color: rgba(255, 215, 0, 0.7);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        display: block;
    }

    .add-btn {
        padding: 0.5rem;
        background: transparent;
        border: 1px dashed rgba(255, 215, 0, 0.3);
        color: rgba(255, 215, 0, 0.7);
        border-radius: 8px;
        cursor: pointer;
        margin-top: 0.5rem;
    }

    .add-btn:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #ffd700;
        color: #ffd700;
    }

    .deploy-btn {
        padding: 1rem;
        background: #ffd700;
        border: none;
        border-radius: 8px;
        color: #0a0a0f;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
    }

    .deploy-btn:hover {
        background: #fff;
        transform: translateY(-2px);
    }
</style>
