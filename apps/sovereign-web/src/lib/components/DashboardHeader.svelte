<script lang="ts">
    import { onMount } from "svelte";

    export let resonanceScore = 0;
    export let lastUpdated = "";

    let currentTime = new Date().toLocaleTimeString();

    let mounted = false;

    onMount(() => {
        mounted = true;
        const interval = setInterval(() => {
            currentTime = new Date().toLocaleTimeString();
        }, 1000);

        return () => clearInterval(interval);
    });

    // Animate resonance changes
    $: animatedResonance = resonanceScore;
</script>

<header class="dashboard-header">
    <div class="header-content">
        <div class="header-left">
            <div class="logo-section">
                <h1 class="logo">
                    <span class="logo-icon">⚛️</span>
                    <span class="logo-text">AGE Protocol</span>
                </h1>
                <span class="version-badge">v0.1.0</span>
            </div>

            <nav class="header-nav">
                <a href="/dashboard" class="nav-link active">Dashboard</a>
                <a href="/atlas" class="nav-link">Atlas</a>
                <a href="/protocols" class="nav-link">Protocols</a>
            </nav>
        </div>

        <div class="header-right">
            <div class="resonance-display">
                <span class="resonance-icon">✨</span>
                <div class="resonance-info">
                    <span class="resonance-label">Resonance</span>
                    <span class="resonance-value">{animatedResonance}</span>
                </div>
            </div>

            <div class="system-time">
                <span class="time-icon">⏰</span>
                <span class="time-value">{currentTime}</span>
            </div>

            <div class="user-menu">
                <button class="user-avatar" aria-label="User menu">
                    <span class="avatar-initials">SID</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Status bar -->
    <div class="status-bar">
        <div class="status-item">
            <span class="status-dot online"></span>
            <span>Connected</span>
        </div>
        <div class="status-item">
            <span class="status-label">Last sync:</span>
            <span
                >{lastUpdated
                    ? new Date(lastUpdated).toLocaleTimeString()
                    : "Just now"}</span
            >
        </div>
        <div class="status-item">
            <span class="status-label">Network:</span>
            <span>Mainnet</span>
        </div>
    </div>
</header>

<style>
    .dashboard-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        font-size: 1.5rem;
    }

    .logo-icon {
        font-size: 2rem;
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

    .logo-text {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    .version-badge {
        padding: 0.25rem 0.5rem;
        background: rgba(147, 112, 219, 0.2);
        border: 1px solid rgba(147, 112, 219, 0.3);
        border-radius: 1rem;
        font-size: 0.7rem;
        color: #9370db;
    }

    .header-nav {
        display: flex;
        gap: 0.5rem;
    }

    .nav-link {
        padding: 0.5rem 1rem;
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        border-radius: 2rem;
        transition: all 0.2s;
    }

    .nav-link:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .nav-link.active {
        background: rgba(147, 112, 219, 0.2);
        color: #9370db;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }

    .resonance-display {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(147, 112, 219, 0.1);
        border: 1px solid rgba(147, 112, 219, 0.2);
        border-radius: 2rem;
    }

    .resonance-icon {
        font-size: 1.2rem;
        animation: sparkle 2s infinite;
    }

    @keyframes sparkle {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.7;
            transform: scale(1.1);
        }
    }

    .resonance-info {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }

    .resonance-label {
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .resonance-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: #9370db;
    }

    .system-time {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 2rem;
    }

    .time-icon {
        opacity: 0.5;
    }

    .time-value {
        font-family: monospace;
        font-size: 0.9rem;
    }

    .user-avatar {
        width: 2.5rem;
        height: 2.5rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 50%;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .user-avatar:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.4);
    }

    .status-bar {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0.5rem 2rem;
        display: flex;
        gap: 2rem;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.02);
        background: rgba(0, 0, 0, 0.2);
    }

    .status-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        opacity: 0.7;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }

    .status-dot.online {
        background: #4caf50;
        box-shadow: 0 0 10px #4caf50;
        animation: pulse 2s infinite;
    }

    .status-label {
        opacity: 0.5;
    }

    @media (max-width: 1024px) {
        .header-left {
            gap: 1rem;
        }

        .header-nav {
            display: none;
        }
    }

    @media (max-width: 768px) {
        .header-content {
            padding: 1rem;
        }

        .resonance-label,
        .status-bar {
            display: none;
        }

        .logo-text {
            font-size: 1rem;
        }
    }
</style>
