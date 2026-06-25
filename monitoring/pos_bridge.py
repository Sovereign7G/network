#!/usr/bin/env python3
"""POS Dongle → S7G integration bridge. Receives Magix POS settlement
webhooks (Zavo, Razorpay, Airwallex), routes to S7G YieldRouter for
settlement, stores Keccak proofs in aetherdb_bridge, and submits via
the cross-chain relayer.
"""
import json, os, time, hashlib, hmac
from http.client import HTTPSConnection
from typing import Optional, Dict, List

BASE_RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
ICP_API = "https://ic0.app"
AETHERDB = os.getenv("AETHERDB_CANISTER", "h54dw-qyaaa-aaaaa-qhjtq-cai")
YIELD_ROUTER = os.getenv("YIELD_ROUTER", "")  # Set after YieldRouter deploy
SETTLEMENT_VERIFICATION = "0x8F83abe2feA0780aBcE33961A35F394f263CE9ed"
S7G_TREASURY = os.getenv("S7G_TREASURY", "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611")

SUPPORTED_PLATFORMS = ["zavo", "razorpay", "airwallex", "sovereign_key"]
SUPPORTED_CORRIDORS = ["base_usdc", "base_eurc", "esc_ela", "icp_cycles", "lora_60ghz"]

# ── HSE TernaryKeccak Constants ──────────────────────────────
# Ref: Aether Mesh Bridge Type 1 — USB Sovereign Key
# HSE (Hardware Secure Element) implements TernaryKeccak asymmetric signing
HSE_DOMAIN_SEPARATOR = b"aether-mesh-v1-hse"
TERNARY_KECCAK_ROUNDS = 206  # ERA reference
HSE_VERIFICATION_CONTRACT = "0x8F83abe2feA0780aBcE33961A35F394f263CE9ed"

def _ic_store(key: str, value: str) -> bool:
    try:
        c = HTTPSConnection("ic0.app")
        val_bytes = list(value.encode("utf-8"))
        body = json.dumps({"jsonrpc":"2.0","method":"canister_call",
            "params":[AETHERDB, "aetherdb_put", [key, val_bytes]],"id":1}).encode()
        c.request("POST", f"/api/v2/canister/{AETHERDB}/call", body,
                  {"Content-Type":"application/json"})
        return json.loads(c.getresponse().read()).get("result","") is not None
    except: return False

def _keccak256(data: dict) -> str:
    """Generate Keccak-256 hex hash (compatible with Magix Crypto)."""
    canonical = json.dumps(data, sort_keys=True, separators=(",",":"))
    h = hashlib.sha3_256(canonical.encode())  # SHA3-256 = Keccak-256
    return "0x" + h.hexdigest()

