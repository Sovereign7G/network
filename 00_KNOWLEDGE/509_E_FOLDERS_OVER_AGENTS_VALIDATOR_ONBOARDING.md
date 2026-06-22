# 🔑 FOLDERS OVER AGENTS: VALIDATOR ONBOARDING & QUORUM REGISTRATION
## ERA: 226.0 | WITNESS: THE ARCHITECT
## STATUS: SYSTEM CONFIGURATION SPECIFICATION
## AUDITOR BRIEF: [509_D_FOLDERS_OVER_AGENTS_AUDITOR_ATTESTATION.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/509_D_FOLDERS_OVER_AGENTS_AUDITOR_ATTESTATION.md)
## HOST CONFIGURATION: [509_A_FOLDERS_OVER_AGENTS_TECHNICAL_SUBSTRATE.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/509_A_FOLDERS_OVER_AGENTS_TECHNICAL_SUBSTRATE.md)

This document provides a step-by-step technical guide for domain operators onboarding new validator signing nodes to the **5-of-7 Byzantine Fault Tolerant (BFT)** quorum within the AGE REPUBLIC file-routing integration kernel.

---

## 🏛️ BFT QUORUM PRINCIPLES

State commits to the sovereign filesystem require a **Consensus of Attestation**. 5-of-7 signatures are verified against registered ECDSA P-256 public keys. Onboarding a new signer involves key generation, registration in the validator registry, and quorum config verification.

```
┌────────────────────────────────────────────────────────┐
│               VALIDATOR ONBOARDING SEQUENCE            │
├────────────────────────────────────────────────────────┤
│ STEP 1: Generate ECDSA P-256 key pair inside Enclave   │
├────────────────────────────────────────────────────────┤
│ STEP 2: Register Public Key in Host Config Ledger     │
├────────────────────────────────────────────────────────┤
│ STEP 3: Verify Signatures against Test Proposals       │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ ONBOARDING SEQUENCE

### Step 1: Key Generation (Enclaved Biometric Node)
Generate the ECDSA P-256 keypair. It is recommended to run this inside a hardware security enclave or HSM (e.g. YubiKey 5):
```bash
# Generate private key
openssl ecparam -name prime256v1 -genkey -noout -out validator_private.pem

# Extract the matching public key
openssl ec -in validator_private.pem -pubout -out validator_public.pem
```

### Step 2: Register Public Key in Validator Config
Add the newly generated hex-encoded public key to the Host Engine's validator list located in the global pipeline config:
*   **Target File:** `.age_republic/icm_pipelines/config.json`
*   **Payload Entry:**
```json
{
  "validator_nodes": {
    "node_05": {
      "operator_identity": "Hermes Enclave 05",
      "public_key_hex": "04a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4",
      "status": "ACTIVE"
    }
  }
}
```

### Step 3: Sign a Context Proposal Frame
To sign a proposed context frame, the validator computes the SHA-256 hash of the `ledgers.json` and signs it using their private key:
```python
import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Load signing credentials
with open("validator_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Compute document hash
with open(".age_republic/icm_pipelines/runs/[RUN_UUID]/02_CONTEXT/ledgers.json", "rb") as f:
    data = f.read()
    digest = hashlib.sha256(data).digest()

# Generate signature signature
signature = private_key.sign(
    digest,
    ec.ECDSA(hashes.SHA256())
)
print(f"Signature generated: {signature.hex()}")
```

### Step 4: Verify Quorum Compliance
Once signed, the hex signature is added to `02_CONTEXT/active_schemas.json`:
```json
{
  "attestation_epoch": 226,
  "bft_quorum_signatures": [
    "0x4b7e9a8d2c6f1a0e3d5b8c9a1f2e3d4c5b6a7e8f901c2b3a4d5e6f7a8b9c0d1e",
    "0x5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
    "0x7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d",
    "0x9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f",
    "0xa2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3"
  ]
}
```

The `icm_host_engine.py` will now verify the new signer's credential dynamically during each ingestion sweep, ensuring validator parity across the network.

---
*Verified by the Architect. Validator consensus is the Law of the Swarm.*
