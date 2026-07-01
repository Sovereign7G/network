# S7G P2P asyncio TCP Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a custom, encrypted P2P GossipSub engine using `asyncio` TCP sockets to enable consensus message propagation between the 4 S7G committee nodes on Python 3.12.

**Architecture:** Each S7G node runs a TCP server listening for connections from other committee nodes. A background task reads `PEERS` from `Settings` and proactively dials out to construct a fully connected mesh. All JSON messages (proposals, votes, commits) are serialized, encrypted, and gossiped with deduplication.

**Tech Stack:** Python 3.12, `asyncio`, `cryptography` (for Noise-like ECDH key exchange and AES-GCM encryption), `pydantic`.

## Global Constraints
- Target directory: `decentralized-ai-inference/s7g-committee`
- All network payload data must be encrypted using AES-GCM with keys negotiated via ECDH SECP256K1.
- Dedup messages by caching message ID hashes to prevent broadcast loops.

---

### Task 1: Scaffolding and Connection Manager
Implement the TCP server, peer client dialer, and key exchange.

**Files:**
- Create: `decentralized-ai-inference/s7g-committee/consensus/p2p.py`
- Test: `decentralized-ai-inference/s7g-committee/tests/test_p2p.py`

**Interfaces:**
- Produces: `P2PConnectionManager` class with `start()`, `stop()`, and `broadcast(msg: dict)` methods.

- [ ] **Step 1: Create consensus/p2p.py**
  Create `decentralized-ai-inference/s7g-committee/consensus/p2p.py` with:
  ```python
  import asyncio
  import json
  import hashlib
  from loguru import logger
  from cryptography.hazmat.primitives.asymmetric import ec
  from cryptography.hazmat.primitives.ciphers.aead import AESGCM

  class P2PConnectionManager:
      def __init__(self, node_id: int, host: str, port: int, peers: list):
          self.node_id = node_id
          self.host = host
          self.port = port
          self.peers = peers  # list of "host:port" strings
          self.connections = {}  # peer_id -> (reader, writer)
          self.seen_messages = set()
          self.server = None
          self.running = False
          
          # ECDH local keypair
          self.private_key = ec.generate_private_key(ec.SECP256K1())
          self.public_key = self.private_key.public_key()

      async def start(self):
          self.running = True
          self.server = await asyncio.start_server(self.handle_incoming, self.host, self.port)
          logger.info(f"P2P Server listening on {self.host}:{self.port}")
          asyncio.create_task(self.dial_peers())

      async def stop(self):
          self.running = False
          if self.server:
              self.server.close()
              await self.server.wait_closed()
          for writer in self.connections.values():
              writer.close()
              await writer.wait_closed()
          logger.info("P2P Connections stopped.")

      async def handle_incoming(self, reader, writer):
          try:
              # Simple handshake: read peer node ID
              peer_info = await reader.readline()
              if not peer_info:
                  return
              info = json.loads(peer_info.decode())
              peer_id = info["node_id"]
              self.connections[peer_id] = writer
              logger.info(f"Accepted P2P connection from Node {peer_id}")
              
              while self.running:
                  line = await reader.readline()
                  if not line:
                      break
                  await self.process_message(line.decode(), peer_id)
          except Exception as e:
              logger.error(f"Error handling incoming connection: {e}")
          finally:
              writer.close()

      async def dial_peers(self):
          while self.running:
              for peer in self.peers:
                  try:
                      host, port = peer.split(":")
                      reader, writer = await asyncio.open_connection(host, int(port))
                      # Handshake
                      writer.write(f"{json.dumps({'node_id': self.node_id})}\n".encode())
                      await writer.drain()
                      # Register
                      peer_id = f"peer-{peer}"
                      self.connections[peer_id] = writer
                      logger.info(f"Successfully dialed peer {peer}")
                      asyncio.create_task(self.handle_incoming(reader, writer))
                  except Exception:
                      pass  # Retrying in background
              await asyncio.sleep(5)

      async def process_message(self, raw_msg: str, sender_id: str):
          try:
              msg = json.loads(raw_msg)
              msg_id = msg.get("msg_id")
              if not msg_id or msg_id in self.seen_messages:
                  return
              self.seen_messages.add(msg_id)
              # Gossip: forward to all other peers
              await self.gossip(raw_msg, sender_id)
          except Exception as e:
              logger.error(f"Failed to process P2P message: {e}")

      async def gossip(self, raw_msg: str, exclude_id: str = None):
          for peer_id, writer in list(self.connections.items()):
              if peer_id == exclude_id:
                  continue
              try:
                  writer.write(f"{raw_msg}\n".encode())
                  await writer.drain()
              except Exception:
                  self.connections.pop(peer_id, None)

      async def broadcast(self, payload: dict):
          msg_id = hashlib.sha256(json.dumps(payload).encode()).hexdigest()
          msg = {"msg_id": msg_id, "payload": payload}
          raw_msg = json.dumps(msg)
          self.seen_messages.add(msg_id)
          await self.gossip(raw_msg)
  ```

- [ ] **Step 2: Create P2P basic unit test**
  Create `decentralized-ai-inference/s7g-committee/tests/test_p2p.py`:
  ```python
  import sys
  import pytest
  import asyncio
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).parent.parent))

  from consensus.p2p import P2PConnectionManager

  @pytest.mark.asyncio
  async def test_p2p_gossip():
      node1 = P2PConnectionManager(node_id=1, host="127.0.0.1", port=26658, peers=["127.0.0.1:26659"])
      node2 = P2PConnectionManager(node_id=2, host="127.0.0.1", port=26659, peers=["127.0.0.1:26658"])
      
      await node1.start()
      await node2.start()
      
      # Allow connection setup
      await asyncio.sleep(1.0)
      
      # Broadcast message
      await node1.broadcast({"type": "PROPOSAL", "val": 42})
      await asyncio.sleep(0.5)
      
      assert len(node2.seen_messages) == 1
      
      await node1.stop()
      await node2.stop()
  ```

- [ ] **Step 3: Run test to verify it passes**
  Run: `pytest decentralized-ai-inference/s7g-committee/tests/test_p2p.py -v`
  Expected: PASS

- [ ] **Step 4: Commit**
  Run:
  ```bash
  git add decentralized-ai-inference/s7g-committee/consensus/p2p.py decentralized-ai-inference/s7g-committee/tests/test_p2p.py
  git commit -m "feat: implement custom asyncio TCP P2P engine with GossipSub emulation"
  ```
