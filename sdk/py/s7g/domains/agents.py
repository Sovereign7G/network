"""Agent swarm & constants (v2.3)."""

from typing import Dict


def swarm_status(self) -> Dict:
    """Get status of all 26 agents."""
    return self._request("GET", "/api/swarm/status")


def swarm_agent_info(self, name: str) -> Dict:
    """Get detailed info for a specific agent."""
    return self._request("GET", f"/api/swarm/agent/{name}")


def swarm_logs(self, agent: str = "", hours: int = 1) -> Dict:
    """Read agent logs from aetherdb_bridge."""
    return self._request("GET", f"/api/swarm/logs?agent={agent}&hours={hours}")


@property
def AGENTS(self):
    return {"total": 62, "ka_sem": 5, "execution": 13, "security": 12,
            "governance": 2, "gtme": 4, "solana_deploy": 3}


@property
def COURTS(self):
    return {"executive": "ExecutiveCourt.sol", "arbitration": "ArbitrationCourt.sol",
            "governance": "AgentGovernance.sol"}


@property
def STABLECOINS(self):
    return ["USDC", "EURC", "USDT", "DAI", "LUSD", "BOLD", "PYUSD"]


@property
def CHAINS(self):
    return ["base", "arbitrum", "solana", "ethereum", "polygon", "tron"]
