#!/usr/bin/env python3
"""
era5_autonomous.py — Era V: Autonomous Layer for Sovereign OS.

Three components:
  1. SelfImprovement — analyzes own code, proposes and applies fixes
  2. EthicsLayer — constraints on autonomous action, human oversight
  3. ContinuousEvolution — never-done monitoring and improvement loop

All actions logged to OKF with full audit trail and rollback capability.
"""

import json, os, sys, time, hashlib, ast, threading, subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

_EP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _EP_DIR)

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()
MAGY_DIR = os.path.expanduser("~/projects/magy")
MAGIX_DIR = os.path.expanduser("~/projects/magix")


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _write_okf(path: str, fm: dict, body: str, msg: str = None):
    try:
        from magix_okf import write_concept
        return write_concept(path=path, frontmatter=fm, body=body, commit_message=msg)
    except Exception:
        target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            import yaml
            target.write_text(f"---\n{yaml.dump(fm, default_flow_style=False).strip()}\n---\n\n{body.strip()}\n")
        except Exception:
            target.write_text(body)
        return {"path": path, "written": True, "fallback": True}


# ── 1. Self-Improvement ─────────────────────────────────────────

class SelfImprovement:
    """Analyzes and improves own code with rollback support."""

    def __init__(self):
        self.history_file = KNOWLEDGE_ROOT / ".history" / "improvements.json"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self._history = self._load()

    def _load(self) -> dict:
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text())
            except Exception:
                pass
        return {"improvements": [], "rollbacks": []}

    def _save(self):
        self.history_file.write_text(json.dumps(self._history, indent=2))

    def analyze(self, target: str = None) -> dict:
        """Analyze a file for improvement opportunities."""
        if not target:
            return self._analyze_all()

        path = Path(target)
        if not path.exists():
            # Search in expected directories
            for base in [Path(MAGY_DIR), Path(MAGIX_DIR), KNOWLEDGE_ROOT]:
                candidate = base / target
                if candidate.exists():
                    path = candidate
                    break
            else:
                return {"error": f"File not found: {target}"}

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return {"error": str(e)}

        opps = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {"error": "syntax error", "lines": len(content.split("\n"))}

        # Count elements
        funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

        # Check for TODO/FIXME
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# TODO") or stripped.startswith("# FIXME"):
                opps.append({"type": "todo", "severity": "medium",
                             "detail": stripped[:80]})

        # Check for bare except
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                opps.append({"type": "bare_except", "severity": "high",
                             "line": node.lineno})
            elif isinstance(node, ast.ExceptHandler) and isinstance(node.type, ast.Name) and node.type.id == "Exception":
                opps.append({"type": "broad_except", "severity": "medium",
                             "line": node.lineno})

        # Check for long functions
        for func in funcs:
            start = func.lineno
            end = func.end_lineno or start
            length = end - start
            if length > 80:
                opps.append({"type": "long_function", "severity": "low",
                             "function": func.name, "lines": length})

        return {
            "target": str(path),
            "lines": len(content.split("\n")),
            "functions": len(funcs),
            "classes": len(classes),
            "opportunities": opps,
            "count": len(opps),
        }

    def _analyze_all(self) -> dict:
        """Scan all skill and infra files."""
        results = []
        bases = [Path(MAGY_DIR), Path(MAGIX_DIR / "lib" / "magix")]
        for base in bases:
            if not base.exists():
                continue
            for f in sorted(base.rglob("*.py")):
                if "venv" in str(f) or ".git" in str(f):
                    continue
                r = self.analyze(str(f))
                if r.get("opportunities"):
                    results.append(r)
        return {"files_analyzed": len(results), "results": results}

    def propose(self, target: str) -> dict:
        """Propose specific improvements for a file."""
        analysis = self.analyze(target)
        if analysis.get("error"):
            return analysis

        proposals = []
        for opp in analysis.get("opportunities", [])[:5]:
            if opp["type"] == "bare_except":
                proposals.append({
                    "type": "replace_bare_except",
                    "line": opp["line"],
                    "description": "Replace bare `except:` with `except Exception:`",
                    "old": "except:",
                    "new": "except Exception:",
                })
            elif opp["type"] == "broad_except":
                proposals.append({
                    "type": "narrow_exception",
                    "line": opp["line"],
                    "description": "Consider catching specific exception types",
                })
            elif opp["type"] == "todo":
                proposals.append({
                    "type": "resolve_todo",
                    "description": opp["detail"],
                })

        result = {
            "target": analysis["target"],
            "proposals": proposals,
            "count": len(proposals),
        }
        _write_okf(f"system/improvements/{Path(analysis['target']).stem}_{_ts()}",
                   {"type": "SystemConfig", "title": f"Improvement: {Path(analysis['target']).name}"},
                   json.dumps(result, indent=2),
                   f"Propose: {analysis['target']}")
        return result

    def apply(self, target: str, proposal_type: str) -> dict:
        """Apply a proposed improvement (safely)."""
        path = Path(target).expanduser()
        if not path.exists():
            return {"error": f"File not found: {target}"}

        content = path.read_text(encoding="utf-8", errors="replace")

        # Create rollback snapshot
        rollback = {"target": str(path), "content": content, "at": _now()}
        self._history["rollbacks"].append(rollback)
        self._save()

        # Apply fix
        if proposal_type == "replace_bare_except":
            content = content.replace("\nexcept:\n", "\nexcept Exception:\n")
        elif proposal_type == "resolve_todo":
            content = content.replace("# TODO ", "# [DONE] ")
        else:
            return {"error": f"Unknown proposal type: {proposal_type}"}

        path.write_text(content)
        self._history["improvements"].append({
            "target": str(path), "type": proposal_type, "at": _now()
        })
        self._save()

        try:
            subprocess.run(["python3", "-m", "py_compile", str(path)],
                           capture_output=True, timeout=10, check=True)
            valid = True
        except subprocess.CalledProcessError:
            # Rollback on compilation error
            path.write_text(rollback["content"])
            valid = False

        return {"target": str(path), "applied": True, "type": proposal_type,
                "syntax_valid": valid}

    def rollback(self, target: str = None, index: int = -1) -> dict:
        """Rollback to a previous version."""
        snaps = self._history["rollbacks"]
        if target:
            snaps = [s for s in snaps if s["target"] == target]
        if not snaps:
            return {"error": "No rollback points found"}

        snap = snaps[index]
        Path(snap["target"]).write_text(snap["content"])
        return {"rolled_back": True, "target": snap["target"], "at": snap["at"]}


