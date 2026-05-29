#!/usr/bin/env python3
"""
🏛️ AGE REPUBLIC :: ZETTO PYTHON BRIDGE
========================================
Direct ctypes bridge from Python → libzetto.so (Rust cdylib).

This eliminates the subprocess/HTTP boundary between Python
orchestration and the Rust linker. The existing FastAPI/asyncio
pipeline can call Zetto in-process — zero serialization overhead
beyond the JSON module descriptor (which Zetto parses in Rust).

Usage:
    from zetto_bridge import ZettoBridge

    bridge = ZettoBridge()
    bridge.init()
    bridge.add_module({
        "id": "voice_engine",
        "path": "src/voice.py",
        "source": "def speak(): ...",
        "imports": ["attestation"],
        "exports": ["speak"],
        "trust_boundary": "axon::teles",
        "is_entry": True,
    })
    result = bridge.link()
    print(result["link_time_us"], "µs")
"""

import ctypes
import json
import os
import time
from pathlib import Path
from typing import Any


class ZettoBridge:
    """Zero-overhead Python → Rust bridge for the Zetto sovereign linker.

    Loads libzetto.so via ctypes and exposes the full C-ABI surface:
    - zetto_init()        → reset linker state
    - zetto_add_module()  → push a module (JSON-encoded)
    - zetto_link()        → execute link pipeline, return result
    - zetto_seal()        → compute Keccak-256 seal
    - zetto_version()     → version string
    """

    def __init__(self, lib_path: str | None = None):
        if lib_path is None:
            lib_path = self._find_lib()
        self._lib = ctypes.CDLL(lib_path)
        self._configure_ffi()
        self._version = self.version()
        print(f"🔗 [Zetto Python Bridge] Loaded: {lib_path}")
        print(f"   Version: {self._version}")

    def _find_lib(self) -> str:
        """Locate libzetto.so relative to this file or in standard paths."""
        base = Path(__file__).resolve().parent
        candidates = [
            base / "zetto" / "target" / "release" / "libzetto.so",
            base / "zetto" / "target" / "debug" / "libzetto.so",
            Path.home() / ".local" / "lib" / "libzetto.so",
        ]
        for p in candidates:
            if p.exists():
                return str(p)
        raise FileNotFoundError(
            f"libzetto.so not found. Build with: cd 04_SUBSTRATES/sovereign_trinity/zetto && cargo build --release\n"
            f"Searched: {[str(p) for p in candidates]}"
        )

    def _configure_ffi(self):
        """Set up ctypes argument/return types for all FFI functions."""
        # void zetto_init()
        self._lib.zetto_init.argtypes = []
        self._lib.zetto_init.restype = None

        # int32 zetto_add_module(const char* json)
        self._lib.zetto_add_module.argtypes = [ctypes.c_char_p]
        self._lib.zetto_add_module.restype = ctypes.c_int32

        # char* zetto_link()
        self._lib.zetto_link.argtypes = []
        self._lib.zetto_link.restype = ctypes.c_char_p

        # char* zetto_seal(const char* content)
        self._lib.zetto_seal.argtypes = [ctypes.c_char_p]
        self._lib.zetto_seal.restype = ctypes.c_char_p

        # void zetto_free_string(char* ptr)
        self._lib.zetto_free_string.argtypes = [ctypes.c_char_p]
        self._lib.zetto_free_string.restype = None

        # char* zetto_version()
        self._lib.zetto_version.argtypes = []
        self._lib.zetto_version.restype = ctypes.c_char_p

    def init(self):
        """Reset the linker state. Call before adding modules."""
        self._lib.zetto_init()

    def add_module(self, module: dict) -> bool:
        """Add a sovereign module to the linker graph.

        Args:
            module: Dict with keys: id, path, source, imports, exports,
                    trust_boundary, is_entry

        Returns:
            True on success, False on parse error.
        """
        json_bytes = json.dumps(module).encode("utf-8")
        result = self._lib.zetto_add_module(json_bytes)
        return result == 0

    def link(self) -> dict:
        """Execute the full Zetto link pipeline.

        Returns:
            LinkResult dict with: chunks, total_modules, total_chunks,
            dead_modules_eliminated, link_time_us, module_graph_edges
        """
        result_ptr = self._lib.zetto_link()
        if not result_ptr:
            raise RuntimeError("Zetto link returned null — internal linker error")
        result_json = result_ptr.decode("utf-8")
        # Note: We don't call zetto_free_string here because ctypes
        # copies the string on .decode(). The Rust side will reclaim
        # memory when the thread-local linker is reset.
        return json.loads(result_json)

    def seal(self, content: str) -> str:
        """Compute a Keccak-256 seal for arbitrary content.

        Args:
            content: The string to seal.

        Returns:
            Hex-encoded Keccak-256 hash prefixed with '0x'.
        """
        result_ptr = self._lib.zetto_seal(content.encode("utf-8"))
        if not result_ptr:
            raise RuntimeError("Zetto seal returned null")
        return result_ptr.decode("utf-8")

    def version(self) -> str:
        """Get the Zetto version string."""
        v_ptr = self._lib.zetto_version()
        return v_ptr.decode("utf-8") if v_ptr else "unknown"

    def link_modules(self, modules: list[dict]) -> dict:
        """Convenience: init, add all modules, and link in one call."""
        self.init()
        added = 0
        for mod in modules:
            if self.add_module(mod):
                added += 1
            else:
                print(f"   ⚠️  Failed to add module: {mod.get('id', 'unknown')}")
        return self.link()


