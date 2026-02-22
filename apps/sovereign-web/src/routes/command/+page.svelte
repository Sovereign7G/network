<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    let command = "";
    let output: string[] = [];

    const commands = [
        { cmd: "help", desc: "Show available commands" },
        { cmd: "dashboard", desc: "Go to dashboard" },
        { cmd: "vault", desc: "Open vault" },
        { cmd: "hearth", desc: "View memories" },
        { cmd: "council", desc: "Governance" },
        { cmd: "atlas", desc: "Open map" },
        { cmd: "send", desc: "Send transaction" },
        { cmd: "stake", desc: "Stake assets" },
        { cmd: "clear", desc: "Clear terminal" },
    ];

    function execute() {
        const trimmed = command.trim().toLowerCase();

        if (trimmed === "clear") {
            output = [];
            command = "";
            return;
        }

        if (trimmed === "help") {
            output.push("> Available commands:");
            commands.forEach((c) =>
                output.push(`  ${c.cmd.padEnd(12)} - ${c.desc}`),
            );
            command = "";
            return;
        }

        if (trimmed === "dashboard") {
            goto("/dashboard");
            return;
        }

        if (trimmed === "vault") {
            goto("/vault");
            return;
        }

        if (trimmed === "hearth") {
            goto("/hearth");
            return;
        }

        if (trimmed === "council") {
            goto("/council");
            return;
        }

        if (trimmed === "atlas") {
            goto("/atlas");
            return;
        }

        if (trimmed === "send") {
            goto("/send");
            return;
        }

        if (trimmed === "stake") {
            goto("/stake");
            return;
        }

        output.push(`> Unknown command: ${trimmed}. Type 'help' for options.`);
        command = "";
    }

    function handleKeyDown(e: KeyboardEvent) {
        if (e.key === "Enter") {
            execute();
        }
    }
</script>

<div class="command-portal">
    <h1 class="glow-text">Command Portal</h1>
    <p class="subtitle">Direct interface to the Cathedral</p>

    <div class="terminal">
        <div class="terminal-output">
            {#each output as line}
                <div class="terminal-line">{line}</div>
            {/each}
        </div>

        <div class="terminal-input-line">
            <span class="prompt">$</span>
            <input
                type="text"
                bind:value={command}
                on:keydown={handleKeyDown}
                class="terminal-input"
                placeholder="Type 'help' for commands..."
                autofocus
            />
        </div>
    </div>

    <div class="quick-commands">
        <h3>Quick Commands</h3>
        <div class="command-grid">
            {#each commands.filter((c) => c.cmd !== "help" && c.cmd !== "clear") as cmd}
                <button
                    class="command-chip"
                    on:click={() => goto(`/${cmd.cmd}`)}
                >
                    {cmd.cmd}
                </button>
            {/each}
        </div>
    </div>
</div>

<style>
    .command-portal {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
    }

    .glow-text {
        font-size: 2.5rem;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 2rem;
    }

    .terminal {
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        font-family: monospace;
        margin-bottom: 2rem;
    }

    .terminal-output {
        min-height: 200px;
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 1rem;
        color: #4caf50;
    }

    .terminal-line {
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(76, 175, 80, 0.1);
    }

    .terminal-input-line {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-top: 1px solid rgba(76, 175, 80, 0.3);
        padding-top: 1rem;
    }

    .prompt {
        color: #4caf50;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .terminal-input {
        flex: 1;
        background: transparent;
        border: none;
        color: white;
        font-family: monospace;
        font-size: 1rem;
        outline: none;
    }

    .quick-commands h3 {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }

    .command-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 0.5rem;
    }

    .command-chip {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s ease;
        text-transform: capitalize;
    }

    .command-chip:hover {
        background: rgba(76, 175, 80, 0.2);
        border-color: #4caf50;
        transform: translateY(-2px);
    }
</style>
