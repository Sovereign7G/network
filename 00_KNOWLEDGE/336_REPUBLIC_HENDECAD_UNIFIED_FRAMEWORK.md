# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/336_REPUBLIC_HENDECAD_UNIFIED_FRAMEWORK`
## Theme: The Sovereign Hendecad — Eleven Unified Principles for AI Agent Systems & Security

---

> [!IMPORTANT]
> **MASTER SYNTHESIS DOCUMENT:**
> This manifest unifies all eleven paradigms analyzed across the ERA 225.0 research cycle into a single, coherent framework of principles for building AI agent systems. The eleven paradigms are: **Acontext**, **Turbovec**, **Context-Aware Semantic Search**, **Agentic Compliance**, **Qwen3.7-Max**, **OSWorld**, **ACC**, **GBrain**, **Bumblebee**, **MLLMs (Forbes)**, and **SuperClaude**.

---

## 🧭 I. The Eleven Paradigms: Origin and Thesis

| # | Paradigm | Source | Core Thesis |
| :--- | :--- | :--- | :--- |
| 1 | **Acontext** | Acontext project | Skill is memory. Store agent state as human-readable Markdown files tracked in Git. |
| 2 | **Turbovec** | Turbovec research | Math replaces k-means training. Data-oblivious quantization with SIMD scanning eliminates training-dependent vector indexing. |
| 3 | **Context-Aware Search** | Semantic search research | Filter first, score second. Boolean metadata pre-filtering before vector similarity eliminates irrelevant candidates at zero compute cost. |
| 4 | **Agentic Compliance** | Compliance architecture | Compliance is path of least resistance. MCP server proxies enforce in-flight masking, virtualized sandboxes, and synthetic data provisioning. |
| 5 | **Qwen3.7-Max** | Alibaba Qwen research | Autonomy is hours, not turns. Tripartite decoupling (Task, Tool, Validator) enables persistent background engineering loops. |
| 6 | **OSWorld** | OSWorld benchmark | UI screens are the human interface. Agents must master OS-level visual grounding with execution-based verification. |
| 7 | **ACC** | arXiv 2605.21850 | Unmask observations; convert procedure into content. Compile multi-turn trajectories into single long-context QA pairs for direct supervision. |
| 8 | **GBrain** | Marktechpost / Garry Tan | Thin harness, fat skills in markdown. Self-wiring knowledge graphs via regex inference cascades over PGLite WASM. |
| 9 | **Bumblebee** | Perplexity (open-source) | The scanner must not become the attack. Read-only, zero-dependency static manifest parsing for supply-chain security. |
| 10 | **MLLMs** | Forbes / Werner | Reasoning must be grounded in observation. Attach sensory gear to the LLM brain; compress with token sparsification for 75% FLOP reduction. |
| 11 | **SuperClaude** | Marktechpost tutorial | Behaviors belong in Markdown, not model weights. Dynamic prompt-time composition from reusable file assets with session serialization. |

---

## 🏛️ II. The Seven Unified Principles

From eleven paradigms, seven fundamental principles emerge. Each principle is supported by multiple paradigms — no single paradigm invented the principle, but each contributes evidence.

---

### Principle 1: Markdown Is the Sovereign Medium

**Statement:** All persistent agent state — knowledge, skills, behavioral instructions, and memory — should be stored as plain-text Markdown files on a local filesystem, tracked by Git.

**Supporting paradigms:**

| Paradigm | What it stores in Markdown | Why |
| :--- | :--- | :--- |
| **Acontext** | Agent skills and task state | Human-readable, Git-portable, epistemic pruning |
| **GBrain** | Knowledge notes with wikilinks | Source of truth for graph extraction and hybrid search |
| **SuperClaude** | Behavioral instructions (commands, agents, modes) | Dynamic prompt assembly, convention-based discovery |

**The convergence:** Three independent projects — a memory layer, a knowledge graph, and a prompt framework — all converge on the same medium: flat Markdown files in a directory structure. This is not coincidence. Markdown is:
- **Human-auditable** — readable in any text editor
- **Version-controllable** — diffable via Git
- **Machine-parseable** — structured enough for regex, frontmatter, and wikilink extraction
- **Portable** — no database server, no vendor lock-in

**Axiom:** If the human curator cannot audit the system state using a basic text editor, the system violates cognitive sovereignty.

---

### Principle 2: Hybrid Multi-Dimensional Retrieval

