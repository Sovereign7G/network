#!/usr/bin/env python3
"""
SCHEMA.md-based validator for OKF concepts.

Parses SCHEMA.md for type definitions, generates JSON Schema,
and validates frontmatter on every write_concept call.
"""

import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_PATH = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE/SCHEMA.md")

# Fallback schemas if SCHEMA.md is unreachable
FALLBACK_SCHEMAS = {
    "KnowledgeBundle": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "KnowledgeBundle"},
            "title": {"type": "string"},
            "version": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        }
    },
    "ResearchFinding": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "ResearchFinding"},
            "title": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "updated": {"type": "string"},
        }
    },
    "EmailThread": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "EmailThread"},
            "title": {"type": "string"},
            "status": {"enum": ["new", "triaged", "needs_reply", "replied", "archived", "document_created"]},
            "tags": {"type": "array", "items": {"type": "string"}},
        }
    },
    "EmailDraft": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "EmailDraft"},
            "title": {"type": "string"},
            "status": {"enum": ["draft", "sent", "editing"]},
            "version": {"type": "integer"},
        }
    },
    "Document": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "Document"},
            "title": {"type": "string"},
            "status": {"enum": ["draft", "review", "approved", "archived"]},
            "author": {"type": "string"},
            "version": {"type": "integer"},
            "related_email": {"type": "string"},
        }
    },
    "ModelComparison": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "ModelComparison"},
            "title": {"type": "string"},
            "winner": {"enum": ["A", "B", "tie"]},
            "model_a": {"type": "string"},
            "model_b": {"type": "string"},
            "duration_ms": {"type": "integer"},
        }
    },
    "Note": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "Note"},
            "title": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        }
    },
    "TelemetryReport": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "TelemetryReport"},
            "title": {"type": "string"},
            "source": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        }
    },
    "SystemConfig": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "SystemConfig"},
            "title": {"type": "string"},
            "version": {"type": "string"},
        }
    },
    "ChatSession": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "ChatSession"},
            "title": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        }
    },
    "CalendarEvent": {
        "type": "object",
        "required": ["type", "title", "date", "status"],
        "properties": {
            "type": {"const": "CalendarEvent"},
            "title": {"type": "string"},
            "date": {"type": "string"},
            "status": {"enum": ["scheduled", "completed", "cancelled"]},
            "updated": {"type": "string"},
        }
    },
    "AntigravityBenchmark": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "AntigravityBenchmark"},
            "title": {"type": "string"},
        }
    },
    "QuantumEntanglement": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "QuantumEntanglement"},
            "title": {"type": "string"},
        }
    },
    "QuantumKeyDistribution": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "QuantumKeyDistribution"},
            "title": {"type": "string"},
        }
    },
    "QuantumLearning": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "QuantumLearning"},
            "title": {"type": "string"},
        }
    },
    "QuantumGenerated": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "QuantumGenerated"},
            "title": {"type": "string"},
        }
    },
    "QuantumOptimization": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "QuantumOptimization"},
            "title": {"type": "string"},
        }
    },
    "KeccakPatch": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "KeccakPatch"},
            "title": {"type": "string"},
        }
    },
    "NeuralCommand": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "NeuralCommand"},
            "title": {"type": "string"},
        }
    },
    "DAOSovereignty": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "DAOSovereignty"},
            "title": {"type": "string"},
        }
    },
    "InterstellarVote": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "InterstellarVote"},
            "title": {"type": "string"},
        }
    },
    "ConsciousState": {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": "ConsciousState"},
            "title": {"type": "string"},
        }
    },
}


def load_schemas() -> Dict[str, dict]:
    """Parse SCHEMA.md and extract YAML frontmatter schemas."""
    if not SCHEMA_PATH.exists():
        return FALLBACK_SCHEMAS

    content = SCHEMA_PATH.read_text(encoding="utf-8")

    # Extract YAML blocks delimited by ---
    schemas = {}
    blocks = re.split(r'^\s*---\s*$', content, flags=re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict) and data.get("type"):
                type_name = data["type"]
                schemas[type_name] = data
        except yaml.YAMLError:
            continue

    return schemas if schemas else FALLBACK_SCHEMAS


