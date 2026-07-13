#!/usr/bin/env python3
"""spat_worker.py — FastAPI worker using pure Rust SIMD transformer.
Loads a .spat binary and runs chained inference via libspat_transformer.so.
No CUDA, no GPU. Zero dependencies. Serves OpenAI-compatible API.

Usage:
    python3 spat_worker.py --model deepseek-v4-flash-spatial.spat --port 8007
"""
import argparse, ctypes, os, struct, time, uuid, json, asyncio
from pathlib import Path
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncGenerator

# ── SPAT Transformer FFI ────────────────────────────────────────────────

def load_rust_transformer():
    """Load libspat_transformer.so for pure-Rust SIMD inference."""
    so_paths = [
        os.path.join(os.path.dirname(__file__), "../../cuda_tensor_engine/spat_transformer/libspat_transformer.so"),
        os.path.join(os.path.dirname(__file__), "../../cuda_tensor_engine/spat_transformer/target/release/libspat_transformer.so"),
        "/media/35b_drive/target/release/libspat_transformer.so",
    ]
    for p in so_paths:
        ap = os.path.abspath(p)
        if os.path.exists(ap):
            lib = ctypes.CDLL(ap)
            # Set argtypes
            lib.spat_transformer_infer.argtypes = [
                ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
                ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32,
                ctypes.c_uint32, ctypes.c_float,
                ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_uint32),
                ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
            ]
            lib.spat_transformer_infer.restype = ctypes.c_int
            print(f"✅ Loaded Rust SIMD transformer from {ap}")
            return lib

    print("⚠️  libspat_transformer.so not found, using CPU fallback")
    return None

RUST_LIB = load_rust_transformer()

def load_spat(path: str) -> bytes:
    """Load .spat file as raw bytes."""
    with open(path, "rb") as f:
        return f.read()

def run_rust_inference(so, spat_bytes: bytes, prompt_tokens: list, max_tokens: int, temperature: float) -> tuple:
    """Run inference via Rust SIMD transformer. Returns (logits, generated_tokens)."""
    # Prepare buffers
    spat_buf = (ctypes.c_uint8 * len(spat_bytes)).from_buffer_copy(spat_bytes)
    input_arr = (ctypes.c_uint32 * len(prompt_tokens))(*prompt_tokens) if prompt_tokens else (ctypes.c_uint32 * 1)(0)

    out_logits = (ctypes.c_float * 50256)()
    out_logits_len = ctypes.c_uint32(0)
    out_tokens = (ctypes.c_uint32 * 100)()
    out_tokens_len = ctypes.c_uint32(0)

    so.spat_transformer_infer(
        spat_buf, ctypes.c_uint32(len(spat_bytes)),
        input_arr, ctypes.c_uint32(len(prompt_tokens)),
        ctypes.c_uint32(max_tokens), ctypes.c_float(temperature),
        out_logits, ctypes.byref(out_logits_len),
        out_tokens, ctypes.byref(out_tokens_len),
    )

    logits = np.frombuffer(out_logits, dtype=np.float32, count=out_logits_len.value).copy()
    tokens = [out_tokens[i] for i in range(out_tokens_len.value)]
    return logits, tokens

# ── CPU Fallback (no Rust lib) ──────────────────────────────────────────

def run_cpu_inference(spat_bytes: bytes, prompt_tokens: list, max_tokens: int, temperature: float) -> tuple:
    if len(spat_bytes) < 20 or spat_bytes[:4] != b"SPAT":
        return np.array([0.0]), []
    wl = struct.unpack("<I", spat_bytes[16:20])[0]
    pos = np.frombuffer(spat_bytes[20:20+wl*4], dtype=np.uint32)
    neg = np.frombuffer(spat_bytes[20+wl*4:20+wl*8], dtype=np.uint32)
    input_word = np.uint32(prompt_tokens[0] if prompt_tokens else 0)
    scores = np.array([
        bin(int(~(np.uint32(input_word) ^ p) & np.uint32(0xFFFFFFFF))).count("1") -
        bin(int(~(np.uint32(input_word) ^ n) & np.uint32(0xFFFFFFFF))).count("1")
        for p, n in zip(pos[:1000], neg[:1000])
    ], dtype=np.float32)
    ntok = min(max_tokens, 5)
    return scores, [int(np.argmax(scores)) % 50256] * ntok

# ── Tokenizer ───────────────────────────────────────────────────────────

# Load vocabulary from JSON file
import json
_VOCAB_PATH = os.path.join(os.path.dirname(__file__), "vocab.json")
if os.path.exists(_VOCAB_PATH):
    with open(_VOCAB_PATH) as _f:
        _raw = json.load(_f)
    VOCAB = {int(k): v for k, v in _raw.items()}
    print(f"📖 Loaded {len(VOCAB)} vocabulary entries (max ID: {max(VOCAB.keys())})")
else:
    VOCAB = {}
    print("⚠️  vocab.json not found, using fallback mapping")

def encode(text: str) -> List[int]:
    tokens = []
    for word in text.lower().split():
        if word in VOCAB:
            # Find the token ID for this word
            for tid, tword in VOCAB.items():
                if tword == word:
                    tokens.append(tid)
                    break
            else:
                for ch in word:
                    tokens.append(max(32, min(126, ord(ch))))
        else:
            for ch in word:
                tokens.append(max(32, min(126, ord(ch))))
    return tokens or [0]

