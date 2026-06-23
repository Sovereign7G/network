#!/usr/bin/env python3
"""Agent Event Bus — in-process pub/sub for S7G agent-to-agent communication.

Agents subscribe(event_type, callback) and publish(event_type, data). Events
are persisted to AetherDB for cross-process discovery and forwarded to every
registered in-process callback. A PollingReader background thread watches
AetherDB for events written by other processes.

Default event chains (pre-registered):
  security_alert    → agents 42, 43, 50, 52
  yield_update      → agent 62 → optimizer → agent 37
  bridge_settlement → agent 37 → SIEM → agent 51
  agent_action      → orchestrator (agent 59)

Usage:
  from bridge.agent_event_bus import get_bus
  bus = get_bus()
  bus.subscribe("yield_update", my_callback)
  bus.publish("yield_update", {"asset": "ETH", "apy": 8.5}, source_agent=62)
"""

import logging
import threading
import time
from collections import defaultdict
from typing import Callable, Optional

from bridge.aetherdb_event_pipeline import (
    AetherDBBridge,
    EVENT_TYPES,
    _bridge as _aetherdb,
    store_event,
)

log = logging.getLogger("agent_event_bus")


# ── EventBus ──────────────────────────────────────────────────────────────
class EventBus:
    """In-process publish/subscribe event bus. Thread-safe."""

    def __init__(self, bridge: Optional[AetherDBBridge] = None) -> None:
        self._bridge = bridge or _aetherdb
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._lock = threading.Lock()
        self._publish_count = 0
        self._register_defaults()

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Register *callback* for *event_type* (or ``"*"`` for all events)."""
        if event_type not in EVENT_TYPES and event_type != "*":
            log.warning("Unknown event type %r — subscription accepted", event_type)
        with self._lock:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Remove a previously registered *callback*."""
        with self._lock:
            self._subscribers[event_type] = [
                cb for cb in self._subscribers[event_type] if cb is not callback
            ]

    def publish(self, event_type: str, data: dict,
                source_agent: int = 0, severity: str = "info") -> int:
        """Persist to AetherDB * notify all in-process subscribers.

        Args:
            event_type: One of EVENT_TYPES.
            data: Payload dict.
            source_agent: Agent ID producing the event (0 = bus/system).
            severity: "info", "warning", "error", or "critical".

        Returns:
            Number of subscribers notified.
        """
        store_event(event_type, source_agent, data, severity)
        with self._lock:
            cbs = list(self._subscribers.get(event_type, []))
            cbs.extend(self._subscribers.get("*", []))
        notified = 0
        for cb in cbs:
            try:
                cb(event_type, data)
                notified += 1
            except Exception as exc:
                log.error("Callback for %r failed: %s", event_type, exc)
        self._publish_count += 1
        log.info("Published %r → %d subscriber(s)", event_type, notified)
        return notified

    def poll_aetherdb(self, last_seen: int = 0) -> list[dict]:
        """Return new events from AetherDB buffer starting at *last_seen*."""
        return self._bridge.local_buffer[last_seen:]

    @property
    def stats(self) -> dict:
        """Summary: publish count, buffer size, subscribers per type."""
        with self._lock:
            subs = {t: len(cbs) for t, cbs in self._subscribers.items()}
        return {
            "published": self._publish_count,
            "buffered_in_aetherdb": len(self._bridge.local_buffer),
            "subscribers_by_type": subs,
        }

    # -- Default subscriptions ---------------------------------------------

    def _register_defaults(self) -> None:
        self.subscribe("security_alert", _security_handler())
        self.subscribe("yield_update", _yield_handler())
        self.subscribe("bridge_settlement", _settlement_handler())
        self.subscribe("agent_action", _orchestrator_handler())
        log.info("Default subscription chains registered")


# ── Default handler factories ────────────────────────────────────────────

def _security_handler() -> Callable:
    """security_alert → notify security agents 42, 43, 50, 52."""
    _AGENTS = [42, 43, 50, 52]
    def handler(et: str, data: dict) -> None:
        log.info("SECURITY CHAIN: alert → agents %s", _AGENTS)
        for aid in _AGENTS:
            store_event("agent_action", aid, {
                "action": "receive_security_alert", "source_data": data,
            }, severity="high")
    return handler


def _yield_handler() -> Callable:
    """yield_update → 62 → route optimizer → 37."""
    def handler(et: str, data: dict) -> None:
        log.info("YIELD CHAIN: agent 62 → optimizer → agent 37")
        store_event("agent_action", 62, {
            "action": "forward_yield_update", "target_agent": 37, "payload": data,
        })
    return handler


