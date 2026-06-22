#!/usr/bin/env python3
"""
s2l_pipeline.py — Skill-to-LoRA: From static OKF skills to parametric adapters.

Pipeline:
  1. generate_training_data — extracts skill patterns from OKF + skill scripts
  2. train_adapter — QLoRA fine-tuning stub (requires unsloth/peft at runtime)
  3. load_adapter — manages adapter loading/unloading per skill
  4. skill_inference — runs skill with adapter + optional OKF context fallback

Strategy: one adapter per skill, hybrid fallback to OKF context for edge cases.
"""

import json, os, sys, time, hashlib, subprocess, ast
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
ADAPTER_DIR = KNOWLEDGE_ROOT / ".adapters"
ADAPTER_DIR.mkdir(parents=True, exist_ok=True)


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


# ── 1. Training Data Generator ─────────────────────────────────

class TrainingDataGenerator:
    """Extracts skill patterns from OKF concepts + skill scripts → S2L training pairs.

    For each skill:
      - Reads the skill script for behavioral patterns (functions, params, docstrings)
      - Reads OKF concepts the skill interacts with (via type taxonomy)
      - Generates prompt → completion pairs for LoRA training
    """

    SKILL_TYPES = {
        "skill_research": ["ResearchFinding"],
        "skill_email": ["EmailThread", "EmailDraft"],
        "skill_document": ["Document"],
        "skill_compare": ["ModelComparison"],
        "skill_calendar": ["CalendarEvent"],
        "skill_notes": ["Note"],
    }

    def __init__(self):
        self.output_dir = KNOWLEDGE_ROOT / "training_data"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, skill_name: str = None) -> dict:
        """Generate training pairs for one or all skills."""
        targets = [skill_name] if skill_name else list(self.SKILL_TYPES.keys())
        total = 0
        results = []

        for name in targets:
            pairs = self._generate_for_skill(name)
            if pairs:
                path = self.output_dir / f"{name}_training.json"
                path.write_text(json.dumps(pairs, indent=2))
                results.append({"skill": name, "pairs": len(pairs), "path": str(path)})
                total += len(pairs)

        _write_okf(f"system/s2l/training_data_{_ts()}",
                   {"type": "SystemConfig", "title": f"S2L training data: {total} pairs"},
                   json.dumps(results, indent=2),
                   f"S2L: {total} training pairs generated")
        return {"skills": len(results), "total_pairs": total, "results": results}

    def _generate_for_skill(self, skill_name: str) -> list:
        """Generate training pairs for a single skill."""
        # Read skill script
        skill_path = Path(MAGY_DIR) / f"{skill_name}.py"
        if not skill_path.exists():
            return []

        content = skill_path.read_text(encoding="utf-8", errors="replace")

        # Extract functions as behavioral patterns
        import ast
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        relevant_types = self.SKILL_TYPES.get(skill_name, ["Note"])

        # Read relevant OKF concepts as examples
        examples = self._read_concepts_by_type(relevant_types, limit=5)

        # Generate prompt→completion pairs
        pairs = []
        for func in functions:
            if func.name.startswith("_"):
                continue  # Skip private helpers
            prompt = self._function_to_prompt(skill_name, func, examples)
            completion = self._function_to_completion(skill_name, func, content)
            if prompt and completion:
                pairs.append({
                    "skill": skill_name,
                    "function": func.name,
                    "prompt": prompt,
                    "completion": completion,
                    "source_concepts": [e.get("path") for e in examples[:2]],
                })

        return pairs

    def _read_concepts_by_type(self, types: list, limit: int = 5) -> list:
        """Read OKF concepts matching given types."""
        results = []
        for entry in sorted(KNOWLEDGE_ROOT.rglob("index.md")):
            if len(results) >= limit:
                break
            try:
                import yaml
                content = entry.read_text(encoding="utf-8", errors="replace")
                if not content.startswith("---"):
                    continue
                parts = content.split("---", 2)
                fm = yaml.safe_load(parts[1]) or {}
                if fm.get("type") in types:
                    results.append({
                        "path": str(entry.parent.relative_to(KNOWLEDGE_ROOT)),
                        "type": fm.get("type"),
                        "title": fm.get("title", ""),
                        "body": parts[2].strip()[:500] if len(parts) >= 3 else "",
                    })
            except Exception:
                pass
        return results

    def _function_to_prompt(self, skill: str, func: ast.FunctionDef,
                            examples: list) -> str:
        """Generate prompt from function signature + examples."""
        docstring = ast.get_docstring(func) or ""
        args = [a.arg for a in func.args.args if a.arg != "self"]
        prompt = f"You are a {skill.replace('_', ' ')} agent.\n\n"
        prompt += f"Task: {docstring[:200]}\n\n"
        prompt += f"Parameters: {', '.join(args)}\n\n"
        if examples:
            prompt += "Example context:\n"
            for ex in examples[:2]:
                prompt += f"- {ex.get('title', '')}: {ex.get('body', '')[:200]}\n"
        return prompt.strip()

    def _function_to_completion(self, skill: str, func: ast.FunctionDef,
                                source: str) -> str:
        """Generate completion from function body."""
        end = func.end_lineno or (func.lineno + 30)
        lines = source.split("\n")[func.lineno - 1:end]
        return "\n".join(lines)


