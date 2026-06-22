---
created: '2026-06-22T18:45:46Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T18:45:49.727798Z'
---

# Implementation Plan — Phase 3: CRDT Implementation & Gossip Protocol

This phase implements 7 Conflict-Free Replicated Data Types (CRDTs) in Rust, builds a property-based merge engine in Elixir, and implements a gossip protocol using Merkle Trees for state synchronization.

## User Review Required

> [!IMPORTANT]
> To maintain codebase casing consistency with the existing modules, all modules will use the `AetherDb` namespace (lowercase `Db`), e.g., `AetherDb.CRDT`, `AetherDb.Gossip`, etc.

## Proposed Changes

### Rust NIF Crate (`native/aetherdb_native`)

We will add a CRDT state engine and serialization layers to the Rust NIF crate.

---

#### [NEW] [crdt.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/crdt.rs)
- Defines the `CrdtType` enum (GCounter, PNCounter, GSet, ORSet, LWWRegister, MVRegister, RGA).
- Implements CRDT state structs with associative, commutative, and idempotent merge semantics.
- Uses `Option<T>` for the `RGA` elements to represent the sentinel node `(0, 0, None)` without requiring type `T` to have a default value.

#### [NEW] [crdt_serialize.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/crdt_serialize.rs)
- Implements `crdt_to_toon` converting Rust CRDT states into `ToonValue`.
- Implements `toon_to_crdt` reconstructing CRDT states from a `ToonValue`.
- Fully supports ORSet `adds` and `removes` serialization.

#### [MODIFY] [lib.rs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/native/aetherdb_native/src/lib.rs)
- Declares the new `crdt` and `crdt_serialize` modules.
- Implements NIF wrappers: `crdt_new/1`, `crdt_merge/2`, `crdt_increment/2`, `crdt_decrement/2`, `crdt_add/4`, `crdt_remove/4`, `crdt_set/4`, `crdt_insert/5`, and `crdt_value/1`.
- Registers these functions under the single NIF initialization entry point.

---

### Elixir Codebase (`lib/aether_db`)

We will add wrapper APIs for CRDTs, property checkers, Merkle trees, and a GenServer-based gossip protocol.

---

#### [MODIFY] [native.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/toon/native.ex)
- Declares the new CRDT NIF stubs so they are loaded from the unified `aetherdb_native` shared library.

#### [NEW] [crdt.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/crdt.ex)
- API wrappers delegating to NIF calls.
- Adds `set/4` and `insert/5` to support Last-Write-Wins/Multi-Value registers and RGA insertions.

#### [NEW] [merge.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/crdt/merge.ex)
- Algebraic property testing helpers (associative, commutative, idempotent, monotonic).
- `merge_many/1` implementation.

#### [NEW] [merkle.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/merkle.ex)
- Complete Merkle Tree implementation mapping leaves to TOON hashes.
- Diffing algorithm to locate divergent token indices between two trees in $O(\log N)$ time.

#### [NEW] [gossip.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/gossip.ex)
- Anti-entropy mesh GenServer running periodic randomized gossip sync rounds.

---

### Test Suite (`test/aether_db`)

---

#### [NEW] [crdt_test.exs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/test/aether_db/crdt_test.exs)
- Comprehensive test coverage for all 7 CRDT types.
- Validates monotonicity, LWW timestamps, and concurrent/merge logic.

#### [NEW] [gossip_test.exs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/test/aether_db/gossip_test.exs)
- Gossip GenServer lifecycle testing (peer list, schedule cast).
- Merkle Tree generation and difference detection testing.

---

## Verification Plan

### Automated Tests
- Compile the Rust NIF and Elixir library:
  ```bash
  mix compile
  ```
- Run the full test suite (aiming for all 43 original + new tests passing):
  ```bash
  mix test
  ```
