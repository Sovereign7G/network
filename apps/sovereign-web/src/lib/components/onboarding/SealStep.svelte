<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";


    export let data;

    const dispatch = createEventDispatcher();

    let isSealing = false;
    let sealComplete = false;
    let acceptedTerms = false;
    let acceptedProtocol = false;

    let sealAnimation = "";

    const SEAL_PHRASES = [
        "Forging sovereign identity...",
        "Establishing resonance field...",
        "Securing cryptographic keys...",
        "Connecting to protocol mesh...",
        "Calibrating hearth frequency...",
    ];

    let currentPhraseIndex = 0;

    let generatedDID = "";
    onMount(() => {
        // Pre-calculate DID
        const timestamp = Date.now();
        const random = Math.floor(Math.random() * 1000000);
        generatedDID = `did:age:${timestamp}${random}`;
    });

    function handleSeal() {
        if (!acceptedTerms || !acceptedProtocol) return;

        isSealing = true;
        sealAnimation = "pulse";

        // Animate through seal phrases
        const interval = setInterval(() => {
            if (currentPhraseIndex < SEAL_PHRASES.length - 1) {
                currentPhraseIndex++;
            } else {
                clearInterval(interval);
                setTimeout(() => {
                    sealComplete = true;
                    sealAnimation = "complete";
                    setTimeout(() => {
                        dispatch("complete", {
                            ...data,

                            did: generatedDID,
                            verificationLevel: 1,
                            acceptedTerms,
                            acceptedProtocol,
                        });
                    }, 1500);
                }, 1000);
            }
        }, 800);
    }
</script>

