#!/usr/bin/env python3
"""High-availability Base↔ICP relayer with active-hot standby failover.
Primary relayer writes heartbeat to aetherdb_bridge. Backup detects
absence and takes over. All state tracked in aetherdb_bridge.
"""
import json, os, time, threading, logging
from http.client import HTTPSConnection
from typing import Optional, Dict, List
from dataclasses import dataclass, field

BASE_RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
ICP_API = "https://ic0.app"
PK = os.environ.get("DEPLOYER_PK", "")

MOVE_VM = "gqshy-7qaaa-aaaaa-qhjua-cai"
AETHERDB = "h54dw-qyaaa-aaaaa-qhjtq-cai"
DAO_ADDR = "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588"
BRIDGE_ADDR = ""  # ICPReverseBridge (set after deploy)
RELAYER_ID = os.getenv("RELAYER_ID", "relayer-001")

POLL = 12
HEARTBEAT_TTL = 120
FAILOVER_TIMEOUT = 300  # 5 min without heartbeat = failover

@dataclass
class PendingItem:
    id: str; item_type: str; data: dict
    queued_at: float; attempts: int = 0; status: str = "pending"

def ic_call(canister: str, method: str, args: list) -> Optional[dict]:
    try:
        c = HTTPSConnection("ic0.app")
        body = json.dumps({"jsonrpc":"2.0","method":"canister_call",
            "params":[canister, method, args],"id":1}).encode()
        c.request("POST",f"/api/v2/canister/{canister}/call",body,
                  {"Content-Type":"application/json"})
        r = json.loads(c.getresponse().read())
        return r
    except: return None

class HARelayer:
    def __init__(self):
        self.id = RELAYER_ID
        self.is_primary = False
        self.pending: List[PendingItem] = []
        self.executed = 0; self.failed = 0
        log = logging.getLogger("HARelayer")
        log.setLevel(logging.INFO); log.addHandler(logging.StreamHandler())
        self.log = log

    def claim_primary(self) -> bool:
        r = ic_call(AETHERDB, "aetherdb_get", ["relayer:primary"])
        current = r.get("result") if r else None
        if current == self.id.encode():
            return True
        if not current or (time.time() - json.loads(current).get("ts",0) > FAILOVER_TIMEOUT):
            ic_call(AETHERDB, "aetherdb_put",
                    ["relayer:primary", json.dumps({"id":self.id,"ts":time.time()})])
            self.log.info(f"Claimed primary: {self.id}")
            return True
        self.log.info(f"Primary is {current}")
        return False

    def heartbeat(self):
        ic_call(AETHERDB, "aetherdb_put",
                [f"relayer:heartbeat:{self.id}",
                 json.dumps({"id":self.id,"ts":time.time(),"pending":len(self.pending)})])

    def poll_dao(self):
        try:
            c = HTTPSConnection("mainnet.base.org")
            c.request("POST","/",json.dumps({"jsonrpc":"2.0","method":"eth_blockNumber",
                "params":[],"id":1}).encode(),{"Content-Type":"application/json"})
            block = json.loads(c.getresponse().read()).get("result","0x0")
            self.log.info(f"Base block: {int(block,16)}")
        except Exception as e:
            self.log.error(f"DAO poll failed: {e}")

    def process_pending(self):
        for item in self.pending[:]:
            if item.status != "pending": continue
            try:
                if item.item_type == "proposal":
                    r = ic_call(MOVE_VM, "queue_proposal", [item.data.get("id","")])
                elif item.item_type == "slash":
                    r = ic_call(AETHERDB, "aetherdb_put",
                                [f"slash:executed:{item.id}", json.dumps(item.data)])
                item.status = "executed"; self.executed += 1
            except:
                item.attempts += 1
                if item.attempts >= 5: item.status = "failed"; self.failed += 1

    def run(self):
        self.log.info(f"Relayer {self.id} starting...")
        while True:
            try:
                self.is_primary = self.claim_primary()
                self.heartbeat()
                if self.is_primary:
                    self.poll_dao()
                    self.process_pending()
            except KeyboardInterrupt: break
            except Exception as e: self.log.error(str(e))
            time.sleep(POLL)

if __name__ == "__main__":
    HARelayer().run()
