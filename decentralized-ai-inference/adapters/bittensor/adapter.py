"""
bittensor_adapter.py — OpenAI-compatible wrapper for Bittensor SN1 inference.
Routes /v1/chat/completions to Bittensor subnet 1 miners.
"""
import os, asyncio, json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Bittensor SN1 Adapter")

# ── Config ──────────────────────────────────────────────────────────────
# In production, use bt.wallet() + bt.subtensor() with real credentials
# For now, query public SN1 endpoints
SN1_ENDPOINT = os.getenv("SN1_ENDPOINT", "https://api.bittensor.com/sn1")
API_KEY = os.getenv("API_KEY", "")

# ── Models ──────────────────────────────────────────────────────────────

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "bittensor-sn1"
    messages: List[Message]
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

# ── Routes ──────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "adapter": "bittensor-sn1"}

@app.post("/v1/chat/completions")
async def chat_completion(req: ChatRequest):
    """Forward chat completion to Bittensor SN1."""
    prompt = req.messages[-1].content if req.messages else ""
    
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    payload = {
        "prompt": prompt,
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SN1_ENDPOINT}/v1/completions",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    return {
        "id": "bittensor-sn1",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": data.get("completion", data.get("text", ""))
            },
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
            "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
            "total_tokens": data.get("usage", {}).get("total_tokens", 0),
        },
    }

@app.post("/v1/completions")
async def completion(req: ChatRequest):
    """Standard completions endpoint (non-chat)."""
    prompt = req.messages[-1].content if req.messages else ""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    payload = {"prompt": prompt, "max_tokens": req.max_tokens}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SN1_ENDPOINT}/v1/completions", json=payload, headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    return {
        "id": "bittensor-sn1",
        "object": "text_completion",
        "choices": [{
            "index": 0,
            "text": data.get("completion", data.get("text", "")),
            "finish_reason": "stop",
        }],
    }
