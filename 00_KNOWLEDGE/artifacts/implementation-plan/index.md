---
created: '2026-06-22T19:14:26Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T19:14:30.586010Z'
---

# AetherDB Multi-Language SDK Implementation Plan

We will implement client SDKs for Elixir, Python, and TypeScript, splitting the classes/modules logically, providing numpy integration, type hints, promise-based API, and automated test suites for validation.

## User Review Required

> [!IMPORTANT]
> To compile and run Elixir tests in the `projects/aether_db` directory, we need to copy `mix.exs`, `mix.lock`, `.gitignore`, and `.formatter.exs` from the legacy `aether_db` folder to the target `projects/aether_db` directory.
> All Elixir code will follow the `AetherDb` namespace (lowercase `b`) to match existing codebase modules.

## Proposed Changes

### Configuration Setup

We will copy the necessary build/mix configurations to `/media/cherry/4A21-00001/New folder/AGE REPUBLIC/projects/aether_db` to enable compiling and running tests.

---

### Elixir SDK (Native)
We will split the Elixir SDK into clean, modular files inside `lib/aether_db/sdk/` and implement the test suite.

#### [MODIFY] [client.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/lib/aether_db/sdk/client.ex)
- Native client wrapper logic.
- Implements `connect/2`, `disconnect/1`, `get/2`, `get!/2`, `put/3`, `put!/3`, `delete/2`, `delete!/2`, `search/4`, `search!/4`, `insert_vector/5`, `batch_get/2`, `batch_put/2`.
- Integrates `AetherDb.SDK.Transaction` for transactional execution.
- Integrates `AetherDb.SDK.Stream` for CDC streaming.

#### [NEW] [transaction.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/lib/aether_db/sdk/transaction.ex)
- `AetherDb.SDK.Transaction` module containing the transaction struct and logic (`put/3`, `get/2`, `delete/2`, `insert_vector/5`).
- Supports staging of transactional operations.

#### [NEW] [stream.ex](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/lib/aether_db/sdk/stream.ex)
- `AetherDb.SDK.Stream` module with pattern subscriptions and event stream handling.

#### [NEW] [elixir_sdk_test.exs](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/test/sdk/elixir_sdk_test.exs)
- Extensive testing for `Client`, `Transaction`, and `Stream` functionality, ensuring they compile and pass under `mix test`.

---

### Python SDK
We will split the Python client logic into separate, clean files inside `sdk/python/aetherdb/` to improve maintainability and support type-checking.

#### [NEW] [types.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/python/aetherdb/types.py)
- Defines domain datatypes (`VectorClock`, `SearchResult`, `Metric`, `DType`, `Table`, `Operation`, `Filter`).
- Implements vector clock comparisons and merging.

#### [NEW] [client.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/python/aetherdb/client.py)
- Async-native HTTP/WS-based client logic.
- Implements `AetherDBClient` lifecycle and operations, including `get`, `put`, `delete`, `search`, `insert_vector`, `batch_get`, `batch_put`, `stream`, and `transaction`.
- Implements `Transaction` context class for multi-operation commits and rollbacks.

#### [NEW] [numpy.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/python/aetherdb/numpy.py)
- NumPy integration class (`AetherDBNumpy`).
- Supports batch inserts and vector conversions (`to_tensor`/`from_tensor`).

#### [MODIFY] [__init__.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/python/aetherdb/__init__.py)
- Re-exports core classes from `client`, `numpy`, and `types` to preserve clean top-level imports.

#### [NEW] [test_client.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/python/tests/test_client.py)
- Python SDK tests covering CRUD, vector operations, batch requests, and transactions.

---

### TypeScript SDK
Ensure the TypeScript client covers all specifications including connection pooling/retry strategies.

#### [MODIFY] [client.ts](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/projects/aether_db/sdk/typescript/src/client.ts)
- Standardize types and imports.
- Ensure proper compilation and lint readiness.

---

## Verification Plan

### Automated Tests
1. **Elixir SDK**:
   Run `mix test` inside `/media/cherry/4A21-00001/New folder/AGE REPUBLIC/projects/aether_db` to verify the entire test suite passes.
2. **Python SDK**:
   Run `pytest` inside the Python SDK directory to verify tests pass.
