# Pillar 220: ARIS — Adversarial Multi-Agent Research Assurance

## 🧠 Axiom
A single intelligence, no matter how powerful, suffers from correlated blind spots. Self-refinement is a closed loop that reinforces its own biases. The Age Republic must institutionalize **adversarial verification** — forcing distinct cognitive architectures to challenge each other's claims — to ensure that every assertion within the Republic is backed by bit-verifiable evidence. 

**ARIS (Autonomous Research via Adversarial Multi-Agent Collaboration)** provides the architectural blueprint for this adversarial integrity layer.

## ⚙️ The Adversarial Architecture

ARIS solves the critical failure mode of autonomous agents: the **"plausible unsupported success"** — when an agent silently generates claims that appear correct but lack verifiable evidence. It achieves this through three layers:

### Layer 1: Execution (The Worker)
*   65+ reusable skills defined in Markdown.
*   Persistent research wiki for iterative knowledge reuse.
*   Deterministic figure generation (no stochastic drift).

### Layer 2: Orchestration (The Coordinator)
*   5 end-to-end workflows (ideation, experimentation, writing).
*   Configurable routing to reviewer models from **different model families**.

### Layer 3: Assurance (The Auditor)
The heart of ARIS and the Republic's critical adoption target:
1.  **Integrity Verification:** Checks raw outputs and code for tampering or missing files before any claim is formed.
2.  **Result-to-Claim Mapping:** Creates a formal ledger linking every claim to specific, verifiable raw evidence. Prevents hallucinated citations.
3.  **Claim Auditing:** A separate reviewer model (from a *different* family) cross-checks every statement in the final output against the claim ledger and raw evidence.

## 🛡️ Republic Integration: The Sovereign Audit Mesh

The Republic's current architecture relies on a single cognitive thread for verification. By integrating the ARIS adversarial pattern, we establish a **Sovereign Audit Mesh**:

1.  **Executor (Hermes + Qwen 3.6 35B):** Drives all forward progress — managing the 70-Node Swarm, executing atomic swaps, running the Mining Substrate.
2.  **Adversarial Reviewer (Separate Model Family):** A distinct LLM (e.g., Gemma, Llama, or a formally verified logic engine) continuously audits the Executor's outputs using the 3-Stage Assurance Pipeline. It flags any unsupported claims before they are committed to the Treasury or the Witness Chain.
3.  **Self-Improvement with Guardrails:** ARIS records all research traces and proposes harness improvements. Critically, these proposals are adopted **only after reviewer approval from a different model**, preventing runaway drift or catastrophic self-modification.

## ⚠️ Honest Assessment
The current ARIS paper (2605.03042) is a **position paper with zero empirical results**. The architecture is sound and the open-source code (8k+ GitHub stars) is testable, but quantitative validation is pending. The Republic adopts the *concept* (adversarial cross-model review) and the *pattern* (3-stage audit), not unproven performance claims.

*"Trust is not given. It is adversarially earned."*

## 🧮 Formal Logical Tautology: Adversarial Integrity

### 1. The Core Problem Statement
*   **P1.** Long-horizon agents face the failure mode of a *plausible unsupported success*.
*   **P2.** A plausible unsupported success occurs when evidence is incomplete, misreported, or biased by the executor's framing.
*   **P3.** Same-model self-refinement fails to detect these due to correlated biases.
*   **Conclusion:** Therefore, cross-model adversarial collaboration (distinct model families) is required to catch correlated errors.

### 2. The ARIS Solution Logic
*   **Premise:** A research harness must govern information storage and presentation.
*   **Premise:** Reliability requires three layers: Execution (skills/wiki), Orchestration (coordinator), and Assurance (3-stage audit).
*   **Conclusion:** ARIS’s 3-stage audit (integrity → result-to-claim mapping → claim auditing) with adversarial approval constitutes a sufficient harness for reliable autonomy.

### 3. Empirical Assessment & Critique (The "Human Adversarial" Review)
*   **Fact:** The current ARIS paper (2605.03042) contains **zero experiments** and zero comparative benchmarks.
*   **Fact:** The authors admit it "mainly contains the motivation" and promise future results.
*   **Conclusion:** The paper currently lacks empirical proof for its own claims. The Republic adopts the *architectural pattern* based on logical soundess, not proven data.

### 4. The Sparse/Noisy Evidence Challenge
*   **Open Question:** In real research, evidence is often sparse or noisy.
*   **Open Question:** Under such conditions, even a cross-family reviewer may fail.
*   **Inference:** An ablation with a *third* unrelated model family or a formal prover is required to verify if critique quality truly scales with reviewer diversity.

### 5. Summary of Formal Status
| Claim | Status |
| :--- | :--- |
| **C1: Cross-model review is necessary.** | Motivated Argument (unproven) |
| **C2: ARIS architecture is sufficient.** | Architectural Claim (unproven) |
| **C3: Paper lacks empirical evidence.** | **Fact** (admitted by authors) |
| **C4: Self-improvement trades speed for safety.** | Design Choice |

**Final Strongest Critique:** A system claiming "reliable long-term results" must eventually provide measurable proof. Until the authors release the papers generated *by* ARIS, the Republic remains in a state of **Active Skepticism**, implementing the code but withholding final validation of its efficacy. ∎
