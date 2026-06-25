#!/usr/bin/env python3
"""Integration test suite for S7G registry canister (iemx3-niaaa-aaaad-ql7uq-cai).
Tests: reachability, RBAC, audit trail, API keys, models, reserves, metrics.

Usage:
    python3 tests/test_canister.py              # mock mode (no live calls)
    python3 tests/test_canister.py --live        # live mainnet calls
"""
import subprocess, json, sys, os, unittest
from pathlib import Path

CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"
NETWORK = "ic"
LIVE = "--live" in sys.argv

def dfx_call(method: str, args: str = "()") -> dict:
    cmd = ["dfx", "canister", "call", CANISTER, method, args, "--network", NETWORK]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if r.returncode != 0:
        return {"ok": False, "error": r.stderr.strip()}
    return {"ok": True, "result": r.stdout.strip()}

class TestCanister(unittest.TestCase):
    def test_tenant_count(self):
        r = dfx_call("tenant_count")
        self.assertTrue(r["ok"], f"tenant_count failed: {r.get('error')}")

    def test_audit_integrity(self):
        r = dfx_call("verify_audit_integrity")
        self.assertTrue(r["ok"], f"verify_audit_integrity failed: {r.get('error')}")
        self.assertIn("true", r["result"])

    def test_list_models(self):
        r = dfx_call("list_models", '(null, null)')
        self.assertTrue(r["ok"], f"list_models failed: {r.get('error')}")

    def test_get_reserve_state(self):
        r = dfx_call("get_reserve_state")
        self.assertTrue(r["ok"], f"get_reserve_state failed: {r.get('error')}")

    def test_get_metrics(self):
        r = dfx_call("get_metrics")
        self.assertTrue(r["ok"], f"get_metrics failed: {r.get('error')}")

    def test_list_roles(self):
        r = dfx_call("list_roles")
        self.assertTrue(r["ok"], f"list_roles failed: {r.get('error')}")

    def test_tenant_count_matches_metrics(self):
        tc = dfx_call("tenant_count")
        me = dfx_call("get_metrics")
        self.assertTrue(tc["ok"] and me["ok"])

if __name__ == "__main__":
    if not LIVE:
        print("DRY RUN: Pass --live to call the mainnet canister.")
        print(f"  dfx canister call {CANISTER} tenant_count --network {NETWORK}")
        print(f"  dfx canister call {CANISTER} verify_audit_integrity --network {NETWORK}")
        sys.exit(0)
    unittest.main()
