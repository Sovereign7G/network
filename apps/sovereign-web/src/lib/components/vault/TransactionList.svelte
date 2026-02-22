<script lang="ts">
    export let transactions = [];

    function formatDate(date) {
        if (!date) return "";
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) return "Just now";
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }

    function getTransactionIcon(type) {
        switch (type) {
            case "receive":
                return "📥";
            case "send":
                return "📤";
            case "stake":
                return "🔒";
            default:
                return "🔄";
        }
    }

    function getTransactionColor(type) {
        switch (type) {
            case "receive":
                return "#4ECDC4";
            case "send":
                return "#FF6B6B";
            case "stake":
                return "#9370DB";
            default:
                return "#FFD700";
        }
    }
</script>

<div class="transaction-list">
    {#if transactions.length === 0}
        <div class="empty-state">
            <span class="empty-icon">📭</span>
            <p>No transactions found</p>
        </div>
    {:else}
        {#each transactions as tx (tx.id)}
            <div class="transaction-item">
                <div
                    class="transaction-icon"
                    style="background: {getTransactionColor(
                        tx.type,
                    )}20; color: {getTransactionColor(tx.type)}"
                >
                    {getTransactionIcon(tx.type)}
                </div>

                <div class="transaction-info">
                    <div class="transaction-header">
                        <span class="transaction-type">
                            {tx.type.charAt(0).toUpperCase() + tx.type.slice(1)}
                            {tx.asset}
                        </span>
                        <span
                            class="transaction-amount"
                            class:positive={tx.type === "receive"}
                            class:negative={tx.type === "send"}
                        >
                            {tx.type === "receive" ? "+" : "-"}{tx.amount}
                            {tx.asset}
                        </span>
                    </div>

                    <div class="transaction-details">
                        {#if tx.from && tx.from !== "0xabcd...efgh"}
                            <span class="transaction-address"
                                >From: {tx.from}</span
                            >
                        {/if}
                        {#if tx.to && tx.to !== "0xabcd...efgh" && tx.to !== "staking_pool"}
                            <span class="transaction-address">To: {tx.to}</span>
                        {/if}
                        {#if tx.to === "staking_pool"}
                            <span class="transaction-address">Staking Pool</span
                            >
                        {/if}
                    </div>

                    <div class="transaction-footer">
                        <span class="transaction-time"
                            >{formatDate(new Date(tx.timestamp))}</span
                        >
                        <span
                            class="transaction-status"
                            class:confirmed={tx.status === "confirmed"}
                            class:pending={tx.status === "pending"}
                        >
                            {tx.status === "confirmed"
                                ? "✓ Confirmed"
                                : "⏳ Pending"}
                        </span>
                    </div>
                </div>

                {#if tx.hash}
                    <button class="view-button" title="View on explorer">
                        🔍
                    </button>
                {/if}
            </div>
        {/each}
    {/if}
</div>

<style>
    .transaction-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 1rem;
        border: 1px dashed rgba(255, 255, 255, 0.1);
    }

    .empty-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    .empty-state p {
        margin: 0;
        opacity: 0.7;
    }

    .transaction-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        transition: all 0.2s;
    }

    .transaction-item:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: #9370db;
    }

    .transaction-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .transaction-info {
        flex: 1;
    }

    .transaction-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.25rem;
    }

    .transaction-type {
        font-weight: 500;
        font-size: 0.9rem;
    }

    .transaction-amount {
        font-weight: 600;
    }

    .transaction-amount.positive {
        color: #4ecdc4;
    }

    .transaction-amount.negative {
        color: #ff6b6b;
    }

    .transaction-details {
        margin-bottom: 0.25rem;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .transaction-address {
        font-family: monospace;
    }

    .transaction-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.7rem;
    }

    .transaction-time {
        opacity: 0.5;
    }

    .transaction-status {
        padding: 0.2rem 0.5rem;
        border-radius: 1rem;
    }

    .transaction-status.confirmed {
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
    }

    .transaction-status.pending {
        background: rgba(255, 193, 7, 0.2);
        color: #ffc107;
    }

    .view-button {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
        opacity: 0.5;
    }

    .view-button:hover {
        opacity: 1;
        background: rgba(255, 255, 255, 0.1);
    }
</style>
