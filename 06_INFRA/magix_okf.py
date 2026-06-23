#!/usr/bin/env python3
"""
magix/okf/__init__.py — Unified OKF module for magix MCP toolset.

Merges okf_bridge.py + kiro_mcp.py into one canonical interface.
All OKF interactions go through this single module.
Serves: serve_concept, write_concept, list_concepts on port 9002.
"""

import json, os, sys, yaml, re, subprocess
from pathlib import Path
from datetime import datetime

# Import SCHEMA.md validator
import sys
_OKF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _OKF_DIR)
from okf_validator import validate as schema_validate, list_types as schema_list_types

# Import S2L Pipeline
try:
    import s2l_pipeline
except ImportError:
    s2l_pipeline = None

# Import Era VI Gateway
try:
    from external_gateway import Gateway
    external_gateway = Gateway()
except ImportError:
    external_gateway = None

# Import Antigravity Benchmark
try:
    import antigravity_benchmark
except ImportError:
    antigravity_benchmark = None

quantum_reasoning = None
quantum_security = None
quantum_learning = None
keccak_integration = None
distributed_consciousness = None

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


def spawn_hermes_subagent(concept_path: str, prompt: str) -> dict:
    """Spawn a Hermes subagent in the background targeting an OKF concept path."""
    target_dir = KNOWLEDGE_ROOT / concept_path.strip("/")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = target_dir / "subagent_run.log"
    cmd = [
        "/home/cherry/.local/bin/hermes",
        "chat",
        "-q", prompt,
        "--yolo",
        "--accept-hooks"
    ]
    
    try:
        # Open log file for stdout and stderr
        log_fh = open(log_file, "w", encoding="utf-8")
        
        # Start background subprocess
        process = subprocess.Popen(
            cmd,
            cwd=target_dir,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            start_new_session=True  # Detach process group
        )
        
        try:
            rel_log = str(log_file.relative_to(KNOWLEDGE_ROOT))
        except ValueError:
            rel_log = str(log_file)
            
        return {
            "status": "ok",
            "concept_path": concept_path,
            "pid": process.pid,
            "log_path": rel_log,
            "command": " ".join(cmd),
            "message": f"Hermes subagent spawned successfully in background (PID: {process.pid}). Log: {log_file.name}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# Import Quantum Modules & Apply Keccak Hotfix
try:
    import quantum_reasoning
    import quantum_security
    import quantum_learning
    import keccak_integration
    # Apply hotfix patches automatically on startup
    keccak_integration.patch_all()
    print("[magix-okf] Era X Quantum Intelligence loaded & Keccak-256 hotfix applied.", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[magix-okf] Warning: Failed to load Era X modules or apply Keccak-256 hotfix: {e}", file=sys.stderr, flush=True)

# Import Era XI Distributed Consciousness
try:
    import distributed_consciousness
    print("[magix-okf] Era XI Distributed Consciousness loaded.", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[magix-okf] Warning: Failed to load Era XI distributed consciousness: {e}", file=sys.stderr, flush=True)


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
    "generate_training_data": lambda args: s2l_pipeline.generate_training_data(args.get("concept_path", "")) if s2l_pipeline else {"status": "error", "error": "s2l_pipeline not imported"},
    "train_adapter": lambda args: s2l_pipeline.train_adapter(args.get("skill_name", "")) if s2l_pipeline else {"status": "error", "error": "s2l_pipeline not imported"},
    "load_adapter": lambda args: s2l_pipeline.load_adapter(args.get("skill_name", "")) if s2l_pipeline else {"status": "error", "error": "s2l_pipeline not imported"},
    "skill_inference": lambda args: s2l_pipeline.skill_inference(args.get("skill_name", ""), args.get("prompt", ""), args.get("threshold", 0.85)) if s2l_pipeline else {"status": "error", "error": "s2l_pipeline not imported"},
    "adapter_status": lambda args: s2l_pipeline.adapter_status() if s2l_pipeline else {"status": "error", "error": "s2l_pipeline not imported"},
    "external_infer": lambda args: external_gateway.infer(args.get("provider", "deepseek"), args.get("prompt", ""), args.get("skill", ""), 1024, args.get("bypass_cache", False)) if external_gateway else {"status": "error", "error": "external_gateway not imported"},
    "gateway_health": lambda args: external_gateway.health() if external_gateway else {"status": "error", "error": "external_gateway not imported"},
    "gateway_policy": lambda args: external_gateway.update_policy(args.get("new_policy")) if args.get("new_policy") is not None else (external_gateway.get_policy() if external_gateway else {"status": "error", "error": "external_gateway not imported"}),
    "gateway_audit": lambda args: external_gateway.get_audit_logs(args.get("limit", 20)) if external_gateway else {"status": "error", "error": "external_gateway not imported"},
    "run_benchmark": lambda args: antigravity_benchmark.run_benchmark() if antigravity_benchmark else {"status": "error", "error": "antigravity_benchmark not imported"},
    "benchmark_status": lambda args: antigravity_benchmark.benchmark_status() if antigravity_benchmark else {"status": "error", "error": "antigravity_benchmark not imported"},
    "quantum_embed": lambda args: quantum_reasoning.quantum_embed(args.get("concept_path", "")) if quantum_reasoning else {"status": "error", "error": "quantum_reasoning not imported"},
    "quantum_entangle": lambda args: quantum_reasoning.quantum_entangle(args.get("concept_paths", [])) if quantum_reasoning else {"status": "error", "error": "quantum_reasoning not imported"},
    "quantum_search": lambda args: quantum_reasoning.quantum_search(args.get("query", ""), args.get("limit", 10)) if quantum_reasoning else {"status": "error", "error": "quantum_reasoning not imported"},
    "quantum_reason": lambda args: quantum_reasoning.quantum_reason(args.get("problem", ""), args.get("concepts", [])) if quantum_reasoning else {"status": "error", "error": "quantum_reasoning not imported"},
    "qkd_generate_key": lambda args: quantum_security.qkd_generate_key(args.get("key_id", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "qkd_distribute": lambda args: quantum_security.qkd_distribute(args.get("sender", ""), args.get("receiver", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "qkd_sign": lambda args: quantum_security.qkd_sign(args.get("data", ""), args.get("key_id", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "qkd_verify": lambda args: quantum_security.qkd_verify(args.get("data", ""), args.get("signature", ""), args.get("key_id", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "qkd_encrypt": lambda args: quantum_security.qkd_encrypt(args.get("data", ""), args.get("public_key", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "qkd_decrypt": lambda args: quantum_security.qkd_decrypt(args.get("encrypted_data", ""), args.get("private_key", "")) if quantum_security else {"status": "error", "error": "quantum_security not imported"},
    "ql_reinforce": lambda args: quantum_learning.ql_reinforce(args.get("skill", ""), args.get("state", ""), args.get("action", ""), args.get("reward", 0.0), args.get("next_state", "")) if quantum_learning else {"status": "error", "error": "quantum_learning not imported"},
    "ql_generate": lambda args: quantum_learning.ql_generate(args.get("context", ""), args.get("max_length", 500)) if quantum_learning else {"status": "error", "error": "quantum_learning not imported"},
    "ql_optimize": lambda args: quantum_learning.ql_optimize(args.get("problem", {})) if quantum_learning else {"status": "error", "error": "quantum_learning not imported"},
    "keccak_hash": lambda args: keccak_integration.keccak_hash(args.get("data", "")) if keccak_integration else {"status": "error", "error": "keccak_integration not imported"},
    "keccak_patch_status": lambda args: keccak_integration.keccak_patch_status() if keccak_integration else {"status": "error", "error": "keccak_integration not imported"},
    "keccak_verify_hash": lambda args: keccak_integration.keccak_verify_hash(args.get("data", ""), args.get("hash_hex", "")) if keccak_integration else {"status": "error", "error": "keccak_integration not imported"},
    "bci_decode_intent": lambda args: distributed_consciousness.bci_decode_intent(args.get("raw_eeg")) if distributed_consciousness else {"status": "error", "error": "distributed_consciousness not imported"},
    "dao_legal_status": lambda args: distributed_consciousness.dao_legal_status() if distributed_consciousness else {"status": "error", "error": "distributed_consciousness not imported"},
    "interstellar_consensus_vote": lambda args: distributed_consciousness.interstellar_consensus_vote(args.get("proposal", "")) if distributed_consciousness else {"status": "error", "error": "distributed_consciousness not imported"},
    "calculate_consciousness_phi": lambda args: distributed_consciousness.calculate_consciousness_phi() if distributed_consciousness else {"status": "error", "error": "distributed_consciousness not imported"},
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
    },
    {
        "name": "generate_training_data",
        "description": "Extract concepts and format training data for S2L fine-tuning.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept_path": {"type": "string", "description": "Optional relative path to subset concepts"}
            }
        }
    },
    {
        "name": "train_adapter",
        "description": "Fine-tune a skill adapter via QLoRA simulation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {"type": "string", "description": "Name of the skill to train (research, email, document, compare, calendar, notes)"}
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "load_adapter",
        "description": "Load a pre-trained LoRA adapter into active memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {"type": "string", "description": "Name of the skill adapter to load"}
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "skill_inference",
        "description": "Execute a skill under the parametric adapter or fallback to in-context prompting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {"type": "string", "description": "Name of the skill to execute"},
                "prompt": {"type": "string", "description": "Operational task prompt"},
                "threshold": {"type": "number", "description": "Fallback confidence threshold (default 0.85)"}
            },
            "required": ["skill_name", "prompt"]
        }
    },
    {
        "name": "adapter_status",
        "description": "Retrieve status of all trained and loaded S2L adapters.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "external_infer",
        "description": "Send a sanitized prompt to DeepSeek, Kimi, or TextCortex EU gateway.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {"type": "string", "description": "The target model provider (deepseek, kimi, textcortex)"},
                "prompt": {"type": "string", "description": "The input task query prompt to execute"},
                "skill": {"type": "string", "description": "Optional skill name category"},
                "bypass_cache": {"type": "boolean", "description": "Bypass the local similarity query cache"}
            },
            "required": ["provider", "prompt"]
        }
    },
    {
        "name": "gateway_health",
        "description": "Check the health and connection status of the Zero-Trust Privacy Gateway.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "gateway_policy",
        "description": "Get or update routing and region policy configurations for the Privacy Gateway.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "new_policy": {
                    "type": "object",
                    "description": "Optional updated policy properties"
                }
            }
        }
    },
    {
        "name": "gateway_audit",
        "description": "Retrieve audit log event entries for tracking requests and responses.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "number", "description": "Maximum number of audit events to return (default 20)"}
            }
        }
    },
    {
        "name": "run_benchmark",
        "description": "Execute the complete Antigravity benchmark suite to measure latency, cache hits, and token savings.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "benchmark_status",
        "description": "Retrieve status of historical Antigravity benchmarks and run metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "quantum_embed",
        "description": "Create quantum embedding for a concept.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept_path": {"type": "string", "description": "Relative path to concept"}
            },
            "required": ["concept_path"]
        }
    },
    {
        "name": "quantum_entangle",
        "description": "Entangle multiple concepts into a superposition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Paths to concepts to entangle"
                }
            },
            "required": ["concept_paths"]
        }
    },
    {
        "name": "quantum_search",
        "description": "Quantum-inspired semantic search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results to return"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "quantum_reason",
        "description": "Quantum-inspired reasoning.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "problem": {"type": "string", "description": "Reasoning problem description"},
                "concepts": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Concepts to base reasoning on"
                }
            },
            "required": ["problem", "concepts"]
        }
    },
    {
        "name": "qkd_generate_key",
        "description": "Generate a quantum-resistant key pair.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key_id": {"type": "string", "description": "ID of key to generate"}
            },
            "required": ["key_id"]
        }
    },
    {
        "name": "qkd_distribute",
        "description": "Simulate quantum key distribution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sender": {"type": "string", "description": "Sender identifier"},
                "receiver": {"type": "string", "description": "Receiver identifier"}
            },
            "required": ["sender", "receiver"]
        }
    },
    {
        "name": "qkd_sign",
        "description": "Create a quantum-resistant signature.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Data to sign"},
                "key_id": {"type": "string", "description": "Key ID to use for signing"}
            },
            "required": ["data", "key_id"]
        }
    },
    {
        "name": "qkd_verify",
        "description": "Verify a quantum-resistant signature.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Original data"},
                "signature": {"type": "string", "description": "Base64 signature string"},
                "key_id": {"type": "string", "description": "Key ID used for signing"}
            },
            "required": ["data", "signature", "key_id"]
        }
    },
    {
        "name": "qkd_encrypt",
        "description": "Encrypt data using post-quantum cryptography.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Data to encrypt"},
                "public_key": {"type": "string", "description": "Base64 public key"}
            },
            "required": ["data", "public_key"]
        }
    },
    {
        "name": "qkd_decrypt",
        "description": "Decrypt data using post-quantum cryptography.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "encrypted_data": {"type": "string", "description": "Base64 encrypted string"},
                "private_key": {"type": "string", "description": "Base64 private key"}
            },
            "required": ["encrypted_data", "private_key"]
        }
    },
    {
        "name": "ql_reinforce",
        "description": "Quantum-enhanced Q-learning step.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill": {"type": "string", "description": "Name of skill being learned"},
                "state": {"type": "string", "description": "Current state"},
                "action": {"type": "string", "description": "Action taken"},
                "reward": {"type": "number", "description": "Reward value"},
                "next_state": {"type": "string", "description": "resulting next state"}
            },
            "required": ["skill", "state", "action", "reward", "next_state"]
        }
    },
    {
        "name": "ql_generate",
        "description": "Generate content using quantum-inspired generative model.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "context": {"type": "string", "description": "Starting text context"},
                "max_length": {"type": "integer", "description": "Max length of generated text"}
            },
            "required": ["context"]
        }
    },
    {
        "name": "ql_optimize",
        "description": "Optimize a problem using quantum-inspired annealing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "problem": {
                    "type": "object",
                    "description": "Problem properties containing variables and iterations"
                }
            },
            "required": ["problem"]
        }
    },
    {
        "name": "keccak_hash",
        "description": "Compute Keccak-256 hash of data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Data to hash"}
            },
            "required": ["data"]
        }
    },
    {
        "name": "keccak_patch_status",
        "description": "Get Keccak-256 patch status.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "keccak_verify_hash",
        "description": "Verify data against Keccak-256 hash.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Original data"},
                "hash_hex": {"type": "string", "description": "Hex hash string to verify"}
            },
            "required": ["data", "hash_hex"]
        }
    },
    {
        "name": "bci_decode_intent",
        "description": "Decode brainwave EEG signals into system intention and log in OKF.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "raw_eeg": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Optional list of float values representing raw brainwave voltage stream."
                }
            }
        }
    },
    {
        "name": "dao_legal_status",
        "description": "Fetch legal sovereignty registry and cert info for the autonomous LLC.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "interstellar_consensus_vote",
        "description": "Execute proposal vote across space nodes and compensate delay lag.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proposal": {"type": "string", "description": "Name or content of proposal to vote on."}
            },
            "required": ["proposal"]
        }
    },
    {
        "name": "calculate_consciousness_phi",
        "description": "Compute IIT system consciousness metric (Phi Φ) for the swarm.",
        "inputSchema": {
            "type": "object",
            "properties": {}
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
        print("🚀 Igniting Magix OKF Server on port 9002...")
        uvicorn.run(app, host="127.0.0.1", port=9002)
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
