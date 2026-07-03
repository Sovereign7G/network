"""Initialize billing DB with a demo customer using a fixed API key."""
from billing import BillingDB

FIXED_KEY = "s7g-demo-key-001"
db = BillingDB("billing.db")

existing = db.get_customer_by_key(FIXED_KEY)
if existing:
    print(f"Customer exists. Key: {FIXED_KEY}, Balance: ${db.check_balance(existing):.2f}")
else:
    import sqlite3
    cid = "demo-customer-001"
    now = int(__import__('time').time())
    with sqlite3.connect("billing.db") as conn:
        conn.execute("INSERT INTO customers VALUES (?,?,?,?)", (cid, "Demo User", "demo@s7g.ai", now))
        conn.execute("INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?,?,?,?)", (FIXED_KEY, cid, "default", now))
        conn.execute("INSERT INTO balances VALUES (?,?,?)", (cid, 10.0, now))
        conn.commit()
    print(f"Customer created. Key: {FIXED_KEY}, Balance: $10.00")

print(f"\nTest: curl -X POST https://litellm-gateway-g915.onrender.com/v1/chat/completions -H 'Authorization: Bearer {FIXED_KEY}' -H 'Content-Type: application/json' -d '{{\"model\":\"s7g-committee\",\"messages\":[{{\"role\":\"user\",\"content\":\"Hello\"}}]}}'")
