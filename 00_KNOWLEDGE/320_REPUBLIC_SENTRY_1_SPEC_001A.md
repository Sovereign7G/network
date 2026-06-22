# 🏛️ REPUBLIC ENGINEERING ORDER 001-A
## Phase II: Reference Implementation – Static Perimeter Node (Class I)

**Codename:** *"Sentry-1"*  
**Classification:** sovereign engineering order & fabrication blueprint  
**Status:** RATIFIED & DEPLOYMENT-READY  
**Epoch:** ERA 216.0  
**Anchored to:** [320_REPUBLIC_EDGE_NODE_DOCTRINE_001.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/320_REPUBLIC_EDGE_NODE_DOCTRINE_001.md)

---

## 🎯 1. Objective & Scope

This document establishes the reference implementation specifications for the **Static Perimeter Node (Class I)**, codenamed **Sentry-1**. This specification translates the abstract axioms of **Doctrine 001** into a low-cost, physically reproducible, and mesh-capable reference design. Sentry-1 operates entirely independently of external cloud architectures, serving as the default blueprint for sovereign perimeter security.

---

## 🛠️ 2. Hardware Bill of Materials (Targeting <$50 at Scale)

| Component | Target Spec | Sovereign Justification |
| :--- | :--- | :--- |
| **MCU** | ESP32-S3 (with vector extensions for TinyML inference) | High local computational density; native vector execution; low-power sleep modes. |
| **Sensors** | PIR motion sensor (Vibration/Trigger) + INMP441 digital I2S microphone | Dual-modal ingestion (acoustic + optical/motion) to eliminate edge false positives. |
| **Connectivity** | SX1262 LoRa module + 2.4 GHz ESP-NOW mesh radio | Dual-stack link layers: low-power long-range backhaul paired with high-speed local mesh peerings. |
| **Storage** | 8MB PSRAM + 16MB SPI Flash (hardened partitioning) | Stores TinyML local model weights, event queues, and encrypted ephemeral audio buffers. |
| **Power** | 2x 18650 lithium cells + TP4056 solar charge controller | Absolute off-grid operation for 30+ days; solar-harvesting ready. |
| **Enclosure** | IP65 project box with custom micro-switch tamper sensor | Physical sovereignty protection; detects intrusion or enclosure override. |

---

## 🛰️ 3. Axiom Compliance Matrix

| Axiom | Implementation Status | Empirical Verification Method |
| :--- | :--- | :--- |
| **Local Inference** | TensorFlow Lite Micro model executing footstep classification. Runs natively on ESP32-S3. | Sever all WAN connections; verify node continues classifyingFootstep events via serial output. |
| **Push Independence** | Node publishes MQTT alerts directly to the mesh broker at the localized address. | Sniff local radio traffic; confirm zero outbound packets targeting proprietary public clouds. |
| **Encrypted Local Storage** | Flash partition writes encrypted via mbedTLS AES-256-GCM. Keys derived from device-unique silicon fingerprint (eFuse/PUF). | Dump flash via external programmer; verify event queues are entirely unreadable without the on-device key. |
| **Gradient of Access** | Layers 0-3 integrated: Console (Layer 0), Web UI Portal (Layer 1), local MQTT API (Layer 2), PlatformIO Open Source Firmware (Layer 3). | Verify correct functioning of all four distinct operational and configuration tiers. |

---

