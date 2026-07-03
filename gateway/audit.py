"""Audit DB — immutable queryable log with cryptographic proof."""
import sqlite3, json
from typing import Optional, List, Dict
from datetime import datetime

class AuditDB:
    def __init__(self, db_path: str = "audit.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT NOT NULL,
                customer_id TEXT NOT NULL, model TEXT NOT NULL, prompt TEXT,
                response TEXT, tokens_used INTEGER, cost REAL,
                signature TEXT, timestamp INTEGER NOT NULL, verified INTEGER DEFAULT 1)""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_customer_ts ON audit_log(customer_id, timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rid ON audit_log(request_id)")
            conn.commit()

    def log(self, rid: str, cid: str, model: str, prompt: str, resp: str,
            tokens: int, cost: float, sig: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO audit_log (request_id, customer_id, model, prompt, response, tokens_used, cost, signature, timestamp) VALUES (?,?,?,?,?,?,?,?,?)",
                         (rid, cid, model, prompt, resp, tokens, cost, sig, int(datetime.utcnow().timestamp())))
            conn.commit(); return True

    def query(self, cid: str = None, from_ts: int = None, to_ts: int = None, limit: int = 100) -> List[Dict]:
        q = "SELECT request_id, customer_id, model, prompt, response, tokens_used, cost, signature, timestamp, verified FROM audit_log WHERE 1=1"; p = []
        if cid: q += " AND customer_id=?"; p.append(cid)
        if from_ts: q += " AND timestamp>=?"; p.append(from_ts)
        if to_ts: q += " AND timestamp<=?"; p.append(to_ts)
        q += " ORDER BY timestamp DESC LIMIT ?"; p.append(limit)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            return [dict(r) for r in conn.execute(q, p).fetchall()]

    def report(self, cid: str, from_ts: int, to_ts: int) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT COUNT(*), COALESCE(SUM(tokens_used),0), COALESCE(SUM(cost),0) FROM audit_log WHERE customer_id=? AND timestamp BETWEEN ? AND ?", (cid, from_ts, to_ts)).fetchone()
            return {"customer_id": cid, "from": from_ts, "to": to_ts, "requests": r[0], "tokens": r[1], "cost": r[2]}

    def verify(self, rid: str, sig: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT 1 FROM audit_log WHERE request_id=? AND signature=?", (rid, sig)).fetchone() is not None

    def provenance(self, rid: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            r = conn.execute("SELECT * FROM audit_log WHERE request_id=?", (rid,)).fetchone()
            return dict(r) if r else None
