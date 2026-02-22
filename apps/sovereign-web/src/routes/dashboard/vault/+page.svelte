<script lang="ts">
    import { onMount } from "svelte";
    import { vaultStore, sovereignStore } from "$lib/stores/master-store";
    import AssetCard from "$lib/components/vault/AssetCard.svelte";
    import TransactionList from "$lib/components/vault/TransactionList.svelte";
    import AllocationChart from "$lib/components/vault/AllocationChart.svelte";
    import PriceChart from "$lib/components/vault/PriceChart.svelte";
    import SendModal from "$lib/components/vault/SendModal.svelte";
    import ReceiveModal from "$lib/components/vault/ReceiveModal.svelte";
    import ForensicYieldExplorer from "$lib/components/dashboard/ForensicYieldExplorer.svelte";
    import CapitalFormationVitals from "$lib/components/dashboard/CapitalFormationVitals.svelte";

    import Tile from "$lib/components/ui/Tile.svelte";
    import GlassCard from "$lib/components/ui/GlassCard.svelte";
    import QuickActions from "$lib/components/dashboard/QuickActions.svelte";
    import { tooltip } from "$lib/actions/tooltip";
    import { fade, scale } from "svelte/transition";

    let mounted = false;
    let showSendModal = false;
    let showReceiveModal = false;
    let selectedAsset = "AGE";
    let timeRange = "1M"; // 1D, 1W, 1M, 1Y
    let searchQuery = "";

    const ASSET_ICONS = {
        AGE: "⚛️",
        RES: "✨",
        USDC: "💵",
        BTC: "₿",
        ETH: "Ξ",
    };

    onMount(() => {
        mounted = true;
    });

    $: filteredTransactions = $vaultStore.transactions.filter((tx: any) => {
        if (!searchQuery) return true;
        return (
            tx.asset.toLowerCase().includes(searchQuery.toLowerCase()) ||
            tx.from?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            tx.to?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            tx.type.toLowerCase().includes(searchQuery.toLowerCase())
        );
    });

    $: totalValueFormatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 0,
    }).format($vaultStore.totalValue);

    $: selectedAssetPrice = $vaultStore?.assetPrices?.[selectedAsset] || 0;
    $: selectedAssetBalance = $vaultStore?.balances?.[selectedAsset] || 0;
    $: if (selectedAssetBalance && selectedAssetPrice) {
        // This is primarily for reactivity tracking
        const _v = selectedAssetBalance * selectedAssetPrice;
    }

    function handleSend(asset: string) {
        selectedAsset = asset;
        showSendModal = true;
    }

    function handleReceive(asset: string) {
        selectedAsset = asset;
        showReceiveModal = true;
    }
</script>

<svelte:head>
    <title>Vault · AGE Protocol</title>
</svelte:head>

