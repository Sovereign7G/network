import time
import struct
import binascii
from typing import Dict, Any, List, Optional
from .toon_serializer import RobustTOONSerializer, ControlBolt, SerializationMode

class DeduplicationAnvil:
    """The Anvil: Deduplicates redundant hammer blows (Thick Intents)."""
    def __init__(self, window_ms: int = 500):
        self.seen = {}  # (node_id, seq) -> timestamp
        self.window = window_ms / 1000.0
    
    def hammer(self, node_id: str, seq: int) -> bool:
        """Returns True if this is the first time seeing this sequence."""
        now = time.time()
        key = (node_id, seq)
        if key in self.seen and (now - self.seen[key]) < self.window:
            return False  # Already hammered through
        self.seen[key] = now
        # Cleanup old entries occasionally
        if len(self.seen) > 1000:
            self._cleanup()
        return True

    def _cleanup(self):
        now = time.time()
        self.seen = {k: v for k, v in self.seen.items() if (now - v) < self.window}

class SovereignMobileNode:
    """The Sovereign Mobile Node: Executes the Kalashnikov Contract."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.serializer = RobustTOONSerializer()
        self.anvil = DeduplicationAnvil()
        self._seq_counter = 0
        self.state = "IDLE"
        self.dedupe_count = 0

    def next_seq(self) -> int:
        self._seq_counter += 1
        return self._seq_counter

    def send_thick_intent(self, intent: str, gas_data: Dict[str, Any] = None):
        """The Long-Stroke Piston: blast redundant intents across the mesh."""
        seq = self.next_seq()
        gas_data = gas_data or {}
        gas_data['seq'] = seq
        
        # Pack the packet using the Over-Tolerance layout
        packet = self.serializer.encode(gas_data, intent=intent, node_id=self.node_id)
        
        print(f"🚀 [NODE:{self.node_id}] Firing Thick Intent: {intent} (seq:{seq})")
        
        # Simulate firing redundant pulses (The Piston)
        for i in range(5):
            # In real impl, this calls mesh.broadcast()
            # self.mesh.broadcast(packet, priority="HIGHEST")
            pass
            
        return seq

    def on_receive(self, raw_packet: str):
        """Receives and processes a packet, applying the Kalashnikov Contract."""
        decoded = self.serializer.decode(raw_packet)
        
        if decoded.get("status") == "bolt_jammed":
            print(f"⚠️ [NODE:{self.node_id}] Bolt jammed! Waiting for redundant pulse.")
            return False

        # If it's an executable intent
        if decoded.get("status") == "executable":
            intent = decoded["intent"]
            seq = decoded["seq"]
            sender = decoded["node_id"]
            
            # The Anvil: Deduplicate redundant blows
            if not self.anvil.hammer(sender, seq):
                # print(f"🔨 [NODE:{self.node_id}] DEDUPE: Already hammered seq {seq}")
                return False
            
            self.dedupe_count += 1
            print(f"✅ [NODE:{self.node_id}] CYCLED ACTION: {intent} from {sender}")
            self._execute_intent(intent, decoded.get("gas", {}))
            return True
        
        return False

    def _execute_intent(self, intent: str, gas: Dict[str, Any]):
        # State transition logic
        if intent.startswith("LOCK"):
            region = intent.split("|")[-1] if "|" in intent else "UNKNOWN"
            self.state = f"LOCKED_{region}"
        elif intent == "HALT":
            self.state = "HALTED"
        else:
            self.state = f"EXECUTED_{intent}"
