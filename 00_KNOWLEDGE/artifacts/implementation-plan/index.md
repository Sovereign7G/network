---
created: '2026-06-22T18:36:41Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T18:36:43.858991Z'
---

# Implementation Plan — Phase 2: Partition Actor Model

This plan outlines the design and proposed files for Phase 2: Partition Actor Model in AetherDb.

## User Review Required

> [!IMPORTANT]
> The modules will use the `AetherDb` namespace (lowercase `b`) instead of the blueprint's `AetherDB` namespace, aligning with the existing `AetherDb.TOON` and `AetherDb.TOONCache` implementations.
> Both `PartitionSupervisor` and `RouteTable` will be integrated into the application's root supervisor.

## Proposed Changes

### Core Storage & Routing Layer

---

#### [NEW] [partition.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition.ex)
- Implements `AetherDb.Partition` GenServer.
- Manages partition actor lifecycle, routing registry name via `AetherDb.PartitionRegistry`, mmap resource, token table, and in-memory key-value state database.
- Implements key/value parsing on startup (`parse_token_table/1`) to reconstruct the sorted token descriptor list and active database keys directly from binary mmap layouts.

#### [NEW] [reader.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition/reader.ex)
- Implements `AetherDb.Partition.Reader` helper functions.
- Provides `binary_search/2`, `range_query/4`, `prefix_search/3`, and `batch_get/3` logic on token tables.

#### [NEW] [writer.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition/writer.ex)
- Implements `AetherDb.Partition.Writer` helper functions.
- Handles updates by merging new key-value pairs into the in-memory map, serializing to a TOON binary via `TOON.serialize/1`, writing to a temp file, executing an atomic rename, and re-opening the file.

#### [NEW] [version.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition/version.ex)
- Implements `AetherDb.Partition.Version` for incrementing, merging, comparing, and serializing deterministic version vectors.

#### [NEW] [cache.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition/cache.ex)
- Implements `AetherDb.Partition.Cache` ETS GenServer cache layer with read-through and write-through optimizations.

#### [NEW] [supervisor.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/partition/supervisor.ex)
- Implements `AetherDb.PartitionSupervisor` to manage partition workers, the unique naming `AetherDb.PartitionRegistry`, the Cache GenServer, and the Routing Table GenServer.

#### [NEW] [route_table.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/route_table.ex)
- Implements `AetherDb.RouteTable` global routing mapping keys to partition processes.

#### [MODIFY] [application.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/lib/aether_db/application.ex)
- Adds `AetherDb.PartitionSupervisor` child specification to the top-level application startup.

#### [NEW] [partition_test.exs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/aether_db/test/aether_db/partition_test.exs)
- Comprehensive test suite checking writes/reads, sort order, cache operations, supervision restarts, range queries, and version vectors.

---

## Verification Plan

### Automated Tests
- Run `mix test` to confirm compilation and verify that all Phase 2 tests (along with legacy tests) pass.