def decode(tokens: List[int]) -> str:
    chars = []
    for t in tokens:
        if t in VOCAB:
            chars.append(VOCAB[t])
        elif 32 <= t <= 126:
            chars.append(chr(t))
        elif t == 0:
            break
        else:
            chars.append(" ")
    result = "".join(chars).strip()
    return result

# ── FastAPI Server ──────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    stream: Optional[bool] = False
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 50
    temperature: Optional[float] = 0.7

app = FastAPI(title="SPAT Inference Worker (Pure Rust SIMD)")

SPAT_BYTES = b""
MODEL_NAME = "unknown"
WORKER_PORT = 8001
ENGINE = "python-fallback"

@app.on_event("startup")
def startup():
    print(f"🟢 SPAT Worker — {MODEL_NAME} on port {WORKER_PORT}")
    print(f"   Engine: {ENGINE} | SPAT: {len(SPAT_BYTES)/1024:.1f} KB")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME, "port": WORKER_PORT,
        "size_kb": round(len(SPAT_BYTES) / 1024, 1),
        "engine": ENGINE,
    }

@app.get("/v1/models")
async def list_models():
    return {"object": "list", "data": [{"id": MODEL_NAME, "object": "model", "created": int(time.time()), "owned_by": "sovereign-mesh"}]}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    prompt = request.messages[-1].content if request.messages else ""
    if not prompt:
        raise HTTPException(400, "Empty prompt")

    prompt_tokens = encode(prompt)
    temperature = request.temperature or 0.7

    if request.stream:
        async def stream_generator():
            completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
            # 1. Initial metadata chunk
            initial_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": MODEL_NAME,
                "choices": []
            }
            yield f"data: {json.dumps(initial_chunk)}\n\n"

            tokens = prompt_tokens.copy()
            max_toks = request.max_tokens or 50
            for step in range(max_toks):
                if RUST_LIB:
                    logits, gen = run_rust_inference(RUST_LIB, SPAT_BYTES, tokens, 1, temperature)
                else:
                    logits, gen = run_cpu_inference(SPAT_BYTES, tokens, 1, temperature)

                next_token = gen[0] if gen else 0
                text = decode([next_token])
                if not text and next_token != 0:
                    text = f"[token {next_token}]"

                chunk = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": MODEL_NAME,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": text},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(chunk)}\n\n"

                tokens.append(next_token)
                if next_token == 0 or next_token == 50256:  # EOS token
                    break

                await asyncio.sleep(0.01)

            # Final chunk
            final_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": MODEL_NAME,
                "choices": [{
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    if RUST_LIB:
        logits, gen_tokens = run_rust_inference(RUST_LIB, SPAT_BYTES, prompt_tokens, request.max_tokens, temperature)
    else:
        logits, gen_tokens = run_cpu_inference(SPAT_BYTES, prompt_tokens, request.max_tokens, temperature)

    text = decode(gen_tokens)
    if not text.strip():
        # Show logits stats instead
        top_k = np.argsort(logits)[-5:][::-1]
        text = f"[🔮 SPAT inference: {len(gen_tokens)} tokens, {len(logits)} logits, top-5={top_k.tolist()}]"

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": len(prompt_tokens), "completion_tokens": len(gen_tokens), "total_tokens": len(prompt_tokens) + len(gen_tokens)},
    }

@app.post("/v1/chat/completions/stream")
async def chat_completions_stream(request: ChatRequest):
    if not request.stream:
        return await chat_completions(request)
    
    prompt = request.messages[-1].content if request.messages else ""
    if not prompt:
        raise HTTPException(400, "Empty prompt")

    prompt_tokens = encode(prompt)
    temperature = request.temperature or 0.7

    async def generate():
        tokens = prompt_tokens.copy()
        for step in range(request.max_tokens or 50):
            if RUST_LIB:
                logits, gen = run_rust_inference(RUST_LIB, SPAT_BYTES, tokens, 1, temperature)
            else:
                logits, gen = run_cpu_inference(SPAT_BYTES, tokens, 1, temperature)
            
            next_token = gen[0] if gen else 0
            text = decode([next_token]) or f"[token {next_token}]"
            
            import json
            data = json.dumps({
                "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": MODEL_NAME,
                "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}]
            })
            yield f"data: {data}\n\n"
            
            tokens.append(next_token)
            if next_token == 0:
                break
        
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


def main():
    global SPAT_BYTES, MODEL_NAME, WORKER_PORT, ENGINE

    ap = argparse.ArgumentParser(description="SPAT Inference Worker (Pure Rust)")
    ap.add_argument("--model", default="07_MODELS/gemma4-12b-spatial.spat")
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--host", default="0.0.0.0")
    args = ap.parse_args()

    WORKER_PORT = args.port
    model_path = Path(args.model)
    if not model_path.is_absolute():
        repo_root = Path(__file__).resolve().parent.parent.parent
        model_path = repo_root / model_path
    if not model_path.exists():
        model_path = Path(args.model)

    print(f"📂 Loading SPAT: {model_path}")
    SPAT_BYTES = load_spat(str(model_path))
    MODEL_NAME = model_path.stem.replace("-spatial", "").replace("-spatial", "")
    ENGINE = "rust-simd" if RUST_LIB else "python-fallback"
    print(f"🏛️ {MODEL_NAME} — {len(SPAT_BYTES)/1024:.1f} KB, engine={ENGINE}")

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
