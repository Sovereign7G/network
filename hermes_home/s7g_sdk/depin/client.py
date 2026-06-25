"""DepinClient — wraps S7G registry canister calls for all P1-P6 domains.

Usage:
    from s7g_sdk.depin import DepinClient
    c = DepinClient()
    c.tenant_count()  # 2
    c.list_models()   # [ModelRegistration, ...]
    c.get_reserve_state()  # {usdc_balance: 0, compliant: false}
"""
import json
import subprocess
import sys
from typing import Any, Optional

REGISTRY_CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"

def _call(method: str, args: str = "()", network: str = "ic") -> Any:
    """Call the registry canister via dfx subprocess."""
    try:
        out = subprocess.check_output(
            ["dfx", "canister", "call", REGISTRY_CANISTER, method, args,
             "--network", network],
            stderr=subprocess.DEVNULL, timeout=30, text=True,
        )
        return out.strip()
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout calling {method}"}
    except subprocess.CalledProcessError:
        return {"error": f"Failed calling {method}"}


class DepinClient:
    """Full API client for the S7G DePIN registry canister."""

    def __init__(self, tenant: Optional[str] = None, network: str = "ic"):
        self.tenant = tenant
        self.network = network

    # ── Tenant API ──────────────────────────────────────────────────

    def register_tenant(self, name: str, tier: str = "starter",
                        label: Optional[str] = None) -> Any:
        a = f'(record {{ name = "{name}"; tier = "{tier}"; label = opt "{label or name}"; credits_canister = null; settlement_canister = null; }})'
        return _call("register_tenant", a, self.network)

    def get_tenant(self, name: str) -> Any:
        return _call("get_tenant", f'("{name}")', self.network)

    def list_tenants(self) -> Any:
        return _call("list_tenants", "()", self.network)

    def tenant_count(self) -> int:
        r = _call("tenant_count", "()", self.network)
        if isinstance(r, str) and "nat64" in r:
            return int(r.split(":")[0].strip("() "))
        return 0

    # ── RBAC ────────────────────────────────────────────────────────

    def assign_role(self, principal: str, role: str,
                    tenant: Optional[str] = None) -> Any:
        t = f'opt "{tenant}"' if tenant else "null"
        return _call("assign_role", f'(principal "{principal}", variant {{ {role} }}, {t})', self.network)

    def remove_role(self, principal: str) -> Any:
        return _call("remove_role", f'(principal "{principal}")', self.network)

    def get_role(self, principal: str) -> Any:
        return _call("get_role", f'(principal "{principal}")', self.network)

    def list_roles(self) -> Any:
        return _call("list_roles", "()", self.network)

    # ── OIDC ────────────────────────────────────────────────────────

    def get_session(self, principal: str) -> Any:
        return _call("get_session", f'(principal "{principal}")', self.network)

    # ── Audit ───────────────────────────────────────────────────────

    def get_audit_log(self, tenant: str = "", start: int = 0, limit: int = 10) -> Any:
        return _call("get_audit_log", f'("{tenant}", {start} : nat64, {limit} : nat64)', self.network)

    def verify_audit_integrity(self) -> bool:
        r = _call("verify_audit_integrity", "()", self.network)
        return "true" in r if isinstance(r, str) else False

    # ── API Keys ────────────────────────────────────────────────────

    def create_api_key(self, tenant: str, rate_limit: int = 1000) -> Any:
        return _call("create_api_key", f'("{tenant}", {rate_limit} : nat64)', self.network)

    def revoke_api_key(self, key_id: str) -> Any:
        return _call("revoke_api_key", f'("{key_id}")', self.network)

    def list_api_keys(self, tenant: str = "") -> Any:
        return _call("list_api_keys", f'("{tenant}")', self.network)

    # ── Model Marketplace ──────────────────────────────────────────

    def list_models(self, provider: Optional[str] = None,
                    capability: Optional[str] = None) -> Any:
        p = f'opt "{provider}"' if provider else "null"
        c = f'opt "{capability}"' if capability else "null"
        return _call("list_models", f"({p}, {c})", self.network)

    def update_model_pricing(self, model_id: str, inp: int, out: int) -> Any:
        return _call("update_model_pricing", f'("{model_id}", {inp} : nat64, {out} : nat64)', self.network)

    # ── Reserves (GENIUS Act) ──────────────────────────────────────

    def get_reserve_state(self) -> Any:
        return _call("get_reserve_state", "()", self.network)

    def deposit_usdc(self, amount: int) -> Any:
        return _call("deposit_usdc", f"({amount} : nat64)", self.network)

    def attest_reserves(self) -> Any:
        return _call("attest_reserves", "()", self.network)

    # ── Metrics ─────────────────────────────────────────────────────

    def get_metrics(self) -> Any:
        return _call("get_metrics", "()", self.network)
