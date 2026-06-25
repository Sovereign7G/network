#!/usr/bin/env bash
# provision_tenant.sh — Create a new tenant with dedicated canister pair.
# Usage: ./provision_tenant.sh TENANT_NAME TIER [REGISTRY_CANISTER]
set -euo pipefail

TENANT="$1"
TIER="${2:-enterprise}"
REGISTRY="${3:-}"  # will be set after first deploy

DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$TENANT" ]; then
    echo "Usage: $0 TENANT_NAME [tier] [registry_canister]"
    exit 1
fi

echo "=== Provisioning tenant: $TENANT ($TIER) ==="

# 1. Generate unique canister names
CREDITS_NAME="credits_${TENANT}"
SETTLEMENT_NAME="settlement_${TENANT}"

echo "Creating canisters..."

# 2. Create credits canister (from the sovereign_icp_backend package)
ICP_BACKEND="/media/cherry/4A21-00001/New folder/AGE REPUBLIC/sovereign_icp_backend"
if [ -f "$ICP_BACKEND/dfx.json" ]; then
    # Deploy a new instance of the credits canister
    dfx canister create "$CREDITS_NAME" --network ic --yes 2>&1 || true
    CREDITS_ID=$(dfx canister id "$CREDITS_NAME" --network ic 2>/dev/null || echo "")
    echo "  Credits:  $CREDITS_ID"

    # Deploy a new instance of the settlement canister
    dfx canister create "$SETTLEMENT_NAME" --network ic --yes 2>&1 || true
    SETTLEMENT_ID=$(dfx canister id "$SETTLEMENT_NAME" --network ic 2>/dev/null || echo "")
    echo "  Settlement: $SETTLEMENT_ID"
else
    echo "WARNING: sovereign_icp_backend not found. Create canisters manually."
    CREDITS_ID=""
    SETTLEMENT_ID=""
fi

# 3. Register with registry
if [ -n "$REGISTRY" ] && [ -n "$CREDITS_ID" ]; then
    ARG="(record { name = \"$TENANT\"; tier = \"$TIER\";"
    [ -n "$CREDITS_ID" ] && ARG="$ARG credits_canister = principal \"$CREDITS_ID\";"
    [ -n "$SETTLEMENT_ID" ] && ARG="$ARG settlement_canister = principal \"$SETTLEMENT_ID\";"
    ARG="$ARG label = opt \"$TENANT ($TIER)\"; })"

    echo ""
    echo "Registering with registry..."
    dfx canister call "$REGISTRY" register_tenant "$ARG" --network ic
fi

echo ""
echo "=== Tenant $TENANT provisioned ==="
echo "  Tier:         $TIER"
echo "  Credits:      ${CREDITS_ID:-manual}"
echo "  Settlement:   ${SETTLEMENT_ID:-manual}"
echo "  Registry:     ${REGISTRY:-not set}"
echo ""
echo "Add credits:"
echo "  ./add_tenant_credits.sh $TENANT AKASH 5000000"
echo ""
echo "Run inference:"
echo "  depin-infer --tenant $TENANT gpt-4o \"Hello\""