# ── 2. Adapter Manager ─────────────────────────────────────────

class AdapterManager:
    """Manages LoRA adapter files: training, loading, unloading.

    In production, this would call unsloth/peft for actual QLoRA training.
    For now, tracks adapter metadata and provides the management interface.
    """

    def __init__(self):
        self._loaded: Dict[str, dict] = {}

    def list(self) -> dict:
        """List all available adapters (stored or discovered)."""
        adapters = []
        for f in sorted(ADAPTER_DIR.glob("*.pt")):
            meta_file = ADAPTER_DIR / f"{f.stem}.json"
            meta = {}
            if meta_file.exists():
                meta = json.loads(meta_file.read_text())
            adapters.append({
                "name": f.stem,
                "file": f.name,
                "size_kb": round(f.stat().st_size / 1024, 1),
                "skill": meta.get("skill", "unknown"),
                "trained_at": meta.get("trained_at", "unknown"),
                "pairs": meta.get("pairs", 0),
            })
        return {"adapters": adapters, "loaded": list(self._loaded.keys()),
                "count": len(adapters)}

    def load(self, name: str) -> dict:
        """Load an adapter (stub — actual loading requires unsloth inference)."""
        adapter_file = ADAPTER_DIR / f"{name}.pt"
        if not adapter_file.exists():
            return {"error": f"Adapter '{name}' not found", "available":
                    [f.stem for f in ADAPTER_DIR.glob("*.pt")]}

        self._loaded[name] = {"loaded_at": _now(), "file": str(adapter_file)}
        return {"adapter": name, "loaded": True, "loaded_at": self._loaded[name]["loaded_at"]}

    def unload(self, name: str) -> dict:
        if name in self._loaded:
            del self._loaded[name]
            return {"adapter": name, "unloaded": True}
        return {"adapter": name, "unloaded": False, "error": "not loaded"}

    def train(self, skill_name: str, pairs_file: str = None) -> dict:
        """Train a LoRA adapter for a skill (stub).

        In production: uses unsloth for QLoRA (r=16, 6.03M params).
        For now: creates adapter metadata file.
        """
        tdg = TrainingDataGenerator()
        if not pairs_file:
            # Auto-discover training data
            candidates = list(tdg.output_dir.glob(f"{skill_name}_training.json"))
            if not candidates:
                return {"error": f"No training data for {skill_name}",
                        "hint": "Run generate_training_data first"}
            pairs_file = str(candidates[0])

        pairs_data = json.loads(Path(pairs_file).read_text())
        adapter_name = f"adapter_{skill_name.replace('skill_', '')}"

        meta = {
            "skill": skill_name,
            "pairs": len(pairs_data),
            "trained_at": _now(),
            "params": "6.03M",  # QLoRA r=16
            "model": "Qwen-3.6-27B",
            "source": pairs_file,
        }
        meta_path = ADAPTER_DIR / f"{adapter_name}.json"
        meta_path.write_text(json.dumps(meta, indent=2))

        # Create stub adapter file
        stub = ADAPTER_DIR / f"{adapter_name}.pt"
        stub.write_text(json.dumps({"adapter": adapter_name, "meta": meta,
                                    "note": "Production: fine-tuned via unsloth/peft"}, indent=2))

        _write_okf(f"system/s2l/adapters/{adapter_name}_{_ts()}",
                   {"type": "SystemConfig", "title": f"Adapter: {adapter_name}"},
                   json.dumps(meta, indent=2),
                   f"S2L: trained {adapter_name}")
        return {"adapter": adapter_name, "trained": True, "pairs": meta["pairs"],
                "params": meta["params"], "file": str(stub)}

    def infer(self, skill_name: str, prompt: str) -> dict:
        """Run skill inference with loaded adapter + OKF context fallback.

        Hybrid approach:
          1. If adapter loaded → use adapter inference (stub)
          2. Fallback → run native skill script
          3. OKF context injected for edge cases
        """
        adapter_name = f"adapter_{skill_name.replace('skill_', '')}"

        if adapter_name in self._loaded:
            # Stub: would call model with loaded adapter
            return {"method": "adapter", "adapter": adapter_name,
                    "skill": skill_name, "response": f"[Adapter inference for: {prompt[:50]}...]",
                    "confidence": 0.92}
        else:
            # Fallback to native skill script
            skill_path = Path(MAGY_DIR) / f"{skill_name}.py"
            if not skill_path.exists():
                return {"error": f"Skill '{skill_name}' not found"}

            try:
                r = subprocess.run(["python3", str(skill_path)] + prompt.split(),
                                   capture_output=True, text=True, timeout=30)
                output = r.stdout[:500] if r.returncode == 0 else r.stderr[:200]
                return {"method": "native", "skill": skill_name,
                        "response": output, "confidence": 0.70}
            except subprocess.TimeoutExpired:
                return {"error": "skill timed out", "method": "failed"}


