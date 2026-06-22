---
created: '2026-06-22T18:22:36Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T18:22:40.709842Z'
---

# Goal: AetherDB v2 — Phase 1 Week 2: Rust Library Implementation

Implement the core TOON storage serialization, deserialization, memory-mapping, and verification library in Rust.

## User Review Required

> [!IMPORTANT]
> - **Memory Layout Alignments**: The serialize and deserialize engines will use binary slices and implement zero-copy/zero-parse lookups by reading the memory-mapped bytes directly using exact offset offsets.
> - **Error Handling**: Custom Rust errors will be mapped to Elixir terms to support standard error propagation back to BEAM processes.

---

## Proposed Changes

### Rust Native Library (`aetherdb_native`)

#### [MODIFY] [lib.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/lib.rs)
- Declare `ToonHeader`, `ToonToken`, `ToonType`, and file loading stubs.
- Define Rustler NIF wrappers:
  - `serialize_toon(map) -> binary`
  - `deserialize_toon(binary) -> map`
  - `read_value(binary, key) -> value`

#### [NEW] [serialize.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/serialize.rs)
- Implement `ToonSerializer` to serialize Elixir/Erlang terms into the raw TOON binary bytes layout, including header generation, token index sorting, and variable-length data section alignments.

#### [NEW] [deserialize.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/deserialize.rs)
- Implement zero-copy reader and deserializer decoding fields directly from mapped binary byte buffers.

#### [NEW] [utils.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/utils.rs)
- Implement `validate_toon_file` and xxHash fingerprint calculations.

---

## Verification Plan

### Automated Tests
- Run `mix test` to verify that our stub functions in Elixir/Rust compiles and passes serialization/deserialization correctness tests.
