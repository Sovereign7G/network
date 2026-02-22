<script lang="ts">
    export let title: string = "";
    export let value: string | number = "";
    export let icon: string = "";
    export let variant: "primary" | "success" | "info" | "warning" | "danger" =
        "primary";
    export let trend: string = "";
    export let subtitle: string = "";

    const colors = {
        primary: "#4CAF50",
        success: "#81C784",
        info: "#3498DB",
        warning: "#F1C40F",
        danger: "#E74C3C",
    };
</script>

<div class="premium-tile boarder-{variant}">
    <div class="tile-header">
        <div
            class="tile-icon-container"
            style="background: {colors[variant]}20; color: {colors[variant]}"
        >
            <span class="tile-icon">{icon}</span>
        </div>
        {#if trend}
            <span class="tile-trend {trend.startsWith('+') ? 'up' : 'down'}"
                >{trend}</span
            >
        {/if}
    </div>

    <div class="tile-body">
        <span class="tile-title">{title}</span>
        <h2 class="tile-value">{value}</h2>
        {#if subtitle}
            <span class="tile-subtitle">{subtitle}</span>
        {/if}
    </div>
</div>

<style>
    .premium-tile {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        position: relative;
        overflow: hidden;
    }

    .tile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .tile-icon-container {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .tile-trend {
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
    }

    .tile-trend.up {
        color: #4caf50;
        background: rgba(76, 175, 80, 0.1);
    }

    .tile-trend.down {
        color: #e74c3c;
        background: rgba(231, 76, 60, 0.1);
    }

    .tile-body {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .tile-title {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .tile-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }

    .tile-subtitle {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
    }
</style>
