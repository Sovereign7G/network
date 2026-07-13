package tokenizer

import "core:testing"

@(test)
test_tokenization :: proc(t: ^testing.T) {
    init_vocabulary()
    defer {
        delete(VOCAB)
        delete(REVERSE_VOCAB)
    }
    
    toks := tokenize("hello world")
    defer delete(toks)
    
    testing.expect_value(t, len(toks), 3)
    testing.expect_value(t, toks[0], u32(15339))
    testing.expect_value(t, toks[1], u32(32)) // space
    testing.expect_value(t, toks[2], u32(1917))
}
