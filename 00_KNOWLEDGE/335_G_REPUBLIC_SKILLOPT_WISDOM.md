# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/335_G_REPUBLIC_SKILLOPT_WISDOM`
## Theme: SkillOpt — Executive Strategy for Self-Evolving Agent Skills in Text-Space

---

> [!IMPORTANT]
> **SYSTEM COMPACT-OPTIMIZER BLUEPRINT:**
> This knowledge manifest formalizes the operational principles, benchmark claims, and engineering strategies of **SkillOpt** (arXiv:2605.23904). It establishes the concept of "Skills as Trainable External Parameters" for frozen agents, leveraging textual learning-rate budgets, validation gates, and rejected-edit buffers to achieve monotonic performance gains with zero runtime deployment overhead.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Current approaches to agent skills are either hand-crafted, generated one-shot, or evolved through loosely controlled self-revision — none of which "behaves like a deep-learning optimizer for the skill, and none of which reliably improves over its starting point under feedback."

**The failure modes of existing skill creation methods:**
| Method | Problem |
| :--- | :--- |
| **Hand-crafted skills** | Manual, non-scalable, expertise-dependent |
| **One-shot LLM generation** | No iterative improvement; first attempt may be suboptimal |
| **Self-revision (loose)** | No systematic optimization; may degrade rather than improve |
| **Trace2Skill, TextGrad, GEPA, EvoSkill** | Unreliable improvement; not guaranteed to beat baseline |

**The deeper problem:**
> *"As AI moves from assistant to worker, the bottleneck is no longer just knowledge — it is procedural capability: tool use, intermediate-state inspection, domain conventions, and recovery from failure."*

**Implicit Claim:** The field lacks a systematic, controllable, optimizer-like approach to skill improvement — one with the same reproducibility and reliability as weight-space optimization in deep learning.

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** SkillOpt is "the first systematic controllable text-space optimizer for agent skills" — treating a natural-language skill as the agent's trainable external state, with stable updates and zero deployment inference overhead.

**The SkillOpt loop:**
```
Rollout → Score → Reflect → Edit → Validate → Accept/Reject → (Repeat)
```

**The optimizer analogy:**
| Neural Network Training | SkillOpt |
| :--- | :--- |
| Model weights (internal) | Skill document (external, text) |
| Forward pass → loss | Rollout → validation score |
| Gradient → weight update | Reflection → add/delete/replace edits |
| Learning rate | Textual learning-rate budget |
| Validation set | Held-out validation score |
| Optimization stability | Rejected-edit buffer, slow/meta update |

**Key claim:** SkillOpt trains the skill as "the external state of a frozen agent" — the underlying LLM does not change. Only the skill document evolves.

---

## 🔬 III. The Technical Arguments

### Argument A: The Skill Should Be Trainable External State
> *"We argue the skill should instead be trained as the external state of a frozen agent, with the same discipline that makes weight-space optimization reproducible."*

**Comparison:**
| Dimension | Traditional Fine-Tuning | SkillOpt |
| :--- | :--- | :--- |
| **What changes** | Model weights | Skill document (text) |
| **Inference overhead** | None (already loaded) | Zero (skill injected into prompt) |
| **Stability** | Requires careful hyperparameters | Rejected-edit buffer + slow updates |
| **Transferability** | Model-specific | Skill document can move across models |
| **Inspectability** | Black box (weights) | White box (text) |
| **Deployment** | Requires model swap | Zero additional cost |

**Argument:** Fine-tuning changes the model. Skill optimization changes the instruction. The latter is cheaper, more inspectable, and more portable.

### Argument B: Systematic Controllable Optimization
**The optimizer model** (separate from the agent model):
1. Takes scored rollouts as input
2. Produces bounded edits: add, delete, or replace on the skill document
3. Edits are constrained by a **textual learning-rate budget** (prevents over-update)

**Validation gate:** An edit is accepted **only when it strictly improves a held-out validation score.**

