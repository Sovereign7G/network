#!/usr/bin/env python3
"""
consensus/kademlia.py — Lightweight DHT for peer discovery.
Simple K-bucket-style routing table, ping/find_node/store operations.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import time

from .p2p_core import P2PHost, MsgType

logger = logging.getLogger(__name__)

K = 8  # bucket size


@dataclass
class KBucketEntry:
    peer_id: str
    address: str
    port: int
    last_seen: float = field(default_factory=time.time)


class Kademlia:
    """Minimal Kademlia DHT for peer discovery over the P2P host."""

    def __init__(self, p2p: P2PHost):
        self.p2p = p2p
        self.routing: Dict[str, KBucketEntry] = {}
        self.store: Dict[str, bytes] = {}

        p2p.register_handler(MsgType.KADEMLIA, self._on_kademlia)

    async def ping(self, peer_id: str) -> bool:
        return await self.p2p.send_to(peer_id, MsgType.KADEMLIA, json.dumps({"op": "ping"}).encode())

    async def find_node(self, target: str) -> List[KBucketEntry]:
        # Return closest K entries by XOR distance
        closest = sorted(
            self.routing.values(),
            key=lambda e: self._xor_distance(e.peer_id, target),
        )[:K]
        return closest

    async def store(self, key: str, value: bytes):
        self.store[key] = value
        # Replicate to closest peers
        peers = await self.find_node(key)
        for p in peers:
            await self.p2p.send_to(
                p.peer_id,
                MsgType.KADEMLIA,
                json.dumps({"op": "store", "key": key, "value": value.hex()}).encode(),
            )

    async def _on_kademlia(self, msg_type: int, payload: bytes, reader, writer):
        try:
            msg = json.loads(payload)
            op = msg.get("op")

            if op == "ping":
                response = json.dumps({"op": "pong", "peer_id": self.p2p.peer_id}).encode()
                header = b"\x53\x37\x47\x01" + bytes([MsgType.KADEMLIA, 0, 0, 0, 0])
                import struct
                header = struct.pack("!3sBBBI", b"S7G", 1, MsgType.KADEMLIA, 0, len(response))
                writer.write(header + response)
                await writer.drain()

            elif op == "store":
                key = msg.get("key")
                value = bytes.fromhex(msg.get("value", ""))
                if key and value:
                    self.store[key] = value

            elif op == "find_node":
                target = msg.get("target")
                peers = await self.find_node(target or self.p2p.peer_id)
                response = json.dumps({
                    "op": "nodes",
                    "peers": [{"peer_id": p.peer_id, "address": p.address, "port": p.port} for p in peers],
                }).encode()
                import struct
                header = struct.pack("!3sBBBI", b"S7G", 1, MsgType.KADEMLIA, 0, len(response))
                writer.write(header + response)
                await writer.drain()

        except Exception as e:
            logger.error(f"Kademlia handler: {e}")

    def _xor_distance(self, a: str, b: str) -> int:
        try:
            return int(a, 16) ^ int(b, 16)
        except ValueError:
            return 0

    def add_peer(self, peer_id: str, address: str, port: int):
        self.routing[peer_id] = KBucketEntry(peer_id=peer_id, address=address, port=port)
