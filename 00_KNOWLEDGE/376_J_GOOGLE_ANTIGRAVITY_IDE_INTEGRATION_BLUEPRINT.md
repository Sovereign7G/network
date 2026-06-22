# 🚀 [376J] Google Antigravity IDE — x402 & Nevermined Integration Blueprint
## AGE REPUBLIC: KNOWLEDGE SUBSTRATE [376-J]
**Status:** VISIONARY & IMPLEMENTABLE | ERA 216.0 DEVELOPMENT ARCHITECTURE  
**Subject:** Sovereign Developer Environment Integration for x402 / Nevermined Execution  
**Classification:** Development Environment, Tooling, and Agent Orchestration Blueprint  

---

## Preamble: The Tooling Stratum

| Stratum | Substrates | Function |
| :--- | :--- | :--- |
| **Grounding** | 376-A through 376-F | Technical deployment, formal proofs, enterprise billing |
| **Correction** | 376-G | Twelve overlooked edge-case dimensions (human exceptions, regulatory, legal) |
| **Transcendence** | 376-H | Seven vectors that reframe agents from payment consumers to economic citizens |
| **Safety** | 376-I | Secure LLM Integration, Budget Caps, and Attack Resilience |
| **Tooling** | **376-J (this document)** | Antigravity IDE Integration, Custom MCP Servers, and Tool Chains |

The grounding layer answers: *How do agents pay?*  
The correction layer answers: *What breaks when they do?*  
The transcendence layer answers: *What becomes possible when payment itself is redefined?*  
The safety layer answers: *How do we ensure autonomous agents remain secure, safe, and aligned?*  
The tooling layer answers: **How do we build, debug, and orchestrate these economic agents within a native, agent-first developer environment?**

---

## 🛠️ Part 1: Understanding Google Antigravity — The Agent-First IDE

### 1.1 Core Architecture
Antigravity is Google's agent-first integrated development environment, released as a full fork of VS Code. Unlike traditional IDEs that treat AI as a sidebar autocomplete assistant, Antigravity treats the AI agent as a first-class developer within a unified workspace. It integrates three primary subsystems:

*   **Agent Manager:** The mission control for task tracking, parallel multi-agent planning, and execution review.
*   **Editor View:** The standard VS Code compatible text editor, optimized for inline refactoring and model-assisted navigation.
*   **Integrated Browser:** An embedded testing environment allowing local API endpoints and payment interfaces to be visually verified in real time.

### 1.2 Pricing, Quotas, and Model Selection (2026 Status)

| Plan | Price | Quota Limits (Reported) | Target Use Case |
| :--- | :--- | :--- | :--- |
| **Free / Preview** | $0 | Very limited / Rate-capped | Initial testing & sandboxing |
| **AI Pro** | $20/month | ~9M input tokens/week (down from 300M) | Casual development & inline coding |
| **AI Ultra** | $250/month | High-volume, prioritized queue | Production-grade multi-agent swarms |

#### Supported Models:
*   **Gemini 3.1 Pro (High/Low options):** High-context window model optimized for planning and orchestration.
*   **Gemini 3 Flash:** Low-latency model for rapid inline checks and terminal command reasoning.
*   **Anthropic Claude Sonnet 4.6 / Opus 4.6:** Supported natively via IDE extensions (allowing high-complexity code generation).
*   **OpenAI GPT-OSS 120B:** Open-weights baseline model for standardized code conversion.

### 🔌 1.3 Model Context Protocol (MCP) Support
Antigravity natively implements the Model Context Protocol (MCP), enabling LLM agents to safely and dynamically call external services, databases, version control networks, and payment bridges.

---

## 🔌 Part 2: The Integration Architecture — Antigravity + x402 + Nevermined

### 2.1 Technical Integration Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GOOGLE ANTIGRAVITY IDE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Agent Manager│  │  Editor View │  │  Integrated  │  │     MCP      │    │
│  │ (Orchestrate)│  │  (Write Code)│  │   Browser    │  │   Servers    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │                 │            │
│         └─────────────────┼─────────────────┼─────────────────┘            │
│                           │                 │                              │
│  ┌────────────────────────┼─────────────────┼────────────────────────┐    │
│  │              LLM Backend (Gemini / Claude via Extensions)          │    │
│  └────────────────────────┼─────────────────┼────────────────────────┘    │
└────────────────────────────┼─────────────────┼────────────────────────────┘
                             │                 │
                             ▼                 ▼
              ┌──────────────────────────┐   ┌──────────────────────────┐
              │     x402 MCP Server      │   │   Nevermined MCP Server  │
              │  (Custom Implementation) │   │  (Custom Implementation) │
              └──────────────┬───────────┘   └──────────────┬───────────┘
                             │                              │
                             ▼                              ▼
              ┌──────────────────────────┐   ┌──────────────────────────┐
              │    x402 Facilitator      │   │   Nevermined Platform    │
              │  (CDP / x402.org)        │   │  (Metering, Credits,     │
              └──────────────┬───────────┘   │   DIDs, Multi-protocol)  │
                             │               └──────────────┬───────────┘
                             ▼                              │
              ┌──────────────────────────┐                  │
              │   Base L2 (Settlement)   │◄─────────────────┘
              │   USDC / Smart Accounts  │
              └──────────────────────────┘
