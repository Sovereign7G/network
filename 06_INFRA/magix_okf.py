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

# Import SCHEMA.md validator
import sys
_OKF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _OKF_DIR)
from okf_validator import validate as schema_validate, list_types as schema_list_types

# Import Era II embedding pipeline
_EMBEDDER = None
def _get_embedder():
    global _EMBEDDER
    if _EMBEDDER is None:
        try:
            from embedding_pipeline import get_embedder
            _EMBEDDER = get_embedder()
        except Exception:
            pass
    return _EMBEDDER

# ── Configuration ───────────────────────────────────────────────

KNOWLEDGE_ROOT = Path(os.environ.get(
    "OKF_ROOT",
    "/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE"
)).expanduser()

SCHEMA_PATH = KNOWLEDGE_ROOT / "SCHEMA.md"

# (valid types loaded dynamically from SCHEMA.md via okf_validator)


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
    """Validate frontmatter against SCHEMA.md via okf_validator."""
    valid, errors = schema_validate(frontmatter)
    return {"valid": valid, "errors": errors}


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

    # Auto-embed for semantic search (Era II)
    embedder = _get_embedder()
    if embedder:
        try:
            embedder.index_concept(path.strip("/"), frontmatter, body)
        except Exception:
            pass  # Embedding failure is non-fatal

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


# ── MCP tool: semantic_search (Era II) ──────────────────────────

def semantic_search(query: str = "", limit: int = 10) -> dict:
    """Vector-based semantic search over OKF concepts."""
    if not query:
        return {"status": "error", "error": "query is required"}
    embedder = _get_embedder()
    if not embedder:
        # Fallback to grep-based search
        return search_concepts(query)
    try:
        results = embedder.search(query, limit)
        return {"status": "ok", "query": query, "results": results, "count": len(results)}
    except Exception as e:
        # Fallback
        return search_concepts(query)


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
    "semantic_search": lambda args: semantic_search(args.get("query", ""), args.get("limit", 10)),
    "embedding_stats": lambda args: get_embedding_stats(),
}


def get_embedding_stats() -> dict:
    """Get embedding pipeline statistics."""
    embedder = _get_embedder()
    if not embedder:
        return {"status": "error", "error": "Embedding pipeline not available"}
    try:
        return {"status": "ok", "stats": embedder.stats()}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── CLI entry point ─────────────────────────────────────────────

def get_embedding_stats() -> dict:
    """Get embedding pipeline statistics."""
    embedder = _get_embedder()
    if not embedder:
        return {"status": "error", "error": "Embedding pipeline not available"}
    try:
        return {"status": "ok", "stats": embedder.stats()}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── MCP tool registry & schemas ─────────────────────────────────

TOOLS = {
    "serve_concept": lambda args: serve_concept(args.get("path", "")),
    "write_concept": lambda args: write_concept(
        args.get("path", ""), args.get("frontmatter"),
        args.get("body", ""), args.get("commit_message")
    ),
    "list_concepts": lambda args: list_concepts(args.get("prefix", "")),
    "search_concepts": lambda args: search_concepts(args.get("query", "")),
    "validate_concept": lambda args: validate_concept_path(args.get("path", "")),
    "semantic_search": lambda args: semantic_search(args.get("query", ""), args.get("limit", 10)),
    "embedding_stats": lambda args: get_embedding_stats(),
    "spawn_hermes_subagent": lambda args: spawn_hermes_subagent(args.get("concept_path", ""), args.get("prompt", "")),
}

MCP_TOOLS_SCHEMA = [
    {
        "name": "serve_concept",
        "description": "Read an OKF concept from 00_KNOWLEDGE. Returns metadata, body, and child concepts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the concept directory (e.g., 'research/topic')"}
            }
        }
    },
    {
        "name": "write_concept",
        "description": "Write or update an OKF concept index.md under 00_KNOWLEDGE. Validates SCHEMA.md constraints.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the concept directory"},
                "frontmatter": {"type": "object", "description": "Key-value metadata dictionary complying with SCHEMA.md"},
                "body": {"type": "string", "description": "Body content of the concept"},
                "commit_message": {"type": "string", "description": "Optional custom git commit message"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_concepts",
        "description": "Browse the OKF bundle structure by listing concepts under a prefix path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prefix": {"type": "string", "description": "Optional subdirectory prefix to list under"}
            }
        }
    },
    {
        "name": "search_concepts",
        "description": "Full-text search query across all OKF concepts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "validate_concept",
        "description": "Validate a concept's metadata frontmatter against SCHEMA.md rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the concept"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "spawn_hermes_subagent",
        "description": "Spawn a Hermes subagent to act on the specified OKF concept with a prompt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept_path": {"type": "string", "description": "OKF concept path to target"},
                "prompt": {"type": "string", "description": "Task prompt for the subagent"}
            },
            "required": ["concept_path", "prompt"]
        }
    }
]


# ── FastAPI Server ──────────────────────────────────────────────

try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(title="Magix OKF MCP Server", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class ToolCallRequest(BaseModel):
        name: str
        arguments: dict = {}

    @app.get("/health")
    @app.get("/api/mcp/health")
    def health():
        return {"status": "HEALTHY", "time": datetime.utcnow().isoformat() + "Z", "root": str(KNOWLEDGE_ROOT)}

    @app.post("/tools/call")
    @app.post("/api/mcp/tools/call")
    def api_tool_call(req: ToolCallRequest):
        handler = TOOLS.get(req.name)
        if not handler:
            return {"status": "error", "error": f"Unknown tool: {req.name}"}
        try:
            return handler(req.arguments)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @app.post("/tools/list")
    @app.get("/tools/list")
    @app.post("/api/mcp/tools/list")
    @app.get("/api/mcp/tools/list")
    def api_tools_list():
        return {"tools": MCP_TOOLS_SCHEMA}

except ImportError:
    app = None


# ── Stdio JSON-RPC Loop ──────────────────────────────────────────

def stdio_loop():
    """Stdio JSON-RPC loop for native MCP clients (like Zed or VSCode)."""
    print("[magix-okf] Starting stdio MCP server loop...", file=sys.stderr, flush=True)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        method = request.get("method", "")
        req_id = request.get("id")
        params = request.get("params", {})
        
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "magix-okf-server",
                        "version": "1.0.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        elif method == "notifications/initialized":
            print("[magix-okf] Client initialized.", file=sys.stderr, flush=True)
            
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": MCP_TOOLS_SCHEMA
                }
            }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            
            try:
                handler = TOOLS.get(tool_name)
                if not handler:
                    res = {"status": "error", "error": f"Unknown tool: {tool_name}"}
                else:
                    res = handler(arguments)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: {e}"}],
                        "isError": True
                    }
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        elif req_id is not None:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


# ── CLI entry point ─────────────────────────────────────────────

def main():
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "serve_concept"):
        stdio_loop()
        sys.exit(0)

    action = sys.argv[1] if len(sys.argv) > 1 else "help"

    if action in ("run-server", "serve", "server"):
        if app is None:
            print("Error: fastapi/pydantic not installed.", file=sys.stderr)
            sys.exit(1)
        import uvicorn
        print("🚀 Igniting Magix OKF Server on port 9000...")
        uvicorn.run(app, host="127.0.0.1", port=9000)
        sys.exit(0)

    if action in ("-h", "--help", "help"):
        print("Usage: python3 -m magix.okf <action> [json_args]")
        print("")
        print("Actions:")
        for name in TOOLS:
            print(f"  {name}")
        print("  run-server")
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