**Statement:** No single retrieval method is sufficient. Sovereign systems must combine dense vector similarity, sparse keyword matching, typed graph traversals, and metadata pre-filtering — fusing results via Reciprocal Rank Fusion (RRF).

**Supporting paradigms:**

| Paradigm | Retrieval contribution |
| :--- | :--- |
| **Turbovec** | Hardware-accelerated dense vector scans (SIMD, AVX-512/NEON, 2-bit/4-bit quantization) |
| **Context-Aware Search** | Boolean metadata pre-filtering before vector scoring; constraint-first execution |
| **GBrain** | Deterministic graph traversals from regex-extracted wikilink edges; RRF fusion of vector + BM25 + graph |

**The convergence:** Vector search misses exact keywords. Keyword search misses synonyms. Both miss typed relationships ("Who works at Acme?"). Only a multi-dimensional pipeline — pre-filtered by metadata constraints, scored across dense vectors and sparse keywords, traversed through typed graph edges, and fused via RRF — achieves sovereign-grade retrieval precision.

**Axiom:** Apply constraints before computation. Filter metadata (boolean masks) before vector scoring. Extract graph edges deterministically (regex) before calling LLMs.

---

### Principle 3: Non-Invasive Observation

**Statement:** The act of inspecting, scanning, or auditing a system must never alter the state being inspected, trigger code execution, or introduce new dependencies.

**Supporting paradigms:**

| Paradigm | What it observes without modifying |
| :--- | :--- |
| **Bumblebee** | Package lockfiles, extension manifests, MCP configs — never runs `npm install` or `pip` |
| **OSWorld** | Screenshots and GUI coordinates — observe-then-act, never modify state during observation |
| **Agentic Compliance** | In-flight API traffic through proxy monitoring — read without intercepting |
| **GBrain** | Markdown files parsed via regex — never modifies source files during graph extraction |

**The convergence:** In security (Bumblebee), a scanner that runs package manager commands triggers the very attack it's looking for. In grounding (OSWorld), an agent that modifies state before observing it cannot verify its actions. In memory (GBrain), modifying source files during indexing creates inconsistency. The principle is universal: **observe first, act second, never conflate the two**.

**Axiom:** A scanner that invokes `npm` to check exposure has already triggered the attack. A grounding agent that acts before observing cannot verify. Read-only is not a feature — it is a security and correctness requirement.

---

### Principle 4: Dynamic Composition over Static Configuration

**Statement:** Agent behaviors, system prompts, retrieval pipelines, and knowledge graphs should be assembled dynamically at execution time from modular, independent building blocks — not baked into static configurations or model weights.

**Supporting paradigms:**

| Paradigm | What it composes dynamically |
| :--- | :--- |
| **SuperClaude** | System prompts from Commands + Agents + Modes Markdown files |
| **GBrain** | Knowledge graphs from regex inference cascades over wikilinks at ingest time |
| **Context-Aware Search** | Query execution plans from metadata constraints + embedding dimensions |
| **ACC** | Training examples from compiled multi-turn trajectory logs |

**The convergence:** SuperClaude composes prompts. GBrain composes graphs. Context-Aware Search composes query plans. ACC composes training data. In every case, the system avoids monolithic static artifacts (one mega-prompt, one pre-built graph, one fixed query template, one labeled dataset) in favor of **dynamic assembly from modular primitives**.

**Axiom:** Composition beats fine-tuning. Assemble behaviors at prompt time from reusable building blocks rather than training separate models.

---

### Principle 5: Persistent, Detached, Cost-Bounded Execution

**Statement:** Autonomous engineering requires background execution that survives context restarts and network failures, with strict financial and temporal governance to prevent runaway loops.

**Supporting paradigms:**

| Paradigm | Persistence mechanism | Governance mechanism |
| :--- | :--- | :--- |
| **Qwen3.7-Max** | Detached PTY loops via RMUX terminal multiplexers | Tripartite decoupling (Task, Tool, Validator); secondary watchdog agents |
| **GBrain** | Cron-driven Autopilot with 5-minute tick loop | Cost-capped remediation plans (`--max-usd 5`) |
| **SuperClaude** | Session JSON save/load across restarts | Explicit history serialization with metadata |
| **Bumblebee** | One-shot scans, externally scheduled (cron/systemd) | No daemon overhead; operator controls cadence |

