<script lang="ts">
    import { goto } from "$app/navigation";
    // Mock vault store to prevent import errors if it doesn't exist
    // Replace with actual import if it exists properly
    const vaultStore = {

        sendTransaction: async (data: any) => {
            return new Promise((resolve) => setTimeout(resolve, 1000));
        },
    };

    let amount = "";
    let recipient = "";
    let asset = "USDC";
    let loading = false;

    async function handleSend() {
        loading = true;
        try {
            await vaultStore.sendTransaction({
                to: recipient,
                amount: parseFloat(amount),
                asset,
            });
            goto("/dashboard/sovereign");
        } catch (error) {
            console.error("Send failed:", error);
        } finally {
            loading = false;
        }
    }
</script>

<div class="send-page">
    <h1 class="glow-text">Send Assets</h1>
    <p class="subtitle">Transfer value across the Cathedral</p>

    <div class="send-card glass">
        <div class="form-group">
            <label for="send-recipient">Recipient</label>
            <input
                id="send-recipient"
                aria-required="true"
                type="text"
                bind:value={recipient}
                placeholder="Enter address or @username"
                class="glass-input"
            />
        </div>

        <div class="form-group">
            <label for="send-amount">Amount</label>
            <input
                id="send-amount"
                aria-required="true"
                type="number"
                bind:value={amount}
                placeholder="0.00"
                class="glass-input"
            />
        </div>

        <div class="form-group">
            <label for="send-asset">Asset</label>
            <select id="send-asset" bind:value={asset} class="glass-select">
                <option value="USDC">USDC</option>
                <option value="AGE">AGE</option>
                <option value="SYND">SYND</option>
            </select>
        </div>

        <button
            class="send-button"
            onclick={handleSend}
            disabled={loading || !amount || !recipient}
        >
            {loading ? "Sending..." : "Send"}
        </button>
    </div>
</div>

<style>
    .send-page {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 2rem;
    }

    .send-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.7);
    }

    .glass-input {
        width: 100%;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .glass-input:focus {
        outline: none;
        border-color: #4caf50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }

    .glass-select {
        width: 100%;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-size: 1rem;
    }

    .send-button {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #4caf50, #45a049);
        border: none;
        border-radius: 12px;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 1rem;
    }

    .send-button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
    }

    .send-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
