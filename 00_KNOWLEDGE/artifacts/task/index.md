---
created: '2026-06-23T02:23:48Z'
tags:
- antigravity
- artifact
- checklist
title: 'Antigravity Artifact: Task Checklist'
type: Note
updated: '2026-06-23T02:23:50.420031Z'
---

# Checklist: Sovereign 7G CI/CD Pipelines & Workflows

- [x] Task 1: Create `.pre-commit-config.yaml` with format/lint hooks (Ruff, Mypy, Forge, Cargo, Mojo)
- [x] Task 2: Create `Makefile` supporting install, lint, test, build, deploy, and clean commands
- [x] Task 3: Update `.github/workflows/ci.yml` with comprehensive lint, build, test, security, deploy, and docker-push jobs
- [x] Task 4: Configure `dfx.json` with ICP canister settings for move_vm, aetherdb_bridge, and swarm_brain
- [x] Task 5: Create `scripts/deploy_icp.sh` and make executable to automate ICP canister deployments
- [x] Task 6: Create `scripts/run_tests.sh` and make executable to orchestrate the multi-phase testing pipeline
- [x] Task 7: Create `monitoring/prometheus/prometheus.yml` scrape configuration
- [x] Task 8: Create `monitoring/grafana/dashboards/sovereign_7g.json` dashboard setup
- [x] Verification: Confirm syntax validity and local executability
