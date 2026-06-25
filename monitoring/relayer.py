#!/usr/bin/env python3
"""Cross-chain relayer — Base ↔ ICP bridge for DAO proposals and slashing events.

Monitors:
  - SovereignDAO.ProposalExecuted on Base → queues module upgrade on ICP move_vm
  - ICP move_vm.get_pending_slashes() → submits to ICPReverseBridge on Base

Requires: DEPLOYER_PK env var with gas funds on Base.
"""
import json, os, time, hmac, hashlib
from http.client import HTTPSConnection
from typing import Optional

BASE_RPC = "https://mainnet.base.org"
ICP_API = "https://oyipx-nyaaa-aaaab-qhbja-cai.raw.icp0.io"
DEPLOYER_PK = os.environ.get("DEPLOYER_PK", "")

# Contracts
DAO_ADDR = "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588"
BRIDGE_ADDR = ""  # ICPReverseBridge — set after deploy

POLL_INTERVAL = 30  # seconds
CONFIRMATIONS = 5   # wait N blocks before relaying

def base_rpc(method: str, params: list) -> Optional[dict]:
    try:
        conn = HTTPSConnection("mainnet.base.org")
        body = json.dumps({"jsonrpc":"2.0","method":method,"params":params,"id":1}).encode()
        conn.request("POST", "/", body, {"Content-Type":"application/json"})
        return json.loads(conn.getresponse().read())
    except: return None

def icp_query(endpoint: str) -> Optional[str]:
    try:
        conn = HTTPSConnection("oyipx-nyaaa-aaaab-qhbja-cai.raw.icp0.io")
        conn.request("GET", f"/{endpoint}")
        return conn.getresponse().read().decode()
    except: return None

def get_last_block() -> int:
    r = base_rpc("eth_blockNumber", [])
    return int(r["result"], 16) if r else 0

def get_logs(addr: str, topic: str, from_block: int, to_block: int) -> list:
    r = base_rpc("eth_getLogs", [{
        "address": addr,
        "topics": [topic],
        "fromBlock": hex(from_block),
        "toBlock": hex(to_block)
    }])
    return r.get("result", []) if r else []

def relayer_loop():
    print("[Relayer] Starting Base↔ICP bridge...")
    last_block = get_last_block()
    seen_proposals = set()
    seen_slashes = set()

    while True:
        try:
            current = get_last_block()
            if current > last_block + CONFIRMATIONS:
                # Check for DAO proposals executed on Base → relay to ICP
                logs = get_logs(DAO_ADDR,
                    "0x712ae0423f3e20f52f1bd0d87f4d4e6b77a15d8a7ee9e6934a5182bc6ae2e9d",
                    last_block, current)
                for log in logs:
                    pid = log.get("transactionHash", "")
                    if pid and pid not in seen_proposals:
                        seen_proposals.add(pid)
                        print(f"[Relayer] DAO proposal executed: {pid[:20]}...")
                        print(f"  → Would queue on ICP move_vm: register_module()")
                        # In production: call ICP canister here

                # Check for pending slashes on ICP → relay to Base
                pending = icp_query("get_pending_slashes")
                if pending and pending not in seen_slashes:
                    seen_slashes.add(pending)
                    print(f"[Relayer] ICP slash events: {pending[:100]}...")
                    print(f"  → Would submit to ICPReverseBridge.submitSlash()")
                    # In production: submit tx to Base here

                last_block = current

            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print(f"[{ts}] Block {current} — {len(seen_proposals)} proposals, {len(seen_slashes)} slashes")

        except Exception as e:
            print(f"[Relayer Error] {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    if not DEPLOYER_PK:
        print("[Relayer] WARNING: DEPLOYER_PK not set — dry-run mode (no transactions sent)")
    relayer_loop()
