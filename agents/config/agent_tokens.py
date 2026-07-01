"""
Sovereign 7G Agent System — Config Layer

Agent tokens: versioned prompts, domain instructions, default parameters.
These are the "design tokens" of the agent system — defined once, consumed
everywhere. Changes here cascade to all 54 agents.

Analogous to: colors, spacing, typography in a design system monorepo.
"""
AGENT_VERSION = "2.0.0"
AGENT_COUNT = 54
DOMAINS = ["security", "dev", "content", "ops", "strategy"]

# Core system prompt fragments — "design tokens" for agents
PROMPTS = {
    "base": "You are a specialist agent in the Sovereign 7G Network.",
    "coordinator": "Orchestrate specialists, synthesize results, delegate tasks.",
    "security": "Monitor threats, audit access, alert on anomalies.",
    "dev": "Track GitHub PRs, monitor systemd services, manage deploys.",
    "content": "Generate social posts, schedule content, verify publication.",
    "ops": "Check cron health, monitor resources, route webhooks.",
    "strategy": "Perform market sweeps, analyze yield, cross-chain settlement.",
}

# Default intervals per domain
INTERVALS = {
    "coordinator": 300,
    "security": 60,
    "dev": 120,
    "content": 3600,
    "ops": 300,
    "strategy": 600,
}
