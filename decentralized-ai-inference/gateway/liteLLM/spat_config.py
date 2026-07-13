"""SPAT model registry — maps model names to local worker ports.
Used by proxy.py for routing SPAT inference requests to GT80S workers."""
SPAT_WORKERS = {
    "gemma-4-12b":    {"port": 8001, "tier": "Tier 1: Edge",      "size_kb": 96.0},
    "ornith-1.0-9b":  {"port": 8002, "tier": "Tier 1: Edge",      "size_kb": 2.1},
    "glm-5.2":        {"port": 8003, "tier": "Tier 2: Consumer",  "size_kb": 4.9},
    "ornith-1.0-35b": {"port": 8004, "tier": "Tier 2: Consumer",  "size_kb": 2.6},
    "minimax-m3":     {"port": 8005, "tier": "Tier 3: Flagship",  "size_kb": 3.8},
    "ornith-1.0-397b":{"port": 8006, "tier": "Tier 3: Flagship",  "size_kb": 2.6},
    "deepseek-v4":    {"port": 8007, "tier": "Tier 3: Flagship",  "size_kb": 2.8},
}

# ICP SPAT inference canister — proof verification
SPAT_CANISTER_ID = "4ee45-7yaaa-aaaaa-qhlbq-cai"

# Worker host (GT80S or localhost)
WORKER_HOST = "localhost"

def is_spat_model(model: str) -> bool:
    return model in SPAT_WORKERS

def get_worker_url(model: str) -> str:
    info = SPAT_WORKERS.get(model)
    if not info:
        raise KeyError(f"Unknown SPAT model: {model}")
    return f"http://{WORKER_HOST}:{info['port']}"
