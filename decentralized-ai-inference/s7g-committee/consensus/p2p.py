import asyncio
import json
import struct
import hashlib
from loguru import logger
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

class P2PConnectionManager:
    def __init__(self, node_id: int, host: str, port: int, peers: list):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers = peers  # list of "host:port" strings
        self.connections = {}  # peer_id -> (reader, writer, aesgcm_instance)
        self.seen_messages = set()
        self.server = None
        self.running = False
        self.tasks = []  # track dialed & keepalive tasks
        self.incoming_tasks = set()  # track accepted server tasks
        
        # SECP256K1 Key Pair for ECDH key exchange
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.pub_bytes = self.public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.UncompressedPoint
        )

    async def start(self):
        self.running = True
        self.server = await asyncio.start_server(self.handle_incoming, self.host, self.port)
        logger.info(f"Node {self.node_id}: S7G P2P Server listening on {self.host}:{self.port}")
        dial_task = asyncio.create_task(self.dial_peers())
        self.tasks.append(dial_task)

    async def stop(self):
        self.running = False
        
        # 1. Close all active peer writers first to break reading loops
        for peer_id, (reader, writer, _) in list(self.connections.items()):
            try:
                writer.close()
            except Exception:
                pass
        self.connections.clear()

        # 2. Cancel all dialed tasks
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()

        # 3. Cancel all accepted incoming tasks
        for task in list(self.incoming_tasks):
            task.cancel()
        self.incoming_tasks.clear()

        # 4. Finally close the server and wait for it to close
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        logger.info(f"Node {self.node_id}: S7G P2P Server stopped.")

    async def handle_incoming(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        current_task = asyncio.current_task()
        self.incoming_tasks.add(current_task)
        peer_id = None
        try:
            # 1. Exchange Node IDs & Public Keys
            handshake_payload = {
                "node_id": self.node_id,
                "public_key": self.pub_bytes.hex()
            }
            writer.write(f"{json.dumps(handshake_payload)}\n".encode())
            await writer.drain()

            # Read client's handshake
            client_handshake_raw = await reader.readline()
            if not client_handshake_raw:
                return
            client_handshake = json.loads(client_handshake_raw.decode())
            peer_id = client_handshake["node_id"]
            peer_pub_hex = client_handshake["public_key"]

            # 2. Key Exchange (ECDH)
            peer_pub_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256K1(), bytes.fromhex(peer_pub_hex)
            )
            shared_key = self.private_key.exchange(ec.ECDH(), peer_pub_key)
            
            # Derive symmetric AES-GCM key
            digest = hashlib.sha256(shared_key).digest()
            aesgcm = AESGCM(digest)

            self.connections[peer_id] = (reader, writer, aesgcm)
            logger.info(f"Node {self.node_id}: Secure P2P connection established with Node {peer_id}")

            # Read encrypted messages loop
            while self.running:
                # Read 4-byte length prefix
                length_bytes = await reader.readexactly(4)
                length = struct.unpack("!I", length_bytes)[0]
                
                # Read encrypted frame
                encrypted_data = await reader.readexactly(length)
                
                # Decrypt frame using AES-GCM (fixed 12-byte nonce derived from payload hash)
                nonce = digest[:12]
                decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
                
                await self.process_message(decrypted_data.decode(), peer_id)
        except asyncio.IncompleteReadError:
            logger.debug(f"Node {self.node_id}: Connection from peer closed.")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Node {self.node_id}: Error handling incoming connection: {e}")
        finally:
            self.incoming_tasks.discard(current_task)
            if peer_id:
                self.connections.pop(peer_id, None)
            writer.close()

    async def dial_peers(self):
        try:
            while self.running:
                for peer in self.peers:
                    # Skip dialing if already connected to this peer ID or endpoint
                    already_connected = False
                    for conn_id in self.connections.keys():
                        if str(conn_id) in peer or peer in str(conn_id) or str(conn_id) == peer:
                            already_connected = True
                            break
                    if already_connected:
                        continue
                    
                    try:
                        host, port = peer.split(":")
                        reader, writer = await asyncio.open_connection(host, int(port))
                        
                        # 1. Exchange Handshake
                        handshake_payload = {
                            "node_id": self.node_id,
                            "public_key": self.pub_bytes.hex()
                        }
                        writer.write(f"{json.dumps(handshake_payload)}\n".encode())
                        await writer.drain()

                        # Read server's handshake
                        server_handshake_raw = await reader.readline()
                        if not server_handshake_raw:
                            continue
                        server_handshake = json.loads(server_handshake_raw.decode())
                        peer_id = server_handshake["node_id"]
                        peer_pub_hex = server_handshake["public_key"]

                        # 2. Key Exchange (ECDH)
                        peer_pub_key = ec.EllipticCurvePublicKey.from_encoded_point(
                            ec.SECP256K1(), bytes.fromhex(peer_pub_hex)
                        )
                        shared_key = self.private_key.exchange(ec.ECDH(), peer_pub_key)
                        
                        # Derive symmetric AES-GCM key
                        digest = hashlib.sha256(shared_key).digest()
                        aesgcm = AESGCM(digest)

                        self.connections[peer_id] = (reader, writer, aesgcm)
                        logger.info(f"Node {self.node_id}: Successfully dialed and secured peer Node {peer_id}")
                        
                        # Read messages loop in background
                        msg_task = asyncio.create_task(self.handle_incoming_messages(reader, peer_id, digest, aesgcm))
                        self.tasks.append(msg_task)
                    except Exception as e:
                        logger.debug(f"Node {self.node_id}: Failed to dial peer {peer}: {e}")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    async def handle_incoming_messages(self, reader, peer_id, digest, aesgcm):
        try:
            while self.running:
                length_bytes = await reader.readexactly(4)
                length = struct.unpack("!I", length_bytes)[0]
                encrypted_data = await reader.readexactly(length)
                nonce = digest[:12]
                decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
                await self.process_message(decrypted_data.decode(), peer_id)
        except asyncio.IncompleteReadError:
            logger.debug(f"Node {self.node_id}: Connection to dialed peer Node {peer_id} closed.")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Node {self.node_id}: Error reading from peer Node {peer_id}: {e}")
        finally:
            self.connections.pop(peer_id, None)

    async def process_message(self, raw_msg: str, sender_id: str):
        try:
            msg = json.loads(raw_msg)
            msg_id = msg.get("msg_id")
            if not msg_id or msg_id in self.seen_messages:
                return
            self.seen_messages.add(msg_id)
            logger.info(f"Node {self.node_id}: Received message {msg_id} from Node {sender_id}")
            # Gossip/forward message to others
            await self.gossip(raw_msg, sender_id)
        except Exception as e:
            logger.error(f"Node {self.node_id}: Error processing message: {e}")

    async def gossip(self, raw_msg: str, exclude_id: str = None):
        logger.info(f"Node {self.node_id}: Gossiping message to peers. Connections: {list(self.connections.keys())}")
        for peer_id, (_, writer, aesgcm) in list(self.connections.items()):
            if peer_id == exclude_id:
                continue
            try:
                # Encrypt frame using key prefix as nonce (stateless)
                nonce = aesgcm._key[:12]
                encrypted_data = aesgcm.encrypt(nonce, raw_msg.encode(), None)
                
                # Write length-prefixed frame
                length_prefix = struct.pack("!I", len(encrypted_data))
                writer.write(length_prefix + encrypted_data)
                await writer.drain()
                logger.info(f"Node {self.node_id}: Sent gossiped message to Node {peer_id}")
            except Exception as e:
                logger.error(f"Node {self.node_id}: Failed to gossip to Node {peer_id}: {e}")
                self.connections.pop(peer_id, None)

    async def broadcast(self, payload: dict):
        msg_id = hashlib.sha256(json.dumps(payload).encode()).hexdigest()
        msg = {"msg_id": msg_id, "payload": payload}
        raw_msg = json.dumps(msg)
        self.seen_messages.add(msg_id)
        logger.info(f"Node {self.node_id}: Broadcasting message {msg_id}")
        await self.gossip(raw_msg)
