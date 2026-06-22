# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/335_F_REPUBLIC_TECENTDB_AGENT_MEMORY_WISDOM`
## Theme: TencentDB Agent Memory, 4-Tier Semantic Pyramid, and Symbolic Context Offloading

---

> [!IMPORTANT]
> **SYSTEM COMPACT-MEMORY BLUEPRINT:**
> This knowledge manifest formalizes the operational principles, benchmark claims, and software patterns of **TencentDB Agent Memory** (MIT-licensed). It establishes how agents eliminate context bloat and recall failure by offloading verbose execution traces to local flat files (`refs/*.md`), maintaining a symbolic Mermaid graph in-context, and structuring long-term memory into a four-tier semantic pyramid (Conversation → Atom → Scenario → Persona) queried via Reciprocal Rank Fusion (RRF).

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Most current memory systems for AI agents are fundamentally flawed — they "shred data into fragments and dump them into a flat vector store," and recall becomes "a blind similarity search across disconnected fragments, with no macro-level guidance."

**The core failures of flat memory:**
| Problem | Manifestation |
| :--- | :--- |
| **Context bloat** | Verbose tool logs, search results, and error traces consume hundreds of thousands of tokens |
| **Recall failure** | Blind similarity search across disconnected fragments, no structural guidance |
| **No traceability** | When recall is wrong, all you see is vector scores — no way to debug |
| **Irreversible compression** | Summaries discard evidence permanently |
| **Repetition** | "We constantly re-explain the same SOPs, project background, tool conventions, and output formats to the Agent" |

**The guiding philosophy:**
> *"Memory is not about hoarding everything in the AI — it is about sparing humans from having to repeat themselves."*

**Implicit Claim:** Flat vector memory is a dead end. Agents need layered, symbolic, traceable memory — not brute-force history accumulation, not irreversible lossy summarization, but a system that is "collapsible and expandable, abstract yet auditable."

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** TencentDB Agent Memory = **symbolic short-term memory + layered long-term memory** — a unified architecture rejecting both flat storage and irreversible compression.

**The two pillars:**
| Pillar | Mechanism | Benefit |
| :--- | :--- | :--- |
| **Symbolic short-term memory** | Offloads verbose tool logs to `refs/*.md`, condenses state into Mermaid canvas | Cuts token usage, preserves full traceability via `node_id` |
| **Layered long-term memory** | 4-tier semantic pyramid (L0 Conversation → L1 Atom → L2 Scenario → L3 Persona) | Progressive disclosure from macro persona down to raw evidence |

**The higher-level goal:**
> *"Let the Agent remember what should be remembered, so people can focus on judgment, creation, and work that truly matters."*

---

## 🔬 III. The Technical Arguments (Architectural Decisions)

### Argument A: The 4-Tier Semantic Pyramid
Instead of a flat vector store, TencentDB Agent Memory builds a hierarchical memory structure:

| Layer | Name | Content | Storage Format |
| :--- | :--- | :--- | :--- |
| **L0** | Conversation | Raw dialogue, full interaction history | Database (full-text retrieval) |
| **L1** | Atom | Atomic facts extracted from conversations | Database + vector |
| **L2** | Scenario | Scene blocks — common solution patterns | Markdown files |
| **L3** | Persona | User profile — preferences, long-term goals | Markdown files (`persona.md`) |

**Progressive disclosure pattern:**
- Persona layer queried first (carries day-to-day user preferences)
- System drills down to Atoms or raw Conversations only when finer detail is needed
- **Lower layers preserve evidence; upper layers preserve structure**

**Argument:** Memory should never be flat — both its formation and its recall must be hierarchical. A four-tier pyramid enables the agent to start with high-level guidance (persona) and drill down to evidence only when necessary.

### Argument B: Heterogeneous Storage Strategy

| Layer Type | Storage | Rationale |
| :--- | :--- | :--- |
| **Bottom layer** (facts, logs, traces) | Database (SQLite + sqlite-vec) | Robust full-text retrieval, vector search |
| **Top layer** (personas, scenes, canvases) | Markdown files | Human-readable, white-box inspection, high information density |

**Argument:** One size does not fit all. Raw facts belong in databases for efficient retrieval; structured knowledge belongs in Markdown for human auditability. The dual-layer strategy optimizes for both machine efficiency and human debuggability.

**Location:** `~/.openclaw/memory-tdai/` — "feel free to open the directory and inspect each layer for yourself."

