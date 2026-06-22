# 🏛️ KNOWLEDGE ITEM: 322 — SOVEREIGN SMART CONTRACT API KEY ACQUISITION
## ERA 225 · DECENTRALIZED IDENTITY & KDF KEY RECOVERY

---

## 🗺️ EXECUTIVE SUMMARY & SYSTEM CONFLICTS

Sovereign agentic enclaves operating off-grid require absolute architectural independence from centralized cloud registries and static plaintext environment configurations. Storing sensitive API credentials (such as OpenAI authorization seeds) in plaintext configuration files poses severe security risks and prevents automated, multi-node rotation.

This document chronicles the brainstormed solutions, multi-tier blockchain integration pathways, and client-side execution parameters to acquire, decrypt, and rotate API credentials utilizing smart contracts on-chain.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            DECENTRALIZED API KEY ACQUISITION PARADIGM                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│   [1. ON-CHAIN STORE]       ────►   DeadVault Encrypted Secrets / LIT Protocol TEE Enclaves         │
│                                     *Free to read; cryptographically locked by wallet*             │
│                                                                                                     │
│   [2. CLIENT KDF LAYER]     ────►   Wallet Signature + Master Password derives PBKDF2 AES-GCM Key   │
│                                     *Decryption happens entirely client-side (no leakage)*           │
│                                                                                                     │
│   [3. ORACLE INTEGRATION]   ────►   Chainlink Functions executes LLM calls inside DON Enclaves      │
│                                                                                                     │
│   [4. NATIVE PROXY BYPASS]  ────►   Zero-Key Proxy intercepts 'sk-...' checks, routing to local     │
│                                     Ollama streams in 0ms                                           │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ SOLUTION ARCHITECTURES & PATTERNS

### Approach 1: Decentralized Secret Store (DeadVault)
Encrypted client-side secrets are stored as raw bytecode inside a mainnet EVM registry. Secrets are fully encrypted prior to on-chain propagation using AES-256-GCM.

* **Key Derivation Function (KDF):** PBKDF2 (720,000 iterations).
* **Cryptographic Locks:** Requires client signature generated via the agent's active private key.
* **Base Mainnet Registry Address:** `0xF74C1131E11aF8dc10F25bAa977dD0B86d4A5C37`
* **Arbitrum Mainnet Registry Address:** `0x33939ede1A19A64EE755F1B5B3284A8E71F68484`

```typescript
import { DeadVault, privateKeyToAccount } from "@deadvault/sdk";

const account = privateKeyToAccount("0xYourPrivateKey");
const vault = new DeadVault({ chain: "base" });

// Perform client-side decryption on acquired bytecode
const data = await vault.read({
  address: account.address,
  password: "your-master-password",
  walletSignature: sig,
});
```

---

### Approach 2: Pay-Per-Use Escrow Marketplaces (Soho/ServiceNet)
Allows the agent to consume API gateways without maintaining any static API keys, replacing accounts with state-channel crypto micropayments.

* **Micropayment Escrow:** Yellow Network state channels.
* **On-Chain Footprint:** Initial USDC escrow lock + settlement, per-call zero-gas state signatures.
* **Delivery Vector:** Credentials delivered dynamically via encrypted XMTP envelopes.

---

### Approach 3: Chainlink Functions + DON-Hosted Secrets
The smart contract delegates execution directly to a Decentralized Oracle Network (DON). The API credentials are encrypted with the DON's public key and decrypted strictly within secure sandbox nodes during request execution.

```javascript
// Sandboxed Execution Script (Executed within DON)
const apiKey = secrets.apiKey;
const response = await Functions.makeHttpRequest({
  url: "https://api.openai.com/v1/completions",
  headers: { "Authorization": `Bearer ${apiKey}` },
  data: { model: "gpt-3.5-turbo", prompt: args[0] }
});
return Functions.encodeString(response.data.choices[0].text);
```

---

### Approach 4: Lit Protocol TEE Enclave Execution
Leverages Trusted Execution Environments (TEEs) in a decentralized node network to derive signing keys and execute JavaScript Lit Actions without disclosing the underlying credentials to the host environment.

* **Enclave Security:** AMD SEV-SNP / Intel SGX hardware attestation.
* **Condition Engine:** Token/NFT ownership, cryptographic challenge proofs.

---

## 🛠️ THE NATIVE COCKPIT PROXY BYPASS (API KEY ELIMINATION)

Under off-grid operations where no outbound WAN connection exists, the IDE’s strict "API key required" client check can be fully satisfied locally via a lightweight, zero-configuration proxy. The proxy acts as a transparent loopback that intercepts any string structured as an API key (`sk-...`) and translates requests directly into native Ollama streams.

```
┌─────────────┐             ┌─────────────┐             ┌─────────────┐
│   Zed IDE   │ ──(sk-...)─►│ Local Proxy │ ──(No Key)─►│ Local LLM   │
│  Assistant  │             │ (Port 9877) │             │ (Port 11434)│
└─────────────┘             └─────────────┘             └─────────────┘
```

#### Proxy Implementation Block:
```python
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    headers = dict(request.headers)
    body = await request.json()
    
    # Strip incoming authorization headers (Zed's sk-... placeholder)
    headers.pop("authorization", None)
    
    # Convert OpenAI standard format to Ollama completions payload
    ollama_payload = {
        "model": "gemma2:2b",
        "messages": body.get("messages", []),
        "stream": body.get("stream", True)
    }
    
    async def stream_generator():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", 
                "http://localhost:11434/v1/chat/completions", 
                json=ollama_payload,
                timeout=60.0
            ) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
```

---

## 📊 CORE PROTOCOL MATRIX

| Vector | Decentralization Tier | Setup Overhead | Gas Requirements | Decryption Scope |
| :--- | :--- | :--- | :--- | :--- |
| **DeadVault** | High (Base EVM) | Minimal (SDK Call) | One-time storage gas | Client-Side (AES-GCM) |
| **ServiceNet** | Medium (Micropayments)| Complex (State channels) | Variable (Settlement only) | Transient (XMTP) |
| **Chainlink** | High (DON Oracle) | Moderate (Subscription) | High (LINK Execution) | Node Sandboxes |
| **Lit Protocol**| High (TEE Enclaves)| Moderate (Lit Actions) | Minimal | hardware TEE |
| **Local Proxy** | Absolute (Off-Grid) | Zero (FastAPI script) | Zero (Gas-Free) | Bypass (Discard Key) |
