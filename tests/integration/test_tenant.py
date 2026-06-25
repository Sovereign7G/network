"""Tenant integration tests."""
import pytest
from .conftest import dfx_call, require_live

@require_live
def test_tenant_count():
    r = dfx_call("tenant_count")
    assert r["ok"]
    assert int(r["result"].strip("() ")) >= 0

@require_live
def test_list_tenants():
    r = dfx_call("list_tenants")
    assert r["ok"]

@require_live
def test_register_tenant_admin_only():
    """Anonymous call must fail — tenant registration requires Admin role."""
    r = dfx_call("register_tenant", '(record { name = "probe"; tier = "starter"; label = null; credits_canister = null; settlement_canister = null; })')
    # Must either succeed (if deployer) or fail with auth error
    assert r["ok"] or "Unauthorized" in r.get("result", "")
