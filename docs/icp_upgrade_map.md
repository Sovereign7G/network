# S7G ICP Canister A2A Upgrade Map
# ================================
# Maps the A2A settlement attestation integration across all 6 ICP
# canisters. Each canister gets new endpoints for batch attestation,
# agent discovery, or settlement event recording.
#
# The upgrade mirror pattern: Python MerkleRollupEngine →
# ICP canister → on-chain storage → A2A agent query

## Canister Upgrade Summary

| Canister | Type | Upgrade File | New Endpoints | Purpose |
|----------|------|-------------|---------------|---------|
| **sovereign_icp_backend** | Rust | `a2a_settlement_upgrade.rs` | 7 | Batch attestation storage, inclusion proofs, agent capability discovery |
| **tenant_registry** | Rust | `a2a_settlement_upgrade.rs` | 6 | Settlement-to-tenant linkage, attestation verification for regulators |
| **sovereign_swarm** | Rust | `a2a_settlement_upgrade.rs` | 3 | Settlement event recording, L2 cross-chain forwarding |
| **aetherdb_bridge** | Rust | No Rust changes needed | 0 | Consumes ICP attestations via inter-canister calls |
| **move_vm_canister** | Rust | No Rust changes needed | 0 | Move VM execution — attestation-agnostic |
| **swarm_brain** | Motoko | No changes | 0 | Orchestrated by sovereign_swarm |

## Data Flow

```
Python A2A Server (off-chain)
  │
  ├─ MerkleRollupEngine.trigger_rollup()
  │   └─ submit_batch_attestation() → sovereign_icp_backend ✓
  │       └─ store_inclusion_proof() → sovereign_icp_backend ✓
  │
  ├─ record_settlement() → tenant_registry ✓
  │   └─ verify_tenant_attestation() → tenant_registry ✓
  │
  └─ record_batch_settlement() → sovereign_swarm ✓
      └─ get_settlement_health() → sovereign_swarm ✓

External A2A Agent (discovery)
  │
  └─ get_agent_capability() → sovereign_icp_backend ✓
      └─ Returns agent_card_url + okf_base_url + supported_methods
```

## Deployment Order

```bash
# 1. Apply Rust upgrades to each canister's lib.rs
#    (follow the instructions in each a2a_settlement_upgrade.rs)

# 2. Copy the Candid file
cp sovereign_icp_backend/src/sovereign_icp_backend_backend/sovereign_icp_backend.did \
   sovereign_icp_backend/src/sovereign_icp_backend_backend/

# 3. Deploy all canisters
dfx deploy --network ic

# 4. Verify
python3 scripts/verify_icp_upgrades.py --network ic
```

## Verification Commands

```bash
# Agent discovery
dfx canister --network ic call sovereign_icp_backend get_agent_capability

# Submit a test attestation
dfx canister --network ic call sovereign_icp_backend submit_batch_attestation \
  '("s7g-batch-1746400000","a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",3,50000,vec{"ICP";"SOL"})'

# Query attestation
dfx canister --network ic call sovereign_icp_backend get_batch_attestation \
  '("s7g-batch-1746400000")'

# Tenant verification
dfx canister --network ic call tenant_registry record_settlement \
  '("demo-tenant","s7g-batch-1746400000","a1b2c3...",50000,3,vec{"ICP";"SOL"})'

dfx canister --network ic call tenant_registry verify_tenant_attestation \
  '("demo-tenant")'

# Swarm health
dfx canister --network ic call sovereign_swarm record_batch_settlement \
  '("s7g-batch-1746400000","a1b2c3...",3,50000.0,vec{"ICP";"SOL"})'

dfx canister --network ic call sovereign_swarm get_settlement_health
```

## Python → ICP Integration

The Python `MerkleRollupEngine.trigger_rollup()` should call these
ICP canister methods after each batch settlement:

```python
from ic.client import ICClient  # pip install ic-py

client = ICClient(network="https://ic0.app")
backend = client.canister("sovereign_icp_backend")

# After MerkleRollupEngine.trigger_rollup():
backend.submit_batch_attestation(
    batch_id, merkle_root, tx_count, total_value, attested_ledgers
)

# For each transaction in the batch:
for tx in batch.transitions:
    proof = merkle_accumulator.get_inclusion_proof(tx.tx_id)
    backend.store_inclusion_proof(tx.tx_id, proof["proof"])
```

## Rollback

If an upgrade fails, roll back with:

```bash
dfx canister --network ic install sovereign_icp_backend --mode reinstall
# State is lost on reinstall. Use --mode upgrade for state-preserving deploys.
```
