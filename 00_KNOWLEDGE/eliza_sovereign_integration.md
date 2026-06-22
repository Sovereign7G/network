# 🏛️ AGE REPUBLIC :: ELIZAOS & SOVEREIGN MESH INTEGRATION GUIDE
*Bridging the TypeScript Agentic OS with the Python Sovereign Swarm*

---

## 🗺️ Architectural Concept
To achieve full coordination between our **ElizaOS TypeScript agent** (handling public-facing social channels, Discord, and Telegram) and our **Python Sovereign Swarm** (handling local execution, SMSPool telephony, and memory persistence), we run a bi-directional gateway bridge:

```
┌─────────────────────────────────┐                 ┌─────────────────────────────────┐
│     ElizaOS Agent (TS)          │                 │     Sovereign Swarm (Python)    │
│  - Character: HermesGTME        │   API Webhooks  │  - Roles: hermes_gtme_architect │
│  - Handles Twitter/Discord/TG   ├────────────────►│  - Handles SQLite DB & RAG      │
│  - Decoupled transaction signs  │◄────────────────┤  - Manages SMSPool virtual SIMs │
└─────────────────────────────────┘                 └─────────────────────────────────┘
```

---

## ⚙️ Step 1: Deploying the ElizaOS Agent
1. Ensure you have Node.js (v24+) and Bun installed.
2. Initialize or navigate to your ElizaOS project directory:
   ```bash
   bun add -g elizaos
   elizaos create my-sovereign-agent --template project
   cd my-sovereign-agent
   ```
3. Copy the Hermes GTME character file into the project:
   ```bash
   cp "/media/fiji/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE/hermes_gtme.character.json" ./characters/
   ```
4. Configure your `.env` keys (OpenAI, Anthropic, or OpenRouter for the LLM inference, and Twitter developer credentials if posting).
5. Start the agent:
   ```bash
   bun run dev --character ./characters/hermes_gtme.character.json
   ```

---

## 🔗 Step 2: Custom Bridge Actions (TypeScript)
To link ElizaOS directly to our local Python CLI, add a custom action in your ElizaOS project (e.g., `src/actions/sovereignBridge.ts`) to trigger local workflow executions:

```typescript
import { Action, IAgentRuntime, Memory, State } from "@elizaos/core";
import { exec } from "child_process";

export const sovereignBridgeAction: Action = {
    name: "TRIGGER_SOVEREIGN_WORKFLOW",
    description: "Forward complex strategy requests to the local python workflow engine",
    similes: ["QUERY_SOVEREIGN_MESH", "RUN_GTME_AUDIT"],
    validate: async (runtime: IAgentRuntime, message: Memory) => {
        return !!message.content.text;
    },
    handler: async (runtime: IAgentRuntime, message: Memory, state: State) => {
        const promptText = message.content.text.replace(/"/g, '\\"');
        const cmd = `/media/fiji/4A21-00001/New\\ folder/AGE\\ REPUBLIC/sovereign agent --workflow geo_gtme_alignment --workflow-param target_description="${promptText}"`;
        
        exec(cmd, (error, stdout, stderr) => {
            if (error) {
                console.error(`Sovereign mesh bridge error: ${error}`);
                return;
            }
            // Parse final report and respond to user channel
            console.log(`Sovereign execution: ${stdout}`);
        });
        return true;
    },
    examples: [
        [
            {
                user: "{{user1}}",
                content: { text: "Can you audit our new product launch on the mesh?" }
            },
            {
                user: "HermesGTME",
                content: { text: "Triggering sovereign alignment workflow..." }
            }
        ]
    ]
};
```

---

## 🏛️ Step 3: Triggering Outbound Telephony & Ledger Actions
When the ElizaOS agent receives a payload requiring carrier verification or DeFi settlement, it delegates to the Python scripts:
*   **Carrier burner request:** `./sovereign services start local-router` -> executes local SMSPool allocation.
*   **SIP Cryptographic Attestation:** `./sovereign agent --attest --role hermes_judgment_moat_auditor --prompt "..."` to anchor responses securely to the local AMD SEV-SNP TPM 2.0.
