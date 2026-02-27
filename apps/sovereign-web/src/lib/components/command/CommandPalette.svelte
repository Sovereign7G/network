<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { fly, fade } from "svelte/transition";
    import { quintOut } from "svelte/easing";
    import { goto } from "$app/navigation";

    export let open = false;

    const dispatch = createEventDispatcher();

    let searchTerm = "";
    let selectedIndex = 0;
    let commandInput: HTMLInputElement;
    let commands = [
        {
            name: "Dashboard",
            action: "/dashboard",
            icon: "🏛️",
            keywords: "home main",
        },
        {
            name: "Vault",
            action: "/dashboard/vault",
            icon: "💰",
            keywords: "wallet balance money",
        },
        {
            name: "Hearth",
            action: "/dashboard/hearth",
            icon: "🔥",
            keywords: "memories log history",
        },
        {
            name: "Council",
            action: "/dashboard/governance",
            icon: "⚖️",
            keywords: "governance vote proposals",
        },
        {
            name: "Atlas",
            action: "/atlas",
            icon: "🗺️",
            keywords: "map navigation",
        },
        {
            name: "Command",
            action: "command",
            icon: "⌨️",
            keywords: "terminal cli",
        },
        {
            name: "Onboarding",
            action: "/onboarding",
            icon: "🚀",
            keywords: "start new citizen",
        },
        {
            name: "Settings",
            action: "/settings",
            icon: "⚙️",
            keywords: "preferences config",
        },
        {
            name: "Profile",
            action: "/profile",
            icon: "👤",
            keywords: "identity citizen",
        },
        {
            name: "Staking",
            action: "/dashboard/wallet",
            icon: "📈",
            keywords: "stake yield earn",
        },
    ];

    // Filter commands based on search
    let filteredCommands = $derived.by(() => {
        const term = searchTerm.trim().toLowerCase();
        if (term === "") return commands;
        return commands.filter(
            (cmd) =>
                cmd.name.toLowerCase().includes(term) ||
                cmd.keywords?.toLowerCase().includes(term),
        );
    });

    // Reset selected index when filter changes
    $effect(() => {
        if (filteredCommands.length > 0) {
            selectedIndex = Math.min(
                selectedIndex,
                filteredCommands.length - 1,
            );
        } else {
            selectedIndex = 0;
        }
    });

    onMount(() => {
        // Keyboard shortcuts
        const handleKeyDown = (e: KeyboardEvent) => {
            // Cmd+K or Ctrl+K to open
            if ((e.metaKey || e.ctrlKey) && e.key === "k") {
                e.preventDefault();
                open = !open;
                if (open) {
                    setTimeout(() => commandInput?.focus(), 100);
                }
            }

            // Escape to close
            if (e.key === "Escape" && open) {
                closePalette();
            }

            // Arrow navigation when open
            if (open) {
                if (e.key === "ArrowDown") {
                    e.preventDefault();
                    if (filteredCommands.length > 0) {
                        selectedIndex =
                            (selectedIndex + 1) % filteredCommands.length;
                    }
                } else if (e.key === "ArrowUp") {
                    e.preventDefault();
                    if (filteredCommands.length > 0) {
                        selectedIndex =
                            selectedIndex > 0
                                ? selectedIndex - 1
                                : filteredCommands.length - 1;
                    }
                } else if (e.key === "Enter" && filteredCommands.length > 0) {
                    e.preventDefault();
                    executeCommand(filteredCommands[selectedIndex]);
                }
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    });

    function closePalette() {
        open = false;
        searchTerm = "";
        selectedIndex = 0;
        if (onclose) onclose();
    }

    function executeCommand(cmd: (typeof commands)[0]) {
        if (cmd.action.startsWith("/")) {
            goto(cmd.action);
        } else if (cmd.action === "command") {
            // Toggle command palette (already open)
        } else {
            // Execute custom action
        }
        closePalette();
    }
</script>

{#if open}
    <div
        class="command-overlay"
        onclick={closePalette}
        transitionfade={{ duration: 150 }}
    >
        <div
            class="command-palette"
            onclick={(e) => e.stopPropagation()}
            transitionfly={{ y: -20, duration: 200, easing: quintOut }}
        >
            <div class="command-header">
                <span class="command-icon">⌘</span>
                <input
                    bind:this={commandInput}
                    type="text"
                    bind:value={searchTerm}
                    placeholder="Search commands or type /..."
                    class="command-input"
                    autofocus
                />
            </div>

            <div class="command-results">
                {#if filteredCommands.length === 0}
                    <div class="no-results">
                        <span class="no-results-icon">🔍</span>
                        <span>No commands found</span>
                    </div>
                {:else}
                    {#each filteredCommands as cmd, index (cmd.name)}
                        <div
                            class="command-item {index === selectedIndex
                                ? 'selected'
                                : ''}"
                            onclick={() => executeCommand(cmd)}
                            onmouseenter={() => (selectedIndex = index)}
                        >
                            <span class="command-item-icon">{cmd.icon}</span>
                            <span class="command-item-name">{cmd.name}</span>
                            <span class="command-item-shortcut">
                                {#if cmd.name === "Command"}
                                    <span class="shortcut-key">⌘K</span>
                                {/if}
                            </span>
                        </div>
                    {/each}
                {/if}
            </div>

            <div class="command-footer">
                <span>↑↓ to navigate</span>
                <span>↵ to select</span>
                <span>esc to close</span>
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
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: flex-start;
        justify-content: center;
        z-index: 9999;
        padding-top: 15vh;
    }

    .command-palette {
        width: 600px;
        max-width: 90vw;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(76, 175, 80, 0.2);
        overflow: hidden;
    }

    .command-header {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .command-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        color: #4caf50;
    }

    .command-input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 1.1rem;
        outline: none;
    }

    .command-input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }

    .command-results {
        max-height: 400px;
        overflow-y: auto;
        padding: 0.5rem;
    }

    .command-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 0.25rem;
    }

    .command-item:hover,
    .command-item.selected {
        background: rgba(76, 175, 80, 0.2);
        transform: translateX(4px);
    }

    .command-item.selected {
        border-left: 3px solid #4caf50;
    }

    .command-item-icon {
        font-size: 1.2rem;
        margin-right: 1rem;
        width: 24px;
        text-align: center;
    }

    .command-item-name {
        flex: 1;
        color: white;
    }

    .command-item-shortcut {
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.8rem;
    }

    .shortcut-key {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }

    .no-results {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        color: rgba(255, 255, 255, 0.5);
        gap: 1rem;
    }

    .no-results-icon {
        font-size: 3rem;
    }

    .command-footer {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.8rem;
    }
</style>
