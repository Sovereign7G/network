#!/usr/bin/env python3
"""
agents/pair_stack_agent.py — S7G Pair Stack Hermes Agent

Orchestrates all 5 phases of the S7G + Pair integration:
- Phase A: Sidecar distribution (canister, resolver, Iroh)
- Phase B: Mobile OTA (iOS/Android stubs, bundle seed)
- Phase C: Provenance (Hypercore audit trail)
- Phase D: Committee P2P (Iroh node discovery)
- Phase E: A2A agent mesh (cross-vendor delegation)

Usage:
    from agents.pair_stack_agent import PairStackAgent
    agent = PairStackAgent()
    await agent.health()
    await agent.deploy_sidecar(version=9, binary_path="/tmp/sidecar")
    await agent.query_provenance(limit=10)
    await agent.discover_committee()
"""

import json
import os
import subprocess
from datetime import datetime

# ── Constants ──────────────────────────────────────────────────────────
CANISTER_ID = os.getenv("S7G_CANISTER_ID", "txdkz-xqaaa-aaaaa-qhkea-cai")
IROH_RELAY = os.getenv("S7G_IROH_RELAY", "http://localhost:3340")
S7G_HOME = os.getenv("S7G_HOME", "/opt/s7g")
DFX_PATH = os.getenv("DFX_PATH", os.path.expanduser("~/.cache/dfinity/versions/0.32.0/dfx"))
DFX_WARNING = "-mainnet_plaintext_identity"
DFX_WORKSPACE = os.getenv("S7G_WORKSPACE", "/tmp/s7g-dfx-workspace")


