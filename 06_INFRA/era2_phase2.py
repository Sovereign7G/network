#!/usr/bin/env python3
"""
era2_phase2.py — Era II, Phase 2: Knowledge Graph + Recommendations + Reasoning.

Four components:
  1. OKFKnowledgeGraph — builds relationship graph from embedding similarity
  2. OKFRecommender — "You might also like..." for concepts and queries
  3. Semantic Dashboard data — /api/graph endpoint for visualizer
  4. OKFReasoningEngine — multi-concept synthesis, writes back to OKF

Usage:
    python3 era2_phase2.py graph          # Build graph, show stats
    python3 era2_phase2.py neighbors <path>  # Show related concepts
    python3 era2_phase2.py recommend <path>  # Recommendations
    python3 era2_phase2.py synthesize <path> # Multi-concept reasoning
    python3 era2_phase2.py api/graph        # JSON for dashboard
"""

import json
import os
import sys
import time
import hashlib
import math
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# ── Paths ───────────────────────────────────────────────────────

_EP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _EP_DIR)

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()


# ── Lazy import of embedding pipeline ───────────────────────────

_EMB = None
def _get_emb():
    global _EMB
    if _EMB is None:
        try:
            from embedding_pipeline import get_embedder
            _EMB = get_embedder()
        except Exception:
            pass
    return _EMB


def _get_all_embeddings():
    """Get all concept embeddings + metadata from Chroma."""
    emb = _get_emb()
    if not emb:
        return [], [], []
    all_data = emb.collection.get(include=["embeddings", "metadatas", "documents"])
    return all_data["ids"], all_data["embeddings"], all_data["metadatas"], all_data["documents"]


def _cosine_sim(a, b):
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na * nb == 0:
        return 0.0
    return dot / (na * nb)


# ── 1. Knowledge Graph ──────────────────────────────────────────

class OKFKnowledgeGraph:
    """Builds and queries the concept relationship graph.

    Edges connect concepts with cosine similarity >= threshold.
    Graph is rebuilt on demand (embedding changes are rare).
    """

    def __init__(self, threshold: float = 0.15):
        self.threshold = threshold
        self._graph: Dict[str, List[Tuple[str, float, dict]]] = {}  # id -> [(neighbor_id, similarity, metadata)]
        self._nodes: Dict[str, dict] = {}
        self._built = False

    def build(self, force: bool = False):
        if self._built and not force:
            return
        ids, embeddings, metadatas, docs = _get_all_embeddings()
        self._graph = {}
        self._nodes = {}

        if not ids:
            self._built = True
            return

        # Add nodes
        for i, cid in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            self._nodes[cid] = {
                "path": meta.get("path", ""),
                "type": meta.get("type", "unknown"),
                "title": meta.get("title", cid),
            }

        # Compute edges
        for i in range(len(ids)):
            neighbors = []
            for j in range(len(ids)):
                if i == j:
                    continue
                sim = _cosine_sim(embeddings[i], embeddings[j])
                if sim >= self.threshold:
                    meta_j = metadatas[j] if j < len(metadatas) else {}
                    neighbors.append((ids[j], round(sim, 4), {
                        "path": meta_j.get("path", ""),
                        "type": meta_j.get("type", "unknown"),
                        "title": meta_j.get("title", ids[j]),
                    }))
            neighbors.sort(key=lambda x: x[1], reverse=True)
            self._graph[ids[i]] = neighbors

        self._built = True

    def stats(self) -> dict:
        self.build()
        total_edges = sum(len(neighbors) for neighbors in self._graph.values())
        return {
            "nodes": len(self._nodes),
            "edges": total_edges // 2,  # Undirected: each edge counted twice
            "threshold": self.threshold,
            "avg_degree": round(total_edges / max(len(self._nodes), 1), 2),
            "types": self._type_distribution(),
        }

    def _type_distribution(self) -> dict:
        counts = {}
        for nid, node in self._nodes.items():
            t = node.get("type", "unknown")
            counts[t] = counts.get(t, 0) + 1
        return counts

    def neighbors(self, concept_path: str, limit: int = 10) -> list:
        """Get neighbors for a concept by path."""
        self.build()
        # Find matching node ID
        cid = self._path_to_id(concept_path)
        if not cid:
            return []
        neighbors = self._graph.get(cid, [])
        results = []
        for nid, sim, meta in neighbors[:limit]:
            results.append({
                "path": meta.get("path", ""),
                "type": meta.get("type", ""),
                "title": meta.get("title", nid),
                "similarity": sim,
            })
        return results

    def _path_to_id(self, path: str) -> Optional[str]:
        for cid, node in self._nodes.items():
            if node.get("path") == path:
                return cid
        return None

    def to_graph_data(self) -> dict:
        """Return graph data suitable for dashboard visualization."""
        self.build()
        nodes = []
        edges = []
        cid_to_idx = {}

        for idx, (cid, node) in enumerate(self._nodes.items()):
            cid_to_idx[cid] = idx
            nodes.append({
                "id": idx,
                "path": node.get("path", ""),
                "type": node.get("type", "unknown"),
                "title": node.get("title", cid),
            })

        seen = set()
        for cid, neighbors in self._graph.items():
            for nid, sim, meta in neighbors:
                edge = tuple(sorted([cid, nid]))
                if edge not in seen:
                    seen.add(edge)
                    edges.append({
                        "source": cid_to_idx[cid],
                        "target": cid_to_idx[nid],
                        "weight": sim,
                    })

        return {"nodes": nodes, "edges": edges}


