"""Agent registry — stores A2A agent cards in SQLite."""
import sqlite3, json, time, uuid
from typing import List, Optional, Dict, Any
from agent_cards import AgentCard, AgentCapability

class AgentRegistry:
    def __init__(self, db_path: str = "agent_registry.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL,
                version TEXT, did TEXT, endpoint TEXT NOT NULL, capabilities TEXT,
                price_per_call REAL, price_per_token REAL, owner TEXT NOT NULL,
                created_at INTEGER, is_active INTEGER DEFAULT 1, tags TEXT)""")
            conn.commit()

    def register(self, card: AgentCard) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""INSERT INTO agents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (card.id, card.name, card.description, card.version, card.did, card.endpoint,
                 json.dumps([c.model_dump() for c in card.capabilities]),
                 card.price_per_call, card.price_per_token, card.owner,
                 int(time.time()), 1, json.dumps(card.tags)))
            conn.commit()
        return card.id

    def get(self, agent_id: str) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT * FROM agents WHERE id=?", (agent_id,)).fetchone()
            if not r: return None
            cols = [d[0] for d in conn.execute("PRAGMA table_info(agents)")]
            return dict(zip(cols, r))

    def list_active(self, tag: str = None, limit: int = 50) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            if tag:
                rows = conn.execute("SELECT * FROM agents WHERE is_active=1 AND tags LIKE ? LIMIT ?",
                    (f"%{tag}%", limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM agents WHERE is_active=1 LIMIT ?", (limit,)).fetchall()
            cols = [d[0] for d in conn.execute("PRAGMA table_info(agents)")]
            return [dict(zip(cols, r)) for r in rows]

    def deactivate(self, agent_id: str, owner: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.execute("UPDATE agents SET is_active=0 WHERE id=? AND owner=?", (agent_id, owner))
            conn.commit()
            return c.rowcount > 0
