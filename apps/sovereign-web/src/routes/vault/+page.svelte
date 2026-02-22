<script lang="ts">
    import { onMount } from "svelte";

    // Mocking the vault store if not properly imported
    import { writable } from "svelte/store";
    const vaultStore = writable({ balance: 1845920.0 });

    // Kintsugi marks - permanent scars from recovered failures
    let kintsugiMarks = [];

    onMount(() => {
        // We handle localStorage in onMount so it safely runs on the client.
        try {
            kintsugiMarks = JSON.parse(
                localStorage.getItem("kintsugi") || "[]",
            );
            if (kintsugiMarks.length === 0) {
                // Add some mock kintsugi marks so the UI can be showcased immediately:
                addKintsugiMark("Failed Bridge Recovery");
                addKintsugiMark("Node Desync Correction");
            }
        } catch (e) {}
    });

    function addKintsugiMark(eventType: string) {
        kintsugiMarks = [
            ...kintsugiMarks,
            {
                id: Date.now() + Math.random(),
                type: eventType,
                date: new Date().toISOString(),
                gold: true,
            },
        ];
        try {
            localStorage.setItem("kintsugi", JSON.stringify(kintsugiMarks));
        } catch (e) {}
    }

    // Massive typography for wealth
    $: wealthFormatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format($vaultStore?.balance || 0);
</script>

<div class="vault-cathedral">
    <!-- Massive Wealth Display -->
    <div class="wealth-altar">
        <span class="wealth-label">Sovereign Treasury</span>
        <div class="wealth-number">{wealthFormatted}</div>
        <div class="wealth-trend">
            <span class="trend-up">↑ 12.4%</span>
            <span class="trend-period">last 30 days</span>
        </div>
    </div>

    <!-- Kintsugi Marks - Gold-repaired failures -->
    {#if kintsugiMarks.length > 0}
        <div class="kintsugi-section">
            <h3>Recovered Transactions</h3>
            <div class="kintsugi-grid">
                {#each kintsugiMarks as mark}
                    <div class="kintsugi-card" style="border-color: #FFD700">
                        <span class="kintsugi-icon">🔨</span>
                        <div class="kintsugi-details">
                            <span class="kintsugi-type">{mark.type}</span>
                            <span class="kintsugi-date"
                                >{new Date(
                                    mark.date,
                                ).toLocaleDateString()}</span
                            >
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .vault-cathedral {
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
        color: white;
    }

    .wealth-altar {
        text-align: center;
        padding: 6rem 2rem;
        background: linear-gradient(
            180deg,
            rgba(255, 215, 0, 0.1),
            transparent
        );
        border-radius: 48px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 215, 0, 0.1);
    }

    .wealth-label {
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 0.9rem;
    }

    .wealth-number {
        font-size: clamp(4rem, 8vw, 8rem);
        font-weight: 300;
        letter-spacing: -0.03em;
        line-height: 1;
        margin: 1.5rem 0;
        background: linear-gradient(135deg, #ffd700, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .wealth-trend {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 100px;
    }

    .trend-up {
        color: #4caf50;
        font-weight: bold;
    }

    .kintsugi-section {
        margin-top: 4rem;
    }

    .kintsugi-section h3 {
        color: rgba(255, 215, 0, 0.8);
        font-weight: 300;
        letter-spacing: 1px;
        margin-bottom: 1.5rem;
    }

    .kintsugi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
    }

    .kintsugi-card {
        border: 2px solid;
        border-radius: 16px;
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }

    .kintsugi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.1);
    }

    .kintsugi-icon {
        font-size: 1.5rem;
    }

    .kintsugi-details {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .kintsugi-type {
        font-weight: 500;
    }

    .kintsugi-date {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
    }
</style>
