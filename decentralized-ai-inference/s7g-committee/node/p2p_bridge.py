#!/usr/bin/env python3
"""
node/p2p_bridge.py — Bridge between FastAPI app and P2P layer

Provides FastAPI endpoints for managing the P2P network:
- View connected peers
- Get P2P statistics
- Trigger peer discovery
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from node.config import settings
from node.dependencies import get_engine

from consensus.p2p_core import P2PHost
from consensus.gossip import GossipSub
from consensus.kademlia import Kademlia

logger = logging.getLogger(__name__)

# ── Singletons ──────────────────────────────────────────────────────────
_p2p_host: Optional[P2PHost] = None
_gossip: Optional[GossipSub] = None
_kademlia: Optional[Kademlia] = None


def get_p2p_host() -> Optional[P2PHost]:
    return _p2p_host


def get_gossip() -> Optional[GossipSub]:
    return _gossip


def get_kademlia() -> Optional[Kademlia]:
    return _kademlia


async def init_p2p():
    """Initialize the P2P layer (called during startup)."""
    global _p2p_host, _gossip, _kademlia

    bootstrap_peers = settings.PEERS
    if isinstance(bootstrap_peers, str):
        bootstrap_peers = [p.strip() for p in bootstrap_peers.split(",") if p.strip()]

    _p2p_host = P2PHost(
        node_id=settings.NODE_ID,
        listen_port=settings.P2P_PORT,
        bootstrap_peers=bootstrap_peers,
    )
    await _p2p_host.start()

    _gossip = GossipSub(_p2p_host)
    _kademlia = Kademlia(_p2p_host)

    # Subscribe PBFT consensus engine to the gossip network
    engine = get_engine()
    async def consensus_callback(data: dict):
        try:
            msg_type = data.get("type")
            if msg_type == "PRE-PREPARE":
                block = data.get("block")
                if engine.pre_prepare(block):
                    sig = engine._sign(block)
                    await _gossip.publish("consensus", {
                        "type": "PREPARE",
                        "block": block,
                        "from_node": settings.NODE_ID,
                        "signature": sig
                    })
            elif msg_type == "PREPARE":
                block = data.get("block")
                from_node = data.get("from_node")
                signature = data.get("signature")
                quorum_reached = engine.prepare(block, from_node, signature)
                if quorum_reached:
                    sig = engine._sign(block)
                    await _gossip.publish("consensus", {
                        "type": "COMMIT",
                        "block": block,
                        "from_node": settings.NODE_ID,
                        "signature": sig
                    })
            elif msg_type == "COMMIT":
                block = data.get("block")
                from_node = data.get("from_node")
                signature = data.get("signature")
                engine.commit(block, from_node, signature)
        except Exception as e:
            logger.error(f"Error in P2P consensus callback: {e}")

    await _gossip.subscribe("consensus", consensus_callback)

    logger.info(
        f"P2P layer initialized: peer_id={_p2p_host.peer_id}, "
        f"port={settings.P2P_PORT}"
    )
    return _p2p_host


async def shutdown_p2p():
    """Shut down the P2P layer."""
    global _p2p_host
    if _p2p_host:
        await _p2p_host.stop()
        _p2p_host = None


# ── FastAPI Router ──────────────────────────────────────────────────────

router = APIRouter(prefix="/p2p", tags=["p2p"])


@router.get("/peers")
async def get_peers():
    """List all connected peers."""
    host = get_p2p_host()
    if not host:
        raise HTTPException(status_code=503, detail="P2P not initialized")
    return {"peers": host.get_peer_list()}


@router.get("/stats")
async def get_p2p_stats():
    """Get P2P statistics."""
    host = get_p2p_host()
    if not host:
        raise HTTPException(status_code=503, detail="P2P not initialized")
    return host.get_stats()


@router.get("/topics")
async def get_topics():
    """List subscribed gossip topics."""
    gs = get_gossip()
    if not gs:
        raise HTTPException(status_code=503, detail="Gossip not initialized")
    return {"topics": list(gs.topics.keys()), "subscribers": {
        t: list(ps) for t, ps in gs.topics.items()
    }}


@router.post("/discover")
async def trigger_discovery():
    """Manually trigger peer discovery via Kademlia."""
    kad = get_kademlia()
    host = get_p2p_host()
    if not kad or not host:
        raise HTTPException(status_code=503, detail="P2P not initialized")
    
    # Bootstrap: find nodes close to our own ID
    closest = await kad.find_node(host.peer_id)
    return {
        "discovered": len(closest),
        "peers": [{"peer_id": p.peer_id, "address": p.address, "port": p.port} for p in closest]
    }


@router.post("/publish/{topic}")
async def publish_to_topic(topic: str, payload: dict):
    """Publish a message to a gossip topic."""
    gs = get_gossip()
    if not gs:
        raise HTTPException(status_code=503, detail="Gossip not initialized")
    
    await gs.publish(topic, payload)
    return {"status": "published", "topic": topic}
