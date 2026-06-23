# S7G Python SDK

**v2.4** — 83 methods across 5 modules. Unified Python client for the S7G network.

```python
pip install s7g
```

```python
from s7g import S7GClient

client = S7GClient()
status = client.swarm_status()
print(f"{status['agents_online']} agents online")
```

## Quick Start

### Check swarm health
```python
from s7g import S7GClient
client = S7GClient()
status = client.swarm_status()
```

### Solana validator info
```python
from s7g.domains.solana import solana_validator_info
info = solana_validator_info()
print(info)
```

### Cross-chain settlement
```python
from s7g.domains.bridge import cctp_cross_chain_settle
result = cctp_cross_chain_settle(amount=1000, target_chain="solana")
```

---

## Modules

| Module | File | Methods |
|--------|------|---------|
| **Core** | `sdk/py/s7g/__init__.py` | 42 |
| **Bridge** | `sdk/py/s7g/domains/bridge.py` | 13 |
| **Solana** | `sdk/py/s7g/domains/solana.py` | 10 |
| **Agents** | `sdk/py/s7g/domains/agents.py` | 6 |
| **Yield** | `sdk/py/s7g/domains/yield_router.py` | 1 |

Full API reference: [docs/SDK_REFERENCE.md](docs/SDK_REFERENCE.md)

---

## SDK Packages

```
sdk/
├── py/s7g/
│   ├── __init__.py          # Core client (42 methods)
│   ├── domains/
│   │   ├── bridge.py        # CCTP, POS, courts (13 methods)
│   │   ├── solana.py        # Validator, staking, swap (10 methods)
│   │   ├── agents.py        # Swarm status, agent info (6 methods)
│   │   └── yield_router.py  # Yield aggregation (1 method)
├── cli/
│   └── commands/init.py     # CLI tool
└── js/src/index.ts          # TypeScript SDK
```
