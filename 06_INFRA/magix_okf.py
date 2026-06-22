#!/usr/bin/env python3
"""
magix/okf/__init__.py — Unified OKF module for magix MCP toolset.

Merges okf_bridge.py + kiro_mcp.py into one canonical interface.
All OKF interactions go through this single module.
Serves: serve_concept, write_concept, list_concepts on port 9000.
"""

import json, os, sys, yaml, re, subprocess
from pathlib import Path
from datetime import datetime

# ── Configuration ───────────────────────────────────────────────

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()

SCHEMA_PATH = KNOWLEDGE_ROOT / "SCHEMA.md"
VALID_TYPES = [
    "KnowledgeBundle", "TelemetryReport", "ResearchFinding",
    "ModelComparison", "EmailThread", "EmailDraft", "Document",
    "SystemConfig", "ChatSession", "Note"
]


# ── OKF parsing ─────────────────────────────────────────────────

def parse_okf(text: str) -> tuple:
    """Parse OKF file into (frontmatter_dict, body_string)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}
    body = parts[2].strip()
    return frontmatter, body


def render_okf(frontmatter: dict, body: str) -> str:
    """Render OKF file from frontmatter dict + body string."""
    fm = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()
    return f"---\n{fm}\n---\n\n{body.strip()}\n"


# ── Schema validation ───────────────────────────────────────────

def validate_concept(frontmatter: dict) -> dict:
    """Validate frontmatter against SCHEMA.md requirements."""
    errors = []
    if not frontmatter.get("type"):
        errors.append("Missing required field: type")
    elif frontmatter["type"] not in VALID_TYPES:
        errors.append(f"Invalid type '{frontmatter['type']}'. Must be one of: {', '.join(VALID_TYPES)}")

    if not frontmatter.get("title"):
        errors.append("Missing required field: title (will be auto-set)")

    result = {"valid": len(errors) == 0, "errors": errors}
    return result


# ── Path utilities ──────────────────────────────────────────────

def list_children(dir_path: Path) -> list:
    """List subdirectories that have an index.md (OKF concepts)."""
    if not dir_path.exists():
        return []
    children = []
    for entry in sorted(dir_path.iterdir()):
        if entry.is_dir() and (entry / "index.md").exists():
            fm, _ = parse_okf((entry / "index.md").read_text())
            children.append({
                "path": str(entry.relative_to(KNOWLEDGE_ROOT)),
                "type": fm.get("type", "unknown"),
                "title": fm.get("title", entry.name),
            })
    return children


# ── Git sync ────────────────────────────────────────────────────

def git_commit(paths: list, message: str):
    """Auto-commit changed OKF files to git."""
    repo_root = KNOWLEDGE_ROOT.parent
    try:
        subprocess.run(["git", "add", "--"] + paths, cwd=repo_root, capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "--allow-empty", "--no-verify", "-m", message],
                       cwd=repo_root, capture_output=True, timeout=10)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


# ── MCP tool: serve_concept ─────────────────────────────────────

def serve_concept(path: str = "") -> dict:
    """Read an OKF concept. Progressive: returns index.md + children."""
    target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
    if not target.exists():
        return {"status": "not_found", "path": path, "available": list_children(KNOWLEDGE_ROOT / path.strip("/"))}

    try:
        content = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {"status": "error", "error": f"Cannot read {target}"}

    frontmatter, body = parse_okf(content)
    return {
        "status": "ok", "path": path,
        "type": frontmatter.get("type", "unknown"),
        "title": frontmatter.get("title", path.split("/")[-1] if path else "root"),
        "tags": frontmatter.get("tags", []),
        "updated": frontmatter.get("updated", None),
        "body": body[:2000],
        "body_full_length": len(body),
        "children": list_children(target.parent),
    }


# ── MCP tool: write_concept ─────────────────────────────────────

def write_concept(path: str = "", frontmatter: dict = None,
                  body: str = "", commit_message: str = None) -> dict:
    """Write an OKF concept. Validates schema, auto-commits to git."""
    if not path:
        return {"status": "error", "error": "path is required"}

    frontmatter = frontmatter or {}

    # Auto-set title from path if missing
    if not frontmatter.get("title"):
        frontmatter["title"] = path.rsplit("/", 1)[-1]

    # Schema validation
    validation = validate_concept(frontmatter)
    if not validation["valid"]:
        return {"status": "validation_error", "errors": validation["errors"]}

    # Auto-add timestamp
    frontmatter["updated"] = datetime.utcnow().isoformat() + "Z"

    target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    content = render_okf(frontmatter, body)
    try:
        target.write_text(content, encoding="utf-8")
    except OSError as e:
        return {"status": "error", "error": str(e)}

    # Auto-commit
    msg = commit_message or f"Write concept: {path}"
    git_commit([str(target)], msg)

    return {"status": "ok", "path": path, "written": True, "commit_message": msg}


# ── MCP tool: list_concepts ─────────────────────────────────────

def list_concepts(prefix: str = "") -> dict:
    """List OKF concepts under a prefix, grouped by type."""
    root = KNOWLEDGE_ROOT / prefix.strip("/") if prefix else KNOWLEDGE_ROOT
    if not root.exists():
        return {"status": "ok", "concepts": [], "count": 0}

    concepts = []
    for entry in sorted(root.rglob("index.md")):
        rel = str(entry.parent.relative_to(KNOWLEDGE_ROOT))
        fm, _ = parse_okf(entry.read_text())
        concepts.append({
            "path": rel,
            "type": fm.get("type", "unknown"),
            "title": fm.get("title", entry.parent.name),
        })

    return {"status": "ok", "prefix": prefix or "/", "concepts": concepts, "count": len(concepts)}


# ── MCP tool: search_concepts ───────────────────────────────────

def search_concepts(query: str = "") -> dict:
    """Full-text grep search across all OKF concepts."""
    if not query:
        return {"status": "error", "error": "query is required"}

    results = []
    for entry in sorted(KNOWLEDGE_ROOT.rglob("index.md")):
        content = entry.read_text()
        if query.lower() in content.lower():
            rel = str(entry.parent.relative_to(KNOWLEDGE_ROOT))
            fm, body = parse_okf(content)
            results.append({
                "path": rel,
                "type": fm.get("type", "unknown"),
                "title": fm.get("title", entry.parent.name),
                "snippet": body[:200].replace("\n", " ") if body else "",
            })
            if len(results) >= 20:
                break

    return {"status": "ok", "query": query, "results": results, "count": len(results)}


# ── MCP tool: validate_concept_path ─────────────────────────────

def validate_concept_path(path: str = "") -> dict:
    """Validate an existing concept against SCHEMA.md."""
    target = KNOWLEDGE_ROOT / path.strip("/") / "index.md"
    if not target.exists():
        return {"status": "not_found", "path": path}

    fm, _ = parse_okf(target.read_text())
    validation = validate_concept(fm)
    return {
        "status": "validated" if validation["valid"] else "invalid",
        "path": path,
        "type": fm.get("type"),
        "valid": validation["valid"],
        "errors": validation["errors"],
    }


# ── MCP tool registry ───────────────────────────────────────────

TOOLS = {
    "serve_concept": lambda args: serve_concept(args.get("path", "")),
    "write_concept": lambda args: write_concept(
        args.get("path", ""), args.get("frontmatter"),
        args.get("body", ""), args.get("commit_message")
    ),
    "list_concepts": lambda args: list_concepts(args.get("prefix", "")),
    "search_concepts": lambda args: search_concepts(args.get("query", "")),
    "validate_concept": lambda args: validate_concept_path(args.get("path", "")),
}


# ── CLI entry point ─────────────────────────────────────────────

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "help"

    if action in ("-h", "--help", "help"):
        print("Usage: python3 -m magix.okf <action> [json_args]")
        print("")
        print("Actions:")
        for name in TOOLS:
            print(f"  {name}")
        print("")
        print("Examples:")
        print('  serve_concept \'{"path": ""}\'')
        print('  write_concept \'{"path": "research/topic", "frontmatter": {"type": "ResearchFinding", "title": "Topic"}, "body": "..."}\'')
        print('  list_concepts \'{"prefix": "research"}\'')
        print('  search_concepts \'{"query": "quantum"}\'')
        sys.exit(0)

    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    handler = TOOLS.get(action)
    if not handler:
        print(json.dumps({"status": "error", "error": f"Unknown action: {action}"}))
        sys.exit(1)

    result = handler(args)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
