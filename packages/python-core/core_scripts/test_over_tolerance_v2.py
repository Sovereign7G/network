import random
import time
from .sovereign_node import SovereignMobileNode
from .toon_serializer import SerializationMode

def corrupt_payload(payload_str: str, rate: float) -> str:
    """Simulates bit/character corruption in the base64 payload."""
    prefix, body = payload_str.split(":", 1)
    arr = list(body)
    for i in range(len(arr)):
        if random.random() < rate:
            arr[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
    return f"{prefix}:{''.join(arr)}"

def test_thick_intent_70_percent_loss():
    """Simulation result: 5 attempts, 70% loss, still executes exactly once."""
    print("\n--- TEST: Thick Intent with 70% Mesh Loss ---")
    transmitter = SovereignMobileNode("STORM-BREAKER")
    receiver = SovereignMobileNode("NEVADA-NODE")
    
    intent = "LOCK|ALPHA"
    
    # Transmitter sends thick intent (5 redundant pulses)
    seq = transmitter.send_thick_intent(intent)
    
    # Simulate 70% packet loss across the 5 redundant pulses
    success_count = 0
    packet = transmitter.serializer.encode({"seq": seq}, intent=intent, node_id="STORM-BREAKER")
    
    for i in range(5):
        if random.random() > 0.70:
            print(f"  [Pulse {i+1}] ✅ Passed through mesh")
            if receiver.on_receive(packet):
                success_count += 1
        else:
            print(f"  [Pulse {i+1}] ❌ Lost in sandstorm")

    # Assertions
    print(f"  Final Receiver State: {receiver.state}")
    print(f"  Receiver Dedupe Count: {receiver.dedupe_count}")
    
    assert receiver.state == "LOCKED_ALPHA"
    assert receiver.dedupe_count == 1  # Exactly once!
    print("✅ TEST PASSED: Intent cycled through 70% loss exactly once.")

def test_loose_hydration_15_percent_bit_corruption():
    """Test: LOCK executes even if gas is corrupted (15% corruption)."""
    print("\n--- TEST: Loose Hydration with 15% Bit Corruption ---")
    transmitter = SovereignMobileNode("STORM-BREAKER")
    receiver = SovereignMobileNode("NEVADA-NODE")
    
    # Move to POWER_TOOL mode to ensure uncompressed gas (easier to see 'venting')
    transmitter.serializer.set_mode(SerializationMode.POWER_TOOL)
    receiver.serializer.set_mode(SerializationMode.POWER_TOOL)
    
    intent = "HALT"
    gas_data = {"telemetry": "0.99", "status": "nominal"}
    
    # Create the packet
    packet = transmitter.serializer.encode(gas_data, intent=intent, node_id="STORM-BREAKER")
    
    # Corrupt the packet (15% rate)
    # Note: If the Bolt is corrupted, it will fail (jam), but we send redundant pulses.
    # Here we test that if the GAS is corrupted but BOLT is intact, it executes.
    # To isolate, we'll manually corrupt the part AFTER the bolt in the base64.
    
    # Extract the payload bytes to corrupt only the gas part for this specific test
    import base64
    prefix, b64_body = packet.split(":", 1)
    raw_bytes = bytearray(base64.b64decode(b64_body))
    
    # Corrupt ONLY bytes 64+ (the gas)
    for i in range(64, len(raw_bytes)):
        if random.random() < 0.15:
            raw_bytes[i] ^= 0xFF
            
    mangled_packet = f"{prefix}:{base64.b64encode(raw_bytes).decode('ascii')}"
    
    print("  Processing mangled packet (15% gas corruption)...")
    success = receiver.on_receive(mangled_packet)
    
    # Assertions
    print(f"  Final Receiver State: {receiver.state}")
    assert success is True
    assert receiver.state == "HALTED"
    print("✅ TEST PASSED: Intent cycled despite corrupted gas.")

if __name__ == "__main__":
    test_thick_intent_70_percent_loss()
    test_loose_hydration_15_percent_bit_corruption()
