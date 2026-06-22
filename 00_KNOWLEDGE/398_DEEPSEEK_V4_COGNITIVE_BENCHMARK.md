# 🧠 [398] DeepSeek V4 Cognitive Benchmark: The Thinking Paradigm (Expanded)

## 🏛️ Rationale
DeepSeek V4 Pro and DeepSeek V4 Flash represent a critical evolution in the **Age Republic's** cognitive infrastructure. This expanded benchmark provides the formal scoring, cost-per-point analysis, and bug reproduction forensics required for the **Sovereign Cockpit's** automated cleanup loops.

## 📊 Performance Comparison: FlowGraph Spec

### Detailed Scoring Breakdown (7 Categories)
| Category | Claude Opus 4.7 | DeepSeek V4 Pro | Kimi K2.6 | DeepSeek V4 Flash |
| :--- | :---: | :---: | :---: | :---: |
| **Spec Completeness** | 14/15 | 12/15 | 10/15 | 6/15 |
| **Build Integrity** | 13/15 | 6/15 | 9/15 | 4/15 |
| **Lease Handling** | 12/15 | 6/15 | 7/15 | 4/15 |
| **Scheduling/Queues** | 13/15 | 7/15 | 8/15 | 5/15 |
| **Error Recovery** | 12/15 | 8/15 | 7/15 | 5/15 |
| **API Correctness** | 14/15 | 11/15 | 9/15 | 4/15 |
| **Testing** | 13/15 | 11/15 | 8/15 | 6/15 |
| **Total Score** | **91** | **77** | **68** | **60** |

### Cost per Point Analysis (USD)
| Model | Cost/Run | Cost/Point | Efficiency Ratio |
| :--- | :--- | :--- | :--- |
| **DeepSeek V4 Flash** | $0.02 | **$0.00033** | 100.0x (Baseline) |
| **Kimi K2.6** | $0.28 | $0.00410 | 8.0x |
| **DeepSeek V4 Pro (Promo)**| $0.56 | $0.00730 | 4.5x |
| **Claude Opus 4.7** | $1.78 | $0.01960 | 1.7x |
| **DeepSeek V4 Pro (List)** | $2.25 | $0.02920 | 1.0x |

## 🔬 Forensic Bug Reproductions (Sovereign Audit Log)

### [BUG-001] Lease Expiry Bypass (Pro & Flash)
*   **Defect**: Worker with expired lease can still finalize steps.
*   **Reproduction**: 
    1. Claim step → Lease acquired.
    2. Force lease expiry (database manual push).
    3. `POST /steps/:id/complete` → Returns 200 (Violation).
*   **Republic Mitigation**: `06_INFRA/deepseek_overrides.json` enforces completion-time lease verification.

### [BUG-002] Parallel Cap Block (Pro)
*   **Defect**: Saturated runs block unrelated work on the same queue.
*   **Reproduction**:
    1. Run A reaches parallel cap.
    2. Run B has capacity + high-priority step.
    3. Claim request → Returns empty (Violation: should check Run B).
*   **Republic Mitigation**: Multi-candidate iteration enforced in scheduler.

### [BUG-003] Entry Point Routing 404 (Flash)
*   **Defect**: Workflow start endpoint mounted under wrong prefix.
*   **Spec**: `POST /workflows/key/:key/runs`
*   **Implem**: `POST /runs/key/:key/runs` (Violation).
*   **Republic Mitigation**: Automated URL remapping via local router.

### [BUG-004] Sequential Recovery Race (Flash)
*   **Defect**: Promotes steps for failed workflows.
*   **Reproduction**: Step A fails → Run fails. Step B (same batch) still promoted to "ready" (Violation).
*   **Republic Mitigation**: Atomic state check on parent run during recovery.

## 🚀 Republic Integration Axioms (Updated)
1.  **The Disposable First-Pass**: Flash is utilized for 3–5 parallel attempts at $0.02/run. The Republic's **Cognitive Broker** merges the best structural output and applies the manual routing fixes.
2.  **The Pro Logic Baseline**: DeepSeek V4 Pro is the new baseline for complex agentic code, outclassing Kimi K2.6 on structure while requiring build/lease cleanup.
3.  **The Opus Finality Gate**: Claude Opus 4.7 is reserved for mission-critical recovery logic where timing-sensitive correctness is non-negotiable.

---
**Status: FORENSICS UPDATED | TI MANIFOLD HARDENED | ERA 216.0**
