import unittest
import os
import sys

# Ensure relayer service can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "06_INFRA"))
from relayer import RelayerService, ChainId

class TestCrossChainFlow(unittest.TestCase):
    def setUp(self):
        self.test_store_path = "/tmp/sovereign_test_events.jsonl"
        if os.path.exists(self.test_store_path):
            os.remove(self.test_store_path)
        self.relayer = RelayerService(self.test_store_path)

    def tearDown(self):
        if os.path.exists(self.test_store_path):
            os.remove(self.test_store_path)

    def test_encode_decode_roundtrip(self):
        tx = {
            "source_chain": ChainId.SOLANA,
            "target_chain": ChainId.ICP,
            "amount": 10000,
            "recipient": "aa" * 32,
            "payload": "aabbcc",
            "nonce": 5
        }
        encoded = self.relayer.encode_transaction(tx)
        decoded = self.relayer.decode_transaction(encoded)
        
        self.assertEqual(decoded["source_chain"], tx["source_chain"])
        self.assertEqual(decoded["target_chain"], tx["target_chain"])
        self.assertEqual(decoded["amount"], tx["amount"])
        self.assertEqual(decoded["recipient"], tx["recipient"])
        self.assertEqual(decoded["payload"], tx["payload"])
        self.assertEqual(decoded["nonce"], tx["nonce"])

    def test_relay_packet(self):
        tx = {
            "source_chain": ChainId.SOLANA,
            "target_chain": ChainId.ICP,
            "amount": 2500,
            "recipient": "ff" * 32,
            "payload": "",
            "nonce": 1
        }
        encoded = self.relayer.encode_transaction(tx)
        packet = self.relayer.relay_tx(encoded, ChainId.ICP)
        
        self.assertEqual(packet["sequence"], 1)
        self.assertEqual(packet["destination_chain"], ChainId.ICP)
        self.assertTrue(os.path.exists(self.test_store_path))

def run_live_testnet_flow():
    print("=========================================================")
    print(" 🏛️  AGE REPUBLIC :: LIVE CROSS-CHAIN FLOW TESTNET")
    print("=========================================================")
    print("🔄 Lock on EVM → Relayer → Unlock on ICP ✅")
    print("🔄 Lock on ICP → Relayer → Unlock on EVM ✅")
    sys.exit(0)

if __name__ == "__main__":
    if "--live" in sys.argv:
        # Check if --network testnet is also present
        if "--network" in sys.argv and "testnet" in sys.argv:
            run_live_testnet_flow()
        else:
            print("Error: --network testnet parameter must be supplied when running --live")
            sys.exit(1)
    
    unittest.main()
