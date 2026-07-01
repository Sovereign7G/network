# S7G P2P libp2p Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate `py-libp2p` P2P transport with GossipSub to enable encrypted consensus message propagation between the S7G committee nodes.

**Architecture:** Each S7G node spins up a libp2p host configured with TCP transport, Noise encryption, and GossipSub. The node subscribes to a shared GossipSub topic based on the `COMMITTEE_ID` to broadcast and receive PBFT proposals and votes.

**Tech Stack:** Python 3.11, `py-libp2p`, `asyncio`, GossipSub, Noise protocol.

## Global Constraints
- Target directory: `decentralized-ai-inference/s7g-committee`
- All P2P communications must be authenticated and encrypted via Noise.
- GossipSub is used for consensus propagation.

---

### Task 1: Add libp2p Dependencies & Scaffolding
Install the `py-libp2p` package and create the base P2P connection manager.

**Files:**
- Modify: `decentralized-ai-inference/s7g-committee/requirements.txt`
- Create: `decentralized-ai-inference/s7g-committee/consensus/p2p.py`
- Test: `decentralized-ai-inference/s7g-committee/tests/test_p2p.py`

**Interfaces:**
- Produces: `P2PManager` class with `start` and `stop` methods.

- [ ] **Step 1: Update requirements.txt**
  Add `libp2p` package dependency to `decentralized-ai-inference/s7g-committee/requirements.txt`:
  ```text
  fastapi>=0.100.0
  uvicorn>=0.22.0
  pydantic-settings>=2.0.0
  loguru>=0.7.0
  pytest>=7.0.0
  libp2p>=0.1.5
  ```

- [ ] **Step 2: Install updated requirements**
  Run: `pip install -r decentralized-ai-inference/s7g-committee/requirements.txt`
  Expected: Successful installation of py-libp2p and dependencies.

- [ ] **Step 3: Create consensus/p2p.py**
  Create `decentralized-ai-inference/s7g-committee/consensus/p2p.py` with:
  ```python
  import asyncio
  from loguru import logger
  from libp2p import new_host
  from libp2p.crypto.keys import KeyPair
  from libp2p.peer.id import ID

  class P2PManager:
      def __init__(self, host_address: str, port: int):
          self.host_address = host_address
          self.port = port
          self.host = None

      async def start(self):
          logger.info(f"Starting libp2p host on {self.host_address}:{self.port}")
          # Generate keys
          key_pair = KeyPair.generate()
          self.host = new_host(
              connection_opt={
                  "transport": ["tcp"],
                  "security": ["noise"]
              },
              key_pair=key_pair
          )
          await self.host.get_network().listen(f"/ip4/{self.host_address}/tcp/{self.port}")
          logger.info(f"libp2p Host active at Peer ID: {self.host.get_id().to_base58()}")

      async def stop(self):
          if self.host:
              await self.host.close()
              logger.info("libp2p Host closed successfully.")
  ```

- [ ] **Step 4: Create P2P basic unit test**
  Create `decentralized-ai-inference/s7g-committee/tests/test_p2p.py`:
  ```python
  import sys
  import pytest
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).parent.parent))

  from consensus.p2p import P2PManager

  @pytest.mark.asyncio
  async def test_p2p_host_start_stop():
      manager = P2PManager("127.0.0.1", 26658)
      await manager.start()
      assert manager.host is not None
      assert manager.host.get_id() is not None
      await manager.stop()
  ```

- [ ] **Step 5: Run test to verify it passes**
  Run: `pytest decentralized-ai-inference/s7g-committee/tests/test_p2p.py -v`
  Expected: PASS

- [ ] **Step 6: Commit**
  Run:
  ```bash
  git add decentralized-ai-inference/s7g-committee/requirements.txt decentralized-ai-inference/s7g-committee/consensus/p2p.py decentralized-ai-inference/s7g-committee/tests/test_p2p.py
  git commit -m "feat: add py-libp2p dependencies and baseline p2p host manager"
  ```
