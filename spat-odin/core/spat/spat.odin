package spat

import "base:intrinsics"
import "core:math"
import "core:mem"

SpatModel :: struct {
    num_layers:        u32,
    threads_per_block: u32,
    weights_len:       u32,
    pos_weights:       []u32,
    neg_weights:       []u32,
    vocab_size:        u32,
}

load_spat :: proc(data: []u8) -> (model: SpatModel, ok: bool) {
    if len(data) < 20 {
        return {}, false
    }
    if data[0] != 'S' || data[1] != 'P' || data[2] != 'A' || data[3] != 'T' {
        return {}, false
    }
    
    version := parse_u32_le(data[4:8])
    num_layers := parse_u32_le(data[8:12])
    threads_per_block := parse_u32_le(data[12:16])
    weights_len := parse_u32_le(data[16:20])
    
    expected_size := 20 + int(weights_len) * 8
    if len(data) < expected_size {
        return {}, false
    }
    
    pos_bytes := data[20 : 20 + weights_len * 4]
    neg_bytes := data[20 + weights_len * 4 : 20 + weights_len * 8]
    
    pos_weights := slice_bytes_to_u32s(pos_bytes)
    neg_weights := slice_bytes_to_u32s(neg_bytes)
    
    model = SpatModel{
        num_layers = num_layers,
        threads_per_block = threads_per_block,
        weights_len = weights_len,
        pos_weights = pos_weights,
        neg_weights = neg_weights,
        vocab_size = weights_len * 32,
    }
    return model, true
}

parse_u32_le :: proc(b: []u8) -> u32 {
    return u32(b[0]) | (u32(b[1]) << 8) | (u32(b[2]) << 16) | (u32(b[3]) << 24)
}

slice_bytes_to_u32s :: proc(b: []u8) -> []u32 {
    n := len(b) / 4
    if n == 0 {
        return nil
    }
    ptr := (^u32)(raw_data(b))
    return mem.slice_ptr(ptr, n)
}

xnor_popcount_score :: proc(input, pos, neg: u32) -> i32 {
    match_pos := ~(input ~ pos)
    match_neg := ~(input ~ neg)
    return i32(intrinsics.count_ones(match_pos)) - i32(intrinsics.count_ones(match_neg))
}

layer_forward :: proc(model: ^SpatModel, hidden: []u32, layer: int) -> []u32 {
    tpb := int(model.threads_per_block)
    start := layer * tpb
    n := len(model.pos_weights)
    end := math.min(start + tpb, n)
    
    if start >= n {
        return hidden
    }
    
    out := make([]u32, len(hidden))
    for h, i in hidden {
        wi := start + (i % (end - start))
        if wi < n {
            score := xnor_popcount_score(h, model.pos_weights[wi], model.neg_weights[wi])
            out[i] = h ~ (model.pos_weights[wi] if score > 0 else model.neg_weights[wi])
        } else {
            out[i] = h
        }
    }
    return out
}

transformer_forward :: proc(model: ^SpatModel, input_tokens: []u32) -> []f32 {
    tpb := int(model.threads_per_block)
    hidden := make([dynamic]u32)
    defer delete(hidden)
    
    for t in input_tokens {
        append(&hidden, t)
    }
    for len(hidden) < tpb {
        append(&hidden, 0)
    }
    
    curr := hidden[:]
    for layer in 0..<model.num_layers {
        next_hidden := layer_forward(model, curr, int(layer))
        if layer > 0 {
            delete(curr)
        }
        curr = next_hidden
    }
    
    n := len(model.pos_weights)
    logits_len := math.max(n, int(model.vocab_size))
    logits := make([]f32, logits_len)
    for i in 0..<n {
        logits[i] = f32(xnor_popcount_score(curr[0], model.pos_weights[i], model.neg_weights[i]))
    }
    if int(model.num_layers) > 0 {
        delete(curr)
    }
    return logits
}
