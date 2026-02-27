<script lang="ts">
    import { onMount } from "svelte";
    import GlassCard from "$lib/components/ui/GlassCard.svelte";

    let terminalOutput = $state([
        { type: "system", text: "AGE PROTOCOL KERNEL v0.92.4-STABLE" },
        { type: "system", text: "INITIALIZING NEURAL COMMAND MANIFOLD..." },
        { type: "system", text: "IDENTITY VERIFIED: did:age:0x7a2...f33" },
        { type: "system", text: 'TYPE "help" FOR AVAILABLE COMMANDS' },
        { type: "system", text: "" },
    ]);

    let currentInput = $state("");
    let terminalContainer: HTMLElement;
    let inputElement: HTMLInputElement;

    $effect(() => {
        if (inputElement) {
            inputElement.focus();
        }
    });

    function handleCommand(e: KeyboardEvent) {
        if (e.key === "Enter" && currentInput.trim()) {
            const input = currentInput.trim();
            terminalOutput = [
                ...terminalOutput,
                { type: "input", text: `> ${input}` },
            ];

            processCommand(input.toLowerCase());
            currentInput = "";
        }
    }

    function processCommand(cmd: string) {
        let response = "";
        switch (cmd) {
            case "help":
                response =
                    "AVAILABLE COMMANDS: status, vault, hearth, sync, clear, exit";
                break;
            case "status":
                response =
                    "SYSTEM STATUS: NOMINAL. ALL NODES RESPONDING. COHERENCE AT 98.4%.";
                break;
            case "clear":
                terminalOutput = [];
                return;
            case "vault":
                response =
                    "ACCESSING VAULT... CURRENT BALANCE: 7247.32 AGE. USE /dashboard/vault FOR FULL UI.";
                break;
            default:
                response = `COMMAND NOT RECOGNIZED: ${cmd}. TYPE "help" FOR ASSISTANCE.`;
        }

        terminalOutput = [
            ...terminalOutput,
            { type: "response", text: response },
        ];
    }

    $effect(() => {
        // terminalOutput is a state variable (implicitly or explicitly)
        // Whenever it changes, scroll to bottom
        if (terminalContainer && terminalOutput) {
            terminalContainer.scrollTop = terminalContainer.scrollHeight;
        }
    });

    onMount(() => {
        if (terminalContainer) {
            terminalContainer.scrollTop = terminalContainer.scrollHeight;
        }
    });
</script>

<svelte:head>
    <title>Command · AGE Protocol</title>
</svelte:head>

<div class="command-container">
    <header class="command-header">
        <h1 class="glow-text">Neural <span class="accent">Terminal</span></h1>
        <p class="subtitle">
            Direct kernel-level interface for protocol execution
        </p>
    </header>

    <div class="terminal-wrapper">
        <GlassCard title="Kernel Interface" icon="⌨️" variant="warning">
            <div class="terminal-body" bind:this={terminalContainer}>
                {#each terminalOutput as line}
                    <div class="line {line.type}">
                        {line.text}
                    </div>
                {/each}
                <div class="input-line">
                    <span class="prompt">></span>
                    <input
                        bind:this={inputElement}
                        type="text"
                        bind:value={currentInput}
                        onkeydown={handleCommand}
                        placeholder="..."
                    />
                </div>
            </div>
        </GlassCard>
    </div>
</div>

<style>
    .command-container {
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }

    .terminal-wrapper {
        height: 600px;
    }

    .command-header {
        margin-bottom: 2rem;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        color: white;
    }

    .glow-text .accent {
        color: #ffaa00;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0.5rem;
    }

    .terminal-wrapper {
        height: 600px;
    }

    .terminal-body {
        height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        font-family: "JetBrains Mono", "Fira Code", "Menlo", monospace;
        font-size: 0.95rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
    }

    .line.system {
        color: rgba(255, 255, 255, 0.4);
        font-style: italic;
    }

    .line.input {
        color: #ffaa00;
        font-weight: bold;
    }

    .line.response {
        color: #4caf50;
        padding-left: 1rem;
        border-left: 2px solid rgba(76, 175, 80, 0.3);
    }

    .input-line {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    .prompt {
        color: #ffaa00;
        font-weight: bold;
    }

    input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        outline: none;
        font-family: inherit;
        font-size: inherit;
    }

    .terminal-body::-webkit-scrollbar {
        width: 6px;
    }

    .terminal-body::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
    }
</style>
