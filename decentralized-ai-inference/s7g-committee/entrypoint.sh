#!/bin/bash
set -e

# ===== CONFIG =====
NODE_ID=${NODE_ID:-1}
NODE_ROLE=${NODE_ROLE:-follower}
COMMITTEE_SIZE=${COMMITTEE_SIZE:-4}
PEERS=${PEERS:-}
GENESIS_FILE=${GENESIS_FILE:-/app/genesis.json}
LEDGER_PATH=${LEDGER_PATH:-/app/ledger}
API_PORT=${API_PORT:-1317}

echo "🚀 Starting S7G Committee Node $NODE_ID"
echo "Role: $NODE_ROLE"
echo "Committee Size: $COMMITTEE_SIZE"
echo "Peers: $PEERS"
echo "Genesis: $GENESIS_FILE"
echo "Ledger: $LEDGER_PATH"
echo "API Port: $API_PORT"

# ===== INITIALIZE LEDGER =====
mkdir -p "$LEDGER_PATH"

# ===== START API SERVER =====
echo "📡 Starting API server on port $API_PORT..."
cd /app
python -m uvicorn node.api:app --host 0.0.0.0 --port $API_PORT --workers 1 &
API_PID=$!
echo "API PID: $API_PID"

# ===== HEALTH CHECK LOOP =====
echo "✅ S7G Node $NODE_ID is operational"
while true; do
    sleep 30
    if curl -s -f http://localhost:$API_PORT/health > /dev/null 2>&1; then
        echo "[$(date)] 💚 Health check passed (Node $NODE_ID)"
    else
        echo "[$(date)] 💔 Health check failed (Node $NODE_ID)"
    fi
done
