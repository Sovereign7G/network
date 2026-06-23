# Contributing to S7G Network

## How to Contribute

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make changes** following the style guide
4. **Test**: All 19 tests must pass
5. **Submit a PR** with a clear description

## Code Style

- Python: PEP 8, 88 char line limit
- Use type hints for all function signatures
- Docstrings for all public methods
- Keep files under 400 lines (refactor otherwise)

## Agent Architecture

Each agent follows this pattern:

```python
class MyAgent:
    """Brief description. Part of the 62-agent swarm."""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc).isoformat()

    def generate_report(self) -> dict:
        """Return structured status."""
        return {"agent_id": N, "agent_name": "MyAgent", "status": "ACTIVE"}

    def run_once(self) -> dict:
        """Called by test suite."""
        return self.generate_report()
```

## Testing

```bash
# Before submitting a PR
python3 tests/test_session_comprehensive.py
# Must show: 19/19 PASS
```

## PR Requirements

- [ ] All 19 tests pass
- [ ] No files over 400 lines
- [ ] Agent follows BaseAgent pattern
- [ ] New env vars documented in README
- [ ] Skills updated if adding new agents

## Adding a New Agent

1. Create file in `agents/agent_name.py`
2. Add to SDK: `sdk/py/s7g/__init__.py` or domain module
3. Add test to `tests/test_session_comprehensive.py`
4. Update agent count in SDK constant
5. Run tests — all must pass
