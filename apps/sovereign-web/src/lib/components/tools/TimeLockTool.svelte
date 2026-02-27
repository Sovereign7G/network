<script lang="ts">
    let unlockDate = "";
    let amount = 1000;
    let asset = "SYND";

    function scheduleLock() {
        alert(`Asset ${amount} ${asset} locked until ${unlockDate}`);
    }
</script>

<div class="timelock-tool">
    <div class="header-info">
        <p>Cryptographically lock assets until a predefined timestamp.</p>
    </div>

    <div class="input-row">
        <div class="input-group flex-2">
            <label for="lock-amount">Amount</label>
            <input id="lock-amount" type="number" bind:value={amount} />
        </div>
        <div class="input-group flex-1">
            <label for="lock-asset">Asset</label>
            <select id="lock-asset" bind:value={asset}>
                <option value="SYND">SYND</option>
                <option value="AGE">AGE</option>
                <option value="USDC">USDC</option>
            </select>
        </div>
    </div>

    <div class="input-group">
        <label for="unlock-date">Unlock Date (UTC)</label>
        <input id="unlock-date" type="datetime-local" bind:value={unlockDate} />
    </div>

    <button
        class="lock-btn"
        onclick={scheduleLock}
        disabled={!unlockDate || !amount}
    >
        Engage Time Lock
    </button>
</div>

<style>
    .timelock-tool {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .header-info p {
        margin: 0;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
    }

    .input-row {
        display: flex;
        gap: 0.5rem;
    }

    .input-group label {
        display: block;
        font-size: 0.75rem;
        color: rgba(255, 215, 0, 0.7);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .flex-1 {
        flex: 1;
    }
    .flex-2 {
        flex: 2;
    }

    input,
    select {
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 8px;
        color: white;
        box-sizing: border-box;
    }

    input[type="datetime-local"]::-webkit-calendar-picker-indicator {
        filter: invert(1);
        cursor: pointer;
    }

    .lock-btn {
        padding: 1rem;
        background: linear-gradient(
            135deg,
            rgba(255, 0, 0, 0.8),
            rgba(200, 0, 0, 0.9)
        );
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s;
    }

    .lock-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .lock-btn:hover:not(:disabled) {
        transform: scale(1.02);
    }
</style>
