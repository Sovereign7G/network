<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { llmService, PROVIDER_CONFIGS } from "$lib/services/llm-service";
    import type { LLMProvider } from "$lib/services/llm-service";

    const dispatch = createEventDispatcher();

    let config = llmService.getConfig();
    let provider = config.provider;
    let apiKey = config.apiKey;
    let model = config.model;
    let temperature = config.temperature;
    let maxTokens = config.maxTokens;
    let streaming = config.streaming;

    let showApiKey = false;
    let isTesting = false;
    let testResult: { success: boolean; message: string } | null = null;

    $: availableModels = PROVIDER_CONFIGS[provider]?.models || [];
    $: providerInfo = PROVIDER_CONFIGS[provider];

    async function handleSave() {
        llmService.updateConfig({
            provider,
            apiKey,
            model,
            temperature,
            maxTokens,
            streaming,
        });
        dispatch("saved");
    }

    async function testConnection() {
        isTesting = true;
        testResult = null;

        // Temporarily update config for test
        const originalConfig = llmService.getConfig();
        llmService.updateConfig({
            provider,
            apiKey,
            model,
            temperature,
            maxTokens,
            streaming: false,
        });

        testResult = await llmService.testConnection();

        // Restore original config
        llmService.updateConfig(originalConfig);
        isTesting = false;
    }
</script>

<div class="llm-config-modal">
    <div class="modal-header">
        <h2 class="modal-title">
            <span class="title-icon">⚙️</span>
            Configure AI Provider
        </h2>
        <button class="close-btn" on:click={() => dispatch("close")}>✕</button>
    </div>

    <div class="modal-body">
        <div class="config-section">
            <label class="config-label">Provider</label>
            <div class="provider-grid">
                {#each Object.entries(PROVIDER_CONFIGS) as [id, info]}
                    <button
                        class="provider-card"
                        class:active={provider === id}
                        on:click={() => {
                            provider = id as LLMProvider;
                            model = info.defaultModel;
                        }}
                    >
                        <span class="provider-icon">{info.icon}</span>
                        <span class="provider-name">{info.name}</span>
                    </button>
                {/each}
            </div>
        </div>

        <div class="config-section">
            <label class="config-label">API Key</label>
            <div class="api-key-input">
                <input
                    type={showApiKey ? "text" : "password"}
                    class="config-input"
                    bind:value={apiKey}
                    placeholder={provider === "local"
                        ? "Not needed for local"
                        : "sk-..."}
                    disabled={provider === "local"}
                />
                {#if provider !== "local"}
                    <button
                        class="toggle-visibility"
                        on:click={() => (showApiKey = !showApiKey)}
                    >
                        {showApiKey ? "👁️" : "👁️🗨️"}
                    </button>
                {/if}
            </div>
            <p class="input-hint">
                {provider === "local"
                    ? "Local models run through Ollama on http://localhost:11434"
                    : "Your API key is stored locally and never sent to our servers"}
            </p>
        </div>

        <div class="config-section">
            <label class="config-label">Model</label>
            <select class="config-select" bind:value={model}>
                {#each availableModels as m}
                    <option value={m}>{m}</option>
                {/each}
            </select>
        </div>

        <div class="config-section">
            <label class="config-label">
                Temperature: {temperature.toFixed(1)}
                <span class="setting-hint">(0 = precise, 1 = creative)</span>
            </label>
            <input
                type="range"
                class="config-slider"
                bind:value={temperature}
                min="0"
                max="1"
                step="0.1"
            />
        </div>

        <div class="config-section">
            <label class="config-label">
                Max Tokens: {maxTokens}
                <span class="setting-hint">(max response length)</span>
            </label>
            <input
                type="range"
                class="config-slider"
                bind:value={maxTokens}
                min="100"
                max={providerInfo.maxTokens}
                step="100"
            />
        </div>

        <div class="config-section">
            <label class="checkbox-label">
                <input type="checkbox" bind:checked={streaming} />
                <span
                    >Enable streaming responses (real-time token-by-token)</span
                >
            </label>
        </div>

        <div class="config-section">
            <button
                class="test-button"
                on:click={testConnection}
                disabled={isTesting || (provider !== "local" && !apiKey)}
            >
                {#if isTesting}
                    <span class="spinner"></span>
                    Testing...
                {:else}
                    Test Connection
                {/if}
            </button>

            {#if testResult}
                <div
                    class="test-result"
                    class:success={testResult.success}
                    class:error={!testResult.success}
                >
                    {#if testResult.success}
                        <span class="result-icon">✅</span>
                        <span>{testResult.message}</span>
                    {:else}
                        <span class="result-icon">❌</span>
                        <span>{testResult.message}</span>
                    {/if}
                </div>
            {/if}
        </div>

        <div class="modal-actions">
            <button class="cancel-btn" on:click={() => dispatch("close")}>
                Cancel
            </button>
            <button class="save-btn" on:click={handleSave}>
                Save Configuration
            </button>
        </div>
    </div>
</div>

<style>
    .llm-config-modal {
        background: #1a1a1a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        overflow: hidden;
        max-width: 500px;
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

    .close-btn {
        width: 2rem;
        height: 2rem;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        font-size: 1.2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .modal-body {
        padding: 1.5rem;
        max-height: 70vh;
        overflow-y: auto;
    }

    .config-section {
        margin-bottom: 1.5rem;
    }

    .config-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .setting-hint {
        margin-left: 0.5rem;
        font-size: 0.7rem;
        opacity: 0.5;
    }

    .provider-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }

    .provider-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .provider-card:hover {
        background: rgba(147, 112, 219, 0.1);
        border-color: #9370db;
        transform: translateY(-2px);
    }

    .provider-card.active {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
    }

    .provider-icon {
        font-size: 2rem;
    }

    .provider-name {
        font-size: 0.8rem;
    }

    .api-key-input {
        display: flex;
        gap: 0.5rem;
    }

    .config-input,
    .config-select {
        flex: 1;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: monospace;
    }

    .config-input:focus,
    .config-select:focus {
        outline: none;
        border-color: #9370db;
    }

    .config-input:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .toggle-visibility {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
    }

    .toggle-visibility:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .input-hint {
        margin: 0.25rem 0 0 0;
        font-size: 0.7rem;
        opacity: 0.5;
    }

    .config-slider {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        -webkit-appearance: none;
    }

    .config-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 1rem;
        height: 1rem;
        background: #9370db;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.2s;
    }

    .config-slider::-webkit-slider-thumb:hover {
        transform: scale(1.2);
        box-shadow: 0 0 20px #9370db;
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }

    .checkbox-label input {
        width: 1rem;
        height: 1rem;
        cursor: pointer;
    }

    .test-button {
        width: 100%;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        transition: all 0.2s;
    }

    .test-button:hover:not(:disabled) {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .test-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .spinner {
        width: 1rem;
        height: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .test-result {
        margin-top: 0.5rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .test-result.success {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid #4caf50;
        color: #4caf50;
    }

    .test-result.error {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        color: #ff6b6b;
    }

    .result-icon {
        font-size: 1.1rem;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }

    .cancel-btn,
    .save-btn {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .cancel-btn {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .cancel-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .save-btn {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
    }

    .save-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }
</style>
