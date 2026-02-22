<script lang="ts">
    let input = "";
    let result = "";

    function calculate() {
        try {
            // Basic math wrapper
            result = new Function(`return ${input}`)().toString();
        } catch {
            result = "Error";
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === "Enter") {
            calculate();
        }
    }
</script>

<div class="calculator-tool">
    <h3>Quick Calculator</h3>
    <input
        type="text"
        bind:value={input}
        placeholder="Enter expression (e.g., 2+2)..."
        on:keydown={handleKeydown}
    />
    <button on:click={calculate}>=</button>
    {#if result}
        <div class="result">Result: {result}</div>
    {/if}
</div>

<style>
    .calculator-tool {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    h3 {
        margin: 0;
        color: white;
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

    button {
        padding: 0.75rem;
        background: #ffd700;
        border: none;
        border-radius: 8px;
        color: #0a0a0f;
        font-weight: bold;
        cursor: pointer;
    }

    .result {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 8px;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
    }
</style>
