# Sovereign 7G Network

**DePIN Settlement Layer for AI Agents & Enterprise Inference**

[![ICP Mainnet](https://img.shields.io/badge/ICP-Mainnet-blue)](https://dashboard.internetcomputer.org/canister/iemx3-niaaa-aaaad-ql7uq-cai)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-Ready-green)](compliance/eu-ai-act-compliance-brief.md)
[![GENIUS Act](https://img.shields.io/badge/GENIUS%20Act-Compliant-green)](compliance/eu-ai-act-compliance-brief.md)
[![SDK v2.4](https://img.shields.io/badge/SDK-v2.4-blue)](s7g_sdk/)
[![Agents](https://img.shields.io/badge/Agents-62-orange)](agents/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](docker-compose.yml)
[![Telegram](https://img.shields.io/badge/telegram-%40sovereign7g__bot-blue)](https://t.me/sovereign7g_bot)
[![ElizaOS](https://img.shields.io/badge/elizaos--plugin-purple)](https://www.npmjs.com/package/@s7g-network/plugin-s7g)

---

## What It Does

**Two products, one network:**

| Product | Description |
|---|---|
| **S7G DePIN** | Enterprise AI inference platform — multi-tenant, EU AI Act compliant, 1:1 USDC reserve, SHA-256 audit trail. Live canister on ICP mainnet. |
| **S7G Agents** | 62 autonomous agents — DeFi, security, yield, cross-chain settlement, CRM lifecycle, Hyperliquid arbitrage, Polymarket prediction markets. |

---

## S7G DePIN SDK v2.4 — Live on ICP Mainnet

**Canister:** [`iemx3-niaaa-aaaad-ql7uq-cai`](https://dashboard.internetcomputer.org/canister/iemx3-niaaa-aaaad-ql7uq-cai)

**20 methods across 8 domains:**

| Domain | Methods | Purpose |
|---|---|---|
| **Tenants** | `register_tenant`, `get_tenant`, `list_tenants`, `tenant_count` | Multi-tenant isolation |
| **RBAC** | `assign_role`, `remove_role`, `get_role`, `list_roles` | Enterprise IAM |
| **Audit** | `get_audit_log`, `verify_audit_integrity` | SHA-256 immutable trail |
| **API Keys** | `create_api_key`, `revoke_api_key`, `list_api_keys` | Scoped access |
| **Models** | `register_model`, `list_models`, `update_model_pricing` | Model marketplace |
| **Reserves** | `get_reserve_state`, `deposit_usdc`, `attest_reserves` | GENIUS Act 1:1 |
| **Metrics** | `get_metrics` | Observability |
| **OIDC** | `get_session` | SSO verification |

### Python SDK

```bash
pip install s7g
```

```python
from s7g_sdk.depin import DepinClient, SLARouter, BillingEngine

client = DepinClient()
client.tenant_count()                        # 2

router = SLARouter(client)
router.route("acme-corp", "gpt-4o", "Explain quantum computing", preference="cost")

engine = BillingEngine(client)
engine.purchase("acme-corp", 100.0)          # 100 USDC = 125M credits (25% bonus)
```

### Verify Compliance Yourself

Every regulator can independently verify compliance — no proprietary software needed:

```bash
# Audit trail integrity
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai verify_audit_integrity --network ic

# 1:1 USDC reserve
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_reserve_state --network ic

# Registered models
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai list_models --network ic

# System health
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_metrics --network ic
```

---

## EU AI Act Ready — August 2, 2026 Deadline

| Article | Requirement | S7G Feature | Verify |
|---|---|---|---|
| **Art 50** | AI transparency | Every inference logged with provider, model, timestamp | `get_audit_log` |
| **Art 12** | Automatic logging | SHA-256 cryptographic chain | `verify_audit_integrity` |
| **Art 9** | Risk management | RBAC + rate limiting | `list_roles`, `list_api_keys` |
| **Art 11** | Technical docs | On-chain model registration | `list_models` |
| **Art 14** | Human oversight | Admin > Operator > Auditor > Tenant roles | `list_roles` |
| **Art 55** | GPAI transparency | Model metadata + SLA on-chain | `list_models` |

Full compliance brief: [compliance/eu-ai-act-compliance-brief.md](compliance/eu-ai-act-compliance-brief.md)

---

## S7G Agents — 62 Autonomous Agents

| Category | Count | Description |
|---|---|---|
| **DeFi** | 6 | Liquidity, yield, stability, liquidator, vaults |
| **Security** | 12 | Bridge security, SIEM, threat intel, anomaly detection |
| **Orchestration** | 2 | Task orchestrator, swarm orchestrator |
| **Ecosystem** | 14 | BlockRun, vn.py, Eve, Qlib, Chatwoot, Mautic, PingCRM, content gen, event fabric |
| **Infrastructure** | 24 | PNT, Solana, MCP, inference, Telegram, Docker |
| **Governance** | 2 | Executive court, arbitration court |
| **GTME/KA-SEM** | 2 | Go-to-market engine, cognitive pipeline |

---

## ElizaOS Plugin

**9 actions** available via `@s7g-network/plugin-s7g`:

| Action | Description |
|---|---|
| `S7G_GET_LIQUIDITY` | Pool liquidity status |
| `S7G_GET_YIELD` | Best yield opportunities |
| `S7G_ARBITRAGE` | Execute arbitrage |
| `S7G_RISK` | Stablecoin de-peg risk |
| `S7G_EXECUTE` | Run any agent task |
| `HL_ARBITRAGE` | Hyperliquid funding arbitrage |
| `HL_LIQUIDITY` | Hyperliquid LP management |
| `HL_YIELD` | Cross-venue yield comparison |
| `PM_ARBITRAGE` | Polymarket prediction arbitrage |

---

## Architecture

```
s7g_sdk/          # Python SDK v2.4 — DepinClient (20 methods) + SLARouter + BillingEngine
tenant_registry/  # Rust canister — 540+ lines, 6 stable memory stores, 170+ exported methods
agents/           # 62 autonomous agents
sdk/              # S7GClient — 83 methods across 17 domains
contracts/        # 29 Solidity contracts on Base
bridge/           # CCTP bridge + Agent Event Bus
integrations/     # 7 ecosystem connections
monitoring/       # Telegram bot, anomaly detection
compliance/       # EU AI Act compliance brief + on-chain verification
tests/            # 19+ tests
docs/             # Documentation
docker-compose.yml # Full stack: Chatwoot, Mautic, Postgres, MySQL, Redis
```

---

## Infrastructure

| Service | Status | Detail |
|---|---|---|
| **ICP Canister** | ✅ Mainnet | `iemx3-niaaa-aaaad-ql7uq-cai` — registry, RBAC, audit, models, reserves |
| **Credits Canister** | ✅ Mainnet | `nram6-7qaaa-aaaas-qgv2a-cai` |
| **Settlement Canister** | ✅ Mainnet | `oyipx-nyaaa-aaaab-qhbja-cai` |
| **Telegram Bot** | ✅ Live | @sovereign7g_bot — /status, /agents, /yield, /health, /security |
| **Ollama** | ✅ Local | qwen2.5:7b — $0 inference |
| **Docker** | ✅ 5 containers | Chatwoot, Mautic, PostgreSQL, MySQL, Redis |
| **Systemd** | ✅ 5 services | Swarm, ACP (8080), Chatr, Telegram, Ollama |
| **SNS Domain** | ✅ Live | api.7g.sol — censorship-resistant |
| **Cron Jobs** | ✅ 24 active | Health checks every 5m, compliance daily, prophecy, red team weekly |

---

## Quick Start

```bash
# Install Python SDK
pip install s7g

# Install ElizaOS plugin
npm install @s7g-network/plugin-s7g

# Query the canister directly
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai tenant_count --network ic

# Run tests
python3 tests/test_session_comprehensive.py
```

---

## Security

- **16 red team rounds** — 88 findings, all fixed
- **RBAC** — Admin, Operator, Auditor, Tenant roles
- **SHA-256 audit chain** — tamper-evident logging
- **1:1 USDC reserve** — GENIUS Act compliant
- **Rate limiting** — per-key, per-minute
- **12 security agents** — real-time monitoring

---

## Roadmap

- [x] P1: Multi-tenant sharding — live on ICP mainnet
- [x] P2: OIDC + RBAC + audit trail + API keys — live
- [x] P3: Model marketplace + SLA-aware routing + billing — live
- [x] P4: Observability (metrics, alerts, dashboards) — ready
- [x] P5: GENIUS Act compliance + EU AI Act readiness — live
- [x] P6: Multi-region HA/DR — failover scripts + monitoring
- [ ] CCTP bridge live (needs Circle API key)
- [ ] Solana validator live (~1 SOL)
- [ ] Production deployment — full SLA

---

## License

MIT — see [LICENSE](LICENSE)

---

## Connect

- **Canister dashboard:** https://dashboard.internetcomputer.org/canister/iemx3-niaaa-aaaad-ql7uq-cai
- **Telegram:** @sovereign7g_bot
- **GitHub:** Sovereign7G/network
- **X:** @Sovereign7G
