# networking/toon_serializer.py - STREAMLINED
import base64
import json
import base64
import json
import zlib
import struct
import binascii
from typing import Dict, Any, Optional
from enum import Enum, auto
import logging

logger = logging.getLogger("toon_serializer")
logging.basicConfig(level=logging.INFO)

class SerializationMode(Enum):
    SWISS_WATCH = auto()      # Zero-copy, compressed, strict
    DIRTY_TOLERANCE = auto()  # FEC padded, loose hydration
    POWER_TOOL = auto()       # Uncompressed, flat, redundant

class ControlBolt:
    WIDTH = 64  # bytes

    def __init__(self, intent: str, node_id: str, seq: int, crc: int = 0):
        self.intent = intent      # 16 bytes max
        self.node_id = node_id    # 32 bytes max
        self.seq = seq            # 8 bytes
        self.crc = crc            # 8 bytes (CRC64-like)
    
    def pack(self) -> bytes:
        # Pack into fixed 64-byte layout
        raw = struct.pack(
            "<16s32sQ",
            self.intent.encode('ascii')[:16].ljust(16, b'\x00'),
            self.node_id.encode('ascii')[:32].ljust(32, b'\x00'),
            self.seq
        )
        # Calculate checksum for the first 56 bytes
        if self.crc == 0:
            self.crc = binascii.crc32(raw) # Use CRC32 for now as mock for CRC64
        return raw + struct.pack("<Q", self.crc)
    
    @staticmethod
    def unpack(data: bytes) -> 'ControlBolt':
        if len(data) < ControlBolt.WIDTH:
            raise ValueError("Data too short for ControlBolt")
        intent_raw, node_id_raw, seq, crc = struct.unpack("<16s32sQQ", data[:64])
        return ControlBolt(
            intent_raw.decode('ascii').strip('\x00'),
            node_id_raw.decode('ascii').strip('\x00'),
            seq,
            crc
        )

