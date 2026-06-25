#!/usr/bin/env python3
"""S7G Distributed Tracing — spans, traces, and exporters across all services.
Each service emits spans with trace_id + parent_span_id for distributed correlation.
Supports: console, JSON, and OTLP exporters.
"""
import json, os, time, uuid, threading
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from http.client import HTTPSConnection
from collections import defaultdict

EXPORTER = os.getenv("TRACE_EXPORTER", "console")  # console, json, otlp

class Span:
    def __init__(self, trace_id: str = "", span_id: str = "",
                 parent_id: Optional[str] = None, name: str = "",
                 service: str = "s7g", start_ns: int = 0, end_ns: int = 0,
                 status: str = "ok", error: Optional[str] = None,
                 tags: Optional[Dict] = None):
        self.trace_id = trace_id; self.span_id = span_id
        self.parent_id = parent_id; self.name = name; self.service = service
        self.start_ns = start_ns; self.end_ns = end_ns
        self.status = status; self.error = error
        self.tags = tags or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_ns = time.time_ns()
        self.status = "error" if exc_type else self.status
        self.error = str(exc_val) if exc_val else self.error
        self._export()

    def _export(self):
        duration_ms = (self.end_ns - self.start_ns) / 1_000_000
        if EXPORTER == "console":
            print(f"[Trace {self.trace_id[:8]}] {self.service}.{self.name} "
                  f"{duration_ms:.1f}ms [{self.status}]")

class Tracer:
    """Lightweight distributed tracer with span correlation."""
    def __init__(self, service: str = "s7g"):
        self.service = service
        self.spans: List[Span] = []
        self._local = threading.local()

    def start_span(self, name: str, trace_id: Optional[str] = None,
                   parent_id: Optional[str] = None, tags: Optional[Dict] = None) -> Span:
        trace_id = trace_id or uuid.uuid4().hex[:16]
        span_id = uuid.uuid4().hex[:16]
        span = Span(trace_id=trace_id, span_id=span_id, parent_id=parent_id,
                    name=name, service=self.service, start_ns=time.time_ns(),
                    tags=tags or {})
        self.spans.append(span)
        self._local.current = span
        return span

    def end_span(self, span: Optional[Span] = None, status: str = "ok",
                 error: Optional[str] = None):
        span = span or getattr(self._local, "current", None)
        if not span: return
        span.end_ns = time.time_ns()
        span.status = status
        span.error = error
        self._export(span)

    def _export(self, span: Span):
        duration_ms = (span.end_ns - span.start_ns) / 1_000_000
        if EXPORTER == "console":
            print(f"[Trace {span.trace_id[:8]}] {span.service}.{span.name} "
                  f"{duration_ms:.1f}ms [{span.status}]")
        elif EXPORTER == "json":
            print(json.dumps({
                "trace_id": span.trace_id, "span_id": span.span_id,
                "parent_id": span.parent_id, "name": span.name,
                "service": span.service, "duration_ms": round(duration_ms, 1),
                "status": span.status, "error": span.error, "tags": span.tags,
            }))

    def trace(self, name: str, tags: Optional[Dict] = None):
        """Decorator for automatic tracing."""
        def decorator(f):
            def wrapper(*args, **kwargs):
                span = self.start_span(name, tags=tags)
                try:
                    result = f(*args, **kwargs)
                    self.end_span(span)
                    return result
                except Exception as e:
                    self.end_span(span, status="error", error=str(e))
                    raise
            return wrapper
        return decorator


# Global tracer instance
tracer = Tracer(service="s7g-test")

@tracer.trace("check_contract")
def check_contract(addr: str) -> bool:
    with tracer.start_span("eth_getCode", tags={"contract": addr[:12]}):
        try:
            c = HTTPSConnection("mainnet.base.org")
            body = json.dumps({"jsonrpc":"2.0","method":"eth_getCode",
                "params":[addr,"latest"],"id":1}).encode()
            c.request("POST","/",body,{"Content-Type":"application/json"})
            r = json.loads(c.getresponse().read()).get("result","0x")
            return r != "0x"
        except Exception as e:
            tracer.end_span(status="error", error=str(e))
            return False

@tracer.trace("query_health")
def query_health():
    contracts = ["0x54951D5021a2774567412fB8DB6FDF4A1EaE2611",
                 "0x45bD704f371bc593f38Bd76D43D356A14Febe477",
                 "0xEfc2803E088e287b4013abB37358e3cf760A4747",
                 "0x6afd8D26dF226980a932439948DEefBd33301bf6",
                 "0x2606fEbB30deE751DfFbCa538df20Eed5E379410",
                 "0x367d9481CfF6e7E18fAE5b11aA524dbbE139f443",
                 "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588"]
    results = {}
    for addr in contracts:
        t0 = time.time()
        ok = check_contract(addr)
        results[addr[:12]] = ok
    return results

if __name__ == "__main__":
    print("=== S7G Tracing Demo ===")
    print(f"Exporter: {EXPORTER}")
    health = query_health()
    ok = sum(1 for v in health.values() if v)
    print(f"\nHealth: {ok}/7 contracts OK")
    print(f"Spans: {len(tracer.spans)} emitted")
