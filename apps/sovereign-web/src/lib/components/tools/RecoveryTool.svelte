<script lang="ts">
    let guardians = ["0xGuardian1...", "0xGuardian2..."];
    let newGuardian = "";
    let gracePeriodDays = 7;

    function addGuardian() {
        if (newGuardian) {
            guardians = [...guardians, newGuardian];
            newGuardian = "";
        }
    }

    function saveConfig() {
        alert("Social Recovery configuration saved.");
    }
</script>

<div class="recovery-tool">
    <div class="header-info">
        <p>Configure Social Recovery guardians to protect against key loss.</p>
    </div>

    <div class="guardians-list">
        <label>Trusted Guardians</label>
        {#each guardians as guardian, i}
            <div class="guardian-item">
                <span>{guardian}</span>
                <button
                    class="remove-btn"
                    on:click={() =>
                        (guardians = guardians.filter((_, idx) => idx !== i))}
                    >×</button
                >
            </div>
        {/each}
        <div class="add-row">
            <input type="text" bind:value={newGuardian} placeholder="0x..." />
            <button class="add-btn" on:click={addGuardian}>Add</button>
        </div>
    </div>

    <div class="input-group">
        <label>Grace Period (Before execution)</label>
        <div class="days-row">
            <input
                type="number"
                bind:value={gracePeriodDays}
                min="1"
                max="30"
            />
            <span>Days</span>
        </div>
    </div>

    <button class="save-btn" on:click={saveConfig}>
        Update Recovery Protocols
    </button>
</div>

<style>
    .recovery-tool {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .header-info p {
        margin: 0;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
    }

    .guardians-list label,
    .input-group label {
        display: block;
        font-size: 0.75rem;
        color: rgba(255, 215, 0, 0.7);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .guardian-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0.75rem;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-family: monospace;
        font-size: 0.9rem;
    }

    .remove-btn {
        background: none;
        border: none;
        color: #ff5252;
        cursor: pointer;
        font-size: 1.2rem;
    }

    .add-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    input {
        flex: 1;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 8px;
        color: white;
        box-sizing: border-box;
    }

    .add-btn {
        padding: 0 1rem;
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 8px;
        color: #ffd700;
        cursor: pointer;
    }

    .days-row {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .days-row input {
        width: 100px;
        flex: none;
    }

    .days-row span {
        color: rgba(255, 255, 255, 0.6);
    }

    .save-btn {
        padding: 1rem;
        background: #ffd700;
        border: none;
        border-radius: 8px;
        color: #0a0a0f;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
    }

    .save-btn:hover {
        background: #fff;
        transform: translateY(-2px);
    }
</style>
