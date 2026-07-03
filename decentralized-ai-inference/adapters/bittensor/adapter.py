"""
bittensor_adapter.py — OpenAI-compatible wrapper for Bittensor SN1 (Apex) inference.
Connects to the Macrocosmos Subnet 1 gateway. Requires SN1_API_KEY.
"""
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Bittensor SN1 Adapter")

# ── Config ──────────────────────────────────────────────────────────────
SN1_ENDPOINT = os.getenv("SN1_ENDPOINT", "https://sn1.api.macrocosmos.ai")
SN1_API_KEY = os.getenv("SN1_API_KEY", "")

# ── Models ──────────────────────────────────────────────────────────────

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "bittensor-sn1"
    messages: List[Message]
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7

# ── Routes ──────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    api_key_set = bool(SN1_API_KEY)
    return {"status": "ok", "adapter": "bittensor-sn1", "api_key_set": api_key_set, "endpoint": SN1_ENDPOINT}

@app.post("/v1/chat/completions")
async def chat_completion(req: ChatRequest):
    prompt = req.messages[-1].content if req.messages else ""
    
    if not SN1_API_KEY:
        raise HTTPException(status_code=401, detail="SN1_API_KEY not configured. Get one from https://sn1.api.macrocosmos.ai")
    headers = {"Content-Type": "application/json"}
    if SN1_API_KEY:
        headers["Authorization"] = f"Bearer {SN1_API_KEY}"
    
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SN1_ENDPOINT}/v1/chat/completions",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"SN1 upstream error: {e.response.text[:500]}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    completion_text = data.get("choices", [{}])[0].get("message", {}).get("content", data.get("completion", ""))
    
    return {
        "id": "bittensor-sn1",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": completion_text},
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
    if not SN1_API_KEY:
        raise HTTPException(status_code=401, detail="SN1_API_KEY not configured")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {SN1_API_KEY}"}
    prompt = req.messages[-1].content if req.messages else ""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SN1_ENDPOINT}/v1/chat/completions",
                json={"model": "meta-llama/Llama-3.2-3B-Instruct", "messages": [{"role": "user", "content": prompt}], "max_tokens": req.max_tokens},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {
        "id": "bittensor-sn1", "object": "text_completion",
        "choices": [{"index": 0, "text": content, "finish_reason": "stop"}],
    }
