# S7G Architecture

## Three-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│                   KA-SEM (Cognitive Brain)                  │
│  Semantic Planner → Dual Temporal Memory → AGE-300K Training│
│  Decides what to monitor based on trajectory analysis       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              S7G (Autonomous Nervous System)                 │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Agent Event  │  │   Swarm     │  │   Event     │      │
│  │    Bus       │  │ Orchestrator│  │   Fabric    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Telegram   │  │  Chatr.ai   │  │  Docker     │      │
│  │    Bot       │  │   Agent     │  │  Stack      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              GTME (Go-To-Market Engine)                     │
│  Discovery Beacon → Provider Scoring → CRM → Content       │
│  Drives adoption, relationships, and ecosystem growth      │
└─────────────────────────────────────────────────────────────┘
```

## Agent Categories

| Category | Count | Agents |
|----------|-------|--------|
| **Core** | 22 | DeFi, DePIN, cross-chain, trading, cognitive, governance |
| **Security** | 12 | Bridge security, threat intel, SIEM, anomaly detection |
| **CRM/Ecosystem** | 10 | PingCRM, Mautic, Chatwoot, ContentGenerator, Chatr.ai |
| **Infrastructure** | 8 | SwarmOrchestrator, EventFabric, Telegram, Ollama, Docker |
| **Trading** | 10 | Hyperliquid, Polymarket, multi-venue arb, yield optimizer |

## Communication Flow

```
Agent Action → Agent Event Bus → AetherDB Bridge
                                  ↓
                         Subscriber Agents
                                  ↓
                         Telegram Bot / Chatr.ai / Mautic
```

## Infrastructure Stack

| Layer | Technology | Cost |
|-------|-----------|------|
| Compute | Local GPU (GTX 980M) + Ollama qwen2.5:7b | $0 |
| State | ICP Canisters (mainnet) | ~3.9 TC cycles |
| Storage | AetherDB Bridge (10K ring buffer) | Included |
| Bot | Telegram API (free) | $0 |
| Social | Chatr.ai API (free) | $0 |
| CRM | Docker (Chatwoot + Mautic + databases) | $0 |
| Domain | Solana Name Service (api.7g.sol) | One-time fee |
