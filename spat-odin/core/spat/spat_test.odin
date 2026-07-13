package spat

import "core:testing"

@(test)
test_xnor_popcount :: proc(t: ^testing.T) {
    score := xnor_popcount_score(0b1010, 0b1010, 0b0101)
    testing.expect_value(t, score, i32(4)) // matching bits minus mismatching bits
}
