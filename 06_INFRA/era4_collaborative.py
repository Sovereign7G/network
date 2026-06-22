#!/usr/bin/env python3
"""
era4_collaborative.py — Era IV: Collaborative Layer for Sovereign OS.

Four components:
  1. FederatedOKF — multi-instance OKF sync via git remotes
  2. AgentSwarm — spawn specialized agents, assign tasks, track results
  3. KnowledgeMarket — publish/acquire concepts with provenance
  4. CollectiveReasoning — solve problems across instances

All results written as OKF concepts with full audit trail.
"""

import json, os, sys, time, hashlib, uuid, subprocess, threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

_EP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _EP_DIR)

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()
MAGY_DIR = os.path.expanduser("~/projects/magy")


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _run_skill(skill_name: str, *args) -> dict:
    """Run a skill script and return JSON result if available."""
    skill_path = os.path.join(MAGY_DIR, skill_name)
    if not os.path.exists(skill_path):
        return {"error": f"Skill not found: {skill_name}"}
    try:
        r = subprocess.run(["python3", skill_path] + list(args),
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                return {"output": r.stdout[:500]}
        return {"error": r.stderr[:200]}
    except subprocess.TimeoutExpired:
        return {"error": "skill timed out"}


# ── 1. Federated OKF ────────────────────────────────────────────

class FederatedOKF:
    """Sync OKF bundles with remote Sovereign OS instances via git."""

    def __init__(self):
        self.remotes_file = KNOWLEDGE_ROOT.parent / ".git" / "federated_remotes.json"
        self._remotes = self._load()

    def _load(self) -> dict:
        if self.remotes_file and self.remotes_file.exists():
            try:
                return json.loads(self.remotes_file.read_text())
            except Exception:
                pass
        return {}

    def _save(self):
        self.remotes_file.write_text(json.dumps(self._remotes, indent=2))

    def add_remote(self, name: str, url: str) -> dict:
        cid = hashlib.md5(url.encode()).hexdigest()[:8]
        self._remotes[name] = {"url": url, "id": cid, "last_sync": None, "status": "pending"}
        try:
            subprocess.run(["git", "remote", "add", name, url],
                           cwd=str(KNOWLEDGE_ROOT.parent), capture_output=True, timeout=10)
        except Exception:
            pass
        self._save()
        return {"remote": name, "id": cid, "added": True}

    def sync(self, remote_name: str = None) -> dict:
        targets = [remote_name] if remote_name else list(self._remotes.keys())
        results = []
        for name in targets:
            info = self._remotes.get(name)
            if not info:
                results.append({"remote": name, "status": "unknown"})
                continue
            try:
                r = subprocess.run(["git", "fetch", name],
                                   cwd=str(KNOWLEDGE_ROOT.parent), capture_output=True, timeout=30)
                info["last_sync"] = _now()
                info["status"] = "synced" if r.returncode == 0 else "fetch_failed"
                results.append({"remote": name, "status": info["status"]})
            except subprocess.TimeoutExpired:
                results.append({"remote": name, "status": "timeout"})
            except Exception as e:
                results.append({"remote": name, "status": "error", "error": str(e)[:100]})
            self._save()
        return {"synced": len(results), "results": results}

    def status(self) -> dict:
        return {"remotes": self._remotes, "count": len(self._remotes)}

    def remove_remote(self, name: str) -> dict:
        if name in self._remotes:
            del self._remotes[name]
            try:
                subprocess.run(["git", "remote", "remove", name],
                               cwd=str(KNOWLEDGE_ROOT.parent), capture_output=True, timeout=10)
            except Exception:
                pass
            self._save()
            return {"remote": name, "removed": True}
        return {"remote": name, "removed": False, "error": "not found"}


# ── 2. Agent Swarm ──────────────────────────────────────────────

class AgentSwarm:
    """Spawn specialized agents, assign tasks, track results via OKF."""

    def __init__(self):
        self.swarm_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.agents: Dict[str, dict] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

    def spawn(self, role: str, capabilities: List[str], context: str = "") -> dict:
        aid = hashlib.md5(f"{role}{time.time()}".encode()).hexdigest()[:12]
        self.agents[aid] = {
            "id": aid, "role": role, "capabilities": capabilities,
            "context": context, "status": "idle", "tasks": [], "results": [],
        }
        _write_okf(f"swarm/{self.swarm_id}/agents/{aid}",
                   {"type": "SystemConfig", "title": f"Swarm agent: {role}"},
                   json.dumps(self.agents[aid], indent=2),
                   f"Swarm: spawn {role}")
        return {"agent_id": aid, "role": role, "swarm_id": self.swarm_id, "status": "spawned"}

    def assign(self, agent_id: str, task: dict) -> dict:
        agent = self.agents.get(agent_id)
        if not agent:
            return {"error": f"Agent {agent_id} not found"}
        tid = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        agent["tasks"].append({"id": tid, "task": task, "status": "assigned"})
        agent["status"] = "working"
        self.executor.submit(self._execute, agent_id, tid, task)
        return {"task_id": tid, "agent_id": agent_id, "status": "assigned"}

    def _execute(self, agent_id: str, task_id: str, task: dict):
        agent = self.agents[agent_id]
        caps = [c.lower() for c in agent.get("capabilities", [])]
        result = {}
        if "research" in caps:
            result = _run_skill("skill_research.py", task.get("topic", "general"))
        elif "email" in caps:
            result = _run_skill("skill_email.py", "process")
        elif "document" in caps:
            result = _run_skill("skill_document.py", "create", task.get("title", "Untitled"))
        elif "compare" in caps:
            result = _run_skill("skill_compare.py", "run",
                                task.get("prompt", "default"), "model_a", "model_b")
        else:
            result = {"note": f"capabilities={caps} no matching skill"}
        agent["results"].append(result)
        agent["status"] = "idle"
        _write_okf(f"swarm/{self.swarm_id}/results/{task_id}",
                   {"type": "Note", "title": f"Task: {task_id}"},
                   json.dumps({"agent_id": agent_id, "task": task, "result": result}, indent=2),
                   f"Swarm: result {task_id}")

    def status(self) -> dict:
        return {
            "swarm_id": self.swarm_id,
            "agents": len(self.agents),
            "agent_list": [{"id": a["id"], "role": a["role"], "status": a["status"],
                            "tasks": len(a["tasks"]), "results": len(a["results"])}
                           for a in self.agents.values()],
        }


# ── 3. Knowledge Market ────────────────────────────────────────

class KnowledgeMarket:
    """Publish, discover, and acquire concepts across instances."""

    def __init__(self):
        self.market_dir = KNOWLEDGE_ROOT / "market"
        self.market_dir.mkdir(parents=True, exist_ok=True)
        self.trades_file = self.market_dir / "trades.json"
        self._trades = self._load_trades()

    def _load_trades(self) -> list:
        if self.trades_file.exists():
            try:
                return json.loads(self.trades_file.read_text())
            except Exception:
                pass
        return []

    def _save_trades(self):
        self.trades_file.write_text(json.dumps(self._trades, indent=2))

    def publish(self, concept_path: str, price: int = 0, tags: List[str] = None) -> dict:
        try:
            from magix_okf import serve_concept
            concept = serve_concept(concept_path)
        except Exception:
            concept = {"status": "not_found"}
        if concept.get("status") != "ok":
            return {"error": f"Concept not found: {concept_path}"}

        lid = hashlib.md5(concept_path.encode()).hexdigest()[:12]
        listing = {
            "id": lid, "path": concept_path,
            "type": concept.get("type", "unknown"),
            "title": concept.get("title", concept_path),
            "price": price, "tags": tags or [],
            "publisher": "local", "published": _now(),
        }
        _write_okf(f"market/listings/{lid}",
                   {"type": "SystemConfig", "title": f"Market: {concept_path}"},
                   json.dumps(listing, indent=2),
                   f"Market: publish {concept_path}")
        return {"listing_id": lid, "published": True, "price": price}

    def acquire(self, listing_id: str, remote_url: str = None) -> dict:
        """Acquire a concept by listing ID."""
        # Try local first
        try:
            from magix_okf import serve_concept
            listing = serve_concept(f"market/listings/{listing_id}")
        except Exception:
            listing = {"status": "not_found"}

        if listing.get("status") != "ok" and remote_url:
            return {"error": "remote acquisition not yet implemented, use federated sync first"}

        if listing.get("status") != "ok":
            return {"error": f"Listing not found: {listing_id}"}

        concept_path = listing.get("frontmatter", {}).get("concept_path", "")
        if not concept_path:
            return {"error": "no concept_path in listing"}

        trade = {"listing_id": listing_id, "path": concept_path, "acquired": _now()}
        self._trades.append(trade)
        self._save_trades()
        return {"acquired": True, "path": concept_path, "listing_id": listing_id}

    def listings(self) -> dict:
        listings = []
        for entry in sorted((KNOWLEDGE_ROOT / "market/listings").rglob("index.md")):
            try:
                import yaml
                content = entry.read_text()
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1]) or {}
                    listings.append(fm)
            except Exception:
                pass
        return {"listings": listings, "count": len(listings), "trades": len(self._trades)}


