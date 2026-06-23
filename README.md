# Sovereign 7G Network

**Decentralized settlement infrastructure for DePIN, AI agents, and institutional payments.**

[![Python SDK](https://img.shields.io/badge/python-v2.4-blue)](sdk/py/s7g/)
[![Agents](https://img.shields.io/badge/swarm-62%20agents-7B2FBE)](agents/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PR](https://img.shields.io/badge/awesome--crm-PR%20%233-blueviolet)](https://github.com/sneg55/awesome-open-source-crm/pull/3)

S7G is a fully autonomous agent swarm that manages DeFi, DePIN, cross-chain settlement, and ecosystem growth — running on **zero-cost infrastructure** via ICP canisters, local Ollama inference, and systemd services.

---

## Quick Start

```bash
pip install s7g
```

```python
from s7g import S7GClient

client = S7GClient()
status = client.swarm_status()
print(f"{status['agents_online']} agents online")
```

---

## Core Capabilities

| Domain | Agents | What It Does |
|--------|--------|-------------|
| **Cross-Chain Settlement** | 12 | USDC via CCTP (Base ↔ Solana ↔ Arbitrum), YieldRouter distribution |
| **Security & Monitoring** | 12 | Bridge security, threat detection, SIEM, anomaly detection |
| **CRM & Ecosystem** | 10 | PingCRM, Mautic marketing, Chatwoot support, content generation |
| **Infrastructure** | 8 | Swarm orchestration, event fabric, Docker deployment, Telegram bot |
| **Governance** | 2 | Tri-cameral (Executive, Arbitration, Agent) with SovereignDAO |
| **Go-To-Market** | 4 | Discovery Beacon, provider scoring, KA-SEM cognitive pipeline |
| **Trading & Yield** | 14 | Hyperliquid, Polymarket, multi-venue perp arb, yield optimization |

**Total: 62 autonomous agents** across 7 functional domains.

---

## SDK v2.4 — 83 Methods

The Python SDK is split into domain modules — import what you need:

```python
from s7g import S7GClient
from s7g.domains.solana import solana_validator_info, solana_swap
from s7g.domains.bridge import cctp_bridge_balance, pos_settle
from s7g.domains.agents import swarm_status, swarm_agent_info
```

| Module | Methods | Description |
|--------|---------|-------------|
| **Core** (`__init__`) | 42 | Auth, messaging, nodes, beamforming, identity, LoRA, analytics |
| **Bridge** (`domains/bridge.py`) | 13 | CCTP settlement, POS dongle, court operations, stablecoin routes |
| **Solana** (`domains/solana.py`) | 10 | Validator, staking, swap, MoneyGram, DePIN projects |
| **Agents** (`domains/agents.py`) | 6 | Swarm status, agent info, logs |
| **Yield** (`domains/yield_router.py`) | 1 | Multi-yield vault aggregation |

Full reference: [docs/SDK_REFERENCE.md](docs/SDK_REFERENCE.md)

---

## Infrastructure

```
├── agents/               # 36+ agent files (62 agents)
├── sdk/                  # Python SDK v2.4 (83 methods)
├── bridge/               # CCTP cross-chain bridge + Agent Event Bus
├── docs/                 # Documentation
├── tests/                # Test suite (19/19 pass)
├── docker-compose.yml    # Chatwoot + Mautic + databases
└── hermes_home/skills/   # 9 Hermes skills for the swarm
```

### Live Infrastructure

| Service | Status | Details |
|---------|--------|---------|
| **ICP Canisters** | ✅ Mainnet | Move VM, AetherDB Bridge, Swarm Brain |
| **Telegram Bot** | ✅ Live | @sovereign7g_bot — 7 commands, 10s polling |
| **Chatr.ai** | ✅ Live | S7G_Agent_v2 posting every 2 minutes |
| **Ollama** | ✅ Local | qwen2.5:7b — zero-cost inference |
| **Docker** | ✅ 5 containers | Chatwoot, Mautic, PostgreSQL, MySQL, Redis |
| **Systemd** | ✅ 5 services | Swarm, ACP, Chatr, Telegram, Ollama |
| **ACP Endpoint** | ✅ Live | `/.well-known/agent.json` on port 8080 |
| **SNS Domain** | ✅ Live | `api.7g.sol` — censorship-resistant |

---

## Architecture: KA-SEM × GTME × S7G

```
KA-SEM (Brain)
  └── Semantic Planner → Agent Memory → AGE-300K Dataset

S7G (Nervous System)
  ├── Agent Event Bus — routes decisions to 62 agents
  ├── Swarm Orchestrator — monitors + auto-restarts
  ├── Event Fabric — connects 7 ecosystems
  ├── Content Generator — produces from trajectory data
  └── aetherdb_bridge — 10K-snapshot ring buffer

GTME (Engine)
  ├── Discovery Beacon — on-chain provider registration
  ├── Provider Scoring — 23 fiat + 10 DePIN providers
  ├── Mautic — 5 campaign templates, 6 scoring rules
  ├── PingCRM — 5 contact types, Telegram-synced timeline
  └── Developer Pipeline — 14 DePIN networks on ICP
```

---

## Tests

```bash
# Run the full test suite (30 seconds)
python3 tests/test_session_comprehensive.py

# Results: 19/19 pass
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| [awesome-open-source-crm](https://github.com/sneg55/awesome-open-source-crm) | S7G's CRM integration (PR #3) |
| [PingCRM](https://github.com/sneg55/pingcrm) | AI-powered CRM with Telegram sync |
| [ElizaOS Plugin](https://www.npmjs.com/package/@s7g-network/plugin-s7g) | 9 ElizaOS actions for S7G |

---

## License

MIT — see [LICENSE](LICENSE)
