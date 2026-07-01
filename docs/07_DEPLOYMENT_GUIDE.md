# S7G + Pair Stack — Complete System Demo

Shows all phases working together: Distribution → Mobile OTA → Provenance → A2A.

Run: `node scripts/complete-demo.js`

## Demo Output

```
═══ Phase A: Sidecar Distribution ═══
  ✅ Canister live on ICP mainnet (v1-v8, 32-byte keys)
  ✅ Sidecar auto-updates via P2P (Iroh → TCP fallback)

═══ Phase B: Mobile OTA ═══
  ✅ iOS stub (Swift) + Android stub (Kotlin) generated
  ✅ Wallet bundle resolved (4,038 bytes, SHA256 verified)

═══ Phase C: Provenance ═══
  ✅ Hypercore feed: 10+ entries logged
  ✅ Chain integrity: SHA256-linked, signed entries

═══ Phase E: A2A Agent Mesh ═══
  ✅ A2A server: 3 skills (attest, provenance, echo)
  ✅ Agent discovery and delegation verified

┌─────────────────────────────────────────────────────────────────┐
│                    DEMO COMPLETE                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Verification

```bash
systemctl --user list-units --no-pager | grep s7g
tail -f /opt/s7g/shroud-enclave/logs/committee.log
tail -f /opt/s7g/shroud-enclave/logs/resolver.log
```
