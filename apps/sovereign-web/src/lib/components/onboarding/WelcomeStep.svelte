<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";

    const dispatch = createEventDispatcher();

    let isTyping = false;
    let displayText = "";
    const fullText =
        "You are about to become a Sovereign Citizen of the AGE Protocol.";

    onMount(() => {
        isTyping = true;
        let i = 0;
        const interval = setInterval(() => {
            if (i < fullText.length) {
                displayText = fullText.slice(0, i + 1);
                i++;
            } else {
                clearInterval(interval);
                isTyping = false;
            }
        }, 50);

        return () => clearInterval(interval);
    });

    const FEATURES = [
        {
            icon: "🔥",
            title: "Hearth",
            description: "Your memory log. Every entry builds resonance.",
        },
        {
            icon: "💰",
            title: "Vault",
            description: "Secure asset management across chains.",
        },
        {
            icon: "⚖️",
            title: "Council",
            description: "Participate in protocol governance.",
        },
        {
            icon: "🧘",
            title: "Wellbeing",
            description: "Track your somatic and energetic state.",
        },
    ];
</script>

<div class="welcome-step">
    <div class="welcome-header">
        <h1 class="welcome-title">
            <span class="title-icon">⚛️</span>
            <span class="title-text">AGE Protocol</span>
        </h1>
        <div class="title-underline"></div>
    </div>

    <div class="welcome-message">
        <p class="typing-text">{displayText}</p>
        {#if !isTyping}
            <span class="cursor">_</span>
        {/if}
    </div>

    <div class="features-grid">
        {#each FEATURES as feature, index}
            <div
                class="feature-card"
                style="animation-delay: {index * 0.1}s"
                in:fly={{ y: 20, duration: 500, delay: index * 100 }}
            >
                <span class="feature-icon">{feature.icon}</span>
                <div>
                    <h3 class="feature-title">{feature.title}</h3>
                    <p class="feature-description">{feature.description}</p>
                </div>
            </div>
        {/each}
    </div>

    <div class="resonance-intro">
        <div class="resonance-badge">
            <span class="badge-icon">✨</span>
            <span class="badge-text">Resonance</span>
        </div>
        <p class="resonance-description">
            Your resonance score grows with every meaningful action. It's the
            measure of your sovereign journey.
        </p>
    </div>

    <div class="welcome-actions">
        <button
            class="begin-button"
            onclick={() => dispatch("next")}
            disabled={isTyping}
        >
            <span class="button-text">Begin the Journey</span>
            <span class="button-icon">→</span>
        </button>

        <p class="terms-note">
            By continuing, you agree to the
            <a href="/protocols" class="terms-link">Protocol Terms</a>
        </p>
    </div>
</div>

<style>
    .welcome-step {
        width: 100%;
        animation: fadeIn 0.5s;
        color: white;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .welcome-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .welcome-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .title-icon {
        font-size: 3rem;
        animation: spin 10s linear infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .title-text {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .title-underline {
        width: 100px;
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent,
            #9370db,
            #ff6b6b,
            transparent
        );
        margin: 0 auto;
    }

    .welcome-message {
        min-height: 80px;
        margin-bottom: 2rem;
        text-align: center;
        font-size: 1.2rem;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.9);
    }

    .typing-text {
        display: inline;
        margin: 0;
    }

    .cursor {
        display: inline-block;
        width: 2px;
        height: 1.2rem;
        background: #9370db;
        margin-left: 2px;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%,
        50% {
            opacity: 1;
        }
        51%,
        100% {
            opacity: 0;
        }
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .feature-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        transition: all 0.3s;
        animation: slideUp 0.5s forwards;
        opacity: 0;
        transform: translateY(20px);
    }

    @keyframes slideUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .feature-card:hover {
        background: rgba(147, 112, 219, 0.1);
        border-color: #9370db;
        transform: translateY(-2px);
    }

    .feature-icon {
        font-size: 2rem;
    }

    .feature-title {
        margin: 0 0 0.25rem 0;
        font-size: 1rem;
    }

    .feature-description {
        margin: 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .resonance-intro {
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid rgba(147, 112, 219, 0.2);
        border-radius: 1rem;
        text-align: center;
    }

    .resonance-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2rem;
        margin-bottom: 0.5rem;
    }

    .badge-icon {
        font-size: 1.2rem;
    }

    .badge-text {
        font-weight: 600;
        color: #9370db;
    }

    .resonance-description {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .welcome-actions {
        text-align: center;
    }

    .begin-button {
        display: inline-flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 3rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 3rem;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        margin-bottom: 1rem;
    }

    .begin-button:hover:not(:disabled) {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 10px 30px -5px #9370db;
    }

    .begin-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .button-icon {
        transition: transform 0.3s;
    }

    .begin-button:hover .button-icon {
        transform: translateX(5px);
    }

    .terms-note {
        font-size: 0.8rem;
        opacity: 0.5;
    }

    .terms-link {
        color: #9370db;
        text-decoration: none;
    }

    .terms-link:hover {
        text-decoration: underline;
    }

    @media (max-width: 768px) {
        .features-grid {
            grid-template-columns: 1fr;
        }

        .welcome-title {
            font-size: 2rem;
        }

        .welcome-message {
            font-size: 1rem;
        }
    }
</style>
