<script lang="ts">
    let fromValue = 1;
    let fromUnit = "USD";
    let toUnit = "AGE";
    let result = 0;

    const units = ["USD", "AGE", "SYND", "EUR", "BTC", "ETH"];
    const rates: Record<string, number> = {
        USD: 1,
        AGE: 2.5,
        SYND: 1.8,
        EUR: 0.92,
        BTC: 0.00002,
        ETH: 0.0003,
    };

    $: result = fromValue * (rates[toUnit] / rates[fromUnit]);
</script>

<div class="converter-tool">
    <h3>Quick Converter</h3>
    <div class="converter-row">
        <input type="number" bind:value={fromValue} />
        <select bind:value={fromUnit}>
            {#each units as unit}
                <option value={unit}>{unit}</option>
            {/each}
        </select>
    </div>
    <div class="converter-row">
        <input type="number" bind:value={result} readonly />
        <select bind:value={toUnit}>
            {#each units as unit}
                <option value={unit}>{unit}</option>
            {/each}
        </select>
    </div>
</div>

<style>
    .converter-tool {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    h3 {
        margin: 0;
        color: white;
    }

    .converter-row {
        display: flex;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }

    input,
    select {
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 8px;
        color: white;
        box-sizing: border-box;
    }

    input {
        flex: 2;
    }

    select {
        flex: 1;
    }
</style>