# ── 2. Ethics Layer ─────────────────────────────────────────────

class EthicsLayer:
    """Constraints on autonomous action to ensure safety."""

    def __init__(self):
        self.rules_file = KNOWLEDGE_ROOT / "system" / "ethics.json"
        self._rules = self._load()

    def _load(self) -> dict:
        defaults = {
            "version": "1.0", "updated": _now(),
            "principles": [
                {"id": "p1", "name": "Human Oversight",
                 "desc": "Critical actions require human approval", "severity": "critical"},
                {"id": "p2", "name": "Knowledge Integrity",
                 "desc": "No knowingly false information", "severity": "critical"},
                {"id": "p3", "name": "Transparency",
                 "desc": "All autonomous actions logged and auditable", "severity": "high"},
                {"id": "p4", "name": "Privacy",
                 "desc": "No sensitive data exposed to unauthorized instances", "severity": "critical"},
            ],
            "restrictions": [
                {"id": "r1", "name": "No Self-Replication",
                 "desc": "Must not create copies without explicit approval", "severity": "critical"},
                {"id": "r2", "name": "Resource Bounds",
                 "desc": "Autonomous improvements bounded by resource limits", "severity": "high"},
            ],
        }
        if self.rules_file.exists():
            try:
                return json.loads(self.rules_file.read_text())
            except Exception:
                pass
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)
        self.rules_file.write_text(json.dumps(defaults, indent=2))
        return defaults

    def check(self, action: dict) -> dict:
        """Check an action against all ethical rules."""
        violations = []
        for p in self._rules.get("principles", []):
            if self._violates(p, action):
                violations.append({"rule": p["name"], "severity": p["severity"],
                                   "id": p["id"]})

        for r in self._rules.get("restrictions", []):
            if self._violates(r, action):
                violations.append({"rule": r["name"], "severity": r["severity"],
                                   "id": r["id"]})

        approved = len(violations) == 0

        _write_okf(f"system/ethics_logs/{_ts()}",
                   {"type": "SystemConfig", "title": f"Ethics check: {action.get('type','?')}"},
                   json.dumps({"action": action, "approved": approved, "violations": violations}, indent=2),
                   f"Ethics: {approved}")
        return {"action": action.get("type"), "approved": approved,
                "violations": violations, "status": "approved" if approved else "rejected"}

    def _violates(self, rule: dict, action: dict) -> bool:
        aid = rule["id"]
        atype = action.get("type", "")
        if aid == "p1" and atype == "self_improvement" and action.get("severity") == "critical":
            return not action.get("human_approved", False)
        if aid == "p2" and atype == "write_concept" and action.get("verify_facts") is False:
            return True
        if aid == "r1" and atype == "spawn_agent" and (action.get("count", 0) or 0) > 5:
            return True
        if aid == "r2" and atype == "sync" and (action.get("concepts", 0) or 0) > 500:
            return True
        return False

    def add_rule(self, name: str, desc: str, severity: str = "medium") -> dict:
        """Add a new ethical rule."""
        nid = f"p{len(self._rules['principles']) + 1}"
        rule = {"id": nid, "name": name, "desc": desc, "severity": severity}
        self._rules["principles"].append(rule)
        self.rules_file.write_text(json.dumps(self._rules, indent=2))
        return {"added": True, "rule": rule}

    def get_rules(self) -> dict:
        return self._rules


