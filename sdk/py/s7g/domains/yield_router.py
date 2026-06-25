"""YieldRouter & vault methods."""

from typing import Dict


def multi_yield_vault(self, action: str = "stats", asset: str = "USDC") -> Dict:
    """MultiYieldVault: deposit, withdraw, or check yields."""
    return self._request("POST", f"/api/stablecoin/vault/{action}", {"asset": asset})