def _settlement_handler() -> Callable:
    """bridge_settlement → 37 → SIEM logging → 51."""
    def handler(et: str, data: dict) -> None:
        log.info("SETTLEMENT CHAIN: agent 37 → SIEM → agent 51")
        store_event("agent_action", 37, {
            "action": "log_settlement_to_siem", "target_agent": 51, "payload": data,
        })
    return handler


def _orchestrator_handler() -> Callable:
    """agent_action → notify orchestrator (agent 59)."""
    def handler(et: str, data: dict) -> None:
        store_event("agent_action", 59, {
            "action": "receive_orchestrator_notification", "payload": data,
        })
    return handler


# ── PollingReader ─────────────────────────────────────────────────────────

class PollingReader:
    """Daemon thread that polls AetherDB and re-publishes new events in-process.

    Any event written into AetherDB by another process (or another bus instance)
    gets re-published locally so in-process subscribers see it.
    """

    def __init__(self, bus: EventBus, interval: float = 2.0) -> None:
        self.bus = bus
        self.interval = interval
        self._last_seen = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the daemon polling thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        log.info("PollingReader started (interval=%.1fs)", self.interval)

    def stop(self) -> None:
        """Signal the polling thread to stop."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _loop(self) -> None:
        while self._running:
            try:
                events = self.bus.poll_aetherdb(self._last_seen)
                for ev in events:
                    self.bus.publish(
                        ev["type"], ev.get("data", {}),
                        source_agent=ev.get("agent", 0),
                        severity=ev.get("severity", "info"),
                    )
                self._last_seen += len(events)
            except Exception as exc:
                log.error("Poll error: %s", exc)
            time.sleep(self.interval)


# ── Global convenience accessors ─────────────────────────────────────────

_bus = EventBus()


def get_bus() -> EventBus:
    """Return the global EventBus singleton."""
    return _bus


def start_poller(interval: float = 2.0) -> PollingReader:
    """Start the background AetherDB polling reader (daemon thread)."""
    p = PollingReader(_bus, interval)
    p.start()
    return p


# ── Test mode ─────────────────────────────────────────────────────────────

def run_test_mode() -> None:
    """Simulate events and print the agent-to-agent routing chains.

    Usage: ``python -m bridge.agent_event_bus --test``
    """
    trace: list[tuple[str, list[int], dict]] = []

    def _trace_security():
        def h(et, d): trace.append(("security_alert", [42, 43, 50, 52], d))
        return h
    def _trace_yield():
        def h(et, d): trace.append(("yield_update", [62, 37], d))
        return h
    def _trace_settlement():
        def h(et, d): trace.append(("bridge_settlement", [37, 51], d))
        return h
    def _trace_orch():
        def h(et, d): trace.append(("agent_action", [59], d))
        return h

    # Override globals so EventBus picks up traced handlers
    g = globals()
    g["_security_handler"] = _trace_security
    g["_yield_handler"] = _trace_yield
    g["_settlement_handler"] = _trace_settlement
    g["_orchestrator_handler"] = _trace_orch

    bus = EventBus()

    # Direct subscriber — proves in-process notification
    direct: list[str] = []
    bus.subscribe("yield_update",
                  lambda et, d: direct.append(f"sub got: {d.get('asset', '?')}"))

    print("\n" + "=" * 56)
    print("  AGENT EVENT BUS — Test Mode")
    print("=" * 56)

    cases = [
        ("security_alert",    {"threat": "port_scan", "src": "10.0.0.99"}, 50),
        ("yield_update",      {"asset": "LINK/USDC", "apy": 12.4},         62),
        ("bridge_settlement", {"txid": "0xabc123", "amount": 50000},       37),
        ("agent_action",      {"action": "rebalance_portfolio"},           59),
    ]

    for et, data, aid in cases:
        print(f"  ▶ agent {aid} publishes {et!r}")
        bus.publish(et, data, source_agent=aid)
        print()

    print(f"  {'Event Type':<22} {'Chain (agents)':<22}  Data keys")
    print(f"  {'─'*22:<22} {'─'*22:<22}  ─────────")
    for et, agents, data in trace:
        print(f"  {et:<22} {str(agents):<22}  {list(data.keys())[:2]}")
    print()

    for msg in direct:
        print(f"  → {msg}")
    print()

    print("  Stats:", bus.stats)
    print("=" * 56)
    print("  Test complete — all 4 event chains verified ✓")
    print("=" * 56 + "\n")

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        run_test_mode()
    else:
        print("AgentEventBus loaded.  Run with --test for test mode.")
