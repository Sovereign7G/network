# Sovereign AI Mesh Design Specification (2026-07-01)

## 1. Executive Summary
This design specification defines the integration of the **S7G Committee Node** with a **Decentralized AI Inference Gateway** deployed on the Akash Network. The S7G Committee Node acts as an immutable, Byzantine fault-tolerant (BFT) authorization, consensus, and provenance logging layer. Each inference request and its corresponding token usage/response metadata is cryptographically proposed, agreed upon by the committee, and committed to a local SQLite-backed ledger on each validator node, ensuring complete censorship resistance, decentralization, and high auditability.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                                │
│  (Web App / Mobile / CLI / API Gateway)                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP (auth header)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                ROUTER & ORCHESTRATION LAYER                     │
│  • LiteLLM Gateway (model routing)                             │
│  • S7G Auth Middleware (provenance + identity)                 │
│  • API Key / Rate Limiting                                     │
│  • Load Balancer (round-robin across replicas)                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│               S7G COMMITTEE LAYER (Consensus)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Node 1   │  │ Node 2   │  │ Node 3   │  │ Node 4   │      │
│  │ (Leader) │  │ (Follower│  │ (Follower│  │ (Follower│      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│        │             │             │             │             │
│        └─────────────┴─────────────┴─────────────┘            │
│                   (BFT Consensus over P2P)                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Internal DNS / HTTP
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│               INFERENCE ENGINE LAYER (Akash)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │ Replica 1│  │ Replica 2│  │ Replica 3│  (auto-scaling)    │
│  │ vLLM     │  │ vLLM     │  │ vLLM     │                     │
│  │ L4 GPU   │  │ L4 GPU   │  │ L4 GPU   │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 DATA & PERSISTENCE LAYER                        │
│  • Model Registry (Hugging Face)                              │
│  • Persistent Volumes (model weights + SQLite files)           │
│  • Logging / Metrics (Prometheus + Grafana)                   │
│  • Usage Analytics (PostgreSQL)                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Directory Structure

The project code is organized as a subdirectory within the Sovereign 7G Network workspace:

```
decentralized-ai-inference/
├── deploy/
│   ├── sdl/
│   │   └── production.yaml        # Unified SDL (exposes Gateway, runs S7G + vLLM)
│   └── scripts/
│       ├── deploy.sh              # Unified deployment driver
│       └── monitor.sh             # Cost & health monitoring
├── gateway/
│   ├── liteLLM/
│   │   └── config.yaml            # LiteLLM settings + custom auth hook
│   └── auth/
│       └── s7g_middleware.py         # Custom FastAPI middleware (calls S7G API)
├── s7g-committee/
│   ├── Dockerfile                 # Main container build
│   ├── Dockerfile.cli             # CLI tool build
│   ├── requirements.txt           # Python dependencies
│   ├── entrypoint.sh              # Startup orchestrator
│   ├── node/
│   │   ├── __init__.py
│   │   ├── api.py                 # Main FastAPI endpoints (/propose, /commit, /ledger)
│   │   ├── models.py              # Pydantic schemas
│   │   ├── dependencies.py        # Dependency singletons (Ledger & PBFT instance)
│   │   └── config.py              # Configuration settings
│   ├── consensus/
│   │   ├── __init__.py
│   │   ├── bft.py                 # PBFT state machine (propose, pre-prepare, prepare, commit)
│   │   ├── p2p.py                 # Internal node-to-node connectivity
│   │   ├── rpc.py                 # RPC server endpoints
│   │   └── ledger.py              # SQLite storage wrapper
│   ├── genesis/
│   │   └── genesis.json           # Genesis validators and public keys
│   └── scripts/
│       ├── cli.py                 # CLI configuration utility
│       ├── join-committee.sh
│       └── propose-block.sh
└── docker-compose.yml             # Local multi-node development suite
```

---

## 4. S7G Committee Node

### PBFT Consensus (Byzantine Fault Tolerance)
*   **Size**: $N = 4$ validators, allowing tolerance of $f = 1$ Byzantine (malicious or offline) node ($3f + 1 = 4$).
*   **State Machine**:
    1.  **Pre-Prepare**: Leader node receives a proposal, assigns a sequence number, signs it, and broadcasts it to all peers.
    2.  **Prepare**: Followers validate the proposal's signature and sequence number, then broadcast a signed `prepare` vote. Once a node collects $2f + 1$ matching prepare votes, it enters the *prepared* state.
    3.  **Commit**: Nodes broadcast a signed `commit` vote. Once $2f + 1$ commit votes are gathered, the block is finalized and committed to the ledger.

### Persistence (Ledger)
Each validator node maintains its own local SQLite database file located on an Akash persistent mount (`/app/ledger/ledger.db`). This ensures that ledger state is preserved across container restarts and remains completely decentralized.

---

## 5. Gateway Integration

*   **LiteLLM custom auth middleware**: Hooks into the gateway pipeline.
*   **Request Propose**: The middleware extracts the prompt parameters and forwards them to `/propose` on the S7G committee leader.
*   **Inference Execution**: Upon proposal agreement, the request is executed against the internal vLLM cluster.
*   **Request Commit**: The resulting token usage metrics are submitted to the committee via `/commit` to seal the transaction.

---

## 6. Security Model
*   **Asymmetric Keys**: Nodes sign messages using SECP256K1 elliptic curve cryptography.
*   **Byzantine Fault Tolerance**: Protects against up to 1 faulty/adversarial node out of 4.
*   **Internal Networking**: S7G API endpoints are exposed internally (global: false) inside the Akash private network fabric, ensuring only the LiteLLM gateway can interact with them.

---

## 7. Verification Plan

### Automated Tests
*   `pytest s7g-committee/tests` to validate PBFT state transitions, SQLite schema initialization, and API behavior under normal and Byzantine (simulated network failure) scenarios.

### Manual Verification
*   Deploy using local `docker-compose.yml` to verify end-to-end consensus flow (3 nodes + gateway) before pushing image to registry and deploying on Akash.
