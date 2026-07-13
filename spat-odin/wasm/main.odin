package wasm

import "../core/spat"
import "../core/tokenizer"
import "core:mem"

global_model: spat.SpatModel
model_loaded := false
out_buffer: [dynamic]u8

@(export)
wasmspat_new :: proc() -> rawptr {
    return rawptr(uintptr(1))
}

@(export)
wasmspat_free :: proc(ptr: rawptr, action: i32) {
    if model_loaded {
        delete(global_model.pos_weights)
        delete(global_model.neg_weights)
        model_loaded = false
    }
}

@(export)
wasmspat_load :: proc(self_ptr: rawptr, data_ptr: ^u8, data_len: int) -> i32 {
    data_slice := mem.slice_ptr(data_ptr, data_len)
    model, ok := spat.load_spat(data_slice)
    if !ok {
        return 1
    }
    global_model = model
    global_model.pos_weights = make([]u32, len(model.pos_weights))
    global_model.neg_weights = make([]u32, len(model.neg_weights))
    copy(global_model.pos_weights, model.pos_weights)
    copy(global_model.neg_weights, model.neg_weights)
    model_loaded = true
    
    tokenizer.init_vocabulary()
    return 0
}

@(export)
wasmspat_generate :: proc(self_ptr: rawptr, prompt_ptr: ^u8, prompt_len: int, max_tokens: int, temp: f32) -> rawptr {
    if !model_loaded {
        return nil
    }
    prompt_bytes := mem.slice_ptr(prompt_ptr, prompt_len)
    prompt_str := string(prompt_bytes)
    
    prompt_tokens := tokenizer.tokenize(prompt_str)
    defer delete(prompt_tokens)
    
    tokens := make([dynamic]u32)
    defer delete(tokens)
    for t in prompt_tokens {
        append(&tokens, t)
    }
    
    generated := make([dynamic]u32)
    defer delete(generated)
    
    for i in 0..<max_tokens {
        logits := spat.transformer_forward(&global_model, tokens[:])
        defer delete(logits)
        
        next := spat.sample_token(logits, temp)
        append(&generated, next)
        append(&tokens, next)
        
        if next == 0 || next == 50256 {
            break
        }
    }
    
    output_str := tokenizer.detokenize(generated[:])
    defer delete(output_str)
    
    clear(&out_buffer)
    for i in 0..<len(output_str) {
        append(&out_buffer, output_str[i])
    }
    append(&out_buffer, 0)
    
    return raw_data(out_buffer)
}

@(export)
wasmspat_num_layers :: proc(self_ptr: rawptr) -> u32 {
    return global_model.num_layers
}

@(export)
wasmspat_weights_len :: proc(self_ptr: rawptr) -> u32 {
    return global_model.weights_len
}

@(export)
wasmspat_model_size_kb :: proc(self_ptr: rawptr) -> f32 {
    return f32(len(global_model.pos_weights) * 8) / 1024.0
}
