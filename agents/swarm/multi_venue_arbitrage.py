"""Multi-venue arbitrage agent — scans Kalshi, Deribit, and Hyperliquid for cross-venue spreads."""
import json
import time
import urllib.request
from typing import Optional, Dict

from hl_feeds.kalshi_feed import KalshiFeed
from hl_feeds.deribit_feed import DeribitFeed

from .base import BaseAgent


class MultiVenueArbitrageAgent(BaseAgent):
    """Scans Kalshi, Deribit, and Hyperliquid for triangular arbitrage opportunities."""
    def __init__(self, name="multi_venue_arbitrage", interval=30):
        super().__init__(name, interval)
        self.kalshi = KalshiFeed()
        self.deribit = DeribitFeed()

    def execute(self) -> Optional[Dict]:
        try:
            req = urllib.request.Request(
                "https://api.hyperliquid.xyz/info",
                data=json.dumps({"type": "allMids"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
            assets = [a for a in ["BTC", "ETH", "SOL"] if a in resp]
            opportunities = []
            for a in assets:
                hl_p = float(resp.get(a, 0) or 0)
                k_p = self.kalshi.get_perp_price(a) or 0
                d_p = self.deribit.get_perp_price(a) or 0
                prices = {k: v for k, v in [("hl", hl_p), ("kalshi", k_p), ("deribit", d_p)] if v > 0}
                if len(prices) >= 2:
                    best = max(prices, key=prices.get)
                    worst = min(prices, key=prices.get)
                    spread = (prices[best] - prices[worst]) / prices[worst]
                    if spread > 0.001:
                        opportunities.append({
                            "asset": a, "spread": round(spread, 4),
                            "buy": worst, "sell": best,
                        })
            return {
                "action": "scan_3_venues",
                "pairs": len(assets),
                "opportunities": len(opportunities),
                "ts": int(time.time()),
            }
        except Exception as e:
            return {"action": "scan_3_venues", "error": str(e)[:100], "ts": int(time.time())}