# ── 2. Recommendations ──────────────────────────────────────────

class OKFRecommender:
    """'You might also like...' based on graph + embedding similarity."""

    def __init__(self):
        self.graph = OKFKnowledgeGraph()

    def for_concept(self, path: str, limit: int = 5) -> list:
        """Recommend concepts related to a given concept."""
        return self.graph.neighbors(path, limit)

    def for_query(self, query: str, limit: int = 5) -> list:
        """Recommend concepts based on a free-text query."""
        emb = _get_emb()
        if not emb:
            return []
        results = emb.search(query, limit=5)
        seen = set()
        recs = []
        for r in results:
            path = r.get("path", "")
            if not path or path in seen:
                continue
            seen.add(path)
            neighbors = self.graph.neighbors(path, limit=3)
            for n in neighbors:
                if n["path"] not in seen:
                    recs.append(n)
                    seen.add(n["path"])
        return recs[:limit]


# ── 3. Reasoning Engine ─────────────────────────────────────────

class OKFReasoningEngine:
    """Reads a concept and its neighbors, synthesizes new insights."""

    def __init__(self):
        self.graph = OKFKnowledgeGraph()

    def synthesize(self, concept_path: str, max_neighbors: int = 5) -> dict:
        """Read concept + neighbors, generate synthesis, write to OKF."""
        # Import OKF tools
        sys.path.insert(0, _EP_DIR)

        # Read core concept
        core = self._read_concept(concept_path)
        if not core:
            return {"status": "error", "error": f"Concept not found: {concept_path}"}

        # Get neighbors
        neighbors = self.graph.neighbors(concept_path, max_neighbors)
        neighbor_details = []
        for n in neighbors:
            detail = self._read_concept(n["path"])
            neighbor_details.append({
                "path": n["path"],
                "title": n.get("title", n["path"]),
                "similarity": n.get("similarity", 0),
                "type": n.get("type", ""),
                "snippet": (detail.get("body", "")[:500] if detail else ""),
            })

        # Build synthesis body
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        synth_path = f"synthesis/{concept_path.replace('/', '_')}_{ts}"

        body_lines = [
            f"# Synthesis: {core.get('title', concept_path)}",
            f"",
            f"**Generated:** {datetime.utcnow().isoformat()}Z",
            f"**Source concept:** {concept_path}",
            f"**Related concepts used:** {len(neighbor_details)}",
            f"",
            f"## Core Concept",
            f"",
            f"**Path:** {concept_path}",
            f"**Type:** {core.get('type', 'unknown')}",
            f"",
            f"{core.get('body', '')[:1000]}",
            f"",
            f"## Related Concepts",
            f"",
        ]
        for nd in neighbor_details:
            body_lines.append(f"### {nd['title']} (similarity: {nd['similarity']})")
            body_lines.append(f"**Path:** {nd['path']}  **Type:** {nd['type']}")
            body_lines.append(f"")
            body_lines.append(f"{nd['snippet']}")
            body_lines.append(f"")

        body_lines.append(f"## Synthesis")
        body_lines.append(f"")
        body_lines.append(f"### Common Themes")
        body_lines.append(f"- Theme 1: ...")
        body_lines.append(f"- Theme 2: ...")
        body_lines.append(f"")
        body_lines.append(f"### Unique Contributions")
        body_lines.append(f"- Each concept contributes: ...")
        body_lines.append(f"")
        body_lines.append(f"### Emerging Insights")
        body_lines.append(f"- New connections: ...")
        body_lines.append(f"")
        body_lines.append(f"### Open Questions")
        body_lines.append(f"- Gap: ...")

        body = "\n".join(body_lines)

        # Write to OKF
        from magix_okf import write_concept
        result = write_concept(
            path=synth_path,
            frontmatter={
                "type": "Note",
                "title": f"Synthesis: {core.get('title', concept_path)}",
                "source_concept": concept_path,
                "related_concepts": [n["path"] for n in neighbor_details],
            },
            body=body,
            commit_message=f"Synthesis: {concept_path} ({len(neighbor_details)} neighbors)",
        )

        return {
            "status": "synthesized",
            "path": synth_path,
            "source": concept_path,
            "neighbors_used": len(neighbor_details),
            "okf_result": result,
        }

    def _read_concept(self, path: str) -> Optional[dict]:
        """Read an OKF concept from disk."""
        target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
        if not target.exists():
            return None
        try:
            from magix_okf import parse_okf
            content = target.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_okf(content)
            return {"path": path, "type": fm.get("type"), "title": fm.get("title"), "body": body}
        except Exception:
            return None


