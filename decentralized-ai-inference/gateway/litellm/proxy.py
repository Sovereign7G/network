#!/usr/bin/env python3
"""FastAPI proxy with billing + multi-provider fallback + audit + rate limiting + Prometheus metrics."""
from fastapi import FastAPI, HTTPException, Header, Body, Request
from fastapi.responses import Response
from typing import Optional
import uuid, time, json, os, sqlite3, collections

from billing import BillingDB
from s7g_client import S7GClient
from audit import AuditDB
from audit_routes import router as audit_router
from agent_routes import router as agent_router

FIXED_KEY = "s7g-demo-key-001"

def _ensure_demo_key():
    db_path = os.getenv("BILLING_DB_PATH", "billing.db")
    try:
        with sqlite3.connect(db_path) as conn:
            exists = conn.execute("SELECT 1 FROM api_keys WHERE key=?", (FIXED_KEY,)).fetchone()
            if not exists:
                cid = "demo-customer-001"; now = int(time.time())
                conn.execute("INSERT INTO customers VALUES (?,?,?,?)", (cid, "Demo User", "demo@s7g.ai", now))
                conn.execute("INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?,?,?,?)", (FIXED_KEY, cid, "default", now))
                conn.execute("INSERT INTO balances VALUES (?,?,?)", (cid, 10.0, now))
                conn.commit(); print(f"Created demo key: {FIXED_KEY} ($10.00)")
    except Exception as e: print(f"Demo key setup: {e}")

_ensure_demo_key()
app = FastAPI(title="Sovereign AI Gateway", version="1.0.0")
app.include_router(audit_router)
app.include_router(agent_router)
_db_path = os.getenv("BILLING_DB_PATH", "billing.db")
billing = BillingDB(_db_path)
s7g = S7GClient("https://s7g-committee.onrender.com", timeout=35.0)
audit = AuditDB("audit.db")
PRICE_PER_1K = 0.001

def estimate_tokens(messages: list) -> int:
    return int(sum(len(m.get("content", "").split()) * 1.3 for m in messages) + 10)

def calculate_cost(tokens: int) -> float:
    return (tokens / 1000.0) * PRICE_PER_1K

PROVIDERS = [
    {"name": "s7g-committee", "url": "https://s7g-committee.onrender.com/propose", "format": "s7g"},
    {"name": "bittensor-sn1", "url": "https://bittensor-adapter.onrender.com/v1/chat/completions", "format": "openai"},
]

# ── Rate Limiting ─────────────────────────────────────────────────────
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))  # requests per window
RATE_WINDOW = int(os.getenv("RATE_WINDOW", "60"))  # seconds
_rate_store: dict = {}

def _check_rate(key: str) -> bool:
    now = time.time()
    window = int(now / RATE_WINDOW)
    k = f"{key}:{window}"
    _rate_store[k] = _rate_store.get(k, 0) + 1
    # gc old windows
    if len(_rate_store) > 10000:
        cutoff = int(now / RATE_WINDOW) - 2
        for wk in list(_rate_store):
            if int(wk.split(":")[-1]) < cutoff:
                del _rate_store[wk]
    return _rate_store[k] <= RATE_LIMIT

# ── Prometheus Metrics ────────────────────────────────────────────────
_metrics = {
    "requests_total": 0, "requests_success": 0, "requests_error": 0,
    "tokens_total": 0, "cost_total": 0.0, "provider_hits": {},
}

@app.get("/metrics")
async def metrics():
    body = []
    body.append(f"# HELP s7g_requests_total Total requests")
    body.append(f"# TYPE s7g_requests_total counter")
    body.append(f"s7g_requests_total {_metrics['requests_total']}")
    body.append(f"s7g_requests_success {_metrics['requests_success']}")
    body.append(f"s7g_requests_error {_metrics['requests_error']}")
    body.append(f"s7g_tokens_total {_metrics['tokens_total']}")
    body.append(f"s7g_cost_total {_metrics['cost_total']}")
    for p, h in _metrics.get("provider_hits", {}).items():
        body.append(f"s7g_provider_hits{{provider=\"{p}\"}} {h}")
    return Response(content="\n".join(body), media_type="text/plain")

@app.post("/v1/chat/completions")
async def chat_completions(request: dict = Body(...), authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid API key")
    api_key = authorization.replace("Bearer ", "")
    cid = billing.get_customer_by_key(api_key)
    if not cid: raise HTTPException(401, "Invalid API key")
    if not _check_rate(api_key):
        raise HTTPException(429, "Rate limit exceeded")
    bal = billing.check_balance(cid)
    if bal <= 0: raise HTTPException(402, "Insufficient credits")
    rid = str(uuid.uuid4())
    messages = request.get("messages", [])
    tokens = estimate_tokens(messages)
    cost = calculate_cost(tokens)
    if bal < cost: raise HTTPException(402, f"Insufficient — need ${cost:.4f}, have ${bal:.4f}")

    _metrics["requests_total"] += 1
    last_error = None
    for provider in PROVIDERS:
        try:
            import httpx
            if provider["format"] == "s7g":
                body = {"request_id": rid, "payload": request}
            else:
                body = request
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(provider["url"], json=body)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            last_error = str(e)[:100]
            continue
        _metrics["requests_success"] += 1
        _metrics["tokens_total"] += tokens
        _metrics["cost_total"] += cost
        pname = provider["name"]
        _metrics["provider_hits"][pname] = _metrics["provider_hits"].get(pname, 0) + 1
        billing.deduct_usage(cid, rid, tokens, cost)
        prompt = messages[-1].get("content", "") if messages else ""
        audit.log(rid, cid, pname, prompt, json.dumps(data), tokens, cost, data.get("committee_signatures", [None])[0] or "")
        return {
            "id": rid, "object": "chat.completion", "created": int(time.time()),
            "model": pname,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": json.dumps(data)}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": tokens, "total_tokens": tokens, "cost": cost},
            "provenance": {"provider": pname, "signatures": data.get("committee_signatures", [])}
        }
    _metrics["requests_error"] += 1
    raise HTTPException(503, f"All providers failed. Last error: {last_error}")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Sovereign AI Gateway", "providers": len(PROVIDERS)}

@app.get("/status")
async def status():
    s = {}
    for p in PROVIDERS:
        try:
            import httpx; r = await httpx.AsyncClient(timeout=5.0).get(p["url"].replace("/propose","").replace("/v1/chat/completions","") + "/health")
            s[p["name"]] = "up" if r.status_code == 200 else f"error {r.status_code}"
        except: s[p["name"]] = "unreachable"
    return {"gateway": "ok", "providers": s}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="0.0.0.0", port=1317)