**Stability mechanisms:**
- Rejected-edit buffer (prevents repeating the same mistakes)
- Epoch-wise slow/meta update (conservative progress)

**Argument:** Skill optimization should be as disciplined as gradient descent — not loosely controlled self-revision that might degrade performance.

### Argument C: Zero Inference Overhead
> *"Zero deployment inference overhead"*

**Contrast with runtime optimization methods:**
- Chain-of-thought tuning: extra tokens per query
- Reflection: multiple model calls
- Self-consistency: sampling multiple times

**SkillOpt:** The optimized skill is just a text document. At deployment, it is injected into the prompt — no additional model calls, no runtime overhead.

### Argument D: Transferable Skills
> *"Optimized skill artifacts retain value when moved across model scales, between Codex and Claude Code execution environments, and to a nearby math benchmark without further optimization."*

**Transfer experiments show:**
- Across model scales (smaller → larger)
- Across execution environments (Codex ↔ Claude Code)
- To nearby benchmarks (no further optimization needed)

**Argument:** Unlike fine-tuned weights (model-specific), optimized skill documents are **portable artifacts** that capture procedural capability in a model-agnostic format.

---

## 📊 IV. The Empirical Arguments (Results)

### Scale and Scope
* **Benchmarks:** 6
* **Target models:** 7
* **Execution harnesses:** 3 (direct chat, Codex, Claude Code)
* **Evaluated cells:** 52
* **SkillOpt results:** **Best or tied on all 52**
* **Competitors beaten per cell:** Human, one-shot LLM, Trace2Skill, TextGrad, GEPA, EvoSkill

**Claim:** "SkillOpt is best or tied on all 52 evaluated (model, benchmark, harness) cells and beats every per-cell competitor."

### Performance Gains (GPT-5.5)
* **Direct chat:** Baseline + **23.5 pts**
* **Codex agentic loop:** Baseline + **24.8 pts**
* **Claude Code:** Baseline + **19.1 pts**

**Argument:** SkillOpt delivers substantial, consistent gains across both direct model calls and complex agentic execution loops.

---

## 🏛️ V. The Design Philosophy

### Principle 1: Skills Are Trainable Parameters
> *"The skill should instead be trained as the external state of a frozen agent"*

**Argument:** The text of a skill document is a form of parameter — one that lives outside the model but influences its behavior. It should be optimizable with the same rigor as weights.

### Principle 2: Optimizer Separates from Agent
SkillOpt uses a **separate optimizer model** (not the agent model) to propose edits. The agent model remains frozen throughout.

**Argument:** The optimizer and the agent have different roles. The optimizer reflects on past performance and suggests improvements; the agent executes. Separation enables specialization.

### Principle 3: Validation Gate Prevents Degradation
> *"An edit is accepted only when it strictly improves a held-out validation score."*

**Argument:** Unconstrained self-improvement can go backward. A validation gate ensures monotonic progress — or at least no regression.

### Principle 4: Textual Learning Rate Prevents Over-Update
> *"A textual learning-rate budget"*

**Argument:** In weight-space, learning rates prevent destructive updates. In text-space, "make at most 3 small changes" serves the same function. The concept generalizes.

### Principle 5: Rejected-Edit Buffer as Momentum/Memory
> *"Rejected-edit buffer"*

**Argument:** Optimizers need to know what *did not* work. A buffer of rejected edits prevents repeating the same mistakes — analogous to momentum in gradient descent.

---

## 🏛️ VI. The Philosophical Framing

### From Assistant to Worker
> *"As AI moves from assistant to worker, the bottleneck is no longer just knowledge — it is procedural capability: tool use, intermediate-state inspection, domain conventions, and recovery from failure."*

**Distinction:**
| Assistant | Worker |
| :--- | :--- |
| Answers questions | Completes tasks |
| Provides information | Performs actions |
| Single-turn or few-turn | Long-horizon, multi-step |
| Knowledge is sufficient | Procedure is critical |