**The convergence:** True engineering autonomy spans hours or days, not single API calls. Four paradigms independently converge on the same pattern: **detach execution from the interactive session, persist state to disk, and govern resource consumption with hard limits**. Whether it's a terminal multiplexer (Qwen), a cron job (GBrain/Bumblebee), or a JSON checkpoint (SuperClaude), the principle is identical.

**Axiom:** Never let the optimizing engine govern its own resource budget. Always keep the cost limiter strictly separated from the execution sandbox.

---

### Principle 6: Grounded Physical and Visual Reasoning

**Statement:** Agents that operate on text-only abstractions cannot reliably interact with physical systems, GUIs, or sensor streams. Grounded reasoning requires direct visual/sensory observation with efficient token compression.

**Supporting paradigms:**

| Paradigm | Grounding modality | Efficiency mechanism |
| :--- | :--- | :--- |
| **OSWorld** | Desktop screenshots + mouse/keyboard coordinates | Parallel headless VMs with KVM acceleration |
| **MLLMs (Forbes)** | IoT sensors, cameras, wearables | Token sparsification: 75% FLOP reduction |
| **ACC** | Multi-turn trajectory logs (tool outputs, screenshots, DB queries) | Compile trajectories into single long-context QA pairs |

**The convergence:** OSWorld grounds agents in desktop GUIs. MLLMs ground agents in physical sensor streams. ACC compiles these observations into training data. All three independently prove that **text-only reasoning is insufficient for real-world autonomy** — but all three also prove that raw multimodal input must be compressed (token sparsification, trajectory compilation) to remain computationally viable.

**Axiom:** Physics is learned by seeing, not reading. But uncompressed visual tokens scale quadratically — sparsify before attending.

---

### Principle 7: Explicit Boundary Auditing and Compliance

**Statement:** As agents acquire system-level permissions through tool registries (MCP servers, browser extensions, editor plugins), these boundaries must be continuously audited, sandboxed, and governed — treating tool configurations as sensitive access control records.

**Supporting paradigms:**

| Paradigm | Boundary type | Enforcement mechanism |
| :--- | :--- | :--- |
| **Agentic Compliance** | API and database access | MCP proxy servers with in-flight masking and synthetic data provisioning |
| **Bumblebee** | Package managers, extensions, MCP configs | Static, read-only manifest scanning with exposure catalogs |
| **SuperClaude** | Behavioral instructions | Explicit conflict resolution rule (framework > user) |
| **Qwen3.7-Max** | Execution scope | Validator agent independent from Task agent |

**The convergence:** Compliance governs what the agent can access. Bumblebee audits what tools are installed. SuperClaude constrains what behaviors are active. Qwen separates who proposes from who validates. All four address the same meta-problem: **agents with broad permissions need explicit, auditable, enforceable boundaries**.

**Axiom:** Treat MCP configuration files as highly sensitive access control records. Inventory them without leaking their secrets. Separate the scanner from the intelligence catalog. Separate the executor from the validator.

---

## 🔬 III. The Eleven-Way Philosophical Matrix

| Dimension | Acontext | Turbovec | Ctx Search | Compliance | Qwen3.7 | OSWorld | ACC | GBrain | Bumblebee | MLLMs | SuperClaude |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Medium** | Markdown | Vectors | Embeddings | Sandboxes | PTY logs | Screenshots | Trajectories | Md + PGLite | Manifests | Sensors | Md assets |
| **P1 (Markdown)** | ✅ Core | — | — | — | — | — | — | ✅ Core | — | — | ✅ Core |
| **P2 (Hybrid)** | — | ✅ Core | ✅ Core | — | — | — | — | ✅ Core | — | — | — |
| **P3 (Read-Only)** | — | — | — | ✅ | — | ✅ | — | ✅ | ✅ Core | — | — |
| **P4 (Dynamic)** | — | — | ✅ | — | — | — | ✅ | ✅ | — | — | ✅ Core |
| **P5 (Persistent)** | — | — | — | — | ✅ Core | — | — | ✅ | ✅ | — | ✅ |
| **P6 (Grounded)** | — | — | — | — | — | ✅ Core | ✅ Core | — | — | ✅ Core | — |
| **P7 (Boundary)** | — | — | — | ✅ Core | ✅ | — | — | — | ✅ Core | — | ✅ |

---

## 🏛️ IV. The Twelve Tensions and Their Resolutions

The eleven paradigms create productive tensions. Below are twelve key tensions, each resolved by combining insights from multiple paradigms.

