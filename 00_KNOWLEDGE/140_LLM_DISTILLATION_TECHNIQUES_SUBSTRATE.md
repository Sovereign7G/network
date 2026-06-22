# LLM Distillation: Technical Substrate (Formalized)
## Model-to-Model Knowledge Transfer Mechanisms

In the Age Republic's cognitive hierarchy, intelligence is formalized as a function of information density and computational efficiency. This substrate documents the mathematical axioms and technical implementations of distillation.

---

### 1. Formal Definitions & Notation
Let:
- \( \mathcal{V} \): Vocabulary set, \( |\mathcal{V}| = V \) (typically \( V > 10^5 \)).
- \( \mathcal{T} \): Teacher model (\( \theta_T \)); \( \mathcal{S} \): Student model (\( \theta_S \)), where \( |\theta_S| \ll |\theta_T| \).
- \( P_{\mathcal{M}}(y | x) \): Softmax probability distribution over \( \mathcal{V} \) produced by model \( \mathcal{M} \).
- \( \hat{y}_{\mathcal{M}}(x) \): Hard (discrete) output of model \( \mathcal{M} \).
- \( \text{KL}(P \parallel Q) \): Kullback–Leibler divergence (information gain) from \( Q \) to \( P \).

### 2. Axioms of Distillation
**Axiom I (Capability Transfer)**: If a teacher \( \mathcal{T} \) exhibits capability \( C \) on input distribution \( \mathcal{X} \), there exists a training procedure such that a student \( \mathcal{S} \) exhibits \( C \) with fidelity \( \delta \geq 0 \), where \( \delta \) is inversely related to the parameter ratio \( |\theta_S| / |\theta_T| \).

**Axiom II (Information Content Hierarchy)**: Let \( I_{\text{label}} \) be information in a hard token. Let \( I_{\text{soft}} \) be information in the teacher's full distribution. Then:
\[ I_{\text{soft}} \geq I_{\text{label}} + H(P_{\mathcal{T}} | x) \]
where \( H(P_{\mathcal{T}} | x) \) is the **Dark Knowledge** (Shannon entropy).

---

### 3. Implementation Manifolds

#### 3.1 Soft-Label Distillation (Logit Optimization)
Soft-label distillation minimizes the weighted KL-divergence between teacher and student distributions.

*   **Objective Function**:
    \[ \mathcal{L}_{\text{soft}}(\theta_S) = \mathbb{E}_{(x, y^*) \sim \mathcal{D}} \left[ \lambda \cdot \mathcal{L}_{\text{CE}}(y^*, P_{\mathcal{S}}(x)) + (1-\lambda) \cdot T^2 \cdot \text{KL}\left(P_{\mathcal{T}}^{(T)}(x) \;\middle\|\; P_{\mathcal{S}}^{(T)}(x)\right) \right] \]
*   **The Gradient Advantage**: The gradient of \( \mathcal{L}_{\text{soft}} \) is non-zero for all vocabulary items \( v \in \mathcal{V} \), providing a much richer signal than cross-entropy (which is zero for all tokens except the ground truth).
*   **Scaling Solutions**: Sparse Distillation (Top-K logits) or Online Inference to mitigate the \( O(N \cdot V) \) memory bottleneck.

#### 3.2 Hard-Label Distillation (Synthetic Siphoning)
The pragmatic standard for black-box teachers (e.g., GPT-4o).

*   **Objective Function**:
    \[ \mathcal{L}_{\text{hard}}(\theta_S) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \mathcal{L}_{\text{CE}}\left( \hat{y}_{\mathcal{T}}(x),\; P_{\mathcal{S}}(x) \right) \right] \]
*   **Chain-of-Thought (CoT)**: By distilling the teacher's **Reasoning Traces**, the student learns the *deductive process* rather than just the final token.
*   **Ceiling Constraint**: Without ground-truth mixing, the student's ceiling accuracy is bounded by the teacher's accuracy: \( \lim_{N \to \infty} \text{Acc}(\mathcal{S}) \leq \text{Acc}(\mathcal{T}) \).

#### 3.3 Co-Distillation (Online Mutual Evolution)
Simultaneous training of teacher and student.

*   **Objective Function**:
    \[ \mathcal{L}_{\text{co}}(\theta_S, \theta_T) = \mathbb{E}_{(x, y^*) \sim \mathcal{D}} \left[ \mathcal{L}_{\text{CE}}(y^*, P_{\mathcal{T}_t}) + \beta \cdot \text{KL}\left(P_{\mathcal{T}_t} \| P_{\mathcal{S}_t}\right) + \gamma \cdot \mathcal{L}_{\text{CE}}(y^*, P_{\mathcal{S}_t}) \right] \]
*   **Dynamic Stability**: Requires a scheduled parameter \( \beta(t) = \beta_{\max} \cdot (1 - e^{-t/\tau}) \) to prevent early-stage teacher noise from corrupting the student's initial weights.

---

### 4. Advanced Scaling Techniques
*   **Sequence-Level Distillation**: Alignment of hidden states or attention patterns for deeper architecture transfer.
*   **Temperature Annealing**: Starting at high \( T \) (e.g., 4–10) to expose dark knowledge, then converging to \( T=1 \).
*   **Hybrid Grounding**: Maintaining ~20% human-verified data in all distillation loops to prevent **Model Collapse** and preserve cognitive diversity.

---
*Documented for the Age Republic by Arham Islam & Antigravity*
