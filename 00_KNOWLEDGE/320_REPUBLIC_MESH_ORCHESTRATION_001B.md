# 🏛️ REPUBLIC ENGINEERING ORDER 001-B
## Phase III: Mesh Orchestration Protocol – Sovereign Network Fabric

**Classification:** sovereign mesh orchestration specification & protocol standard  
**Status:** RATIFIED & DEPLOYMENT-READY  
**Epoch:** ERA 216.0  
**Anchored to:** [320_REPUBLIC_SENTRY_1_SPEC_001A.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/320_REPUBLIC_SENTRY_1_SPEC_001A.md)

---

## 🎯 1. Objective & Scope

This document establishes **Republic Engineering Order 001-B**, defining the **Mesh Orchestration Protocol** for coordinating distributed networks of **Sentry-1 (Class I)** static perimeter nodes. Sentry-1 nodes must combine dynamically to form a self-healing, tamper-resilient perimeter fabric without relying on centralized internet gateways, DHCP registers, cloud databases, or active WAN controls.

---

## 📡 2. Zero-Configuration Node Discovery (ESP-NOW Broadcast)

To prevent centralized chokepoints and tracking risks, Sentry-1 nodes auto-discover peer connections entirely over-the-air (OTA) via **ESP-NOW Link-Layer Broadcasts**.

```
  [Sentry-1 (Leaf)] ────────(ESP-NOW Discovery Probe)───────► [Sentry-2 (Leaf)]
          │                                                          │
          └───(Heartbeat Ack)───► [Mesh Anchor] ◄───(Heartbeat Ack)──┘
                                        │
                               (Elect Cluster Head)
                                        ▼
                            [Dynamic Gateway Peering]
```

### 1. Peer Discovery Protocol (P2P Sweep)
*   **Discovery Interval:** Nodes periodically broadcast an encrypted `DISCOVERY_PROBE` frame on channel 1, 6, and 11 every 60 seconds (with random jitter to prevent collision).
*   **Encrypted Handshake:** Peer nodes acknowledge with a signed `DISCOVERY_ACK` frame. Public keys are pinned during localized node fabrication. No external keys are accepted over-the-air.
*   **Discovery Frame Payload Structure:**
    $$\text{Payload} = \text{AES-GCM}(\text{NodeID} \parallel \text{BootCount} \parallel \text{MeshEpoch} \parallel \text{KeyFingerprint})$$

### 2. Zero Network Configuration (Self-Addressing)
*   **Direct MAC Addressing:** IP addressing, DHCP, and mDNS are completely stripped. Nodes communicate directly utilizing physical **MAC Addresses** at Layer 2.
*   **Local Neighborhood State:** Each node maintains a volatile **Neighbor Table** holding up to 32 adjacent nodes, indexed by MAC address, RSSI, and battery telemetry.

---

## 🧠 3. Lightweight Consensus & Alert Propagation (2-of-3 Validation)

To eliminate false triggers caused by environmental disturbances, the Sentry-1 fabric enforces a localized **Consensus Validation** mechanism.

```
       [MOTION SENSOR TICK]
                │
                ▼
        [Node-1 (Alert)] ──(Local Gossip Broadcast)──┐
                                                     ▼
        [Node-2 (Alert)] ──(Local Gossip Broadcast)─> [Spatial Consensus Met (2-of-3)]
                                                     ▲
        [Node-3 (Idle)]  ────────────────────────────┘
                                                     │
                                                     ▼
                                        [Alert Escalate to Relay]
```

### 1. Spatial Consensus Protocol (Gossip)
*   **Event Trigger:** When a Sentry-1 node detects a valid TinyML footstep classification (Confidence > 0.82), it enters `ALERT_PENDING` and broadcasts a signed `ALERT_PROPOSAL` frame.
*   **Consensus Window:** Adjacent peer nodes listen for Gossip frames within a strict 5000ms window.
*   **Spatial Verification Rule:** An alert is elevated to `ALERT_ACTIVE` and escalated to the Backbone Relay **only if** $\ge 2$ neighboring nodes within a localized 3-hop topology broadcast matching `ALERT_PROPOSAL` telemetry within the consensus window:
    $$\text{Alert State} = \begin{cases} \text{ALERT\_ACTIVE} & \text{if } \sum_{i=1}^{k} \text{Proposal}_i \ge 2 \text{ within } 5000\text{ms} \\ \text{ALERT\_PENDING} & \text{otherwise} \end{cases}$$

