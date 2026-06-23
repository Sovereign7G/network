#!/usr/bin/env python3
"""S7G Developer SDK — x402-enabled 7G API client.
Enables developers and AI agents to call 7G services with pay-per-use micropayments.

Usage:
    client = S7GClient(wallet_private_key="0x...")
    result = client.initiate_call("alice.eth", "bob.eth")
    beam = client.calculate_beam(37.77, -122.42, "node-123")
"""
import json, os, time, hashlib, hmac
from decimal import Decimal
from http.client import HTTPSConnection
from typing import Dict, Optional

S7G_API = os.getenv("S7G_API_URL", "https://api.7g.network")
S7G_TREASURY = os.getenv("S7G_TREASURY", "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611")

class S7GClient:
    """x402-enabled 7G client for developers and AI agents."""

    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        self.api_key = api_key or os.getenv("S7G_API_KEY", "")
        self.secret = secret or os.getenv("S7G_SECRET", "")
        self.base = S7G_API

    def _sign(self, path: str, amount: Decimal) -> str:
        """Create an X-PAYMENT header value using HMAC."""
        payload = json.dumps({
            "path": path, "amount": str(amount),
            "recipient": S7G_TREASURY, "ts": int(time.time()),
            "apikey": self.api_key,
        })
        sig = hmac.new(
            self.secret.encode(), f"{path}:{amount}:{S7G_TREASURY}".encode(),
            hashlib.sha256
        ).hexdigest()[:16]
        return f"{payload}.{sig}"

    def _request(self, method: str, path: str, body: Optional[Dict] = None,
                 amount: Optional[Decimal] = None) -> Dict:
        price = amount or Decimal("0.001")
        x_payment = self._sign(path, price)

        # Try with payment
        try:
            c = HTTPSConnection(self.base.replace("https://", ""))
            c.request(method, path,
                      body=json.dumps(body).encode() if body else None,
                      headers={
                          "Content-Type": "application/json",
                          "X-PAYMENT": x_payment,
                          "X-API-Key": self.api_key,
                      })
            resp = c.getresponse()
            data = json.loads(resp.read().decode())
            if resp.status == 402:
                # Follow 402 flow — retry with payment
                new_payment = self._sign(path, price)
                return self._request(method, path, body, amount)
            return data
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def initiate_call(self, caller: str, callee: str) -> Dict:
        """Initiate a 7G call. ~$0.001."""
        return self._request("POST", "/api/call/initiate",
                             {"caller": caller, "callee": callee},
                             Decimal("0.001"))

    def get_call_status(self, session_id: str) -> Dict:
        """Get call status. ~$0.0001."""
        return self._request("GET", f"/api/call/status?session_id={session_id}",
                             amount=Decimal("0.0001"))

    def calculate_beam(self, lat: float, lon: float, node_id: str) -> Dict:
        """Calculate beamforming coefficients. ~$0.001."""
        return self._request("POST", "/api/beam/calculate",
                             {"lat": lat, "lon": lon, "node_id": node_id},
                             Decimal("0.001"))

    def get_beam_status(self, beam_id: str) -> Dict:
        """Get beam status. ~$0.0001."""
        return self._request("GET", f"/api/beam/status?beam_id={beam_id}",
                             amount=Decimal("0.0001"))

    def register_node(self, node_id: str, wallet: str) -> Dict:
        """Register a 7G node. ~$0.01."""
        return self._request("POST", "/api/node/register",
                             {"node_id": node_id, "wallet": wallet},
                             Decimal("0.01"))

    def heartbeat(self, node_id: str) -> Dict:
        """Send a node heartbeat. ~$0.0001."""
        return self._request("POST", "/api/node/heartbeat",
                             {"node_id": node_id},
                             amount=Decimal("0.0001"))
