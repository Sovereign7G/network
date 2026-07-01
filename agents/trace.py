"""Trace ID generation for swarm agents."""
import uuid
import time

def new_trace_id() -> str:
    """Generate a unique trace ID using timestamp prefix + UUID fragment."""
    ts_hex = format(int(time.time() * 1000), "x")[-8:]
    uid = str(uuid.uuid4())[:8]
    return f"trc-{ts_hex}-{uid}"
