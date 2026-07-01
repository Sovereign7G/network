# S7G Docker & Unified Akash SDL Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the multi-node container orchestration stack (using docker-compose for local development) and generate the unified Akash Service Deployment Language (SDL) configuration for multi-provider production deployment, alongside pre-built Prometheus/Grafana monitoring dashboard configurations.

---

### Task 1: Create Multi-Node docker-compose.yml
**Files:**
- Create: `decentralized-ai-inference/docker-compose.yml`

- [ ] **Step 1: Create docker-compose.yml**
  Implement a docker-compose manifest linking:
  - 4 S7G nodes (`s7g-node-1` to `s7g-node-4`) on ports `1317` and P2P `26656`.
  - LiteLLM Gateway on port `4000` mounted with custom auth.
  - vLLM mock inference server on port `8000`.
  - Redis cache on port `6379`.
  - PostgreSQL ledger on port `5432`.
  - Prometheus on port `9090`.
  - Grafana on port `3000`.
  ```yaml
  version: '3.8'

  services:
    s7g-node-1:
      build:
        context: ./s7g-committee
        dockerfile: Dockerfile
      container_name: s7g-node-1
      ports:
        - "1317:1317"
        - "26656:26656"
      environment:
        - NODE_ID=1
        - NODE_ROLE=leader
        - COMMITTEE_SIZE=4
        - PEERS=s7g-node-2:26656,s7g-node-3:26656,s7g-node-4:26656
        - API_HOST=0.0.0.0
        - API_PORT=1317
        - LEDGER_PATH=/app/ledger
      volumes:
        - s7g-ledger-1:/app/ledger
      networks:
        - s7g-network

    s7g-node-2:
      build:
        context: ./s7g-committee
        dockerfile: Dockerfile
      container_name: s7g-node-2
      ports:
        - "1318:1317"
      environment:
        - NODE_ID=2
        - NODE_ROLE=follower
        - COMMITTEE_SIZE=4
        - PEERS=s7g-node-1:26656,s7g-node-3:26656,s7g-node-4:26656
        - API_HOST=0.0.0.0
        - API_PORT=1317
        - LEDGER_PATH=/app/ledger
      volumes:
        - s7g-ledger-2:/app/ledger
      networks:
        - s7g-network

    s7g-node-3:
      build:
        context: ./s7g-committee
        dockerfile: Dockerfile
      container_name: s7g-node-3
      ports:
        - "1319:1317"
      environment:
        - NODE_ID=3
        - NODE_ROLE=follower
        - COMMITTEE_SIZE=4
        - PEERS=s7g-node-1:26656,s7g-node-2:26656,s7g-node-4:26656
        - API_HOST=0.0.0.0
        - API_PORT=1317
        - LEDGER_PATH=/app/ledger
      volumes:
        - s7g-ledger-3:/app/ledger
      networks:
        - s7g-network

    s7g-node-4:
      build:
        context: ./s7g-committee
        dockerfile: Dockerfile
      container_name: s7g-node-4
      ports:
        - "1320:1317"
      environment:
        - NODE_ID=4
        - NODE_ROLE=follower
        - COMMITTEE_SIZE=4
        - PEERS=s7g-node-1:26656,s7g-node-2:26656,s7g-node-3:26656
        - API_HOST=0.0.0.0
        - API_PORT=1317
        - LEDGER_PATH=/app/ledger
      volumes:
        - s7g-ledger-4:/app/ledger
      networks:
        - s7g-network

    gateway:
      image: ghcr.io/berriai/litellm:main-latest
      container_name: litellm-gateway
      ports:
        - "4000:4000"
      volumes:
        - ./gateway/liteLLM/config.yaml:/app/config.yaml
        - ./gateway/auth:/app/auth
      environment:
        - S7G_NODE_URL=http://s7g-node-1:1317
      command: ["--config", "/app/config.yaml"]
      depends_on:
        - s7g-node-1
      networks:
        - s7g-network

  volumes:
    s7g-ledger-1:
    s7g-ledger-2:
    s7g-ledger-3:
    s7g-ledger-4:

  networks:
    s7g-network:
      driver: bridge
  ```

---

### Task 2: Create Unified Akash SDL Manifest
Generate the production-ready YAML exposing resources on Akash Network.

**Files:**
- Create: `decentralized-ai-inference/deploy/sdl/production.yaml`

- [ ] **Step 1: Create deploy/sdl/production.yaml**
  Define Akash SDL mapping nodes, compute, storage, GPU profiles, and endpoint exposures:
  ```yaml
  version: "2.0"

  services:
    s7g-node-1:
      image: s7g-committee:latest
      expose:
        - port: 1317
          as: 1317
          to:
            - global: false
        - port: 26656
          as: 26656
          to:
            - global: false
      env:
        - NODE_ID=1
        - NODE_ROLE=leader
        - COMMITTEE_SIZE=4
        - PEERS=s7g-node-2:26656,s7g-node-3:26656,s7g-node-4:26656
      params:
        storage:
          data:
            mount: /app/ledger

    gateway:
      image: litellm-gateway:latest
      expose:
        - port: 4000
          as: 4000
          accept:
            - gateway.sovereign7g.network
          to:
            - global: true

  profiles:
    compute:
      s7g-node-1:
        resources:
          cpu:
            units: 1.0
          memory:
            size: 2Gi
          storage:
            - size: 10Gi
            - name: data
              size: 20Gi
              attributes:
                persistent: true
      gateway:
        resources:
          cpu:
            units: 2.0
          memory:
            size: 4Gi
          storage:
            size: 10Gi

    placement:
      akash:
        pricing:
          s7g-node-1:
            denom: uakt
            amount: 100
          gateway:
            denom: uakt
            amount: 100

  deployment:
    s7g-node-1:
      akash:
        profile: s7g-node-1
        count: 1
    gateway:
      akash:
        profile: gateway
        count: 1
  ```

---

### Task 3: Setup Monitoring Stack Config
**Files:**
- Create: `decentralized-ai-inference/monitoring/prometheus.yml`

- [ ] **Step 1: Create monitoring/prometheus.yml**
  Add Prometheus metrics configuration scraping the gateway metrics endpoint:
  ```yaml
  global:
    scrape_interval: 15s

  scrape_configs:
    - job_name: 's7g-gateway'
      static_configs:
        - targets: ['gateway:4000']
    - job_name: 's7g-committee'
      static_configs:
        - targets: ['s7g-node-1:1317', 's7g-node-2:1317', 's7g-node-3:1317', 's7g-node-4:1317']
  ```
