# gateway/billing.py
import sqlite3, uuid, time
from typing import Optional, List, Tuple

class BillingDB:
    def __init__(self, db_path: str = "billing.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)")
            conn.execute("INSERT OR IGNORE INTO schema_version (version) VALUES (1)")
            conn.execute("""CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, created_at INTEGER NOT NULL)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS api_keys (
                key TEXT PRIMARY KEY, customer_id TEXT NOT NULL, name TEXT NOT NULL,
                is_active INTEGER DEFAULT 1, created_at INTEGER NOT NULL, last_used_at INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id))""")
            conn.execute("""CREATE TABLE IF NOT EXISTS balances (
                customer_id TEXT PRIMARY KEY, credits REAL DEFAULT 0, updated_at INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id))""")
            conn.execute("""CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT NOT NULL,
                request_id TEXT NOT NULL, tokens_used INTEGER NOT NULL, cost REAL NOT NULL,
                timestamp INTEGER NOT NULL, FOREIGN KEY (customer_id) REFERENCES customers(id))""")
            conn.execute("""CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, amount REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending', created_at INTEGER NOT NULL,
                due_date INTEGER NOT NULL, FOREIGN KEY (customer_id) REFERENCES customers(id))""")
            conn.commit()

    def create_customer(self, name: str, email: str) -> Tuple[str, str]:
        cid = str(uuid.uuid4()); key = str(uuid.uuid4()).replace("-", ""); now = int(time.time())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO customers VALUES (?,?,?,?)", (cid, name, email, now))
            conn.execute("INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?,?,?,?)", (key, cid, "default", now))
            conn.execute("INSERT INTO balances VALUES (?,?,?)", (cid, 0, now))
            conn.commit()
        return cid, key

    def get_customer_by_key(self, api_key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT customer_id FROM api_keys WHERE key=? AND is_active=1", (api_key,)).fetchone()
            return r[0] if r else None

    def check_balance(self, customer_id: str) -> float:
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT credits FROM balances WHERE customer_id=?", (customer_id,)).fetchone()
            return r[0] if r else 0.0

    def grant_credits(self, customer_id: str, amount: float):
        now = int(time.time())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE balances SET credits = credits + ?, updated_at = ? WHERE customer_id = ?",
                (amount, now, customer_id)
            )
            conn.commit()

    def add_credits(self, customer_id: str, amount: float):
        self.grant_credits(customer_id, amount); return True

    def deduct_usage(self, customer_id: str, rid: str, tokens: int, cost: float) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            bal = conn.execute("SELECT credits FROM balances WHERE customer_id=?", (customer_id,)).fetchone()
            if not bal or bal[0] < cost: return False
            conn.execute("UPDATE balances SET credits=credits-?, updated_at=? WHERE customer_id=?", (cost, int(time.time()), customer_id))
            conn.execute("INSERT INTO usage_logs (customer_id, request_id, tokens_used, cost, timestamp) VALUES (?,?,?,?,?)", (customer_id, rid, tokens, cost, int(time.time())))
            conn.commit(); return True

    def get_usage(self, customer_id: str, limit: int = 100) -> List[Tuple]:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT request_id, tokens_used, cost, timestamp FROM usage_logs WHERE customer_id=? ORDER BY timestamp DESC LIMIT ?", (customer_id, limit)).fetchall()

    def create_invoice(self, customer_id: str, amount: float, due_days: int = 30) -> str:
        iid = str(uuid.uuid4()); now = int(time.time())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO invoices VALUES (?,?,?,?,?,?)", (iid, customer_id, amount, 'pending', now, now + due_days * 86400))
            conn.commit(); return iid

    def get_invoices(self, customer_id: str) -> List[Tuple]:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT id, amount, status, created_at, due_date FROM invoices WHERE customer_id=? ORDER BY created_at DESC", (customer_id,)).fetchall()