**Argument:** The era of AI as knowledge assistant is giving way to AI as autonomous worker. Worker agents need procedural skills — sequences of actions, tool-use patterns, error recovery strategies — not just facts.

### Skills as the New Adaptation Layer
> *"Optimized, reusable, and inspectable skills could become a new adaptation layer for future agents."*

**The adaptation stack:**
| Layer | What Changes | Cost |
| :--- | :--- | :--- |
| Pre-training | Model weights | Very high |
| Fine-tuning | Model weights | High |
| In-context learning | Prompt | Low |
| **Skill optimization** | **Skill document** | **Low (optimization time only)** |

**Argument:** Skills occupy a sweet spot in the adaptation hierarchy: more expressive than simple prompts, cheaper than fine-tuning, and more portable than either.

---

## 🚫 VII. The Anti-Arguments (What SkillOpt Rejects)

| Rejected Practice | SkillOpt Alternative |
| :--- | :--- |
| **Hand-crafted skills** | Systematic optimization |
| **One-shot LLM skill generation** | Iterative improvement with validation |
| **Loosely controlled self-revision** | Bounded edits + validation gate |
| **Fine-tuning model weights for skills** | Skills as external state (frozen agent) |
| **Runtime optimization (CoT, etc.)** | Zero inference overhead (skills pre-optimized) |
| **Model-specific skill artifacts** | Portable skills (transfer across models, environments) |
| **Unconstrained edits** | Textual learning-rate budget |
| **No memory of what failed** | Rejected-edit buffer |

---

## 🏛️ VIII. The Philosophical Core (Seven Sentences)

1. **The bottleneck for AI workers is procedural capability, not knowledge** — tool use, inspection, conventions, and recovery matter more than facts.
2. **A skill should be trained like a neural network** — with systematic optimization, validation, and stability mechanisms.
3. **The optimizer and the agent should be separate** — one reflects and edits; the other executes.
4. **No edit without validation** — improvement must be measured, not assumed.
5. **A textual learning rate prevents over-update** — bounded edits are safer than open-ended revision.
6. **Rejected edits are learning signals** — knowing what failed prevents repeating mistakes.
7. **Optimized skills are portable artifacts** — they transfer across models, environments, and benchmarks.

---

## 🧠 IX. Lessons and Wisdom Extracted

### Lesson 1: Procedural > Factual for Workers
For autonomous agents, knowing *how* (procedure, tool use, recovery) matters more than knowing *what* (facts). Skill optimization targets the former.

### Lesson 2: External State is Easier to Optimize Than Internal Weights
Fine-tuning changes the model internally. Skill optimization changes the instruction externally. External optimization is cheaper, faster, more inspectable, and more portable.

### Lesson 3: Validation Gates Prevent Degradation
Unconstrained self-improvement can go backward. A validation gate ensures monotonic progress — or at least no regression.

### Lesson 4: Text-Space Needs Learning Rates Too
In weight-space, learning rates prevent destructive updates. In text-space, "make at most 3 small changes" serves the same function. The concept generalizes.

### Lesson 5: Failure Memory is as Important as Success Memory
Optimizers need to know what *did not* work. A buffer of rejected edits prevents repeating the same mistakes — analogous to momentum in gradient descent.

### Lesson 6: Zero Inference Overhead is a Deployment Superpower
Optimization that happens offline (training) and produces a static artifact (skill document) is infinitely more deployable than runtime optimization that adds latency and cost per query.

### Lesson 7: Transferability is the Ultimate Test of Generalization
If a skill only works on one model in one environment, it has overfit. True procedural capability transfers.

### Lesson 8: Skills as Adaptation Layer
The adaptation stack needs a layer between prompting (low expressivity, low cost) and fine-tuning (high expressivity, high cost). Skills — optimizable, portable, inspectable text — fit this niche perfectly.
