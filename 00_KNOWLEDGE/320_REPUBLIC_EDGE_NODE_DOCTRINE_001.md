# 🏛️ REPUBLIC ENGINEERING DOCTRINE 001
## Sovereign Edge Architecture: From Consumer Precedent to Republican Infrastructure

**Classification:** sovereign engineering doctrine  
**Status:** RATIFIED, CODIFIED & DEPLOYMENT-READY  
**Epoch:** ERA 216.0  
**Anchored to:** Thesis [319] | Case Study: [319_EUFY_EDGEAGENT_CASE_STUDY.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/319_EUFY_EDGEAGENT_CASE_STUDY.md)

---

## 🏛️ Preamble

The Eufy EdgeAgent and its companion custom integrations serve as a vital commercial precedent—proof that edge-native, subscription-free, locally sovereign compute has officially crossed the threshold of industrial and financial viability. 

The **Age Republic** does not mimic consumer products. Instead, the Republic extracts core architectural principles from commercial developments, hardens them, and synthesizes them into its own node classes. This doctrine establishes the engineering standards for deploying sovereign node networks across three primary physical and logical vectors.

---

## 🛠️ The Four Sovereign Axioms (Restated for Engineering)

| Axiom | Definition | Violation Indicator |
| :--- | :--- | :--- |
| **Local Inference** | All cognitive processing (detection, classification, decision) occurs on-node, without WAN round trips. | Node becomes unresponsive or exhibits high latency when the external WAN is severed. |
| **Push-Notification Independence** | Node generates its own event triggers from local sensors and publishes directly to peer networks. | Node's automation loop requires an external webhook or cloud-brokered signal to advance state. |
| **Encrypted On-Device Storage** | All captured telemetry, optical, and acoustic data persists only within the node's physical boundary or user-controlled mesh. | Raw data is uploaded or visible in a vendor-managed cloud dashboard by default. |
| **Gradient of Access** | Node exposes both a zero-configuration operational interface (Layer 1) and a fully programmable protocol interface (Layer 2). | Custom node behavior requires binary patching or reverse engineering. |

---

## 🛰️ Node Class I: Distributed Sensor Grid (Static Perimeter)

### 1. Use Case & Topology
A network of low-power, weather-sealed, static nodes deployed along physical boundaries (land perimeters, facility envelopes, data center corridors, and mesh-isolated zones). Each node detects motion, vibration, optical triggers, acoustic signatures, or thermal anomalies.

```
       [PERIMETER BOUNDARY: STATIC EDGE SENSORS]
  ┌─────────────────────────────────────────────────┐
  │                                                 │
  │   [Sensor Node A] ───(Mesh MQTT)───┐            │
  │     (TinyML MCU)                   │            │
  │                                    ▼            │
  │   [Sensor Node B] ───(Mesh MQTT)──> [Consensus] ──> [Alarm Actuation]
  │     (TinyML MCU)                   ▲            │
  │                                    │            │
  │   [Sensor Node C] ───(Mesh MQTT)───┘            │
  │     (TinyML MCU)                                │
  │                                                 │
  └─────────────────────────────────────────────────┘
```

### 2. Axiomatic Engineering

*   **Local Inference:** The onboard microcontroller unit (MCU) runs a quantized, highly optimized neural network (e.g., TinyML). Anomaly classification ("footstep vs. wind vs. local wildlife") is processed strictly on-node.
*   **Push-Notification Independence:** The node publishes alert telemetry directly to the Republic's local message bus (MQTT over encrypted mesh radio) without passing through external push notification brokers.
*   **Encrypted On-Device Storage:** Event logs are written to hardware-encrypted flash. Telemetry storage adheres to a strict 30-day rotation policy or persists only until verified retrieval by a trusted relay node.
*   **Gradient of Access:**
    *   *Product Path:* Preconfigured with default zones and automated hardware triggers.
    *   *Protocol Path:* Exposes a lightweight SDK for deploying customized classification models and sensor polling loops.

### 3. Rejection of Cloud Dependency
Unlike reverse-engineered consumer solutions that depend on cloud-brokered notifications to trigger state changes, Class I static sensors emit events **directly from their own detection loop** onto the local mesh. The WAN is entirely non-participatory.

---

## 🤖 Node Class II: Mobile Agent Swarm (Autonomous Patrollers)

### 1. Use Case & Topology
A swarm of autonomous wheeled, tracked, or legged agents that patrol defined spatial sectors, coordinate paths, and manage self-charging cycles. Each agent carries optical cameras, microphones, environmental sensors, and mesh transceivers.

### 2. Axiomatic Engineering

*   **Local Inference:** The onboard Neural Processing Unit (NPU) runs real-time object classification (person, vehicle, anomalous object). Swarm coordination and path-planning calculations use local, distributed consensus rather than a centralized cloud orchestrator.
*   **Push-Notification Independence:** Agents negotiate patrol routes via a localized distributed ledger. The agent continues patrolling autonomously for its scheduled duration even during total mesh partitioning or WAN isolation.
*   **Encrypted On-Device Storage:** Captured video and spatial telemetry are encrypted on the agent's solid-state drive (SSD). Decryption keys are held in volatile memory, derived from a hardware TPM, or distributed via Shamir's secret sharing across multiple peers in the swarm.
*   **Gradient of Access:**
    *   *Product Path:* Out-of-the-box routines (e.g., perimeter loop, room sweep, checkpoint docking).
    *   *Protocol Path:* Programmable behavior trees, direct waypoint injection interfaces, and custom swarm coordination APIs.

