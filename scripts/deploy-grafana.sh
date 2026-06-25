#!/bin/bash
# Deploy Grafana + Prometheus stack for S7G observability.
# Usage: ./scripts/deploy-grafana.sh [up|down|restart]

set -e
ACTION="${1:-up}"

case "$ACTION" in
  up)
    echo "Starting Grafana + Prometheus..."
    docker compose -f docker-compose.yml up -d grafana prometheus
    echo "Waiting for Grafana..."
    until curl -sf http://localhost:3000/api/health > /dev/null 2>&1; do sleep 2; done
    echo "Importing S7G dashboard..."
    curl -sf -X POST http://admin:admin@localhost:3000/api/dashboards/db \
      -H "Content-Type: application/json" \
      -d @observability/grafana-dashboard.json > /dev/null && echo "Dashboard imported." || echo "Import skipped (dashboard may already exist)."
    echo "Grafana: http://localhost:3000 (admin/admin)"
    echo "Prometheus: http://localhost:9090"
    ;;
  down)
    docker compose -f docker-compose.yml down grafana prometheus
    ;;
  restart)
    "$0" down; "$0" up
    ;;
  *)
    echo "Usage: $0 [up|down|restart]"
    exit 1
    ;;
esac
