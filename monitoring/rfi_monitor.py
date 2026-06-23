#!/usr/bin/env python3
"""RFI (Radio Frequency Interference) monitor for DSA deployment.
Monitors spectrum usage across 7G mesh nodes to ensure zero-RF compliance.
Alerts when spectral pollution is detected near DSA dishes.
"""
import json, os, time, socket, threading
from http.client import HTTPSConnection
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque

DSA_FREQ_BANDS = {
    "l_band":  (1.2e9,  1.7e9),   # 1.2-1.7 GHz — HI line, pulsars
    "s_band":  (2.3e9,  3.0e9),   # 2.3-3.0 GHz — continuum
    "c_band":  (4.8e9,  5.5e9),   # 4.8-5.5 GHz — OH masers
    "x_band":  (8.0e9,  8.8e9),   # 8.0-8.8 GHz — VLBI
    "ku_band": (12.0e9, 12.75e9), # 12-12.75 GHz — molecular lines
}

RFI_THRESHOLDS = {
    "max_power_dbm":    -80,   # -80 dBm max allowed
    "max_spikes_per_s": 10,    # 10 spikes/sec max
    "max_duration_s":   0.1,   # 100ms max interference event
    "alert_cooldown_s": 300,   # 5 min between alerts
}

@dataclass
class RFIEvent:
    frequency: float; power_dbm: float; duration_s: float
    timestamp: float; node_id: str; band: str; severity: str

class RFIMonitor:
    """Real-time RFI monitoring for DSA radio-quiet zones."""
    def __init__(self, node_id: str, aetherdb_id: str = "h54dw-qyaaa-aaaaa-qhjtq-cai"):
        self.node_id = node_id
        self.aetherdb_id = aetherdb_id
        self.events: deque[RFIEvent] = deque(maxlen=10000)
        self.alerts: List[RFIEvent] = []
        self.spike_count: Dict[str, int] = {}
        self._running = True

    def scan_band(self, band_name: str, low_hz: float, high_hz: float) -> List[float]:
        """Simulate spectrum scan across a frequency band.
        In production: reads from SDR ADC samples via Mojo FFI.
        """
        import random
        n = 100  # 100 frequency points
        powers = []
        for i in range(n):
            f = low_hz + (high_hz - low_hz) * i / n
            base = -95  # desert noise floor
            rfi = random.gauss(0, 5)  # random interference
            p = base + rfi
            powers.append(p)
        return powers

    def detect_rfi(self, powers: List[float], band: str) -> Optional[RFIEvent]:
        """Detect RFI events from spectrum scan data."""
        now = time.time()
        violations = [p for p in powers if p > RFI_THRESHOLDS["max_power_dbm"]]
        if violations:
            max_power = max(violations)
            self.spike_count[band] = self.spike_count.get(band, 0) + len(violations)
            if self.spike_count[band] > RFI_THRESHOLDS["max_spikes_per_s"]:
                if now - self.last_alert(band) > RFI_THRESHOLDS["alert_cooldown_s"]:
                    sev = "CRITICAL" if max_power > -60 else "WARNING"
                    return RFIEvent(frequency=0, power_dbm=max_power,
                                    duration_s=0.05, timestamp=now,
                                    node_id=self.node_id, band=band, severity=sev)
        return None

    def last_alert(self, band: str) -> float:
        for e in reversed(self.events):
            if e.band == band: return e.timestamp
        return 0

    def log_event(self, event: RFIEvent):
        self.events.append(event)
        if event.severity in ("CRITICAL", "WARNING"):
            self.alerts.append(event)
        # Store to aetherdb_bridge
        try:
            key = f"rfi:{event.node_id}:{event.band}:{int(event.timestamp)}"
            val = json.dumps({"freq":event.frequency,"power":event.power_dbm,
                              "dur":event.duration_s,"sev":event.severity})
            c = HTTPSConnection("ic0.app")
            body = json.dumps({"jsonrpc":"2.0","method":"canister_call",
                "params":[self.aetherdb_id,"aetherdb_put",
                         [key, list(val.encode("utf-8"))]],"id":1}).encode()
            c.request("POST",f"/api/v2/canister/{self.aetherdb_id}/call",body,
                      {"Content-Type":"application/json"})
        except: pass

    def scan_cycle(self):
        """Run one full spectrum scan across all DSA bands."""
        for band, (low, high) in DSA_FREQ_BANDS.items():
            powers = self.scan_band(band, low, high)
            event = self.detect_rfi(powers, band)
            if event:
                self.log_event(event)
                print(f"[RFI] {event.severity} in {band}: {event.power_dbm:.1f} dBm at node {event.node_id}")

    def run_continuous(self, interval_s: float = 1.0):
        """Continuous RFI monitoring loop."""
        while self._running:
            self.scan_cycle()
            time.sleep(interval_s)

    def report(self) -> Dict:
        return {"total_events": len(self.events), "alerts": len(self.alerts),
                "active_alerts": len([a for a in self.alerts if time.time() - a.timestamp < 3600])}

if __name__ == "__main__":
    import random
    mon = RFIMonitor(node_id="dsa-node-001")
    print("=== DSA RFI Monitor ===")
    print(f"Bands monitored: {list(DSA_FREQ_BANDS.keys())}")
    print(f"Threshold: {RFI_THRESHOLDS['max_power_dbm']} dBm")
    for _ in range(5):
        mon.scan_cycle()
        time.sleep(0.1)
    print(f"\nReport: {json.dumps(mon.report(), indent=2)}")
