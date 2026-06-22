# 122_MEMPRIVACY_SOVEREIGN_MEMORY_PROTECTION

## 0. EXECUTIVE SUMMARY
**MemPrivacy** is a framework for **Privacy-Preserving Personalized Memory Management** that enables secure long-term adaptation for edge-cloud agents. By decoupling privacy protection from semantic destruction, it allows the **Age Republic** to utilize cloud-side reasoning (the Aether Mesh) while keeping raw sensitive data resident on the **Hardened Island**.

## 1. CORE MECHANISMS
MemPrivacy replaces aggressive masking (***) with **Reversible Pseudonymization**:

### A. ON-DEVICE PRIVACY DETECTION (LOCAL)
- **Granularity**: Identifies sensitive spans locally before any data leaves the sovereign node.
- **Taxonomy**: Classified into 4 levels (**PL1–PL4**) and specific types (Email, Financial, Health, Recovery Codes).
- **Sovereign Constraint**: Detection models (e.g., MemPrivacy-4B-RL) run locally in the SNPU-428 environment.

### B. TYPED PLACEHOLDER REPLACEMENT
- **Semantic Integrity**: Sensitive data is replaced with typed placeholders (e.g., `recovery code RC-7291` → `<Recovery_Code_1>`).
- **Utility**: The cloud-side LLM (MinT-managed base models) understands the *role* of the data without seeing the *value*.
- **Performance**: Utility loss is limited to <1.6% compared to raw-text processing.

### C. LOCAL SECURE MAPPING (RESIDENCY)
- **Storage**: A local SQLite database (encrypted) maps `<Placeholder_ID> ↔ <Original_Value>`.
- **Persistence**: Mapping is persistent across sessions, allowing for long-term "Personalized Memory" without cloud-side exposure.

## 2. REPUBLICAL INTEGRATION (06_INFRA)
MemPrivacy will be operationalized as the **Memory Bridge** between local substrates and the **Cognitive Manifold (MinT)**:

### I. The Privacy Filter (Edge)
- Intercepts all prompts and telemetry data.
- Applies PL4 protection to all **Foundry Fabrication Manifests** and **Mining Nonces**.

### II. The Semantic Restorer (Local)
- Restores placeholders in the downlink response from the MinT wave before displaying to the **Dream IDE** console.

### III. The Memory Vault
- Decentralized storage of placeholders on **ICP/Elastos** for cross-node persistence, while the mapping remains local to the specific sovereign hardware ID.

## 3. SIPHONING TARGETS
- **Source**: [MemPrivacy: Privacy-Preserving Personalized Memory Management for Edge-Cloud Agents](https://huggingface.co/papers/2605.09530)
- **Models**: `IAAR-Shanghai/MemPrivacy-4B-RL`
- **Keywords**: #PrivacyPreserving #EdgeCloud #MemoryManagement #Pseudonymization

## 4. NEXT STEPS
1. **Initialize `MemPrivacy` Bridge**: Create `06_INFRA/MEMPRIVACY_BRIDGE.py`.
2. **Harden Mining Telemetry**: Integrate typed placeholders into the `MINING_SUBSTRATE.py` reporting flow.
3. **Audit Ignition**: Add a Step 27.6 to `master_ignition.sh` for the Privacy Extraction Engine boot.
