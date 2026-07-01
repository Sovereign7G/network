#!/usr/bin/env python3
"""
consensus/gossip.py — GossipSub-style pubsub for consensus messages.
Topics: proposals, prepares, commits, ledger-sync.
"""

import asyncio
import json
import logging
from typing import Dict, Set, Callable, Any
from collections import defaultdict

from .p2p_core import P2PHost, MsgType

logger = logging.getLogger(__name__)


class GossipSub:
    """Simple pubsub over P2P host. Topics are strings, messages are JSON."""

    def __init__(self, p2p: P2PHost):
        self.p2p = p2p
        self.subscribers: Dict[str, Set[Callable]] = defaultdict(set)
        self.seen: Set[str] = set()  # dedup: "topic:seq"

        # Register gossip handler
        p2p.register_handler(MsgType.GOSSIP, self._on_gossip)

    async def publish(self, topic: str, data: Any):
        payload = json.dumps({"topic": topic, "data": data, "sender": self.p2p.peer_id}).encode()
        await self.p2p.broadcast(MsgType.GOSSIP, payload)
        await self._deliver(topic, data, self.p2p.peer_id)

    async def subscribe(self, topic: str, callback: Callable):
        self.subscribers[topic].add(callback)

    async def _on_gossip(self, msg_type: int, payload: bytes, reader, writer):
        try:
            msg = json.loads(payload)
            topic = msg.get("topic")
            data = msg.get("data")
            sender = msg.get("sender", "unknown")
            if topic and data:
                await self._deliver(topic, data, sender)
        except Exception as e:
            logger.error(f"Gossip handler: {e}")

    async def _deliver(self, topic: str, data: Any, sender: str):
        for cb in self.subscribers.get(topic, set()):
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(data)
                else:
                    cb(data)
            except Exception as e:
                logger.error(f"Gossip callback: {e}")