<div class="seal-step">
    <div
        class="seal-container"
        class:sealing={isSealing}
        class:complete={sealComplete}
    >
        <!-- Animated seal ring -->
        <div class="seal-ring">
            <div class="seal-ring-inner"></div>
        </div>

        <!-- Central icon -->
        <div class="seal-icon">
            {#if sealComplete}
                <span class="complete-icon">✅</span>
            {:else if isSealing}
                <span class="sealing-icon">⚛️</span>
            {:else}
                <span class="default-icon">🔮</span>
            {/if}
        </div>

        <!-- Orbiting particles -->
        <div class="seal-particles">
            <div class="particle p1"></div>
            <div class="particle p2"></div>
            <div class="particle p3"></div>
        </div>
    </div>

    <div class="seal-content">
        <h2 class="seal-title">
            {#if sealComplete}
                Sovereign Identity Created
            {:else if isSealing}
                Sealing Your Identity
            {:else}
                Seal Your Sovereignty
            {/if}
        </h2>

        {#if !isSealing && !sealComplete}
            <div class="identity-summary">
                <div class="summary-item">
                    <span class="summary-label">Name</span>
                    <span class="summary-value">{data.displayName}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Handle</span>
                    <span class="summary-value">@{data.handle}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">DID</span>
                    <span class="summary-value did">{generatedDID}</span>
                </div>
                {#if data.interests.length > 0}
                    <div class="summary-item">
                        <span class="summary-label">Interests</span>
                        <span class="summary-value"
                            >{data.interests.join(" · ")}</span
                        >
                    </div>
                {/if}
            </div>

            <div class="verification-badge">
                <span class="badge-icon">🛡️</span>
                <div>
                    <strong>Verification Level 1</strong>
                    <p>Basic sovereign identity established</p>
                </div>
            </div>

            <div class="terms-section">
                <label class="terms-checkbox">
                    <input type="checkbox" bind:checked={acceptedTerms} />
                    <span>I accept the AGE Protocol Terms of Service</span>
                </label>

                <label class="terms-checkbox">
                    <input type="checkbox" bind:checked={acceptedProtocol} />
                    <span>I agree to participate in protocol governance</span>
                </label>
            </div>

            <div class="seal-actions">
                <button class="back-button" onclick={() => dispatch("back")}>
                    ← Back
                </button>
                <button
                    class="seal-button"
                    class:ready={acceptedTerms && acceptedProtocol}
                    onclick={handleSeal}
                    disabled={!acceptedTerms || !acceptedProtocol}
                >
                    <span class="button-text">Seal Identity</span>
                    <span class="button-icon">🔒</span>
                </button>
            </div>
        {/if}

        {#if isSealing && !sealComplete}
            <div class="sealing-status">
                <div class="status-phrase">
                    {SEAL_PHRASES[currentPhraseIndex]}
                </div>
                <div class="status-progress">
                    <div
                        class="progress-bar"
                        style="width: {((currentPhraseIndex + 1) /
                            SEAL_PHRASES.length) *
                            100}%"
                    ></div>
                </div>
            </div>
        {/if}

        {#if sealComplete}
            <div class="complete-message">
                <p>Your sovereign journey begins now.</p>
                <p class="small">Redirecting to your dashboard...</p>
            </div>
        {/if}
    </div>
</div>

<style>
    .seal-step {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
        color: white;
    }

    .seal-container {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }

    .seal-ring {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 2px solid transparent;
        border-radius: 50%;
        animation: rotate 10s linear infinite;
        border-top-color: #9370db;
        border-bottom-color: #ff6b6b;
    }

    .seal-ring-inner {
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        bottom: 10px;
        border: 2px solid transparent;
        border-radius: 50%;
        animation: rotate-reverse 8s linear infinite;
        border-left-color: #9370db;
        border-right-color: #ff6b6b;
    }

    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes rotate-reverse {
        from {
            transform: rotate(360deg);
        }
        to {
            transform: rotate(0deg);
        }
    }

    .seal-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 4rem;
        z-index: 2;
    }

    .sealing-icon {
        display: inline-block;
        animation: spin 1s linear infinite;
    }

    .seal-particles {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }

    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border-radius: 50%;
        filter: blur(2px);
    }

    .p1 {
        top: 20%;
        left: 20%;
        animation: orbit1 4s linear infinite;
    }

    .p2 {
        top: 70%;
        right: 20%;
        animation: orbit2 5s linear infinite;
    }

    .p3 {
        bottom: 20%;
        left: 50%;
        animation: orbit3 6s linear infinite;
    }

    @keyframes orbit1 {
        0% {
            transform: rotate(0deg) translateX(30px) rotate(0deg);
        }
        100% {
            transform: rotate(360deg) translateX(30px) rotate(-360deg);
        }
    }

    @keyframes orbit2 {
        0% {
            transform: rotate(120deg) translateX(40px) rotate(-120deg);
        }
        100% {
            transform: rotate(480deg) translateX(40px) rotate(-480deg);
        }
    }

    @keyframes orbit3 {
        0% {
            transform: rotate(240deg) translateX(35px) rotate(-240deg);
        }
        100% {
            transform: rotate(600deg) translateX(35px) rotate(-600deg);
        }
    }

    .seal-content {
        text-align: center;
        width: 100%;
        max-width: 500px;
    }

    .seal-title {
        font-size: 1.8rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .identity-summary {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        text-align: left;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .summary-item:last-child {
        border-bottom: none;
    }

    .summary-label {
        opacity: 0.6;
        font-size: 0.9rem;
    }

    .summary-value {
        font-weight: 500;
    }

    .summary-value.did {
        font-family: monospace;
        font-size: 0.8rem;
        color: #9370db;
    }

    .verification-badge {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.2);
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        text-align: left;
    }

    .badge-icon {
        font-size: 2rem;
    }

    .verification-badge p {
        margin: 0.25rem 0 0 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .terms-section {
        margin-bottom: 1.5rem;
    }

    .terms-checkbox {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        cursor: pointer;
    }

    .terms-checkbox input {
        width: 1.2rem;
        height: 1.2rem;
        cursor: pointer;
    }

    .seal-actions {
        display: flex;
        gap: 1rem;
    }

    .back-button {
        flex: 1;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: none;
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .back-button:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .seal-button {
        flex: 2;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        cursor: not-allowed;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        transition: all 0.2s;
        opacity: 0.5;
    }

    .seal-button.ready {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        cursor: pointer;
        opacity: 1;
    }

    .seal-button.ready:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }

    .sealing-status {
        margin-top: 2rem;
    }

    .status-phrase {
        margin-bottom: 1rem;
        font-size: 1.1rem;
        color: #9370db;
    }

    .status-progress {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #9370db, #ff6b6b);
        transition: width 0.3s;
    }

    .complete-message {
        margin-top: 2rem;
    }

    .complete-message p {
        margin: 0.5rem 0;
    }

    .complete-message .small {
        font-size: 0.9rem;
        opacity: 0.6;
    }
</style>
