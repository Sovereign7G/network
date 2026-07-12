use std::fs::File;
use std::io::Read;
use std::convert::TryInto;

#[cfg(not(target_arch = "wasm32"))]
extern "C" {
    fn run_oewse_pouw_search(
        prompt_bits: *const u32,
        weight_matrix_pos: *const u32,
        weight_matrix_neg: *const u32,
        target_difficulty: u32,
        max_nonces: u32,
        blocks: u32,
        threads_per_block: u32,
        out_nonce: *mut u32,
        out_proof_hash: *mut u32,
    );
    fn init_oewse_context(threads_per_block: u32) -> *mut std::ffi::c_void;
    fn upload_oewse_weights(
        context_ptr: *mut std::ffi::c_void,
        weight_matrix_pos: *const u32,
        weight_matrix_neg: *const u32,
        threads_per_block: u32,
    );
    fn run_oewse_pouw_search_with_context(
        context_ptr: *mut std::ffi::c_void,
        prompt_bits: *const u32,
        target_difficulty: u32,
        max_nonces: u32,
        blocks: u32,
        threads_per_block: u32,
        out_nonce: *mut u32,
        out_proof_hash: *mut u32,
    );
    fn free_oewse_context(context_ptr: *mut std::ffi::c_void);
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen::prelude::wasm_bindgen]
pub struct OewseGpuContext {
    weights_pos: Vec<u32>,
    weights_neg: Vec<u32>,
    threads_per_block: u32,
}

#[cfg(not(target_arch = "wasm32"))]
pub struct OewseGpuContext {
    ptr: *mut std::ffi::c_void,
    threads_per_block: u32,
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen::prelude::wasm_bindgen]
impl OewseGpuContext {
    #[wasm_bindgen::prelude::wasm_bindgen(constructor)]
    pub fn new(threads_per_block: u32) -> Self {
        Self {
            weights_pos: Vec::new(),
            weights_neg: Vec::new(),
            threads_per_block,
        }
    }

    pub fn upload_weights(&mut self, weights_pos: &[u32], weights_neg: &[u32]) {
        self.weights_pos = weights_pos.to_vec();
        self.weights_neg = weights_neg.to_vec();
    }

    pub fn load_spatial_model(path: &str) -> Result<OewseGpuContext, String> {
        // Simple loading stub for WASM filesystem
        let mut ctx = OewseGpuContext::new(256);
        ctx.upload_weights(&vec![0; 40 * 256], &vec![0; 40 * 256]);
        Ok(ctx)
    }

    pub fn mine_inference_proof(
        &self,
        prompt: &[u32],
        difficulty: u32,
    ) -> Option<String> {
        // CPU fallback simulation of PoUW XNOR + popcount search
        let mixed_input = prompt[0] ^ 0x01;
        let w_pos = self.weights_pos.get(0).cloned().unwrap_or(0);
        let match_pos = !(mixed_input ^ w_pos);
        let similarity = match_pos.count_ones();
        
        if similarity > 16 {
            Some(format!("{{ \"nonce\": 123456, \"proof_hash\": {} }}", similarity))
        } else {
            None
        }
    }
}

#[cfg(not(target_arch = "wasm32"))]
impl OewseGpuContext {
    pub fn new(threads_per_block: u32) -> Self {
        let ptr = unsafe { init_oewse_context(threads_per_block) };
        Self { ptr, threads_per_block }
    }

    pub fn upload_weights(&self, weights_pos: &[u32], weights_neg: &[u32]) {
        unsafe {
            upload_oewse_weights(self.ptr, weights_pos.as_ptr(), weights_neg.as_ptr(), self.threads_per_block);
        }
    }

    pub fn load_spatial_model(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let mut file = File::open(path)?;
        
        let mut magic = [0u8; 4];
        file.read_exact(&mut magic)?;
        if &magic != b"SPAT" {
            return Err("Invalid spatial model file: magic header mismatch".into());
        }

        let mut version = [0u8; 4];
        file.read_exact(&mut version)?;
        let version = u32::from_le_bytes(version);
        if version != 1 {
            return Err(format!("Unsupported spatial model version: {}", version).into());
        }

        let mut header = [0u8; 12];
        file.read_exact(&mut header)?;
        
        let _num_layers = u32::from_le_bytes(header[0..4].try_into()?);
        let threads_per_block = u32::from_le_bytes(header[4..8].try_into()?);
        let weights_len = u32::from_le_bytes(header[8..12].try_into()?) as usize;

        let mut weights_pos_bytes = vec![0u8; weights_len * 4];
        file.read_exact(&mut weights_pos_bytes)?;
        let mut weights_pos = vec![0u32; weights_len];
        for (i, chunk) in weights_pos_bytes.chunks_exact(4).enumerate() {
            weights_pos[i] = u32::from_le_bytes(chunk.try_into()?);
        }

        let mut weights_neg_bytes = vec![0u8; weights_len * 4];
        file.read_exact(&mut weights_neg_bytes)?;
        let mut weights_neg = vec![0u32; weights_len];
        for (i, chunk) in weights_neg_bytes.chunks_exact(4).enumerate() {
            weights_neg[i] = u32::from_le_bytes(chunk.try_into()?);
        }

        let ctx = Self::new(threads_per_block);
        ctx.upload_weights(&weights_pos, &weights_neg);

        Ok(ctx)
    }

    pub fn mine_inference_proof(
        &self,
        prompt: &[u32; 128],
        difficulty: u32,
    ) -> Option<(u32, u32)> {
        let mut winning_nonce: u32 = 0;
        let mut final_proof_hash: u32 = 0;
        let blocks = 512;
        let max_nonces_per_thread = 1000;

        unsafe {
            run_oewse_pouw_search_with_context(
                self.ptr,
                prompt.as_ptr(),
                difficulty,
                max_nonces_per_thread,
                blocks,
                self.threads_per_block,
                &mut winning_nonce as *mut u32,
                &mut final_proof_hash as *mut u32,
            );
        }

        if winning_nonce != 0 {
            Some((winning_nonce, final_proof_hash))
        } else {
            None
        }
    }
}

#[cfg(not(target_arch = "wasm32"))]
impl Drop for OewseGpuContext {
    fn drop(&mut self) {
        unsafe {
            free_oewse_context(self.ptr);
        }
    }
}

#[cfg(not(target_arch = "wasm32"))]
unsafe impl Send for OewseGpuContext {}
#[cfg(not(target_arch = "wasm32"))]
unsafe impl Sync for OewseGpuContext {}

#[cfg(not(target_arch = "wasm32"))]
pub fn mine_inference_proof(
    prompt: &[u32; 128],
    weights_pos: &[u32],
    weights_neg: &[u32],
    difficulty: u32,
) -> Option<(u32, u32)> {
    let mut winning_nonce: u32 = 0;
    let mut final_proof_hash: u32 = 0;

    let threads_per_block = 256;
    let blocks = 512;
    let max_nonces_per_thread = 1000;

    unsafe {
        run_oewse_pouw_search(
            prompt.as_ptr(),
            weights_pos.as_ptr(),
            weights_neg.as_ptr(),
            difficulty,
            max_nonces_per_thread,
            blocks,
            threads_per_block,
            &mut winning_nonce as *mut u32,
            &mut final_proof_hash as *mut u32,
        );
    }

    if winning_nonce != 0 {
        Some((winning_nonce, final_proof_hash))
    } else {
        None
    }
}
