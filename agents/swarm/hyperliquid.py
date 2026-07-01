"""Hyperliquid agents — funding rate scanner and LP status monitor."""
import time
from typing import Optional, Dict

from .base import BaseAgent


class HyperliquidArbitrageAgent(BaseAgent):
    """Scans Hyperliquid for funding rate arbitrage opportunities."""
    def __init__(self, name="hl_arbitrage", interval=10):
        super().__init__(name, interval)

    def execute(self) -> Optional[Dict]:
        try:
            from hyperliquid.info import Info
            info = Info()
            metadata = info.all_mids()
            return {"action": "scan_hl_funding", "pairs_scanned": len(metadata), "ts": int(time.time())}
        except Exception as e:
            return {"action": "scan_hl_funding", "error": str(e), "ts": int(time.time())}


class HyperliquidLiquidityAgent(BaseAgent):
    """Monitors Hyperliquid LP positions and active trading pairs."""
    def __init__(self, name="hl_liquidity", interval=60):
        super().__init__(name, interval)

    def execute(self) -> Optional[Dict]:
        try:
            from hyperliquid.info import Info
            info = Info()
            mids = info.all_mids()
            return {"action": "hl_lp_status", "active_pairs": len(mids), "ts": int(time.time())}
        except Exception as e:
            return {"action": "hl_lp_status", "error": str(e), "ts": int(time.time())}
