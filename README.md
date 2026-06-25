# Sovereign 7G Network

## DePIN Settlement Layer for AI Agents & Enterprise Inference

![ICP Mainnet](https://img.shields.io/badge/ICP-Mainnet-blue)
![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-Ready-green)
![GENIUS Act](https://img.shields.io/badge/GENIUS%20Act-Compliant-green)
![SDK v2.4](https://img.shields.io/badge/SDK-v2.4-blue)
![30 Agents](https://img.shields.io/badge/Agents-30-orange)

---

## What It Does

**Two products, one network:**

| Product | Description |
|---|---|
| **S7G DePIN** | Enterprise AI inference platform — multi-tenant, EU AI Act compliant, 1:1 USDC reserve, SHA-256 audit trail |
| **S7G Agents** | 30 autonomous agents — DeFi, DePIN, cross-chain settlement, Hyperliquid arbitrage, Polymarket prediction markets |

---

## S7G DePIN SDK v2.4 — Live on ICP Mainnet

**20 methods across 8 domains:**

| Domain | Methods |
|---|---|
| Credits | `get_balance`, `add_credits`, `spend_credits` |
| Tenants | `register_tenant`, `get_tenant`, `list_tenants` |
| RBAC | `assign_role`, `remove_role`, `list_roles` |
| Audit | `get_audit_log`, `verify_audit_integrity` |
| API Keys | `create_api_key`, `revoke_api_key`, `list_api_keys` |
| Models | `register_model`, `list_models`, `update_model_pricing` |
| Reserves | `get_reserve_state`, `deposit_usdc`, `attest_reserves` |
| Inference | `infer` (SLA-aware routing) |

**Canister ID:** `iemx3-niaaa-aaaad-ql7uq-cai`

### Python SDK

```python
from s7g_sdk.depin import DepinClient

client = DepinClient(tenant="acme-corp")
balance = client.get_balance("OPENAI")
result = client.infer("gpt-4o", "Explain quantum computing")
```

### Verify Compliance Yourself

```bash
# Verify audit trail integrity
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai verify_audit_integrity --network ic

# Check 1:1 reserve ratio
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_reserve_state --network ic

# View audit logs
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_audit_log '("acme-corp", 0, 10)' --network ic
```

---

## EU AI Act Ready — August 2 Deadline

| Article | Requirement | S7G Feature |
|---|---|---|
| Art 50 | AI transparency | Every inference logged with provider, model, timestamp |
| Art 12 | Automatic logging | SHA-256 audit chain (`get_audit_log`) |
| Art 9 | Risk management | RBAC guards + rate limiting (`assign_role`) |
| Art 11 | Technical docs | On-chain model registration (`register_model`) |
| Art 14 | Human oversight | Admin/Operator/Auditor/Tenant roles |
| Art 55 | GPAI transparency | Model metadata + SLA on-chain |

**GENIUS Act 1:1 Reserve:**

```bash
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_reserve_state --network ic
# Returns: usdc_balance, credits_issued, reserve_ratio, compliant
```

---

## 30 Autonomous Agents

| Category | Agents | Description |
|---|---|---|
| **Liquidity** | 8 | Pool management, yield harvesting, rebalancing |
| **Arbitrage** | 6 | Cross-chain CCTP, Hyperliquid funding, Polymarket predictions |
| **Risk** | 4 | Stablecoin de-peg monitoring, position sizing |
| **Governance** | 4 | Proposal drafting, voting, delegation |
| **Execution** | 8 | Trade execution, order routing, slippage management |

---

## ElizaOS Actions (9)

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

## Infrastructure

| Component | Description |
|---|---|
| **Network** | ICP mainnet (canister: `iemx3-niaaa-aaaad-ql7uq-cai`) |
| **Bridge** | CCTP cross-chain (Base ↔ Ethereum ↔ Solana) |
| **Domain** | `api.7g.sol` (SNS — no ICANN, no renewal) |
| **SDK** | Python (`s7g_sdk`) + ElizaOS plugin (`@s7g-network/plugin-s7g`) |
| **Contracts** | 29 Solidity contracts on Base |
| **Monitoring** | Telegram + Discord alert bots |

---

## Quick Start

```bash
# Install Python SDK
pip install s7g

# Install ElizaOS plugin
npm install @s7g-network/plugin-s7g

# Query the canister directly
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai tenant_count --network ic

# Run inference
depin-infer acme-corp gpt-4o "Explain quantum computing"
```

---

## Security

The system has undergone 16 red-team engagements targeting the canister interface, the Python bridge, and the CLI toolchain — 88 findings remediated across four audit passes. No outstanding findings in any severity tier.

**Access controls.** All canister mutations are gated on a four-tier RBAC model (Admin, Operator, Auditor, Tenant). API keys are tenant-scoped with configurable per-minute rate caps. OIDC SSO integration supports Azure AD and Okta as identity providers.

**Audit trail.** Every state change is written to a SHA-256 hash chain stored in stable memory. The chain is independently verifiable — any regulator can call `verify_audit_integrity()` on the live canister to confirm tamper-evident logging.

**Reserve compliance.** Credits issued against USDC deposits maintain a 1:1 reserve ratio enforced at the canister level. The reserve state is public and queryable via `get_reserve_state()`.

**Operational safeguards.** Async writes prevent partial state updates on failure. Rate limiting is applied per API key, per minute, with configurable thresholds. The system degrades gracefully under load rather than dropping requests.

See `s7g-red-team-audit` skill for details.

---

## License

MIT

---

## Links

- [ICP Canister](https://dashboard.internetcomputer.org/canister/iemx3-niaaa-aaaad-ql7uq-cai)
- [SNS Domain](https://sns.ic0.app)
- [ElizaOS Plugin](https://www.npmjs.com/package/@s7g-network/plugin-s7g)
- [Python SDK](https://pypi.org/project/s7g/)
