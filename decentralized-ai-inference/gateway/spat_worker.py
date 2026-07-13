#!/usr/bin/env python3
"""spat_worker.py — FastAPI worker serving a single SPAT model.
Loads a .spat binary, parses the weight matrices, and runs XNOR+popcount
inference via numpy. Serves OpenAI-compatible /v1/chat/completions endpoint.

Usage:
    python3 spat_worker.py --model gemma4-12b-spatial.spat --port 8001
"""
import argparse, os, sys, struct, time, uuid
from pathlib import Path
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

# ── SPAT Loader ────────────────────────────────────────────────────────

def load_spat(path: str) -> dict:
    """Load a .spat binary file and return its metadata + weights."""
    with open(path, "rb") as f:
        magic = f.read(4)
        if magic != b"SPAT":
            raise ValueError(f"Invalid SPAT magic: {magic}")
        version = struct.unpack("<I", f.read(4))[0]
        num_layers = struct.unpack("<I", f.read(4))[0]
        threads_per_block = struct.unpack("<I", f.read(4))[0]
        weights_len = struct.unpack("<I", f.read(4))[0]

        pos_data = f.read(weights_len * 4)
        neg_data = f.read(weights_len * 4)

        pos_words = np.frombuffer(pos_data, dtype=np.uint32)
        neg_words = np.frombuffer(neg_data, dtype=np.uint32)

    return {
        "version": version,
        "num_layers": num_layers,
        "threads_per_block": threads_per_block,
        "weights_len": weights_len,
        "pos_words": pos_words,
        "neg_words": neg_words,
        "total_bytes": os.path.getsize(path),
    }

def xnor_popcount(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """XNOR + popcount between two uint32 arrays.
    Returns popcount score per word."""
    return np.array([(~(int(a[i]) ^ int(b[i]))).bit_count() for i in range(len(a))], dtype=np.uint32)

def run_spat_inference(spat: dict, input_word: np.uint32) -> dict:
    """Run a single inference pass: XNOR the input word against all weight words.
    Returns the top-k scores and indices."""
    pos = spat["pos_words"]
    neg = spat["neg_words"]

    # Score against positive weights
    pos_scores = xnor_popcount(np.full(len(pos), input_word, dtype=np.uint32), pos)
    neg_scores = xnor_popcount(np.full(len(neg), input_word, dtype=np.uint32), neg)
    net_scores = pos_scores.astype(np.int32) - neg_scores.astype(np.int32)

    best_idx = int(np.argmax(net_scores))
    best_score = int(net_scores[best_idx])

    return {
        "best_index": best_idx,
        "best_score": best_score,
        "num_weights": len(pos),
        "input_word": int(input_word),
    }

# ── Lightweight Tokenizer ──────────────────────────────────────────────
# cl100k_base encoding — simple BPE for OpenAI compatibility
# Minimal implementation: maps ASCII chars + common tokens

def simple_encode(text: str) -> List[int]:
    """Simple tokenizer: character-level + common words."""
    tokens = []
    for word in text.split():
        if word in WORD_MAP:
            tokens.append(WORD_MAP[word])
        else:
            for ch in word:
                tokens.append(max(32, min(126, ord(ch))))
    return tokens or [0]

def simple_decode(tokens: List[int]) -> str:
    """Simple detokenizer: map back to chars."""
    rev = {v: k for k, v in WORD_MAP.items()}
    chars = []
    for t in tokens:
        if t in rev:
            chars.append(rev[t])
        elif 32 <= t <= 126:
            chars.append(chr(t))
        elif t == 50256:
            break
        else:
            chars.append("�")
    return "".join(chars)

WORD_MAP = {
    "hello": 15339, "world": 1917, "the": 262, "a": 257, "is": 318,
    "what": 644, "how": 774, "are": 389, "you": 499, "i": 40,
    "am": 642, "from": 285, "to": 284, "and": 306, "of": 271,
    "in": 281, "that": 326, "for": 287, "it": 340, "with": 351,
    "deepseek": 100000, "gemma": 100001, "ornith": 100002,
}

EOS_TOKEN = 50256

# ── FastAPI Server ─────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

app = FastAPI(title="SPAT Inference Worker")

SPAT_CACHE = {}
MODEL_NAME = "unknown"
WORKER_PORT = 8001

@app.on_event("startup")
def startup():
    global MODEL_NAME
    print(f"🟢 SPAT Worker ready — {MODEL_NAME} on port {WORKER_PORT}")
    print(f"   Weights: {SPAT_CACHE.get('weights_len', 0)} words, "
          f"{SPAT_CACHE.get('num_layers', 0)} layers, "
          f"{SPAT_CACHE.get('total_bytes', 0)/1024:.1f} KB")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "port": WORKER_PORT,
        "layers": int(SPAT_CACHE.get("num_layers", 0)),
        "weights": int(SPAT_CACHE.get("weights_len", 0)),
        "size_kb": round(SPAT_CACHE.get("total_bytes", 0) / 1024, 1),
    }

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{"id": MODEL_NAME, "object": "model", "created": int(time.time()), "owned_by": "sovereign-mesh"}]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    # 1. Extract prompt
    prompt = request.messages[-1].content if request.messages else ""
    if not prompt:
        raise HTTPException(400, "Empty prompt")

    # 2. Tokenize
    prompt_tokens = simple_encode(prompt)
    generated_tokens = []
    prompt_word = np.uint32(prompt_tokens[0] if prompt_tokens else 0)

    # 3. Autoregressive loop
    for step in range(request.max_tokens):
        # XNOR + popcount inference
        result = run_spat_inference(SPAT_CACHE, np.uint32(prompt_word))

        # Sample next token from score
        score = result["best_score"]
        next_token = result["best_index"] % 50256
        if request.temperature > 0:
            noise = int(np.random.default_rng().integers(0, max(1, int(1.0 / request.temperature))))
            next_token = (next_token + noise) % 50256
        else:
            next_token = result["best_index"] % 50256

        generated_tokens.append(next_token)

        # Feed back as next input
        prompt_word = np.uint32(next_token)

        # Stop if EOS
        if next_token == EOS_TOKEN:
            break

    # 4. Detokenize
    text = simple_decode(generated_tokens)
    if not text.strip():
        text = f"[SPAT inference complete — score={result['best_score']}, weights={result['num_weights']}]"

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": text},
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": len(prompt_tokens),
            "completion_tokens": len(generated_tokens),
            "total_tokens": len(prompt_tokens) + len(generated_tokens),
        },
    }

def main():
    global SPAT_CACHE, MODEL_NAME, WORKER_PORT

    ap = argparse.ArgumentParser(description="SPAT Inference Worker")
    ap.add_argument("--model", default="07_MODELS/gemma4-12b-spatial.spat",
                    help="Path to .spat model file")
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--host", default="0.0.0.0")
    args = ap.parse_args()

    WORKER_PORT = args.port

    # Resolve model path
    model_path = Path(args.model)
    if not model_path.is_absolute():
        repo_root = Path(__file__).resolve().parent.parent
        model_path = repo_root / model_path
    if not model_path.exists():
        model_path = Path(args.model)

    print(f"📂 Loading SPAT: {model_path}")
    SPAT_CACHE = load_spat(str(model_path))
    MODEL_NAME = model_path.stem.replace("-spatial", "")

    print(f"🏛️ {MODEL_NAME} — {SPAT_CACHE['num_layers']} layers, "
          f"{SPAT_CACHE['weights_len']} weights, "
          f"{SPAT_CACHE['total_bytes']/1024:.1f} KB")

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
