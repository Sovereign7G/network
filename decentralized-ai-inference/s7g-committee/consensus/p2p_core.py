#!/usr/bin/env python3
"""
consensus/p2p_core.py — Custom Asyncio TCP P2P Core
- Encrypted peer-to-peer communication via asyncio TCP
- Peer identity via Ed25519
- Length-prefixed binary protocol

Message format:
  Magic(3) + Version(1) + Type(1) + Reserved(1) + Len(4) + Payload(N)

Message types: HANDSHAKE=1, GOSSIP=2, KADEMLIA=3, RELAY=4, KEEPALIVE=5
"""

import asyncio
import json
import struct
import hashlib
import logging
import time
from typing import Dict, Optional, Callable, Any, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ── Constants ───────────────────────────────────────────────────────────
MAGIC = b"\x53\x37\x47"  # "S7G"
VERSION = 0x01
HEADER_SIZE = 10  # Magic(3) + Version(1) + Type(1) + Reserved(1) + Len(4)

class MsgType:
    HANDSHAKE = 1
    GOSSIP = 2
    KADEMLIA = 3
    RELAY = 4
    KEEPALIVE = 5
    PBFT_PROPOSAL = 6
    PBFT_PREPARE = 7
    PBFT_COMMIT = 8


@dataclass
class Peer:
    peer_id: str
    host: str
    port: int
    writer: Optional[asyncio.StreamWriter] = None
    reader: Optional[asyncio.StreamReader] = None
    connected_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    is_connected: bool = False

    def to_dict(self) -> dict:
        return {
            "peer_id": self.peer_id,
            "host": self.host,
            "port": self.port,
            "connected_at": self.connected_at,
            "last_seen": self.last_seen,
            "is_connected": self.is_connected,
        }


