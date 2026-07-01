# S7G Governance — Built-In Control Plane

The Sovereign 7G Network's governance is not an add-on. It is built
into the architecture at every layer, following the same principle
IBM Research applies in CUGA: "the governed path is the default."

## Project Governance

Following the Valkey/Linux Foundation model of open, community-driven
governance for open-source infrastructure.

### Maintainer Model

See `MAINTAINERS.md` for the current maintainer list and the process
for becoming a maintainer.

### Decision-Making

Decisions are made by lazy consensus:
- Proposals are submitted as GitHub issues with the `proposal` label
- A 7-day comment period follows
- If no objections are raised, the proposal is accepted
- For contentious decisions, maintainers vote (simple majority)

### Contribution Process

See `CONTRIBUTING.md` for the full contribution guide.

### Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR** — Breaking changes to the A2A protocol or Agent Card format
- **MINOR** — New specialists, skills, or non-breaking features
- **PATCH** — Bug fixes, documentation, verification improvements

Each release is tagged in git and the Agent Card's `version` field is
updated to match.

## Technical Governance — Built-In Control Plane

### Layer 1: Authentication (ACP/A2A)

All agent invocations require Bearer token authentication. The ACP
server validates every request before routing it to any agent.

```
Authorization: Bearer ***
→ 401 if missing or invalid
→ 200 if valid
```

### Layer 2: Rate Limiting

Every IP is limited to 100 requests per minute. Prevents abuse while
allowing legitimate multi-agent traffic.

### Layer 3: Goal Lifecycle

Goals pass through explicit states with built-in verification:

```
planning → submitted → working → verifying → completed/failed
                              ↓
                            paused ← resume
```

Each state transition is logged with a trace ID. Failed verification
prevents a goal from reaching "completed" — the agent must either
succeed or explicitly fail.

### Layer 4: Verification

Every goal result runs through domain-specific verification checks:

| Domain | Verification Checks |
|--------|-------------------|
| Coordinator | Specialists responded, results synthesized |
| Security | Threats checked, no false positives |
| Dev | PRs reviewed, services healthy |
| Content | Content generated, publication verified |
| Ops | Cron jobs healthy, webhooks delivered |
| Strategy | Market data collected, routes verified |

### Layer 5: Tracing

Every action generates a unique trace ID. Full audit trail:

```
Goal: goal-abc123
  ├── Step 1: coordinator/analyze_swarm_status → goal-abc123-0
  ├── Step 2: coordinator/delegate_to_specialists → goal-abc123-1
  ├── Step 3: security/audit_logs → goal-abc123-2
  └── Verification: 3/3 checks passed
```

### Layer 6: Standard Response Contract

All tool responses follow the defined envelope (see AGENT_CONTRACT.md):

```python
# Success — agent continues
{"ok": true, "data": {...}, "trace_id": "..."}

# Failure — agent replans
{"ok": false, "error": "...", "code": "ERROR_CODE", "trace_id": "..."}
```

This is the same pattern IBM Research identifies as critical:
"CUGA's planner handles a declared failure gracefully and chokes on
an undeclared one."

## Why This Matters

> "The control plane is already there. The governed path is the default...
> you're not retrofitting controls onto something built for open access."
> — IBM Research, "Build real agentic apps using CUGA" (June 23, 2026)

Your system was built with governance from day one:
- A2A auth was implemented before the first external connection
- Goal lifecycle and verification were added before public registration
- Tracing was built before the first agent went live

This is not a retrofitted compliance layer. It is the architecture.
