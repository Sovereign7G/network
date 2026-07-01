#!/bin/bash
# Phase D: Committee P2P Deployment Script
# Run on each VPS node after initial SSH setup
#
# Usage:
#   ssh vps1.sovereign7g.xyz
#   curl -sL https://sovereign7g.xyz/deploy-phase-d.sh | bash
#
# Or copy the script and run locally:
#   scp deploy-phase-d.sh vps1.sovereign7g.xyz:/tmp/
#   ssh vps1.sovereign7g.xyz bash /tmp/deploy-phase-d.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Phase D: Committee P2P Deployment                        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Configuration ────────────────────────────────────────────────────
COMMITTEE_ID="${S7G_COMMITTEE_ID:-s7g-committee-$(openssl rand -hex 8)}"
RELAY_URL="${S7G_IROH_RELAY:-http://localhost:3340}"
S7G_HOME="${S7G_HOME:-/opt/s7g}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Committee ID: $COMMITTEE_ID"
echo "  Relay URL: $RELAY_URL"
echo "  Install dir: $S7G_HOME"
echo ""

# ── Step 1: Install system dependencies ─────────────────────────────
echo -e "${GREEN}[1/5]${NC} Installing system dependencies..."
sudo apt-get update -qq && sudo apt-get install -y -qq nodejs npm curl jq 2>/dev/null

# ── Step 2: Create directory structure ───────────────────────────────
echo -e "${GREEN}[2/5]${NC} Creating directory structure..."
sudo mkdir -p "$S7G_HOME/shroud-enclave"/{bin,current,logs,config,node_modules}
sudo chown -R $USER:$USER "$S7G_HOME"

# ── Step 3: Install Node.js dependencies ─────────────────────────────
echo -e "${GREEN}[3/5]${NC} Installing Node.js dependencies..."
cd "$S7G_HOME/shroud-enclave"
if [ ! -f node_modules/@number0/iroh/package.json ]; then
    npm install @number0/iroh hypercore
fi

# ── Step 4: Create committee config ──────────────────────────────────
echo -e "${GREEN}[4/5]${NC} Creating committee configuration..."
cat > "$S7G_HOME/shroud-enclave/config/committee.json" << EOF
{
    "committeeId": "$COMMITTEE_ID",
    "relayUrl": "$RELAY_URL",
    "nodeId": "$(hostname)-$(openssl rand -hex 4)",
    "services": ["attestation", "consensus", "provenance"],
    "deployedAt": "$(date -Iseconds)"
}
EOF
echo "  Config written to $S7G_HOME/shroud-enclave/config/committee.json"

# ── Step 5: Create and start systemd service ─────────────────────────
echo -e "${GREEN}[5/5]${NC} Installing systemd service..."

SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_DIR/s7g-committee.service" << 'SERVICEEOF'
[Unit]
Description=S7G Committee P2P Node
After=network.target
Wants=network.target

[Service]
Type=simple
WorkingDirectory=/opt/s7g/shroud-enclave
Environment=S7G_IROH_RELAY=http://localhost:3340
ExecStart=/usr/bin/node /opt/s7g/shroud-enclave/bin/s7g-committee-node.js
Restart=always
RestartSec=10
StandardOutput=append:/opt/s7g/shroud-enclave/logs/committee.log
StandardError=append:/opt/s7g/shroud-enclave/logs/committee.log

[Install]
WantedBy=default.target
SERVICEEOF

# Set the committee ID from config
sed -i "s|Environment=S7G_COMMITTEE_ID=|Environment=S7G_COMMITTEE_ID=$COMMITTEE_ID|" "$SERVICE_DIR/s7g-committee.service" 2>/dev/null || true

systemctl --user daemon-reload
systemctl --user enable s7g-committee
systemctl --user start s7g-committee

# ── Verify ───────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}✅ Phase D deployment complete!${NC}"
echo ""
echo "  Committee ID: $COMMITTEE_ID"
echo "  Node service: systemctl --user status s7g-committee"
echo "  Logs: tail -f $S7G_HOME/shroud-enclave/logs/committee.log"
echo ""
echo "  To check peer discovery:"
echo "    grep -i \"member\\|discovered\" $S7G_HOME/shroud-enclave/logs/committee.log"
echo ""
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