class RobustTOONSerializer:
    """
    Production-hardened TOON serializer with simplified format inference
    """
    
    # V1: zlib + b64, V2: raw json + b64
    COMPRESSED_PREFIX = '1:'

    def __init__(self, compression_level: int = 6):
        self.compression_level = compression_level
        self.mode = SerializationMode.SWISS_WATCH
        self.stats = {
            'serializations': 0,
            'deserializations': 0,
            'compression_ratio': 0.0,
            'errors': 0,
            'fouling_events': 0
        }
    
    def set_mode(self, mode: SerializationMode):
        self.mode = mode
        logger.info(f"Serialization mode changed to {self.mode.name}")

    def degrade_on_condition(self, packet_loss: float, bit_corruption: float, latency_ms: float):
        if packet_loss > 0.50 or bit_corruption > 0.10 or latency_ms > 500:
            self.set_mode(SerializationMode.POWER_TOOL)
        elif packet_loss > 0.20 or bit_corruption > 0.03 or latency_ms > 200:
            self.set_mode(SerializationMode.DIRTY_TOLERANCE)
        else:
            self.set_mode(SerializationMode.SWISS_WATCH)
    
    def encode(self, data: Dict[str, Any], intent: Optional[str] = None, node_id: str = "unknown") -> str:
        """Encode data to an optimized format, optionally including a ControlBolt."""
        self.stats['serializations'] += 1
        
        # If in POWER_TOOL mode or an intent is specified, we use the Over-Tolerance layout
        if self.mode == SerializationMode.POWER_TOOL or intent:
            return self._encode_over_tolerance(data, intent, node_id)

        try:
            # Primary path: JSON + compression
            json_str = json.dumps(data, separators=(',', ':'))
            compressed = zlib.compress(json_str.encode('utf-8'), self.compression_level)
            encoded = base64.b64encode(compressed).decode('ascii')
            
            # Calculate compression ratio
            original_size = len(json_str.encode('utf-8'))
            compressed_size = len(compressed)
            self.stats['compression_ratio'] = compressed_size / max(original_size, 1)
            
            return self.COMPRESSED_PREFIX + encoded
            
        except (zlib.error, TypeError, ValueError) as e:
            # Fallback: JSON without compression
            logger.warning("TOON compression failed, falling back to JSON", error=str(e))
            try:
                json_str = json.dumps(data)
                encoded = base64.b64encode(json_str.encode('utf-8')).decode('ascii')
                return '2:' + encoded  # Use a different prefix for uncompressed
            except Exception as fallback_error:
                # Final fallback: Minimal safe encoding
                logger.error("JSON fallback failed, using safe encoding", error=str(fallback_error))
                self.stats['errors'] += 1
                return self._safe_encode(data)

    def _encode_over_tolerance(self, data: Dict[str, Any], intent: str, node_id: str) -> str:
        """Encodes with a ControlBolt for high reliability."""
        seq = data.get('seq', 0)
        bolt = ControlBolt(intent or "GENERIC", node_id, seq)
        bolt_bytes = bolt.pack()
        
        if self.mode == SerializationMode.POWER_TOOL:
            # Flat-text gas, no compression
            gas_str = "|".join([f"{k}={v}" for k, v in data.items()])
            gas_bytes = gas_str.encode('utf-8')
        else:
            # Standard gas
            gas_bytes = zlib.compress(json.dumps(data).encode('utf-8'))
            
        # Combine and base64 for transmission
        return "OT:" + base64.b64encode(bolt_bytes + gas_bytes).decode('ascii')
    
    def decode(self, toon_data: str) -> Dict[str, Any]:
        """Decode data with automatic format detection"""
        self.stats['deserializations'] += 1
        
        if not isinstance(toon_data, str):
            logger.error("Received non-string data for decoding", data_type=type(toon_data))
            return {"error": "Invalid input type"}
        
        try:
            # Explicitly check for a version prefix
            if ':' in toon_data:
                prefix, payload = toon_data.split(':', 1)
                if prefix == '1':
                    # V1: Compressed
                    decoded_bytes = base64.b64decode(payload)
                    decompressed = zlib.decompress(decoded_bytes)
                    return json.loads(decompressed.decode('utf-8'))
                elif prefix == '2':
                    # V2: Uncompressed
                    decoded_bytes = base64.b64decode(payload)
                    return json.loads(decoded_bytes.decode('utf-8'))
                elif prefix == 'OT':
                    # OT: Over-Tolerance (ControlBolt + Gas)
                    return self.loose_hydrate(base64.b64decode(payload))

            # Fallback for old format or direct JSON
            return self._auto_decode_legacy(toon_data)
                
        except Exception as e:
            logger.error("All decoding attempts failed", error=str(e))
            self.stats['errors'] += 1
            return {"error": "Failed to decode message", "original_data": toon_data[:100] + "..."}
    
    def _auto_decode_legacy(self, data: str) -> Dict[str, Any]:
        """Legacy auto-detection for unprefixed data."""
        # Attempt 1: Direct JSON parsing (most likely for un-encoded messages)
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            logger.debug("Legacy decode: Not direct JSON, attempting base64 decode.")

        # Attempt 2 & 3: Base64 decoding, then check for compression
        try:
            decoded_bytes = base64.b64decode(data)
            try:
                # Attempt 2: Compressed payload
                decompressed = zlib.decompress(decoded_bytes)
                return json.loads(decompressed.decode('utf-8'))
            except zlib.error:
                # Attempt 3: Uncompressed, base64-encoded JSON
                return json.loads(decoded_bytes.decode('utf-8'))
        except (base64.binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ValueError(f"Unable to auto-detect legacy encoding format: {e}")
    
    def loose_hydrate(self, mangled_bytes: bytes) -> Dict[str, Any]:
        """
        Attempts to extract the Control Bolt first.
        If the bolt is intact -> executable state.
        Telemetry gas is best-effort.
        """
        try:
            if len(mangled_bytes) < ControlBolt.WIDTH:
                return {"error": "packet_too_short"}
            
            bolt = ControlBolt.unpack(mangled_bytes[:ControlBolt.WIDTH])
            # Checksum verification
            expected_crc = binascii.crc32(mangled_bytes[:56])
            if bolt.crc != expected_crc:
                logger.warning(f"ControlBolt checksum failed (expected {expected_crc}, got {bolt.crc})")
                return {"status": "bolt_jammed", "error": "checksum_failure"}

            return {
                "status": "executable",
                "intent": bolt.intent,
                "node_id": bolt.node_id,
                "seq": bolt.seq,
                "gas": self._try_parse_gas(mangled_bytes[ControlBolt.WIDTH:]),
                "fouling_flag": False
            }
        except Exception as e:
            logger.error(f"Loose hydration failed: {e}")
            self.stats['fouling_events'] += 1
            return {"status": "bolt_jammed", "error": str(e)}

    def _try_parse_gas(self, gas_bytes: bytes) -> Dict[str, Any]:
        """Best-effort gas parsing. Failure never blocks intent execution."""
        if not gas_bytes:
            return {}
        
        # Try JSON (compressed or raw)
        try:
            # Try decompressing first
            try:
                data = zlib.decompress(gas_bytes)
                return json.loads(data.decode('utf-8'))
            except zlib.error:
                # Try raw JSON
                return json.loads(gas_bytes.decode('utf-8'))
        except Exception:
            # Try flat-text fallback (key=value|key2=value2)
            try:
                gas_str = gas_bytes.decode('utf-8')
                if '=' in gas_str:
                    return dict(item.split('=') for item in gas_str.split('|') if '=' in item)
            except Exception:
                pass
            
            logger.debug("Gas venting: payload corrupted")
            return {"status": "vented", "reason": "corruption"}

    def _safe_encode(self, data: Dict[str, Any]) -> str:
        """Safe encoding when all else fails"""
        try:
            # Create minimal safe representation
            safe_data = {
                'timestamp': data.get('timestamp'),
                'type': data.get('type', 'unknown'),
                'error': 'fallback_encoding_used'
            }
            return base64.b64encode(json.dumps(safe_data).encode('utf-8')).decode('ascii')
        except Exception:
            # Absolute last resort
            return base64.b64encode(b'{"error":"encoding_failed"}').decode('ascii')