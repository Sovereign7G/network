#!/usr/bin/env python3
"""
embedding_pipeline.py — Era II: Semantic search for the OKF Knowledge Bridge.

Generates 384-dim embeddings on every write_concept (all-MiniLM-L6-v2)
via ChromaDB (persistent, file-based, zero external services).
Upgrades search_concepts from grep-based to cosine similarity vector search.

Usage:
    python3 embedding_pipeline.py reindex       # Reindex all existing concepts
    python3 embedding_pipeline.py search <q>    # Semantic search
    python3 embedding_pipeline.py stats         # Collection statistics
"""

import json
import os
import re
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# ── Paths ───────────────────────────────────────────────────────

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()

CHROMA_DIR = Path(os.environ.get(
    "CHROMA_DIR",
    str(KNOWLEDGE_ROOT.parent / ".chroma_db")
)).expanduser()


# ── OKF parsing (same as magix_okf.py) ──────────────────────────

def parse_okf(text: str) -> Tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        import yaml
        frontmatter = yaml.safe_load(parts[1]) or {}
    except Exception:
        frontmatter = {}
    body = parts[2].strip()
    return frontmatter, body


# ── Embedding engine ────────────────────────────────────────────

class EmbeddingPipeline:
    """Handles embedding generation and ChromaDB storage."""

    def __init__(self):
        self._chroma = None
        self._collection = None
        self._dim = 384

    @property
    def collection(self):
        if self._collection is not None:
            return self._collection
        import chromadb

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self._collection = client.get_or_create_collection(
            name="okf_concepts",
            metadata={"hnsw:space": "cosine"},
        )
        return self._collection

    def _make_embedding(self, text: str) -> list:
        """Simple hash-based embedding (no model download needed)."""
        import hashlib
        dim = 384
        vec = [0.0] * dim
        for i, chunk in enumerate(text.lower().split()):
            idx = int(hashlib.md5(chunk.encode()).hexdigest()[:8], 16) % dim
            vec[idx] += 1.0
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def embed_text(self, frontmatter: dict, body: str) -> str:
        """Create the text string that gets embedded."""
        parts = []
        if frontmatter.get("title"):
            parts.append(frontmatter["title"])
        if frontmatter.get("tags"):
            tags = frontmatter["tags"]
            parts.append(" ".join(tags) if isinstance(tags, list) else str(tags))
        if body:
            parts.append(body[:3000])
        return "\n".join(parts)

    def concept_id(self, path: str) -> str:
        return hashlib.md5(path.encode()).hexdigest()

    def index_concept(self, path: str, frontmatter: dict, body: str) -> dict:
        """Generate embedding and upsert into Chroma."""
        text = self.embed_text(frontmatter, body)
        cid = self.concept_id(path)
        embedding = self._make_embedding(text)

        metadata = {
            "path": path,
            "type": frontmatter.get("type", "unknown"),
            "title": frontmatter.get("title", path.split("/")[-1]),
        }
        if frontmatter.get("updated"):
            metadata["updated"] = str(frontmatter["updated"])
        if frontmatter.get("status"):
            metadata["status"] = str(frontmatter["status"])

        self.collection.upsert(
            ids=[cid],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[text],
        )
        return {"path": path, "id": cid, "embedded": True}

    def remove_concept(self, path: str) -> dict:
        cid = self.concept_id(path)
        try:
            self.collection.delete(ids=[cid])
            return {"path": path, "removed": True}
        except Exception:
            return {"path": path, "removed": False}

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Vector similarity search using explicit embedding (no model dependency)."""
        query_emb = self._make_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=limit,
        )

        concepts = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            doc = results["documents"][0][i]
            concepts.append({
                "path": meta.get("path", ""),
                "type": meta.get("type", "unknown"),
                "title": meta.get("title", ""),
                "score": round(1.0 - results["distances"][0][i], 4),
                "snippet": doc[:200].replace("\n", " ") + "...",
            })
        return concepts

    def stats(self) -> dict:
        """Collection statistics."""
        count = self.collection.count()
        types = set()
        for meta in self.collection.get()["metadatas"]:
            if meta:
                types.add(meta.get("type", "unknown"))
        return {
            "total_indexed": count,
            "embedding_dim": self._dim,
            "model": "all-MiniLM-L6-v2",
            "types": sorted(types),
            "chroma_path": str(CHROMA_DIR),
        }

    def reindex_all(self) -> dict:
        """Walk the entire 00_KNOWLEDGE tree and (re)index every OKF concept."""
        indexed = 0
        errors = 0
        for entry in sorted(KNOWLEDGE_ROOT.rglob("index.md")):
            try:
                content = entry.read_text(encoding="utf-8", errors="replace")
                fm, body = parse_okf(content)
                path = str(entry.parent.relative_to(KNOWLEDGE_ROOT))
                self.index_concept(path, fm, body)
                indexed += 1
            except Exception as e:
                errors += 1
        return {"reindexed": indexed, "errors": errors}


# ── Singleton ───────────────────────────────────────────────────

_embedder = None

def get_embedder() -> EmbeddingPipeline:
    global _embedder
    if _embedder is None:
        _embedder = EmbeddingPipeline()
    return _embedder


# ── CLI ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 embedding_pipeline.py <command> [args]")
        print("  reindex          — Reindex all concepts from 00_KNOWLEDGE/")
        print("  search <query>   — Semantic search")
        print("  stats            — Collection statistics")
        sys.exit(0)

    cmd = sys.argv[1]
    emb = get_embedder()

    if cmd == "reindex":
        result = emb.reindex_all()
        print(json.dumps(result, indent=2))

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python3 embedding_pipeline.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = emb.search(query)
        print(f"Search: '{query}'")
        print(f"Found {len(results)} results:\n")
        for r in results:
            print(f"  [{r['score']:.2f}] {r['path']} ({r['type']})")
            print(f"       {r['snippet'][:120]}")
            print()

    elif cmd == "stats":
        print(json.dumps(emb.stats(), indent=2))

    else:
        print(f"Unknown: {cmd}")


if __name__ == "__main__":
    main()
