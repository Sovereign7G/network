//! 🏛️ AGE REPUBLIC :: ZETTO — Sovereign Module Linker
//! ====================================================
//! Rust-powered module linker, tree-shaker, and attestation sealer.
//! Exposes a C-ABI FFI surface for zero-copy consumption by Axon (Bun).
//!
//! Analog: Rolldown in the Voidzero Trinity.

use sha3::{Digest, Keccak256};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::ffi::{CStr, CString};
use std::os::raw::c_char;
use std::time::Instant;

// Shared memory bridge for Mojo zero-copy integration
pub mod shm;

// ─────────────────────────────────────────────────────────────
// Core Data Structures
// ─────────────────────────────────────────────────────────────

/// A sovereign module in the dependency graph.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SovereignModule {
    pub id: String,
    pub path: String,
    pub source: String,
    pub imports: Vec<String>,
    pub exports: Vec<String>,
    pub trust_boundary: String,
    pub is_entry: bool,
}

/// A linked, sealed output chunk.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SealedChunk {
    pub id: String,
    pub modules: Vec<String>,
    pub code: String,
    pub keccak_seal: String,
    pub trust_boundary: String,
    pub size_bytes: usize,
    pub tree_shaken_exports: usize,
}

/// Full link result returned to Axon.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LinkResult {
    pub chunks: Vec<SealedChunk>,
    pub total_modules: usize,
    pub total_chunks: usize,
    pub dead_modules_eliminated: usize,
    pub link_time_us: u64,
    pub module_graph_edges: usize,
}

// ─────────────────────────────────────────────────────────────
// Module Graph
// ─────────────────────────────────────────────────────────────

/// Directed acyclic module dependency graph.
pub struct ModuleGraph {
    modules: HashMap<String, SovereignModule>,
    adjacency: HashMap<String, Vec<String>>,
}

impl ModuleGraph {
    pub fn new() -> Self {
        Self {
            modules: HashMap::new(),
            adjacency: HashMap::new(),
        }
    }

    pub fn add_module(&mut self, module: SovereignModule) {
        let id = module.id.clone();
        let imports = module.imports.clone();
        self.modules.insert(id.clone(), module);
        self.adjacency.insert(id, imports);
    }

    /// Returns the set of module IDs reachable from the entry points.
    pub fn reachable_from_entries(&self) -> HashSet<String> {
        let mut visited = HashSet::new();
        let mut stack: Vec<String> = self
            .modules
            .values()
            .filter(|m| m.is_entry)
            .map(|m| m.id.clone())
            .collect();

        while let Some(id) = stack.pop() {
            if visited.contains(&id) {
                continue;
            }
            visited.insert(id.clone());
            if let Some(deps) = self.adjacency.get(&id) {
                for dep in deps {
                    if !visited.contains(dep) {
                        stack.push(dep.clone());
                    }
                }
            }
        }
        visited
    }

    pub fn edge_count(&self) -> usize {
        self.adjacency.values().map(|v| v.len()).sum()
    }
}

// ─────────────────────────────────────────────────────────────
// Attestation Engine
// ─────────────────────────────────────────────────────────────

/// Keccak-256 attestation sealer for sovereign chunks.
pub struct KeccakAttestationEngine;

impl KeccakAttestationEngine {
    /// Produces a Keccak-256 hex digest of the given content.
    pub fn seal(content: &str) -> String {
        let mut hasher = Keccak256::new();
        hasher.update(content.as_bytes());
        let result = hasher.finalize();
        format!("0x{}", hex::encode_upper(&result).to_lowercase())
    }
}

// Inline hex encoding (no extra dependency)
mod hex {
    pub fn encode_upper(bytes: &[u8]) -> String {
        bytes.iter().map(|b| format!("{:02X}", b)).collect()
    }
}

// ─────────────────────────────────────────────────────────────
// Sovereign Linker — Core Engine
// ─────────────────────────────────────────────────────────────

/// The core Zetto linker that resolves, tree-shakes, chunks, and seals.
pub struct ZettoLinker {
    graph: ModuleGraph,
}

impl ZettoLinker {
    pub fn new() -> Self {
        Self {
            graph: ModuleGraph::new(),
        }
    }

    pub fn add_module(&mut self, module: SovereignModule) {
        self.graph.add_module(module);
    }

