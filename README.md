# S7G Network — Sovereign P2P Operable System

---

## Core Components

### Sidecar Distribution System
Distributed sidecar resolver enabling P2P node discovery with ICP canister integration for on-chain governance. Seeder service provides network bootstrapping with cryptographic verification of all distribution payloads.

### Mobile Over-the-Air Updates
Native iOS (Swift) and Android (Kotlin) stubs with automated CI/CD builds via GitHub Actions. Update payloads are cryptographically signed, enabling direct distribution without App Store review.

### Cryptographic Provenance
Hypercore append-only logs provide an immutable audit trail for all system events, with integration to ICP canister for on-chain verification.

### P2P Committee Mesh
Iroh relay with QUIC transport, Hyperswarm DHT for peer discovery, and direct P2P tunnels between committee members. Systemd service ensures persistent operation.

### A2A Agent Network
DID-based identity framework (DIF/AGE) with an A2A agent server supporting attestation, provenance queries, and health/connectivity testing. Task delegation across the agent mesh with sub-100ms response time.

---

## Deployment Status

| Service | Status |
|---------|--------|
| ICP Canister | Live (v1–v8) |
| Resolver Daemon | systemd |
| Iroh Relay | v1.0.1 |
| Committee Node | systemd |
| Provenance Feed | Active |
| Mobile Stubs | iOS + Android |
| A2A Server | Built |
| CI/CD Pipeline | Operational |

---

## Technical Stack

**Distribution Layer**
- Hyperswarm DHT — peer discovery
- Hypercore — append-only logs
- Iroh relay — TCP/443 QUIC transport
- Pair CLI — deployment tooling

**Governance Layer**
- DID-based identity (DIF/AGE)
- 3-of-5 multi-sig (5 governors, threshold=3)
- ICP canister — 32-byte keys, on-chain provenance
- Resolver daemon — auto-updating nodes

---

## Documentation

| Resource | Path |
|----------|------|
| Reference Index | `docs/00_INDEX.md` |
| Skill Definition | `hermes_home/skills/s7g-pair-integration/SKILL.md` |
| CI/CD Pipeline | `.github/workflows/mobile-stub-build.yml` |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Holepunch** — Hyperswarm, Hypercore, Autobase, Iroh
- **ICP** — Internet Computer canister
- **DIF/AGE** — DID-based identity framework
