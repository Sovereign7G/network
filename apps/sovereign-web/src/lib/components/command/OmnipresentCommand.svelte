<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { writable } from "svelte/store";

    const vaultStore = writable({ balance: 1845920.0 });

    export let open = false;

    let input = "";
    let results = [];
    let selectedIndex = 0;

    onMount(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "k") {
                e.preventDefault();
                open = !open;
            }
            if (e.key === "Escape" && open) open = false;
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    });

    $: parseInput(input);

    function parseInput(val: string) {
        if (!val.trim()) {
            results = [];
            return;
        }

        // Natural language parsing
        const sendMatch = val.match(
            /send (\d+(?:\.\d+)?) (usdc|age|synd) to (.+)/i,
        );
        if (sendMatch) {
            results = [
                {
                    type: "send",
                    amount: sendMatch[1],
                    asset: sendMatch[2].toUpperCase(),
                    recipient: sendMatch[3],
                    confidence: 0.95,
                    action: () =>
                        executeSend(sendMatch[1], sendMatch[2], sendMatch[3]),
                },
            ];
            return;
        }

        const bridgeMatch = val.match(
            /bridge (\d+(?:\.\d+)?) (usdc|age|synd) from (\w+) to (\w+)/i,
        );
        if (bridgeMatch) {
            results = [
                {
                    type: "bridge",
                    amount: bridgeMatch[1],
                    asset: bridgeMatch[2].toUpperCase(),
                    from: bridgeMatch[3],
                    to: bridgeMatch[4],
                    confidence: 0.9,
                    action: () => {
                        open = false;
                        goto(
                            `/bridge?from=${bridgeMatch[3]}&to=${bridgeMatch[4]}&amount=${bridgeMatch[1]}`,
                        );
                    },
                },
            ];
            return;
        }

        // Navigation
        if (
            val.match(
                /^(go to|open|navigate to) (vault|dashboard|hearth|council|atlas)$/i,
            )
        ) {
            const page = val
                .match(/(vault|dashboard|hearth|council|atlas)/i)[0]
                .toLowerCase();
            results = [
                {
                    type: "navigate",
                    destination: page,
                    confidence: 0.98,
                    action: () => {
                        open = false;
                        goto(`/${page}`);
                    },
                },
            ];
            return;
        }

        // Default fast filter
        results = [
            {
                type: "navigate",
                destination: "dashboard",
                confidence: 0.5,
                action: () => {
                    open = false;
                    goto("/dashboard");
                },
            },
            {
                type: "navigate",
                destination: "vault",
                confidence: 0.5,
                action: () => {
                    open = false;
                    goto("/vault");
                },
            },
        ].filter((r) => r.destination.includes(val.toLowerCase()));
    }

    function executeSend(amount, asset, recipient) {
        // Auto-resolve address, check balance, show inline confirmation
        alert(`Mock Send: Sent ${amount} ${asset} to ${recipient}`);
        open = false;
    }
</script>

{#if open}
    <div class="command-overlay" onclick={() => (open = false)}>
        <div class="command-palette" onclick={(e) => e.stopPropagation()}>
            <div class="command-input-area">
                <span class="prompt">⌘</span>
                <input
                    autofocus
                    bind:value={input}
                    placeholder="Ask anything... 'send 500 USDC to @treasury'"
                    class="command-input"
                />
            </div>

            {#if results.length > 0}
                <div class="command-results">
                    {#each results as result, i}
                        <div
                            class="result-item {i === selectedIndex
                                ? 'selected'
                                : ''}"
                            onclick={result.action}
                        >
                            <span class="result-type">{result.type}</span>
                            <span class="result-desc">
                                {#if result.type === "send"}
                                    Send {result.amount}
                                    {result.asset} to {result.recipient}
                                {:else if result.type === "bridge"}
                                    Bridge {result.amount}
                                    {result.asset} from {result.from} to {result.to}
                                {:else if result.type === "navigate"}
                                    Go to {result.destination}
                                {/if}
                            </span>
                            <span class="result-confidence"
                                >{Math.round(result.confidence * 100)}%</span
                            >
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
{/if}

<style>
    .command-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(40px);
        display: flex;
        align-items: flex-start;
        justify-content: center;
        z-index: 9999;
        padding-top: 20vh;
    }

    .command-palette {
        width: 600px;
        max-width: 90vw;
        background: rgba(20, 20, 30, 0.9);
        border: 1px solid #ffd700;
        border-radius: 24px;
        overflow: hidden;
    }

    .command-input-area {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .prompt {
        font-size: 1.5rem;
        color: #ffd700;
    }

    .command-input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 1.2rem;
        outline: none;
    }

    .command-input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }

    .command-results {
        padding: 0.5rem;
    }

    .result-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .result-item:hover,
    .result-item.selected {
        background: rgba(255, 215, 0, 0.1);
        transform: translateX(4px);
    }

    .result-type {
        padding: 0.25rem 0.5rem;
        background: rgba(255, 215, 0, 0.2);
        border-radius: 4px;
        color: #ffd700;
        font-size: 0.7rem;
        text-transform: uppercase;
    }

    .result-desc {
        flex: 1;
        color: white;
    }

    .result-confidence {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
    }
</style>
