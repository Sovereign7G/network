package tests

import "core:testing"
import ctx "../core/context"

@(test)
test_context_creation :: proc(t: ^testing.T) {
    c := ctx.RuntimeContext{
        node_id = "test-node",
    }
    testing.expect_value(t, c.node_id, "test-node")
}
