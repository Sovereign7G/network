<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let asset;
    export let address;

    const dispatch = createEventDispatcher();

    let copied = false;

    function copyAddress() {
        navigator.clipboard.writeText(address);
        copied = true;
        setTimeout(() => (copied = false), 2000);
    }
</script>

<div class="receive-modal">
    <div class="modal-header">
        <h2 class="modal-title">
            <span class="title-icon">📥</span>
            Receive {asset}
        </h2>
        <button class="close-button" on:click={() => dispatch("close")}
            >✕</button
        >
    </div>

    <div class="modal-body">
        <div class="qr-code">
            <!-- Placeholder for QR code - in production, generate actual QR -->
            <div class="qr-placeholder">
                <span class="qr-icon">📱</span>
                <span class="qr-text">QR Code</span>
            </div>
        </div>

        <div class="address-section">
            <label class="address-label">Your {asset} Address</label>
            <div class="address-box">
                <code class="address">{address}</code>
                <button class="copy-button" on:click={copyAddress}>
                    <span class="copy-icon">{copied ? "✅" : "📋"}</span>
                </button>
            </div>
            {#if copied}
                <span class="copied-message">Copied to clipboard!</span>
            {/if}
        </div>

        <div class="warning-note">
            <span class="warning-icon">⚠️</span>
            <span
                >Send only {asset} to this address. Other assets may be lost.</span
            >
        </div>

        <div class="modal-actions">
            <button class="done-button" on:click={() => dispatch("close")}>
                Done
            </button>
        </div>
    </div>
</div>

<style>
    .receive-modal {
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
        padding: 2rem;
    }

    .qr-code {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .qr-placeholder {
        width: 200px;
        height: 200px;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border-radius: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        opacity: 0.8;
    }

    .qr-icon {
        font-size: 3rem;
    }

    .qr-text {
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .address-section {
        margin-bottom: 1.5rem;
    }

    .address-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .address-box {
        display: flex;
        align-items: center;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        overflow: hidden;
    }

    .address {
        flex: 1;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.9rem;
        word-break: break-all;
    }

    .copy-button {
        padding: 1rem;
        background: none;
        border: none;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .copy-button:hover {
        background: rgba(147, 112, 219, 0.2);
    }

    .copied-message {
        display: block;
        margin-top: 0.5rem;
        color: #4caf50;
        font-size: 0.9rem;
        text-align: center;
    }

    .warning-note {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid #ffc107;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }

    .warning-icon {
        font-size: 1.2rem;
    }

    .modal-actions {
        display: flex;
        justify-content: center;
    }

    .done-button {
        padding: 1rem 3rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 2rem;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .done-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }
</style>
