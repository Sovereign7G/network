# S7G Agent Response Contract

Every agent tool and A2A method in the Sovereign 7G Network returns
a standardized response envelope, following the proven CUGA pattern
from IBM Research (see: https://huggingface.co/blog/ibm-research/cuga-apps).

## Envelope

```python
# Every tool/agent response follows this structure
{
    "ok": True,           # bool — success/failure
    "data": {...},         # any — the actual response payload
    "error": None,         # str | None — error message on failure
    "code": None,          # str | None — error code (e.g. "RATE_LIMITED")
    "trace_id": "a1b2..."  # str — distributed trace for debugging
}
```

## Success

```python
{"ok": True, "data": {"status": "completed", "agent_id": "coordinator"}, "error": None, "code": None, "trace_id": "tx-abc123"}
```

## Failure

```python
{"ok": False, "data": None, "error": "Tool 'search_catalog' returned 429", "code": "RATE_LIMITED", "trace_id": "tx-def456"}
```

## Why This Convention Matters

> "It looks like boilerplate. It isn't. CUGA's planner handles a declared failure gracefully and chokes on an undeclared one."
> — IBM Research, "Build real agentic apps using CUGA" (June 23, 2026)

A declared failure (`ok: false`) lets the agent:
- Skip the failed step and continue
- Re-route to an alternative tool
- Log the error with trace context
- Re-plan instead of crashing

An undeclared failure (bare exception) forces the agent to:
- Derail mid-plan
- Lose intermediate state
- Produce a partial or incorrect result

## Integration with A2A

The A2A JSON-RPC 2.0 response format wraps this envelope:

```python
# A2A success
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "status": "completed",
        "result": {"ok": True, "data": {...}, "trace_id": "tx-abc"}
    }
}

# A2A failure
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32603,
        "message": "Tool returned error: RATE_LIMITED"
    }
}
```

## Verification Checks

Goal verification runs against this envelope:

```python
def verify_result(result: dict) -> dict:
    checks = [
        {"name": "ok_flag", "passed": result.get("ok") is True},
        {"name": "has_trace", "passed": bool(result.get("trace_id"))},
        {"name": "no_error", "passed": result.get("error") is None},
    ]
    return {
        "success": all(c["passed"] for c in checks),
        "checks": checks,
        "summary": f"{sum(c['passed'] for c in checks)}/{len(checks)} checks passed"
    }
```