def get_schema_for_type(type_name: str) -> Optional[dict]:
    """Get JSON Schema constraints for a type."""
    schemas = load_schemas()
    raw = schemas.get(type_name)
    if not raw:
        return None

    # Build JSON Schema from the schema definition
    schema = {
        "type": "object",
        "required": ["type", "title"],
        "properties": {
            "type": {"const": type_name},
            "title": {"type": "string"},
        }
    }

    # Add optional fields
    for field in ["tags", "source", "version", "author", "model_a", "model_b",
                  "winner", "status", "priority", "duration_ms", "related_email"]:
        if field in raw:
            schema["properties"][field] = _infer_type(raw[field])

    return schema


def _infer_type(value: Any) -> dict:
    """Infer JSON Schema type from a Python value."""
    if isinstance(value, list):
        return {"type": "array", "items": {"type": "string"}} if not value else {"type": "array"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, dict):
        return {"type": "object"}
    return {"type": "string"}


def validate(frontmatter: dict) -> Tuple[bool, List[str]]:
    """Validate frontmatter against SCHEMA.md type schema.

    Returns (is_valid, list_of_error_messages).
    """
    errors = []
    type_name = frontmatter.get("type")

    if not type_name:
        return False, ["Missing required field: type"]

    # Check type is registered
    schemas = load_schemas()
    if type_name not in schemas:
        valid = ", ".join(sorted(schemas.keys()))
        return False, [f"Unknown type '{type_name}'. Valid types: {valid}"]

    # Check required fields from schema definition
    raw = schemas[type_name]
    raw_required = raw.get("required", [])
    for field in ["type", "title"]:
        if field in raw_required and field not in frontmatter:
            errors.append(f"Missing required field '{field}' for type '{type_name}'")

    # Check enum constraints
    enum_fields = {"status": ["new", "triaged", "needs_reply", "replied", "archived",
                              "document_created", "draft", "sent", "editing",
                              "review", "approved", "scheduled", "completed", "cancelled"],
                   "winner": ["A", "B", "tie"],
                   "priority": ["low", "medium", "high", "urgent"]}
    # Also merge per-schema status enums into the master list
    for type_name, schema in schemas.items():
        raw_status = schema.get("status")
        if isinstance(raw_status, str) and "|" in raw_status:
            for s in raw_status.split("|"):
                s = s.strip()
                if s and s not in enum_fields["status"]:
                    enum_fields["status"].append(s)
    for field, valid_values in enum_fields.items():
        if field in frontmatter and frontmatter[field] not in valid_values:
            errors.append(f"Invalid '{field}': '{frontmatter[field]}'. Valid: {valid_values}")

    return len(errors) == 0, errors


def list_types() -> Dict[str, List[str]]:
    """List all registered types with their required fields."""
    schemas = load_schemas()
    result = {}
    for name, schema in schemas.items():
        result[name] = {
            "required": schema.get("required", ["type", "title"]),
            "fields": [k for k in schema.keys() if k not in ("type", "required")],
        }
    return result


# ── CLI ─────────────────────────────────────────────────────────

def main():
    import sys, json
    action = sys.argv[1] if len(sys.argv) > 1 else "list"

    if action == "validate":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        target = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC/00_KNOWLEDGE") / path.strip("/") / "index.md"
        if not target.exists():
            print(json.dumps({"status": "not_found"}))
            sys.exit(0)
        import okf_bridge
        fm, _ = okf_bridge.parse_okf(target.read_text())
        valid, errors = validate(fm)
        print(json.dumps({"valid": valid, "errors": errors}, indent=2))

    elif action == "list":
        types = list_types()
        print(f"Registered types ({len(types)}):")
        for name, info in sorted(types.items()):
            print(f"  {name}: required={info['required']}, fields={info['fields']}")

    elif action == "schemas":
        schemas = load_schemas()
        for name, schema in sorted(schemas.items()):
            print(f"---\n# {name}")
            print(yaml.dump(schema, default_flow_style=False, allow_unicode=True).strip())
            print()

    else:
        print(f"Unknown: {action}")


if __name__ == "__main__":
    main()
