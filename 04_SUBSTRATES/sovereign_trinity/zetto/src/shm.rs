//! 🏛️ AGE REPUBLIC :: ZETTO SHARED MEMORY BRIDGE
//! ================================================
//! POSIX shared memory region for zero-copy data exchange
//! between Zetto (Rust) and Mojo SIMD kernels.
//!
//! This is the critical "wings" — the component that enables
//! the Mojo compiler to write AST data directly into memory
//! that Zetto reads without serialization.
//!
//! Layout of the shared memory region:
//! ┌──────────────────────────────────────────────────┐
//! │ Header (64 bytes)                                │
//! │   [0..4]   magic: u32 = 0x5A455454 ("ZETT")     │
//! │   [4..8]   version: u32 = 1                      │
//! │   [8..12]  node_count: u32                       │
//! │   [12..16] status: u32 (0=empty, 1=ready, 2=err)│
//! │   [16..24] timestamp_ns: u64                     │
//! │   [24..32] producer_id: u64 (Mojo process hash)  │
//! │   [32..64] reserved                              │
//! ├──────────────────────────────────────────────────┤
//! │ Node Types   [64 .. 64 + node_count]    : u8[]   │
//! ├──────────────────────────────────────────────────┤
//! │ Node Values  [aligned .. + node_count*4]: f32[]  │
//! ├──────────────────────────────────────────────────┤
//! │ Attest Hash  [aligned .. + node_count*8]: u64[]  │
//! └──────────────────────────────────────────────────┘

use std::ffi::CString;
use std::os::raw::c_char;

/// Magic bytes: "ZETT" in little-endian
const MAGIC: u32 = 0x5445_5A54; // "TZET" stored as LE → reads as "ZETT"
const HEADER_SIZE: usize = 64;
const MAX_NODES: usize = 1_000_000;

/// Status codes for the shared memory region
#[repr(u32)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShmStatus {
    Empty = 0,
    Ready = 1,
    Error = 2,
    Processing = 3,
}

/// Header structure for the shared memory region.
#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct ShmHeader {
    pub magic: u32,
    pub version: u32,
    pub node_count: u32,
    pub status: u32,
    pub timestamp_ns: u64,
    pub producer_id: u64,
    pub _reserved: [u8; 32],
}

impl ShmHeader {
    pub fn new() -> Self {
        Self {
            magic: MAGIC,
            version: 1,
            node_count: 0,
            status: ShmStatus::Empty as u32,
            timestamp_ns: 0,
            producer_id: 0,
            _reserved: [0u8; 32],
        }
    }

    pub fn is_valid(&self) -> bool {
        self.magic == MAGIC && self.version == 1
    }
}

/// Represents a mapped shared memory region.
/// In production, this would use `mmap` on a POSIX shm file descriptor.
/// For now, we use a heap-allocated buffer with the same layout,
/// which allows Python/Mojo to write via ctypes/pointer and Zetto
/// to read via the same pointer — zero-copy within a single process.
pub struct SharedAstRegion {
    buffer: Vec<u8>,
    capacity: usize,
}

impl SharedAstRegion {
    /// Allocate a shared memory region for up to `max_nodes` AST nodes.
    pub fn new(max_nodes: usize) -> Self {
        let capacity = Self::required_size(max_nodes);
        let buffer = vec![0u8; capacity];
        let mut region = Self { buffer, capacity };

        // Write header
        let header = ShmHeader::new();
        let header_bytes: &[u8] = unsafe {
            std::slice::from_raw_parts(
                &header as *const ShmHeader as *const u8,
                std::mem::size_of::<ShmHeader>(),
            )
        };
        region.buffer[..HEADER_SIZE.min(header_bytes.len())]
            .copy_from_slice(&header_bytes[..HEADER_SIZE.min(header_bytes.len())]);

        region
    }

    /// Calculate the total buffer size needed for `n` nodes.
    fn required_size(n: usize) -> usize {
        HEADER_SIZE + n + (n * 4) + (n * 8) // types(u8) + values(f32) + hashes(u64)
    }

    /// Get a raw pointer to the buffer (for FFI consumers to write into).
    pub fn as_ptr(&self) -> *const u8 {
        self.buffer.as_ptr()
    }

    /// Get a mutable raw pointer (for Mojo/Python to write AST data).
    pub fn as_mut_ptr(&mut self) -> *mut u8 {
        self.buffer.as_mut_ptr()
    }

