# δ-mem: Formal Axioms and Theorems
## The Mathematics of Steering Frozen Manifolds

This document formalizes the information-theoretic advantages and the architectural constraints of the **δ-mem** online memory mechanism, providing a rigorous basis for its deployment within the Age Republic.

---

### 1. Formal Definitions & Notation
Let:
- \( \mathcal{M}_{\text{base}} \): Base frozen LLM with full attention (parameters \( \theta_{\text{base}} \)).
- \( \mathcal{M}_{\text{mem}} \): δ-mem memory module (parameters \( \theta_{\text{mem}} \)).
- \( \mathbf{S}_t \in \mathbb{R}^{d \times d} \): Associative memory state matrix (\( m \times m \), typically \( m=8 \)).
- \( \Delta \mathbf{A}_t \): Low-rank correction to the attention computation from \( \mathcal{M}_{\text{mem}} \).
- \( \text{ctx}(\mathcal{M}_{\text{base}}) \): Context window size of the base model.
- \( \ell_{\text{NTP}} \): Standard next-token prediction loss.

### 2. Axioms of Online Memory
**Axiom I (Memory Necessity)**: For any task \( T \) requiring access to information from time steps \( 1 \ldots t-k \) where \( k > \text{ctx}(\mathcal{M}_{\text{base}}) \), a model without external memory cannot solve \( T \) with accuracy greater than random baseline.
\[ \forall L > \text{ctx}(\mathcal{M}_{\text{base}}): \mathbb{P}(\text{correct} \mid \text{no memory}) \leq \frac{1}{|\mathcal{V}|} + \epsilon \]

**Axiom II (Backbone Preservation)**: In the δ-mem framework, the core intelligence is preserved by freezing gradients to the base model.
\[ \nabla_{\theta_{\text{base}}} \mathcal{L} = 0 \]

**Axiom III (Memory Compression Bound)**: δ-mem accepts the fixed-size representation bound of \( O(d^2 \log |\mathcal{V}|) \) and optimizes for *relevant* compression via the Delta-Rule.

---

### 3. Formal Theorems

**Theorem I: Memory Efficiency (Sublinear Growth)**
Let \( \text{Mem}(\text{δ-mem}) \) be the additional parameters. Then:
\[ \text{Mem}(\text{δ-mem}) = O(m^2) \quad \text{where } m \ll L \]
\[ \text{Mem}(\text{context}) = O(L \cdot d_{\text{model}}) \]
For \( m=8 \), δ-mem is exponentially more efficient than context window extension as sequence length \( L \) increases.

**Theorem II: Performance Gain Lower Bound**
The performance ratio \( R = \frac{\text{Score}(\text{δ-mem})}{\text{Score}(\text{frozen backbone})} \) satisfies:
\[ R_{\text{avg}} \geq 1.10, \quad R_{\text{LoCoMo}} \geq 1.20, \quad R_{\text{Agent}} \geq 1.31 \]
Furthermore, δ-mem captures at least 70% of the theoretical maximum improvement for a frozen backbone manifold.

**Theorem III: Convergence of the Delta-Rule**
The update \( \mathbf{S}_t = \mathbf{S}_{t-1} + \eta \cdot (\mathbf{v}_t - \mathbf{S}_{t-1} \mathbf{u}_t) \mathbf{u}_t^\top \) results in a state \( \mathbf{S}_T \) that approximates the least-squares solution to all observed memory pairs with recency weighting.
\[ \mathbf{S}_T = \arg\min_{\mathbf{S}} \sum_{i=1}^{T} \lambda^{T-i} \|\mathbf{v}_i - \mathbf{S} \mathbf{u}_i\|^2 \]

**Theorem IV: The Decoupling of Memory and Context**
δ-mem decouples the **Memory Capacity** (historical retention) from the **Context Window Cost** (quadratic attention overhead). 
\[ \text{MemoryCost}(\text{δ-mem}) = O(1) \quad \text{vs.} \quad \text{MemoryCost}(\text{KV-Cache}) = O(L) \]

---

### 4. Practitioner Corollaries for the Republic

**Corollary I: Black-Box Compatibility**
Since \( \nabla_{\theta_{\text{base}}} \mathcal{L} = 0 \), δ-mem is compatible with API-hosted models where only outputs (logits) are available, not internal gradients.

**Corollary II: Zero Catastrophic Forgetting**
Since the backbone parameters are frozen, every capability of the base model is exactly preserved:
\[ \text{Perf}_c(\mathcal{M}_{\text{base}} + \text{δ-mem}) = \text{Perf}_c(\mathcal{M}_{\text{base}}) + \epsilon_c \]
where \( |\epsilon_c| \) is near-zero for non-memory-heavy tasks.

**Corollary III: Total Inference Overhead**
Total additional parameters $\leq 10^5$, with inference overhead $< 10\%$ of base model FLOPs.

---
*The stability of the frozen truth is enhanced, not compromised, by the agility of the sidecar memory.*
*— Age Republic Intelligence Doctrine*
