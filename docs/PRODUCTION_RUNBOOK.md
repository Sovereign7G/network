# Sovereign Mesh Production Runbook

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Deployment](#deployment)
3. [Monitoring & Alerting](#monitoring--alerting)
4. [Incident Response](#incident-response)
5. [Disaster Recovery](#disaster-recovery)
6. [Security Procedures](#security-procedures)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

### Components
| Component | Provider | Region | Purpose |
|-----------|----------|--------|---------|
| Edge DNS/Proxy | Cloudflare | Global | DDoS, WAF, rate limiting |
| Edge Worker | Cloudflare Workers | Global | Token validation, edge OPA |
| Tunnel | Cloudflare Tunnel | Global | Secure edge-to-origin |
| API Gateway | GKE / EKS | us-central1, us-east1 | FastAPI router |
| P2P Mesh | GKE / EKS | us-central1, us-east1 | P2P node coordination |
| Redis | Memorystore / ElastiCache | Multi-region | Rate limiting state |
| Database | Cloud Spanner / RDS | Multi-region | Ledger, OPA state |

### Synthetic IP Range
- **Range**: `100.80.0.0/16`
- **Purpose**: Internal routing between edge and origin
- **eBPF**: Kernel-level rewrite in Linux

## Deployment

### Prerequisites
```bash
# Install required tools
brew install cloudflared wrangler terraform kubectl helm
brew install locust  # for load testing
```

### Deploy to Production
```bash
# Full deployment
./scripts/deploy_production.sh

# Deploy only Cloudflare components
./scripts/deploy_cloudflare.sh

# Deploy only GCP
cd terraform/environments/production && terraform apply

# Deploy only AWS
cd terraform/environments/production-aws && terraform apply
```

### Rollback Procedure
```bash
# Rollback to previous version
kubectl rollout undo deployment/sovereign-router -n sovereign-mesh

# Rollback Cloudflare Worker
wrangler rollback --env production

# Rollback Terraform
terraform apply -var="image_tag=previous-tag"
```

## Monitoring & Alerting

### Critical Metrics

| Metric | Threshold | Action |
|--------|-----------|--------|
| Edge latency P99 | > 100ms | Investigate Cloudflare |
| Error rate | > 1% | Check edge worker logs |
| Rate limiting | > 1000/min | Scale backend |
| Tunnel health | == 0 | Restart cloudflared |
| eBPF routing | > 100µs | Check kernel module |

### Dashboards
- **Production Overview**: https://grafana.sovereign-mesh.io/d/prod
- **Edge Metrics**: https://grafana.sovereign-mesh.io/d/edge
- **eBPF Performance**: https://grafana.sovereign-mesh.io/d/ebpf

### Alerts (PagerDuty)

| Alert | Severity | Runbook |
|-------|----------|---------|
| `EdgeLatencyHigh` | P2 | Check Cloudflare status |
| `TunnelDown` | P1 | Restart cloudflared |
| `DatabaseUnreachable` | P0 | Failover to secondary region |
| `RateLimitExhausted` | P3 | Scale backend pods |

## Incident Response

### P0 (Critical) - Complete Outage

1. **Immediate**:
   ```bash
   # Check Cloudflare status
   cloudflared tunnel list
   cloudflared tunnel route dns list
   
   # Failover to secondary region
   kubectl config use-context gke_us-central1
   kubectl scale deployment/sovereign-router --replicas=10
   ```

2. **Post-incident**:
   - Update runbook
   - Schedule root cause analysis
   - Implement preventive measures

### P1 (High) - Performance Degradation

1. **Diagnose**:
   ```bash
   # Check edge latency
   curl -w "@curl-format.txt" https://api.sovereign-mesh.io/health
   
   # Check pod health
   kubectl get pods -n sovereign-mesh
   kubectl top pods -n sovereign-mesh
   ```

2. **Mitigate**:
   ```bash
   # Scale horizontally
   kubectl scale deployment/sovereign-router --replicas=20
   
   # Enable additional rate limiting at edge
   wrangler kv:key put --env production "rate_limit_enabled" "true"
   ```

## Disaster Recovery

### RTO: 15 minutes | RPO: 5 minutes

### Failover to Secondary Region

```bash
# GCP → AWS failover
export PRIMARY_REGION="us-central1"
export SECONDARY_REGION="us-east-1-aws"

# Update Cloudflare DNS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"content":"'$AWS_LOAD_BALANCER_IP'"}'

# Redirect traffic
kubectl config use-context eks_sovereign-cluster
kubectl scale deployment/sovereign-router --replicas=10
```

### Database Recovery

```bash
# Restore from backup
gcloud spanner databases restore \
  --source-database=sovereign_mesh \
  --target-database=sovereign_mesh_restored \
  --source-backup=backup-$(date +%Y%m%d)

# Promote read replica to primary
aws rds promote-read-replica \
  --db-instance-identifier sovereign-mesh-replica
```

## Security Procedures

### Token Rotation

```bash
# Rotate sovereign token
export NEW_TOKEN=$(openssl rand -hex 32)
wrangler kv:key put --env production "token:admin:${NEW_TOKEN}" "${NEW_TOKEN}"
kubectl create secret generic sovereign-token --from-literal=token=$NEW_TOKEN --dry-run=client -o yaml | kubectl apply -f -
```

### Certificate Renewal

```bash
# Let's Encrypt auto-renewal (handled by cert-manager)
kubectl get certificaterequests -n cert-manager

# Manual renewal if needed
certbot renew --force-renewal
```

## Maintenance

### Daily Tasks

```bash
# Check error logs
kubectl logs -l app=sovereign-router --tail=100 --prefix

# Review rate limiting metrics
./scripts/check_rate_limits.sh

# Verify eBPF module is loaded
./scripts/check_ebpf.sh
```

### Weekly Tasks

```bash
# Security scan
docker scout cves sovereign-mesh:prod

# Performance baseline
locust -f load_tests/edge_load_test.py --users 1000 --headless --csv reports/weekly

# Backup databases
./scripts/backup_databases.sh
```

### Monthly Tasks

```bash
# Update dependencies
pip list --outdated
npm outdated

# Rotate all credentials
./scripts/rotate_all_secrets.sh

# Simulate disaster recovery
./scripts/disaster_recovery_test.sh
```

## Troubleshooting

### Common Issues

| Issue | Symptoms | Resolution |
|-------|----------|------------|
| **Tunnel disconnected** | 502 errors | `kubectl rollout restart deployment/cloudflared` |
| **Rate limiting too aggressive** | 429 errors | `wrangler kv:key put --env production "rate_limit_scale" "2.0"` |
| **eBPF not loaded** | Synthetic IPs not routing | `sudo bpftool prog list \| grep sovereign` |
| **WebSocket connections failing** | P2P mesh offline | Check port 9877: `netstat -an \| grep 9877` |
| **High memory usage** | OOM kills | `kubectl top pods` then scale or increase limits |

### Diagnostic Commands

```bash
# Complete health check
./scripts/health_check.sh

# Trace request through edge
curl -v -H "X-Debug: true" https://api.sovereign-mesh.io/health

# Check Cloudflare cache
curl -sI https://api.sovereign-mesh.io | grep -i cf-

# Verify synthetic IP routing
for ip in 100.80.{1..3}.{1..3}; do
  curl -s "https://api.sovereign-mesh.io/api/benchmark/route?dest=$ip" | jq '.latency_us'
done
```

## Emergency Contacts

| Role | Contact | Response Time |
|------|---------|---------------|
| SRE Lead | sre@sovereign-mesh.io | 5 min |
| Security Engineer | security@sovereign-mesh.io | 15 min |
| Cloudflare Support | enterprise@cloudflare.com | 30 min |
| GCP Support | gcp-support@google.com | 1 hour |
| AWS Support | aws-support@amazon.com | 1 hour |

## Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2024-01-15 | 2.0.0 | Sovereign Team | Production release |
| 2024-01-10 | 1.5.0 | Sovereign Team | Added eBPF routing |
| 2024-01-01 | 1.0.0 | Sovereign Team | Initial deployment |
