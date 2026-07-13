//! spat_transformer — SIMD-optimized SPAT inference engine.
//! Pure Rust, zero CUDA dependencies.
//! Loads a .spat file and runs chained XNOR+popcount across all layers.
//! Auto-vectorized by LLVM (AVX2, SSE4.2, NEON).

use std::fs;
use std::path::Path;

#[derive(Clone)]
pub struct SpatModel {
    pub num_layers: u32,
    pub threads_per_block: u32,
    pub weights_len: u32,
    pub pos_weights: Vec<u32>,
    pub neg_weights: Vec<u32>,
    pub vocab_size: u32,
}

impl SpatModel {
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let data = fs::read(path)?;
        Self::from_bytes(&data)
    }

    pub fn from_bytes(data: &[u8]) -> Result<Self, Box<dyn std::error::Error>> {
        if data.len() < 20 || &data[0..4] != b"SPAT" {
            return Err("Invalid SPAT header".into());
        }
        let _version = u32::from_le_bytes(data[4..8].try_into()?);
        let num_layers = u32::from_le_bytes(data[8..12].try_into()?);
        let threads_per_block = u32::from_le_bytes(data[12..16].try_into()?);
        let weights_len = u32::from_le_bytes(data[16..20].try_into()?) as usize;
        let pos_start = 20;
        let neg_start = pos_start + weights_len * 4;
        let pos_weights: Vec<u32> = data[pos_start..pos_start + weights_len * 4]
            .chunks_exact(4).map(|c| u32::from_le_bytes(c.try_into().unwrap())).collect();
        let neg_weights: Vec<u32> = data[neg_start..neg_start + weights_len * 4]
            .chunks_exact(4).map(|c| u32::from_le_bytes(c.try_into().unwrap())).collect();
        Ok(Self { num_layers, threads_per_block, weights_len: weights_len as u32, pos_weights, neg_weights, vocab_size: (weights_len as u32) * 32 })
    }
}

#[inline(always)]
fn xnor_popcount_score(input: u32, pos: u32, neg: u32) -> i32 {
    let match_pos = !(input ^ pos);
    let match_neg = !(input ^ neg);
    (match_pos.count_ones() as i32).wrapping_sub(match_neg.count_ones() as i32)
}

fn forward_single(model: &SpatModel, input_word: u32) -> Vec<f32> {
    let n = model.pos_weights.len();
    let mut logits = vec![0.0f32; n.max(model.vocab_size as usize)];
    for i in 0..n {
        logits[i] = xnor_popcount_score(input_word, model.pos_weights[i], model.neg_weights[i]) as f32;
    }
    logits
}

fn layer_forward(model: &SpatModel, hidden: &[u32], layer: usize) -> Vec<u32> {
    let tpb = model.threads_per_block as usize;
    let start = layer * tpb;
    let end = (start + tpb).min(model.pos_weights.len());
    if start >= model.pos_weights.len() { return hidden.to_vec(); }
    let mut out = Vec::with_capacity(hidden.len());
    for (i, &h) in hidden.iter().enumerate() {
        let wi = start + (i % (end - start));
        if wi < model.pos_weights.len() {
            let score = xnor_popcount_score(h, model.pos_weights[wi], model.neg_weights[wi]);
            out.push(if score > 0 { h ^ model.pos_weights[wi] } else { h ^ model.neg_weights[wi] });
        } else { out.push(h); }
    }
    out
}

/// Run full transformer forward pass — all layers in sequence.
pub fn transformer_forward(model: &SpatModel, input_tokens: &[u32]) -> Vec<f32> {
    let mut hidden: Vec<u32> = input_tokens.to_vec();
    while hidden.len() < model.threads_per_block as usize { hidden.push(0); }
    for layer in 0..model.num_layers as usize {
        hidden = layer_forward(model, &hidden, layer);
    }
    forward_single(model, hidden[0])
}