class PairStackAgent:
    """Hermes agent for the complete S7G + Pair stack."""

    def __init__(self):
        self.name = "s7g-pair-stack"
        self.version = "2.4.0"
        self.canister = CANISTER_ID
        self.relay = IROH_RELAY

    # ── Phase A: Sidecar Distribution ──────────────────────────────────

    def register_sidecar(self, version: int, discovery_key: str, sha256: str) -> dict:
        """Register a new sidecar version on ICP canister."""
        cmd = (
            f"cd {DFX_WORKSPACE} && DFX_WARNING={DFX_WARNING} {DFX_PATH} "
            f"canister call {self.canister} register_sidecar_version "
            f"'({version}, blob \"{discovery_key}\", blob \"{sha256}\")' --network ic"
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        success = "variant { Ok }" in result.stdout
        return {"action": "register_sidecar", "version": version, "success": success,
                "output": result.stdout.strip()}

    def get_latest_sidecar(self) -> dict:
        """Query the canister for the latest sidecar version and key."""
        cmd = (
            f"cd {DFX_WORKSPACE} && DFX_WARNING={DFX_WARNING} {DFX_PATH} "
            f"canister call {self.canister} get_latest_sidecar_key --network ic"
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return {"canister": self.canister, "response": result.stdout.strip()}

    def resolver_status(self) -> dict:
        """Check if the resolver daemon is running."""
        result = subprocess.run(
            ["systemctl", "--user", "status", "s7g-sidecar-resolver"],
            capture_output=True, text=True, timeout=5
        )
        active = "active (running)" in result.stdout
        return {"service": "s7g-sidecar-resolver", "active": active}

    # ── Phase C: Provenance ────────────────────────────────────────────

    def query_provenance(self, limit: int = 10) -> dict:
        """Read entries from the Hypercore provenance feed."""
        import sys
        sys.path.insert(0, f"{S7G_HOME}/shroud-enclave/lib")
        try:
            # Try reading the Hypercore feed directly
            cmd = (
                f"cd {S7G_HOME}/shroud-enclave && /usr/bin/nodejs -e "
                f"'const Hypercore = require(\"hypercore\");"
                f"(async()=>{{const c=new Hypercore(\"{S7G_HOME}/shroud-enclave/data/provenance/feed\");"
                f"await c.ready();const e=[];for(let i=Math.max(0,c.length-{limit});i<c.length;i++)"
                f"e.push(JSON.parse((await c.get(i)).toString()));console.log(JSON.stringify(e))}})()'"
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            entries = json.loads(result.stdout) if result.stdout else []
            return {"entries": len(entries), "data": entries}
        except Exception as e:
            return {"entries": 0, "error": str(e)}

    def verify_provenance(self) -> dict:
        """Verify the integrity of the provenance chain."""
        cmd = (
            f"cd {S7G_HOME}/shroud-enclave && /usr/bin/nodejs -e "
            f"'const{ProvenanceLayer}=require(\"./lib/provenance\");"
            f"(async()=>{{const p=new ProvenanceLayer({{storagePath:\"{S7G_HOME}/shroud-enclave/data/provenance\"}});"
            f"const r=await p.verifyChain();console.log(JSON.stringify(r))}})()'"
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        try:
            return json.loads(result.stdout) if result.stdout else {"valid": False}
        except json.JSONDecodeError:
            return {"valid": False, "error": result.stdout}

    # ── Phase D: Committee P2P ─────────────────────────────────────────

    def discover_committee(self) -> dict:
        """Check committee node status."""
        result = subprocess.run(
            ["systemctl", "--user", "status", "s7g-committee"],
            capture_output=True, text=True, timeout=5
        )
        active = "active (running)" in result.stdout
        return {"service": "s7g-committee", "active": active,
                "log": result.stdout[:200]}

    def committee_health(self) -> dict:
        """Get detailed committee node health metrics."""
        import subprocess
        try:
            disk = subprocess.run(["du", "-sh", S7G_HOME], capture_output=True, text=True)
            return {"node_id": os.uname().nodename, "storage": disk.stdout.strip()}
        except Exception as e:
            return {"node_id": os.uname().nodename, "error": str(e)}

    # ── Phase E: A2A Agent Mesh ────────────────────────────────────────

    def a2a_delegate(self, skill: str, payload: dict, target_did: str = None) -> dict:
        """Delegate a task to an A2A agent via the a2a-server."""
        import json
        env = json.dumps({"skill": skill, "payload": payload})
        cmd = (
            f"cd {S7G_HOME}/shroud-enclave && /usr/bin/nodejs "
            f"/home/cherry/.hermes/skills/devops/s7g-pair-integration/scripts/a2a-server.js "
            f"--client --skill={skill} --payload='{json.dumps(payload)[:200]}'"
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {"skill": skill, "result": result.stdout.strip()[:500]}

    # ── General Health ─────────────────────────────────────────────────

    def health(self) -> dict:
        """Complete system health check."""
        resolver = self.resolver_status()
        committee = self.discover_committee()
        return {
            "agent": self.name,
            "version": self.version,
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "resolver": resolver["active"],
                "committee": committee["active"],
                "iroh_relay": self._check_port(3340),
                "canister": self._check_canister(),
            }
        }

    def _check_port(self, port: int) -> bool:
        """Check if a port is listening."""
        result = subprocess.run(
            ["ss", "-tlnp"], capture_output=True, text=True, timeout=5
        )
        return f":{port}" in result.stdout

    def _check_canister(self) -> bool:
        """Check if the canister responds."""
        try:
            result = self.get_latest_sidecar()
            return "opt record" in result.get("response", "")
        except Exception:
            return False


# ── CLI Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    agent = PairStackAgent()

    if len(sys.argv) < 2:
        print(json.dumps(agent.health(), indent=2))
        sys.exit(0)

    command = sys.argv[1]
    handlers = {
        "health": agent.health,
        "register": lambda: agent.register_sidecar(
            int(sys.argv[2]), sys.argv[3], sys.argv[4]
        ) if len(sys.argv) >= 5 else {"error": "Usage: register <version> <discovery_key> <sha256>"},
        "latest": agent.get_latest_sidecar,
        "resolver": agent.resolver_status,
        "provenance": lambda: agent.query_provenance(int(sys.argv[2]) if len(sys.argv) > 2 else 10),
        "verify": agent.verify_provenance,
        "committee": agent.discover_committee,
        "delegate": lambda: agent.a2a_delegate(
            sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        ),
    }

    handler = handlers.get(command)
    if handler:
        print(json.dumps(handler(), indent=2))
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(handlers.keys())}")
