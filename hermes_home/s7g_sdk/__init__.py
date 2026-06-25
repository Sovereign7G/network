"""s7g_sdk — Python SDK for the S7G DePIN Operable System.

Provides programmatic access to all registry canister methods
via the DepinClient class, plus SLA-aware routing and billing.

Usage:
    from s7g_sdk import DepinClient
    client = DepinClient()
    client.tenant_count()  # 2
    client.get_reserve_state()  # {usdc_balance: 0, ...}

    from s7g_sdk import SLARouter
    router = SLARouter(client)
    router.route("acme-corp", "gpt-4o", "Hello", preference="cost")
"""
from .depin.client import DepinClient
from .depin.sla_router import SLARouter
from .depin.billing import BillingEngine
