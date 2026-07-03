#!/usr/bin/env python3
"""FastAPI proxy with billing + multi-provider fallback + audit."""
from fastapi import FastAPI, HTTPException, Header, Body
from typing import Optional
import uuid, time, json, os, sqlite3

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
    {"name": "s7g-committee", "url": "https://s7g-committee.onrender.com/propose"},
    {"name": "bittensor-sn1", "url": "https://bittensor-adapter.onrender.com/v1/chat/completions"},
    {"name": "icp-llama", "url": "https://llm-canister.icp0.io/v1/chat/completions"},
]

@app.post("/v1/chat/completions")
async def chat_completions(request: dict = Body(...), authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid API key")
    api_key = authorization.replace("Bearer ", "")
    cid = billing.get_customer_by_key(api_key)
    if not cid: raise HTTPException(401, "Invalid API key")
    bal = billing.check_balance(cid)
    if bal <= 0: raise HTTPException(402, "Insufficient credits")
    rid = str(uuid.uuid4())
    messages = request.get("messages", [])
    tokens = estimate_tokens(messages)
    cost = calculate_cost(tokens)
    if bal < cost: raise HTTPException(402, f"Insufficient — need ${cost:.4f}, have ${bal:.4f}")

    last_error = None
    for provider in PROVIDERS:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(provider["url"], json=request)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            last_error = str(e)[:100]
            continue
        billing.deduct_usage(cid, rid, tokens, cost)
        prompt = messages[-1].get("content", "") if messages else ""
        audit.log(rid, cid, provider["name"], prompt, json.dumps(data), tokens, cost, data.get("committee_signatures", [None])[0] or "")
        return {
            "id": rid, "object": "chat.completion", "created": int(time.time()),
            "model": provider["name"],
            "choices": [{"index": 0, "message": {"role": "assistant", "content": json.dumps(data)}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": tokens, "total_tokens": tokens, "cost": cost},
            "provenance": {"provider": provider["name"], "signatures": data.get("committee_signatures", [])}
        }
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