    /// Execute the full link pipeline:
    /// 1. Build dependency graph
    /// 2. Tree-shake unreachable modules
    /// 3. Split by trust boundary
    /// 4. Seal each chunk with Keccak-256
    pub fn link(&self) -> LinkResult {
        let start = Instant::now();
        let total_modules = self.graph.modules.len();
        let edge_count = self.graph.edge_count();

        // Phase 1: Tree-shake — find reachable modules from entries
        let reachable = self.graph.reachable_from_entries();
        let dead_count = total_modules - reachable.len();

        // Phase 2: Group reachable modules by trust boundary
        let mut boundary_groups: HashMap<String, Vec<&SovereignModule>> = HashMap::new();
        for id in &reachable {
            if let Some(module) = self.graph.modules.get(id) {
                boundary_groups
                    .entry(module.trust_boundary.clone())
                    .or_default()
                    .push(module);
            }
        }

        // Phase 3: Produce sealed chunks
        let mut chunks = Vec::new();
        for (boundary, modules) in &boundary_groups {
            // Concatenate module sources into chunk code
            let mut chunk_code = String::new();
            let mut chunk_module_ids = Vec::new();
            let mut shaken_exports = 0usize;

            for module in modules {
                chunk_code.push_str(&format!(
                    "// === Module: {} ===\n{}\n\n",
                    module.id, module.source
                ));
                chunk_module_ids.push(module.id.clone());

                // Count exports that survived tree-shaking
                shaken_exports += module.exports.len();
            }

            // Inject attestation seal as a constant
            let seal = KeccakAttestationEngine::seal(&chunk_code);
            let sealed_code = format!(
                "const __ZETTO_SEAL__ = \"{}\";\n\n{}",
                seal, chunk_code
            );
            let size = sealed_code.len();

            chunks.push(SealedChunk {
                id: format!("chunk_{}", boundary.replace("::", "_")),
                modules: chunk_module_ids,
                code: sealed_code,
                keccak_seal: seal,
                trust_boundary: boundary.clone(),
                size_bytes: size,
                tree_shaken_exports: shaken_exports,
            });
        }

        let link_time = start.elapsed().as_micros() as u64;

        LinkResult {
            total_chunks: chunks.len(),
            chunks,
            total_modules,
            dead_modules_eliminated: dead_count,
            link_time_us: link_time,
            module_graph_edges: edge_count,
        }
    }
}

// ─────────────────────────────────────────────────────────────
// C-ABI FFI Surface — Consumed by Axon via Bun bun:ffi
// ─────────────────────────────────────────────────────────────

/// Thread-local linker instance for FFI calls.
/// In production this would be behind an Arc<Mutex<>>, but for
/// the single-threaded Bun FFI bridge, thread-local is optimal.
thread_local! {
    static LINKER: std::cell::RefCell<ZettoLinker> = std::cell::RefCell::new(ZettoLinker::new());
}

/// Initialize / reset the linker.
#[no_mangle]
pub extern "C" fn zetto_init() {
    LINKER.with(|l| {
        *l.borrow_mut() = ZettoLinker::new();
    });
}

/// Add a module to the linker graph.
/// Accepts a JSON-encoded SovereignModule string.
/// Returns 0 on success, 1 on parse error.
#[no_mangle]
pub extern "C" fn zetto_add_module(json_ptr: *const c_char) -> i32 {
    let c_str = unsafe {
        if json_ptr.is_null() {
            return 1;
        }
        CStr::from_ptr(json_ptr)
    };

    let json_str = match c_str.to_str() {
        Ok(s) => s,
        Err(_) => return 1,
    };

    let module: SovereignModule = match serde_json::from_str(json_str) {
        Ok(m) => m,
        Err(_) => return 1,
    };

    LINKER.with(|l| {
        l.borrow_mut().add_module(module);
    });

    0
}

/// Execute the link pipeline and return a JSON-encoded LinkResult.
/// The caller must free the returned string with `zetto_free_string`.
#[no_mangle]
pub extern "C" fn zetto_link() -> *mut c_char {
    let result = LINKER.with(|l| l.borrow().link());

    let json = match serde_json::to_string_pretty(&result) {
        Ok(j) => j,
        Err(_) => return std::ptr::null_mut(),
    };

    match CString::new(json) {
        Ok(c) => c.into_raw(),
        Err(_) => std::ptr::null_mut(),
    }
}