# ── 4. Collective Reasoning ─────────────────────────────────────

class CollectiveReasoning:
    """Solve problems across multiple instances."""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}

    def reason(self, problem: str, instances: List[dict] = None) -> dict:
        sid = hashlib.md5(f"{problem}{time.time()}".encode()).hexdigest()[:12]
        instances = instances or []

        results = []
        with ThreadPoolExecutor(max_workers=max(1, len(instances))) as ex:
            futures = {}
            for inst in instances:
                name = inst.get("name", "unknown")
                fut = ex.submit(self._query_instance, inst, problem)
                futures[fut] = name
            for fut in as_completed(futures):
                results.append({"instance": futures[fut], "data": fut.result()})

        # Build synthesis
        lines = [f"# Collective Reasoning: {problem}", "",
                 f"**Session:** {sid}", f"**Participants:** {len(instances)}", ""]
        for r in results:
            lines.append(f"## {r['instance']}")
            lines.append(str(r["data"])[:500])
            lines.append("")
        lines.append("## Synthesis")
        lines.append("Synthesis from all instances combined.")
        body = "\n".join(lines)

        self.sessions[sid] = {"problem": problem, "results": results, "status": "completed"}
        _write_okf(f"collective/{sid}",
                   {"type": "Note", "title": f"Collective: {problem[:50]}"},
                   body, f"Collective reasoning: {problem[:60]}")
        return {"session_id": sid, "results": results, "status": "completed"}

    def _query_instance(self, instance: dict, problem: str) -> Any:
        name = instance.get("name", "")
        skill = instance.get("skill", "")
        if skill:
            result = _run_skill(skill, problem)
            return result
        return {"note": f"simulated response from {name}"}

    def session_status(self, session_id: str = None) -> dict:
        if session_id:
            return self.sessions.get(session_id, {"error": "not found"})
        return {"sessions": len(self.sessions), "active": sum(1 for s in self.sessions.values()
                                                               if s.get("status") == "in_progress")}