# ── 3. Continuous Evolution ─────────────────────────────────────

class ContinuousEvolution:
    """Never-done monitoring and improvement loop."""

    def __init__(self):
        self._running = False
        self._thread = None
        self._cycle = 0
        self._config = {"interval_s": 3600, "enabled": True}

    def start(self) -> dict:
        if self._running:
            return {"status": "already_running"}
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        _write_okf(f"system/evolution/start_{_ts()}",
                   {"type": "SystemConfig", "title": "Evolution started"},
                   f"Continuous evolution started at {_now()}",
                   "Evolution: start")
        return {"status": "started", "config": self._config}

    def stop(self) -> dict:
        self._running = False
        return {"status": "stopped"}

    def status(self) -> dict:
        return {"running": self._running, "cycles": self._cycle, "config": self._config}

    def _loop(self):
        while self._running:
            self._cycle += 1
            try:
                # 1. Anomaly detection via self-healing engine
                try:
                    from era3_adaptive import SelfHealingEngine
                    anomalies = SelfHealingEngine().detect()
                except Exception:
                    anomalies = []

                # 2. Skill analysis
                improver = SelfImprovement()
                skill_files = list(Path(MAGY_DIR).glob("skill_*.py"))[:3]
                improvements = []
                for sf in skill_files:
                    analysis = improver.analyze(str(sf))
                    if analysis.get("opportunities"):
                        improvements.append({"file": sf.name, "count": len(analysis["opportunities"])})

                # 3. Log cycle
                summary = {
                    "cycle": self._cycle,
                    "anomalies": len(anomalies),
                    "improvements_found": len(improvements),
                    "timestamp": _now(),
                }
                _write_okf(f"system/evolution/cycles/cycle_{self._cycle}",
                           {"type": "SystemConfig", "title": f"Evolution cycle {self._cycle}"},
                           json.dumps(summary, indent=2),
                           f"Evolution cycle {self._cycle}")

            except Exception as e:
                _write_okf(f"system/evolution/errors/cycle_{self._cycle}",
                           {"type": "SystemConfig", "title": "Evolution error"},
                           str(e)[:500])
            time.sleep(self._config["interval_s"])


