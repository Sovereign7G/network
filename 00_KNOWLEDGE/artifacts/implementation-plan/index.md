---
created: '2026-06-22T21:19:43Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T21:19:46.860574Z'
---

# Implementation Plan: Cross-Chain Canister Security Fixes

This plan outlines the concrete code changes required to address the 5 code-level security issues identified during the Cross-Chain Security Audit.

## User Review Required

> [!IMPORTANT]
> - We will enforce a strict access control check on `register_module` inside the `move_vm` canister, restricting registrations to a whitelisted controller principal initialized on startup.
> - We will implement stable memory persistence inside the Rust-based `move_vm` canister to prevent data loss on canister upgrades.
> - We will implement real cycle transfers in the Motoko billing gateway (`BifrostGateway.mo`) to actually distribute operator and developer shares.
> - We will adapt the Motoko API key registry (`PrometheusKeyRegistry.mo`) to use standard `ICRC-1`/`ICRC-2` interfaces to match the ICP ledger protocols and prevent runtime traps.

---

## Proposed Changes

### Component 1: Move VM Canister (`move_vm`)

#### [MODIFY] [lib.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/src/move_vm_canister/src/lib.rs)
- **Access Control on `register_module` (Issue 1)**:
  - Add a static thread-local `CONTROLLER` of type `String`.
  - Add an `init()` hook marked with `#[ic_cdk_macros::init]` to store the deployer principal string as the initial controller.
  - In `register_module`, assert that `caller().to_string() == controller` before registering any new module.
- **Stable Memory state persistence (Issue 3)**:
  - Add a `#[ic_cdk_macros::pre_upgrade]` hook that serializes `MODULES`, `PROOFS`, `METRICS`, and `CONTROLLER` into stable memory using `ic_cdk::storage::stable_save`.
  - Add a `#[ic_cdk_macros::post_upgrade]` hook that restores the state from stable memory using `ic_cdk::storage::stable_restore`.
- **Verify Proof Cryptographic check (Issue 4)**:
  - Implement a helper function `verify_zk_proof(statement: &str, proof: &[u8], proof_type: u8) -> bool` to perform standard structure, length, and coupling verification of ZK proofs instead of auto-verifying.

---

### Component 2: Motoko Cycle Billing Gateway (`BifrostGateway`)

#### [MODIFY] [BifrostGateway.mo](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/BifrostGateway.mo)
- **Actual cycle distribution (Issue 2)**:
  - Import the standard `ExperimentalCycles` base module.
  - Define a generic `CyclesReceiver` actor type signature exposing `depositCycles() : async ()`.
  - In `settleInference`, allocate the computed `devShare` and `operatorShare` cycle payouts using `ExperimentalCycles.add()` and invoke the recipients' `depositCycles()` canisters asynchronously.

---

### Component 3: Prometheus Key Registry (`PrometheusKeyRegistry`)

#### [MODIFY] [PrometheusKeyRegistry.mo](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/PrometheusKeyRegistry.mo)
- **ICRC-1 / ICRC-2 Ledger compatibility (Issue 5)**:
  - Define the standard types for ICRC ledger operations: `Account`, `TransferArgs`, `TransferResult`, `TransferFromArgs`, and `TransferFromResult`.
  - Update `ageLedger` actor declaration to match the standard ICRC-1 (`icrc1_transfer`) and ICRC-2 (`icrc2_transfer_from`) specifications.
  - In `registerKey`, perform the deposit using `icrc2_transfer_from` (transferring from `msg.caller`'s approved allowance to the key registry).
  - In `deactivateKey`, perform the refund using `icrc1_transfer` to refund the operator account.

---

## Verification Plan

### Automated Build Checks
We will run compilation checks on all canisters to ensure that the modifications compile correctly:
- Run `cargo check` inside `src/move_vm_canister/` to verify Rust code correctness.
- Run `dfx start --background` and `dfx deploy` on a local replica (if available) to verify canister packaging and deployment paths.

### Manual Verification
- We will double check all ledger canister signatures and stable storage serialize/deserialize hooks to guarantee stable upgrades.
