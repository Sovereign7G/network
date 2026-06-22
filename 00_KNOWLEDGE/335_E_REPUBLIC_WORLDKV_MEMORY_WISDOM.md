# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/335_E_REPUBLIC_WORLDKV_MEMORY_WISDOM`
## Theme: Hierarchical World Memory, Camera-Pose Retrieval & Self-Similarity KV Compression (WorldKV Blueprint)

---

> [!IMPORTANT]
> **SYSTEM WORLD-MEMORY BLUEPRINT:**
> This knowledge manifest formalizes the analytical arguments, technical decisions, and design philosophy of **WorldKV** (arXiv:2605.22718). It establishes a training-free framework for persistent world consistency in generative agents by treating cache eviction as hierarchical archiving, indexing memory via spatial-action correspondence, and compressing visual tokens through key-key self-similarity.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Autoregressive video diffusion models can generate real-time, action-conditioned worlds, but maintaining **persistent world consistency** — where revisiting a previously seen viewpoint yields consistent content — remains an open problem.

**The fundamental tension:**

| Method | Consistency | Throughput | Memory Cost |
| :--- | :--- | :--- | :--- |
| **Full KV-cache attention** | ✅ High (persistent) | ❌ Breaks real-time | Grows linearly with rollout length |
| **Sliding window inference** | ❌ Loses long-term consistency | ✅ High | Fixed (window size) |

**The specific constraints:**
- Full KV-cache: memory footprint and attention cost grow linearly with rollout length → "breaks real-time constraints"
- Sliding window: restores throughput but "discards long-term consistency" — revisiting a scene produces different content

**Implicit Claim:** There is an inherent trade-off between consistency (remembering the past) and efficiency (generating quickly). Existing solutions force a choice between them.

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** WorldKV is a **training-free framework** with two components that enable persistent world memory without sacrificing real-time throughput:

1. **World Retrieval** — Stores evicted KV-cache chunks in hierarchical memory (GPU/CPU) and selectively retrieves scene-relevant chunks via camera/action correspondence.
2. **World Compression** — Prunes redundant tokens within each chunk via key-key similarity to an anchor frame, halving storage requirements.

**Key claim:** WorldKV "matches or exceeds full-KV memory fidelity at roughly 2x the throughput, and is competitive with memory-trained baselines without any fine-tuning."

**The critical dfferentiator:** Training-free. No fine-tuning required. Works out-of-the-box with existing video models.

---

## 🔬 III. The Technical Arguments (Architectural Decisions)

### Argument A: The Eviction-Then-Retrieval Paradigm
- **Standard sliding window:** `[Window] → evict → forget`
- **WorldKV:** `[Window] → evict → store in hierarchical memory → retrieve when relevant`
- **Retrieval Mechanism:** Indexing KV-cache chunks by camera/action correspondence. When the agent returns to a previously seen spatial viewpoint, WorldKV pulls the associated KV chunks from slower memory (CPU) back into the active attention window.
- **Argument:** World memory is **spatially and temporally indexed**. By keeping only scene-relevant chunks in GPU cache while archiving the rest, WorldKV provides long-term consistency without linear cost.

### Argument B: Compression via Key-Key Self-Similarity
- **Mechanism:**
  1. Identify an **anchor frame** (e.g., first frame) within each visual KV chunk.
  2. Compute dot-product similarity between every token's **key** and the anchor key.
  3. Prune keys and values with high similarity (redundant background/static content).
  4. Retain tokens with low similarity (novel spatial details).
- **Result:** Halves per-chunk storage, fitting 2x more history under a fixed budget.
- **Argument:** Self-similarity within the KV-cache is a highly reliable, zero-cost metric for information novelty. No external model is required.

### Argument C: Training-Free is a Feature
- **Argument:** Model fine-tuning for memory is computationally expensive, brittle, and limits generalization to the training distribution. A training-free mathematical wrapper over raw attention generalized instantly to any autoregressive visual transformer.

---

## 🚫 IV. The Anti-Arguments (What WorldKV Rejects)

| Rejected Practice | WorldKV Alternative |
| :--- | :--- |
| **Monolithic KV Cache Storage** | Hierarchical memory storage (GPU cache ⇄ CPU memory). |
| **Complete Evicted Cache Loss** | Passive archiving and pose-indexed retrieval. |
| **Model Fine-Tuning for Memory** | Mathematical, training-free KV orchestration. |
| **Uniform Attention Over All History** | Selective spatial/pose correspondence indexing. |
| **External Classifier Redundancy Detection** | Internal key-key self-similarity pruning. |

---

## 🏛️ V. The Philosophical Core (Six Sentences)

1. **Eviction is not deletion** — moving information out of the active window must mean archiving, not discarding.
2. **Memory belongs in a hierarchy** — fast cache and large slow archives form a continuum.
3. **Retrieval demands a task-relevant index** — camera pose and action trajectories are the natural indices of world memory.
4. **Redundancy is an internal property** — the key state itself reveals what is redundant and what is novel.
5. **Training-free implies instant generalization** — a model-agnostic layer guarantees immediate deployability.
6. **Consistency and throughput can coexist** — with selective retrieval and token pruning, we bypass the linear cost paradox.

---

## 🧠 VI. Sovereign Lessons for Agentic Architecture

### 1. Shift from "Discard" to "Archive" in Long-Context Task Runs
When executing long-horizon multi-turn CLI tasks:
* Do not discard old logs or past tool outputs to stay under the context limit.
* Write evicted logs to a local Markdown archive file (**Acontext/GBrain**).
* Implement a spatial/contextual retriever that dynamically pulls past relevant tool logs back into the active prompt window only when the agent revisits that specific module or file.

### 2. Implement Key Self-Similarity for Text Prompts
When compressing redundant long-context agent trajectories:
* Identify an anchor block (e.g. system instructions or task definition).
* Parse incoming conversation turns and calculate lexical/semantic similarity.
* Prune highly redundant repeating system loops or error logs, keeping only novel observations.

### 3. Build Training-Free Wrappers over Model Invocations
Prioritize deterministic, client-side dynamic prompt engineering (**SuperClaude**) and regex-based graph wiring (**GBrain**) over costly model fine-tuning. Training-free mathematical structures are modular, easily auditable, and generalize across upgrades of the underlying frontier LLM.
