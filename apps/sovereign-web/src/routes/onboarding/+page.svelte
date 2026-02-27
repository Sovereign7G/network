<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import {
        onboardingStore,
        ONBOARDING_STEPS,
    } from "$lib/stores/onboarding-store.svelte";
    import { sovereignStore } from "$lib/stores/master-store";
    import WelcomeStep from "$lib/components/onboarding/WelcomeStep.svelte";
    import IdentityStep from "$lib/components/onboarding/IdentityStep.svelte";
    import SealStep from "$lib/components/onboarding/SealStep.svelte";
    import { fade, fly, scale } from "svelte/transition";

    let mounted = false;
    let particles = [];

    onMount(() => {
        mounted = true;

        // Generate floating particles for ambiance
        for (let i = 0; i < 50; i++) {
            particles.push({
                id: i,
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 3 + 1,
                delay: Math.random() * 5,
                duration: Math.random() * 10 + 10,
            });
        }

        // Check if already onboarded
        const sovereign = localStorage.getItem("sovereign");
        if (sovereign) {
            try {
                const data = JSON.parse(sovereign);
                if (data.id) {
                    goto("/dashboard");
                }
            } catch (e) {
                console.error("Failed to parse sovereign data:", e);
            }
        }
    });

    function handleComplete(event) {
        const sovereignData = event.detail;
        console.log(
            "🎉 Onboarding complete! Creating sovereign:",
            sovereignData,
        );

        // Initialize sovereign identity
        const state = {
            id: `did:age:${Date.now()}`,
            did: `did:age:${Date.now()}`,
            handle:
                sovereignData.handle ||
                sovereignData.displayName.toLowerCase().replace(/\s+/g, "_"),
            profile: {
                displayName: sovereignData.displayName,
                avatar: sovereignData.avatar,
                bio: sovereignData.bio || "",
                location: null,
            },
            verificationLevel: sovereignData.verificationLevel || 1,
            createdAt: new Date().toISOString(),
        };

        sovereignStore.initialize(state);

        // 🏛️ SOVEREIGN BRIDGE: Register on backend
        sovereignStore.registerIdentity(state).catch((err) => {
            console.error(
                "⚠️ Backend identity registration failed (offline mode):",
                err,
            );
        });

        // Mark onboarding as complete
        onboardingStore.completeOnboarding();

        // Navigate to dashboard
        setTimeout(() => {
            goto("/dashboard");
        }, 1500);
    }
</script>

<svelte:head>
    <title>Become Sovereign · AGE Protocol</title>
</svelte:head>

