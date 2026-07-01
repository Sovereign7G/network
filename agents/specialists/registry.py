"""
Specialist agent registry — maps agents to domains for coordinator delegation.

Domains: security, dev, content, ops, strategy (from telegram_bot.py AGENT_TOPIC_MAP)
Categories: security, infrastructure, ecosystem, core (from swarm_orchestrator.py AGENT_CATEGORIES)
"""
from typing import Dict, List

# Agent name -> domain mapping (mirrors AGENT_TOPIC_MAP in telegram_bot.py)
AGENT_DOMAIN_MAP: Dict[str, str] = {
    # Security
    "guardrail_monitor":      "security",
    "threat_intel":           "security",
    "bridge_security":        "security",
    "cross_chain_security":   "security",
    "ai_attack_detector":     "security",
    "cybersentinel":          "security",
    "siem_integration":       "security",
    # Dev / Infrastructure
    "solana_validator":       "dev",
    "solana_depin":           "dev",
    "settlement":             "dev",
    "mcp_payment_router":     "dev",
    "blockrun_integration":   "dev",
    "powershell_monitor":     "dev",
    "aetherdb":               "dev",
    "icp":                    "dev",
    # Content
    "chatr_agent":            "content",
    "content_generator":      "content",
    "chatwoot_support":       "content",
    # Yield / Ops
    "yield_optimizer":        "ops",
    "yield_harvester":        "ops",
    "arbitrage":              "ops",
    "liquidity":              "ops",
    "liquidity_rebalancer":   "ops",
    "fee_collector":          "ops",
    "stablecoin_router":      "ops",
    "fx_hedge":               "ops",
    "risk_assessor":          "ops",
    # Strategy
    "competitive_intel":      "strategy",
    "revenue_optimization":   "strategy",
    "adoption_funnel":        "strategy",
    "reporting":              "strategy",
    "synthesis":              "strategy",
    "action_planner":         "strategy",
}

# Domain categories (maps domain -> list of agent names)
def get_agents_by_domain() -> Dict[str, List[str]]:
    """Return grouped agent names by domain."""
    domains: Dict[str, List[str]] = {}
    for agent, domain in AGENT_DOMAIN_MAP.items():
        domains.setdefault(domain, []).append(agent)
    return domains

# Orchestrator categories (from swarm_orchestrator.py)
ORCHESTRATOR_CATEGORIES = {
    "security": {"ids": [42, 43, 50, 51, 52, 56, 57, 68, 69], "min": 5},
    "infrastructure": {"ids": [36, 37, 38, 59, 62, 64, 70, 71], "min": 4},
    "ecosystem": {"ids": [44, 46, 47, 48, 49, 72, 73, 74, 75, 76, 77, 78, 79, 80, 83], "min": 5},
    "core": {"ids": list(range(1, 36)), "min": 10},
}


def get_domain_for_agent(agent_name: str) -> str:
    """Return the domain for a given agent name."""
    return AGENT_DOMAIN_MAP.get(agent_name, "general")


def get_agents_in_domain(domain: str) -> List[str]:
    """Return all agent names in a domain."""
    return [a for a, d in AGENT_DOMAIN_MAP.items() if d == domain]
