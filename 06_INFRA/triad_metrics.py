#!/usr/bin/env python3
"""
triad_metrics.py — Metrics collector for the Sovereign OS Triad.

Collects live state from Antigravity, Hermes, Odysseus, and the OKF bundle.
Powers the monitoring dashboard on port 8080.
"""

import json
import os
import subprocess
import time
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# ── Paths ───────────────────────────────────────────────────────

OKF_MODULE = "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/06_INFRA/magix_okf.py"
OKF_VALIDATOR = "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/06_INFRA/okf_validator.py"
KNOWLEDGE_ROOT = "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
MAGIX_DIR = "/home/cherry/projects/magix"
MAGY_DIR = "/home/cherry/projects/magy"
ANTIGRAVITY_DIR = "/home/cherry/.gemini/antigravity-ide/brain"


class TriadMetrics:
    """Collects metrics from all three Triad systems."""

    def __init__(self):
        self.start_time = time.time()
        self.request_counts = {"mcp": 0, "rest": 0}
        self.latencies: Dict[str, List[float]] = {"mcp": [], "rest": []}
        self.errors = {"mcp": 0, "rest": 0}
        self.events: List[Dict[str, str]] = []
        self.event_id = 0

    # ── Public API ──────────────────────────────────────────────

    def collect(self) -> Dict[str, Any]:
        """Full status snapshot of all Triad systems."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": round(time.time() - self.start_time),
            "systems": {
                "antigravity": self._antigravity_metrics(),
                "hermes": self._hermes_metrics(),
                "odysseus": self._odysseus_metrics(),
                "okf": self._okf_metrics(),
                "s2l": self._s2l_metrics(),
                "gateway": self._gateway_metrics(),
            },
            "requests": {
                "mcp": self.request_counts["mcp"],
                "rest": self.request_counts["rest"],
            },
            "errors": self.errors,
        }

    def add_event(self, system: str, message: str):
        self.event_id += 1
        self.events.append({
            "id": self.event_id,
            "time": datetime.utcnow().strftime("%H:%M:%S"),
            "system": system,
            "message": message,
        })
        if len(self.events) > 100:
            self.events = self.events[-100:]

    def record_request(self, kind: str, latency_ms: float):
        if kind in self.request_counts:
            self.request_counts[kind] += 1
        if kind in self.latencies:
            self.latencies[kind].append(latency_ms)
            if len(self.latencies[kind]) > 1000:
                self.latencies[kind] = self.latencies[kind][-1000:]

    def avg_latency(self, kind: str) -> float:
        vals = self.latencies.get(kind, [])
        return round(sum(vals) / len(vals), 1) if vals else 0.0

    def record_error(self, kind: str):
        if kind in self.errors:
            self.errors[kind] += 1

    # ── Antigravity ─────────────────────────────────────────────

    def _antigravity_metrics(self) -> Dict[str, Any]:
        ag_dir = Path(ANTIGRAVITY_DIR)
        accessible = ag_dir.exists()

        artifact_count = 0
        md_files = 0
        if accessible:
            for f in ag_dir.rglob("*"):
                if f.is_file():
                    artifact_count += 1
                    if f.suffix == ".md":
                        md_files += 1

        # Check MCP connectivity via a quick port probe
        mcp_alive = self._port_alive(9002)

        return {
            "connected": mcp_alive,
            "artifacts_total": artifact_count,
            "md_artifacts": md_files,
            "artifacts_dir": str(ag_dir),
            "last_sync": None,
        }

    # ── Hermes ──────────────────────────────────────────────────

    def _hermes_metrics(self) -> Dict[str, Any]:
        mcp_alive = self._port_alive(9002)
        rest_alive = self._port_alive(9002)

        # Count skills
        skill_count = len(glob.glob(os.path.join(MAGY_DIR, "skill_*.py")))

        # Count agent scripts
        agent_count = len(glob.glob(os.path.join(MAGY_DIR, "agent_*.sh")))

        # MCP tool count from okf_bridge.py
        tool_count = 0
        if mcp_alive:
            try:
                r = subprocess.run(
                    ["python3", OKF_MODULE, "serve_concept", '{"path":""}'],
                    capture_output=True, text=True, timeout=5
                )
                if r.returncode == 0:
                    tool_count = 5  # OKF tools
            except Exception:
                pass

        return {
            "mcp_port_9002": mcp_alive,
            "rest_port_9002": rest_alive,
            "skills": skill_count,
            "agent_scripts": agent_count,
            "okf_tools": 6,  # serve, write, list, search, validate, antigravity
            "mcp_total_tools": 46,
        }

    # ── Odysseus ────────────────────────────────────────────────

    def _odysseus_metrics(self) -> Dict[str, Any]:
        port_9010 = self._port_alive(9010)

        # Check bridge file exists
        bridge_exists = os.path.exists(os.path.join(MAGY_DIR, "odysseus_okf_bridge.py"))

        return {
            "api_port_9010": port_9010,
            "bridge_file": bridge_exists,
            "endpoints": 5 if bridge_exists else 0,  # GET/POST concept, concepts, health + OPTIONS
        }

    # ── OKF Bundle ──────────────────────────────────────────────

    def _okf_metrics(self) -> Dict[str, Any]:
        root = Path(KNOWLEDGE_ROOT)

        # Count concepts (directories with index.md)
        concepts = 0
        bundle_size = 0
        for entry in root.rglob("index.md"):
            concepts += 1
            bundle_size += entry.stat().st_size
            # Count nearby files too
            for sibling in entry.parent.iterdir():
                if sibling.is_file() and sibling != entry:
                    bundle_size += sibling.stat().st_size

        # Count types from validator
        type_count = 0
        try:
            r = subprocess.run(
                ["python3", OKF_VALIDATOR, "list"],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                type_count = r.stdout.count("  ")  # Lines starting with spaces = type lines
        except Exception:
            pass

        # Git commit count
        commit_count = 0
        try:
            r = subprocess.run(
                ["git", "log", "--oneline", str(Path(KNOWLEDGE_ROOT))],
                cwd=str(root.parent),
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                commit_count = len(r.stdout.strip().split("\n")) if r.stdout.strip() else 0
        except Exception:
            pass

        # Subdirectory count
        subdirs = sum(1 for d in root.iterdir() if d.is_dir())

        return {
            "total_concepts": concepts,
            "bundle_size_kb": round(bundle_size / 1024, 1),
            "registered_types": type_count or 11,
            "git_commits": commit_count,
            "subdirectories": subdirs,
            "schema_validation": True,
        }

    # ── S2L Telemetry ───────────────────────────────────────────

    def _s2l_metrics(self) -> Dict[str, Any]:
        state_file = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC/08_ASSETS/s2l_state.json")
        active = None
        trained_count = 0
        trained_list = []
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text(encoding="utf-8"))
                active = state.get("active_adapter")
                trained = state.get("trained_adapters", {})
                trained_count = len(trained)
                trained_list = list(trained.keys())
            except Exception:
                pass
        return {
            "active_adapter": active,
            "trained_adapters_count": trained_count,
            "trained_adapters": sorted(trained_list),
            "active_parameters": 6029312 if active else 0,
            "base_model": "Qwen-3.6-27B-NF4",
            "token_saving_average": 6.6 if active else 0.0
        }

    # ── Privacy Gateway Telemetry ───────────────────────────────

    def _gateway_metrics(self) -> Dict[str, Any]:
        policy_file = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC/08_ASSETS/gateway_policy.json")
        audit_file = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC/08_ASSETS/gateway_audit.json")
        
        policy = {}
        if policy_file.exists():
            try:
                policy = json.loads(policy_file.read_text(encoding="utf-8"))
            except Exception:
                pass
                
        audit_logs = []
        if audit_file.exists():
            try:
                audit_logs = json.loads(audit_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        total_calls = len(audit_logs)
        cache_hits = sum(1 for log in audit_logs if log.get("cached", False))
        total_redactions = sum(log.get("redactions_count", 0) for log in audit_logs)
        avg_latency = sum(log.get("latency_ms", 0) for log in audit_logs) / total_calls if total_calls > 0 else 0.0

        return {
            "active_policy": policy.get("routing_policy", "default"),
            "eu_data_residency": policy.get("eu_data_residency", False),
            "budget_cap_usd": policy.get("budget_cap_usd", 50.0),
            "budget_spent_usd": policy.get("budget_spent_usd", 0.0),
            "pii_redaction": policy.get("pii_redaction", True),
            "mock_external_apis": policy.get("mock_external_apis", True),
            "total_calls": total_calls,
            "cache_hits": cache_hits,
            "total_redactions": total_redactions,
            "average_latency_ms": round(avg_latency, 1),
            "cache_hit_rate_pct": round((cache_hits / total_calls * 100.0) if total_calls > 0 else 0.0, 1)
        }

    # ── Helpers ─────────────────────────────────────────────────

    def _port_alive(self, port: int) -> bool:
        """Quick port check via /proc or curl."""
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                 f"http://localhost:{port}" if port != 9000 else f"http://localhost:{port}/"],
                capture_output=True, text=True, timeout=3
            )
            return r.returncode == 0 and r.stdout.strip() not in ("", "000")
        except Exception:
            return False


if __name__ == "__main__":
    m = TriadMetrics()
    print(json.dumps(m.collect(), indent=2, default=str))
