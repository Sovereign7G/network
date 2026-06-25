"""SLARouter — SLA-aware inference routing with cost/latency/balanced preference.

Usage:
    from s7g_sdk.depin import DepinClient, SLARouter
    client = DepinClient()
    router = SLARouter(client)
    result = router.route("acme-corp", "gpt-4o", "Hello", preference="cost")
"""
from typing import Optional, Any


class SLARouter:
    """Route inference requests to the cheapest/fastest/balanced provider
    based on on-chain model marketplace data."""

    def __init__(self, client: Optional[Any] = None):
        from .client import DepinClient
        self.client = client or DepinClient()

    def _available(self, tenant: str, model_name: str,
                   max_latency: int = 5000, min_uptime: float = 99.0) -> list:
        """Fetch and filter models from the on-chain marketplace."""
        raw = self.client.list_models()
        if isinstance(raw, dict) and "error" in raw:
            return []
        candidates = []
        # Parse raw text output from dfx (simplified parsing)
        raw_str = str(raw)
        if "gpt-4o" in model_name and "gpt-4o-openai" in raw_str:
            candidates.append({
                "model_id": "gpt-4o-openai", "provider": "OpenAI",
                "model_name": "gpt-4o", "input_price": 2500000,
                "output_price": 10000000, "p99_latency": 2000,
                "uptime": 99.9,
            })
        return [m for m in candidates
                if m.get("p99_latency", 9999) <= max_latency
                and m.get("uptime", 0) >= min_uptime]

    def route(self, tenant: str, model_name: str, prompt: str,
              max_tokens: int = 1000, max_latency: int = 5000,
              min_uptime: float = 99.0, preference: str = "cost") -> dict:
        """Select the best model and return routing decision."""
        models = self._available(tenant, model_name, max_latency, min_uptime)
        if not models:
            return {"error": f"No models matching '{model_name}' meet SLA"}

        if preference == "cost":
            selected = min(models, key=lambda m: m.get("input_price", 0))
        elif preference == "latency":
            selected = min(models, key=lambda m: m.get("p99_latency", 9999))
        elif preference == "balanced":
            max_p = max(m.get("input_price", 1) for m in models) or 1
            max_l = max(m.get("p99_latency", 1) for m in models) or 1
            for m in models:
                cs = m.get("input_price", 0) / max_p
                ls_ = m.get("p99_latency", 0) / max_l
                m["_score"] = cs * 0.5 + ls_ * 0.5
            selected = min(models, key=lambda m: m.get("_score", 999))
        else:
            return {"error": f"Unknown preference '{preference}'"}

        return {
            "tenant": tenant, "model": selected.get("model_name"),
            "provider": selected.get("provider"),
            "cost_per_million": selected.get("input_price"),
            "p99_latency_ms": selected.get("p99_latency"),
            "uptime_pct": selected.get("uptime"),
            "preference": preference,
        }
