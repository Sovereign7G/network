#!/usr/bin/env python3
"""
agents/hermes_agents.py — Complete S7G Hermes Agent Registry

All agents registered for the S7G network, including the new
Pair Stack agents for distribution, provenance, committee P2P, and A2A mesh.

Phase A: s7g-sidecar — Sidecar distribution over P2P
Phase B: s7g-mobile-ota — Mobile OTA stubs (CI/CD)
Phase C: s7g-provenance — Hypercore audit trail
Phase D: s7g-committee — Committee P2P node
Phase E: s7g-a2a-bridge — A2A cross-vendor agent mesh
Core:   s7g-graph-query, s7g-triage, s7g-semantic, s7g-slack
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hermes_security_auditor import HermesSecurityAuditor
from hermes_cost_optimizer import HermesCostOptimizer
from hermes_capacity_planner import HermesCapacityPlanner
from hermes_env_manager import HermesEnvironmentManager
from pair_stack_agent import PairStackAgent

__all__ = [
    "HermesSecurityAuditor",
    "HermesCostOptimizer",
    "HermesCapacityPlanner",
    "HermesEnvironmentManager",
    "PairStackAgent",
]
