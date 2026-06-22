# δ-mem: Efficient Online Memory Substrate
## Sidecar Associative Memory for Frozen Manifolds

In the Age Republic's cognitive architecture, the retention of long-term historical context is achieved through **δ-mem** (Delta-Mem), a non-invasive memory substrate that augments frozen LLM backbones with dynamic associative capabilities.

---

### 1. Architecture: The Sidecar Paradigm
Unlike context window expansion which scales quadratically in compute, δ-mem operates as a **Sidecar Substrate**. It extracts hidden states from a frozen backbone and processes them through a compact associative memory matrix.

*   **Memory State**: A fixed-size matrix \( S_t \in \mathbb{R}^{d \times d} \) (e.g., $8 \times 8$).
*   **Backbone**: Remains **Frozen**, ensuring the preservation of the model's fundamental sovereign intelligence.
*   **Readout**: Generates low-rank corrections (\( \Delta q, \Delta o \)) to "steer" the backbone's attention heads.

### 2. Mathematical Formalization

#### 2.1 The Delta-Rule Update (Equation 3)
The memory state \( S_t \) is updated dynamically during the generation process using the Delta-Rule:
\[ S_t = \lambda_t S_{t-1} + \beta_t (v_t^m - S_{t-1} k_t^m) (k_t^m)^\top \]
*   **\( \beta_t \)**: Write gate (controls information intake).
*   **\( \lambda_t \)**: Retention gate (controls forgetting/decay).
*   **\( v_t^m, k_t^m \)**: Memory value and key vectors projected from the hidden state.

#### 2.2 The Read Operation (Equation 6)
Information is retrieved by querying the state matrix:
\[ r_t = S_{t-1} q_t^m \]
where \( q_t^m \) is the memory query at time \( t \).

#### 2.3 Attention Steering (Equations 7 & 8)
The read signal \( r_t \) is transformed into additive corrections for the Attention **Query (\( q \))** and **Output (\( o \))**:
\[ \Delta q_t = W_q^A r_t, \quad \Delta o_t = W_o^A r_t \]
\[ q_t^c = q_t^0 + \frac{\alpha}{r} \Delta q_t \]
*   **\( q_t^0 \)**: The original query from the frozen backbone.
*   **\( q_t^c \)**: The corrected query influenced by the historical context.

---

### 3. Performance Metrics and Efficiency
The Striking efficiency of δ-mem is demonstrated by the fact that a **64-parameter state (8x8)** achieves performance gains typically reserved for massive context expansions.

| Metric | Improvement vs. Frozen Backbone | vs. Best Non-δ-mem Baseline |
| :--- | :--- | :--- |
| **Average Score** | 1.10x | 1.15x |
| **MemoryAgentBench** | — | **1.31x** |
| **LoCoMo** | — | 1.20x |

### 4. Comparative Landscape: δ-mem vs. Legacy Mechanisms

| Method | Memory Footprint | Integration with Attention | Backbone Change |
| :--- | :--- | :--- | :--- |
| **Context Window** | O(L) | Direct (Quadratic cost) | None (Inference costly) |
| **RAG (Retrieval)** | External Index | Separate (Prepend context) | None |
| **Recurrent (RWKV)** | O(d²) or O(d) | Replaces Attention | **Full architecture change** |
| **δ-mem** | **O(1) [Fixed 8x8]** | **Low-rank correction** | **Frozen Backbone** |

### 5. Deployment Corollaries for the Republic
*   **Decoupled Complexity**: δ-mem decouples **Memory Capacity** from **Context Length Cost**. We can maintain long-term session history across thousands of turns without the quadratic VRAM explosion of full-attention windows.
*   **Orthogonal Integration**: δ-mem is additive. It can be combined with RAG (memory for session traces, RAG for external ground truth) and sliding window attention (Mistral) without conflict.
*   **Extreme Efficiency**: 64 parameters is smaller than a single attention head. This proves that the **Structure** of associative memory (Delta-Rule) is more potent than raw parameter volume.

---
*Documented for the Age Republic by Arham Islam & Antigravity*
