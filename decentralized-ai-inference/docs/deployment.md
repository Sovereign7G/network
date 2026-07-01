# S7G Decentralized AI Inference Deployment Guide

This guide details the steps to deploy the complete 9-service Sovereign AI Mesh stack containing the S7G PBFT consensus nodes, LiteLLM Gateway, and monitoring framework.

---

## 💻 Local Development Deployment

To start the full stack locally with Docker Compose:

```bash
cd decentralized-ai-inference
docker-compose up --build -d
```

Verify service exposures:
- **FastAPI / REST API**: `http://localhost:1317`
- **LiteLLM Gateway**: `http://localhost:4000`
- **vLLM Mock**: `http://localhost:8000`
- **Prometheus Dashboard**: `http://localhost:9090`
- **Grafana Visualization**: `http://localhost:3000`

---

## 🌐 Production Deployment (Akash Network)

Production deployments use the Akash Service Deployment Language (SDL) configuration.

### Prerequisites
1. Ensure the Akash CLI is configured and funded with UAKT.
2. Build and push custom Docker container images to a registry (Docker Hub/GHCR).

### Running Deploy Script
Execute the deployment manager script to launch the lease:
```bash
./deploy/scripts/deploy.sh
```

### Health check & Validation
Verify that the deployed nodes are operational:
```bash
./deploy/scripts/healthcheck.sh http://<your-node-ip>:1317
```

### Rollback on Outage
If a deployment version needs to be rolled back to a previous revision:
```bash
./deploy/scripts/rollback.sh <deployment-id>
```