# ─────────────────────────────────────────────────────────────
# Integration Test — Validates the Python→Rust bridge works
# ─────────────────────────────────────────────────────────────

def _benchmark():
    """Run a quick integration benchmark comparing Python-native
    attestation vs Zetto Rust-native attestation."""

    bridge = ZettoBridge()

    print("\n" + "=" * 60)
    print("🏛️  ZETTO PYTHON BRIDGE :: Integration Benchmark")
    print("=" * 60)

    # --- Test 1: Module linking ---
    bridge.init()

    modules = []
    # Entry module
    entry_imports = [f"mod_{i}" for i in range(50)]
    modules.append({
        "id": "sovereign_entry",
        "path": "src/entry.py",
        "source": "# Sovereign entry point\nimport sys\ndef main(): pass",
        "imports": entry_imports,
        "exports": ["main"],
        "trust_boundary": "sovereign::core",
        "is_entry": True,
    })

    # 50 reachable modules across 3 trust boundaries
    boundaries = ["axon::teles", "axon::vision", "sovereign::logic"]
    for i in range(50):
        modules.append({
            "id": f"mod_{i}",
            "path": f"src/mod_{i}.py",
            "source": f"def fn_{i}(): return {i}",
            "imports": [],
            "exports": [f"fn_{i}"],
            "trust_boundary": boundaries[i % len(boundaries)],
            "is_entry": False,
        })

    # 20 dead modules (should be tree-shaken)
    for i in range(20):
        modules.append({
            "id": f"dead_{i}",
            "path": f"src/dead_{i}.py",
            "source": f"# Dead code\ndef unused_{i}(): pass",
            "imports": [],
            "exports": [f"unused_{i}"],
            "trust_boundary": "dead::zone",
            "is_entry": False,
        })

    t0 = time.perf_counter()
    result = bridge.link_modules(modules)
    link_ms = (time.perf_counter() - t0) * 1000

    print(f"\n📊 Link Result:")
    print(f"   Total modules:     {result['total_modules']}")
    print(f"   Dead eliminated:   {result['dead_modules_eliminated']}")
    print(f"   Output chunks:     {result['total_chunks']}")
    print(f"   Graph edges:       {result['module_graph_edges']}")
    print(f"   Native link time:  {result['link_time_us']}µs")
    print(f"   Python wall clock: {link_ms:.2f}ms")

    for chunk in result["chunks"]:
        print(f"   📦 {chunk['id']} | {len(chunk['modules'])} mods | "
              f"{chunk['size_bytes'] / 1024:.1f}KB | {chunk['keccak_seal'][:24]}...")

    # --- Test 2: Seal throughput ---
    print(f"\n📊 Keccak-256 Seal Throughput:")
    n_seals = 5000
    payload = "sovereign attestation payload"
    t0 = time.perf_counter()
    last_seal = ""
    for i in range(n_seals):
        last_seal = bridge.seal(f"{payload}_{i}")
    seal_ms = (time.perf_counter() - t0) * 1000
    print(f"   {n_seals} seals in {seal_ms:.2f}ms")
    print(f"   Throughput: {n_seals / (seal_ms / 1000):.0f} seals/sec")
    print(f"   Per seal: {seal_ms / n_seals * 1000:.2f}µs")
    print(f"   Sample: {last_seal}")

    # --- Test 3: Python hashlib comparison ---
    import hashlib
    print(f"\n📊 Python hashlib.sha3_256 Comparison:")
    t0 = time.perf_counter()
    for i in range(n_seals):
        hashlib.sha3_256(f"{payload}_{i}".encode()).hexdigest()
    py_seal_ms = (time.perf_counter() - t0) * 1000
    speedup = py_seal_ms / seal_ms
    print(f"   Python native: {py_seal_ms:.2f}ms ({n_seals / (py_seal_ms / 1000):.0f} seals/sec)")
    print(f"   Zetto Rust:    {seal_ms:.2f}ms ({n_seals / (seal_ms / 1000):.0f} seals/sec)")
    print(f"   Speedup:       {speedup:.1f}×")

    # Verdict
    print(f"\n{'=' * 60}")
    if result["dead_modules_eliminated"] == 20 and result["total_chunks"] >= 3:
        print("✅ BRIDGE VERIFIED — Tree-shaking, chunking, and sealing operational.")
    else:
        print("❌ BRIDGE ISSUE — Check module graph construction.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    _benchmark()
