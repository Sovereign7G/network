#!/usr/bin/env python3
"""Shared fixtures for canister integration tests."""
import subprocess, json
from pathlib import Path

CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"
NETWORK = "ic"

def dfx_call(method: str, args: str = "()") -> dict:
    cmd = ["dfx", "canister", "call", CANISTER, method, args, "--network", NETWORK]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return {"ok": False, "error": r.stderr.strip()}
    return {"ok": True, "result": r.stdout.strip()}

def require_live(test_fn):
    """Decorator: skip test if canister unreachable."""
    import functools
    @functools.wraps(test_fn)
    def wrapper(*args, **kwargs):
        r = dfx_call("tenant_count")
        if not r["ok"]:
            import pytest
            pytest.skip("Canister unreachable")
        return test_fn(*args, **kwargs)
    return wrapper
