"""SLA-aware model router — selects the cheapest/fastest/balanced model
from the on-chain model marketplace for each inference request.

Usage:
    python3 sla_router.py --tenant acme-corp --model gpt-4o --prompt "hello" --preference cost
    python3 sla_router.py --tenant acme-corp --model llama3-8b --preference latency
"""
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional

REGISTRY = "iemx3-niaaa-aaaad-ql7uq-cai"

@dataclass
class ModelOption:
    model_id: str; provider: str; model_name: str
    input_price: int; output_price: int; max_tokens: int
    capabilities: list; regions: list; p50_latency: int
    p99_latency: int; uptime: float; active: bool
    score: float = 0.0

def _fetch_models() -> list:
    """Fetch all registered models from the on-chain marketplace."""
    try:
        out = subprocess.check_output(
            ["dfx", "canister", "call", REGISTRY, "list_models",
             "(null, null)", "--network", "ic"],
            stderr=subprocess.STDOUT, timeout=15, text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return _parse_models(out)

def _model_price(m: ModelOption, tokens: int) -> int:
    return (m.input_price * tokens // 1_000_000) + (m.output_price * tokens // 1_000_000)

def route(tenant: str, model_name: str, prompt: str,
          preference: str = "cost", max_latency: int = 5000,
          min_uptime: float = 99.0) -> dict:
    """Route an inference request to the best model."""
    models = _fetch_models()
    candidates = [m for m in models if m.model_name == model_name
                  and m.active and m.p99_latency <= max_latency
                  and m.uptime >= min_uptime]
    if not candidates:
        return {"error": f"No models matching '{model_name}' meet SLA requirements"}
    if preference == "cost":
        selected = min(candidates, key=lambda m: m.input_price)
    elif preference == "latency":
        selected = min(candidates, key=lambda m: m.p99_latency)
    elif preference == "balanced":
        max_p = max(m.input_price for m in candidates) or 1
        max_l = max(m.p99_latency for m in candidates) or 1
        for m in candidates:
            m.score = (m.input_price / max_p) * 0.5 + (m.p99_latency / max_l) * 0.5
        selected = min(candidates, key=lambda m: m.score)
    else:
        return {"error": f"Unknown preference '{preference}'"}
    return {
        "tenant": tenant, "model": selected.model_name,
        "provider": selected.provider,
        "cost_per_million": selected.input_price,
        "p99_latency_ms": selected.p99_latency,
        "uptime_pct": selected.uptime,
        "preference": preference,
    }

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--tenant", default="acme-corp")
    p.add_argument("--model", required=True)
    p.add_argument("--prompt", default="")
    p.add_argument("--preference", choices=["cost","latency","balanced"], default="cost")
    p.add_argument("--max-latency", type=int, default=5000)
    p.add_argument("--min-uptime", type=float, default=99.0)
    args = p.parse_args()
    result = route(args.tenant, args.model, args.prompt,
                   args.preference, args.max_latency, args.min_uptime)
    print(json.dumps(result, indent=2))
