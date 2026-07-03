"""
bittensor_adapter.py — OpenAI-compatible wrapper for Bittensor SN1 inference.
Routes /v1/chat/completions to Bittensor subnet 1 miners.
Mock mode enabled by default — set MOCK_MODE=false and SN1_API_KEY for real inference.
"""
import os, json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Bittensor SN1 Adapter")

# ── Config ──────────────────────────────────────────────────────────────
SN1_ENDPOINT = os.getenv("SN1_ENDPOINT", "https://sn1.api.macrocosmos.ai")
SN1_API_KEY = os.getenv("SN1_API_KEY", "")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

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
    return {"status": "ok", "adapter": "bittensor-sn1", "mock_mode": MOCK_MODE}

@app.post("/v1/chat/completions")
async def chat_completion(req: ChatRequest):
    """Forward chat completion to Bittensor SN1 or return mock response."""
    prompt = req.messages[-1].content if req.messages else ""
    
    if MOCK_MODE:
        return {
            "id": "bittensor-sn1-mock",
            "object": "chat.completion",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"This is a mock response from Bittensor SN1 adapter.\n\nYou asked: \"{prompt}\"\n\nTo enable real inference, set MOCK_MODE=false and SN1_API_KEY in the Render environment variables."
                },
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
    
    headers = {"Content-Type": "application/json"}
    if SN1_API_KEY:
        headers["Authorization"] = f"Bearer {SN1_API_KEY}"
    
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
    
    if MOCK_MODE:
        return {
            "id": "bittensor-sn1-mock",
            "object": "text_completion",
            "choices": [{
                "index": 0,
                "text": f"Mock response. Prompt: \"{prompt}\"",
                "finish_reason": "stop",
            }],
        }
    
    headers = {"Content-Type": "application/json"}
    if SN1_API_KEY:
        headers["Authorization"] = f"Bearer {SN1_API_KEY}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SN1_ENDPOINT}/v1/completions",
                json={"prompt": prompt, "max_tokens": req.max_tokens},
                headers=headers,
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
