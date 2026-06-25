# S7G Python SDK

**v2.4** — 83 methods across 5 modules. Unified client for the S7G network.

```python
pip install s7g
```

```python
from s7g import S7GClient
client = S7GClient()
status = client.swarm_status()
```

---

## Modules

| Module | Methods | Description |
|--------|---------|-------------|
| **Core** (`__init__.py`) | 42 | Voice, messaging, nodes, beamforming, analytics, identity, LoRA IoT, ICP mesh |
| **Bridge** (`domains/bridge.py`) | 13 | CCTP settlement, POS dongle, court operations, stablecoin routes |
| **Solana** (`domains/solana.py`) | 10 | Validator info, staking, swap, balance, transfer, MoneyGram, DePIN |
| **Agents** (`domains/agents.py`) | 6 | Swarm status (62 agents), agent info, logs |
| **Yield** (`domains/yield_router.py`) | 1 | Multi-chain yield aggregation |

---

## Core (`sdk/py/s7g/__init__.py`)

```python
from s7g import S7GClient
client = S7GClient(api_base="https://api.7g.sol")
```

| Method | Description |
|--------|-------------|
| `send_message(to, text)` | Send SIP/SMS message |
| `get_messages(limit=50)` | Retrieve message history |
| `initiate_call(to, duration)` | Start SIP call session |
| `end_call(session_id)` | Terminate active call |
| `register_node(node_id, location)` | Register mesh node |
| `node_status(node_id)` | Get node health metrics |
| `list_nodes(status=None)` | List all registered nodes |
| `beam_steer(node_id, azimuth, elevation)` | Steer beam direction |
| `beam_status(beam_id)` | Get beam parameters |
| `get_analytics(metric, period)` | Query network analytics |
| `resolve_identity(name, protocol)` | Resolve ENS/HNS/SNS/DID |
| `lora_send(device_id, payload)` | Send LoRA packet |
| `lora_receive(device_id)` | Read LoRA telemetry |
| `mesh_register(node_id, endpoint)` | Register in ICP mesh |
| `mesh_route(source, dest)` | Get mesh routing path |

---

## Bridge (`sdk/py/s7g/domains/bridge.py`)

```python
from s7g.domains.bridge import cctp_bridge_balance, cctp_cross_chain_settle
```

| Method | Description |
|--------|-------------|
| `cctp_bridge_balance()` | Query CCTP bridge balance |
| `cctp_cross_chain_settle(amount, target_chain)` | Cross-chain USDC settlement |
| `cctp_verify_attestation(tx_hash)` | Verify CCTP attestation |
| `pos_settle(amount, currency)` | Settle POS transaction |
| `pos_verify(proof_hash)` | Verify POS payment proof |
| `pos_status()` | POS system health |
| `executive_court(action, agent_id)` | Executive court ruling |
| `arbitration_court(dispute_id)` | Arbitration resolution |
| `governance_proposal(proposal)` | Submit governance proposal |

---

## Solana (`sdk/py/s7g/domains/solana.py`)

```python
from s7g.domains.solana import solana_validator_info, solana_stake, solana_swap
```

| Method | Description |
|--------|-------------|
| `solana_validator_info()` | Solana validator status |
| `solana_stake(amount)` | Stake SOL via validator |
| `solana_unstake(amount)` | Unstake SOL |
| `solana_rewards()` | Claim validator rewards |
| `solana_swap(token_in, token_out, amount)` | Jupiter swap |
| `solana_balance(token=None)` | Token balance |
| `solana_transfer(to, amount, token)` | Transfer tokens |
| `solana_moneygram_status()` | MoneyGram validator status |
| `solana_network_stats()` | Solana network metrics |
| `solana_depin_projects()` | DePIN project overview |

---

## Agents (`sdk/py/s7g/domains/agents.py`)

```python
from s7g.domains.agents import swarm_status, swarm_agent_info
```

| Method | Description |
|--------|-------------|
| `swarm_status()` | Swarm health overview (62 agents) |
| `swarm_agent_info(agent_id)` | Specific agent details |
| `swarm_logs(agent_id=None, limit=50)` | Agent log entries |

### Constants

```python
client.AGENTS       # {"total": 62, "ka_sem": 5, ...}
client.COURTS       # Court contract addresses
client.STABLECOINS  # Stablecoin addresses by chain
client.CHAINS       # Supported chain configs
```

---

## Yield (`sdk/py/s7g/domains/yield_router.py`)

| Method | Description |
|--------|-------------|
| `multi_yield_vault()` | Multi-chain yield aggregation |

---

## Error Handling

All methods return `S7GCall`:

```python
result = client.solana_balance()
print(result.data)    # Response payload
print(result.ok)      # bool
print(result.error)   # Error message if failed
```
