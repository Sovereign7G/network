# Settlement Canister Recovery
## Canister: oyipx-nyaaa-aaaab-qhbja-cai (saved in its own repo)

This covers recovery for the settlement canister (DePIN jobs, EVM signing,
TON, attestation, invitations). The registry canister recovery is covered
in `tenant-registry-ops` skill.

## Prerequisites

- dfx 0.32+ or icp-cli installed
- Deployer identity with cycles (≥10B)
- Rust wasm32-unknown-unknown target

## Recovery Steps

### 1. Build the canister

```bash
cd /media/cherry/4A21-00001/New\ folder/AGE\ REPUBLIC/sovereign_icp_backend
cargo build --target wasm32-unknown-unknown --release
```

Build output: `target/wasm32-unknown-unknown/release/sovereign_icp_backend_backend.wasm`

### 2. Verify canister still exists

```bash
dfx canister info oyipx-nyaaa-aaaab-qhbja-cai --network ic
```

If the canister was deleted, it must be recreated (see Step 4).

### 3. Upgrade existing canister

```bash
dfx canister install oyipx-nyaaa-aaaab-qhbja-cai \
  --wasm target/wasm32-unknown-unknown/release/sovereign_icp_backend_backend.wasm \
  --network ic --mode upgrade --yes
```

### 4. Create canister from scratch (if deleted)

```bash
# This canister is NOT in the S7G repo — it has its own repo.
# Use icp-cli for creation (dfx canister create is broken):
icp identity default deployer
icp canister create sovereign_icp_backend \
  -e ic --controller $(dfx identity get-principal) --cycles 600000000000
icp canister install oyipx-nyaaa-aaaab-qhbja-cai \
  --wasm target/wasm32-unknown-unknown/release/sovereign_icp_backend_backend.wasm \
  --mode install --network ic
```

### 5. Verify

```bash
dfx canister call oyipx-nyaaa-aaaab-qhbja-cai get_job_stats '("check")' --network ic
# Should return JSON with job counts (0 if empty)
```

## Data Loss on Reinstall

If the canister is reinstalled (not upgraded), ALL state is lost:
- DePIN job history
- Outreach records
- Invitations
- Node balances
- EVM nonce tracker

Only upgrade preserves state. There is no backup mechanism.
