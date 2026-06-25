#!/usr/bin/env bash
# deploy_registry.sh — Deploy Tenant Registry canister to IC mainnet.
# Usage: ./deploy_registry.sh [network]
#   network: ic (default) or local

set -euo pipefail

NET="${1:-ic}"
DIR="$(cd "$(dirname "$0")" && pwd)"
WASM="$DIR/target/wasm32-unknown-unknown/release/tenant_registry_backend.wasm"

echo "=== Deploying Tenant Registry ==="
echo "Network:  $NET"
echo "WASM:     $WASM"

# Build
cd "$DIR"
cargo build --target wasm32-unknown-unknown --release

# Check WASM exists
if [ ! -f "$WASM" ]; then
    echo "ERROR: WASM not found at $WASM"
    exit 1
fi

WASM_SIZE=$(stat --format=%s "$WASM" 2>/dev/null || stat -f%z "$WASM")
echo "WASM size: $((WASM_SIZE / 1024)) KB"

# Deploy
echo ""
echo "Deploying..."
dfx deploy tenant_registry --network "$NET" --yes 2>&1 || true

# If the canister was already created, do upgrade instead
echo ""
echo "Or upgrade existing canister:"
echo "  dfx canister install tenant_registry \\"
echo "    --wasm \"$WASM\" \\"
echo "    --network \"$NET\" --mode upgrade --yes"
echo ""

echo "=== Done ==="
echo ""
echo "Verify with:"
echo "  ic canister call tenant_registry tenant_count '()' --network $NET"
