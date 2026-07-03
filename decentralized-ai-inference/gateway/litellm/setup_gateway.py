"""Initialize billing DB with a demo customer using a fixed API key."""
from billing import BillingDB

db = BillingDB("billing.db")
key = "s7g-demo-key-001"

# Check if demo customer already exists
existing = db.get_customer_by_key(key)
if existing:
    cid = existing
    print(f"Demo customer already exists. ID: {cid}")
else:
    cid, key = db.create_customer("Demo User", "demo@s7g.ai")
    # Overwrite with deterministic key
    import sqlite3
    with sqlite3.connect("billing.db") as conn:
        conn.execute("DELETE FROM api_keys WHERE customer_id=?", (cid,))
        conn.execute("INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?,?,?,?)",
                     (key, cid, "default", int(__import__('time').time())))
        conn.commit()
    db.add_credits(cid, 10.0)
    print(f"Customer ID: {cid}")
    print(f"API Key: {key}")

print(f"Balance: ${db.check_balance(cid):.2f}")
print(f"\nTest with:")
print(f"  curl -X POST https://litellm-gateway-g915.onrender.com/v1/chat/completions \\")
print(f"    -H 'Authorization: Bearer *** \\")
print(f"    -H 'Content-Type: application/json' \\")
print(f"    -d '{{\"model\":\"s7g-committee\",\"messages\":[{{\"role\":\"user\",\"content\":\"Hello\"}}]}}'")