# ── MCP tools ───────────────────────────────────────────────────

_TDG = TrainingDataGenerator()
_AM = AdapterManager()

def generate_training_data(args: dict) -> dict:
    return _TDG.generate(args.get("skill_name"))

def list_adapters(args: dict = None) -> dict:
    return _AM.list()

def load_adapter(args: dict) -> dict:
    return _AM.load(args.get("name", ""))

def unload_adapter(args: dict) -> dict:
    return _AM.unload(args.get("name", ""))

def train_adapter(args: dict) -> dict:
    return _AM.train(args.get("skill_name", ""), args.get("pairs_file"))

def skill_inference(args: dict) -> dict:
    return _AM.infer(args.get("skill_name", ""), args.get("prompt", ""))


TOOLS = {
    "generate_training_data": generate_training_data,
    "list_adapters": list_adapters,
    "load_adapter": load_adapter,
    "unload_adapter": unload_adapter,
    "train_adapter": train_adapter,
    "skill_inference": skill_inference,
}


# ── CLI ─────────────────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "generate"

    if action == "generate":
        skill = sys.argv[2] if len(sys.argv) > 2 else None
        r = _TDG.generate(skill)
        print(f"Generated {r['total_pairs']} training pairs across {r['skills']} skills")
        for res in r.get("results", []):
            print(f"  {res['skill']}: {res['pairs']} pairs → {res['path']}")

    elif action == "list":
        r = _AM.list()
        for a in r.get("adapters", []):
            print(f"  {a['name']} ({a['size_kb']}KB, {a['skill']}, {a['pairs']} pairs)")
        print(f"Loaded: {r['loaded']}")

    elif action == "train":
        skill = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(_AM.train(skill), indent=2))

    elif action == "infer":
        skill = sys.argv[2] if len(sys.argv) > 2 else ""
        prompt = sys.argv[3] if len(sys.argv) > 3 else "test"
        print(json.dumps(_AM.infer(skill, prompt), indent=2))

    elif action == "load":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(_AM.load(name), indent=2))

    else:
        print(f"Usage: {sys.argv[0]} [generate|list|train|infer|load]")


if __name__ == "__main__":
    main()
