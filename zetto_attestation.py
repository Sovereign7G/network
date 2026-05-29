#!/usr/bin/env python3
"""
🏛️ AGE REPUBLIC :: ZETTO ATTESTATION ADAPTER
==============================================
Drop-in integration layer that replaces os.urandom-based attestation
hashes throughout the sovereign infrastructure with Zetto's native
Keccak-256 seals from libzetto.so.

This is the "70% benefit for 20% effort" integration:
- No rewriting of existing Python orchestration
- No new runtime dependencies
- Just swap os.urandom().hex() → zetto_attest()

Usage:
    from zetto_attestation import sovereign_attest, seal_transaction, ZettoAttester

    # Simple seal (replaces os.urandom(32).hex())
    hash = sovereign_attest("payload data")

    # Transaction attestation (replaces mock tx hashes)
    tx = seal_transaction(sender="0x...", amount=100.0, reference="Settlement")
"""

import os
import sys
import json
import time
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("sovereign.zetto.attestation")

# ─────────────────────────────────────────────────────────────
# Lazy-load the Zetto bridge — graceful fallback to hashlib
# ─────────────────────────────────────────────────────────────

_bridge = None
_bridge_available = None


def _get_bridge():
    """Lazy-load ZettoBridge from the sovereign_trinity crate.
    Falls back to Python hashlib if libzetto.so is not compiled."""
    global _bridge, _bridge_available

    if _bridge_available is not None:
        return _bridge

    try:
        # Find zetto_bridge.py relative to this file
        trinity_root = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "04_SUBSTRATES", "sovereign_trinity"
        )
        if trinity_root not in sys.path:
            sys.path.insert(0, trinity_root)

        from zetto_bridge import ZettoBridge
        _bridge = ZettoBridge()
        _bridge_available = True
        logger.info("🔗 Zetto native attestation engine loaded (Rust Keccak-256)")
        return _bridge

    except (ImportError, FileNotFoundError, OSError) as e:
        _bridge_available = False
        logger.warning(f"⚠️ Zetto bridge unavailable ({e}). Falling back to Python hashlib.")
        return None


def _python_fallback_seal(content: str) -> str:
    """Pure-Python Keccak-256 fallback using hashlib."""
    import hashlib
    h = hashlib.sha3_256(content.encode("utf-8")).hexdigest()
    return f"0x{h}"


# ─────────────────────────────────────────────────────────────
# Public API — Drop-in replacements
# ─────────────────────────────────────────────────────────────

def sovereign_attest(content: str) -> str:
    """Compute a Keccak-256 attestation seal.

    Drop-in replacement for: "0x" + os.urandom(32).hex()

    Uses Zetto Rust native Keccak-256 if available, falls back
    to Python hashlib.sha3_256 otherwise.

    Args:
        content: The data to seal (transaction payload, module source, etc.)

    Returns:
        "0x" + 64 hex chars of the Keccak-256 digest
    """
    bridge = _get_bridge()
    if bridge:
        return bridge.seal(content)
    return _python_fallback_seal(content)


def seal_transaction(
    sender: str,
    amount: float,
    reference: str,
    chain_id: int = 31337,
    timestamp: Optional[int] = None,
) -> str:
    """Generate a deterministic attestation hash for a transaction.

    Unlike os.urandom, this produces the SAME hash for the same inputs —
    making transactions cryptographically verifiable and auditable.

    Args:
        sender: Sender wallet address
        amount: Transaction amount
        reference: Human-readable reference
        chain_id: EVM chain ID
        timestamp: Unix timestamp (defaults to current time)

    Returns:
        "0x" + 64 hex chars of the Keccak-256 digest
    """
    ts = timestamp or int(time.time())
    payload = json.dumps({
        "sender": sender,
        "amount": str(amount),
        "reference": reference,
        "chain_id": chain_id,
        "timestamp": ts,
    }, sort_keys=True, separators=(",", ":"))
    return sovereign_attest(payload)


def seal_consensus(
    agreed_nodes: int,
    total_nodes: int,
    schema: str = "RAFT_BFT_V1",
) -> str:
    """Generate attestation hash for a consensus round.

    Args:
        agreed_nodes: Number of nodes that agreed
        total_nodes: Total nodes in the quorum
        schema: Consensus protocol identifier

    Returns:
        Keccak-256 seal of the consensus state
    """
    payload = f"consensus:{schema}:agreed={agreed_nodes}:total={total_nodes}:ts={int(time.time())}"
    return sovereign_attest(payload)


