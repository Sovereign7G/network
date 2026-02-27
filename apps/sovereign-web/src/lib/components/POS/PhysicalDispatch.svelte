<script lang="ts">
    import { onMount } from "svelte";

    export let merchantId: string = "did:age:merchant_brazil";
    export let merchantLocation: { lat: number; lng: number } = {
        lat: -23.5505,
        lng: -46.6333,
    };

    let deliveryMode = false;
    let deliveryRadius = 3; // km
    let deliveryFee = 5.0; // BRL
    let deliveryFeeUSDC = 1.0; // Approx $1
    let activeDeliveries: any[] = [];

    onMount(() => {
        // Simulated subscription to Courier acceptance events
    });

    async function generateDeliveryQR() {
        // A mock order generator for UI demonstration
        const order = {
            id: Math.floor(Math.random() * 10000),
            customer: {
                address: "Avenida Paulista",
                location: { lat: -23.5614, lng: -46.6564 },
            },
        };
        activeDeliveries = [
            ...activeDeliveries,
            {
                orderId: order.id,
                status: "accepted",
                destination: { description: order.customer.address },
                courierAlias: "João Costa",
                reward: { amount: deliveryFeeUSDC },
            },
        ];
    }

    async function confirmDelivery(orderId: string) {
        activeDeliveries = activeDeliveries.filter(
            (d) => d.orderId !== orderId,
        );
        alert("✅ Delivery confirmed! Payment released to courier.");
    }
</script>

{#if deliveryMode}
    <div class="delivery-panel">
        <h2>📦 Entrega via AGE (Sem Taxas)</h2>

        <div class="settings">
            <label>
                <span class="label-text">Raio de entrega</span>
                <input
                    type="range"
                    bind:value={deliveryRadius}
                    min="1"
                    max="10"
                    step="0.5"
                />
                <span class="value-text">{deliveryRadius} km</span>
            </label>

            <label>
                <span class="label-text">Taxa (R$)</span>
                <input
                    type="number"
                    bind:value={deliveryFee}
                    step="0.50"
                    min="0"
                />
                <span class="value-text"
                    >≈ ${(deliveryFee / 5).toFixed(2)} USDC</span
                >
            </label>
            <button class="generate-qr-btn" onclick={generateDeliveryQR}
                >Gerar age://dispatch QR</button
            >
        </div>

        <div class="active-deliveries">
            <h3>Entregas ativas</h3>
            {#if activeDeliveries.length === 0}
                <p class="empty-state">Nenhuma entrega em andamento</p>
            {/if}
            {#each activeDeliveries as delivery}
                <div class="delivery-card">
                    <div class="delivery-header">
                        <span class="order-id">Pedido #{delivery.orderId}</span>
                        <span class="status {delivery.status}"
                            >{delivery.status}</span
                        >
                    </div>

                    <div class="delivery-details">
                        <div class="detail-row">
                            <span class="label">Destino:</span>
                            <span class="val"
                                >{delivery.destination.description}</span
                            >
                        </div>
                        <div class="detail-row">
                            <span class="label">Entregador:</span>
                            <span class="val">{delivery.courierAlias}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Recompensa:</span>
                            <span class="val reward-val"
                                >${delivery.reward.amount} USDC</span
                            >
                        </div>
                    </div>

                    <button
                        class="confirm-delivery"
                        onclick={() => confirmDelivery(delivery.orderId)}
                    >
                        ✅ Confirmar (NFC / QR Sync)
                    </button>
                </div>
            {/each}
        </div>

        <button class="back" onclick={() => (deliveryMode = false)}
            >← Voltar ao PDV</button
        >
    </div>
{:else}
    <div class="pos-actions">
        <button class="delivery-btn" onclick={() => (deliveryMode = true)}>
            🚚 AGE Courier Mode (Bypass Uber)
        </button>
    </div>
{/if}

<style>
    .delivery-panel {
        padding: 24px;
        background: #111;
        color: white;
        border-radius: 12px;
        font-family: "Inter", sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h2 {
        margin-top: 0;
        color: #4caf50;
        font-size: 20px;
    }

    .settings {
        background: rgba(255, 255, 255, 0.05);
        padding: 18px;
        border-radius: 8px;
        margin: 20px 0;
    }
    .settings label {
        display: flex;
        align-items: center;
        gap: 15px;
        margin: 12px 0;
    }
    .label-text {
        width: 120px;
        font-size: 13px;
        color: #ccc;
    }
    .value-text {
        width: 80px;
        text-align: right;
        font-size: 13px;
        color: #4caf50;
        font-family: "Menlo", monospace;
    }
    .settings input[type="range"] {
        flex: 1;
        accent-color: #4caf50;
    }
    .settings input[type="number"] {
        width: 80px;
        background: #222;
        border: 1px solid #444;
        color: white;
        padding: 6px;
        border-radius: 4px;
    }

    .generate-qr-btn {
        padding: 10px;
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
        border: 1px solid #4caf50;
        width: 100%;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        margin-top: 10px;
    }

    h3 {
        font-size: 16px;
        margin-bottom: 15px;
        color: #eee;
    }
    .empty-state {
        color: #666;
        font-size: 13px;
        font-style: italic;
    }

    .delivery-card {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: #1a1a1a;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    .delivery-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .order-id {
        font-weight: bold;
        font-family: "Menlo", monospace;
        font-size: 13px;
        color: #fff;
    }
    .status {
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .status.accepted {
        background: rgba(33, 150, 243, 0.2);
        color: #2196f3;
    }

    .delivery-details {
        margin: 12px 0;
        font-size: 13px;
    }
    .detail-row {
        display: flex;
        align-items: center;
        margin: 6px 0;
    }
    .label {
        color: #888;
        width: 90px;
    }
    .val {
        color: #eee;
    }
    .reward-val {
        color: #4caf50;
        font-weight: bold;
    }

    .confirm-delivery {
        width: 100%;
        padding: 12px;
        background: #4caf50;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 12px;
    }
    .back {
        margin-top: 24px;
        padding: 12px;
        background: #222;
        color: #ccc;
        border: 1px solid #333;
        border-radius: 6px;
        width: 100%;
        cursor: pointer;
    }

    .pos-actions {
        padding: 20px;
        background: #111;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .delivery-btn {
        background: #4caf50;
        color: white;
        border: none;
        padding: 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        width: 100%;
    }
</style>
