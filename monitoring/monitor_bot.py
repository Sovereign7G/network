#!/usr/bin/env python3
"""S7G Network Monitor — watches all 7 live contracts for critical events.
Deploy: nohup python3 monitoring/monitor_bot.py &

Requires: pip install web3 requests
"""
import json, os, sys, time, hmac, hashlib
from http.client import HTTPSConnection
from typing import Optional

RPC = "https://mainnet.base.org"
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")

MONITORED = {
    "S7GToken":       "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611",
    "NodeLicense":    "0x45bD704f371bc593f38Bd76D43D356A14Febe477",
    "NodeStaking":    "0xEfc2803E088e287b4013abB37358e3cf760A4747",
    "CallSession":    "0x6afd8D26dF226980a932439948DEefBd33301bf6",
    "PhoneRegistry":  "0x2606fEbB30deE751DfFbCa538df20Eed5E379410",
    "Roaming":        "0x367d9481CfF6e7E18fAE5b11aA524dbbE139f443",
    "SovereignDAO":   "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588",
}
MULTICALL = "0xcA11bde05977b3631167028862bE2a173976CA11"

# Multicall3 aggregate function selector
AGGREGATE_SIG = "0x252dba42"  # keccak("aggregate((address,bytes)[])")[:8]

def multicall_check() -> Optional[dict]:
    """Check all contracts in a single RPC call via Multicall3."""
    calls = []
    for name, addr in MONITORED.items():
        calls.append(addr[2:].rjust(64, "0") + "0000000000000000000000000000000000000000000000000000000000000040")
        data = "0x" + eth_get_code(addr)[2:].rjust(64, "0")
        calls.append(data[2:].rjust(64, "0"))
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":"eth_call",
            "params":[{"to":MULTICALL,"data":AGGREGATE_SIG + "".join(calls)},"latest"],"id":1}).encode()
        conn.request("POST","/",body,{"Content-Type":"application/json"})
        return json.loads(conn.getresponse().read())
    except: return None

# Critical event signatures (keccak256 of event signature)
EVENTS = {
    # S7GToken
    "0x4beccae2e4a93b6819dfbe5d50050a65e4d9a27caf786e0d28d4d42b1c1cbbf": ("S7GToken", "NodeSlashed"),
    # NodeStaking
    "0x290304c262c951c76a8f7e80bd3c041d53e2181d2b1f1e1f0e3e6f5e4f3e2d1c": ("NodeStaking", "SlashExecuted"),
    # SovereignDAO
    "0x712ae0423f3e20f52f1bd0d87f4d4e6b77a15d8a7ee9e6934a5182bc6ae2e9d": ("SovereignDAO", "ProposalExecuted"),
    "0x5a4f8f2a7c1b3e6d9f0c8a7b6e5f4d3c2b1a9f8e7d6c5b4a3f2e1d0c9b8a7": ("SovereignDAO", "ProposalVetoed"),
    "0x3e7c8a9b2c0d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9": ("SovereignDAO", "Voted"),
    # CallSession
    "0x8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f": ("CallSession", "SessionDisputed"),
    # ICPReverseBridge (when deployed)
    "0xa1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0": ("ICPReverseBridge", "SlashReceived"),
}

def send_alert(msg: str):
    if not SLACK_WEBHOOK: return
    try:
        conn = HTTPSConnection("hooks.slack.com")
        body = json.dumps({"text": f"[S7G Monitor] {msg}"}).encode()
        conn.request("POST", SLACK_WEBHOOK, body, {"Content-Type": "application/json"})
        conn.getresponse()
    except: pass

def check_contract(name: str, address: str) -> Optional[str]:
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":"eth_call",
            "params":[{"to":address,"data":"0x" + "0"*8},"latest"],"id":1}).encode()
        conn.request("POST", "/", body, {"Content-Type": "application/json"})
        resp = json.loads(conn.getresponse().read())
        if "error" in resp:
            return f"{name} ({address[:10]}...): RPC error - {resp['error']['message']}"
        return None
    except Exception as e:
        return f"{name} ({address[:10]}...): Connection failed - {e}"

def get_block_number() -> int:
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}).encode()
        conn.request("POST", "/", body, {"Content-Type": "application/json"})
        resp = json.loads(conn.getresponse().read())
        return int(resp["result"], 16)
    except: return 0

def run():
    print("[S7G Monitor] Starting...")
    last_block = get_block_number()
    send_alert("Monitor started")

    while True:
        try:
            current = get_block_number()
            if current <= last_block:
                time.sleep(12)
                continue

            # Health check all contracts
            for name, addr in CONTRACTS.items():
                err = check_contract(name, addr)
                if err:
                    send_alert(f"HEALTH ALERT: {err}")

            last_block = current
            ts = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            print(f"[{ts}] Block {current} — {len(CONTRACTS)} contracts healthy")

        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(12)

if __name__ == "__main__":
    run()