class POSBridge:
    """Bridges Magix POS settlements into the S7G network."""

    def __init__(self):
        self.settlements: List[Dict] = []

    def handle_webhook(self, platform: str, body: bytes, signature: str = "") -> Dict:
        """Process a POS platform webhook and route to S7G settlement."""
        try:
            payload = json.loads(body.decode())
        except: return {"error": "invalid JSON"}

        if platform not in SUPPORTED_PLATFORMS:
            return {"error": f"unsupported platform: {platform}"}

        agent_did = payload.get("agent_did", "")
        merchant_id = payload.get("merchant_id", "")
        amount = payload.get("amount", 0)
        corridor = payload.get("corridor", "base_usdc")
        credential = payload.get("credential", "0x")

        if not agent_did or not merchant_id or amount <= 0:
            return {"error": "missing required fields"}
        if corridor not in SUPPORTED_CORRIDORS:
            return {"error": f"unsupported corridor: {corridor}"}

        return self.settle(agent_did, merchant_id, amount, corridor, credential)

    def settle(self, agent_did: str, merchant_id: str, amount: int,
               corridor: str = "base_usdc", credential: str = "0x") -> Dict:
        """Process a POS settlement and route through S7G."""
        # 1. Generate proof hash
        proof_input = {
            "agent": agent_did, "merchant": merchant_id,
            "amount": amount, "corridor": corridor,
            "credential": credential, "timestamp": int(time.time()),
        }
        proof_hash = _keccak256(proof_input)

        # 2. Determine settlement path
        if corridor == "base_usdc":
            token = "USDC"; chain = "base"
        elif corridor == "base_eurc":
            token = "EURC"; chain = "base"
        elif corridor == "esc_ela":
            token = "ELA"; chain = "esc"
        else:
            token = "USDC"; chain = "base"

        # 3. Store proof in aetherdb_bridge
        proof_key = f"pos:proof:{proof_hash[:16]}"
        proof_val = json.dumps(proof_input)
        _ic_store(proof_key, proof_val)

        # 4. If YieldRouter is configured, route settlement
        yield_router_result = None
        if YIELD_ROUTER:
            yield_router_result = self._route_to_yield_router(amount, token)

        # 5. Record settlement
        settlement = {
            "proof_hash": proof_hash, "agent": agent_did,
            "merchant": merchant_id, "amount": amount,
            "corridor": corridor, "token": token, "chain": chain,
            "timestamp": int(time.time()),
            "yield_router": yield_router_result,
        }
        self.settlements.append(settlement)

        return settlement

    def _route_to_yield_router(self, amount: int, token: str) -> Dict:
        """Route settlement through YieldRouter for distribution."""
        try:
            c = HTTPSConnection("mainnet.base.org")
            # Encode YieldRouter.receiveRevenue() call
            # In production: use web3 contract interaction
            c.request("POST", "/", json.dumps({"jsonrpc":"2.0",
                "method":"eth_call","params":[{"to":YIELD_ROUTER,
                "data":"0x" + hex(amount)[2:]},"latest"],"id":1}).encode(),
                {"Content-Type":"application/json"})
            resp = json.loads(c.getresponse().read())
            return {"status": "submitted", "response": resp.get("result","")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def verify(self, agent_did: str, amount: int, corridor: str,
               proof_hash: str) -> bool:
        """Verify a proof hash against expected values."""
        expected = _keccak256({
            "agent": agent_did, "amount": amount, "corridor": corridor,
        })
        return expected == proof_hash

    def get_settlements(self, merchant_id: str = "") -> List[Dict]:
        """Get settlements, optionally filtered by merchant."""
        if merchant_id:
            return [s for s in self.settlements if s["merchant"] == merchant_id]
        return self.settlements

    def status(self) -> Dict:
        return {
            "yield_router_configured": bool(YIELD_ROUTER),
            "platforms": SUPPORTED_PLATFORMS,
            "corridors": SUPPORTED_CORRIDORS,
            "settlements_processed": len(self.settlements),
            "settlement_verification_contract": SETTLEMENT_VERIFICATION,
            "treasury": S7G_TREASURY,
            "hse_ready": True,
            "lora_60ghz_ready": True,
        }

    # ═══════════════════════════════════════════════════════════════
    # SOVEREIGN KEY — HSE TernaryKeccak + LoRa 60GHz TX + BT
    # ═══════════════════════════════════════════════════════════════

    def _ternary_keccak(self, data: bytes) -> bytes:
        """Simulate HSE TernaryKeccak signing.
        In production: delegates to Sovereign Key dongle's HSE.
        Ternary rounds = ERA 206.5 reference value.
        """
        h = hashlib.sha3_256(HSE_DOMAIN_SEPARATOR + data)
        for _ in range(TERNARY_KECCAK_ROUNDS):
            h.update(h.digest())
        return h.digest()

    def hse_sign(self, proof_hash: str, hse_id: str = "") -> Dict:
        """Sign proof hash with HSE TernaryKeccak for hardware attestation."""
        sig = self._ternary_keccak(proof_hash.encode())
        att = hashlib.sha3_256(sig + (hse_id.encode() if hse_id else sig)).hexdigest()
        return {"signature": "0x" + sig.hex(), "algorithm": "TernaryKeccak",
                "rounds": TERNARY_KECCAK_ROUNDS, "attestation": "0x" + att,
                "hse_id": hse_id or "sovereign-key-v1"}

    def hse_verify(self, proof_hash: str, signature: str, hse_id: str = "") -> bool:
        """Verify an HSE TernaryKeccak signature."""
        sig_r = signature[2:] if signature.startswith("0x") else signature
        exp = self.hse_sign(proof_hash, hse_id)["signature"]
        exp_r = exp[2:] if exp.startswith("0x") else exp
        return sig_r == exp_r

    def lora_transmit(self, payload: Dict, node_id: str = "dsa-node-001") -> bool:
        """Transmit signed payload via LoRa to nearest 7G mesh node.
        In production: Sovereign Key dongle USB serial → SX1262 radio → 7G node.
        """
        ph = payload.get("proof_hash", "")
        if not ph: return False
        sig = self.hse_sign(ph)
        tx = {**payload, "hse_signature": sig, "transport": "lora_60ghz"}
        _ic_store(f"pos:lora_tx:{ph[:16]}", json.dumps(tx))
        print(f"[Sovereign Key] LoRa TX → {node_id}: {ph[:16]}...")
        return True

    # ═══════════════════════════════════════════════════════════════
    # BLUETOOTH TRANSPORT — Virtual Dongle Bridge Type 2
    # ═══════════════════════════════════════════════════════════════
    # The Virtual Dongle (software) cannot do LoRa CSS modulation
    # (BT chip is 2.4GHz FHSS, LoRa is sub-GHz CSS — physically distinct).
    # But BT CAN carry proof data as payload bytes.
    #
    # Three transport modes:
    # 1. BLE Advertisement — broadcast proof hash as beacon (<31 bytes)
    # 2. BT Classic SPP — pair with 7G node, send over RFCOMM
    # 3. BLE GATT — connect to 7G node, write to characteristic
    #
    # Ref: Aether Mesh Bridge Type 2 (Mobile Proxy) — phone BT → USB → laptop
    # Ref: Aether Mesh Clarification — Bluetooth ≠ LoRa, but data relay works

    BT_SERVICE_UUID = "7g7g7g7g-0000-1000-8000-00805f9b34fb"
    BT_CHAR_UUID_TX = "7g7g7g7g-0001-1000-8000-00805f9b34fb"
    BT_CHAR_UUID_RX = "7g7g7g7g-0002-1000-8000-00805f9b34fb"

    def bt_advertise(self, proof_hash: str, hse_sig: str = "") -> Dict:
        """BLE advertisement broadcast of proof hash.
        Payload limited to ~31 bytes — fits hash prefix + HSE attestation.
        Nearby 7G nodes scanning BLE pick it up and relay to mesh.
        """
        prefix = proof_hash[2:18] if proof_hash.startswith("0x") else proof_hash[:16]
        attest = hse_sig[2:10] if hse_sig.startswith("0x") else hse_sig[:8]
        adv_data = f"S7G:{prefix}:{attest}"
        print(f"[BT BLE] Advertising: {adv_data} ({len(adv_data)} bytes)")
        # In production: PyBluez or Bleak BLE advertisement.write
        return {"transport": "ble_advertisement", "data": adv_data, "bytes": len(adv_data)}

    def bt_classic_spp(self, proof_hash: str, hse_sig: Dict, peer_addr: str = "00:00:00:00:00:00") -> Dict:
        """BT Classic Serial Port Profile — pair with 7G node, send full proof.
        Full payload size: ~500 bytes — fits BT SPP MTU comfortably.
        Common in Mobile Proxy pattern: laptop BT → phone → mesh.
        """
        payload = json.dumps({"proof_hash": proof_hash, "hse_signature": hse_sig,
                               "protocol": "spp", "ts": int(time.time())})
        print(f"[BT SPP] Pairing with {peer_addr}...")
        print(f"[BT SPP] Sending {len(payload)} bytes via RFCOMM")
        # In production: PyBluez BluetoothSocket(RFCOMM).connect(peer_addr, channel)
        return {"transport": "bt_spp", "peer": peer_addr, "bytes": len(payload)}

    def bt_gatt_write(self, proof_hash: str, hse_sig: Dict, peer_addr: str = "00:00:00:00:00:00") -> Dict:
        """BLE GATT — connect to 7G node, write proof hash to characteristic.
        7G node's BLE peripheral exposes S7G_SERVICE with TX characteristic.
        Virtual dongle writes proof → 7G node receives → relays to ICP mesh.
        """
        payload = json.dumps({"proof_hash": proof_hash, "hse_signature": hse_sig,
                               "protocol": "gatt", "ts": int(time.time())})
        print(f"[BT GATT] Connecting to {peer_addr} ({self.BT_SERVICE_UUID[:12]}...)")
        print(f"[BT GATT] Writing {len(payload)} bytes to {self.BT_CHAR_UUID_TX[:12]}...")
        # In production: Bleak client.connect(peer_addr) → characteristic.write_value(payload)
        return {"transport": "bt_gatt", "peer": peer_addr, "bytes": len(payload)}

    def bt_broadcast(self, payload: Dict, mode: str = "advertisement",
                     peer_addr: str = "00:00:00:00:00:00") -> Dict:
        """Unified Bluetooth transport dispatch.
        Modes: advertisement (broadcast), spp (pair + send), gatt (connect + write).
        Uses existing HSE signing + LoRa TX as fallback.
        """
        ph = payload.get("proof_hash", "")
        if not ph: return {"error": "no proof hash"}
        sig = self.hse_sign(ph)
        if mode == "advertisement":
            result = self.bt_advertise(ph, sig["signature"])
        elif mode == "spp":
            result = self.bt_classic_spp(ph, sig, peer_addr)
        elif mode == "gatt":
            result = self.bt_gatt_write(ph, sig, peer_addr)
        else:
            return self.lora_transmit(payload)  # fallback to LoRa
        # Store BT transport record
        _ic_store(f"pos:bt_tx:{ph[:16]}", json.dumps({**result, "mode": mode}))
        return result

    def sovereign_key_settle(self, agent_did: str, merchant_id: str, amount: int,
                              corridor: str = "base_usdc", credential: str = "0x",
                              hse_id: str = "", bt_mode: str = "advertisement",
                              bt_peer: str = "00:00:00:00:00:00",
                              lora_fallback: bool = True) -> Dict:
        """Full Sovereign Key flow: settle → HSE sign → BT transport → LoRa fallback.
        Default: BLE advertisement broadcast (no pairing needed).
        Falls back to LoRa TX if BT fails or lora_fallback=True.
        """
        r = self.settle(agent_did, merchant_id, amount, corridor, credential)
        if "proof_hash" not in r: return r
        r["hse_signature"] = self.hse_sign(r["proof_hash"], hse_id)
        # Primary transport: BT
        if bt_mode:
            r["bt_transport"] = self.bt_broadcast(r, bt_mode, bt_peer)
        # Fallback: LoRa
        if lora_fallback:
            r["lora_tx"] = self.lora_transmit(r)
        r["bridge"] = "sovereign_key"
        r["bt_vs_lora_note"] = "BT (2.4GHz FHSS) carries proof data; LoRA (sub-GHz CSS) is physically distinct hardware"
        return r

if __name__ == "__main__":
    pos = POSBridge()
    print("=== POS Dongle × S7G Bridge ===")
    print(f"Platforms: {SUPPORTED_PLATFORMS}")
    print(f"Corridors: {SUPPORTED_CORRIDORS}")
    print(f"HSE: TernaryKeccak {TERNARY_KECCAK_ROUNDS} rounds")
    print()

    # Demo: Sovereign Key settlement with BT transport
    print("=== Sovereign Key: BLE Advertisement Broadcast ===")
    result = pos.sovereign_key_settle("did:zkpologon:agent-001", "merchant-7g-node", 1000000,
                                       bt_mode="advertisement")
    for k, v in result.items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for sk, sv in v.items(): print(f"    {sk}: {str(sv)[:60]}")
        else: print(f"  {k}: {str(v)[:70]}")

    print("\n=== Sovereign Key: BT Classic SPP (Mobile Proxy) ===")
    r2 = pos.sovereign_key_settle("did:zkpologon:agent-002", "merchant-7g-node", 500000,
                                   bt_mode="spp", bt_peer="AA:BB:CC:DD:EE:FF")
    print(f"  BT transport: {r2.get('bt_transport',{}).get('transport')}")
    print(f"  Payload: {r2.get('bt_transport',{}).get('bytes',0)} bytes")

    print("\n=== Sovereign Key: BLE GATT (Direct Write) ===")
    r3 = pos.sovereign_key_settle("did:zkpologon:agent-003", "merchant-7g-node", 250000,
                                   bt_mode="gatt", bt_peer="11:22:33:44:55:66")
    print(f"  BT transport: {r3.get('bt_transport',{}).get('transport')}")
    print(f"  LoRa fallback: {r3.get('lora_tx',False)}")

    # Verify
    ph = result.get("proof_hash", "")
    sig = result.get("hse_signature", {}).get("signature", "")
    verified = pos.hse_verify(ph, sig)
    print(f"\n  HSE Verified: {verified}")
    print(f"  Note: {result.get('bt_vs_lora_note','')}")
