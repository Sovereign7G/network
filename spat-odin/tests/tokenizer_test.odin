package tests

import "core:testing"
import tok "../core/tokenizer"

@(test)
test_tokenization :: proc(t: ^testing.T) {
    tok.init_vocabulary()
    defer {
        delete(tok.VOCAB)
        delete(tok.REVERSE_VOCAB)
    }
    
    toks := tok.tokenize("hello world")
    defer delete(toks)
    
    testing.expect_value(t, len(toks), 3)
    testing.expect_value(t, toks[0], u32(15339))
    testing.expect_value(t, toks[1], u32(32)) // space
    testing.expect_value(t, toks[2], u32(1917))
}
