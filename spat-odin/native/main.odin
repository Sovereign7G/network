package main

import "../core/spat"
import "../core/tokenizer"
import "core:fmt"
import "core:net"
import "core:strings"
import "core:os"
import "core:mem"

global_model: spat.SpatModel
model_loaded := false

main :: proc() {
    // Default model path
    model_path := "07_MODELS/gemma4-12b-spatial.spat"
    
    // Check command line arguments for alternative model path
    if len(os.args) > 1 {
        model_path = os.args[1]
    }
    
    fmt.printf("📂 Loading SPAT model: %s\n", model_path)
    
    // Read model file
    data, err := os.read_entire_file(model_path, context.allocator)
    if err != nil {
        fmt.eprintf("Failed to read model file: %s, error: %v\n", model_path, err)
        os.exit(1)
    }
    defer delete(data)
    
    // Parse model bytes
    model, load_ok := spat.load_spat(data)
    if !load_ok {
        fmt.eprintf("Failed to parse SPAT model\n")
        os.exit(1)
    }
    
    // Store in global
    global_model = model
    global_model.pos_weights = make([]u32, len(model.pos_weights))
    global_model.neg_weights = make([]u32, len(model.neg_weights))
    copy(global_model.pos_weights, model.pos_weights)
    copy(global_model.neg_weights, model.neg_weights)
    model_loaded = true
    
    fmt.printf("🏛️ Model loaded. num_layers=%d, weights_len=%d\n", global_model.num_layers, global_model.weights_len)
    
    // Initialize tokenizer
    tokenizer.init_vocabulary()
    
    // Bind socket on port 8010
    fmt.printf("🏛️ Starting Native Odin SPAT Runtime on port 8010...\n")
    endpoint := net.Endpoint{address = net.IP4_Address{0, 0, 0, 0}, port = 8010}
    listener, net_err := net.listen_tcp(endpoint)
    if net_err != nil {
        fmt.eprintf("Failed to listen: %v\n", net_err)
        os.exit(1)
    }
    defer net.close(listener)
    
    for {
        client, _, client_err := net.accept_tcp(listener)
        if client_err != nil {
            continue
        }
        handle_client(client)
    }
}

handle_client :: proc(socket: net.TCP_Socket) {
    defer net.close(socket)
    
    buffer: [4096]u8
    bytes_received, err := net.recv_tcp(socket, buffer[:])
    if err != nil || bytes_received <= 0 {
        return
    }
    
    request_str := string(buffer[:bytes_received])
    
    if strings.contains(request_str, "POST /v1/chat/completions") {
        body_start := strings.index(request_str, "\r\n\r\n")
        if body_start == -1 {
            send_bad_request(socket)
            return
        }
        body := request_str[body_start + 4:]
        prompt := extract_json_field(body, "content")
        
        // Tokenize
        prompt_tokens := tokenizer.tokenize(prompt)
        defer delete(prompt_tokens)
        
        // Autoregressive generation loop
        tokens := make([dynamic]u32)
        defer delete(tokens)
        for t in prompt_tokens {
            append(&tokens, t)
        }
        
        generated := make([dynamic]u32)
        defer delete(generated)
        
        max_tokens := 50
        temp: f32 = 0.7
        
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
        
        // Detokenize
        output_str := tokenizer.detokenize(generated[:])
        defer delete(output_str)
        
        response_body := fmt.tprintf(`{"choices":[{"message":{"content":"%s"}}]}`, output_str)
        
        http_response := fmt.tprintf(
            "HTTP/1.1 200 OK\r\n" +
            "Content-Type: application/json\r\n" +
            "Content-Length: %d\r\n" +
            "Connection: close\r\n\r\n" +
            "%s",
            len(response_body),
            response_body,
        )
        net.send_tcp(socket, transmute([]u8)http_response)
    } else {
        send_not_found(socket)
    }
}

extract_json_field :: proc(json, field: string) -> string {
    key := fmt.tprintf("\"%s\"", field)
    idx := strings.index(json, key)
    if idx == -1 {
        return "Hello"
    }
    start := idx + len(key)
    colon_idx := strings.index(json[start:], ":")
    if colon_idx == -1 {
        return "Hello"
    }
    quote_idx := strings.index(json[start + colon_idx:], "\"")
    if quote_idx == -1 {
        return "Hello"
    }
    str_start := start + colon_idx + quote_idx + 1
    str_end := strings.index(json[str_start:], "\"")
    if str_end == -1 {
        return "Hello"
    }
    return json[str_start : str_start + str_end]
}

send_bad_request :: proc(socket: net.TCP_Socket) {
    resp := "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
    net.send_tcp(socket, transmute([]u8)resp)
}

send_not_found :: proc(socket: net.TCP_Socket) {
    resp := "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
    net.send_tcp(socket, transmute([]u8)resp)
}
