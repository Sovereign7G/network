<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { goto } from "$app/navigation";

    let { open = $bindable(false) } = $props();

    let input = $state("");
    let selectedIndex = $state(0);

    let results = $derived.by(() => {
        if (input.startsWith("/")) {
            return commands["/"].filter((cmd) =>
                cmd.name.toLowerCase().includes(input.slice(1).toLowerCase()),
            );
        } else if (input.startsWith("@")) {
            return commands["@"].filter((cmd) =>
                cmd.name.toLowerCase().includes(input.slice(1).toLowerCase()),
            );
        }
        return [];
    });

    const commands = {
        "/": [
            { name: "Dashboard", command: "/dashboard", icon: "🏛️" },
            { name: "Vault", command: "/vault", icon: "💰" },
            { name: "Hearth", command: "/hearth", icon: "🔥" },
            { name: "Council", command: "/council", icon: "⚖️" },
            { name: "Atlas", command: "/atlas", icon: "🗺️" },
            { name: "Node", command: "/node", icon: "⚡" },
            { name: "Bridge", command: "/bridge", icon: "🌉" },
        ],
        "@": [
            { name: "Current Citizen", command: "@me", icon: "👤" },
            { name: "Treasury", command: "@treasury", icon: "🏦" },
            { name: "Council", command: "@council", icon: "⚖️" },
        ],
    };

    function handleKeydownGlobal(e: KeyboardEvent) {
        if ((e.metaKey || e.ctrlKey) && e.key === "k") {
            e.preventDefault();
            open = true;
        }
    }

    function handleCustomCommandOpen(e: CustomEvent) {
        open = true;
        if (e.detail && e.detail.prompt) {
            input = e.detail.prompt;
        }
    }

    onMount(() => {
        window.addEventListener("keydown", handleKeydownGlobal);
        document.addEventListener(
            "command:open",
            handleCustomCommandOpen as EventListener,
        );
    });

    onDestroy(() => {
        window.removeEventListener("keydown", handleKeydownGlobal);
        document.removeEventListener(
            "command:open",
            handleCustomCommandOpen as EventListener,
        );
    });

    function executeCommand(cmd: any) {
        if (cmd.command.startsWith("/")) {
            goto(cmd.command);
        } else if (cmd.command.startsWith("@")) {
            // Handle mentions
        }
        open = false;
        input = "";
    }

    function handleInputKeydown(e: KeyboardEvent) {
        if (e.key === "ArrowDown") {
            e.preventDefault();
            selectedIndex = (selectedIndex + 1) % (results.length || 1);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            selectedIndex =
                (selectedIndex - 1 + (results.length || 1)) %
                (results.length || 1);
        } else if (e.key === "Enter") {
            e.preventDefault();
            if (results[selectedIndex]) {
                executeCommand(results[selectedIndex]);
            }
        } else if (e.key === "Escape") {
            open = false;
            input = "";
        }
    }
</script>

{#if open}
    <div
        class="command-overlay"
        role="presentation"
        onclick={() => (open = false)}
        onkeydown={(e: KeyboardEvent) => e.key === "Escape" && (open = false)}
        tabindex="-1"
    >
        <div
            class="command-palette"
            role="dialog"
            aria-modal="true"
            aria-label="Command Palette"
            onclick={(e: MouseEvent) => e.stopPropagation()}
            onkeydown={(e: KeyboardEvent) => e.stopPropagation()}
            tabindex="0"
        >
            <div class="command-input-area">
                <span class="prompt">⌘</span>
                <input
                    bind:value={input}
                    onkeydown={handleInputKeydown}
                    placeholder="Type '/' for commands, '@' to mention..."
                    class="command-input"
                    aria-label="Search commands"
                />
            </div>

            {#if results.length > 0}
                <div class="command-results" role="listbox">
                    {#each results as result, i}
                        <button
                            class="result-item {i === selectedIndex
                                ? 'selected'
                                : ''}"
                            role="option"
                            aria-selected={i === selectedIndex}
                            onclick={() => executeCommand(result)}
                            onkeydown={(e: KeyboardEvent) =>
                                e.key === "Enter" && executeCommand(result)}
                        >
                            <span class="result-icon">{result.icon}</span>
                            <span class="result-name">{result.name}</span>
                            <span class="result-command">{result.command}</span>
                        </button>
                    {/each}
                </div>
            {:else if input}
                <div class="no-results" role="status">
                    <span>No commands found</span>
                </div>
            {/if}

            <div class="command-footer">
                <span>↑↓ navigate</span>
                <span>↵ select</span>
                <span>esc close</span>
            </div>
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
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
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
        max-height: 300px;
        overflow-y: auto;
    }

    .result-item {
        display: flex;
        align-items: center;
        width: 100%;
        background: transparent;
        border: none;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        font-family: inherit;
    }

    .result-item:hover,
    .result-item.selected {
        background: rgba(255, 215, 0, 0.1);
    }

    .result-icon {
        font-size: 1.2rem;
    }

    .result-name {
        flex: 1;
        color: white;
    }

    .result-command {
        color: rgba(255, 255, 255, 0.3);
        font-family: monospace;
    }

    .no-results {
        padding: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.3);
    }

    .command-footer {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 0.75rem;
        border-top: 1px solid rgba(255, 215, 0, 0.2);
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.8rem;
    }
</style>