### T1. Text-Only Reasoning vs. Grounded Observation
- **Tension:** Acontext/SuperClaude are text-centric; OSWorld/MLLMs demand visual grounding.
- **Resolution:** Use text (Markdown) as the storage and behavioral medium. Use vision as the observation and interaction medium. Compile visual observations into text-based training data (ACC) and distill outcomes into Markdown state (Acontext).

### T2. Opaque Databases vs. Inspectable Files
- **Tension:** Turbovec/pgvector need binary vector indexes for speed. Acontext/GBrain demand human-readable files.
- **Resolution:** Markdown is the source of truth; databases are ephemeral accelerators. If the database is deleted, rebuild it from the files. Never the reverse.

### T3. Static Prompts vs. Dynamic Composition
- **Tension:** Large monolithic system prompts waste tokens and cause role drift. But minimal prompts lack specificity.
- **Resolution:** SuperClaude's pattern — store behavioral assets as modular Markdown files, assemble dynamically at prompt time based on the active command/agent/mode.

### T4. Continuous Daemon vs. One-Shot Scanner
- **Tension:** Bumblebee argues one-shot is cleaner. Qwen3.7-Max argues persistent loops are necessary.
- **Resolution:** Different tools for different concerns. Security scanning should be one-shot (no attack surface). Engineering optimization should be persistent but cost-bounded. Let the OS schedule both.

### T5. Zero Dependencies vs. Rich Libraries
- **Tension:** Bumblebee uses zero non-stdlib Go dependencies. GBrain uses PGLite WASM + pgvector.
- **Resolution:** Security-critical tools (scanners, auditors) should be dependency-free. Knowledge tools (indexes, search) can use verified, local-first libraries. The risk tolerance depends on the attack surface.

### T6. Fine-Tuning vs. Prompt Composition
- **Tension:** ACC compiles training data to fine-tune smaller models. SuperClaude argues composition beats fine-tuning.
- **Resolution:** Both are necessary at different scales. Use SuperClaude composition for behavioral specialization (cheap, fast, auditable). Use ACC compilation for capability compression (30B model beats 235B on specific tasks after training).

### T7. Token Efficiency vs. Context Richness
- **Tension:** MLLM sparsification discards tokens. ACC argues for unmasking observations (more tokens).
- **Resolution:** Unmask observations during training (ACC). Sparsify observations during inference (MLLMs). The training and inference phases have different token-efficiency requirements.

### T8. Autonomy vs. Governance
- **Tension:** Qwen3.7-Max wants maximum autonomous execution freedom. Agentic Compliance wants maximum constraint.
- **Resolution:** Tripartite decoupling — the Task agent has freedom, the Validator agent has authority, and neither controls the other. Freedom within boundaries, not freedom from boundaries.

### T9. Execution-Based Verification vs. LLM-Based Soft Grading
- **Tension:** OSWorld demands execution-based verification (did the file actually get created?). Softer approaches use LLM-as-judge.
- **Resolution:** Always prefer execution-based verification when possible. Use LLM grading only for subjective qualities (code style, explanation clarity) that cannot be asserted programmatically.

### T10. Convention vs. Configuration
- **Tension:** SuperClaude discovers assets by folder convention. Compliance requires explicit access control lists.
- **Resolution:** Use convention for discoverability (what exists). Use explicit configuration for authorization (what is permitted). Discovery is open; enforcement is strict.

### T11. Local-First vs. Cloud-Scale
- **Tension:** GBrain's PGLite is local WASM. Production systems need cloud database scale.
- **Resolution:** GBrain's migration path: develop locally with PGLite, deploy to Supabase when scale demands it. The migration command is one line. Local-first with a cloud escape hatch.

### T12. Human Review vs. Full Automation
- **Tension:** Bumblebee's threat intel workflow requires human PR review. Qwen3.7-Max aims for fully autonomous loops.
- **Resolution:** Automate generation. Require human review for policy changes. The human reviews the catalog (what to look for), not every scan (what was found). Authority flows from humans; execution flows from machines.

---

## 🏛️ V. The Master Axioms of the Sovereign Hendecad

### Axiom 1: The Source of Truth Belongs to the Human
All knowledge, skills, behaviors, and memory traces must ultimately live in open, version-controlled, human-readable text files. Binary databases are ephemeral accelerators. If the human cannot audit the state with a text editor, the system has failed.

### Axiom 2: Composition at Prompt Time, Compilation at Train Time
For behavioral specialization, compose system prompts dynamically from modular Markdown assets (SuperClaude pattern). For capability compression, compile multi-turn trajectories into training data (ACC pattern). Both are composition — one at inference, one at training.

