#!/usr/bin/env python3
"""external_gateway.py — zero-trust external model gateway"""
import json
import os
import sys
import time
import re
import urllib.request
import hashlib
from pathlib import Path

# Paths
WORKSPACE_ROOT = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC")
ASSETS_DIR = WORKSPACE_ROOT / "08_ASSETS"
POLICY_FILE = ASSETS_DIR / "gateway_policy.json"
CACHE_FILE = ASSETS_DIR / "gateway_cache.json"
AUDIT_FILE = ASSETS_DIR / "gateway_audit.json"

CONFIG = {
    "deepseek": {
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "region": "china",
        "env_key": "DEEPSEEK_API_KEY"
    },
    "kimi": {
        "endpoint": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "region": "china",
        "env_key": "KIMI_API_KEY"
    },
    "textcortex": {
        "endpoint": "https://api.textcortex.com/v1/texts/completions",
        "model": "textcortex-v4-pro",
        "region": "eu",
        "env_key": "TEXTCORTEX_API_KEY"
    }
}

SENSITIVE_PATTERNS = [
    r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b',  # Email
    r'\b0x[a-fA-F0-9]{40}\b',          # Ethereum Address
    r'\b[a-fA-F0-9]{64}\b',            # 256-bit Hex Key (Private Key / Hashes)
    r'00_KNOWLEDGE/\S+',               # Filesystem path signatures
    r'\boyipx-[\w-]+\b',               # Principal IDs
    r'\b[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{5}-[a-z2-7]{3}\b' # NNS Principal format
]

STABLE_PREFIX = (
    "SYSTEM INSTRUCTIONS: You are Hermes Desktop, a secure agent running inside the Sovereign OS. "
    "You have access to the OKF (Open Knowledge Federation) memory bridge and local compute. "
    "Ensure all operations comply with absolute data sovereignty. Never disclose keys, addresses, or internal pathways. "
    "TOOL SCHEMAS:\n"
    "- serve_concept: Read concepts from OKF.\n"
    "- write_concept: Write/update concepts.\n"
    "- list_concepts: Search list paths.\n"
    "- external_infer: Route query to LLM.\n"
    "OKF SCHEMA RULES: Concepts must have YAML frontmatter with tags, title, type, and updated date.\n"
)

