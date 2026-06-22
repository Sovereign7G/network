# LLM Distillation: Formal Axioms and Theorems
## The Logic of Cognitive Fidelity

This document formalizes the comparative efficiency and fundamental limits of knowledge transfer between model generations in the Age Republic.

---

### 1. Comparative Theorems

**Theorem I: The Pareto Efficiency Frontier of Distillation**
No single distillation technique can simultaneously maximize information transfer, minimize compute cost, and maintain black-box compatibility. This creates a three-way trade-off manifold:

| Technique | Information Transfer | Compute (Train) | Black-Box Compatible |
| :--- | :--- | :--- | :--- |
| **Soft-label** | High (\( \sim H(P_{\mathcal{T}}) \)) | High (\( O(NV) \)) | No |
| **Hard-label** | Low (\( \sim 1 \) bit) | Low (\( O(N) \)) | **Yes** |
| **Co-distillation** | Medium-High | **Very High** (\( O(2N) \)) | No |

**Theorem II: The Dark Knowledge Necessity**
For tasks requiring out-of-distribution (OOD) reasoning, soft-label distillation yields a relative improvement \( \Delta_{\text{OOD}} \geq 0.15 \) over hard-label distillation. This is because "Dark Knowledge" encodes the semantic feature similarities that prevent brittle decision boundaries.

**Theorem III: Optimal Choice Criterion**
The optimal selection of a distillation technique \( \mathcal{K}^* \) is defined as:
\[
\min_{\text{tech} \in \{\text{soft, hard, co}\}} \left( \alpha \cdot (1 - \text{Fidelity}(\text{tech})) + \beta \cdot \text{Cost}(\text{tech}) + \gamma \cdot \mathbb{I}_{\text{API}}(\text{tech}) \right)
\]
*Justification:* Empirical results from Llama 4 (co-distillation) and DeepSeek R1 (hard-label) confirm these thresholds within specific compute budgets.

---

### 2. Practitioner Corollaries for Sovereign Infrastructure

**Corollary I: The Proprietary Constraint**
When utilizing a proprietary teacher (e.g., GPT-4o, Claude), the Republic is forced into **Hard-Label Distillation**. Mitigation must occur via:
*   **CoT Traces**: Increasing effective information per sample.
*   **Temperature Sampling**: Enhancing synthetic diversity.
*   **Self-Consistency Filtering**: Majority voting across multiple teacher samples to prune hallucinations.

**Corollary II: Compression Ratios**
Co-distillation is only beneficial when the student capacity is significant (\( |\theta_S| \approx 0.5 \cdot |\theta_T| \)). For extreme compression (e.g., 10x smaller models), **Static Soft-Label Distillation** dominates in fidelity.

**Corollary III: Grounding Requirement**
To prevent **Model Collapse** (the degradation of signal across generations), every distilled manifold must maintain a hybrid training loop containing ~20% foundational human-verified data.

---

### 3. Proof Sketches and Intuitions

*   **Richness of Signal**: The soft-label gradient is non-zero for all vocabulary items, allowing the student to learn what a token *is not* as much as what it *is*.
*   **Error Propagation**: Pure hard-label distillation converges to the teacher's decision boundary. If the teacher's error rate is \( \epsilon \), the student's ceiling accuracy is locked at \( 1 - \epsilon \).
*   **Non-Stationary Risk**: In co-distillation, early-stage teacher predictions are random (\( \text{Acc} \approx 1/V \)). Without a stabilization schedule (\( \beta(t) \)), the student's initial weights will be corrupted by noise.

---
*The logic of the student is bounded by the fidelity of the teacher, unless grounded in the truth.*
*— Age Republic Intelligence Doctrine*