### Argument C: Symbolic Short-Term Memory via Mermaid
**The problem:** In long tasks, the largest token consumers are verbose intermediate logs — search results, code, error traces.

**The solution:**
1. **Context offloading** — Full tool logs moved to external files (`refs/*.md`)
2. **Symbolic encoding** — State transitions encoded in high-density Mermaid syntax inside a lightweight task canvas
3. **`node_id` tracing** — Agent reasons over symbol graph; to verify a detail, it greps for `node_id` and retrieves full raw text

**Visual flow (from GitHub README):**
```
Verbose Logs → Offload full text → External FS (refs/*.md)
Verbose Logs → Extract relations → Mermaid Canvas (with node_id)
Mermaid Canvas → Light injection → Agent Context (few hundred tokens)
Agent ↔ Recall via node_id ↔ External FS
```

**Claim:** "Maximum semantics in minimum symbols" — Mermaid is precise enough for LLMs to parse, concise enough for humans to read.

### Argument D: Full Traceability via Deterministic Drill-Down
> *"Compression often sacrifices traceability. TencentDB Agent Memory avoids irreversible compression by maintaining a deterministic path from high-level abstractions back to ground-truth evidence."*

**The drill-down chain:**
- **Question type:** Daily preferences, voice, long-term goals
  - **First look at:** L3 Persona / L2 Scenario
  - **Drill down to:** L1 Atom / L0 Conversation when facts are needed

- **Question type:** Specific facts, dates, project details
  - **First look at:** L1 Atom / L0 Conversation
  - **Drill down to:** Widen time range or fall back to semantic recall

- **Question type:** Continuing a long-running task
  - **First look at:** Active Mermaid task canvas
  - **Drill down to:** JSONL when summary lacks detail → `refs/*.md` for raw text

**Argument:** The biggest risk in compression is saving tokens at the cost of losing evidence. A memory system must guarantee a complete, deterministic path from abstraction back to ground truth.

### Argument E: White-Box Debuggability
> *"Most memory systems fall short here: when recall is wrong, all you see is a list of vector scores, with no way to tell where things went wrong."*

**What TencentDB Agent Memory makes inspectable:**
- L2 Scenario blocks → plain Markdown, open and inspect
- L3 Persona → lives in `persona.md`, traces back to Scenarios that produced it
- Task canvases → Mermaid, readable by both humans and Agents
- Raw payloads, summaries, nodes → linked by `result_ref` and `node_id`

**Argument:** Memory is not a black box. Debugging should be "a deterministic walk along the chain 'Persona → Scenario → Atom → Conversation' until the root cause surfaces."

### Argument F: Hybrid Retrieval Strategy
**Default retrieval:** Hybrid = BM25 keyword + vector embeddings + Reciprocal Rank Fusion (RRF)

| Strategy | Use Case |
| :--- | :--- |
| `keyword` | Exact matches, known terms |
| `embedding` | Semantic similarity |
| `hybrid` (default) | Both — fused via RRF |

**Configuration options:**
- BM25 tokenizer supports both Chinese (`jieba`) and English
- Default `maxResults`: 5
- Default `timeoutMs`: 5000 (skip injection on timeout rather than blocking)

**Argument:** No single retrieval method is sufficient. Keyword search misses semantics; vector search misses exact matches. RRF fusion combines them without learned weights.

### Argument G: Zero-Config Local First
**Default backend:** SQLite + sqlite-vec — "no external API is required"

**OpenClaw integration:** One config flag:
```json
{
  "memory-tencentdb": {
    "enabled": true
  }
}
```

**Argument:** Memory should work out of the box. Local SQLite means zero cloud dependencies, zero API costs, zero data egress concerns. Optional Tencent Cloud Vector Database (TCVDB) for scale.

### Argument H: Agent Tools for Memory Access
Two tools exposed to agents:
- `tdai_memory_search` — search layered memory
- `tdai_conversation_search` — search raw conversation history

Both return references with `node_id` and `result_ref` fields for traceback.

**Argument:** Agents need explicit tools to access memory — not just implicit context injection. Tool-based access gives agents agency over what they retrieve.

---

## 📊 IV. The Empirical Arguments (Benchmark Results)

**Important caveat:** "These numbers come from Tencent's own evaluations" — self-reported, not third-party verified.

### Short-Term Memory Benchmarks (with OpenClaw plugin)

