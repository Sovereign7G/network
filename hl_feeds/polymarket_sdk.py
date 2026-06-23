#!/usr/bin/env python3
"""Polymarket SDK — Prediction market client via CLOB API."""
import json, urllib.request, time
from typing import Optional

class PolymarketClient:
    BASE = "https://clob.polymarket.com"
    def get_markets(self, limit: int = 50, offset: int = 0) -> list:
        try:
            r = urllib.request.urlopen(f"{self.BASE}/markets?limit={limit}&offset={offset}", timeout=10)
            return json.loads(r.read()).get("data", [])
        except: return []
    def get_market(self, market_id: str) -> Optional[dict]:
        try:
            r = urllib.request.urlopen(f"{self.BASE}/markets/{market_id}", timeout=10)
            return json.loads(r.read())
        except: return None
    def get_price(self, market_id: str, outcome: str = "YES") -> Optional[float]:
        m = self.get_market(market_id)
        if m:
            for o in m.get("outcomes", []):
                if o.get("name","").upper() == outcome.upper():
                    return float(o.get("price", 0.5))
        return None
