#!/usr/bin/env python3
"""
semantic_search_cache.py — P1: FTS5 + embedding search over session history.

Combines SQLite FTS5 (full-text keyword search) with LanceDB-like vector
embedding similarity (semantic search). Sessions are indexed on save and
retrievable via either search method or a merged ranking.

Mirrors the Magix.Session.Search Elixir module pattern.
"""

import json
import hashlib
import sqlite3
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class SemanticSearchCache:
    """Dual-index session search: FTS5 full-text + embedding similarity.

    Usage:
        sc = SemanticSearchCache()
        sc.index_session("session_1", [{"role": "user", "content": "hello"}])
        results = sc.search("hello")  # returns merged FTS + semantic results
    """

    def __init__(self, db_path: str = "/tmp/odysseus_search.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    # ── Public API ──────────────────────────────────────────────

    def index_session(self, session_id: str, messages: List[Dict[str, str]],
                      metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Index a session for both FTS5 and semantic retrieval."""
        content = self._serialize_messages(messages)
        embedding = json.dumps(self._compute_embedding(content))
        summary = self._summarize(messages)

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (id, content, summary, embedding, message_count, timestamp, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, content, summary, json.dumps(embedding),
            len(messages), int(time.time()),
            hashlib.sha256(content.encode()).hexdigest()[:16]
        ))
        self.conn.commit()
        return {"indexed": session_id, "messages": len(messages), "embedding_dim": len(embedding)}

    def search(self, query: str, limit: int = 10, min_score: float = 0.1) -> List[Dict[str, Any]]:
        """Search sessions — FTS5 first, then semantic, then merge ranked."""
        query_embedding = self._compute_embedding(query)
        fts_results = self._fts_search(query, limit * 2)
        semantic_results = self._semantic_search(query_embedding, limit * 2) if query_embedding else []
        merged = self._merge_ranked(fts_results, semantic_results, query_embedding, limit)
        return merged[:limit]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def delete_session(self, session_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def stats(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM sessions")
        count = cursor.fetchone()["count"]
        cursor.execute("SELECT SUM(message_count) as total FROM sessions")
        msgs = cursor.fetchone()["total"] or 0
        return {"sessions": count, "total_messages": msgs}

    # ── FTS5 full-text search ───────────────────────────────────

    def _fts_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT s.id, s.content, s.summary, s.message_count, s.timestamp,
                       rank AS score
                FROM sessions_fts f
                JOIN sessions s ON s.rowid = f.rowid
                WHERE sessions_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            # Invalid FTS query (special chars, etc.)
            return []

    # ── Semantic similarity search ──────────────────────────────

    def _semantic_search(self, query_emb: List[float], limit: int) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, content, summary, message_count, timestamp, embedding FROM sessions WHERE embedding IS NOT NULL")
        results = []
        for row in cursor.fetchall():
            stored_emb = json.loads(row["embedding"])
            sim = self._cosine_similarity(query_emb, stored_emb)
            results.append({
                "id": row["id"],
                "content": row["content"],
                "summary": row["summary"],
                "message_count": row["message_count"],
                "timestamp": row["timestamp"],
                "similarity": sim,
            })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]

    # ── Merge & rank ────────────────────────────────────────────

    def _merge_ranked(self, fts_results: List[Dict], semantic_results: List[Dict],
                      query_emb: List[float], limit: int) -> List[Dict[str, Any]]:
        seen: Dict[str, Dict[str, Any]] = {}

        for r in fts_results:
            seen[r["id"]] = {**r, "_score": 1.0 + (1.0 / (1.0 + abs(r.get("score", 0))))}

        for r in semantic_results:
            sid = r["id"]
            boost = r.get("similarity", 0)
            if sid in seen:
                seen[sid]["_score"] = seen[sid]["_score"] * 0.5 + boost * 0.5
                seen[sid]["similarity"] = boost
            else:
                seen[sid] = {**r, "_score": boost}

        results = sorted(seen.values(), key=lambda x: x["_score"], reverse=True)
        return results[:limit]

    # ── Embedding computation ───────────────────────────────────

    def _compute_embedding(self, text: str) -> List[float]:
        """Character-n-gram frequency embedding (384-dim).

        In production, replace with a real embedding model (all-MiniLM-L6-v2, etc.).
        This is a deterministic, content-addressed fallback that preserves
        enough signal for basic semantic matching.
        """
        dim = 384
        vec = [0.0] * dim
        text = text.lower()
        # 2-gram and 3-gram frequencies as pseudo-embedding
        for n in (2, 3):
            for i in range(len(text) - n + 1):
                gram = text[i:i + n]
                idx = int(hashlib.md5(gram.encode()).hexdigest()[:8], 16) % dim
                vec[idx] += 1.0
        # Normalize
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        if na * nb == 0:
            return 0.0
        return dot / (na * nb)

    # ── Helpers ─────────────────────────────────────────────────

    def _init_db(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                content TEXT,
                summary TEXT DEFAULT '',
                embedding TEXT,
                message_count INTEGER DEFAULT 0,
                timestamp INTEGER,
                hash TEXT
            )
        """)
        # FTS5 virtual table
        try:
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts
                USING fts5(content, tokenize='porter unicode61')
            """)
        except sqlite3.OperationalError:
            pass  # Already exists
        # Triggers for FTS sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS sessions_ai AFTER INSERT ON sessions
            BEGIN
                INSERT INTO sessions_fts(rowid, content) VALUES (new.rowid, new.content);
            END
        """)
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS sessions_ad AFTER DELETE ON sessions
            BEGIN
                INSERT INTO sessions_fts(sessions_fts, rowid, content) VALUES ('delete', old.rowid, old.content);
            END
        """)
        self.conn.commit()

    def _serialize_messages(self, messages: List[Dict[str, str]]) -> str:
        return "\n".join(m.get("content", "") for m in messages if m.get("content"))

    def _summarize(self, messages: List[Dict[str, str]]) -> str:
        """Simple extractive summary — first user message + last exchange."""
        parts = []
        for m in messages[:3]:
            parts.append(f"[{m.get('role', 'unknown')}] {m.get('content', '')[:120]}")
        if len(messages) > 3:
            parts.append(f"... ({len(messages) - 3} more messages)")
        return " | ".join(parts)


# ── CLI Demo ────────────────────────────────────────────────────

def main():
    import sys, os
    sc = SemanticSearchCache()

    action = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if action == "demo":
        # Index some demo sessions
        sessions = [
            ("session_001", [
                {"role": "user", "content": "How do I deploy the ICP canister?"},
                {"role": "assistant", "content": "Use dfx deploy --network ic"}
            ]),
            ("session_002", [
                {"role": "user", "content": "What's the cycle balance?"},
                {"role": "assistant", "content": "933 billion cycles remaining"}
            ]),
            ("session_003", [
                {"role": "user", "content": "How do I top up cycles?"},
                {"role": "assistant", "content": "Use dfx ledger top-up --amount 0.38 <canister_id>"}
            ]),
        ]
        for sid, msgs in sessions:
            r = sc.index_session(sid, msgs)
            print(f"Indexed: {sid} ({r['messages']} messages, {r['embedding_dim']}d)")

        print("\n--- Search: 'deploy canister' ---")
        for r in sc.search("deploy canister"):
            print(f"  [{r['id']}] score={r['_score']:.2f} sim={r.get('similarity', 0):.2f}: {r.get('summary', '')[:80]}")

        print("\n--- Search: 'cycle balance' ---")
        for r in sc.search("cycle balance"):
            print(f"  [{r['id']}] score={r['_score']:.2f} sim={r.get('similarity', 0):.2f}: {r.get('summary', '')[:80]}")

        print(f"\nStats: {json.dumps(sc.stats(), indent=2)}")

    elif action == "index":
        data = json.loads(sys.stdin.read())
        print(json.dumps(sc.index_session(data["id"], data["messages"])))

    elif action == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else "hello"
        print(json.dumps(sc.search(query), default=str, indent=2))

    elif action == "stats":
        print(json.dumps(sc.stats(), indent=2))

    else:
        print(f"Usage: {sys.argv[0]} [demo|index|search|stats]")


if __name__ == "__main__":
    main()
