#!/usr/bin/env python3
"""
P1 — Differential AST Checkpoints
Extends session_restore_optimized.py with progressive restoration.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class DiffCheckpoint:
    def __init__(self, base_path="/tmp/odysseus_checkpoints"):
        self.path = Path(base_path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.initial_ast = {}
        self.last_ast = {}
        self.checkpoints = []
    
    def save_checkpoint(self, current_ast: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = time.time_ns()
        diff = self.generate_diff(self.last_ast, current_ast)
        diff_hash = hashlib.sha256(json.dumps(diff).encode()).hexdigest()
        
        checkpoint = {"timestamp": timestamp, "diff_hash": diff_hash, "diff": diff}
        self.checkpoints.append(checkpoint)
        
        with open(self.path / f"{timestamp}.json", "w") as f:
            json.dump(checkpoint, f)
        
        self.last_ast = current_ast
        return {"checkpoint_id": timestamp, "diff_hash": diff_hash}
    
    def restore(self, timestamp: int) -> Dict[str, Any]:
        ast = self.initial_ast.copy()
        for cp in sorted(self.checkpoints, key=lambda x: x["timestamp"]):
            if cp["timestamp"] <= timestamp:
                ast = self.apply_diff(ast, cp["diff"])
        return ast
    
    def generate_diff(self, old: Dict, new: Dict) -> Dict:
        diff = {}
        for key, value in new.items():
            if key not in old:
                diff[f"+{key}"] = value
            elif old[key] != value:
                diff[f"~{key}"] = {"old": old[key], "new": value}
        for key in old:
            if key not in new:
                diff[f"-{key}"] = old[key]
        return diff
    
    def apply_diff(self, ast: Dict, diff: Dict) -> Dict:
        result = ast.copy()
        for key, value in diff.items():
            if key.startswith("+"):
                result[key[1:]] = value
            elif key.startswith("~"):
                result[key[1:]] = value["new"]
            elif key.startswith("-"):
                result.pop(key[1:], None)
        return result

if __name__ == "__main__":
    print("🔍 P1 — Differential AST Checkpoints")
    print("=" * 40)
    
    dc = DiffCheckpoint()
    
    # Simulate session AST
    ast1 = {"messages": [{"role": "user", "content": "Hello"}], "context": {"user": "test"}}
    ast2 = {"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}], "context": {"user": "test"}}
    
    print("\n📝 Saving checkpoint 1...")
    result1 = dc.save_checkpoint(ast1)
    print(f"   Checkpoint ID: {result1['checkpoint_id']}")
    
    print("\n📝 Saving checkpoint 2...")
    result2 = dc.save_checkpoint(ast2)
    print(f"   Checkpoint ID: {result2['checkpoint_id']}")
    
    print("\n📂 Restoring to checkpoint 1...")
    restored = dc.restore(result1['checkpoint_id'])
    print(f"   Messages: {len(restored.get('messages', []))}")
    
    print("\n✅ P1 — Differential AST Checkpoints complete!")
