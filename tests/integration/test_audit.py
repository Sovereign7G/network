"""Audit trail integration tests."""
from .conftest import dfx_call, require_live

@require_live
def test_audit_integrity():
    r = dfx_call("verify_audit_integrity")
    assert r["ok"]
    assert "true" in r["result"]

@require_live
def test_audit_log():
    r = dfx_call("get_audit_log", '("", 0, 5)')
    assert r["ok"]

@require_live
def test_models():
    r = dfx_call("list_models", '(null, null)')
    assert r["ok"]

@require_live
def test_reserve_state():
    r = dfx_call("get_reserve_state")
    assert r["ok"]

@require_live
def test_metrics():
    r = dfx_call("get_metrics")
    assert r["ok"]

@require_live
def test_roles():
    r = dfx_call("list_roles")
    assert r["ok"]
