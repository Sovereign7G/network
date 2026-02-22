<script lang="ts">
    export let percentage = 0;

    // Smooth transition
    $: fillStyle = `height: ${percentage}%; 
                    transition: height 0.3s ease-out;`;

    // Proportional glow intensity based on percentage
    $: glowIntensity = Math.min(percentage / 100, 1) * 0.8;
</script>

<div class="gauge-container" style="--glow-opacity: {glowIntensity}">
    <div class="gauge-background"></div>
    <div class="liquid-fill" style={fillStyle}>
        <div class="wave"></div>
        <div class="wave wave-secondary"></div>
    </div>
    <div class="gauge-value">{Math.round(percentage)}%</div>
</div>

<style>
    .gauge-container {
        position: relative;
        width: 100px;
        height: 200px;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(76, 175, 80, var(--glow-opacity));
        display: flex;
        align-items: flex-end;
    }

    .gauge-background {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            180deg,
            transparent,
            rgba(76, 175, 80, 0.1)
        );
    }

    .liquid-fill {
        position: relative;
        width: 100%;
        background: linear-gradient(180deg, #4caf50, #2e7d32);
        border-radius: 0 0 48px 48px;
        transition: height 300ms ease-out;
    }

    .wave {
        position: absolute;
        top: -15px;
        left: 0;
        width: 200%;
        height: 30px;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 10 Q25 20 50 10 T100 10 L100 20 L0 20 Z" fill="rgba(76, 175, 80, 0.8)"/></svg>')
            repeat-x;
        background-size: 50px 20px;
        animation: wave-move 2s linear infinite;
    }

    .wave-secondary {
        top: -10px;
        opacity: 0.5;
        animation: wave-move 3s linear infinite reverse;
    }

    .gauge-value {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        z-index: 10;
    }

    @keyframes wave-move {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50px);
        }
    }
</style>
