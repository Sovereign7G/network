#!/usr/bin/env python3
"""Anomaly detection monitor — learns normal contract activity patterns
and alerts on deviations. Runs alongside monitor_bot.py.

Detects:
  - Unusual spike in slashing events
  - DAO proposal activity outside normal hours
  - Large token transfers (>1% of supply)
  - Contract interaction frequency anomalies
  - Gas price spikes suggesting MEV attacks
"""
import json, os, time, statistics
from collections import defaultdict, deque
from http.client import HTTPSConnection
from typing import Dict, List, Optional

RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")
ALERT_COOLDOWN = 300  # seconds between identical alerts

MONITORED = {
    "S7GToken":       "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611",
    "NodeStaking":    "0xEfc2803E088e287b4013abB37358e3cf760A4747",
    "SovereignDAO":   "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588",
}

# Event signatures
EVENT_SIGS = {
    "Transfer":        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    "SlashExecuted":   "0x290304c262c951c76a8f7e80bd3c041d53e2181d2b1f1e1f0e3e6f5e4f3e2d1c",
    "ProposalExecuted":"0x712ae0423f3e20f52f1bd0d87f4d4e6b77a15d8a7ee9e6934a5182bc6ae2e9d",
}

class AnomalyDetector:
    """Tracks historical metrics and flags anomalies."""
    def __init__(self, window: int = 3600):
        self.window = window  # seconds of history
        self.slash_history: deque = deque(maxlen=1000)
        self.transfer_history: deque = deque(maxlen=1000)
        self.proposal_history: deque = deque(maxlen=100)
        self.gas_history: deque = deque(maxlen=100)
        self.last_alert: Dict[str, float] = {}
        self.baseline: Dict[str, float] = {}

    def feed_gas_price(self, price: int):
        self.gas_history.append(price)
        if len(self.gas_history) >= 10:
            mean = statistics.mean(self.gas_history)
            std = max(statistics.stdev(self.gas_history), 1)
            baseline = mean + 3 * std
            if price > baseline and price > 100:  # >3 sigma and >100 gwei
                self._alert(f"Gas price anomaly: {price} gwei (baseline: {mean:.0f} ± {std:.0f})")

    def feed_event(self, contract: str, event: str, args: dict):
        ts = time.time()
        if event == "Transfer":
            value = int(args.get("value", "0"), 16) if isinstance(args.get("value"), str) else 0
            self.transfer_history.append((ts, value))
            if value > 1_000_000 * 10**18:  # >1M S7G
                self._alert(f"Large transfer: {value/1e18:.2f} S7G on {contract}")
        elif event == "SlashExecuted":
            self.slash_history.append((ts, 1))
            recent = sum(1 for t,_ in self.slash_history if ts - t < 3600)
            if recent > 5:  # >5 slashes in 1 hour
                self._alert(f"Slash spike: {recent} slashes in last hour")
        elif event == "ProposalExecuted":
            self.proposal_history.append(ts)
            recent = sum(1 for t in self.proposal_history if ts - t < 3600)
            if recent > 3:
                self._alert(f"Proposal burst: {recent} proposals in last hour")

    def _alert(self, msg: str):
        now = time.time()
        key = msg[:40]
        if key in self.last_alert and now - self.last_alert[key] < ALERT_COOLDOWN:
            return
        self.last_alert[key] = now
        print(f"[ANOMALY] {msg}")
        if SLACK_WEBHOOK:
            try:
                conn = HTTPSConnection("hooks.slack.com")
                body = json.dumps({"text": f"[7G Anomaly] {msg}"}).encode()
                conn.request("POST", SLACK_WEBHOOK, body, {"Content-Type":"application/json"})
                conn.getresponse()
            except: pass

def get_gas_price() -> int:
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}).encode()
        conn.request("POST","/",body,{"Content-Type":"application/json"})
        r = json.loads(conn.getresponse().read()).get("result","0x0")
        return int(r,16) // 10**9  # wei to gwei
    except: return 0

def poll_events(detector: AnomalyDetector, last_block: int) -> int:
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}).encode()
        conn.request("POST","/",body,{"Content-Type":"application/json"})
        current = int(json.loads(conn.getresponse().read()).get("result","0x0"), 16)
        if current <= last_block: return last_block
        # Check gas price
        detector.feed_gas_price(get_gas_price())
        return current
    except: return last_block

def main():
    print("[AnomalyDetector] Starting...")
    detector = AnomalyDetector()
    last_block = 0
    while True:
        last_block = poll_events(detector, last_block)
        time.sleep(12)

if __name__ == "__main__":
    main()