### Axiom 3: Filter Before You Score, Observe Before You Act
Apply boolean metadata constraints before vector similarity computation. Observe system state (screenshots, manifests) before modifying it. In both retrieval and action, the constraint phase is computationally cheaper and logically prior.

### Axiom 4: The Scanner Must Not Become the Attack
Security tools must be read-only, dependency-free, and incapable of triggering the vulnerabilities they detect. This principle extends to all observation: indexing should not modify source files, grounding should not alter GUI state during observation, and verification should not have side effects.

### Axiom 5: Detach Execution, Serialize State, Bound Cost
Long-running autonomous work requires persistent execution (terminal multiplexers, cron jobs), serialized state (JSON checkpoints, Git commits), and hard cost limits (USD caps, token budgets). All three are required — any one alone is insufficient.

### Axiom 6: Ground Reasoning in Observation
Text-only reasoning is insufficient for physical systems, GUI interactions, and sensor-driven tasks. Attach visual and sensory inputs to the language core, but compress them aggressively (token sparsification, trajectory compilation) to maintain computational viability.

### Axiom 7: Separate Executor from Validator from Auditor
The agent that proposes an action (Task) must not evaluate its own output (Validator). The tool that scans for vulnerabilities (Bumblebee) must not supply the threat intelligence (exposure catalog). The framework that injects behavioral instructions (SuperClaude) must declare which instructions are active (▶ Active context). Separation of concerns is the foundation of trustworthy autonomy.

---

## 📊 VI. The Hendecad at a Glance

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                   THE SOVEREIGN HENDECAD                        │
    │              Eleven Paradigms, Seven Principles                 │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   STORAGE LAYER          RETRIEVAL LAYER         ACTION LAYER   │
    │   ─────────────          ───────────────         ────────────   │
    │   Acontext (Md)          Turbovec (SIMD)         Qwen3.7 (PTY) │
    │   GBrain (PGLite)        Ctx Search (Filter)     OSWorld (GUI)  │
    │   SuperClaude (Assets)   GBrain (RRF+Graph)      MLLM (Sensor)  │
    │                                                                 │
    │   TRAINING LAYER         SECURITY LAYER                         │
    │   ──────────────         ──────────────                         │
    │   ACC (Trajectories)     Compliance (MCP)                       │
    │   MLLM (Sparsify)        Bumblebee (Scan)                       │
    │                          SuperClaude (Conflict)                  │
    │                                                                 │
    │   SEVEN PRINCIPLES:                                             │
    │   P1. Markdown is sovereign         P5. Persist + bound cost    │
    │   P2. Hybrid multi-dim retrieval    P6. Ground in observation   │
    │   P3. Non-invasive observation      P7. Audit all boundaries    │
    │   P4. Dynamic composition                                       │
    │                                                                 │
    │   SEVEN AXIOMS:                                                 │
    │   A1. Source of truth = human       A5. Detach + serialize      │
    │   A2. Compose at prompt, compile    A6. Ground in observation   │
    │       at train                      A7. Separate executor /     │
    │   A3. Filter before score               validator / auditor     │
    │   A4. Scanner ≠ attack                                          │
    └─────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ VII. Final Synthesis

Eleven independent research efforts — spanning memory management, vector indexing, semantic search, runtime compliance, long-horizon autonomy, OS-level grounding, trajectory compilation, self-wiring knowledge graphs, supply-chain security, multimodal sensing, and prompt orchestration — converge on seven principles and seven axioms.

The convergence is not accidental. It reflects the fundamental requirements of systems that must be:
- **Inspectable** by humans (Markdown, Git, active context headers)
- **Efficient** at machine scale (SIMD, token sparsification, metadata pre-filtering)
- **Persistent** across sessions and failures (JSON checkpoints, terminal multiplexers, cron)
- **Secure** against supply-chain and execution attacks (read-only scanning, zero dependencies, sandboxing)
- **Grounded** in physical and visual reality (screenshots, sensors, trajectory logs)
- **Composable** from modular building blocks (prompt assets, retrieval dimensions, behavioral files)
- **Governed** by explicit, auditable boundaries (validators, exposure catalogs, conflict resolution rules)

These are not merely aspirational guidelines. They are engineering constraints that eleven independent teams discovered through practical implementation. The Sovereign Hendecad codifies them as a unified framework for building the next generation of AI agent systems.
