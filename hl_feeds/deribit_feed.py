#!/usr/bin/env python3
"""Deribit Price Feed — Simulated perpetual futures prices."""
import json, os, time
from typing import Optional

class DeribitFeed:
    BASE_URL = "https://www.deribit.com/api/v2"
    def __init__(self):
        self.cache = {}
    def get_perp_price(self, asset: str) -> Optional[float]:
        try:
            import requests
            r = requests.get(f"{self.BASE_URL}/public/ticker?instrument_name={asset}-PERPETUAL", timeout=5)
            if r.status_code == 200:
                return float(r.json().get("result",{}).get("last_price", 0))
        except Exception as e:
            import sys; print(f"Deribit feed error: {e}", file=sys.stderr)
        return None
    def get_funding_rate(self, asset: str) -> Optional[float]:
        return 0.0001
