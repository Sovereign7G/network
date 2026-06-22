#!/usr/bin/env python3
"""
ab_model_compare.py — P2: A/B model comparison for Odysseus chat sessions.

Runs the same prompt through primary (Bifrost gateway) and fallback
(Cookbook-recommended) models, diffs responses, tracks latency, and
generates a comparison summary. Results are stored in the session
via StickyDualSync for audit trail and regression tracking.
"""

import json
import time
import difflib
import urllib.request
import urllib.error
import sys
from typing import Dict, Any, Optional


class ABModelCompare:
    """Compares primary vs fallback model responses for the same prompt.

    Primary:   openai/lfm2.5-8b-a1b via Bifrost gateway (port 8080)
    Fallback:  meta-llama/Llama-3-8B-Instruct via Cookbook (port 8080)
    """

    def __init__(self, primary_endpoint: str = "http://localhost:8080/api/v1/chat",
                 fallback_endpoint: str = "http://localhost:8080/api/v1/chat"):
        self.primary = {
            "name": "openai/lfm2.5-8b-a1b",
            "endpoint": primary_endpoint,
        }
        self.fallback = {
            "name": "meta-llama/Llama-3-8B-Instruct",
            "endpoint": fallback_endpoint,
        }

    def compare(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run A/B comparison, returns structured result with diff and summary."""
        t0 = time.time()

        primary_resp, primary_err, primary_ms = self._query(self.primary, prompt, context)
        fallback_resp, fallback_err, fallback_ms = self._query(self.fallback, prompt, context)

        diff = self._diff_responses(primary_resp or "", fallback_resp or "")
        elapsed = time.time() - t0

        return {
            "prompt": prompt[:200],
            "timestamp": int(t0 * 1000),
            "elapsed_ms": round(elapsed * 1000),
            "primary": {
                "model": self.primary["name"],
                "response": primary_resp,
                "latency_ms": primary_ms,
                "error": primary_err,
            },
            "fallback": {
                "model": self.fallback["name"],
                "response": fallback_resp,
                "latency_ms": fallback_ms,
                "error": fallback_err,
            },
            "diff": diff,
            "summary": self._summarize(diff, primary_ms, fallback_ms, primary_err or fallback_err),
        }

    # ── Model query ─────────────────────────────────────────────

    def _query(self, model: Dict[str, str], prompt: str,
               context: Optional[Dict[str, Any]] = None) -> tuple:
        """Query a model endpoint. Returns (response, error, latency_ms)."""
        t0 = time.time()
        payload = json.dumps({
            "model": model["name"],
            "messages": [{"role": "user", "content": prompt}],
            **(context or {}),
        }).encode()

        try:
            req = urllib.request.Request(
                model["endpoint"], data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode()
                ms = round((time.time() - t0) * 1000)
                try:
                    data = json.loads(body)
                    return data.get("response") or data.get("content") or body[:500], None, ms
                except json.JSONDecodeError:
                    return body[:500], None, ms
        except urllib.error.HTTPError as e:
            ms = round((time.time() - t0) * 1000)
            return None, f"HTTP {e.code}", ms
        except Exception as e:
            ms = round((time.time() - t0) * 1000)
            return None, str(e)[:100], ms

    # ── Diff engine ─────────────────────────────────────────────

    def _diff_responses(self, a: str, b: str) -> Dict[str, Any]:
        """Token-level diff between two response strings."""
        matcher = difflib.SequenceMatcher(None, a.split(), b.split())
        added, removed = [], []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                added.extend(b.split()[j1:j2][:5])
            elif tag == "delete":
                removed.extend(a.split()[i1:i2][:5])
            elif tag == "replace":
                removed.extend(a.split()[i1:i2][:3])
                added.extend(b.split()[j1:j2][:3])

        return {
            "similarity": round(matcher.ratio(), 4),
            "common_tokens": matcher.quick_ratio(),
            "added_preview": added[:5],
            "removed_preview": removed[:5],
            "len_a": len(a),
            "len_b": len(b),
        }

    def _summarize(self, diff: Dict[str, Any], primary_ms: float,
                   fallback_ms: float, any_error: Optional[str]) -> str:
        """Generate one-line human summary."""
        if any_error:
            return f"Error: {any_error[:60]}"
        faster = "primary" if primary_ms < fallback_ms else "fallback"
        speed_gap = abs(primary_ms - fallback_ms)
        return (
            f"Sim={diff['similarity']:.1%}, "
            f"{faster} faster by {speed_gap:.0f}ms, "
            f"Δlen={diff['len_b'] - diff['len_a']}"
        )


# ── CLI demo ────────────────────────────────────────────────────

def main():
    import sys
    ab = ABModelCompare()

    action = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if action == "demo":
        prompt = "What is the current settlement rate on Base mainnet?"
        print(f"Prompt: {prompt}\n")
        result = ab.compare(prompt)

        print(f"Primary  ({result['primary']['model']}):")
        print(f"  latency={result['primary']['latency_ms']}ms  error={result['primary']['error']}")
        print(f"  response: {str(result['primary']['response'])[:80]}")
        print()
        print(f"Fallback ({result['fallback']['model']}):")
        print(f"  latency={result['fallback']['latency_ms']}ms  error={result['fallback']['error']}")
        print(f"  response: {str(result['fallback']['response'])[:80]}")
        print()
        print(f"Similarity: {result['diff']['similarity']:.1%}")
        print(f"Summary: {result['summary']}")
        print(f"Total: {result['elapsed_ms']}ms")

    elif action == "compare":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "hello"
        result = ab.compare(prompt)
        print(json.dumps(result, indent=2, default=str))

    else:
        print(f"Usage: {sys.argv[0]} [demo|compare <prompt>]")


if __name__ == "__main__":
    main()