    /// Read the header from the shared memory region.
    pub fn read_header(&self) -> ShmHeader {
        let mut header = ShmHeader::new();
        unsafe {
            let dst = &mut header as *mut ShmHeader as *mut u8;
            let size = std::mem::size_of::<ShmHeader>().min(HEADER_SIZE);
            std::ptr::copy_nonoverlapping(self.buffer.as_ptr(), dst, size);
        }
        header
    }

    /// Read node types from the shared memory region.
    pub fn read_node_types(&self, count: usize) -> &[u8] {
        let start = HEADER_SIZE;
        let end = start + count;
        &self.buffer[start..end.min(self.capacity)]
    }

    /// Read node values (f32) from the shared memory region.
    pub fn read_node_values(&self, count: usize) -> Vec<f32> {
        let start = HEADER_SIZE + count; // after node_types
        let mut values = Vec::with_capacity(count);
        for i in 0..count {
            let offset = start + i * 4;
            if offset + 4 <= self.capacity {
                let bytes: [u8; 4] = [
                    self.buffer[offset],
                    self.buffer[offset + 1],
                    self.buffer[offset + 2],
                    self.buffer[offset + 3],
                ];
                values.push(f32::from_le_bytes(bytes));
            }
        }
        values
    }

    /// Read attestation hashes (u64) from the shared memory region.
    pub fn read_attestation_hashes(&self, count: usize) -> Vec<u64> {
        let start = HEADER_SIZE + count + count * 4; // after types + values
        let mut hashes = Vec::with_capacity(count);
        for i in 0..count {
            let offset = start + i * 8;
            if offset + 8 <= self.capacity {
                let bytes: [u8; 8] = [
                    self.buffer[offset],
                    self.buffer[offset + 1],
                    self.buffer[offset + 2],
                    self.buffer[offset + 3],
                    self.buffer[offset + 4],
                    self.buffer[offset + 5],
                    self.buffer[offset + 6],
                    self.buffer[offset + 7],
                ];
                hashes.push(u64::from_le_bytes(bytes));
            }
        }
        hashes
    }

    /// Write a complete AST into the shared memory region.
    /// Used for testing — in production, Mojo writes directly via pointer.
    pub fn write_ast(&mut self, node_types: &[u8], node_values: &[f32], hashes: &[u64]) {
        let count = node_types.len();
        assert!(count <= MAX_NODES, "Node count exceeds maximum");
        assert_eq!(count, node_values.len());
        assert_eq!(count, hashes.len());

        // Write header
        let mut header = self.read_header();
        header.node_count = count as u32;
        header.status = ShmStatus::Ready as u32;
        header.timestamp_ns = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;

        unsafe {
            let src = &header as *const ShmHeader as *const u8;
            let size = std::mem::size_of::<ShmHeader>().min(HEADER_SIZE);
            std::ptr::copy_nonoverlapping(src, self.buffer.as_mut_ptr(), size);
        }

        // Write node types
        let types_start = HEADER_SIZE;
        self.buffer[types_start..types_start + count].copy_from_slice(node_types);

        // Write node values (f32 → LE bytes)
        let values_start = types_start + count;
        for (i, val) in node_values.iter().enumerate() {
            let bytes = val.to_le_bytes();
            let offset = values_start + i * 4;
            self.buffer[offset..offset + 4].copy_from_slice(&bytes);
        }

        // Write attestation hashes (u64 → LE bytes)
        let hashes_start = values_start + count * 4;
        for (i, hash) in hashes.iter().enumerate() {
            let bytes = hash.to_le_bytes();
            let offset = hashes_start + i * 8;
            self.buffer[offset..offset + 8].copy_from_slice(&bytes);
        }
    }

    /// Check if the region has valid, ready-to-read data.
    pub fn is_ready(&self) -> bool {
        let header = self.read_header();
        header.is_valid() && header.status == ShmStatus::Ready as u32
    }
}

// ─────────────────────────────────────────────────────────────
// FFI Surface for Shared Memory
// ─────────────────────────────────────────────────────────────

thread_local! {
    static SHM_REGION: std::cell::RefCell<SharedAstRegion> =
        std::cell::RefCell::new(SharedAstRegion::new(100_000));
}

