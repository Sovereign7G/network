"""SDK unit tests — BillingEngine, SLARouter.
Tests against the actual SDK code with mocked canister calls.

Run: PYTHONPATH="/media/cherry/4A21-00001/New folder/AGE REPUBLIC/hermes_home:$PYTHONPATH" python3 -m pytest tests/test_sdk.py -v
"""
import sys, os, pytest

SDK_PATH = "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/hermes_home"
sys.path.insert(0, SDK_PATH)

# ── BillingEngine Tests ────────────────────────────────────────────

class TestBillingEngine:
    def test_convert_100_usdc(self):
        from s7g_sdk.depin.billing import BillingEngine, CONVERSION_RATE
        assert CONVERSION_RATE == 1_000_000
        engine = BillingEngine.__new__(BillingEngine)
        assert engine.convert(100.0) == 100_000_000

    def test_convert_zero(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        assert engine.convert(0) == 0

    def test_discount_none(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        assert engine.discount(1_000) == 0.0

    def test_discount_10m(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        assert engine.discount(10_000_000) == 0.10

    def test_discount_100m(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        assert engine.discount(100_000_000) == 0.25

    def test_estimate_5m(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        result = engine.estimate(5_000_000)
        assert result["base_credits"] == 5_000_000
        assert result["discount"] == 0.0
        assert result["total_credits"] == 5_000_000
        assert result["usdc_needed"] == 5.0

    def test_estimate_with_bonus(self):
        from s7g_sdk.depin.billing import BillingEngine
        engine = BillingEngine.__new__(BillingEngine)
        result = engine.estimate(100_000_000)
        assert result["base_credits"] == 100_000_000
        assert result["discount"] == 0.25
        assert result["bonus"] == 25_000_000
        assert result["total_credits"] == 125_000_000

# ── SLARouter Tests ────────────────────────────────────────────────

class TestSLARouter:
    def test_router_available_returns_list(self):
        from s7g_sdk.depin.sla_router import SLARouter
        router = SLARouter.__new__(SLARouter)
        router.client = None
        # Mock list_models
        class MockClient:
            @staticmethod
            def list_models():
                return [{"model_id": "gpt-4o-openai", "provider": "OpenAI",
                         "model_name": "gpt-4o", "input_price": 2500000,
                         "p99_latency": 2000, "uptime": 99.9}]
        router.client = MockClient()
        models = router._available("test", "gpt-4o", max_latency=5000, min_uptime=99.0)
        assert len(models) > 0
        assert models[0]["provider"] == "OpenAI"

    def test_router_no_match(self):
        from s7g_sdk.depin.sla_router import SLARouter
        router = SLARouter.__new__(SLARouter)
        class EmptyClient:
            @staticmethod
            def list_models():
                return []
        router.client = EmptyClient()
        models = router._available("test", "nonexistent")
        assert len(models) == 0

    def test_router_cost_preference(self):
        from s7g_sdk.depin.sla_router import SLARouter
        router = SLARouter.__new__(SLARouter)
        class MockClient:
            @staticmethod
            def list_models():
                return [{"model_id": "m1", "provider": "P1", "model_name": "gpt-4o",
                         "input_price": 5000000, "p99_latency": 3000, "uptime": 99.5},
                        {"model_id": "m2", "provider": "P2", "model_name": "gpt-4o",
                         "input_price": 2500000, "p99_latency": 2000, "uptime": 99.9}]
        router.client = MockClient()
        result = router.route("tenant", "gpt-4o", "hello", preference="cost")
        assert result["provider"] == "P2"

    def test_router_latency_preference(self):
        from s7g_sdk.depin.sla_router import SLARouter
        router = SLARouter.__new__(SLARouter)
        class MockClient:
            @staticmethod
            def list_models():
                return [{"model_id": "m1", "provider": "Fast", "model_name": "gpt-4o",
                         "input_price": 5000000, "p99_latency": 500, "uptime": 99.9},
                        {"model_id": "m2", "provider": "Slow", "model_name": "gpt-4o",
                         "input_price": 1000000, "p99_latency": 5000, "uptime": 99.9}]
        router.client = MockClient()
        result = router.route("tenant", "gpt-4o", "hello", preference="latency")
        assert result["provider"] == "Fast"

    def test_router_invalid_preference(self):
        from s7g_sdk.depin.sla_router import SLARouter
        router = SLARouter.__new__(SLARouter)
        class EmptyClient:
            @staticmethod
            def list_models():
                return [{"model_id": "m1", "provider": "P1", "model_name": "m",
                         "input_price": 100, "p99_latency": 100, "uptime": 99.9}]
        router.client = EmptyClient()
        result = router.route("t", "m", "hello", preference="garbage")
        assert "error" in result

# ── Canister Integration Tests (live) ─────────────────────────────

class TestCanisterIntegration:
    def test_live_tenant_count(self):
        """Verify canister responds with a numeric count."""
        import subprocess
        r = subprocess.run(
            ["dfx", "canister", "call", "iemx3-niaaa-aaaad-ql7uq-cai",
             "tenant_count", "--network", "ic"],
            capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "nat64" in r.stdout, f"Unexpected: {r.stdout.strip()}"

    def test_live_audit_integrity(self):
        import subprocess
        r = subprocess.run(
            ["dfx", "canister", "call", "iemx3-niaaa-aaaad-ql7uq-cai",
             "verify_audit_integrity", "--network", "ic"],
            capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "true" in r.stdout.lower(), f"Unexpected: {r.stdout.strip()}"
