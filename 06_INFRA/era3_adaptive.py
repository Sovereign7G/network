#!/usr/bin/env python3
"""
era3_adaptive.py — Era III: Adaptive Layer for Sovereign OS.

Four components:
  1. AutoTypeGenerator — discovers new concept types from unstructured data
  2. SkillEvolution — tracks usage, captures human edits, proposes improvements
  3. SelfHealingEngine — detects anomalies, spawns repairs
  4. FeedbackLearner — human edits become training data

All results are written back to OKF concepts with git audit trail.
"""

import json, os, sys, re, time, hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any, Optional, Tuple

_EP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _EP_DIR)

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()

SCHEMA_PATH = KNOWLEDGE_ROOT / "SCHEMA.md"
FEEDBACK_DIR = KNOWLEDGE_ROOT / ".feedback"
METRICS_DIR = KNOWLEDGE_ROOT / ".metrics"
REPAIR_DIR = KNOWLEDGE_ROOT / ".repairs"

for d in [FEEDBACK_DIR, METRICS_DIR, REPAIR_DIR]:
    d.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, _EP_DIR)


def _okf_parse(text: str) -> tuple:
    """Parse OKF file into (frontmatter, body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        import yaml
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    return fm, parts[2].strip()


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _write_okf(path: str, fm: dict, body: str, msg: str = None):
    """Write an OKF concept via magix_okf if available."""
    try:
        from magix_okf import write_concept
        return write_concept(path=path, frontmatter=fm, body=body, commit_message=msg)
    except Exception:
        # Fallback: write directly
        target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        import yaml
        fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
        target.write_text(f"---\n{fm_yaml}\n---\n\n{body.strip()}\n")
        return {"path": path, "written": True, "fallback": True}


# ── 1. Auto-Type Generator ──────────────────────────────────────

class AutoTypeGenerator:
    """Discovers new concept types from unstructured OKF writes."""

    def discover_patterns(self) -> List[Dict[str, Any]]:
        """Scan concepts without proper types and propose new schemas."""
        unstructured = []
        for entry in sorted(KNOWLEDGE_ROOT.rglob("index.md")):
            try:
                content = entry.read_text(encoding="utf-8", errors="replace")
                fm, body = _okf_parse(content)
                t = fm.get("type", "")
                # Consider "Note", unnamed, or concepts with unusual structure
                if t in (None, "", "Note") or (t not in self._known_types() and len(body) > 100):
                    unstructured.append({
                        "path": str(entry.parent.relative_to(KNOWLEDGE_ROOT)),
                        "body": body[:2000],
                        "title": fm.get("title", entry.parent.name),
                        "tags": fm.get("tags", []),
                    })
            except Exception:
                continue

        patterns = self._extract_patterns(unstructured)
        proposals = self._generate_proposals(patterns, unstructured)
        return proposals

    def _known_types(self) -> set:
        try:
            from okf_validator import load_schemas
            return set(load_schemas().keys())
        except Exception:
            return set()

    def _extract_patterns(self, concepts: list) -> dict:
        patterns = {"titles": [], "sections": [], "verbs": [], "entities": []}
        for c in concepts:
            body = c["body"]
            titles = re.findall(r"^#\s+(.+)$", body, re.MULTILINE)
            patterns["titles"].extend(titles)
            sections = re.findall(r"^##\s+(.+)$", body, re.MULTILINE)
            patterns["sections"].extend(sections)
            verbs = re.findall(r"\b(analyze|report|summary|comparison|review|plan|proposal|status|update|meeting|notes|minutes|draft|final|v\d+)\b", body.lower())
            patterns["verbs"].extend(verbs)
            entities = re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", body)
            patterns["entities"].extend(entities)
        return patterns

    def _generate_proposals(self, patterns: dict, concepts: list) -> list:
        proposals = []
        verb_counts = Counter(patterns["verbs"])
        section_counts = Counter(patterns["sections"])

        # Propose from strongest verb signals
        type_map = {
            "meeting": {"type": "MeetingNotes", "required": ["date", "attendees"]},
            "minutes": {"type": "MeetingNotes", "required": ["date", "attendees"]},
            "status": {"type": "StatusUpdate", "required": ["project", "status"]},
            "report": {"type": "Report", "required": ["date"]},
            "proposal": {"type": "Proposal", "required": ["author"]},
            "plan": {"type": "Plan", "required": ["milestones"]},
            "review": {"type": "Review", "required": ["subject", "rating"]},
            "summary": {"type": "Summary", "required": ["source"]},
            "comparison": {"type": "Comparison", "required": ["items"]},
        }

        for verb, count in verb_counts.most_common(10):
            if count >= 2 and verb in type_map and count >= 3:
                tinfo = type_map[verb]
                proposals.append({
                    "type": tinfo["type"],
                    "confidence": round(min(count / 10, 1.0), 2),
                    "source": f"'{verb}' appears in {count} concepts",
                    "required": tinfo["required"],
                    "example": verb,
                })

        # Deduplicate
        seen = set()
        unique = []
        for p in proposals:
            if p["type"] not in seen:
                seen.add(p["type"])
                unique.append(p)
        return unique[:5]

    def register_type(self, type_name: str, required: list) -> dict:
        """Register a discovered type in SCHEMA.md."""
        schema_block = f"""
{type_name}:
  type: object
  required:
    - type
    - title
{os.linesep.join(f'    - {r}' for r in required)}
  properties:
    type:
      const: {type_name}
    title:
      type: string
    tags:
      type: array
      items: string
    status:
      enum: ["draft", "active", "archived"]
    updated:
      type: string
      format: date-time
