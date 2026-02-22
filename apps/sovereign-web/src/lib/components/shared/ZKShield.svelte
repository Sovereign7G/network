<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let isProtected = true;
    export let isVerifying = false;

    const dispatch = createEventDispatcher();

    function triggerVerification() {
        if (!isProtected || isVerifying) return;
        isVerifying = true;
        dispatch("verify");
        setTimeout(() => {
            isProtected = false;
            isVerifying = false;
        }, 800);
    }
</script>

<div
    class="zk-shield-wrapper"
    on:click={triggerVerification}
    role="button"
    tabindex="0"
>
    <div class="content" class:blurred={isProtected}>
        <slot></slot>
    </div>

    {#if isProtected}
        <div class="shield-overlay" class:verifying={isVerifying}>
            {#if isVerifying}
                <div class="pulse-indicator"></div>
            {:else}
                <span class="icon">🔒 ZK-Shielded</span>
            {/if}
        </div>
    {/if}
</div>

<style>
    .zk-shield-wrapper {
        position: relative;
        display: inline-block;
        cursor: pointer;
        border-radius: 8px;
        overflow: hidden;
    }

    .content {
        transition: filter 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    .blurred {
        filter: blur(25px);
        user-select: none;
        pointer-events: none;
    }

    .shield-overlay {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-family: inherit;
        backdrop-filter: blur(2px);
    }

    .shield-overlay.verifying {
        background: rgba(33, 150, 243, 0.2);
    }

    .pulse-indicator {
        width: 30px;
        height: 30px;
        border: 2px solid #2196f3;
        border-radius: 50%;
        animation: verify-pulse 0.8s infinite;
    }

    @keyframes verify-pulse {
        0% {
            transform: scale(0.5);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
</style>
