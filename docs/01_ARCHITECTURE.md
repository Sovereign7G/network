# S7G + Pair Stack — Complete System Architecture

## Architecture Principle: Distribution-Governance Separation

The integration cleanly separates two concerns. **Pair makes distribution possible; S7G makes it accountable and governed.**

| Layer | What | Maintains |
|---|---|---|
| **Pair Stack** | Distribution — DHT/Iroh transport, Hypercore/Autobase data, `pair seed/build/multisig` CLI | Holepunch OSS (~100 repos) |
| **S7G/SHROUD** | Governance — DID roles (DIF/AGE), 3-of-5 multi-sig, on-chain provenance on ICP | ICP canister (`txdkz-xqaaa-aaaaa-qhkea-cai`) |

The canister stores 32-byte discovery keys (pointers), not multi-MB binaries. The Pair stack delivers the actual bytes.

## Transport Tiers (Fallback Chain)

| Tier | Transport | Status |
|---|---|---|
| 1 (production) | Iroh relay (TCP/443 QUIC) | ✅ Installed (`iroh-relay v1.0.1`) |
| 2 (fallback) | Direct TCP | ✅ Verified (seed → resolve → SHA256) |
| 3 (when UDP open) | Hyperswarm DHT (UDP 49737) | Joins existing Pear ecosystem (1M users) |

## The Complete Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    S7G + Pair Stack — Complete                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Pair Stack = Distribution (possible)                                 │
│  ├── Hyperswarm DHT (peer discovery)                                  │
│  ├── Hypercore (append-only logs)                                     │
│  ├── Iroh relay (TCP/443 QUIC transport)                             │
│  └── pair seed / pair multisig (deployment CLI)                      │
│                                                                         │
│  S7G = Governance (accountable)                                       │
│  ├── DID-based identity (DIF/AGE)                                    │
│  ├── 3-of-5 multi-sig (5 governors, threshold=3)                     │
│  ├── ICP canister (32-byte keys, on-chain provenance)                │
│  └── Resolver daemon (auto-updating nodes)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```