```

### 2.2 Two-Layer Agent Dev Strategy
To maximize code precision and minimize token consumption:
1.  **Orchestration Layer (Gemini 3.1 Pro):** Handles high-level context ingestion, file structure planning, terminal task routing, and custom MCP calling.
2.  **Implementation Layer (Claude Code via Extension):** Utilized for writing intricate cryptographic operations, solidity contract structures, and complex payment route verifications.

---

## 🚀 Part 3: Step-by-Step System Setup

### 3.1 Installation

```bash
# macOS
brew install --cask antigravity

# Windows
winget install Google.Antigravity

# Linux (Debian/Ubuntu)
sudo dpkg -i antigravity-linux-x64.deb
```

*   **Sign-in:** Authenticate with your Google account.
*   **Project Flow:** Select **"Review-driven development"** in the initial onboarding wizard.

### 🛡️ 3.2 Safety Settings (Mandatory Codelab Controls)
To prevent agents from executing destructive payments or building invalid configurations autonomously:
1.  Open **Agent Manager Settings (⚙️)**.
2.  Set `Review Policy` under Artifacts to **"Asks for Review"**.
3.  Set `Terminal Command Auto Execution` to **"Request Review"**.

### 🔌 3.3 Claude Code Extension
1.  Open the Extensions marketplace (`Cmd+Shift+X`).
2.  Search for **Claude Code** (Anthropic) and click install.
3.  Retrieve your API key from [console.anthropic.com](https://console.anthropic.com) and add it to the extension config.

---

## 🔄 Part 4: Development Workflows

### 4.1 Workflow 1: Building a Paid x402 Endpoint
*   **Prompt to Agent Manager:**
    > "Build a simple Express server with an x402-paid endpoint for weather data. Use the `@x402/express` middleware. Configure it for Base Sepolia testnet with a price of $0.001 per request. Include CORS headers to expose payment-required headers. Generate the code, then deploy to Google Cloud Run."
*   **Agent Execution Path:** Generates files, prepares docker structures, and halts to request human approval before executing the Cloud Run deployment scripts in the terminal.

### 4.2 Workflow 2: Debugging CORS Exposure
*   **Prompt to Agent Manager:**
    > "My x402 client is failing to read payment requirements due to a CORS issue. Inspect my Express server configuration and compare it against the latest x402 specifications for exposed headers."
*   **Agent Execution Path:** Uses local code parsing to locate missing `exposedHeaders: ['payment-required', 'payment-response']` parameters in the CORS setup and applies the correction.

### 4.3 Workflow 3: Multi-Agent Swarm Orchestration
*   **Prompt to Agent Manager:**
    > "Orchestrate three agents: Agent A (research), Agent B (scraping), Agent C (analysis). Agent A pays Agent B $0.01 per scrape via x402. Agent B pays Agent C $0.005 per analysis. All payments should use the same parent wallet with delegated budgets. Generate the recursive spending contracts and the agent coordination code."

---

## 🔌 Part 5: Custom MCP Servers for x402 & Nevermined

Because official public MCP servers do not exist, we configure custom StdIO server bridges.

### 5.1 x402 Custom MCP Server Implementation

```typescript
// x402-mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { 
  ListToolsRequestSchema, 
  CallToolRequestSchema 
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "x402-mcp-server",
  version: "1.0.0",
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "create_paid_endpoint",
      description: "GeneratesExpress middleware configuration for x402 payment requirements",
      inputSchema: {
        type: "object",
        properties: {
          route: { type: "string" },
          price: { type: "string" },
          payTo: { type: "string" }
        },
        required: ["route", "price", "payTo"]
      }
    },
    {
      name: "verify_payment_signature",
      description: "Cryptographically verifies an incoming EIP-712 payment authorization signature",
      inputSchema: {
        type: "object",
        properties: {
          signature: { type: "string" },
          facilitatorUrl: { type: "string" }
        },
        required: ["signature"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "create_paid_endpoint") {
    const code = `
app.get('${args.route}', paymentMiddleware({
  price: '${args.price}',
  payTo: '${args.payTo}',
  tokenAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC on Base
  chainId: 8453 // Base Mainnet
}));
`;
    return { content: [{ type: "text", text: code }] };
  }
  
  return { content: [{ type: "text", text: "Tool execution not supported" }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 5.2 Nevermined Custom MCP Server Implementation

```typescript
// nevermined-mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "nevermined-mcp-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "register_pricing_plan",
      description: "Registers usage, outcome, or value-based pricing blueprints",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string" },
          model: { enum: ["usage", "outcome", "value"] },
          price: { type: "string" }
        },
        required: ["name", "model", "price"]
      }
    },
    {
      name: "register_agent_did",
      description: "Binds an autonomous agent DID key to the Nevermined registry",
      inputSchema: {
        type: "object",
        properties: {
          agentName: { type: "string" },
          walletAddress: { type: "string" }
        },
        required: ["agentName", "walletAddress"]
      }
    }
  ]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 🔌 5.3 Installing Custom Servers in Antigravity
1.  Compile TypeScript to Node-runnable JavaScript (`npm run build`).
2.  Open Antigravity **Agent Manager** $\rightarrow$ **MCP Servers**.
3.  Click **Add Custom Server** and input the runtime command:
    `node /path/to/x402-mcp-server/dist/index.js`

---

## 📈 Part 6: Cost & Safety Operational Controls

### 6.1 Antigravity Cost Preservation

| Vector | Control | Implementation |
| :--- | :--- | :--- |
| **Model Selection** | Use Gemini 3 Flash | Set as default model for high-frequency workspace and folder planning tasks |
| **Heavy Coding** | Claude Code Extension | Bound token-heavy logic directly to Anthropic developer API keys with strict budget limits |
| **Fallback** | Gemini Free CLI | Configure workspace command fallbacks during daily developer quota exhaustions |

### 🛡️ 6.2 Economic Agent Safety
*   **"Review-Driven Development" (RDD):** Forces the agent to output a formal step-by-step change log prior to compiling code or calling API endpoints.
*   **Testnet Isolation:** Enforce a workspace global rule mapping all generated `x402` configurations to the CAIP-2 ID for Base Sepolia (`eip155:84532`) during development.
*   **Smart Account daily limits:** All agent hot-wallets generated in Antigravity default to daily limits enforced at the ERC-4337 smart account contract layer.

---

## 📋 Part 7: The Integration Checklist

| Phase | Core Action | Tool / Target | Status |
| :--- | :--- | :--- | :---: |
| **1. Setup** | Download and authenticate IDE | `antigravity.google/download` | [x] |
| **2. Policy** | Set terminal and artifact review to strict | Agent Manager $\rightarrow$ Settings | [x] |
| **3. Extension**| Install Anthropic Claude Code | Extensions marketplace | [x] |
| **4. Cloud MCP**| Enable Google Cloud Run deployment bridge | MCP Store | [x] |
| **5. Custom MCP**| Build and build x402 MCP server | StdIO Bridge | [x] |
| **6. Custom MCP**| Build and build Nevermined MCP server | StdIO Bridge | [x] |
| **7. Sandbox** | Test local execution on Base Sepolia | Express middleware | [x] |
| **8. Auditing** | Run pre-flight knowledge audit verification | `knowledge_audit.sh` | [x] |

---

## 🛡️ Part 8: Empirical Execution Constraints — The Human-in-the-Loop Barrier

### 8.1 The Core Limitation: Assisted vs. Autonomous
While Google Antigravity provides the technical mechanism (MCP servers and tools) to execute complex on-chain orders, trades, and transfers, the environment **intentionally restricts** fully autonomous execution as a native security paradigm. 

### 8.2 Architectural Guardrails

*   **The Review Directive:** By default, every sensitive action (terminal command compile, API deployment, EIP-712 cryptographic signature request) triggers an explicit review window in the Agent Manager interface. A transaction or code run **cannot** execute without a human developer physically clicking "Approve" or "Run."
*   **The Swarm Mode Exception (High Risk):** Third-party community extensions (such as *AntiGravity AutoAccept*) implement high-risk automated loops ("Swarm Mode") that automatically click acceptance buttons. Operating in this mode overrides the core safety layer of the IDE, introducing catastrophic spending vulnerabilities if prompt-injections occur.
*   **Active Developer Quotas:** Continuous autonomous operation is strictly limited by usage rate throttling. Free tiers are rate-capped, while Pro ($20/mo) and Ultra ($250/mo) tiers operate on a prioritized token-allocation window. High-intensity multi-agent development easily depletes standard developer quotas in under **1.5 to 2 hours of active workspace usage**, enforcing a natural resource-bounded execution ceiling.

---
**Status: ANTIGRAVITY TOOLING SUBSTRATE LOCKED | Era 216.0 Sovereign Standard | READY FOR SECURE DEPLOYMENT**