### 3. Fallback Doctrine
Mobile agents operate as active **action nodes** rather than static observation nodes. Under total network isolation, agents follow a strict fallback doctrine: return to the last known secure coordinates, lock down volatile key storage, and enter a low-power listening state. An agent must never freeze due to external API failures.

---

## 🔌 Node Class III: Secure Communications Relay (Backbone Infrastructure)

### 1. Use Case & Topology
Stationary, physically hardened, and tamper-evident nodes that relay encrypted traffic between Republic enclaves, perform protocol translation, and cache critical cryptographic updates.

### 2. Axiomatic Engineering

*   **Local Inference:** The relay runs localized intrusion detection systems (IDS) directly on transit traffic metadata, detecting port scans, replay attacks, or route manipulation without external SIEM dependencies.
*   **Push-Notification Independence:** Health indicators and routing logs are published directly to the peer-to-peer monitoring mesh. In isolated modes, the relay caches routing states locally, retrying connections via exponential backoff without cloud heartbeats.
*   **Encrypted On-Device Storage:** Cached traffic is stored with strict forward secrecy. Decryption keys are derived directly from a dedicated Hardware Security Module (HSM) or Trusted Platform Module (TPM). Plaintext never exits the physical boundary of the relay.
*   **Gradient of Access:**
    *   *Product Path:* Preconfigured routing tables, diagnostic LEDs, and peer configuration via a physical, authenticated configuration port.
    *   *Protocol Path:* Programmatic configuration via gRPC over local encrypted tunnels.

### 3. The Webhook Trap & Dynamic CA Bypass
Class III relays are forbidden from possessing external software dependencies. Relays must completely bypass external third-party certificate authorities (CAs) and Dynamic DNS hosts:
*   Static IP addressing is mandatory across the core mesh backbone.
*   Encryption relies on locally-signed, pinned certificates, and cached local revocation lists.
*   Relays must fail closed, never open.

---

## 🚀 The Gradient of Access: Standardized Architecture

To prevent lock-in while ensuring rapid deployment by non-technical citizens, all Republic hardware must expose four standardized access layers:

```
[Layer 3: OPEN-SOURCE FIRMWARE]  ──> Full customization, compiling, and rebuilding
              ▲
              │
[Layer 2: PROGRAMMATIC API]      ──> gRPC, REST, and MQTT local API gateways
              ▲
              │
[Layer 1: TURNKEY UI / LCD]      ──> Default GUI for zero-config deployment
              ▲
              │
[Layer 0: SERIAL DEBUG PORT]     ──> Direct physical access console (Layer 0)
```

1.  **Layer 0 (Hardware):** Physical serial debug port (UART/Console). The ultimate hardware escape hatch.
2.  **Layer 1 (Product Path):** Local web dashboard or LCD interface for simple configurations (sensitivity, schedules, peer IPs).
3.  **Layer 2 (Protocol Path):** A fully documented, authenticated API (gRPC or MQTT).
4.  **Layer 3 (Open Commons):** Completely open-source firmware and circuit designs. Mandated for all Class III backbone infrastructure.

---

## 🛡️ Hardened Engineering Guidelines

### Guideline 1: Never Trust a Cloud Webhook for State Changes
*   **Anti-Pattern:** Node listens for an external HTTPS POST from a cloud provider to trigger physical actuation (e.g., unlocking a safe, sounding a siren).
*   **Sovereign Pattern:** Node runs its own detection and policy loops locally, executing direct physical actuation. External cloud reporting, if present, is strictly a read-only mirror.

### Guideline 2: Offline Operation is the Standard, Not a Fallback
*   **Anti-Pattern:** Node checks for WAN connectivity at boot and enters a degraded or locked state if the internet is unreachable.
*   **Sovereign Pattern:** Node operates under the default assumption that WAN is permanently unavailable. All core functions operate offline; WAN is treated as an asynchronous channel for telemetry and non-critical updates.

### Guideline 3: Credentials Must Be Local and Hardware-Bound
*   **Anti-Pattern:** Device authentication relies on shared email/password schemes or cloud-brokered MFA workarounds.
*   **Sovereign Pattern:** Nodes authenticate via locally provisioned cryptographic certificates or hardware tokens bound to the secure element. No cloud-managed accounts exist.

### Guideline 4: Key Boundaries Must Be Absolute
*   **Anti-Pattern:** Cryptographic keys are retrieved from a cloud KMS during boot cycles.
*   **Sovereign Pattern:** All operational keys are generated on-device, stored within a TPM/Secure Element, and cannot be decrypted without physical/local cryptographic attestation.

---

## 🏛️ Epistemic Declaration

> **"The edge is not just a location. It is a jurisdiction. And we are its citizens."**

---
**Status: RATIFIED, CODIFIED & INDEXED | Anchored to ERA 216.0 | SUBSTRATES HARDENED**