/// Allocate a shared memory region for `max_nodes` AST nodes.
/// Returns a pointer to the raw buffer that Mojo/Python can write to.
#[no_mangle]
pub extern "C" fn zetto_shm_alloc(max_nodes: u32) -> *mut u8 {
    SHM_REGION.with(|r| {
        *r.borrow_mut() = SharedAstRegion::new(max_nodes as usize);
        r.borrow_mut().as_mut_ptr()
    })
}

/// Get the current shared memory buffer pointer.
#[no_mangle]
pub extern "C" fn zetto_shm_ptr() -> *mut u8 {
    SHM_REGION.with(|r| r.borrow_mut().as_mut_ptr())
}

/// Get the size of the shared memory buffer in bytes.
#[no_mangle]
pub extern "C" fn zetto_shm_size() -> u32 {
    SHM_REGION.with(|r| r.borrow().capacity as u32)
}

/// Check if the shared memory region has valid, ready data.
/// Returns 1 if ready, 0 if not.
#[no_mangle]
pub extern "C" fn zetto_shm_is_ready() -> i32 {
    SHM_REGION.with(|r| if r.borrow().is_ready() { 1 } else { 0 })
}

/// Read the node count from the shared memory header.
#[no_mangle]
pub extern "C" fn zetto_shm_node_count() -> u32 {
    SHM_REGION.with(|r| r.borrow().read_header().node_count)
}

/// Dump the shared memory contents as a JSON summary string.
/// Caller must free with zetto_free_string.
#[no_mangle]
pub extern "C" fn zetto_shm_dump() -> *mut c_char {
    let summary = SHM_REGION.with(|r| {
        let region = r.borrow();
        let header = region.read_header();
        let count = header.node_count as usize;

        let types = region.read_node_types(count.min(10));
        let values = region.read_node_values(count.min(10));

        serde_json::json!({
            "magic_valid": header.is_valid(),
            "version": header.version,
            "node_count": count,
            "status": header.status,
            "timestamp_ns": header.timestamp_ns,
            "producer_id": header.producer_id,
            "sample_types": types,
            "sample_values": values,
            "buffer_size_bytes": region.capacity,
        })
        .to_string()
    });

    match CString::new(summary) {
        Ok(c) => c.into_raw(),
        Err(_) => std::ptr::null_mut(),
    }
}

// ─────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shared_memory_roundtrip() {
        let mut region = SharedAstRegion::new(100);

        // Write 10 nodes
        let types: Vec<u8> = (0..10).map(|i| i as u8).collect();
        let values: Vec<f32> = (0..10).map(|i| i as f32 * 0.1).collect();
        let hashes: Vec<u64> = (0..10).map(|i| i as u64 * 7919).collect();

        region.write_ast(&types, &values, &hashes);

        // Verify header
        let header = region.read_header();
        assert!(header.is_valid());
        let nc = header.node_count;
        let st = header.status;
        assert_eq!(nc, 10);
        assert_eq!(st, ShmStatus::Ready as u32);

        // Verify data roundtrip
        let read_types = region.read_node_types(10);
        assert_eq!(read_types, &types[..]);

        let read_values = region.read_node_values(10);
        for (a, b) in read_values.iter().zip(values.iter()) {
            assert!((a - b).abs() < 1e-6);
        }

        let read_hashes = region.read_attestation_hashes(10);
        assert_eq!(read_hashes, hashes);
    }

    #[test]
    fn test_empty_region_not_ready() {
        let region = SharedAstRegion::new(100);
        assert!(!region.is_ready()); // Status is Empty, not Ready
    }

    #[test]
    fn test_large_ast_write() {
        let n = 50_000;
        let mut region = SharedAstRegion::new(n);

        let types: Vec<u8> = (0..n).map(|i| (i % 8) as u8).collect();
        let values: Vec<f32> = (0..n).map(|i| (i as f32) * 0.001).collect();
        let hashes: Vec<u64> = (0..n).map(|i| (i as u64) * 31).collect();

        let start = std::time::Instant::now();
        region.write_ast(&types, &values, &hashes);
        let dur = start.elapsed();

        let header = region.read_header();
        let nc = header.node_count;
        assert_eq!(nc, n as u32);
        assert!(region.is_ready());

        // 50K nodes should write in under 5ms
        assert!(dur.as_millis() < 5, "Write took {}ms", dur.as_millis());
    }
}