<!-- Ambient particle background -->
<div class="onboarding-ambient">
    {#each particles as particle}
        <div
            class="particle"
            style="
        left: {particle.x}%;
        top: {particle.y}%;
        width: {particle.size}px;
        height: {particle.size}px;
        animation-delay: {particle.delay}s;
        animation-duration: {particle.duration}s;
      "
        ></div>
    {/each}
</div>

<!-- Main onboarding container -->
<div class="onboarding-container">
    <!-- Progress bar -->
    <div class="onboarding-progress" in:fade>
        <div class="progress-bar">
            <div
                class="progress-fill"
                style="width: {onboardingStore.state.progress}%"
                in:fade
            ></div>
        </div>
        <div class="progress-steps">
            {#each Object.values(ONBOARDING_STEPS) as step, index}
                <div
                    class="progress-step"
                    class:active={onboardingStore.state.currentStep === step}
                    class:completed={Object.values(ONBOARDING_STEPS).indexOf(
                        onboardingStore.state.currentStep,
                    ) > index}
                >
                    <span class="step-dot"></span>
                    <span class="step-label"
                        >{step.charAt(0).toUpperCase() + step.slice(1)}</span
                    >
                </div>
            {/each}
        </div>
    </div>

    <!-- Step content with transitions -->
    <div class="onboarding-content">
        {#if onboardingStore.state.currentStep === ONBOARDING_STEPS.WELCOME}
            <div
                in:fly={{ y: 20, duration: 500 }}
                out:fly={{ y: -20, duration: 300 }}
            >
                <WelcomeStep onnext={() => onboardingStore.nextStep()} />
            </div>
        {/if}

        {#if onboardingStore.state.currentStep === ONBOARDING_STEPS.IDENTITY}
            <div
                in:fly={{ y: 20, duration: 500 }}
                out:fly={{ y: -20, duration: 300 }}
            >
                <IdentityStep
                    data={onboardingStore.state.data}
                    onnext={(data) => {
                        onboardingStore.updateData(data.detail);
                        onboardingStore.nextStep();
                    }}
                    onback={() => onboardingStore.previousStep()}
                />
            </div>
        {/if}

        {#if onboardingStore.state.currentStep === ONBOARDING_STEPS.SEAL}
            <div in:scale={{ duration: 500 }} out:scale={{ duration: 300 }}>
                <SealStep
                    data={onboardingStore.state.data}
                    oncomplete={handleComplete}
                    onback={() => onboardingStore.previousStep()}
                />
            </div>
        {/if}
    </div>

    <!-- Decorative elements -->
    <div class="onboarding-decoration">
        <div class="decoration-circle circle1"></div>
        <div class="decoration-circle circle2"></div>
        <div class="decoration-line"></div>
    </div>
</div>

<style>
    .onboarding-ambient {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    .particle {
        position: absolute;
        background: rgba(147, 112, 219, 0.3);
        border-radius: 50%;
        pointer-events: none;
        animation: float linear infinite;
    }

    @keyframes float {
        0% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 0.5;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            transform: translateY(-100vh) translateX(20px);
            opacity: 0;
        }
    }

    .onboarding-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        position: relative;
        z-index: 1;
        background: radial-gradient(
                circle at 20% 30%,
                rgba(147, 112, 219, 0.15),
                transparent 40%
            ),
            radial-gradient(
                circle at 80% 70%,
                rgba(255, 107, 107, 0.1),
                transparent 40%
            ),
            #0a0a0a;
    }

    .onboarding-progress {
        width: 100%;
        max-width: 600px;
        margin-bottom: 3rem;
    }

    .progress-bar {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
        margin-bottom: 1rem;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #9370db, #ff6b6b);
        transition: width 0.5s;
        border-radius: 2px;
    }

    .progress-steps {
        display: flex;
        justify-content: space-between;
    }

    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        opacity: 0.5;
        transition: all 0.3s;
    }

    .progress-step.active {
        opacity: 1;
    }

    .progress-step.completed {
        opacity: 0.8;
    }

    .progress-step.completed .step-dot {
        background: #4caf50;
        border-color: #4caf50;
    }

    .step-dot {
        width: 12px;
        height: 12px;
        border: 2px solid #9370db;
        border-radius: 50%;
        background: transparent;
        transition: all 0.3s;
    }

    .progress-step.active .step-dot {
        background: #9370db;
        box-shadow: 0 0 20px #9370db;
        transform: scale(1.2);
    }

    .step-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
    }

    .onboarding-content {
        width: 100%;
        max-width: 600px;
        min-height: 400px;
        display: flex;
        justify-content: center;
    }

    .onboarding-decoration {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: -1;
    }

    .decoration-circle {
        position: absolute;
        border-radius: 50%;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        filter: blur(60px);
        opacity: 0.1;
    }

    .circle1 {
        width: 300px;
        height: 300px;
        top: 10%;
        left: 5%;
    }

    .circle2 {
        width: 400px;
        height: 400px;
        bottom: 10%;
        right: 5%;
        background: linear-gradient(135deg, #ff6b6b, #9370db);
    }

    .decoration-line {
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(147, 112, 219, 0.3),
            transparent
        );
        transform: rotate(10deg);
    }

    @media (max-width: 768px) {
        .onboarding-container {
            padding: 1rem;
        }

        .step-label {
            font-size: 0.6rem;
        }
    }
</style>