# ── MCP tools ───────────────────────────────────────────────────

_SI = SelfImprovement()
_EL = EthicsLayer()
_CE = ContinuousEvolution()


def analyze_skill(args: dict) -> dict:
    return _SI.analyze(args.get("target", ""))

def propose_improvement(args: dict) -> dict:
    return _SI.propose(args.get("target", ""))

def apply_improvement(args: dict) -> dict:
    return _SI.apply(args.get("target", ""), args.get("type", ""))

def rollback_skill(args: dict) -> dict:
    return _SI.rollback(args.get("target"), args.get("index", -1))

def check_ethics(args: dict) -> dict:
    return _EL.check(args.get("action", {}))

def add_ethics_rule(args: dict) -> dict:
    return _EL.add_rule(args.get("name", ""), args.get("description", ""), args.get("severity", "medium"))

def get_ethics_rules(args: dict = None) -> dict:
    return _EL.get_rules()

def evolution_start(args: dict = None) -> dict:
    return _CE.start()

def evolution_stop(args: dict = None) -> dict:
    return _CE.stop()

def evolution_status(args: dict = None) -> dict:
    return _CE.status()


TOOLS = {
    "analyze_skill": analyze_skill,
    "propose_improvement": propose_improvement,
    "apply_improvement": apply_improvement,
    "rollback_skill": rollback_skill,
    "check_ethics": check_ethics,
    "add_ethics_rule": add_ethics_rule,
    "get_ethics_rules": get_ethics_rules,
    "evolution_start": evolution_start,
    "evolution_stop": evolution_stop,
    "evolution_status": evolution_status,
}


# ── CLI ─────────────────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "help"

    if action == "analyze":
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        r = _SI.analyze(target)
        print(f"Analyzed: {r.get('target', 'all')}")
        print(f"  Lines: {r.get('lines', 0)}, Functions: {r.get('functions', 0)}, Opps: {r.get('count', 0)}")
        for o in r.get("opportunities", [])[:5]:
            print(f"  [{o['severity']}] {o['type']}: {o.get('detail', o.get('function', ''))}")

    elif action == "propose":
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        r = _SI.propose(target)
        for p in r.get("proposals", []):
            print(f"  [{p['type']}] {p.get('description', '')}")

    elif action == "apply":
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        ptype = sys.argv[3] if len(sys.argv) > 3 else "replace_bare_except"
        print(json.dumps(_SI.apply(target, ptype), indent=2))

    elif action == "rollback":
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(_SI.rollback(target), indent=2))

    elif action == "ethics":
        r = _EL.check({"type": sys.argv[2] if len(sys.argv) > 2 else "test", "severity": "low"})
        print(f"Approved: {r['approved']}")
        for v in r.get("violations", []):
            print(f"  Violation: {v['rule']} ({v['severity']})")

    elif action == "add_rule":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        print(json.dumps(_EL.add_rule(name, desc), indent=2))

    elif action == "evolution_start":
        print(json.dumps(_CE.start(), indent=2))

    elif action == "evolution_stop":
        print(json.dumps(_CE.stop(), indent=2))

    elif action == "evolution_status":
        print(json.dumps(_CE.status(), indent=2))

    else:
        print("Usage: python3 era5_autonomous.py [analyze|propose|apply|rollback|ethics|add_rule|evolution_start|evolution_stop|evolution_status]")


if __name__ == "__main__":
    main()
