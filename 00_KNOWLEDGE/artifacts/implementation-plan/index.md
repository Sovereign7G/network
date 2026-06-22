---
created: '2026-06-22T15:06:45Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T15:06:49.692657Z'
---

# Implementation Plan: Zero-Trust External Model Privacy Gateway for Sovereign OS

This plan outlines the architecture and execution strategy for **Era VI: Zero-Trust External Model Privacy Gateway**. The gateway acts as a secure intermediary routing agent requests to DeepSeek, Kimi, and EU-hosted compliant providers (e.g. TextCortex) without exposing proprietary OKF concepts or violating data residency restrictions.

## User Review Required

> [!IMPORTANT]
> - **Zero-Trust Policy**: By default, all external APIs are treated as untrusted. Raw OKF files or concepts are never sent directly to external providers.
> - **Real & Mock Dual Execution**: To ensure seamless running in the development testbed, the gateway will attempt real API requests if keys (`DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `TEXTCORTEX_API_KEY`) are present in the environment; otherwise, it will fall back to high-fidelity mocks with correct telemetry metadata.
> - **Budget Enforcement**: A monthly/daily budget limit will be stored in the routing policy. Any request exceeding the cap will be blocked locally.

## Open Questions

> [!NOTE]
> - **Caching Policy**: We propose a simple token-overlap/Jaccard similarity threshold of $0.85$ to detect duplicate or highly similar queries in the local cache (`08_ASSETS/gateway_cache.json`). Please review if you prefer a different match metric.
> - **EU Data Residency**: We will configure TextCortex as the default provider when `eu_data_residency` is enabled in the policy JSON.

---

## Proposed Changes

### Privacy Gateway Engine Development

#### [MODIFY] [external_gateway.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/external_gateway.py)
- **Zero-Trust Policy Configuration**:
  - Load and save configuration parameters from `08_ASSETS/gateway_policy.json`.
  - Config parameters: `routing_policy` (default/secure/eu-only), `eu_data_residency` (boolean), `budget_cap_usd` (float), `budget_spent_usd` (float), `pii_redaction` (boolean), `mock_external_apis` (boolean).
- **Sanitizer & Redactor Layer**:
  - Expand `SENSITIVE` regular expressions to strip emails, Ethereum addresses, hex private keys, relative paths (e.g. `00_KNOWLEDGE/...`), and specific proprietary tags.
- **Local Query Cache**:
  - Implement a JSON-backed cache in `08_ASSETS/gateway_cache.json`.
  - Query caching returns previously retrieved results for identical/similar prompts to save tokens and prevent unnecessary data egress.
- **Audit Logs**:
  - Log audit logs to `08_ASSETS/gateway_audit.json` with timestamp, provider, prompt hash, response hash, latency, token count, and budget impact.
- **Multi-Provider Routing Wrappers**:
  - Support `deepseek`, `kimi`, and `textcortex` endpoints.
  - Implement robust mock fallback for all three providers when keys are missing.

---

### OKF Server Registration

#### [MODIFY] [magix_okf.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/magix_okf.py)
- Register the 4 new MCP tools:
  - `external_infer(provider: str, prompt: str, skill: str = "", bypass_cache: bool = False)`: Route sanitized prompt to external models.
  - `gateway_health()`: Report connection status, available providers, and telemetry counts.
  - `gateway_policy(new_policy: dict = None)`: View or update routing/region/filter policies.
  - `gateway_audit()`: Retrieve tail of audit log hashes.
- Register endpoints inside the FastAPI server.

---

### Telemetry & Dashboard Integration

#### [MODIFY] [triad_metrics.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/triad_metrics.py)
- Collect live Gateway metrics: total external calls, cache hits, sanitization/redaction events, budget spent, and average latency.
- Expose the gateway metrics in `TriadMetrics.collect()`.

#### [MODIFY] [triad_dashboard.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/triad_dashboard.py)
- Add a new "🔒 Privacy Gateway" dashboard panel.
- Show active routing rules, budget consumption, cache hit rate, and audit event logs.

---

## Verification Plan

### Automated Tests
- Call the `gateway_health` MCP tool via HTTP to ensure config parameters are read correctly.
- Test `external_infer` tool using curl:
  - Verify that private info (e.g. `user@example.com` or `0x1234...`) gets successfully redacted in the request and logged in the audit trail.
  - Verify cache hits on repeated prompts.
- Verify `gateway_policy` can get and set the active policy dynamically.

### Manual Verification
- Access the dashboard on port 8080 and verify the "Privacy Gateway" panel is updated in real time.