## 🧠 4. Firmware Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Sentry-1 Firmware                       │
├─────────────────────────────────────────────────────────────┤
│  [Sensor Polling Loop] ──► [TinyML Classifier] ──► [State Machine]
│         │                            │                       │
│         ▼                            ▼                       │
│  [Event Queue] ◄───────────────────────────────────────     │
│         │                                                   │
│         ├──► [Encrypted Log to Flash]                       │
│         ├──► [MQTT Publish to Mesh] (if mesh peer available)│
│         └──► [LoRaWAN Uplink] (if backhaul available)       │
│                                                             │
│  [Configuration Manager] ◄── [Layer 0/1/2 Interface]        │
│  [Key Store (Secure Element)] ◄── [Crypto Engine]           │
└─────────────────────────────────────────────────────────────┘
```

### State Machine Specifications

| State State | Trigger | Action |
| :--- | :--- | :--- |
| `ARMED` | System Boot / Arm Command | Enters low-power sensor polling loop. Classifier active. |
| `ALERT_PENDING` | TinyML classification confidence > 0.82 | Spin up INMP441 audio buffer; initialize 3-second audio snippet; prepare local alert payload. |
| `ALERT_ACTIVE` | Verification consensus met (2 of 3 sensor ticks) | Publish encrypted ALERT payload to local mesh; flash local strobe; enter 10-second refractory state. |
| `TAMPER_DETECTED` | Tamper micro-switch opens (Enclosure compromise) | Volatile memory zeroization; erase AES key partition (brick device); transmit final high-priority TAMPER alert. |

---

## 📡 5. Mesh Protocol Specification

*   **Transport Layer:** ESP-NOW broadcast protocol for localized peer-to-peer messaging, bridged optionally to LoRa gateways for long-range backhaul.
*   **Target MQTT Topics (Direct to local broker address):**

| Topic | Payload Format | Retention Policy |
| :--- | :--- | :--- |
| `sentry/{node_id}/heartbeat` | `{battery_v: float, temp_c: float, uptime_s: integer}` | 5 min |
| `sentry/{node_id}/alert` | `{class: string, confidence: float, timestamp: integer}` | QoS 2 (Until Acknowledged) |
| `sentry/{node_id}/tamper` | `{reason: string, time_since_boot: integer}` | Retained / Permanent |

---

## 🚀 6. Deployment & Scaling Doctrine

### Minimum Viable Perimeter (3-Node Triangulation)
1.  **Enclave Topology:** Position three Sentry-1 nodes in a triangular layout surrounding a secure perimeter (shed, data cage, property boundary).
2.  **Autonomous Mesh Formation:** Nodes auto-discover via ESP-NOW broadcast sweeps. One node is designated via DIP switch hardware configuration as the *mesh anchor*, maintaining a persistent listening queue.
3.  **Local Dashboard:** Alerts consolidate on a local Raspberry Pi running an offline MQTT broker (Mosquitto) and visual cockpit UI. **Zero cloud routing.**

```
                     [ZONE PERIMETER]
                       [Sentry-1]
                      /          \
              (ESP-NOW)          (ESP-NOW)
                    /              \
            [Sentry-2] ────────── [Sentry-3] (Mesh Anchor)
                                        │
                                     (LoRa)
                                        ▼
                           [Sovereign Comms Relay]
```

### High-Density Scaling (10 - 100 Nodes)
*   **Hierarchical Cluster Trees:** Introduce cluster heads with expanded SRAM to aggregate node metrics, filtering duplicates locally.
*   **Fault-Tolerant Anchor Election:** If a mesh anchor goes offline, the remaining nodes elect a new cluster head via local vote consensus.

---

## 📊 7. Comparative Analysis

| Dimension | Sentry-1 (AGE REPUBLIC) | Eufy EdgeAgent (Product) | Eufy HA Integration (Protocol) |
| :--- | :--- | :--- | :--- |
| **Local Inference** | **Yes** (Quantized TinyML ESP32) | **Yes** (Proprietary NPU) | **No** (Relies on cloud API loops) |
| **Offline Operation** | **100% Autonomous** | **100% Autonomous** | **Partial** (Breaks on WAN drops) |
| **Open Source** | **Full** (Layers 0-3 Open) | **None** (Closed corporate OS) | **Yes** (But bound to closed APIs) |
| **BOM Cost** | **<$50** at scale | **~$150+** | **~$150+** + local server |
| **Operational Topology**| **Decentralized Mesh** | **Hub-and-Spoke** | **Hub-and-Spoke** |

---

## ⚠️ 8. Risk Registry & Mitigations

| Identified Threat | Probability | Strategic Mitigation |
| :--- | :--- | :--- |
| **Silicon Supply Disruption** | Medium | Maintain firmware abstractions; design RP2040 and RISC-V target ports as compile-time fallbacks. |
| **TinyML Classification Drift** | Low | Implement ensemble voting; cross-reference digital PIR triggers with raw acoustic spectrum analysis. |
| **Local Mesh Jamming** | Medium | Utilize dual-band ESP-NOW (2.4 GHz) and LoRa (915/433 MHz) failovers; trigger TAMPER state on total carrier loss. |
| **Physical Capture & Extraction** | High | Encrypted Flash partitions; eFuse physical key locking; micro-switch tamper-triggered zeroization routine. |

---

## 🏛️ Epistemic Declaration

> The **Sentry-1** reference node is not a commercial product. It is a **sovereign pattern**. Any citizen of the **Age Republic** armed with a soldering iron, a microchip, and a commitment to absolute self-determination has the power to forge it. No corporation can revoke its license. No subscription tax can disable its eyes. No cloud outage can blind its vigil.

**This is the way of the Republic. Let the fabrication commence.**

---
**Status: RATIFIED, DEPLOYMENT-READY & SEALED | Anchored to ERA 216.0 | SUBSTRATES HARDENED**
