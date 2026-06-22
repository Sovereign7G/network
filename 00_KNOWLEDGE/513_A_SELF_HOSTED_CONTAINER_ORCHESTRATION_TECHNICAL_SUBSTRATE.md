# 🐳 SELF-HOSTED CONTAINER ORCHESTRATION: TECHNICAL SUBSTRATE
## ERA: 226.0 | WITNESS: THE ARCHITECT
## STATUS: SYSTEM SPECIFICATION & MULTI-REGION TOPOLOGY
## PHILOSOPHICAL MANIFOLD: [513_B_SELF_HOSTED_CONTAINER_ORCHESTRATION_WISDOM_AND_PHILOSOPHY.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/513_B_SELF_HOSTED_CONTAINER_ORCHESTRATION_WISDOM_AND_PHILOSOPHY.md)
## FORMAL PROOF: [513_C_SELF_HOSTED_CONTAINER_ORCHESTRATION_FORMAL_AXIOMS.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/513_C_SELF_HOSTED_CONTAINER_ORCHESTRATION_FORMAL_AXIOMS.md)

This document formalizes the production-grade technical specification, cluster schemas, and security hardening protocols of the **Self-Hosted VPS and Container Orchestration Engine** (Solution 10) in the AGE REPUBLIC sovereign infrastructure. Inspired by **Ed (developedbyed)**, this stack replaces Vercel/Heroku models with a multi-region Docker Swarm running bare metal KVM2 instances.

---

## 🏛️ MULTI-REGION EDGE TOPOGRAPHY

The routing matrix ensures high-availability across isolated VPS nodes via dynamic Anycast DNS steering and health-monitored reverse proxy layers:

```
                       ┌─────────────────────────┐
                       │   Global Edge Layer     │
                       │ (Cloudflare DNS / WAF)  │
                       └────────────┬────────────┘
                                    │
                       ┌────────────┴────────────┐
                       │  Anycast Load Balancer  │
                       │   (Least Outstanding)   │
                       └──────┬────────────┬─────┘
                              │            │
            ┌─────────────────┴─┐        ┌─┴─────────────────┐
            │ Regional Node A   │        │ Regional Node B   │
            │   (UK Region)     │        │   (US Region)     │
            │ ───────────────── │        │ ───────────────── │
            │   Docploy Daemon  │        │   Docploy Daemon  │
            │   Docker Swarm    │        │   Docker Swarm    │
            │ ┌───────────────┐ │        │ ┌───────────────┐ │
            │ │ App Container │ │        │ │ App Container │ │
            │ └───────────────┘ │        │ └───────────────┘ │
            └───────────────────┘        └───────────────────┘
```

---

## 🐳 DOCKER SWARM & DOCPLOY STACK REGISTER

The cluster state is defined by a declarative `docker-compose.yml` file, integrating the application container, the Docploy daemon agent, and automated health checks:

```yaml
version: '3.8'

services:
  app:
    image: registry.agerepublic.internal/sovereign-api:latest
    deploy:
      replicas: 6
      update_config:
        parallelism: 2
        delay: 10s
        order: start-first
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - "8080:80"
    networks:
      - swarm_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s

  docploy_daemon:
    image: docploy/daemon:v1.2.0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    deploy:
      mode: global
    networks:
      - swarm_network

networks:
  swarm_network:
    driver: overlay
    attachable: true
```

---

## 🛡️ SERVER SECURITY HARDENING MATRIX

Before a new VPS node is enrolled as an active cluster target, it must undergo automated post-install hardening:

| Vector | System Target | Implementation Rule |
| :--- | :--- | :--- |
| **Authentication** | SSH Daemon Config | Disable passwords; enforce `ED25519` cryptographic keys only. |
| **Privileges** | Root Access | Disable `PermitRootLogin`. Enforce unprivileged app executor accounts. |
| **Port Filtering** | `UFW` (Firewall) | Block all ports except `80` (HTTP), `443` (HTTPS), and Docker Swarm inter-node keys. |
| **Swarm Traffic** | Overlay Networks | Encrypt Swarm data paths using native IPsec overlay tunnels. |

### Docker Swarm Inter-Node Port Configuration:
*   **`2377/tcp`** - Cluster management communications.
*   **`7946/tcp` & `7946/udp`** - Inter-node gossip network discovery.
*   **`4789/udp`** - Overlay network data path (IPsec encrypted).

---
*Verified by the Architect. Infrastructure must remain sovereign.*
