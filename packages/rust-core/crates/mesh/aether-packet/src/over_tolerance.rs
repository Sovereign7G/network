use reed_solomon_erasure::galois_8::ReedSolomon;
use crc::{Crc, CRC_64_ECMA_182};

pub const CASTAGNOLI: Crc<u64> = Crc::<u64>::new(&CRC_64_ECMA_182);

#[derive(Debug)]
pub enum BoltError {
    Truncated,
    ChecksumFailed,
}

#[repr(C, packed)]
pub struct ControlBolt {
    pub intent: [u8; 16],
    pub node_id: [u8; 32],
    pub seq: u64,
    pub crc: u64,
}

impl ControlBolt {
    pub const WIDTH: usize = 64;
    
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, BoltError> {
        if bytes.len() < Self::WIDTH {
            return Err(BoltError::Truncated);
        }
        
        // Zero-copy read
        let bolt = unsafe { std::ptr::read(bytes.as_ptr() as *const Self) };
        
        // Verify checksum
        let expected_crc = CASTAGNOLI.checksum(&bytes[..56]);
        if bolt.crc != expected_crc {
            return Err(BoltError::ChecksumFailed);
        }
        
        Ok(bolt)
    }
    
    pub fn intent_str(&self) -> &str {
        let end = self.intent.iter().position(|&b| b == 0).unwrap_or(16);
        std::str::from_utf8(&self.intent[..end]).unwrap_or("UNKNOWN")
    }
}

pub struct RattleSpace {
    rs: ReedSolomon,
}

impl RattleSpace {
    pub fn new() -> Self {
        // 3 data + 1 parity = 33% overhead
        let rs = ReedSolomon::new(3, 1).expect("Failed to init ReedSolomon");
        Self { rs }
    }
    
    pub fn recover(&self, mangled: &[u8]) -> Option<Vec<u8>> {
        // This is a simplified reconstruction for simulation/verification
        // Real impl would handle shard alignment
        let mut shards: Vec<Option<Vec<u8>>> = vec![
            Some(mangled[..100].to_vec()), 
            Some(mangled[100..200].to_vec()), 
            Some(mangled[200..300].to_vec()),
            None // The "rattle space" parity shard
        ];
        
        if self.rs.reconstruct(&mut shards).is_ok() {
            let mut result = Vec::new();
            for i in 0..3 {
                if let Some(shard) = &shards[i] {
                    result.extend_from_slice(shard);
                }
            }
            Some(result)
        } else {
            None
        }
    }
}
