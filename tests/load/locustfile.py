"""Locust load test for S7G registry canister.
Usage: locust -f tests/load/locustfile.py --host=https://icp0.io --users=20 --spawn-rate=5
"""
from locust import HttpUser, task, between
import subprocess, json

CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"

def dfx_call(method, args="()"):
    cmd = ["dfx", "canister", "call", CANISTER, method, args, "--network", "ic"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.returncode == 0, r.stdout.strip()

class CanisterUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task(5)
    def query_tenant_count(self):
        ok, _ = dfx_call("tenant_count")

    @task(3)
    def query_audit_integrity(self):
        ok, _ = dfx_call("verify_audit_integrity")

    @task(3)
    def query_metrics(self):
        ok, _ = dfx_call("get_metrics")

    @task(2)
    def query_reserves(self):
        ok, _ = dfx_call("get_reserve_state")

    @task(2)
    def query_models(self):
        ok, _ = dfx_call("list_models", '(null, null)')

    @task(1)
    def query_roles(self):
        ok, _ = dfx_call("list_roles")
