"""BillingEngine — USDC-to-credit conversion with bulk discount tiers.

Usage:
    from s7g_sdk.depin import DepinClient, BillingEngine
    engine = BillingEngine()
    engine.purchase("acme-corp", 100.0)
    engine.estimate(5000000)
"""
from typing import Optional, Any

CONVERSION_RATE = 1_000_000  # 1 USDC = 1M credits
DISCOUNT_TIERS = [
    (100_000_000, 0.25),
    (10_000_000, 0.10),
    (0, 0.0),
]


class BillingEngine:
    """Purchase, estimate, and manage credits with bulk discounts."""

    def __init__(self, client: Optional[Any] = None):
        from .client import DepinClient
        self.client = client or DepinClient()

    def convert(self, usdc: float) -> int:
        return int(usdc * CONVERSION_RATE)

    def discount(self, credits: int) -> float:
        for threshold, d in DISCOUNT_TIERS:
            if credits >= threshold:
                return d
        return 0.0

    def estimate(self, credits: int) -> dict:
        d = self.discount(credits)
        bonus = int(credits * d)
        total = credits + bonus
        return {
            "base_credits": credits, "discount": d,
            "bonus": bonus, "total_credits": total,
            "usdc_needed": round(total / CONVERSION_RATE, 2),
        }

    def purchase(self, tenant: str, usdc_amount: float) -> dict:
        credits = self.convert(usdc_amount)
        d = self.discount(credits)
        bonus = int(credits * d)
        total = credits + bonus
        result = self.client.get_tenant(tenant)
        return {
            "tenant": tenant, "usdc": usdc_amount,
            "base_credits": credits, "bonus": bonus,
            "total_credits": total, "discount": d,
            "tenant_exists": "error" not in str(result).lower(),
        }
