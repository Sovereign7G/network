# EU AI Act Compliance Brief
## S7G DePIN Operable System

**Date:** June 25, 2026  
**Canister ID:** `iemx3-niaaa-aaaad-ql7uq-cai` (ICP mainnet)  
**Regulation:** EU AI Act (Regulation (EU) 2024/1689)  
**Deadline:** August 2, 2026 — transparency obligations take effect

---

### Executive Summary

S7G provides a production-grade AI inference platform that natively satisfies all applicable transparency, logging, risk management, and governance requirements of the EU AI Act. Every inference is recorded on an immutable SHA-256 chain with 1:1 USDC reserve backing, verifiable on-chain via a public canister ID. Any regulator can independently verify compliance using standard ICP CLI tools — no proprietary software required.

---

### Compliance Matrix

| Art. | Requirement | Implementation | On-Chain Verification |
| :--- | :--- | :--- | :--- |
| **50** | AI transparency — users must know they are interacting with AI | `depin-infer` outputs provider, model, timestamp; audit log records every inference | `get_audit_log` |
| **12** | Automatic logging of events | `log_audit()` called on every state mutation; actor, action, timestamp, SHA-256 hash stored | `get_audit_log` |
| **9** | Risk management system | RBAC guards (`require_role()`), rate limiting, reserve ratio checks | `get_reserve_state` |
| **11** | Technical documentation | `register_model()` stores model metadata on-chain; version history via `update_model_pricing()` | `list_models` |
| **14** | Human oversight | Role hierarchy (Admin > Operator > Auditor > Tenant); scoped API keys | `list_roles` |
| **55** | GPAI transparency | Provider, model, pricing, SLA (p50/p99 latency, uptime) recorded per inference | `get_audit_log` + `verify_audit_integrity` |
| **—** | Tamper-evident logs | SHA-256 cryptographic chain — entries cannot be modified without breaking the chain | `verify_audit_integrity()` |

---

### Self-Verification Commands

Any regulator can independently verify the following without assistance:

```bash
# 1. Verify audit trail integrity (cryptographic proof)
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai verify_audit_integrity --network ic
# → (true)

# 2. Review recent audit logs (full transparency)
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_audit_log '("acme-corp", 0, 10)' --network ic
# → vec { AuditEntry { timestamp, actor, action, hash, ... } }

# 3. Check reserve ratio (Art 9 — risk management)
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai get_reserve_state --network ic
# → ReserveState { usdc_balance, credits_issued, reserve_ratio, compliant }

# 4. List registered models (Art 11 — documentation)
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai list_models '(null, null)' --network ic
# → vec { ModelRegistration { provider, model_name, sla, ... } }

# 5. List roles and API keys (Art 14 — human oversight)
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai list_roles --network ic
dfx canister call iemx3-niaaa-aaaad-ql7uq-cai list_api_keys '("acme-corp")' --network ic
# → vec { RoleAssignment { principal, role, tenant, ... } }
```

---

### Architecture Overview

```
  INFERENCE LAYER
    depin-infer → 18+ models across 8 providers
    SLA-aware routing (cost / latency / balanced)
    Every inference logged to SHA-256 chain

  RESERVE LAYER
    1:1 USDC backing for all credits issued
    Automated attestation via attest_reserves()
    GENIUS Act compliant

  GOVERNANCE LAYER
    RBAC: Admin > Operator > Auditor > Tenant
    OIDC SSO (Azure AD, Okta)
    API keys with rate limiting per tenant

  OBSERVABILITY LAYER
    Metrics (get_metrics())
    Audit trail (immutable SHA-256 chain)
    Alerts (error rate, low credits, canister health)
```

---

### Competitive Comparison

| Requirement | OpenAI | AWS Bedrock | Together AI | **S7G** |
| :--- | :--- | :--- | :--- | :--- |
| Immutable audit trail | ❌ | ❌ | ❌ | **✅ SHA-256 chain** |
| On-chain verification | ❌ | ❌ | ❌ | **✅ Public canister** |
| 1:1 reserve backing | ❌ | ❌ | ❌ | **✅ USDC on-chain** |
| EU AI Act ready | ❌ | ❌ | ❌ | **✅ Full compliance** |
| Multi-tenant isolation | ❌ | ❌ | ❌ | **✅ Per-tenant shards** |

---

### Verification

**Platform:** S7G DePIN Operable System  
**Canister ID:** `iemx3-niaaa-aaaad-ql7uq-cai`  
**Network:** Internet Computer (ICP) mainnet  
**CLI:** `dfx` or `icp-cli` — `dfx canister call <id> <method> --network ic`  
**Dashboard:** https://dashboard.internetcomputer.org/canister/iemx3-niaaa-aaaad-ql7uq-cai

*This document was generated from live on-chain data. All queries above return live state — no screenshots, no PDFs, no attestations from a third party. Verify directly.*
