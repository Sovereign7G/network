package spat_context

import "core:testing"

@(test)
test_context_creation :: proc(t: ^testing.T) {
    ctx := RuntimeContext{
        node_id = "test-node",
    }
    testing.expect_value(t, ctx.node_id, "test-node")
}
