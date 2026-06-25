"""Billing engine — USDC to credits conversion, tiered pricing, bulk discounts.

Usage:
    export STRIPE_KEY="sk_..."
    python3 billing.py --purchase acme-corp --usdc 100
    python3 billing.py --estimate 1000000
"""
import json
import os
import subprocess
import sys
from typing import Optional

CREDITS_CANISTER = "nram6-7qaaa-aaaas-qgv2a-cai"
REGISTRY_CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"
RATE = 1_000_000  # 1 USDC = 1,000,000 credits

def convert(usdc: float) -> int:
    return int(usdc * RATE)

def discount(credits: int) -> float:
    if credits >= 100_000_000:
        return 0.25
    elif credits >= 10_000_000:
        return 0.10
    return 0.0

def credit_membership(credits: int) -> int:
    return credits + int(credits * discount(credits) / (1 - discount(credits)))

def estimate(credits: int) -> dict:
    d = discount(credits)
    total = credit_membership(credits)
    return {
        "base_credits": credits, "discount": d,
        "total_credits": total,
        "usdc_needed": round(total / RATE, 2),
    }

def purchase(tenant: str, usdc_amount: float) -> dict:
    credits = convert(usdc_amount)
    d = discount(credits)
    total = credit_membership(credits)
    try:
        out = subprocess.check_output(
            ["dfx", "canister", "call", REGISTRY_CANISTER,
             "get_tenant", f'("{tenant}")', "--network", "ic"],
            stderr=subprocess.STDOUT, timeout=15, text=True,
        )
    except subprocess.CalledProcessError:
        return {"error": f"Tenant '{tenant}' not found"}
    return {
        "tenant": tenant, "usdc": usdc_amount,
        "base_credits": credits, "bonus_credits": total - credits,
        "total_credits": total, "discount": d,
    }

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--purchase", help="Tenant name to purchase credits for")
    p.add_argument("--usdc", type=float, help="USDC amount")
    p.add_argument("--estimate", type=int, help="Estimate credits needed")
    args = p.parse_args()
    if args.purchase and args.usdc:
        result = purchase(args.purchase, args.usdc)
    elif args.estimate:
        result = estimate(args.estimate)
    else:
        p.print_help(); sys.exit(1)
    print(json.dumps(result, indent=2))
