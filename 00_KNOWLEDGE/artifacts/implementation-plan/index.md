---
created: '2026-06-22T21:51:39Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T21:51:43.295980Z'
---

# Implementation Plan: 7G Network Operational & Design Gap Closure

This plan outlines the concrete code changes and infrastructure additions required to transition the Sovereign 7G Network from a secure logic model into a production-ready, observable, and bridged live network.

---

## User Review Required

> [!IMPORTANT]
> - **Private Keys and Gas**: The Python relayer and on-chain integration tests will require access to a wallet private key containing Base Sepolia/Mainnet gas to sign transactions. These keys must be loaded via environment variables (`PRIVATE_KEY` / `RELAYER_KEY`), not hardcoded.
> - **Safe Multisig Address**: Safe deployments are network-specific. We will document the transfer of `DEFAULT_ADMIN_ROLE` to a generic Safe address. In live operations, this address must be pre-configured.
> - **On-Chain Transactions in SIP Proxy**: Adding on-chain calls to `SipProxy` increases latency of SIP handling because blockchain transactions take a block time (~2s on Base) to mine. We will implement these calls asynchronously to prevent blocking the UDP socket event loop.

---

## Proposed Changes

### Component 1: Solidity Smart Contracts

#### [MODIFY] [NodeLicense.sol](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/contracts/NodeLicense.sol)
- **Revocation & Recovery (Gap 7)**:
  - Add `revokeLicense(uint256 tokenId)` restricted to `ISSUER_ROLE`. This sets `licenses[tokenId].isActive = false` and emits a suspension/revocation event.
  - Add `recoverLicense(uint256 tokenId)` restricted to `ISSUER_ROLE`. This restores `licenses[tokenId].isActive = true` and emits a recovery event.

---

### Component 2: Cross-Chain Relayer & Signaling Plane

#### [NEW] [relayer.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/relayer.py)
- **Base ↔ ICP Relay (Gap 3)**:
  - Implement an async Python relayer using `web3.py` and standard HTTP requests.
  - **Base → ICP**: Listens for `ProposalExecuted` events from `SovereignDAO` on Base, hashes the execution state, and registers modules/calls on the ICP Move VM canister.
  - **ICP → Base**: Periodically polls the `move_vm` canister for new slash events via `get_pending_slashes()`, and calls `ICPReverseBridge.submitSlash()` on Base.
  - Implements local nonce caching for replay protection.

#### [MODIFY] [sip_proxy.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/sip_proxy.py)
- **On-Chain Settlement Integration (Gap 5)**:
  - Import `Web3` to connect to Base.
  - In `handle_invite()`, spawn a background async task to invoke `CallSession.initializeSession()` using the contract ABI.
  - In `handle_bye()`, spawn a background async task to calculate session durations and packet/latency stats, and call `CallSession.endSession()` followed by `CallSession.settleSession()`.

---

### Component 3: Live Verification & Monitoring Infrastructure

#### [NEW] [monitoring/bot.js](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/monitoring/bot.js)
- **Transaction Monitoring Bot (Gap 1)**:
  - Create a Node.js daemon using `ethers.js` to subscribe to event logs of the 7 deployed contracts.
  - Specifically monitor and print alerts for:
    - `NodeSlashed` and `SlashExecuted` events.
    - `RoleGranted` and `RoleRevoked` admin actions.
    - Large token transfer events or failed settlements.

#### [NEW] [test_onchain.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/test_onchain.py)
- **On-Chain Integration Test Suite (Gap 4)**:
  - Implement a Python integration test suite using Web3.
  - Sends actual signed transactions to a local testnet / Base RPC endpoint to verify live node staking, claiming rewards, eSIM registering, and session creation/settlement.

#### [NEW] [emergency_response_plan.md](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/emergency_response_plan.md)
- **Key Rotation & Disaster Playbook (Gap 2)**:
  - Document step-by-step procedures for:
    - Revoking compromised keys using a Safe multisig wallet.
    - Transferring contract permissions to a safe multisig.
    - Pausing staking contract operations under exploit scenarios.

---

### Component 4: DEX Pool Bootstrapping

#### [NEW] [deploy_liquidity.sh](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/scripts/deploy_liquidity.sh)
- **DEX Pool Deployment Guide (Gap 6)**:
  - Document the exact shell commands using Forge and Cast to deploy `S7GLiquidityBootstrapper.sol` and seed the S7G/ETH liquidity pool on Uniswap V3.

---

## Verification Plan

### Automated Checks
- Run `forge build` to verify modified contracts compile.
- Run `cargo check` to verify Rust workspaces.
- Run `python3 test_sip_proxy.py` to confirm the SIP Proxy signaling plane still passes loopbacks cleanly.

### Manual Verification
- We will execute the new on-chain tests against a local Anvil fork of Base Mainnet to ensure no real money is spent during validation, while guaranteeing complete E2E on-chain validation of staking and sessions.
