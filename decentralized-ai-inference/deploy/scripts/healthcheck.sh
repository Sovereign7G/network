#!/bin/bash
set -e

# ==============================================================================
# healthcheck.sh — S7G post-deployment verification script
# ==============================================================================

TARGET_URL=${1:-"http://localhost:1317"}

echo "🔍 Running S7G Node healthcheck against: ${TARGET_URL}"

STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/health")

if [ "$STATUS_CODE" -eq 200 ]; then
    echo "✅ S7G node is healthy (HTTP 200)"
    exit 0
else
    echo "❌ S7G node is unhealthy (HTTP ${STATUS_CODE})"
    exit 1
fi
