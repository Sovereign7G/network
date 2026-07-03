#!/usr/bin/env python3
"""FastAPI proxy with billing + S7G committee integration."""
from fastapi import FastAPI, HTTPException, Header, Body
from typing import Optional
import uuid, time, json

from billing import BillingDB
from s7g_client import S7GClient
import sqlite3

FIXED_KEY = "s7g-demo-key-001"

def _ensure_demo_key():
    """Create demo customer with fixed API key on startup if missing."""
    try:
        with sqlite3.connect("billing.db") as conn:
            exists = conn.execute("SELECT 1 FROM api_keys WHERE key=?", (FIXED_KEY,)).fetchone()
            if not exists:
                cid = "demo-customer-001"
                now = int(__import__('time').time())
                conn.execute("INSERT INTO customers VALUES (?,?,?,?)", (cid, "Demo User", "demo@s7g.ai", now))
                conn.execute("INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?,?,?,?)", (FIXED_KEY, cid, "default", now))
                conn.execute("INSERT INTO balances VALUES (?,?,?)", (cid, 10.0, now))
                conn.commit()
                print(f"Created demo key: {FIXED_KEY} ($10.00)")
    except Exception as e:
        print(f"Demo key setup: {e}")

_ensure_demo_key()

app = FastAPI(title="Sovereign AI Gateway", version="1.0.0")
billing = BillingDB("billing.db")
s7g = S7GClient("https://s7g-committee.onrender.com", timeout=35.0)
PRICE_PER_1K = 0.001

def estimate_tokens(messages: list) -> int:
    return sum(len(m.get("content", "").split()) * 1.3 for m in messages) + 10

def calculate_cost(tokens: int) -> float:
    return (tokens / 1000.0) * PRICE_PER_1K

@app.post("/v1/chat/completions")
async def chat_completions(request: dict = Body(...), authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid API key")
    api_key = authorization.replace("Bearer ", "")
    cid = billing.get_customer_by_key(api_key)
    if not cid:
        raise HTTPException(401, "Invalid API key")
    bal = billing.check_balance(cid)
    if bal <= 0:
        raise HTTPException(402, "Insufficient credits")
    rid = str(uuid.uuid4())
    messages = request.get("messages", [])
    tokens = int(estimate_tokens(messages))
    cost = calculate_cost(tokens)
    if bal < cost:
        raise HTTPException(402, f"Insufficient — need ${cost:.4f}, have ${bal:.4f}")
    try:
        s7g_resp = await s7g.propose(rid, {
            "model": request.get("model", "s7g-committee"),
            "messages": messages,
            "temperature": request.get("temperature", 0.7),
            "max_tokens": request.get("max_tokens", 1000)
        })
    except Exception as e:
        detail = str(e)
        if "timeout" in detail.lower():
            raise HTTPException(504, "Committee timeout (cold start ~10-15s)")
        raise HTTPException(502, f"S7G error: {detail[:200]}")
    if not billing.deduct_usage(cid, rid, tokens, cost):
        raise HTTPException(500, "Failed to deduct credits")
    return {
        "id": rid, "object": "chat.completion", "created": int(time.time()),
        "model": request.get("model", "s7g-committee"),
        "choices": [{"index": 0, "message": {"role": "assistant", "content": str(s7g_resp)}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": tokens, "completion_tokens": 0, "total_tokens": tokens, "cost": cost},
        "provenance": {
            "proposal_id": s7g_resp.get("proposal_id"),
            "status": s7g_resp.get("status"),
            "committee_signatures": s7g_resp.get("committee_signatures", [])
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Sovereign AI Gateway"}

@app.get("/status")
async def status():
    s = await s7g.status()
    return {"gateway": "ok", "committee": s}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1317)
