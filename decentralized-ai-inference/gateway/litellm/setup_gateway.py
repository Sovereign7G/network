"""
setup_gateway.py — Initialize the Sovereign AI Gateway.
Creates billing DB, adds a test customer, starts the server.
"""
from billing import BillingDB
import os

db = BillingDB("billing.db")
cid, key = db.create_customer("Demo User", "demo@s7g.ai")
db.add_credits(cid, 10.0)  # $10 free credits

print(f"Customer ID: {cid}")
print(f"API Key: {key}")
print(f"Balance: ${db.check_balance(cid):.2f}")
print(f"\nTest with:")
print(f"  curl -X POST http://localhost:1317/v1/chat/completions \\")
print(f"    -H 'Authorization: Bearer {key}' \\")
print(f"    -H 'Content-Type: application/json' \\")
print(f"    -d '{{\"model\":\"s7g-committee\",\"messages\":[{{\"role\":\"user\",\"content\":\"Hello\"}}]}}'")