# ── OKF write helper ────────────────────────────────────────────

def _write_okf(path: str, fm: dict, body: str, msg: str = None):
    try:
        from magix_okf import write_concept
        return write_concept(path=path, frontmatter=fm, body=body, commit_message=msg)
    except Exception:
        target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            import yaml
            fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            target.write_text(f"---\n{fm_yaml}\n---\n\n{body.strip()}\n")
        except Exception:
            target.write_text(body)
        return {"path": path, "written": True, "fallback": True}


# ── MCP tools ───────────────────────────────────────────────────

_FED = FederatedOKF()
_SWARM = AgentSwarm()
_MARKET = KnowledgeMarket()
_COLLECTIVE = CollectiveReasoning()

def federated_add_remote(args: dict) -> dict:
    return _FED.add_remote(args.get("name", ""), args.get("url", ""))

def federated_sync(args: dict) -> dict:
    return _FED.sync(args.get("remote_name"))

def federated_status(args: dict = None) -> dict:
    return _FED.status()

def swarm_spawn(args: dict) -> dict:
    return _SWARM.spawn(args.get("role", "worker"), args.get("capabilities", []), args.get("context", ""))

def swarm_assign(args: dict) -> dict:
    return _SWARM.assign(args.get("agent_id", ""), args.get("task", {}))

def swarm_status(args: dict = None) -> dict:
    return _SWARM.status()

def market_publish(args: dict) -> dict:
    return _MARKET.publish(args.get("path", ""), args.get("price", 0), args.get("tags"))

def market_listings(args: dict = None) -> dict:
    return _MARKET.listings()

def market_acquire(args: dict) -> dict:
    return _MARKET.acquire(args.get("listing_id", ""), args.get("remote_url"))

def collective_reason(args: dict) -> dict:
    return _COLLECTIVE.reason(args.get("problem", ""), args.get("instances", []))


TOOLS = {
    "federated_add_remote": federated_add_remote,
    "federated_sync": federated_sync,
    "federated_status": federated_status,
    "swarm_spawn": swarm_spawn,
    "swarm_assign": swarm_assign,
    "swarm_status": swarm_status,
    "market_publish": market_publish,
    "market_listings": market_listings,
    "market_acquire": market_acquire,
    "collective_reason": collective_reason,
}


# ── CLI ─────────────────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    if action == "federated_status":
        s = _FED.status()
        print(f"Federated remotes: {s['count']}")
        for n, info in s["remotes"].items():
            print(f"  {n}: {info['url']} | last_sync={info.get('last_sync','never')}")
    elif action == "federated_add":
        print(json.dumps(_FED.add_remote(sys.argv[2], sys.argv[3]), indent=2))
    elif action == "swarm_spawn":
        role = sys.argv[2] if len(sys.argv) > 2 else "research"
        caps = sys.argv[3].split(",") if len(sys.argv) > 3 else ["research"]
        print(json.dumps(_SWARM.spawn(role, caps), indent=2))
    elif action == "swarm_status":
        print(json.dumps(_SWARM.status(), indent=2))
    elif action == "market_publish":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        price = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        print(json.dumps(_MARKET.publish(path, price), indent=2))
    elif action == "market_listings":
        print(json.dumps(_MARKET.listings(), indent=2))
    elif action == "collective_reason":
        problem = sys.argv[2] if len(sys.argv) > 2 else "test"
        print(json.dumps(_COLLECTIVE.reason(problem), indent=2))
    elif action == "collective_status":
        print(json.dumps(_COLLECTIVE.session_status(), indent=2))
    else:
        print("Usage: python3 era4_collaborative.py [federated_status|federated_add|swarm_spawn|swarm_status|market_publish|market_listings|collective_reason|collective_status]")


if __name__ == "__main__":
    main()
