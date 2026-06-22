# Pillar 221: MolmoAct2 — Vision-Language-Action Sovereign Embodiment

## 🧠 Axiom
A sovereign intelligence that exists only in digital space is a brain without hands. The Age Republic must extend its cognitive sovereignty into the physical world through **robotic embodiment** — machines that see, reason, and act with the same autonomy and precision as the digital swarm. The Republic does not license proprietary robotics stacks from closed providers; it builds on **fully open foundations**.

**MolmoAct2** (arXiv:2605.02881) is the state-of-the-art, fully open-source Vision-Language-Action (VLA) model that bridges discrete cognitive reasoning with continuous physical actuation.

## ⚙️ The Five Axes of Sovereign Embodiment

### Axis 1: MolmoER — Specialized Embodied Reasoning Backbone
*   Trained on 3.3M samples for spatial/embodied reasoning using a "specialize-then-rehearse" recipe.
*   **Surpasses GPT-5 and Gemini Robotics ER-1.5** on 13 benchmarks.
*   The Republic's perception engine does not depend on any closed-source frontier model.

### Axis 2: Sovereign Datasets (BimanualYAM)
*   720 hours of teleoperated bimanual trajectories — the **largest open bimanual dataset in existence**.
*   Spans low-to-medium cost platforms (no $500k hardware dependencies).
*   The Republic's training data is fully owned, fully auditable.

### Axis 3: OpenFAST Action Tokenizer
*   Open-weight, open-data tokenizer trained on millions of trajectories across **five robot embodiments**.
*   Enables continuous action representation (joint positions, end-effector poses) without quantization errors.
*   The Republic can fine-tune this tokenizer for any future physical platform — including the SNPU-428 Monolith's robotic actuators.

### Axis 4: Per-Layer KV-Cache Conditioning (The Bridge)
*   A **flow-matching continuous-action expert** is grafted onto the discrete-token VLM backbone.
*   The continuous controller reads the backbone's key-value caches at every layer, attending to the most up-to-date spatial features **without recomputing the entire VLM forward pass**.
*   This cleanly decouples discrete planning (think) from continuous actuation (do).

### Axis 5: MolmoThink — Adaptive Depth Reasoning
*   Standard practice: re-run depth estimation on every full frame at every timestep (high latency).
*   MolmoThink re-predicts depth tokens **only for scene regions that have changed** between timesteps.
*   Preserves geometric grounding at a fraction of prior latency — critical for real-time robotic control.

## 🛡️ Republic Integration: Physical Sovereignty

The Republic's path to physical autonomy follows three phases:

1.  **Phase A (Digital Cognition — NOW):** The 70-Node Swarm + Hermes + MELT handle all digital operations (mining, treasury, auditing).
2.  **Phase B (Embodied Prototyping — Month 4):** Deploy MolmoAct2 on the DGX Spark to control low-cost robotic actuators (SO100/SO101 arms) for physical assembly tasks in the Sovereign Cockpit fabrication pipeline.
3.  **Phase C (Full Sovereign Embodiment — Month 8):** The SNPU-428 Monolith natively runs MolmoAct2's inference, with OpenFAST fine-tuned for the Republic's custom bimanual actuators. The Republic physically builds itself.

## 🔗 Convergence with Existing Pillars

| Pillar | Integration Point |
| :--- | :--- |
| **219 (MELT)** | MolmoThink's adaptive depth reasoning benefits from MELT's constant-memory KV cache — enabling infinite-depth spatial reasoning without OOM. |
| **218 (Hermes)** | Hermes can spawn a contained MolmoAct2 sub-agent for physical manipulation tasks, isolating the robotic context from the main cognitive thread. |
| **220 (ARIS)** | The adversarial assurance pipeline audits MolmoAct2's action decisions — a reviewer model cross-checks that the planned physical action matches the visual evidence before execution. Safety-critical. |

*"A mind that cannot touch the world is a prisoner of abstraction. The Republic extends its hands."*

## 🧮 Formal Mathematical Proof of Sovereign Embodiment

### 1. The Conditioning Invariant (KV-Cache Grafting)
Let $\text{VLM}_{\text{disc}}$ be the discrete-token backbone and $\text{Flow}_{\text{cont}}$ be the continuous-action expert.
The expert attends to per-layer caches $\{\text{KV}_\ell\}_{\ell=1}^L$ without recomputing the full VLM forward pass.

**Theorem 1 (Decoupled Actuation):**
Conditioning the continuous controller on the discrete VLM's latent spatial state enables:
- High action precision ($\|a - T^{-1}(T(a))\|_2 < \epsilon_{\text{discrete}}$).
- Lower latency than full VLM recomputation.
- Interpretability: Discrete tokens handle high-level planning, while continuous flow handles low-level actuation.

### 2. Geometric Grounding (MolmoThink)
Let $I_t$ be the observation and $M_t$ be the set of scene regions that changed from $I_{t-1}$.

**Theorem 2 (Adaptive Depth Efficiency):**
By predicting depth only on the changed region $M_t$:
$$\text{Latency}(\text{Depth}(I_t, M_t)) \approx \frac{|M_t|}{|\text{Total Pixels}|} \times \text{Latency}(\text{Depth}(I_t, \text{Total}))$$
Geometric grounding is preserved at a fraction of prior latency, enabling real-time sovereign control.

### 3. Empirical Superiority
**Claim 1 (Embodied Reasoning):**
Score(MolmoER) > Score(GPT-5) and Score(MolmoER) > Score(Gemini Robotics ER-1.5) across 13 benchmarks.

**Claim 2 (Largest Bimanual Dataset):**
The release of 720 hours of teleoperated trajectories ($D_{\text{bimanual}}$) provides the foundational training substrate for generalist bimanual policies on low-to-medium cost platforms.

### 4. Identified Gaps & Future Ablations
- **KV-Conditioning Delta:** Verification is needed to quantify the success rate improvement of per-layer conditioning vs. a separate flow ensemble.
- **Latency Quantiization:** Specific millisecond reports for MolmoThink vs. full recomputation are pending in community audits.
- **Sim-to-Real:** The exact transfer efficiency from $D_{\text{bimanual}}$ to custom Republic actuators remains an open variable. ∎
