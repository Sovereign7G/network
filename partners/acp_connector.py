#!/usr/bin/env python3
"""
ACP Partner Connector — Discover and connect to partner agent platforms.
"""
import json, time, http.client, urllib.parse
from typing import Dict, List, Optional

class ACPClient:
    """Minimal ACP client for partner discovery and task execution."""
    
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.info = {}

    def _request(self, method: str, path: str, body: dict = None) -> Optional[Dict]:
        try:
            parsed = urllib.parse.urlparse(self.base)
            conn_cls = http.client.HTTPConnection if parsed.scheme == "http" else http.client.HTTPSConnection
            c = conn_cls(parsed.netloc, timeout=10)
            b = json.dumps(body).encode() if body else None
            c.request(method, path, b, {"Content-Type":"application/json"})
            r = c.getresponse()
            return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    def discover(self) -> Optional[Dict]:
        self.info = self._request("GET", "/.well-known/agent.json")
        return self.info

    def execute(self, task: str, params: dict = None, agent: str = "auto") -> Optional[Dict]:
        return self._request("POST", "/api/agent/execute",
                             {"task": task, "parameters": params or {}, "agent": agent})

PARTNER_REGISTRY = {
    "helium": {"url": "https://acp.helium.com", "desc": "DePIN IoT network"},
    "chainlink": {"url": "https://acp.chainlink.com", "desc": "Price oracle network"},
    "thegraph": {"url": "https://acp.thegraph.com", "desc": "Data indexing protocol"},
}

if __name__ == '__main__':
    print("=== ACP Partner Discovery ===\n")
    for name, cfg in PARTNER_REGISTRY.items():
        client = ACPClient(cfg["url"])
        info = client.discover()
        status = "✅" if info and "name" in info else "❌"
        print(f"  {status} {name:12s} {cfg['desc']:30s} {cfg['url']}")
        if info and "name" in info:
            print(f"       Name: {info.get('name')}")
            print(f"       Agents: {info.get('agents', '?')}")
    print("\nPartners can be connected once their ACP endpoints are live.")
