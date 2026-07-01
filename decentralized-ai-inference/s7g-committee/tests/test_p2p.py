import sys
import pytest
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from consensus.p2p_core import P2PHost
from consensus.gossip import GossipSub

@pytest.mark.asyncio
async def test_p2p_secure_gossip():
    # Start two P2PHost nodes
    node1 = P2PHost(node_id=1, listen_port=26671, bootstrap_peers=["127.0.0.1:26672"])
    node2 = P2PHost(node_id=2, listen_port=26672, bootstrap_peers=["127.0.0.1:26671"])
    
    await node1.start()
    await node2.start()
    
    # Initialize GossipSub layers
    gossip1 = GossipSub(node1)
    gossip2 = GossipSub(node2)
    
    # Wait for the handshake and TCP key negotiation
    await asyncio.sleep(1.0)
    
    # Subscribe node2 to consensus topic
    received_messages = []
    async def consensus_callback(data: dict):
        received_messages.append(data)
        
    await gossip2.subscribe("consensus", consensus_callback)
    
    # Publish an encrypted consensus message from node1
    await gossip1.publish("consensus", {"type": "PROPOSAL", "data": "cons-data"})
    await asyncio.sleep(0.5)
    
    # Check if node2 received the gossiped message
    assert len(received_messages) == 1
    assert received_messages[0]["type"] == "PROPOSAL"
    
    await node1.stop()
    await node2.stop()
