#!/bin/bash
# deploy-bifrost.sh — Deploy Bifrost upstream config for S7G AI Mesh
set -e

echo "🚀 Deploying Bifrost upstream configuration for S7G AI Mesh..."

# 1. Determine Bifrost config directory
BIFROST_DIR="${BIFROST_DIR:-/etc/bifrost}"
if [ ! -d "$BIFROST_DIR" ]; then
    echo "⚠️  Bifrost config dir not found at $BIFROST_DIR"
    echo "   Copying config locally instead."
    BIFROST_DIR="./gateway/bifrost"
fi

# 2. Copy upstream config
cp decentralized-ai-inference/gateway/bifrost/upstreams.yaml "$BIFROST_DIR/upstreams.yaml"
echo "✅ Upstream config deployed to $BIFROST_DIR/upstreams.yaml"

# 3. Reload Bifrost
if command -v bifrost &>/dev/null; then
    bifrost reload
    echo "✅ Bifrost reloaded"
else
    echo "⚠️  'bifrost' command not found. Reload manually or restart the service."
fi

# 4. Test the chain
echo ""
echo "🔍 Testing upstream chain..."
echo "   S7G:      http://localhost:4000/health"
echo "   Bifrost:  http://localhost:8080/v1/chat/completions"
echo ""
echo "   curl -X POST http://localhost:8080/v1/chat/completions \\"
echo "     -H 'X-API-Key: \${BIFROST_API_KEY}' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"model\":\"sovereign-llama3\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'"