# ── MCP tool registry ───────────────────────────────────────────

_GRAPH = OKFKnowledgeGraph()

def graph_status(args: dict = None) -> dict:
    _GRAPH.build()
    return {"status": "ok", "graph": _GRAPH.stats()}

def get_neighbors(args: dict) -> dict:
    path = args.get("path", "")
    limit = args.get("limit", 10)
    _GRAPH.build()
    results = _GRAPH.neighbors(path, limit)
    return {"status": "ok", "path": path, "neighbors": results, "count": len(results)}

def recommend(args: dict) -> dict:
    path = args.get("path", "")
    query = args.get("query", "")
    limit = args.get("limit", 5)
    rec = OKFRecommender()
    if path:
        results = rec.for_concept(path, limit)
    elif query:
        results = rec.for_query(query, limit)
    else:
        return {"status": "error", "error": "path or query required"}
    return {"status": "ok", "results": results, "count": len(results)}

def synthesize(args: dict) -> dict:
    path = args.get("path", "")
    if not path:
        return {"status": "error", "error": "path required"}
    engine = OKFReasoningEngine()
    return engine.synthesize(path)

def graph_data(args: dict = None) -> dict:
    _GRAPH.build()
    return _GRAPH.to_graph_data()

TOOLS = {
    "graph_status": graph_status,
    "get_neighbors": get_neighbors,
    "recommend": recommend,
    "synthesize": synthesize,
    "graph_data": graph_data,
}


# ── CLI ─────────────────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "graph"

    if action in ("graph", "status"):
        _GRAPH.build()
        s = _GRAPH.stats()
        print(f"Knowledge Graph: {s['nodes']} nodes, {s['edges']} edges")
        print(f"Threshold: {s['threshold']}, Avg degree: {s['avg_degree']}")
        print(f"Types: {json.dumps(s['types'], indent=2)}")

    elif action == "neighbors":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        if not path:
            print("Usage: python3 era2_phase2.py neighbors <path>")
            sys.exit(1)
        _GRAPH.build()
        results = _GRAPH.neighbors(path)
        print(f"Neighbors of '{path}':")
        for r in results:
            print(f"  [{r['similarity']:.2f}] {r['path']} ({r['type']})")

    elif action == "recommend":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        rec = OKFRecommender()
        results = rec.for_concept(path) if path else rec.for_query(query)
        print("Recommendations:")
        for r in results:
            print(f"  [{r.get('similarity', 0):.2f}] {r.get('path', '')} ({r.get('type', '')})")

    elif action == "synthesize":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        if not path:
            print("Usage: python3 era2_phase2.py synthesize <path>")
            sys.exit(1)
        engine = OKFReasoningEngine()
        result = engine.synthesize(path)
        print(json.dumps(result, indent=2))

    elif action in ("api/graph", "graph_data"):
        _GRAPH.build()
        print(json.dumps(_GRAPH.to_graph_data(), indent=2))

    else:
        print(f"Usage: {sys.argv[0]} [graph|neighbors|recommend|synthesize|api/graph]")


if __name__ == "__main__":
    main()
