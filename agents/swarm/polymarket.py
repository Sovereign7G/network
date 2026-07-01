"""Polymarket arbitrage agent — scans prediction markets for mispriced opportunities."""
import json
import time
import urllib.request
from typing import Optional, Dict

from hl_feeds.polymarket_sdk import PolymarketClient

from .base import BaseAgent


class PolymarketArbitrageAgent(BaseAgent):
    """Scans Polymarket for mispriced binary prediction markets (price edge > 5%)."""
    def __init__(self, name="pm_arbitrage", interval=60):
        super().__init__(name, interval)
        self.pm = PolymarketClient()

    def execute(self) -> Optional[Dict]:
        try:
            mkts = self.pm.get_markets(limit=20)
            opps = []
            for m in mkts.get("data", mkts) if isinstance(mkts, dict) else mkts:
                name = m.get("question", "") or m.get("title", "") or m.get("id", "")
                price = m.get("price", 0.5)
                if isinstance(price, str):
                    price = float(price)
                spread = abs(price - 0.5)
                if spread > 0.05:
                    opps.append({"market": name[:40], "price": price, "edge": round(spread, 3)})
            return {"action": "scan_polymarket", "markets": len(opps), "ts": int(time.time())}
        except Exception as e:
            return {"action": "scan_polymarket", "error": str(e)[:80], "ts": int(time.time())}
