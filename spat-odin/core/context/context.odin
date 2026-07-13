package spat_context

import "core:mem"
import "core:log"

RuntimeContext :: struct {
    allocator: mem.Allocator,
    logger:    log.Logger,
    node_id:   string,
}
