import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

class Ledger:
    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path / "ledger.db"
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(str(self.ledger_path))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                sequence INTEGER PRIMARY KEY,
                request_id TEXT UNIQUE NOT NULL,
                payload TEXT NOT NULL,
                response_summary TEXT,
                timestamp INTEGER NOT NULL,
                proposer_id INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def append(self, sequence: int, request_id: str, payload: dict, response_summary: dict, timestamp: int, proposer_id: int):
        self.cursor.execute("""
            INSERT INTO blocks (sequence, request_id, payload, response_summary, timestamp, proposer_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sequence, request_id, json.dumps(payload), json.dumps(response_summary), timestamp, proposer_id))
        self.conn.commit()

    def get_all(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM blocks ORDER BY sequence ASC")
        rows = self.cursor.fetchall()
        return [{
            "sequence": r["sequence"],
            "request_id": r["request_id"],
            "payload": json.loads(r["payload"]),
            "response_summary": json.loads(r["response_summary"]) if r["response_summary"] else {},
            "timestamp": r["timestamp"],
            "proposer_id": r["proposer_id"]
        } for r in rows]

    def count(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM blocks")
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()
