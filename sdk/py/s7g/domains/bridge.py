"""CCTP bridge, POS settlement, Court operations & stablecoin routes."""

from typing import Dict


def pos_settle(self, agent_did: str, merchant_id: str, amount: int,
               corridor: str = "base_usdc", credential: str = "0x") -> Dict:
    """Settle a POS transaction through the S7G network."""
    return self._request("POST", "/api/pos/settle", {
        "agent_did": agent_did, "merchant_id": merchant_id,
        "amount": amount, "corridor": corridor, "credential": credential,
    })


def pos_verify(self, agent_did: str, amount: int, corridor: str,
               proof_hash: str) -> Dict:
    """Verify a POS settlement proof."""
    return self._request("POST", "/api/pos/verify", {
        "agent_did": agent_did, "amount": amount,
        "corridor": corridor, "proof_hash": proof_hash,
    })


def pos_status(self) -> Dict:
    """Get POS integration status."""
    return self._request("GET", "/api/pos/status")


@property
def POS_PLATFORMS(self):
    return ["zavo", "razorpay", "airwallex"]


@property
def POS_CORRIDORS(self):
    return ["base_usdc", "base_eurc", "esc_ela", "icp_cycles"]


# ── Court Operations (S7G v2.2) ──────────────────────────────


def court_executive_pause(self, agent_name: str) -> Dict:
    """ExecutiveCourt: pause an agent (3-of-5 judges)."""
    return self._request("POST", "/api/court/executive/pause", {"agent": agent_name})


def court_executive_freeze(self, corridor: str) -> Dict:
    """ExecutiveCourt: freeze a stablecoin corridor."""
    return self._request("POST", "/api/court/executive/freeze", {"corridor": corridor})


def court_arbitration_file(self, defendant: str, evidence: str) -> Dict:
    """ArbitrationCourt: file a dispute (requires 1,000 S7G bond)."""
    return self._request("POST", "/api/court/arbitration/file",
                         {"defendant": defendant, "evidence": evidence})


def court_arbitration_status(self, case_id: int) -> Dict:
    """ArbitrationCourt: check case status."""
    return self._request("GET", f"/api/court/arbitration/{case_id}")


def court_governance_params(self, agent: str = "", param: str = "") -> Dict:
    """AgentGovernance: get or set agent parameters."""
    return self._request("GET", f"/api/court/governance/params?agent={agent}&param={param}")


def court_governance_propose(self, agent: str, param: str, value: int) -> Dict:
    """AgentGovernance: propose a parameter change (7-day optimistic)."""
    return self._request("POST", "/api/court/governance/propose",
                         {"agent": agent, "param": param, "value": value})


# ── Stablecoin Engine ────────────────────────────────────────


def cctp_bridge_status(self, chain: str = "base") -> Dict:
    """CCTP Bridge: check cross-chain USDC bridge status."""
    return self._request("GET", f"/api/stablecoin/cctp?chain={chain}")


def cctp_transfer(self, amount: int, source: str, dest: str) -> Dict:
    """CCTP Bridge: transfer USDC cross-chain with CCTP."""
    return self._request("POST", "/api/stablecoin/cctp/transfer",
                         {"amount": amount, "source": source, "dest": dest})


def stablecoin_routes(self) -> Dict:
    """Get current stablecoin routing table (all corridors)."""
    return self._request("GET", "/api/stablecoin/routes")


def global_rate_card(self, currency: str = "USD") -> Dict:
    """GlobalRateCard: get per-minute rate for any currency."""
    return self._request("GET", f"/api/stablecoin/rates?currency={currency}")


def solana_cctp_settle(self, amount: int, dest: str = "base") -> Dict:
    """Settle USDC from Solana to Base via CCTP bridge."""
    return self._request("POST", "/api/solana/cctp/settle",
                         {"amount": amount, "dest": dest})