"""
        try:
            with open(SCHEMA_PATH, "a") as f:
                f.write("\n" + schema_block.strip() + "\n")
            _write_okf(
                f"system/auto_types/{type_name}",
                {"type": "SystemConfig", "title": f"Auto-registered type: {type_name}"},
                f"Type '{type_name}' was automatically discovered and registered in SCHEMA.md.\nRequired fields: {required}",
                f"Auto-register type: {type_name}",
            )
            return {"registered": True, "type": type_name, "required": required}
        except Exception as e:
            return {"registered": False, "error": str(e)}


# ── 2. Skill Evolution ──────────────────────────────────────────

class SkillEvolution:
    """Tracks skill execution, captures human edits, proposes improvements."""

    def __init__(self):
        self.metrics_file = METRICS_DIR / "skill_metrics.json"
        self._metrics = self._load()

    def _load(self) -> dict:
        if self.metrics_file.exists():
            try:
                return json.loads(self.metrics_file.read_text())
            except Exception:
                pass
        return {}

    def _save(self):
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics_file.write_text(json.dumps(self._metrics, indent=2))

    def track(self, skill_name: str, success: bool, duration_ms: float = 0,
              output: str = "", context: str = "") -> dict:
        if skill_name not in self._metrics:
            self._metrics[skill_name] = {"executions": 0, "successes": 0, "failures": 0,
                                          "avg_duration_ms": 0, "human_edits": 0}
        m = self._metrics[skill_name]
        m["executions"] += 1
        if success:
            m["successes"] += 1
        else:
            m["failures"] += 1
        old_avg = m["avg_duration_ms"]
        m["avg_duration_ms"] = round((old_avg * (m["executions"] - 1) + duration_ms) / m["executions"], 1)
        self._save()
        return {"tracked": True, "skill": skill_name}

    def capture_human_edit(self, skill_name: str, original: str, edited: str) -> dict:
        path = FEEDBACK_DIR / f"{skill_name}_{_ts()}.json"
        path.write_text(json.dumps({
            "skill": skill_name, "original": original[:500], "edited": edited[:500],
            "timestamp": _now(),
        }, indent=2))
        if skill_name in self._metrics:
            self._metrics[skill_name]["human_edits"] = self._metrics[skill_name].get("human_edits", 0) + 1
            self._save()
        return {"captured": True, "path": str(path)}

    def propose_improvement(self, skill_name: str) -> dict:
        m = self._metrics.get(skill_name)
        if not m:
            return {"status": "no_data", "skill": skill_name}
        edit_count = m.get("human_edits", 0)
        if edit_count < 3:
            return {"status": "insufficient_data", "skill": skill_name, "edits_needed": 3 - edit_count}

        success_rate = m["successes"] / max(m["executions"], 1)
        proposals = []
        if success_rate < 0.8:
            proposals.append(f"Success rate is {success_rate:.0%} — review skill logic")
        if m.get("avg_duration_ms", 0) > 5000:
            proposals.append(f"Avg duration {m['avg_duration_ms']}ms — consider optimization")
        if edit_count > 5:
            proposals.append(f"{edit_count} human edits — review output quality")

        result = {
            "skill": skill_name,
            "executions": m["executions"],
            "success_rate": round(success_rate, 2),
            "avg_duration_ms": m.get("avg_duration_ms", 0),
            "human_edits": edit_count,
            "proposals": proposals or ["No improvements needed"],
        }
        _write_okf(
            f"system/improvements/{skill_name}_{_ts()}",
            {"type": "SystemConfig", "title": f"Improvement: {skill_name}"},
            json.dumps(result, indent=2),
            f"Improvement analysis: {skill_name}",
        )
        return result


# ── 3. Self-Healing Engine ──────────────────────────────────────

class SelfHealingEngine:
    """Detects anomalies and spawns repair actions."""

    def detect(self) -> list:
        anomalies = []

        # Check schema violations
        violations = self._check_schema_violations()
        if violations > 0:
            anomalies.append({"type": "schema_violation", "severity": "high",
                              "count": violations,
                              "detail": f"{violations} concepts with invalid types"})

        # Check embedding health
        try:
            from embedding_pipeline import get_embedder
            emb = get_embedder()
            if emb:
                count = emb.collection.count()
                expected = sum(1 for _ in KNOWLEDGE_ROOT.rglob("index.md"))
                if count < expected * 0.8:
                    anomalies.append({"type": "embedding_stale", "severity": "medium",
                                      "count": count, "expected": expected,
                                      "detail": f"Only {count}/{expected} concepts embedded"})
        except Exception:
            pass

        # Check for stale feedback
        stale = list(FEEDBACK_DIR.glob("*.json"))
        if len(stale) > 20:
            anomalies.append({"type": "feedback_backlog", "severity": "low",
                              "count": len(stale),
                              "detail": f"{len(stale)} unprocessed feedback items"})

        return anomalies

    def _check_schema_violations(self) -> int:
        violations = 0
        try:
            from okf_validator import load_schemas
            schemas = load_schemas()
            valid_types = set(schemas.keys())
            for entry in KNOWLEDGE_ROOT.rglob("index.md"):
                try:
                    fm, _ = _okf_parse(entry.read_text())
                    t = fm.get("type", "")
                    if t not in valid_types:
                        violations += 1
                except Exception:
                    pass
        except Exception:
            pass
        return violations

    def repair(self, anomaly: dict) -> dict:
        """Execute repair action for an anomaly."""
        repair_id = _ts()

        if anomaly["type"] == "embedding_stale":
            try:
                from embedding_pipeline import get_embedder
                emb = get_embedder()
                if emb:
                    r = emb.reindex_all()
                    result = {"action": "reindexed", "concepts": r.get("reindexed", 0)}
            except Exception as e:
                result = {"action": "failed", "error": str(e)}

        elif anomaly["type"] == "feedback_backlog":
            feedback_dir = FEEDBACK_DIR
            count = len(list(feedback_dir.glob("*.json")))
            result = {"action": "backlogged", "count": count, "note": "Manual review recommended"}

        else:
            result = {"action": "noop", "note": f"No repair defined for {anomaly['type']}"}

        report = {
            "repair_id": repair_id,
            "anomaly": anomaly["type"],
            "severity": anomaly.get("severity"),
            "result": result,
            "timestamp": _now(),
        }
        _write_okf(
            f"system/repairs/{repair_id}",
            {"type": "SystemConfig", "title": f"Repair: {anomaly['type']}"},
            json.dumps(report, indent=2),
            f"Auto-repair: {anomaly['type']}",
        )
        return report


# ── 4. Feedback Learner ─────────────────────────────────────────

class FeedbackLearner:
    """Human edits become training data for future outputs."""

    def generate_training(self, skill_name: str = None, limit: int = 50) -> dict:
        pattern = f"{skill_name}_*.json" if skill_name else "*.json"
        files = sorted(FEEDBACK_DIR.glob(pattern), reverse=True)[:limit]
        data = []
        for f in files:
            try:
                data.append(json.loads(f.read_text()))
            except Exception:
                pass
        return {"files": len(files), "entries": len(data), "skill": skill_name or "all"}

    def analyze_trends(self) -> list:
        files = sorted(FEEDBACK_DIR.glob("*.json"), reverse=True)[:100]
        trends = Counter()
        for f in files:
            try:
                d = json.loads(f.read_text())
                skill = d.get("skill", "unknown")
                trends[skill] += 1
            except Exception:
                pass
        return [{"skill": s, "feedback_count": c} for s, c in trends.most_common()]


# ── MCP tool registry ───────────────────────────────────────────

_AUTO = AutoTypeGenerator()
_EVOLVE = SkillEvolution()
_HEAL = SelfHealingEngine()
_LEARN = FeedbackLearner()

def discover_types(args: dict = None) -> dict:
    proposals = _AUTO.discover_patterns()
    return {"status": "ok", "proposals": proposals, "count": len(proposals)}

def register_type(args: dict) -> dict:
    type_name = args.get("type_name", "")
    required = args.get("required", ["timestamp"])
    if not type_name:
        return {"status": "error", "error": "type_name required"}
    return _AUTO.register_type(type_name, required)

def track_skill(args: dict) -> dict:
    return _EVOLVE.track(
        args.get("skill_name", ""),
        args.get("success", True),
        args.get("duration_ms", 0),
        args.get("output", ""),
        args.get("context", ""),
    )

def capture_feedback(args: dict) -> dict:
    return _EVOLVE.capture_human_edit(
        args.get("skill_name", ""),
        args.get("original", ""),
        args.get("edited", ""),
    )

def propose_improvement(args: dict) -> dict:
    return _EVOLVE.propose_improvement(args.get("skill_name", ""))

def detect_anomalies(args: dict = None) -> dict:
    anomalies = _HEAL.detect()
    return {"status": "ok", "anomalies": anomalies, "count": len(anomalies)}

def repair_anomaly(args: dict) -> dict:
    anomaly_type = args.get("type", "")
    severity = args.get("severity", "medium")
    return _HEAL.repair({"type": anomaly_type, "severity": severity})

def feedback_trends(args: dict = None) -> dict:
    return {"status": "ok", "trends": _LEARN.analyze_trends()}


TOOLS = {
    "discover_types": discover_types,
    "register_type": register_type,
    "track_skill": track_skill,
    "capture_feedback": capture_feedback,
    "propose_improvement": propose_improvement,
    "detect_anomalies": detect_anomalies,
    "repair_anomaly": repair_anomaly,
    "feedback_trends": feedback_trends,
}


# ── CLI ─────────────────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "discover_types"

    if action == "discover_types":
        p = _AUTO.discover_patterns()
        print(f"Type proposals ({len(p)}):")
        for prop in p:
            print(f"  [{prop['confidence']}] {prop['type']} — {prop['source']}")

    elif action == "register_type":
        t = sys.argv[2] if len(sys.argv) > 2 else ""
        req = sys.argv[3].split(",") if len(sys.argv) > 3 else ["timestamp"]
        r = _AUTO.register_type(t, req)
        print(json.dumps(r, indent=2))

    elif action == "track":
        s = sys.argv[2] if len(sys.argv) > 2 else "test_skill"
        r = _EVOLVE.track(s, True)
        print(json.dumps(r, indent=2))

    elif action == "improve":
        s = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(_EVOLVE.propose_improvement(s), indent=2))

    elif action == "detect":
        a = _HEAL.detect()
        print(f"Anomalies ({len(a)}):")
        for an in a:
            print(f"  [{an['severity']}] {an['type']}: {an.get('detail', '')}")
        if not a:
            print("  None — system healthy")

    elif action == "repair":
        t = sys.argv[2] if len(sys.argv) > 2 else "embedding_stale"
        print(json.dumps(_HEAL.repair({"type": t, "severity": "medium"}), indent=2))

    elif action == "feedback_trends":
        trends = _LEARN.analyze_trends()
        for t in trends:
            print(f"  {t['skill']}: {t['feedback_count']} feedback entries")

    else:
        print(f"Usage: {sys.argv[0]} [discover_types|register_type|track|improve|detect|repair|feedback_trends]")


if __name__ == "__main__":
    main()
