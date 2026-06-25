# Contributing to Sovereign 7G

## How to Contribute

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make changes** (PEP 8, 88 char limit, type hints required)
4. **Test**: All 19 tests must pass
5. **Submit a PR** with a clear description

## Agent Architecture

```python
class MyAgent:
    """Brief description. Part of the 62-agent swarm."""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc).isoformat()

    def generate_report(self) -> dict:
        return {"agent_id": N, "status": "ACTIVE"}

    def run_once(self) -> dict:
        return self.generate_report()
```

## PR Requirements

- [ ] All 19 tests pass
- [ ] No files over 400 lines
- [ ] Agent follows base pattern
- [ ] New env vars documented
- [ ] Agent count updated in SDK
