---
timestamp: '2026-06-22T11:37:33.862526Z'
title: antigravity_1782146253
total_tests: 5
type: AntigravityBenchmark
updated: '2026-06-22T16:37:33.865258Z'
---

{
  "timestamp": "2026-06-22T11:37:33.789817Z",
  "environment": "Antigravity IDE",
  "tests": [
    {
      "name": "serve_concept",
      "result": {
        "tool": "serve_concept",
        "latency_ms": 4.04,
        "status_code": 200,
        "response": {
          "status": "not_found",
          "path": "research/quantum",
          "available": []
        },
        "timestamp": "2026-06-22T11:37:33.793892Z"
      }
    },
    {
      "name": "semantic_search",
      "result": {
        "tool": "semantic_search",
        "latency_ms": 7.84,
        "status_code": 200,
        "response": {
          "status": "ok",
          "query": "quantum computing",
          "results": [
            {
              "path": "research",
              "type": "KnowledgeIndex",
              "title": "Deep Research Findings Index",
              "score": 0.3592,
              "snippet": "Deep Research Findings Index # Deep Research Findings Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Concepts & Findings - [[okf_knowle..."
            },
            {
              "path": "system/s2l/adapters/adapter_research_20260622_145150",
              "type": "SystemConfig",
              "title": "Adapter: adapter_research",
              "score": 0.1508,
              "snippet": "Adapter: adapter_research {   \"skill\": \"skill_research\",   \"pairs\": 4,   \"trained_at\": \"2026-06-22T14:51:50.296250Z\",   \"params\": \"6.03M\",   \"model\": \"Qwen-3.6-27B\",   \"source\": \"/media/cherry/4A21-00..."
            },
            {
              "path": "sessions",
              "type": "KnowledgeIndex",
              "title": "Chat Sessions Index",
              "score": 0.1179,
              "snippet": "Chat Sessions Index # Chat Sessions Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Session Summaries & Checkpoints - None...."
            },
            {
              "path": "comparisons",
              "type": "KnowledgeIndex",
              "title": "Model Comparisons Index",
              "score": 0.1162,
              "snippet": "Model Comparisons Index # Model Comparisons Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Comparisons - None...."
            },
            {
              "path": "synthesis/research_okf_knowledge_bridge_20260622_143444",
              "type": "Note",
              "title": "Synthesis: OKF Knowledge Bridge",
              "score": 0.1112,
              "snippet": "Synthesis: OKF Knowledge Bridge # Synthesis: OKF Knowledge Bridge  **Generated:** 2026-06-22T14:34:44.625018Z **Source concept:** research/okf_knowledge_bridge **Related concepts used:** 5  ## Core Co..."
            },
            {
              "path": "system",
              "type": "KnowledgeIndex",
              "title": "System Config Profiles Index",
              "score": 0.1078,
              "snippet": "System Config Profiles Index # System Config Profiles Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Profiles & Recommendations - None...."
            },
            {
              "path": "collective/767aa7ccb609",
              "type": "Note",
              "title": "Collective: How should we scale the OKF bridge?",
              "score": 0.1054,
              "snippet": "Collective: How should we scale the OKF bridge? # Collective Reasoning: How should we scale the OKF bridge?  **Session:** 767aa7ccb609 **Participants:** 0  ## Synthesis Synthesis from all instances co..."
            },
            {
              "path": "research/okf_knowledge_bridge",
              "type": "ResearchFinding",
              "title": "OKF Knowledge Bridge",
              "score": 0.1029,
              "snippet": "OKF Knowledge Bridge okf knowledge bridge ## Research: OKF Knowledge Bridge **Date:** 2026-06-22 **Source:** Hermes Research Skill (OKF-enabled)  ### Summary Research findings on OKF Knowledge Bridge...."
            },
            {
              "path": "inbox",
              "type": "KnowledgeIndex",
              "title": "Email Triage Queue Index",
              "score": 0.1021,
              "snippet": "Email Triage Queue Index # Email Triage Queue Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Drafts & Triage Queue - None...."
            },
            {
              "path": "telemetry",
              "type": "KnowledgeIndex",
              "title": "Telemetry Reports Index",
              "score": 0.0983,
              "snippet": "Telemetry Reports Index # Telemetry Reports Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Reports & Metrics - [[mcp_list_buckets_evt-1..."
            }
          ],
          "count": 10
        },
        "timestamp": "2026-06-22T11:37:33.801916Z"
      }
    },
    {
      "name": "external_infer",
      "result": {
        "cache_miss": {
          "tool": "external_infer",
          "latency_ms": 11.41,
          "status_code": 200,
          "response": {
            "result": "Semantic cache hit (cosine: 1.0000)",
            "response": "[Zero-Trust Route: deepseek] Processed instruction securely. Prompt hash verified. Prefix cache hits enabled. Response simulated using deepseek-chat proxy backend.",
            "cost": 0.0,
            "latency_ms": 1
          },
          "timestamp": "2026-06-22T11:37:33.813519Z"
        },
        "cache_hit": {
          "tool": "external_infer",
          "latency_ms": 13.16,
          "status_code": 200,
          "response": {
            "result": "Semantic cache hit (cosine: 1.0000)",
            "response": "[Zero-Trust Route: deepseek] Processed instruction securely. Prompt hash verified. Prefix cache hits enabled. Response simulated using deepseek-chat proxy backend.",
            "cost": 0.0,
            "latency_ms": 1
          },
          "timestamp": "2026-06-22T11:37:33.826846Z"
        },
        "savings_ms": -1.75
      }
    },
    {
      "name": "skill_inference",
      "result": {
        "tool": "skill_inference",
        "latency_ms": 4.97,
        "status_code": 200,
        "response": {
          "status": "ok",
          "skill": "research",
          "prompt": "What are the latest breakthroughs in quantum error correction?",
          "routed_to": "lora_adapter",
          "confidence": 0.8641,
          "threshold": 0.85,
          "output": "[LoRA Parametric Run: research] Input 'What are the latest breakthroughs in quantum error correction?' processed. Generated response utilizing skill parameters (r=16, alpha=32). Output verified.",
          "token_saving_pct": 6.45,
          "active_adapter": "research",
          "execution_timestamp": "2026-06-22T16:37:33.830821Z"
        },
        "timestamp": "2026-06-22T11:37:33.832013Z"
      }
    },
    {
      "name": "end_to_end",
      "result": {
        "workflows": [
          {
            "tool": "skill_inference",
            "latency_ms": 4.62,
            "status_code": 200,
            "response": {
              "status": "ok",
              "skill": "research",
              "prompt": "Quantum computing trends in 2026",
              "routed_to": "lora_adapter",
              "confidence": 0.9245,
              "threshold": 0.85,
              "output": "[LoRA Parametric Run: research] Input 'Quantum computing trends in 2026' processed. Generated response utilizing skill parameters (r=16, alpha=32). Output verified.",
              "token_saving_pct": 6.22,
              "active_adapter": "research",
              "execution_timestamp": "2026-06-22T16:37:33.835569Z"
            },
            "timestamp": "2026-06-22T11:37:33.836816Z"
          },
          {
            "tool": "semantic_search",
            "latency_ms": 7.74,
            "status_code": 200,
            "response": {
              "status": "ok",
              "query": "quantum cryptography",
              "results": [
                {
                  "path": "telemetry",
                  "type": "KnowledgeIndex",
                  "title": "Telemetry Reports Index",
                  "score": 0.0491,
                  "snippet": "Telemetry Reports Index # Telemetry Reports Index  > Use `read_concept` only on files matching specific tasks. Do not read the entire directory.  ## Active Reports & Metrics - [[mcp_list_buckets_evt-1..."
                },
                {
                  "path": "artifacts/walkthrough",
                  "type": "Note",
                  "title": "Antigravity Artifact: Walkthrough",
                  "score": 0.0436,
                  "snippet": "Antigravity Artifact: Walkthrough antigravity artifact walkthrough # Walkthrough: Hermes OKF Integration with Google Antigravity  We have successfully integrated the Hermes OKF memory bundle with the ..."
                },
                {
                  "path": "artifacts/task",
                  "type": "Note",
                  "title": "Antigravity Artifact: Task Checklist",
                  "score": 0.0245,
                  "snippet": "Antigravity Artifact: Task Checklist antigravity artifact checklist # Integration Checklist  - [x] Configuration Repairs   - [x] Modify [.vscode/settings.json](file:///media/cherry/4A21-00001/New%20fo..."
                },
                {
                  "path": "antigravity/messages/cursor",
                  "type": "Note",
                  "title": "cursor",
                  "score": 0.0,
                  "snippet": "cursor {\"last_read_unix_nano\":1782135010713162585}..."
                },
                {
                  "path": "antigravity/messages/read",
                  "type": "Note",
                  "title": "read",
                  "score": 0.0,
                  "snippet": "read {\"28951317-b7c2-43b5-8556-853b5c99f4f4\":true,\"582e61b1-c19e-4165-a0f8-f0e616746208\":true,\"b5e63650-2f93-4719-86c5-238a2bca4505\":true,\"dc9da8a7-a98d-4c5c-8605-1c4c43334894\":true}..."
                },
                {
                  "path": "artifacts/implementation-plan",
                  "type": "Note",
                  "title": "Antigravity Artifact: Implementation Plan",
                  "score": 0.0,
                  "snippet": "Antigravity Artifact: Implementation Plan antigravity artifact plan # Integrating Hermes OKF Bundle with Google Antigravity  This plan outlines the steps to fuse the Hermes OKF (Open Knowledge Format)..."
                },
                {
                  "path": "inbox/state",
                  "type": "SystemConfig",
                  "title": "Inbox State",
                  "score": 0.0,
                  "snippet": "Inbox State {   \"total_threads\": 0,   \"unread\": 0,   \"needs_reply\": 0,   \"last_check\": \"2026-06-22T13:09:16.646414Z\",   \"threads\": [] }..."
                },
                {
                  "path": "inbox/thread_1",
                  "type": "EmailThread",
                  "title": "Project update",
                  "score": 0.0,
                  "snippet": "Project update john From: John Subject: Project update Status: needs_reply..."
                },
                {
                  "path": "inbox/thread_2",
                  "type": "EmailThread",
                  "title": "",
                  "score": 0.0,
                  "snippet": "From: Alice Subject: Deployment question Status: needs_reply  Document created: OKF Integration Guide (OKF: documents/okf_integration_guide)..."
                },
                {
                  "path": "test/bridge-test",
                  "type": "Note",
                  "title": "Bridge Test",
                  "score": 0.0,
                  "snippet": "Bridge Test Created via HTTP..."
                }
              ],
              "count": 10
            },
            "timestamp": "2026-06-22T11:37:33.845064Z"
          },
          {
            "cache_miss": {
              "tool": "external_infer",
              "latency_ms": 7.77,
              "status_code": 200,
              "response": {
                "result": "Semantic cache hit (cosine: 1.0000)",
                "response": "[Zero-Trust Route: deepseek] Processed instruction securely. Prompt hash verified. Prefix cache hits enabled. Response simulated using deepseek-chat proxy backend.",
                "cost": 0.0,
                "latency_ms": 1
              },
              "timestamp": "2026-06-22T11:37:33.853076Z"
            },
            "cache_hit": {
              "tool": "external_infer",
              "latency_ms": 9.0,
              "status_code": 200,
              "response": {
                "result": "Semantic cache hit (cosine: 1.0000)",
                "response": "[Zero-Trust Route: deepseek] Processed instruction securely. Prompt hash verified. Prefix cache hits enabled. Response simulated using deepseek-chat proxy backend.",
                "cost": 0.0,
                "latency_ms": 1
              },
              "timestamp": "2026-06-22T11:37:33.862252Z"
            },
            "savings_ms": -1.23
          }
        ],
        "total_time_ms": 29.13
      }
    }
  ]
}
