<script lang="ts">
    import { goto } from "$app/navigation";

    const actions = [
        { name: "Send", path: "/send", icon: "📤", color: "#4CAF50" },
        { name: "Bridge", path: "/bridge", icon: "🌉", color: "#2196F3" },
        { name: "Stake", path: "/stake", icon: "📈", color: "#9C27B0" },
        { name: "Node", path: "/node", icon: "⚡", color: "#FF9800" },
    ];
</script>

<div class="quick-actions">
    {#each actions as action}
        <button
            class="action-button"
            style="--action-color: {action.color}"
            onclick={() => goto(action.path)}
        >
            <span class="action-icon">{action.icon}</span>
            <span class="action-name">{action.name}</span>
        </button>
    {/each}
</div>

<style>
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 2rem;
    }

    .action-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1.5rem;
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .action-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            120deg,
            transparent 30%,
            rgba(255, 255, 255, 0.05) 50%,
            transparent 70%
        );
        transition: left 0.6s;
    }

    .action-button:hover::before {
        left: 100%;
    }

    .action-button:hover {
        transform: translateY(-4px);
        border-color: var(--action-color);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }

    .action-icon {
        font-size: 2rem;
    }

    .action-name {
        font-size: 1rem;
        font-weight: 500;
    }

    @media (max-width: 768px) {
        .quick-actions {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