| Benchmark | OpenClaw Alone | + Plugin | Relative Δ | Tokens (Alone → Plugin) | Token Δ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WideSearch** | 33% | **50%** | **+51.52%** | 221.31M → 85.64M | **−61.38%** |
| **SWE-bench** | 58.4% | **64.2%** | +9.93% | 3474.1M → 2375.4M | −33.09% |
| **AA-LCR** | 44.0% | **47.5%** | +7.95% | 112.0M → 77.3M | −30.98% |

### Long-Term Memory Benchmark

| Benchmark | Without | + Plugin | Improvement |
| :--- | :--- | :--- | :--- |
| **PersonaMem** | 48% | **76%** | **+59% relative** |

**Critical methodological note:**
> *"These results are measured over continuous long-horizon sessions, not isolated turns. For example, SWE-bench runs 50 consecutive tasks per session to simulate the context-accumulation pressure of real-world long-horizon agents."*

**Argument:** Traditional benchmarks test isolated turns. Real agents face context accumulation over many consecutive tasks. Measuring over 50-task sessions reveals memory degradation that single-turn benchmarks miss.

---

## 🚫 V. The Anti-Arguments (What TencentDB Rejects)

| Rejected Practice | TencentDB Alternative |
| :--- | :--- |
| **Flat vector memory** | 4-tier semantic pyramid (L0→L1→L2→L3) |
| **Blind similarity search** | Progressive disclosure + hybrid retrieval + drill-down |
| **Irreversible summarization** | Deterministic path from abstraction to evidence |
| **Black-box debugging** | Human-readable Markdown + Mermaid + `node_id` traceability |
| **External API dependencies** | Local SQLite + sqlite-vec by default |
| **Single retrieval method** | Hybrid (BM25 + vector + RRF) |
| **Manual memory management** | Automatic capture, extraction, and recall |
| **Framework lock-in** | OpenClaw plugin + Hermes Gateway adapter |

---

## 🏛️ VI. The Philosophical Core (Eight Sentences)

1. **Memory is about sparing humans from having to repeat themselves** — not about hoarding everything in the AI.
2. **Memory should never be flat** — both its formation and recall must be hierarchical.
3. **Lower layers preserve evidence; upper layers preserve structure** — different representations for different purposes.
4. **Compression without traceability is unacceptable** — every abstraction must have a deterministic path back to evidence.
5. **Mermaid is maximum semantics in minimum symbols** — precise enough for LLMs, concise enough for humans.
6. **Debuggability requires white-box intermediates** — Markdown, Mermaid, and `node_id` tracing are not optional.
7. **Local-first is production-first** — zero external API dependencies means zero data egress, zero vendor lock-in.
8. **Configuration should scale with expertise** — sensible defaults for daily use, deep knobs for advanced tuning.

---

## 🧠 VII. Lessons and Wisdom Extracted

### Lesson 1: Flat Memory is a Failure Mode
Vector similarity is not a substitute for structure. Without hierarchy, memory retrieval is guessing, not reasoning.

### Lesson 2: Progressive Disclosure is the Correct Pattern
Good memory systems present the right level of detail for the current need — macro guidance first, evidence on demand.

### Lesson 3: Two Storage Tiers, Two Purposes
Databases optimize for retrieval; Markdown optimizes for human inspection. Use both for their respective strengths.

### Lesson 4: Traceability is Non-Negotiable
If you cannot trace a memory back to its source, you cannot trust it. Irreversible compression is acceptable for summarization but unacceptable for memory systems.

### Lesson 5: Mermaid is Underrated for Agent Context
The ideal intermediate representation for agent memory is human-readable and machine-parseable. Mermaid (flowcharts, sequence diagrams, state machines) fits this niche perfectly.

### Lesson 6: Context Offloading Requires Retrieval Index
Offloading without indexing is just deletion. The `node_id` provides the index that makes offloaded content retrievable.

### Lesson 7: Persona Accuracy is a Memory Problem, Not a Model Problem
A 28-point gain from better memory architecture (not a better LLM) demonstrates that memory design matters as much as model capability.

### Lesson 8: Long-Horizon Evaluation Reveals Memory Failure
Single-turn benchmarks hide memory degradation. Long-horizon evaluation (50+ consecutive tasks) reveals whether memory actually persists.

### Lesson 9: White-Box is a Feature, Not a Nice-to-Have
When memory fails, engineers need to know why. White-box intermediates (Markdown, Mermaid, JSONL) transform debugging from guessing to tracing.

### Lesson 10: Zero-Config is a Deployment Requirement
If installation takes more than one config flag, many users will never try it. Zero-config defaults (SQLite, hybrid retrieval, automatic capture) lower the barrier to entry.