class P2PHost:
    """Async TCP P2P host for committee node communication."""

    def __init__(
        self,
        node_id: int,
        listen_port: int = 26656,
        bootstrap_peers: Optional[List[str]] = None,
    ):
        self.node_id = node_id
        self.listen_port = listen_port
        self.bootstrap_peers = bootstrap_peers or []

        # Identity (simulated Ed25519-style key via SHA256 for Phase B)
        self.peer_id = hashlib.sha256(
            f"s7g-node-{node_id}".encode()
        ).hexdigest()[:16]

        # State
        self.peers: Dict[str, Peer] = {}
        self._handlers: Dict[int, Callable] = {}
        self._server: Optional[asyncio.Server] = None
        self._running = False
        self._keepalive_task: Optional[asyncio.Task] = None
        self._read_tasks: List[asyncio.Task] = []

        # Stats
        self.bytes_sent = 0
        self.bytes_received = 0
        self.messages_sent = 0
        self.messages_received = 0

        # Register default Handshake handler
        self.register_handler(MsgType.HANDSHAKE, self._on_handshake)

    def register_handler(self, msg_type: int, handler: Callable):
        self._handlers[msg_type] = handler

    async def start(self):
        self._running = True
        self._server = await asyncio.start_server(
            self._on_connect, host="0.0.0.0", port=self.listen_port
        )
        logger.info(
            f"P2P listening on 0.0.0.0:{self.listen_port}, "
            f"peer_id={self.peer_id}"
        )

        # Connect to bootstrap peers
        for addr in self.bootstrap_peers:
            try:
                host, port = addr.rsplit(":", 1)
                await self._connect(host, int(port))
            except Exception as e:
                logger.warning(f"Bootstrap connect {addr} failed: {e}")

        self._keepalive_task = asyncio.create_task(self._keepalive_loop())
        return self

    async def stop(self):
        self.running = False
        if self._keepalive_task:
            self._keepalive_task.cancel()
        
        # 1. Close all active peer writers first
        for pid, peer in list(self.peers.items()):
            if peer.writer:
                try:
                    peer.writer.close()
                except Exception:
                    pass
        self.peers.clear()

        # 2. Cancel all dialed connection readers
        for task in self._read_tasks:
            task.cancel()
        self._read_tasks.clear()

        # 3. Close the server and wait
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        logger.info("P2P stopped")

    async def _on_handshake(self, msg_type: int, payload: bytes, reader, writer):
        try:
            data = json.loads(payload.decode())
            peer_id = data.get("peer_id")
            if peer_id:
                addr = writer.get_extra_info("peername")
                peer = Peer(
                    peer_id=peer_id, host=addr[0], port=addr[1],
                    reader=reader, writer=writer, is_connected=True,
                )
                self.peers[peer_id] = peer
                logger.info(f"Registered incoming peer {peer_id} ({addr[0]}:{addr[1]})")
        except Exception as e:
            logger.error(f"Handshake error: {e}")

    async def _on_connect(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        logger.debug(f"Incoming connection from {addr}")
        try:
            while self._running:
                header = await reader.readexactly(HEADER_SIZE)
                magic, ver, msg_type, _, payload_len = struct.unpack("!3sBBBI", header)
                if magic != MAGIC:
                    logger.warning(f"Bad magic from {addr}")
                    break
                payload = await reader.readexactly(payload_len) if payload_len > 0 else b""

                self.bytes_received += HEADER_SIZE + payload_len
                self.messages_received += 1

                handler = self._handlers.get(msg_type)
                if handler:
                    await handler(msg_type, payload, reader, writer)
                else:
                    logger.debug(f"No handler for type {msg_type}")

        except (asyncio.IncompleteReadError, ConnectionResetError, ConnectionError):
            pass
        except asyncio.CancelledError:
            pass
        finally:
            writer.close()

    async def _read_loop(self, peer_id: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while self._running:
                header = await reader.readexactly(HEADER_SIZE)
                magic, ver, msg_type, _, payload_len = struct.unpack("!3sBBBI", header)
                if magic != MAGIC:
                    break
                payload = await reader.readexactly(payload_len) if payload_len > 0 else b""

                self.bytes_received += HEADER_SIZE + payload_len
                self.messages_received += 1

                handler = self._handlers.get(msg_type)
                if handler:
                    await handler(msg_type, payload, reader, writer)
        except (asyncio.IncompleteReadError, ConnectionResetError, ConnectionError):
            pass
        except asyncio.CancelledError:
            pass
        finally:
            writer.close()
            peer = self.peers.get(peer_id)
            if peer:
                peer.is_connected = False

    async def _connect(self, host: str, port: int) -> Optional[Peer]:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            peer_id = hashlib.sha256(f"s7g-{host}:{port}".encode()).hexdigest()[:16]

            # Send handshake
            handshake = json.dumps({"peer_id": self.peer_id, "node_id": self.node_id}).encode()
            await self._send(writer, MsgType.HANDSHAKE, handshake)

            peer = Peer(
                peer_id=peer_id, host=host, port=port,
                reader=reader, writer=writer, is_connected=True,
            )
            self.peers[peer_id] = peer
            logger.info(f"Connected to peer {peer_id} ({host}:{port})")

            # Start dialed socket read loop in background
            read_task = asyncio.create_task(self._read_loop(peer_id, reader, writer))
            self._read_tasks.append(read_task)

            return peer
        except Exception as e:
            logger.warning(f"Connect to {host}:{port} failed: {e}")
            return None

    async def broadcast(self, msg_type: int, payload: bytes):
        for pid, peer in list(self.peers.items()):
            if peer.is_connected and peer.writer:
                try:
                    await self._send(peer.writer, msg_type, payload)
                    self.messages_sent += 1
                except Exception as e:
                    logger.warning(f"Broadcast to {pid} failed: {e}")
                    peer.is_connected = False

    async def send_to(self, peer_id: str, msg_type: int, payload: bytes) -> bool:
        peer = self.peers.get(peer_id)
        if not peer or not peer.writer:
            return False
        try:
            await self._send(peer.writer, msg_type, payload)
            self.messages_sent += 1
            return True
        except Exception:
            return False

    async def _send(self, writer: asyncio.StreamWriter, msg_type: int, payload: bytes):
        header = struct.pack("!3sBBBI", MAGIC, VERSION, msg_type, 0, len(payload))
        writer.write(header + payload)
        await writer.drain()
        self.bytes_sent += len(header) + len(payload)

    async def _keepalive_loop(self, interval: int = 30):
        while self._running:
            await asyncio.sleep(interval)
            for pid, peer in list(self.peers.items()):
                if peer.writer:
                    try:
                        await self._send(peer.writer, MsgType.KEEPALIVE, b"")
                    except Exception:
                        peer.is_connected = False

    def get_peer_list(self) -> list:
        return [p.to_dict() for p in self.peers.values() if p.is_connected]

    def get_stats(self) -> dict:
        return {
            "peer_id": self.peer_id,
            "node_id": self.node_id,
            "listen_port": self.listen_port,
            "connected_peers": len([p for p in self.peers.values() if p.is_connected]),
            "known_peers": len(self.peers),
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
        }
