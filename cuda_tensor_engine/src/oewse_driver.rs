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
    // Cached weights for transformer forward pass
    weights_pos: Vec<u32>,
    weights_neg: Vec<u32>,
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
        _difficulty: u32,
    ) -> u32 {
        // CPU fallback simulation of PoUW XNOR + popcount search
        let mixed_input = prompt[0] ^ 0x01;
        let w_pos = self.weights_pos.get(0).cloned().unwrap_or(0);
        let match_pos = !(mixed_input ^ w_pos);
        match_pos.count_ones()
    }

    pub fn get_packed_weight_textures(&self) -> js_sys::Array {
        let array = js_sys::Array::new();
        for layer in 0..48 {
            let start = layer * 4096 * 16;
            let end = start + 4096 * 16;
            let mut packed = Vec::with_capacity(4096 * 16 * 4);
            for i in start..end {
                let pos_val = self.weights_pos.get(i).cloned().unwrap_or(0) as u8;
                let neg_val = self.weights_neg.get(i).cloned().unwrap_or(0) as u8;
                packed.push(pos_val);
                packed.push(neg_val);
                packed.push(0);
                packed.push(255);
            }
            let js_arr = js_sys::Uint8Array::from(packed.as_slice());
            array.push(&js_arr);
        }
        array
    }

    pub fn get_num_layers(&self) -> u32 {
        48
    }

    pub fn get_tile_width(&self) -> u32 {
        4096
    }

    pub fn get_tile_height(&self) -> u32 {
        16
    }
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen::prelude::wasm_bindgen]
pub struct IrohNode {
    node_id: String,
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen::prelude::wasm_bindgen]
impl IrohNode {
    #[wasm_bindgen::prelude::wasm_bindgen(constructor)]
    pub fn new(node_id: String) -> Self {
        Self { node_id }
    }

    pub fn node_id(&self) -> String {
        self.node_id.clone()
    }
}

#[cfg(not(target_arch = "wasm32"))]
impl OewseGpuContext {
    pub fn new(threads_per_block: u32) -> Self {
        let ptr = unsafe { init_oewse_context(threads_per_block) };
        Self { ptr, threads_per_block, weights_pos: Vec::new(), weights_neg: Vec::new() }
    }

    pub fn upload_weights(&mut self, weights_pos: &[u32], weights_neg: &[u32]) {
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

        let mut ctx = Self::new(threads_per_block);
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

// ── Transformer Inference FFI ────────────────────────────────────────────

extern "C" {
    fn run_oewse_transformer_infer(
        prompt_tokens: *const u32,
        weight_matrix_pos: *const u32,
        weight_matrix_neg: *const u32,
        output_logits: *mut f32,
        num_layers: u32,
        hidden_dim: u32,
        vocab_size: u32,
        threads_per_block: u32,
        blocks: u32,
    );
}

/// Run chained transformer inference: 40+ layers of XNOR + popcount,
/// producing float logits for token sampling.
/// This is the free-function version (no context required).
pub fn transformer_infer(
    prompt_tokens: &[u32; 128],
    weights_pos: &[u32],
    weights_neg: &[u32],
    output_logits: &mut [f32],
    num_layers: u32,
    hidden_dim: u32,
    vocab_size: u32,
) {
    if weights_pos.is_empty() || weights_neg.is_empty() {
        eprintln!("transformer_infer: no weights loaded");
        return;
    }
    let threads_per_block = 256;
    let blocks = (vocab_size + threads_per_block - 1) / threads_per_block;

    unsafe {
        run_oewse_transformer_infer(
            prompt_tokens.as_ptr(),
            weights_pos.as_ptr(),
            weights_neg.as_ptr(),
            output_logits.as_mut_ptr(),
            num_layers,
            hidden_dim,
            vocab_size,
            threads_per_block,
            blocks,
        );
    }
}

// ── OewseGpuContext method for transformer forward pass ────────────────

#[cfg(not(target_arch = "wasm32"))]
impl OewseGpuContext {
    /// Run full transformer forward pass through all SPAT layers.
    /// Uses the cached weights loaded via upload_weights().
    pub fn transformer_forward(
        &self,
        prompt_tokens: &[u32; 128],
        output_logits: &mut [f32],
        vocab_size: u32,
    ) {
        if self.weights_pos.is_empty() || self.weights_neg.is_empty() {
            eprintln!("transformer_forward: no weights cached — call upload_weights first");
            return;
        }
        let n_layers = self.weights_pos.len() as u32 / self.threads_per_block;
        let h_dim = 4096;
        transformer_infer(
            prompt_tokens,
            &self.weights_pos,
            &self.weights_neg,
            output_logits,
            n_layers,
            h_dim,
            vocab_size,
        );
    }
}
