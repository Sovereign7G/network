package tokenizer

import "core:strings"

VOCAB: map[string]u32
REVERSE_VOCAB: map[u32]string

init_vocabulary :: proc() {
    VOCAB = make(map[string]u32)
    REVERSE_VOCAB = make(map[u32]string)
    
    seed_vocab("hello", 15339)
    seed_vocab("world", 1917)
    seed_vocab("the", 262)
    seed_vocab("sovereign", 100000)
    seed_vocab("ai", 100001)
    seed_vocab("mesh", 100002)
    seed_vocab("spat", 100003)
}

seed_vocab :: proc(word: string, id: u32) {
    VOCAB[word] = id
    REVERSE_VOCAB[id] = word
}

tokenize :: proc(text: string) -> []u32 {
    tokens := make([dynamic]u32)
    words := strings.split(text, " ")
    defer delete(words)
    
    for word, index in words {
        if id, exists := VOCAB[word]; exists {
            append(&tokens, id)
        } else {
            for i := 0; i < len(word); i += 1 {
                ch := word[i]
                val := u32(ch)
                if val >= 32 && val <= 126 {
                    append(&tokens, val)
                }
            }
        }
        if index < len(words) - 1 {
            append(&tokens, 32)
        }
    }
    return tokens[:]
}

detokenize :: proc(tokens: []u32) -> string {
    builder := strings.builder_make()
    defer strings.builder_destroy(&builder)
    
    for token in tokens {
        if word, exists := REVERSE_VOCAB[token]; exists {
            strings.write_string(&builder, word)
        } else if token >= 32 && token <= 126 {
            strings.write_byte(&builder, u8(token))
        } else if token == 0 {
            break
        } else {
            strings.write_byte(&builder, ' ')
        }
    }
    return strings.to_string(builder)
}