/// Sample next token from logits with temperature.
pub fn sample_token(logits: &[f32], temperature: f32) -> u32 {
    if temperature < 0.001 {
        return logits.iter().enumerate().max_by(|(_,a),(_,b)| a.partial_cmp(b).unwrap()).map(|(i,_)| i as u32).unwrap_or(0);
    }
    let max_l = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let mut exp_sum = 0.0f32;
    let mut probs: Vec<f32> = Vec::with_capacity(logits.len());
    for &l in logits { let e = ((l - max_l) / temperature).exp(); exp_sum += e; probs.push(e); }
    if exp_sum <= 0.0 { return 0; }
    for p in &mut probs { *p /= exp_sum; }
    let r: f32 = rand::random();
    let mut cum = 0.0;
    for (i, &p) in probs.iter().enumerate() { cum += p; if r <= cum { return i as u32; } }
    (probs.len() - 1) as u32
}

/// Generate text: autoregressive loop.
pub fn generate(model: &SpatModel, prompt_tokens: &[u32], max_tokens: usize, temperature: f32) -> Vec<u32> {
    let mut tokens = prompt_tokens.to_vec();
    let mut generated = Vec::new();
    for _ in 0..max_tokens {
        let logits = transformer_forward(model, &tokens);
        let next = sample_token(&logits, temperature);
        generated.push(next);
        tokens.push(next);
        if next == 0 { break; }
    }
    generated
}

/// C-compatible FFI entry point for Python ctypes.
#[no_mangle]
pub extern "C" fn spat_transformer_infer(
    spat_bytes: *const u8, spat_len: u32,
    input_tokens: *const u32, input_len: u32,
    max_tokens: u32, temperature: f32,
    out_logits: *mut f32, out_logits_len: *mut u32,
    out_tokens: *mut u32, out_tokens_len: *mut u32,
) -> i32 {
    let spat_slice = unsafe { std::slice::from_raw_parts(spat_bytes, spat_len as usize) };
    let model = match SpatModel::from_bytes(spat_slice) { Ok(m) => m, Err(e) => { eprintln!("{}", e); return -1; } };
    let tokens = unsafe { std::slice::from_raw_parts(input_tokens, input_len as usize) };
    let generated = generate(&model, tokens, max_tokens as usize, temperature);
    unsafe {
        *out_tokens_len = generated.len() as u32;
        for (i, &t) in generated.iter().enumerate() { *out_tokens.add(i) = t; }
        let logits = transformer_forward(&model, tokens);
        *out_logits_len = logits.len() as u32;
        for (i, &l) in logits.iter().enumerate() { *out_logits.add(i) = l; }
    }
    0
}

// ── WASM Bindings ────────────────────────────────────────────────────

#[cfg(feature = "wasm")]
mod wasm_bindings {
    use wasm_bindgen::prelude::*;
    use crate::{SpatModel, generate, transformer_forward};

    #[wasm_bindgen]
    pub struct WasmSPAT {
        model: SpatModel,
    }

    #[wasm_bindgen]
    impl WasmSPAT {
        #[wasm_bindgen(constructor)]
        pub fn new() -> Self {
            WasmSPAT { model: SpatModel { num_layers: 0, threads_per_block: 0, weights_len: 0, pos_weights: vec![], neg_weights: vec![], vocab_size: 0 } }
        }

        pub fn load(&mut self, data: &[u8]) -> Result<(), String> {
            self.model = SpatModel::from_bytes(data).map_err(|e| e.to_string())?;
            Ok(())
        }

        pub fn generate(&self, prompt: &str, max_tokens: usize, temperature: f32) -> String {
            let tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
            let generated = generate(&self.model, &tokens, max_tokens, temperature);
            String::from_utf8_lossy(&generated.iter().map(|&t| t as u8).collect::<Vec<_>>()).to_string()
        }

        pub fn num_layers(&self) -> u32 { self.model.num_layers }
        pub fn weights_len(&self) -> u32 { self.model.weights_len }
        pub fn model_size_kb(&self) -> f32 { (self.model.pos_weights.len() * 8) as f32 / 1024.0 }
    }
}