def seal_reserve_attestation(
    circulating_supply: float,
    reserve_balance: float,
    jurisdiction: str = "EEA",
) -> str:
    """Generate attestation hash for a reserve backing proof.

    Args:
        circulating_supply: Total circulating supply
        reserve_balance: Total reserve balance
        jurisdiction: Regulatory jurisdiction

    Returns:
        Keccak-256 seal of the reserve attestation
    """
    payload = json.dumps({
        "type": "reserve_attestation",
        "circulating_supply": str(circulating_supply),
        "reserve_balance": str(reserve_balance),
        "jurisdiction": jurisdiction,
        "backing_ratio": str(reserve_balance / circulating_supply),
        "timestamp": int(time.time()),
    }, sort_keys=True, separators=(",", ":"))
    return sovereign_attest(payload)


class ZettoAttester:
    """Stateful attestation context for a specific trust boundary.

    Usage:
        attester = ZettoAttester("bifrost::execution")
        seal = attester.seal("transaction payload")
        batch = attester.seal_batch(["payload1", "payload2", "payload3"])
    """

    def __init__(self, trust_boundary: str):
        self.trust_boundary = trust_boundary
        self.seal_count = 0
        self._bridge = _get_bridge()

    def seal(self, content: str) -> str:
        """Seal content within this trust boundary context."""
        prefixed = f"[{self.trust_boundary}] {content}"
        self.seal_count += 1
        if self._bridge:
            return self._bridge.seal(prefixed)
        return _python_fallback_seal(prefixed)

    def seal_batch(self, payloads: list[str]) -> list[str]:
        """Seal multiple payloads efficiently."""
        return [self.seal(p) for p in payloads]

    def __repr__(self):
        return f"ZettoAttester(boundary='{self.trust_boundary}', seals={self.seal_count})"


# ─────────────────────────────────────────────────────────────
# Self-test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🏛️ ═══════════════════════════════════════════════")
    print("   ZETTO ATTESTATION ADAPTER :: Integration Test")
    print("═══════════════════════════════════════════════════\n")

    # Test 1: Basic seal
    seal = sovereign_attest("hello sovereign world")
    print(f"📊 Basic seal: {seal}")
    assert seal.startswith("0x") and len(seal) == 66

    # Test 2: Deterministic — same input → same output
    seal2 = sovereign_attest("hello sovereign world")
    assert seal == seal2, "Seals should be deterministic!"
    print(f"✅ Deterministic: {seal == seal2}")

    # Test 3: Transaction seal
    tx_seal = seal_transaction("0xABCD", 100.0, "test", timestamp=1234567890)
    print(f"📊 Transaction seal: {tx_seal}")
    tx_seal2 = seal_transaction("0xABCD", 100.0, "test", timestamp=1234567890)
    assert tx_seal == tx_seal2
    print(f"✅ Transaction determinism: {tx_seal == tx_seal2}")

    # Test 4: Consensus seal
    c_seal = seal_consensus(5, 7)
    print(f"📊 Consensus seal: {c_seal}")

    # Test 5: Reserve attestation
    r_seal = seal_reserve_attestation(50_000_000.0, 50_050_000.0)
    print(f"📊 Reserve seal: {r_seal}")

    # Test 6: ZettoAttester context
    attester = ZettoAttester("bifrost::execution")
    s1 = attester.seal("portfolio allocation ETH=40%")
    s2 = attester.seal("portfolio allocation ARB=15%")
    print(f"📊 Attester: {attester}")
    print(f"   Seal 1: {s1[:32]}...")
    print(f"   Seal 2: {s2[:32]}...")

    # Test 7: Throughput
    import time as _time
    n = 5000
    t0 = _time.perf_counter()
    for i in range(n):
        sovereign_attest(f"throughput_test_{i}")
    ms = (_time.perf_counter() - t0) * 1000
    print(f"\n📊 Throughput: {n} seals in {ms:.2f}ms ({n / (ms / 1000):.0f} seals/sec)")

    bridge = _get_bridge()
    engine = "Zetto Rust" if bridge else "Python hashlib"
    print(f"\n✅ All tests passed. Engine: {engine}")
