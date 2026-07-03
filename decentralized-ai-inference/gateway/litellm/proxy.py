"""
proxy.py — Lightweight OpenAI-compatible proxy for S7G inference.
Forwards /v1/chat/completions to the S7G committee.
~50MB image, runs on Render free tier.
"""
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="S7G Proxy")

S7G_API = os.getenv("S7G_API_URL", "https://s7g-committee.onrender.com")
MASTER_KEY = os.getenv("MASTER_API_KEY", "")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "s7g-committee"
    messages: List[Message]

@app.get("/health")
async def health():
    return {"status": "ok", "proxy": "s7g", "upstream": S7G_API}

@app.get("/v1/models")
async def list_models():
    return {"data": [{"id": "s7g-committee", "object": "model"}]}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    prompt = req.messages[-1].content if req.messages else ""
    payload = {"request_id": f"proxy-{os.urandom(4).hex()}", "payload": {"prompt": prompt, "model": req.model}}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{S7G_API}/propose", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    return {
        "id": data.get("proposal_id", "s7g-proxy"),
        "object": "chat.completion",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": str(data)}, "finish_reason": "stop"}],
    }
