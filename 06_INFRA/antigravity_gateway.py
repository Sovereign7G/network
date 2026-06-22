#!/usr/bin/env python3
"""antigravity_gateway.py — Zero-trust gateway for Antigravity IDE.

Sanitizes all Antigravity requests/responses. Antigravity orchestrates
but never sees raw OKF data. All interactions logged for audit.
"""

import json, os, sys, re, hashlib
from pathlib import Path
from datetime import datetime

PATTERNS = {
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "okf_path": r'00_KNOWLEDGE/[a-zA-Z0-9_/.-]+',
    "api_key": r'(api[_-]?key|token|secret)[:=]\s*[a-zA-Z0-9]+',
    "contract": r'0x[a-fA-F0-9]{40}',
    "canister_id": r'oyipx-[\w-]+',
}

class Gateway:
    def __init__(self):
        self._log = []
        self.count = 0

    def sanitize_request(self, req):
        safe = dict(req)
        for k in ("prompt","context","query","input"):
            if k in safe and isinstance(safe[k], str):
                safe[k] = self._clean(safe[k])
        if "concept_path" in safe:
            safe["concept_path"] = self._safe_path(safe["concept_path"])
        self._log_it("request", safe)
        return safe

    def sanitize_response(self, resp):
        safe = dict(resp)
        for k in ("output","result","body"):
            if k in safe and isinstance(safe[k], str):
                safe[k] = self._clean(safe[k])
        if "okf_data" in safe and isinstance(safe["okf_data"], dict):
            safe["okf_data"] = self._summarize(safe["okf_data"])
        self._log_it("response", safe)
        return safe

    def _clean(self, text):
        for name, pat in PATTERNS.items():
            text = re.sub(pat, f"[REDACTED:{name}]", text)
        if len(text) > 5000:
            text = text[:5000] + "... [TRUNCATED]"
        return text

    def _safe_path(self, path):
        if not re.match(r'^[a-zA-Z0-9_/.-]+$', path):
            return "[REDACTED:invalid_path]"
        parts = path.strip("/").split("/")
        if len(parts) > 5:
            parts = parts[:5] + ["..."]
        return "/".join(parts)

    def _summarize(self, data):
        fm = data.get("frontmatter", {})
        body = data.get("body", "")
        return {
            "type": fm.get("type", "unknown"),
            "title": fm.get("title", "untitled"),
            "summary": (body[:300] + "...") if len(body) > 300 else body,
        }

    def _log_it(self, direction, data):
        self.count += 1
        entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "dir": direction,
            "hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16],
        }
        self._log.append(entry)
        if len(self._log) > 500:
            self._log = self._log[-500:]

    def status(self):
        return {"sanitized": self.count, "log_entries": len(self._log),
                "patterns": list(PATTERNS.keys())}

    def audit(self, limit=20):
        return self._log[-limit:]

if __name__ == "__main__":
    g = Gateway()
    a = sys.argv[1] if len(sys.argv) > 1 else "status"
    if a == "status":
        print(json.dumps(g.status(), indent=2))
    elif a == "sanitize":
        d = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {"prompt": "test@example.com"}
        print(json.dumps(g.sanitize_request(d), indent=2))
    elif a == "audit":
        print(json.dumps(g.audit(), indent=2))
