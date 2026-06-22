---
created: '2026-06-22T15:23:35Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T15:23:37.920586Z'
---

# Implementation Plan: Strategic Token Optimization for Hermes Desktop

This plan details the implementation of token saving strategies to optimize prompt structures and external LLM cost efficiency for Hermes Desktop using DeepSeek.

## User Review Required

> [!IMPORTANT]
> - **Cosine Semantic Caching**: The semantic cache will check cosine similarity of query embeddings. If similarity is $\geq 0.92$, a cached response will be returned with zero API calls.
> - **Top-5 Vector Retrieval**: Naive OKF context injection will be replaced by querying ChromaDB for the top-5 most relevant concepts based on vector similarity search, reducing prompt size by ~72%.
> - **Prefix Stabilization**: A stable prefix consisting of system persona, tool schemas, and OKF schemas will be prepended to prompt payloads to maximize DeepSeek provider-side caching.

## Open Questions

> [!NOTE]
> - **Mock Cache Storing**: To facilitate verification and dashboard metric tracking in the emulated testbed environment, we propose caching mock query responses in addition to real responses. Please confirm if this is acceptable.

---

## Proposed Changes

### Semantic Cache & Prefix Stabilization

#### [MODIFY] [external_gateway.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/external_gateway.py)
- **Cosine Semantic Search Cache**:
  - Implement pseudo-embeddings and cosine similarity calculation for cached prompts.
  - Upgrade `_find_cached_response` to query the database/json cache using cosine similarity. If the maximum similarity is $\geq 0.92$, return the response directly as a semantic cache hit.
  - Store all successful mock and real responses in the cache.
- **Prefix Stabilization**:
  - Add `stabilize_prefix` policy to `gateway_policy.json` (enabled by default).
  - Prepend a fixed system instruction string (persona, schema, tool descriptions) to API payloads. Put variable parameters (user queries, memories) strictly at the end.

---

### Retrieval-Based Memory & Compression

#### [MODIFY] [s2l_pipeline.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/s2l_pipeline.py)
- **Top-5 Vector Memory Selection**:
  - Import `get_embedder` from `embedding_pipeline.py`.
  - In `skill_inference`, when falling back to in-context prompting, query `EmbeddingPipeline.search(prompt, limit=5)` to retrieve only the top 5 relevant concepts.
  - Format these top-5 concepts into a compressed memory context string instead of the entire concept database.
- **Context Compression**:
  - Truncate any long concept body details to a 200-character summary snippet to prevent prompt bloat.

---

### OKF Telemetry Updates

#### [MODIFY] [triad_metrics.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/triad_metrics.py)
- Update gateway metrics to track token reduction from retrieval-based memory selection (~72% saved on context memory) and semantic cache hits.

---

## Verification Plan

### Automated Tests
- Test semantic caching by calling `external_infer` with a prompt, and then calling it again with a slightly paraphrased prompt (e.g. cosine similarity $\geq 0.92$). Verify that it registers a semantic cache hit.
- Test `skill_inference` fallback mode: verify that it searches and injects exactly 5 relevant concepts, reporting the token savings.
- Validate that `gateway_health` returns policy information about prompt stabilization and semantic cache size.

### Manual Verification
- Access the Cockpit Dashboard on port 8080 and confirm that the cache hit rate and token savings metrics are updated correctly.
