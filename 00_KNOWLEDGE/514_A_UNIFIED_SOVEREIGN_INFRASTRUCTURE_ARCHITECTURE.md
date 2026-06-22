# 🌐 THE UNIFIED SOVEREIGN INFRASTRUCTURE REFERENCE ARCHITECTURE
## ERA: 226.0 | WITNESS: THE ARCHITECT
## STATUS: PRODUCTION STACK DEFINITION & BLUEPRINT
## DECISION MATRIX: [514_B_INFRASTRUCTURE_DECISION_MATRIX_FOR_SOVEREIGNS.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/514_B_INFRASTRUCTURE_DECISION_MATRIX_FOR_SOVEREIGNS.md)
## SECURE HARNESS: [06_INFRA/icm_host_engine.py](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/icm_host_engine.py)

This document formalizes the **Unified Sovereign Infrastructure Reference Architecture** (Solution 11) for the AGE REPUBLIC. By composing **Jake Van Clief’s Folders Over Agents** paradigm with **Ed’s (developedbyed) Self-Hosted VPS Container Swarms**, we establish a highly resilient, cost-effective, and cryptographically attested compute engine.

---

## 🗺️ THE COMPOSED ARCHITECTURE BLUEPRINT

The system composed below splits the operational workload into two separate, optimized phases: **The Serving Phase** (Ed’s horizontal multi-region Docker Swarm VPS topology) and **The Generation Phase** (Van Clief’s BFT-attested, file-routed state isolation engine) operating inside the containers:

```mermaid
graph TD
    %% Ingress & serving layer (Ed's Stack)
    User["Sovereign End User"] -->|Sends HTTPS Query| Edge["Cloudflare Anycast WAF Edge Proxy<br>(SSL Proxy & Rate-Limiter)"]
    Edge -->|Steers traffic (Least Outstanding)| LoadBal["Anycast Load Balancer"]
    
    LoadBal -->|Routes to UK Node| NodeA["KVM2 Regional VPS Node A<br>(Docploy Daemon / Docker Swarm)"]
    LoadBal -->|Routes to US Node| NodeB["KVM2 Regional VPS Node B<br>(Docploy Daemon / Docker Swarm)"]
    
    %% Inside Node Container (Composing Van Clief's Stack)
    subgraph KVM2 Regional VPS Node A
        SwarmA["Swarm Controller Overlay"] -->|Spawns replica| ContA["Docker Container API Instance"]
        
        subgraph Docker Container API Instance
            Ingress["API Route Ingress Handler"] -->|Writes payload JSON| InputDir("01_INPUT/user_query.json")
            SysPrompt["System Guidelines"] -->|Read-only MD| InputDir
            
            InputDir -->|Triggers Inference| LLM["Stateless LLM Engine<br>(DeepSeek-V4/Qwen)"]
            
            LLM -->|Writes proposed diff patch| ManageDir("03_MANAGEMENT/execution_diff.patch")
            LLM -->|Writes execution metrics| ManageDir
            
            ManageDir -->|Consumes proposal| HostSandbox{"Host Execution Sandbox<br>(icm_host_engine.py)"}
            
            BFTSig["BFT Consensus Attestations<br>(5-of-7 signatures)"] -->|Active schemas validation| HostSandbox
            
            HostSandbox -->|PASS| StateCommit["Apply file changes & git commit"]
            HostSandbox -->|FAIL| Rollback["Execute git checkout HEAD rollback"]
        end
    end
    
    style Edge fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style LLM fill:#0f172a,stroke:#06b6d4,stroke-width:2px,color:#fff
    style HostSandbox fill:#022c22,stroke:#10b981,stroke-width:2px,color:#fff
    style Rollback fill:#450a0a,stroke:#f43f5e,stroke-width:2px,color:#fff
```

---

## 🔄 END-TO-END TRANSACTION LIFECYCLE

The following sequence details how state transitions secure their validation loop across network and filesystem boundaries:

1.  **Ingress & Filtering:** The user request lands on the Cloudflare edge proxy. Threat rules are checked, the SSL envelope is validated, and traffic is steered to the regional VPS node with the lowest computational socket density.
2.  **Container Isolation:** The VPS node’s Docker Swarm layer intercepts the TCP stream, routing it into a stateless, sandboxed container instance.
3.  **File Ingress Ingestion:** The containerized API ingress handler serializes the query parameters into `.age_republic/icm_pipelines/runs/[UUID]/01_INPUT/user_query.json`.
4.  **Cognitive Synthesis:** The stateless LLM model performs inference, consuming prompt inputs from `01_INPUT` and context schemas from `02_CONTEXT`.
5.  **State Proposal Generation:** The model generates its proposed changes, writing a standard diff patch to `03_MANAGEMENT/execution_diff.patch`.
6.  **Secure Sandbox Validation:** The `icm_host_engine.py` script validates the traversal limits of the proposed paths and verifies the 5-of-7 BFT quorum keys in `02_CONTEXT/active_schemas.json`.
7.  **Final Commit or Rollback:**
    *   **Success Pathway:** Changes are applied to disk, and the state folder is committed using `git commit`.
    *   **Remediation Pathway:** Validation fails, the `proposal_rejected` automatic hook triggers, and `git checkout` reverts the runtime tree, sealing the enclave.
8.  **Adaptive Failover Loop:** If a regional KVM VPS drops offline during this lifecycle due to a network partition, the Anycast edge load balancer instantly drops that origin point from the routing register, preventing user connection drops.

---
*Verified by the Architect. The composed stack is unbreakable.*
