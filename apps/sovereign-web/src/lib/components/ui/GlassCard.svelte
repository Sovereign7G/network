<script lang="ts">
    export let title: string = "";
    export let icon: string = "";
    export let variant: "default" | "primary" | "success" | "info" | "warning" =
        "default";

    const variantClasses = {
        default: "border-white/10",
        primary: "border-primary/30",
        success: "border-success/30",
        info: "border-info/30",
        warning: "border-warning/30",
    };
</script>

<div class="glass-card {variantClasses[variant]}">
    {#if title || icon}
        <div class="card-header">
            {#if icon}<span class="card-icon">{icon}</span>{/if}
            {#if title}<h3 class="card-title">{title}</h3>{/if}
        </div>
    {/if}

    <div class="card-content">
        <slot />
    </div>
</div>

<style>
    .glass-card {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid;
        border-radius: 24px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            120deg,
            transparent 30%,
            rgba(255, 255, 255, 0.03) 50%,
            transparent 70%
        );
        transition: left 0.6s;
        pointer-events: none;
    }

    .glass-card:hover::before {
        left: 100%;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(76, 175, 80, 0.15);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .card-icon {
        font-size: 1.5rem;
    }

    .card-title {
        margin: 0;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 500;
    }

    .card-content {
        color: rgba(255, 255, 255, 0.8);
    }
</style>
