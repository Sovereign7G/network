# 🏛️ AGE REPUBLIC :: UNIFIED COGNITIVE & INFRASTRUCTURE ROUTER ARCHITECTURE
## Era 232.0 — Sealed and Attested Systemic Blueprint

This document maps the precise interaction pipelines, intent-resolution matrices, and attestation boundaries that coordinate the **Model Context Protocol (MCP) Router**, the **Sovereign AGY Command-Line Suite**, the **Conversational NL Parser**, and the **x402 Hardware-Bound Secure Enclaves**.

```mermaid
graph TD
    %% User/Agent Interface
    A["👤 Operator / AI Agent Chat Input"] -->|Natural Language Prompt| B["💬 Conversational Interpreter<br>(conversational_parser.py)"]
    
    %% Intent Resolution
    B -->|Decodes Intent Schema| C["⚙️ Sovereign Command-Line Suite<br>(agy_cli.py)"]
    
    %% CLI Command Subsystems
    C -->|agy say / agy chat| C1["📊 Token Ledger Audit<br>(cmd_token)"]
    C -->|agy transfer| C2["🔐 Biometric Attestation Gate<br>(cmd_transfer)"]
    C -->|agy wallet| C3["💳 Secure Enclave Audit<br>(cmd_wallet)"]
    C -->|agy launch| C4["🚀 EVM Contract Deployment<br>(cmd_launch)"]
    C -->|agy bridge| C5["📡 Quad-Mode Inference Bridge<br>(cmd_bridge)"]
    
    %% Attestation & Security
    C2 -->|Locks APHS Proposal| D["🛡️ Token Ledger Memory Database<br>(memory_vault.db)"]
    D -->|Request Operator Attestation| E["🔑 Hardware Verification Enclave<br>(.heavyskill_Antigravity.key)"]
    E -->|Validates SHA-256 Checksum| F["🟢 Broadcasters to EVM Substrate L2<br>(Arbitrum / Gas Channels)"]
    
    %% MCP Router Layer
    G["🕸️ Model Context Protocol Server<br>(sovereign_mcp_server.py:8091/8092)"] -->|Triage API Gate| C
    G -->|Real-time Ingress| H["👁️ Sovereign Event Watcher<br>(event_watcher.py)"]
    G -->|Telemetry HUD| I["📈 WebSocket Client Streams<br>(ws_server.py)"]
    G -->|Enclave Actions| J["🛠️ MicroVM Provisioner<br>(deploy_enclave_as_microvm.sh)"]
```

---

## 1. The Conversational Intent Parsing Pipeline
When an operator or conductor agent submits a natural language message (e.g. *"sweep 500 SWARM to my x402 address"*), the request is intercepted by `conversational_parser.py` inside the active cockpit handler:

```python
interpret_cockpit_message(msg, linked_wallet)
```

### Decoded Intent Resolution Table

| Target Input Phrase | Decoded Intent | Mapped AGY CLI Subcommand | Target Subsystem / Execution Node |
| :--- | :--- | :--- | :--- |
| `"sweep 500 SWARM to my x402"` | `transfer` | `agy transfer --amount 500 --token SWARM --target <wallet> --confirm biometric` | Biometric attestation gate & ledger database |
| `"audit my tokens / balances"` | `token_balance` | `agy token --balance` | Reads local ledger vault balances |
| `"verify my enclave status"` | `wallet_status` | `agy wallet --status` | Connects to x402 API & dynamic L1/L2 RPC gas checks |
| `"launch contract to arbitrum"` | `launch_contract`| `agy launch --live --network arbitrum` | Compiler (forge solc) & EVM deployment gateway |
| `"ask the bridge: [prompt]"` | `bridge_query` | `agy bridge --mode local --prompt "[prompt]"` | Quad-Mode inference engine & Token balance billing |

---

## 2. Secure Attestation & AI-Proposed, Human-Signed (APHS) Transfers
For security, raw CLI commands cannot bypass attestation checks when mutating treasury states. Every payout is governed by the **APHS Protocol**:

1. **Proposal Isolation**: The CLI builds a proposal payload `proposal_id = aphs_[timestamp]` and writes it to the local encrypted SQLite DB (`memory_vault.db`).
2. **Attestation Gate**: The execution suspends until operator approval is confirmed. The system scans the secure hardware keyspace for `.heavyskill_Antigravity.key` (attested hardware token).
3. **Bytecode Broadcast**: Upon signature validation, a deterministic Keccak-256 transaction hash is calculated, and the payout is broadcast to L2 EVM gas pipelines (e.g., Arbitrum).

---

## 3. Model Context Protocol (MCP) Triage Server
Operating continuously on ports **8091 (HTTP)** and **8092 (WebSockets)**, `sovereign_mcp_server.py` acts as the global triage gateway. It bridges autonomous agents to physical infrastructure resources:

* **Enclave Lifecycle Registry (`/api/mcp/enclaves`)**: Scans `05_SECURITY/` and tracks region enclaves (Norway, Sydney, Tokyo, Quebec).
* **Headless Action Queue (`/api/mcp/pending` & `/api/mcp/approve`)**: Handles high-risk commands (Isolation of compromised nodes, deployment of new enclaves, slashing validator shortfalls).
* **Dynamic Heat Map (`/api/mcp/enclaves/state`)**: Feeds real-time telemetry coordinates to cockpit dashboards.
* **Integrity Auditing (`/api/mcp/integrity`)**: Executes automated local system scans, verifying file integrity at machine speed.
* **Bi-directional Webhook Ingress (`/api/mcp/webhook/eventgrid`)**: Implements event-driven file synchronization (MOU agreements, export ledgers) over cloud-to-local enclaves.

---

## 4. Coala Memory Framework Integration
The routing infrastructure maps directly to the **Coala 4-Pillar Memory Architecture**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    COALA MEMORY LAYER INTEGRATION                          │
├────────────────────────────────────────────────────────────────────────────┤
│  • WORKING   ──► ws_server.py streams live cockpit state & active telemetry │
│  • SEMANTIC  ──► SQLite memory_vault.db registers wallet balances / tags  │
│  • PROCEDURAL──► agy_cli.py subcommands define the executable tool space   │
│  • EPISODIC  ──► audit.log tracks every signed proposal & action execution │
└────────────────────────────────────────────────────────────────────────────┘
```

**This architecture guarantees absolute sovereignty, ensuring that while AI agents proposes and orchestrates actions, human physical keys retain the ultimate signature authority over the federation's state.**