### 2. Dynamic Cooldown & Refractory Triage
*   Once consensus is verified, the mesh anchor broadcasts a validated `ALERT_CONFIRMED` payload. All leaf nodes in the localized zone enter a 10-second cooldown, preventing message storms.

---

## 👑 4. Dynamic Cluster Head & Role Election

To maximize off-grid battery lifespans, leadership and mesh-aggregation roles are distributed dynamically based on a deterministic **Sovereign Fitness Metric**.

### 1. Fitness Score Calculation
At the start of every Mesh Epoch (24-hour cycle), nodes broadcast their current telemetry. A fitness score ($F$) is calculated locally for each node:
$$F = (W_b \cdot \text{BatteryV}) + (W_l \cdot \text{MeanRSSI}) - (W_a \cdot \text{ActiveUptime\_s})$$
Where:
*   $\text{BatteryV} =$ Normalized remaining battery voltage (3.0V to 4.2V).
*   $\text{MeanRSSI} =$ Mean link-quality score across neighbors.
*   $\text{ActiveUptime\_s} =$ Time spent serving as Cluster Head in recent epochs.
*   $W_b, W_l, W_a =$ Calibrated weighting coefficients.

### 2. Election Algorithm
*   The node with the highest local fitness score ($F$) is elected **Cluster Head (Mesh Anchor)** for the epoch.
*   **Decentralized Failover:** If the Cluster Head fails to broadcast a `HEARTBEAT` tick for $\ge 300$ seconds, the peer nodes immediately trigger a re-election cycle, elevating the node with the next highest $F$ score. No fixed leaders exist.

---

## 🛡️ 5. Secure Mesh-Based Signed OTA Updates

Sovereign nodes do not query centralized update servers. Firmware distribution occurs via peer-to-peer **Mesh-Gossip Propagation**.

```
                   [Republic Cryptographic Keypair]
                                │ (Signed Update Binary)
                                ▼
                     [Sovereign Comms Relay]
                                │ (LoRa Broadcast blocks)
                                ▼
                       [Sentry-1 (Anchor)]
                              /     \
                      (Mesh OTA)   (Mesh OTA)
                            /         \
                     [Sentry-2]     [Sentry-3]
```

### 1. Cryptographic Signature Verification
*   All firmware update binaries must be cryptographically signed using the Republic's master private key (Ed25519 scheme).
*   The Sentry-1 secure bootloader holds the hardcoded Republic public key. Firmware blocks lacking a verified signature are rejected.

### 2. Mesh-OTA Block Distribution
*   The secure comms relay injects the signed update binary into the nearest mesh anchor node via physical serial or LoRa.
*   The anchor node partitions the binary into 256-byte blocks, broadcasting them over the local ESP-NOW mesh using an incremental block gossip protocol.
*   Nodes verify block hashes incrementally, caching the firmware on their secondary flash partition. Once all blocks are received and verified, the node reboots and executes a safe bootloader rollback check.

---

## 🌉 6. Mesh-to-Backbone Gateway Specification

The Cluster Head bridges the local ESP-NOW mesh to the wider **Republic Class III Comms Relay** using a dual-radio physical translation gateway.

### 1. Physical Hardware Bridge (Sentry-Gate)
*   **Radio Transceiver:** Merges an ESP32-S3 (for ESP-NOW/WiFi) and an SX1262 LoRa module (for long-range backbone backhaul).
*   **Gateway Actuation:** The gateway converts Layer 2 ESP-NOW broadcast alerts into encrypted LoRa packets, utilizing frequency-hopping spread spectrum (FHSS) to bypass WAN interference or localized jamming.

### 2. Packet Translation Protocol
*   Alert payloads are converted from lightweight JSON/binary arrays to securely padded packets:
    $$\text{Payload}_{\text{LoRa}} = \text{AES-256-GCM}_{\text{MeshKey}}(\text{Timestamp} \parallel \text{SourceMAC} \parallel \text{AlertPayload})$$
*   Decryption occurs strictly inside the physical enclave of the Comms Relay.

---

## 🏛️ Epistemic Declaration

> **"The edge is not just a location. It is a jurisdiction. And we are its citizens."**

---
**Status: RATIFIED, COPIED & INDEXED | Anchored to ERA 216.0 | SUBSTRATES HARDENED**
