import sqlite3
import uuid
import time
from typing import Optional, Tuple

class BillingDB:
    def __init__(self, db_path: str = "gateway/billing.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at INTEGER NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    key TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at INTEGER NOT NULL,
                    last_used_at INTEGER,
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS balances (
                    customer_id TEXT PRIMARY KEY,
                    credits REAL DEFAULT 0.0,
                    updated_at INTEGER NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT NOT NULL,
                    request_id TEXT UNIQUE NOT NULL,
                    tokens_used INTEGER NOT NULL,
                    cost REAL NOT NULL,
                    timestamp INTEGER NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def create_customer(self, name: str, email: str) -> Tuple[str, str]:
        customer_id = str(uuid.uuid4())
        api_key = str(uuid.uuid4()).replace("-", "")
        now = int(time.time())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO customers (id, name, email, created_at) VALUES (?, ?, ?, ?)",
                (customer_id, name, email, now)
            )
            conn.execute(
                "INSERT INTO api_keys (key, customer_id, name, created_at) VALUES (?, ?, ?, ?)",
                (api_key, customer_id, "default", now)
            )
            conn.execute(
                "INSERT INTO balances (customer_id, credits, updated_at) VALUES (?, 0.0, ?)",
                (customer_id, now)
            )
            conn.commit()
        return customer_id, api_key

    def check_balance(self, customer_id: str) -> float:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT credits FROM balances WHERE customer_id = ?", (customer_id,))
            row = cur.fetchone()
            return row[0] if row else 0.0

    def get_customer_by_key(self, api_key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT customer_id FROM api_keys WHERE key = ? AND is_active = 1",
                (api_key,)
            )
            row = cur.fetchone()
            return row[0] if row else None

    def grant_credits(self, customer_id: str, amount: float):
        now = int(time.time())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE balances SET credits = credits + ?, updated_at = ? WHERE customer_id = ?",
                (amount, now, customer_id)
            )
            conn.commit()

    def deduct_usage(self, customer_id: str, request_id: str, tokens: int, cost: float) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            # Check balance
            balance = self.check_balance(customer_id)
            if balance < cost:
                return False
            # Deduct
            conn.execute(
                "UPDATE balances SET credits = credits - ?, updated_at = ? WHERE customer_id = ?",
                (cost, int(time.time()), customer_id)
            )
            # Log usage
            conn.execute(
                "INSERT INTO usage_logs (customer_id, request_id, tokens_used, cost, timestamp) VALUES (?, ?, ?, ?, ?)",
                (customer_id, request_id, tokens, cost, int(time.time()))
            )
            conn.commit()
            return True

    def close(self):
        pass