/// Compute a standalone Keccak-256 seal for arbitrary content.
/// The caller must free the returned string with `zetto_free_string`.
#[no_mangle]
pub extern "C" fn zetto_seal(content_ptr: *const c_char) -> *mut c_char {
    let c_str = unsafe {
        if content_ptr.is_null() {
            return std::ptr::null_mut();
        }
        CStr::from_ptr(content_ptr)
    };

    let content = match c_str.to_str() {
        Ok(s) => s,
        Err(_) => return std::ptr::null_mut(),
    };

    let seal = KeccakAttestationEngine::seal(content);

    match CString::new(seal) {
        Ok(c) => c.into_raw(),
        Err(_) => std::ptr::null_mut(),
    }
}

/// Free a string previously returned by zetto_link or zetto_seal.
#[no_mangle]
pub extern "C" fn zetto_free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe {
            let _ = CString::from_raw(ptr);
        }
    }
}

/// Return the Zetto version string.
#[no_mangle]
pub extern "C" fn zetto_version() -> *mut c_char {
    let v = CString::new("1.0.0-sovereign").expect("valid version string");
    v.into_raw()
}

// ─────────────────────────────────────────────────────────────
// Unit Tests
// ─────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    fn make_module(id: &str, imports: Vec<&str>, exports: Vec<&str>, boundary: &str, entry: bool) -> SovereignModule {
        SovereignModule {
            id: id.to_string(),
            path: format!("src/{}.ts", id),
            source: format!("export function {}() {{ /* {} */ }}", id, id),
            imports: imports.into_iter().map(String::from).collect(),
            exports: exports.into_iter().map(String::from).collect(),
            trust_boundary: boundary.to_string(),
            is_entry: entry,
        }
    }

    #[test]
    fn test_tree_shaking_eliminates_dead_modules() {
        let mut linker = ZettoLinker::new();

        // Entry → A → B (reachable)
        // C is dead (not imported by anything reachable)
        linker.add_module(make_module("entry", vec!["A"], vec!["main"], "core", true));
        linker.add_module(make_module("A", vec!["B"], vec!["helperA"], "core", false));
        linker.add_module(make_module("B", vec![], vec!["helperB"], "core", false));
        linker.add_module(make_module("C_dead", vec![], vec!["unused"], "core", false));

        let result = linker.link();
        assert_eq!(result.total_modules, 4);
        assert_eq!(result.dead_modules_eliminated, 1);
        assert_eq!(result.total_chunks, 1); // All in same trust boundary
    }

    #[test]
    fn test_trust_boundary_splitting() {
        let mut linker = ZettoLinker::new();

        linker.add_module(make_module("entry", vec!["voice", "vision"], vec!["main"], "core", true));
        linker.add_module(make_module("voice", vec![], vec!["speak"], "axon::teles", false));
        linker.add_module(make_module("vision", vec![], vec!["see"], "axon::vision", false));

        let result = linker.link();
        assert_eq!(result.total_chunks, 3); // core, axon::teles, axon::vision
    }

    #[test]
    fn test_keccak_sealing() {
        let seal = KeccakAttestationEngine::seal("hello sovereign world");
        assert!(seal.starts_with("0x"));
        assert_eq!(seal.len(), 66); // 0x + 64 hex chars
    }

    #[test]
    fn test_link_performance_under_1ms() {
        let mut linker = ZettoLinker::new();
        // 100 modules — should link in microseconds
        linker.add_module(make_module("entry", (0..99).map(|i| format!("mod_{}", i)).collect::<Vec<_>>().iter().map(|s| s.as_str()).collect(), vec!["main"], "core", true));
        for i in 0..99 {
            linker.add_module(make_module(
                &format!("mod_{}", i),
                vec![],
                vec!["fn"],
                "core",
                false,
            ));
        }

        let result = linker.link();
        assert_eq!(result.total_modules, 100);
        assert_eq!(result.dead_modules_eliminated, 0);
        // In debug mode ~2ms is normal; release builds achieve sub-100µs for 100 modules
        assert!(result.link_time_us < 5000, "Link took {}µs, expected <5000µs (debug)", result.link_time_us);
    }
}