class Gateway:
    def __init__(self):
        self._load_policy()
        self._load_cache()

    def _load_policy(self):
        if POLICY_FILE.exists():
            try:
                self.policy = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
                # Ensure new keys are set
                updated = False
                if "stabilize_prompt_prefix" not in self.policy:
                    self.policy["stabilize_prompt_prefix"] = True
                    updated = True
                if updated:
                    self._save_policy()
            except Exception:
                self.policy = self._default_policy()
        else:
            self.policy = self._default_policy()
            self._save_policy()

    def _save_policy(self):
        try:
            POLICY_FILE.write_text(json.dumps(self.policy, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _default_policy(self):
        return {
            "routing_policy": "default",
            "region_restriction": "none",
            "budget_cap_usd": 50.0,
            "budget_spent_usd": 0.0,
            "pii_redaction": True,
            "mock_external_apis": True,
            "preferred_provider": "deepseek",
            "eu_data_residency": False,
            "stabilize_prompt_prefix": True
        }

    def _load_cache(self):
        if CACHE_FILE.exists():
            try:
                self.cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            except Exception:
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self):
        try:
            CACHE_FILE.write_text(json.dumps(self.cache, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _compute_embedding(self, text: str) -> list:
        dim = 384
        vec = [0.0] * dim
        text = re.sub(r'[^\w\s]', '', text.lower())
        for n in (2, 3):
            for i in range(len(text) - n + 1):
                gram = text[i:i + n]
                idx = int(hashlib.md5(gram.encode()).hexdigest()[:8], 16) % dim
                vec[idx] += 1.0
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def _cosine_similarity(self, a: list, b: list) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        if na * nb == 0:
            return 0.0
        return dot / (na * nb)

    def _find_cached_response(self, prompt):
        query_emb = self._compute_embedding(prompt)
        best_sim = 0.0
        best_response = None
        best_prompt_key = None
        
        for cached_prompt, entry in self.cache.items():
            if isinstance(entry, dict):
                stored_emb = entry.get("embedding")
                stored_resp = entry.get("response")
            else:
                stored_resp = entry
                stored_emb = self._compute_embedding(cached_prompt)
                # auto-upgrade format
                self.cache[cached_prompt] = {
                    "response": stored_resp,
                    "embedding": stored_emb
                }
                self._save_cache()
                
            if stored_emb:
                sim = self._cosine_similarity(query_emb, stored_emb)
                if sim > best_sim:
                    best_sim = sim
                    best_response = stored_resp
                    best_prompt_key = cached_prompt
                    
        # Cosine similarity threshold >= 0.92
        if best_sim >= 0.92:
            return best_response, best_sim
        return None, best_sim

    def _sanitize(self, txt):
        count = 0
        if not self.policy.get("pii_redaction", True):
            return txt, 0
        for pattern in SENSITIVE_PATTERNS:
            matches = re.findall(pattern, txt)
            if matches:
                count += len(matches)
                txt = re.sub(pattern, "[REDACTED]", txt)
        return txt, count

    def get_policy(self):
        self._load_policy()
        return self.policy

    def update_policy(self, new_policy):
        self._load_policy()
        self.policy.update(new_policy)
        self._save_policy()
        return self.policy

    def get_audit_logs(self, limit=20):
        if AUDIT_FILE.exists():
            try:
                logs = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
                return logs[-limit:]
            except Exception:
                return []
        return []

    def _log_audit(self, provider, prompt, response, latency_ms, redactions_count, cached, cost):
        logs = []
        if AUDIT_FILE.exists():
            try:
                logs = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
            except Exception:
                logs = []
        
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        response_hash = hashlib.sha256(response.encode()).hexdigest() if response else ""
        
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "provider": provider,
            "prompt_hash": prompt_hash,
            "response_hash": response_hash,
            "latency_ms": latency_ms,
            "redactions_count": redactions_count,
            "cached": cached,
            "cost_usd": cost
        }
        logs.append(entry)
        
        if len(logs) > 500:
            logs = logs[-500:]
            
        try:
            AUDIT_FILE.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception:
            pass

    def infer(self, provider, prompt, skill="", max_tokens=1024, bypass_cache=False):
        t0 = time.time()
        self._load_policy()

        # Check budget limits
        budget_cap = self.policy.get("budget_cap_usd", 50.0)
        budget_spent = self.policy.get("budget_spent_usd", 0.0)
        if budget_spent >= budget_cap:
            return {
                "result": "error",
                "error": f"Gateway budget cap exceeded. Limit: ${budget_cap:.2f}, Spent: ${budget_spent:.2f}"
            }

        if self.policy.get("eu_data_residency", False):
            provider = "textcortex"

        cfg = CONFIG.get(provider)
        if not cfg:
            return {"status": "error", "error": f"Unknown provider: {provider}"}

        # Check semantic cache first unless bypassed
        if not bypass_cache:
            cached_res, similarity = self._find_cached_response(prompt)
            if cached_res:
                lat = round((time.time() - t0) * 1000)
                self._log_audit(provider, prompt, cached_res, lat, 0, True, 0.0)
                return {
                    "result": f"Semantic cache hit (cosine: {similarity:.4f})",
                    "response": cached_res,
                    "cost": 0.0,
                    "latency_ms": lat
                }

        # Sanitize prompt
        safe_prompt, redact_count = self._sanitize(prompt)

        # Prepend stable prompt prefix
        if self.policy.get("stabilize_prompt_prefix", True):
            prompt_payload = f"{STABLE_PREFIX}\n--- VARIABLE CONTENT ---\n{safe_prompt}"
        else:
            prompt_payload = safe_prompt

        env_key_name = cfg["env_key"]
        api_key = os.environ.get(env_key_name, "")
        is_mock = self.policy.get("mock_external_apis", True) or not api_key

        cost = 0.002
        response_content = None
        status = "success"
        error_msg = None

        if is_mock:
            time.sleep(0.4)
            response_content = (
                f"[Zero-Trust Route: {provider}] Processed instruction securely. "
                f"Prompt hash verified. Prefix cache hits enabled. "
                f"Response simulated using {cfg['model']} proxy backend."
            )
        else:
            try:
                payload = json.dumps({
                    "model": cfg["model"],
                    "messages": [{"role": "user", "content": prompt_payload}],
                    "max_tokens": max_tokens
                }).encode("utf-8")
                req = urllib.request.Request(
                    cfg["endpoint"],
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as r:
                    resp = json.loads(r.read().decode("utf-8"))
                    response_content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
            except Exception as e:
                status = "error"
                error_msg = str(e)

        # Apply response filter
        if response_content:
            response_content, resp_redacts = self._sanitize(response_content)
            redact_count += resp_redacts
            
            # Save to semantic cache if successful
            if status == "success":
                self.cache[prompt] = {
                    "response": response_content,
                    "embedding": self._compute_embedding(prompt)
                }
                self._save_cache()

        lat = round((time.time() - t0) * 1000)

        if status == "success":
            self.policy["budget_spent_usd"] = round(budget_spent + cost, 4)
            self._save_policy()

        self._log_audit(provider, prompt, response_content or "", lat, redact_count, False, cost if status == "success" else 0.0)

        if status == "error":
            return {"result": "error", "error": error_msg, "latency_ms": lat}

        return {
            "result": "success",
            "provider": provider,
            "model": cfg["model"],
            "response": response_content,
            "latency_ms": lat,
            "cached": False,
            "redactions": redact_count,
            "cost": cost
        }

    def health(self):
        self._load_policy()
        status_map = {}
        for n, c in CONFIG.items():
            key_present = bool(os.environ.get(c["env_key"], ""))
            status_map[n] = {
                "configured": True,
                "region": c["region"],
                "model": c["model"],
                "api_key_set": key_present,
                "mock_active": self.policy.get("mock_external_apis", True) or not key_present
            }
        
        return {
            "status": "HEALTHY",
            "policy": self.policy,
            "providers": status_map,
            "cache_size": len(self.cache)
        }

if __name__ == "__main__":
    g = Gateway()
    action = sys.argv[1] if len(sys.argv) > 1 else "health"
    if action == "health":
        print(json.dumps(g.health(), indent=2))
    elif action == "infer" and len(sys.argv) > 3:
        prov = sys.argv[2]
        prompt = sys.argv[3]
        print(json.dumps(g.infer(prov, prompt), indent=2))
