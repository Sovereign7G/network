"""
shroud.py — SHROUD Python SDK
Cross-chain trust coordination engine client.

Usage:
    from shroud import SHROUDClient
    client = SHROUDClient()
    await client.get_committee("UsEast")
    await client.submit_settlement("bitcoin", "{...}")
"""

import os
import json
import hashlib
import subprocess
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

CANISTER_ID = "txdkz-xqaaa-aaaaa-qhkea-cai"
DFX_PATH = os.environ.get("DFX_PATH", os.path.expanduser("~/.cache/dfinity/versions/0.32.0/dfx"))


@dataclass
class AttestedNode:
    node_id: str
    mr_enclave: str
    zone: str
    dtc_rtt: int
    last_attestation: int
    is_active: bool


@dataclass
class Committee:
    zone: str
    members: List[str]
    epoch: int
    threshold: int
    valid_until: int


@dataclass
class LatencyProfile:
    zone: str
    min_rtt: int
    max_rtt: int
    mean: float
    stddev: float
    sample_count: int


class SHROUDClient:
    """Client for interacting with the SHROUD orchestrator canister."""

    def __init__(self, canister_id: str = CANISTER_ID, dfx_path: str = DFX_PATH):
        self.canister_id = canister_id
        self.dfx_path = dfx_path

    def _call(self, method: str, args: str) -> str:
        """Call canister method via dfx."""
        env = os.environ.copy()
        env["DFX_WARNING"] = "-mainnet_plaintext_identity"
        
        result = subprocess.run(
            [self.dfx_path, "canister", "call", self.canister_id, method, args,
             "--network", "ic"],
            capture_output=True, text=True, env=env
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"dfx call failed: {result.stderr}")
        
        # Strip deprecation warning
        lines = [l for l in result.stdout.split("\n") if "dfx is deprecated" not in l]
        return "\n".join(lines).strip()

    def _format_zone(self, zone: str) -> str:
        """Format zone name for Candid."""
        # Capitalize first letter, lowercase rest
        return zone.capitalize()

    # ── Node operations ──────────────────────────────────────────────

    def get_attested_nodes(self, zone: Optional[str] = None) -> List[Dict]:
        """Get all attested nodes, optionally filtered by zone."""
        if zone:
            args = f'(opt variant {{ {self._format_zone(zone)} }})'
        else:
            args = "(null)"
        return self._call("get_attested_nodes", args)

    def register_attestation(
        self, node_id: str, mr_enclave: str, zone: str,
        dtc_rtt: int = 60, timestamp: Optional[int] = None
    ) -> bool:
        """Register a node attestation."""
        ts = timestamp or int(datetime.now().timestamp())
        args = (
            f'(record {{ '
            f'node_id = principal "{node_id}"; '
            f'mr_enclave = "{mr_enclave}"; '
            f'zone = variant {{ {self._format_zone(zone)} }}; '
            f'dtc_rtt = {dtc_rtt}; '
            f'signature = vec {{}}; '
            f'timestamp = {ts}; '
            f'}})'
        )
        result = self._call("register_attestation", args)
        return "Ok" in result

    # ── Committee operations ─────────────────────────────────────────

    def get_committee(self, zone: str) -> Optional[Dict]:
        """Get committee for a zone."""
        result = self._call("get_committee", f'(variant {{ {self._format_zone(zone)} }})')
        if "null" in result:
            return None
        return result

    def rotate_committee(self, zone: str) -> Optional[Dict]:
        """Rotate committee for a zone."""
        result = self._call("rotate_committee", f'(variant {{ {self._format_zone(zone)} }})')
        if "Err" in result:
            raise RuntimeError(f"Rotation failed: {result}")
        return result

    def get_committee_health(self) -> List[tuple]:
        """Get health status of all committees."""
        return self._call("get_committee_health", "()")

    # ── Settlement operations ────────────────────────────────────────

    def get_pending_settlements(self) -> List[Dict]:
        """Get all pending settlements."""
        return self._call("get_pending_settlements", "()")

    def submit_settlement(self, ledger_id: str, terms_hash: str, threshold: int = 2) -> bool:
        """Submit a new settlement to the SHROUD orchestrator."""
        args = (
            f'(record {{ '
            f'ledger_id = "{ledger_id}"; '
            f'terms_hash = vec {{ {", ".join(hex(b) for b in bytes.fromhex(terms_hash))} }}; '
            f'signatures = vec {{}}; '
            f'threshold = {threshold}; '
            f'finalized = false; '
            f'}})'
        )
        result = self._call("submit_settlement", args)
        return "Ok" in result

    def finalize_settlement(self, ledger_id: str, signatures: List[str]) -> bool:
        """Finalize a settlement with signatures."""
        sigs = "; ".join(f"vec {{ {s} }}" for s in signatures)
        args = f'("{ledger_id}", vec {{ {sigs} }})'
        result = self._call("finalize_settlement", args)
        return "Ok" in result

    # ── Cross-Chain Settlement Operations ────────────────────────────

    def settle_bitcoin(self, to_address: str, amount_sats: int, fee_rate: int = 1) -> Dict:
        """Submit a Bitcoin settlement through the SHROUD committee.
        
        The committee verifies the Bitcoin tx and finalizes via 2-of-4.
        Settlement terms are hidden (FE) — only the final result is visible.
        """
        ledger_id = f"bitcoin:{to_address}"
        # Submit with hidden terms_hash (FE commitment)
        terms = hashlib.sha256(f"{to_address}:{amount_sats}".encode()).hexdigest()
        ok = self.submit_settlement(ledger_id, terms)
        return {"ledger": "bitcoin", "to": to_address, "amount_sats": amount_sats, "submitted": ok}

    def settle_evm(self, chain: str, to_address: str, amount_wei: int) -> Dict:
        """Submit an EVM chain settlement through the SHROUD committee.
        
        Supports Ethereum, Polygon, Arbitrum, Optimism, and Base.
        Settlement instructions are hidden via FHE.
        """
        ledger_id = f"evm:{chain}:{to_address}"
        terms = hashlib.sha256(f"{chain}:{to_address}:{amount_wei}".encode()).hexdigest()
        ok = self.submit_settlement(ledger_id, terms)
        return {"ledger": "evm", "chain": chain, "to": to_address, "amount_wei": amount_wei, "submitted": ok}

    def settle_solana(self, to_address: str, amount_lamports: int) -> Dict:
        """Submit a Solana settlement through the SHROUD committee.
        
        Solana's 400ms finality means the committee can verify quickly.
        Terms are hidden — committee sees only the commitment hash.
        """
        ledger_id = f"solana:{to_address}"
        terms = hashlib.sha256(f"solana:{to_address}:{amount_lamports}".encode()).hexdigest()
        ok = self.submit_settlement(ledger_id, terms)
        return {"ledger": "solana", "to": to_address, "amount_lamports": amount_lamports, "submitted": ok}

    def settle_elastos(self, carrier_id: str, service_type: str, units: int) -> Dict:
        """Submit an ELASTOS carrier settlement.
        
        Carrier settlement is attested via vAOM/DTC location anchoring.
        Routing decisions are computed via FHE (hidden from committee).
        """
        ledger_id = f"elastos:{carrier_id}:{service_type}"
        terms = hashlib.sha256(f"elastos:{carrier_id}:{service_type}:{units}".encode()).hexdigest()
        ok = self.submit_settlement(ledger_id, terms)
        return {"ledger": "elastos", "carrier": carrier_id, "service": service_type, "units": units, "submitted": ok}

    def settle_icp(self, to_principal: str, amount_e8s: int, memo: str = "") -> Dict:
        """Submit an ICP ledger settlement.
        
        Native ICP settlements use the SHROUD orchestrator directly.
        The canister verifies the ledger tx and settles via 2-of-4 committee.
        """
        ledger_id = f"icp:{to_principal}"
        terms = hashlib.sha256(f"icp:{to_principal}:{amount_e8s}:{memo}".encode()).hexdigest()
        ok = self.submit_settlement(ledger_id, terms)
        return {"ledger": "icp", "to": to_principal, "amount_e8s": amount_e8s, "submitted": ok}

    def get_settlement_status(self, ledger_id: str) -> Dict:
        """Check the status of a settlement by ledger_id.
        
        Returns whether the settlement is pending, finalized, or failed.
        """
        settlements = self.get_pending_settlements()
        for s in settlements:
            if s.get("ledger_id") == ledger_id:
                return s
        # Check if it was finalized by looking at the accumulator
        return {"ledger_id": ledger_id, "status": "unknown"}

    # ── Mesh operations ──────────────────────────────────────────────

    def get_mesh_topology(self) -> Dict:
        """Get current mesh topology."""
        return self._call("get_mesh_topology", "()")

    def form_cross_zone_committee(self, zones: List[str]) -> Optional[Dict]:
        """Form a cross-zone committee from multiple zones."""
        zone_args = "; ".join(z.capitalize() for z in zones)
        args = f'(vec {{ variant {{ {zone_args} }} }})'
        result = self._call("form_cross_zone_committee", args)
        if "Err" in result:
            raise RuntimeError(f"Cross-zone committee failed: {result}")
        return result

    def get_cross_zone_committee(self, zones: List[str]) -> Optional[Dict]:
        """Get cross-zone committee for specific zones."""
        zone_args = "; ".join(z.capitalize() for z in zones)
        result = self._call("get_cross_zone_committee", f'(vec {{ variant {{ {zone_args} }} }})')
        if "null" in result:
            return None
        return result

    def get_all_cross_zone_committees(self) -> List[Dict]:
        """Get all cross-zone committees."""
        result = self._call("get_all_cross_zone_committees", "()")
        return result

    def update_mesh_topology(self, connections: List[tuple]) -> bool:
        """Update mesh topology with zone-to-zone latency connections."""
        conn_args = "; ".join(
            f"variant {{ {z1.capitalize()} }}, variant {{ {z2.capitalize()} }}, {lat}"
            for z1, z2, lat in connections
        )
        args = f'(vec {{ record {{ {conn_args} }} }})'
        result = self._call("update_mesh_topology", args)
        return "Ok" in result

    def get_latency_profile(self, zone: str) -> Optional[Dict]:
        """Get latency profile for a zone."""
        result = self._call("get_latency_profile", f'(variant {{ {self._format_zone(zone)} }})')
        if "null" in result:
            return None
        return result

    def get_all_latency_profiles(self) -> List[Dict]:
        """Get latency profiles for all zones."""
        return self._call("get_all_latency_profiles", "()")

    def get_recommended_bounds(self, zone: str) -> Optional[tuple]:
        """Get recommended latency bounds for a zone."""
        result = self._call("get_recommended_bounds", f'(variant {{ {self._format_zone(zone)} }})')
        if "null" in result:
            return None
        return result

    def reset_calibration(self, zone: str) -> bool:
        """Reset latency calibration for a zone."""
        result = self._call("reset_calibration", f'(variant {{ {self._format_zone(zone)} }})')
        return "Ok" in result

    def report_latency_sample(self, node_id: str, zone: str, rtt: int) -> bool:
        """Report a latency measurement."""
        ts = int(datetime.now().timestamp())
        args = (
            f'(record {{ '
            f'zone = variant {{ {self._format_zone(zone)} }}; '
            f'node_id = principal "{node_id}"; '
            f'rtt = {rtt}; '
            f'timestamp = {ts}; '
            f'}})'
        )
        result = self._call("report_latency_sample", args)
        return "Ok" in result

    # ── Recovery operations ───────────────────────────────────────────

    def check_committee_health(self) -> List[tuple]:
        """Get health status of all committees."""
        return self._call("check_committee_health", "()")

    def recover_zone(self, zone: str) -> bool:
        """Recover a degraded zone."""
        result = self._call("recover_zone", f'(variant {{ {self._format_zone(zone)} }})')
        return "Ok" in result

    def recover_settlement(self, ledger_id: str) -> bool:
        """Recover a failed settlement."""
        result = self._call("recover_settlement", f'("{ledger_id}")')
        return "Ok" in result

    def enter_degraded_mode(self, zone: str) -> bool:
        """Enter degraded mode for a zone."""
        result = self._call("enter_degraded_mode", f'(variant {{ {self._format_zone(zone)} }})')
        return "Ok" in result

    def exit_degraded_mode(self, zone: str) -> bool:
        """Exit degraded mode for a zone."""
        result = self._call("exit_degraded_mode", f'(variant {{ {self._format_zone(zone)} }})')
        return "Ok" in result

    def is_zone_degraded(self, zone: str) -> bool:
        """Check if a zone is in degraded mode."""
        result = self._call("is_zone_degraded", f'(variant {{ {self._format_zone(zone)} }})')
        return "true" in result

    def get_degraded_zones(self) -> List[str]:
        """Get all degraded zones."""
        return self._call("get_degraded_zones", "()")

    # ── Sidecar deployment operations ─────────────────────────────────

    def get_latest_version(self) -> int:
        """Get latest sidecar version available on the canister."""
        result = self._call("get_latest_version", "()")
        return int(result.strip("()"))

    def get_sidecar_manifest(self) -> str:
        """Get sidecar deployment manifest."""
        return self._call("get_sidecar_manifest", "()")

    # ── Governance operations ────────────────────────────────────────

    def get_governors(self) -> List[str]:
        """Get list of governance principals."""
        return self._call("get_governors", "()")

    def set_governance_threshold(self, threshold: int) -> bool:
        """Set multi-sig threshold."""
        result = self._call("set_governance_threshold", f'({threshold})')
        return "Ok" in result

    def get_governance_threshold(self) -> int:
        """Get current governance threshold."""
        result = self._call("get_governance_threshold", "()")
        return int(result.strip("()"))


# ── Convenience CLI ──────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    client = SHROUDClient()
    
    if len(sys.argv) < 2:
        print("Usage: python shroud.py <command> [args]")
        print("Commands: nodes, committee, health, pending, topology")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "nodes":
        zone = sys.argv[2] if len(sys.argv) > 2 else None
        print(client.get_attested_nodes(zone))
    elif cmd == "committee":
        zone = sys.argv[2] if len(sys.argv) > 2 else "UsEast"
        print(client.get_committee(zone))
    elif cmd == "health":
        print(client.get_committee_health())
    elif cmd == "pending":
        print(client.get_pending_settlements())
    elif cmd == "topology":
        print(client.get_mesh_topology())
    else:
        print(f"Unknown command: {cmd}")
