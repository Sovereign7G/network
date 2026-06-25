#!/usr/bin/env python3
"""Kalshi Price Feed — Simulated perpetual futures prices."""
import json, os, time
from typing import Optional

class KalshiFeed:
    BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
    def __init__(self):
        self.cache = {}
    def get_perp_price(self, asset: str) -> Optional[float]:
        try:
            import requests
            r = requests.get(f"{self.BASE_URL}/market?ticker={asset}-PERP", timeout=5)
            if r.status_code == 200:
                return float(r.json().get("price", 0))
        except Exception as e:
            import sys; print(f"Kalshi feed error: {e}", file=sys.stderr)
        return None
    def get_funding_rate(self, asset: str) -> Optional[float]:
        return 0.0001
    def get_available_assets(self) -> list:
        return ["BTC", "ETH", "SOL"]