<div class="vault-container">
    <!-- Header Section -->
    <div class="vault-header">
        <div class="greeting-section">
            <h1 class="glow-text">
                Sovereign <span class="accent">Vault</span>
            </h1>
            <p class="subtitle">
                Secure capital preservation and treasury orchestration
            </p>
        </div>

        <div class="header-actions">
            <button
                class="action-btn primary"
                on:click={() => (showReceiveModal = true)}
                use:tooltip={"Securely receive assets into your sovereign identity."}
            >
                <span>📥 Receive</span>
            </button>
            <button
                class="action-btn"
                on:click={() => (showSendModal = true)}
                use:tooltip={"Allocate capital to external or internal logic nodes."}
            >
                <span>📤 Send</span>
            </button>
        </div>
    </div>

    <!-- Primary Metrics Grid -->
    <div class="metrics-grid">
        <div
            use:tooltip={"Combined market value of all holdings across the Cathedral."}
        >
            <Tile
                title="Total Portfolio"
                value={totalValueFormatted}
                icon="💰"
                variant="primary"
                trend={$vaultStore.totalValueChange}
            />
        </div>

        <div use:tooltip={"Liquid capital available for immediate deployment."}>
            <Tile
                title="Available"
                value={"$" + ($vaultStore.totalValue * 0.8).toLocaleString()}
                icon="💧"
                variant="success"
                subtitle="80% Liquidity"
            />
        </div>

        <div
            use:tooltip={"Assets committed to network security and yield generation."}
        >
            <Tile
                title="Staked"
                value={"$" + ($vaultStore.totalValue * 0.2).toLocaleString()}
                icon="🔒"
                variant="info"
                subtitle="Earning ~12% APY"
            />
        </div>

        <div
            use:tooltip={"Net change in treasury value over the last 24 orbital hours."}
        >
            <Tile
                title="24h Delta"
                value="+$847.00"
                icon="📊"
                variant="warning"
                trend="+3.2%"
            />
        </div>
    </div>

    <!-- Main Content Area - Three Column Layout -->
    <div class="vault-main">
        <!-- Column 1: Assets & Allocation -->
        <div class="column">
            <div use:tooltip={"Detailed breakdown of your capital assets."}>
                <GlassCard title="Holdings" icon="💼" variant="primary">
                    <div class="assets-list">
                        {#each Object.entries($vaultStore.balances) as [asset, balance]}
                            <AssetCard
                                {asset}
                                {balance}
                                price={$vaultStore.assetPrices[asset]}
                                icon={ASSET_ICONS[asset] || "🪙"}
                                on:send={() => handleSend(asset)}
                                on:receive={() => handleReceive(asset)}
                            />
                        {/each}
                    </div>
                </GlassCard>
            </div>

            <div use:tooltip={"Geometric distribution of risks and yields."}>
                <GlassCard title="Allocation" icon="🥧" variant="info">
                    <AllocationChart allocation={$vaultStore.allocation} />
                </GlassCard>
            </div>
        </div>

        <!-- Column 2: Market Logic & Analytics -->
        <div class="column">
            <div
                use:tooltip={"Deep-mesh temporal analytics for selected assets."}
            >
                <GlassCard title="Market Manifold" icon="📈" variant="warning">
                    <div class="chart-controls">
                        <select class="asset-select" bind:value={selectedAsset}>
                            {#each Object.keys($vaultStore.assetPrices) as asset}
                                <option value={asset}>
                                    {asset} - {ASSET_ICONS[asset]}
                                </option>
                            {/each}
                        </select>
                        <div class="time-range">
                            {#each ["1D", "1W", "1M", "1Y"] as range}
                                <button
                                    class="range-button"
                                    class:active={timeRange === range}
                                    on:click={() => (timeRange = range)}
                                >
                                    {range}
                                </button>
                            {/each}
                        </div>
                    </div>

                    <div class="asset-focus">
                        <span class="focus-label">{selectedAsset} Focus</span>
                        <span class="focus-value">
                            {selectedAssetBalance.toFixed(4)}
                            {selectedAsset}
                            <span class="focus-usd"
                                >(${(
                                    selectedAssetBalance * selectedAssetPrice
                                ).toLocaleString()})</span
                            >
                        </span>
                    </div>

                    <PriceChart
                        data={$vaultStore.priceHistory?.[selectedAsset] || []}
                        color={selectedAsset === "AGE" ? "#4CAF50" : "#3498db"}
                    />
                </GlassCard>
            </div>

            <div
                use:tooltip={"Real-time vital signs of protocol-level capital formation."}
            >
                <CapitalFormationVitals />
            </div>
        </div>

        <!-- Column 3: Ledger & Forensics -->
        <div class="column">
            <div
                use:tooltip={"Immutably recorded movements within the manifold."}
            >
                <GlassCard title="Ledger Feed" icon="📋" variant="info">
                    <div class="search-bar">
                        <input
                            type="text"
                            placeholder="Scan ledger..."
                            bind:value={searchQuery}
                        />
                    </div>
                    <div class="tx-list-container">
                        <TransactionList transactions={filteredTransactions} />
                    </div>
                </GlassCard>
            </div>

            <div use:tooltip={"Forensic analysis of yield vectors."}>
                <ForensicYieldExplorer />
            </div>
        </div>
    </div>

    <!-- Quick Actions Bar -->
    <div use:tooltip={"Unified access for rapid treasury operations."}>
        <QuickActions />
    </div>

    <!-- Modals -->
    {#if showSendModal}
        <div
            class="modal-overlay"
            in:fade
            on:click={() => (showSendModal = false)}
        >
            <div class="modal-content" in:scale on:click|stopPropagation>
                <SendModal
                    asset={selectedAsset}
                    balance={selectedAssetBalance}
                    on:close={() => (showSendModal = false)}
                    on:send={(e) => {
                        vaultStore.addTransaction(e.detail);
                        showSendModal = false;
                    }}
                />
            </div>
        </div>
    {/if}

    {#if showReceiveModal}
        <div
            class="modal-overlay"
            in:fade
            on:click={() => (showReceiveModal = false)}
        >
            <div class="modal-content" in:scale on:click|stopPropagation>
                <ReceiveModal
                    asset={selectedAsset}
                    address={$sovereignStore?.did || "did:age:..."}
                    on:close={() => (showReceiveModal = false)}
                />
            </div>
        </div>
    {/if}
</div>

<style>
    .vault-container {
        padding: 2rem;
        max-width: 1700px;
        margin: 0 auto;
    }

    .vault-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        color: white;
    }

    .glow-text .accent {
        color: #4caf50;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin: 0.5rem 0 0;
    }

    .header-actions {
        display: flex;
        gap: 1rem;
    }

    .action-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
    }

    .action-btn.primary {
        background: linear-gradient(135deg, #4caf50, #45a049);
        border: none;
    }

    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .vault-main {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .column {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .assets-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .chart-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        gap: 1rem;
    }

    .asset-select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        cursor: pointer;
    }

    .time-range {
        display: flex;
        gap: 0.25rem;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.25rem;
        border-radius: 8px;
    }

    .range-button {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.2s;
    }

    .range-button.active {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .asset-focus {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(76, 175, 80, 0.05);
        border-radius: 12px;
        border-left: 3px solid #4caf50;
    }

    .focus-label {
        display: block;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .focus-value {
        font-size: 1.25rem;
        font-weight: bold;
        color: #4caf50;
    }

    .focus-usd {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin-left: 0.5rem;
    }

    .search-bar {
        margin-bottom: 1rem;
    }

    .search-bar input {
        width: 100%;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        font-size: 0.9rem;
    }

    .tx-list-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .tx-list-container::-webkit-scrollbar {
        width: 4px;
    }

    .tx-list-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
    }

    .modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    }

    .modal-content {
        width: 100%;
        max-width: 500px;
        max-height: 90vh;
        overflow-y: auto;
    }

    @media (max-width: 1400px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .vault-main {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 768px) {
        .vault-main {
            grid-template-columns: 1fr;
        }

        .vault-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1.5rem;
        }
    }
</style>
