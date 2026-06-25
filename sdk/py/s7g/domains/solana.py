"""Solana integration methods (v2.3+)."""

from typing import Dict


def solana_validator_info(self, identity: str = "") -> Dict:
    """Get Solana validator info. If identity empty, returns S7G validator."""
    return self._request("GET", f"/api/solana/validator?identity={identity}")


def solana_validator_stake(self, amount_sol: float) -> Dict:
    """Stake SOL to S7G Solana validator node."""
    return self._request("POST", "/api/solana/stake",
                         {"amount": amount_sol, "action": "stake"})


def solana_validator_unstake(self, amount_sol: float) -> Dict:
    """Unstake SOL from S7G Solana validator."""
    return self._request("POST", "/api/solana/stake",
                         {"amount": amount_sol, "action": "unstake"})


def solana_validator_rewards(self) -> Dict:
    """Get S7G Solana validator reward history."""
    return self._request("GET", "/api/solana/rewards")


def solana_swap(self, token_in: str, token_out: str, amount: float) -> Dict:
    """Swap tokens on Solana via Jupiter aggregator."""
    return self._request("POST", "/api/solana/swap",
                         {"token_in": token_in, "token_out": token_out, "amount": amount})


def solana_balance(self, address: str = "") -> Dict:
    """Get SOL or token balance on Solana."""
    return self._request("GET", f"/api/solana/balance?address={address}")


def solana_transfer(self, to: str, amount_sol: float) -> Dict:
    """Transfer SOL to another address."""
    return self._request("POST", "/api/solana/transfer",
                         {"to": to, "amount": amount_sol})


def solana_moneygram_track(self) -> Dict:
    """Track MoneyGram Solana validator activity."""
    return self._request("GET", "/api/solana/moneygram")


def solana_network_stats(self) -> Dict:
    """Get Solana network statistics (TPS, validators, epoch)."""
    return self._request("GET", "/api/solana/network")


def solana_depin_projects(self) -> Dict:
    """Get list of DePIN projects active on Solana."""
    return self._request("GET", "/api/solana/depin")
