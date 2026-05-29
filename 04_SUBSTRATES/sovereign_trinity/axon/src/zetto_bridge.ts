/**
 * 🏛️ AGE REPUBLIC :: ZETTO FFI BRIDGE
 * =====================================
 * Zero-copy bridge from Axon (TypeScript/Bun) to Zetto (Rust cdylib).
 * Uses Bun's native bun:ffi for direct shared library access.
 *
 * Analog: How Vite calls Rolldown internally — but via Bun FFI
 * instead of Node N-API.
 */

import { dlopen, FFIType, suffix, ptr, toArrayBuffer, CString } from "bun:ffi";
import { resolve, dirname } from "path";
import { existsSync } from "fs";

// ─────────────────────────────────────────────────────────────
// Types matching Zetto Rust structs
// ─────────────────────────────────────────────────────────────

export interface SovereignModule {
  id: string;
  path: string;
  source: string;
  imports: string[];
  exports: string[];
  trust_boundary: string;
  is_entry: boolean;
}

export interface SealedChunk {
  id: string;
  modules: string[];
  code: string;
  keccak_seal: string;
  trust_boundary: string;
  size_bytes: number;
  tree_shaken_exports: number;
}

export interface LinkResult {
  chunks: SealedChunk[];
  total_modules: number;
  total_chunks: number;
  dead_modules_eliminated: number;
  link_time_us: number;
  module_graph_edges: number;
}

// ─────────────────────────────────────────────────────────────
// Locate the compiled Zetto shared library
// ─────────────────────────────────────────────────────────────

function findZettoLib(): string {
  const rawPath = decodeURIComponent(new URL(import.meta.url).pathname);
  const trinityRoot = resolve(dirname(rawPath), "../..");
  const candidates = [
    resolve(trinityRoot, `zetto/target/release/libzetto.${suffix}`),
    resolve(trinityRoot, `zetto/target/debug/libzetto.${suffix}`),
    resolve(trinityRoot, `libzetto.${suffix}`),
  ];

  for (const path of candidates) {
    if (existsSync(path)) {
      return path;
    }
  }

  throw new Error(
    `❌ Zetto shared library not found. Run 'npm run build:zetto' first.\n` +
    `   Searched: ${candidates.join("\n             ")}`
  );
}

// ─────────────────────────────────────────────────────────────
// Open the Zetto shared library via Bun FFI
// ─────────────────────────────────────────────────────────────

let zettoLib: ReturnType<typeof dlopen> | null = null;

function getLib() {
  if (!zettoLib) {
    const libPath = findZettoLib();
    zettoLib = dlopen(libPath, {
      zetto_init: {
        args: [],
        returns: FFIType.void,
      },
      zetto_add_module: {
        args: [FFIType.ptr],
        returns: FFIType.i32,
      },
      zetto_link: {
        args: [],
        returns: FFIType.ptr,
      },
      zetto_seal: {
        args: [FFIType.ptr],
        returns: FFIType.ptr,
      },
      zetto_free_string: {
        args: [FFIType.ptr],
        returns: FFIType.void,
      },
      zetto_version: {
        args: [],
        returns: FFIType.ptr,
      },
    });
    console.log(`🔗 [Zetto FFI] Loaded native library from: ${libPath}`);
  }
  return zettoLib;
}

// ─────────────────────────────────────────────────────────────
// Read a C string from a raw pointer
// ─────────────────────────────────────────────────────────────

function readCString(pointer: any): string {
  if (!pointer || pointer === 0) {
    throw new Error("Received null pointer from Zetto");
  }
  // Read bytes until null terminator
  const buf = toArrayBuffer(pointer, 0, 1024 * 1024); // max 1MB
  const bytes = new Uint8Array(buf);
  let end = bytes.indexOf(0);
  if (end === -1) end = bytes.length;
  return new TextDecoder().decode(bytes.subarray(0, end));
}

// ─────────────────────────────────────────────────────────────
// Public API — The Axon→Zetto Bridge
// ─────────────────────────────────────────────────────────────

/**
 * Initialize / reset the Zetto linker.
 * Must be called before adding modules.
 */
export function zettoInit(): void {
  const lib = getLib();
  lib.symbols.zetto_init();
}

/**
 * Add a sovereign module to the linker graph.
 * @returns true on success, false on parse error
 */
export function zettoAddModule(module: SovereignModule): boolean {
  const lib = getLib();
  const json = JSON.stringify(module);
  const buf = Buffer.from(json + "\0", "utf-8");
  const result = lib.symbols.zetto_add_module(ptr(buf)) as number;
  return result === 0;
}

/**
 * Execute the full Zetto link pipeline:
 * resolve → tree-shake → chunk by trust boundary → Keccak-256 seal
 *
 * @returns The complete LinkResult with sealed chunks
 */
export function zettoLink(): LinkResult {
  const lib = getLib();
  const resultPtr = lib.symbols.zetto_link();

  if (!resultPtr || resultPtr === 0) {
    throw new Error("Zetto link returned null — internal linker error");
  }

  const jsonStr = readCString(resultPtr);
  lib.symbols.zetto_free_string(resultPtr);

  return JSON.parse(jsonStr) as LinkResult;
}

/**
 * Compute a standalone Keccak-256 seal for arbitrary content.
 */
export function zettoSeal(content: string): string {
  const lib = getLib();
  const buf = Buffer.from(content + "\0", "utf-8");
  const resultPtr = lib.symbols.zetto_seal(ptr(buf));

  if (!resultPtr || resultPtr === 0) {
    throw new Error("Zetto seal returned null");
  }

  const seal = readCString(resultPtr);
  lib.symbols.zetto_free_string(resultPtr);
  return seal;
}

/**
 * Get the Zetto version string.
 */
export function zettoVersion(): string {
  const lib = getLib();
  const vPtr = lib.symbols.zetto_version();
  const version = readCString(vPtr);
  lib.symbols.zetto_free_string(vPtr);
  return version;
}

/**
 * High-level convenience: link a full set of modules in one call.
 * Initializes the linker, adds all modules, and returns the result.
 */
export function zettoLinkModules(modules: SovereignModule[]): LinkResult {
  zettoInit();
  for (const mod of modules) {
    const ok = zettoAddModule(mod);
    if (!ok) {
      throw new Error(`Failed to add module: ${mod.id}`);
    }
  }
  return zettoLink();
}
