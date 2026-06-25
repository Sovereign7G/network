#!/usr/bin/env python3
"""OIDC Relayer — validates JWTs from identity providers and creates
sessions on the registry canister.

Flow:
  1. User authenticates with Azure AD / Okta / Google
  2. User sends JWT to this relayer (POST /login)
  3. Relayer validates JWT signature against provider's JWKS
  4. Relayer calls registry canister's oidc_login() to create session
  5. User receives session principal for subsequent canister calls

Usage:
    export OIDC_AZURE_TENANT="your-tenant-id"
    export OIDC_AZURE_CLIENT_ID="your-client-id"
    export OIDC_OKTA_DOMAIN="your-org.okta.com"
    export OIDC_OKTA_CLIENT_ID="your-client-id"
    python3 relayer.py

Dependencies: pip install pyjwt cryptography requests flask
"""
import json
import os
import subprocess
import sys
import time
from typing import Optional

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Install flask: pip install flask")
    sys.exit(1)

try:
    import jwt
    from jwt.algorithms import RSAAlgorithm
except ImportError:
    print("Install pyjwt: pip install pyjwt cryptography")
    sys.exit(1)

import requests

REGISTRY_CANISTER = "iemx3-niaaa-aaaad-ql7uq-cai"
PORT = int(os.environ.get("OIDC_RELAYER_PORT", "8100"))

app = Flask(__name__)

# ── OIDC Configuration ──────────────────────────────────────────────

def _azure_jwks_uri():
    tenant = os.environ.get("OIDC_AZURE_TENANT")
    if not tenant:
        return None
    return f"https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys"

def _okta_jwks_uri():
    domain = os.environ.get("OIDC_OKTA_DOMAIN")
    if not domain:
        return None
    return f"https://{domain}/oauth2/default/v1/keys"

JWKS_URIS = {
    "azure": _azure_jwks_uri,
    "okta": _okta_jwks_uri,
}

CLIENT_IDS = {
    "azure": os.environ.get("OIDC_AZURE_CLIENT_ID", ""),
    "okta": os.environ.get("OIDC_OKTA_CLIENT_ID", ""),
}

# ── JWKS Cache ──────────────────────────────────────────────────────

_jwks_cache: dict[str, tuple[float, list[dict]]] = {}
JWKS_TTL = 3600  # 1 hour

def _fetch_jwks(provider: str) -> list[dict]:
    now = time.time()
    cached = _jwks_cache.get(provider)
    if cached and (now - cached[0]) < JWKS_TTL:
        return cached[1]
    uri_fn = JWKS_URIS.get(provider)
    if not uri_fn:
        return []
    uri = uri_fn()
    if not uri:
        return []
    resp = requests.get(uri, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    keys = data.get("keys", [])
    _jwks_cache[provider] = (now, keys)
    return keys

# ── Canister Call ───────────────────────────────────────────────────

def _call_canister(method: str, args: str) -> Optional[str]:
    """Call registry canister via dfx (subprocess)."""
    try:
        out = subprocess.check_output(
            ["dfx", "canister", "call", REGISTRY_CANISTER, method, args,
             "--network", "ic"],
            stderr=subprocess.STDOUT, timeout=30, text=True,
        )
        return out.strip()
    except subprocess.CalledProcessError as e:
        print(f"Canister call failed: {e.output}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Canister call error: {e}", file=sys.stderr)
        return None

# ── Routes ──────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    token = data.get("token")
    provider = data.get("provider", "azure")

    if not token:
        return jsonify({"error": "token required"}), 400

    # 1. Fetch JWKS
    try:
        jwks = _fetch_jwks(provider)
        if not jwks:
            return jsonify({"error": f"No JWKS available for {provider}"}), 500
    except Exception as e:
        return jsonify({"error": f"JWKS fetch failed: {e}"}), 500

    # 2. Validate JWT
    claims = None
    for key_data in jwks:
        try:
            public_key = RSAAlgorithm.from_jwk(json.dumps(key_data))
            claims = jwt.decode(
                token, public_key, algorithms=["RS256"],
                audience=CLIENT_IDS.get(provider, ""),
                options={"verify_exp": True},
            )
            break
        except jwt.InvalidAudienceError:
            continue
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception:
            continue

    if not claims:
        return jsonify({"error": "Could not verify token with any JWKS key"}), 401

    # 3. Build canister claims
    sub = claims.get("sub", "")
    email = claims.get("email") or claims.get("preferred_username", "")
    name = claims.get("name") or email.split("@")[0] if email else sub
    oidc_roles = claims.get("roles", []) or claims.get("groups", [])

    canister_args = (
        '({ sub = "' + sub + '"; email = "' + email + '"; '
        'name = "' + name + '"; roles = '
        + json.dumps(oidc_roles) + '; issuer = "' + provider + '" }, '
        'opt 3600)'
    )

    result = _call_canister("oidc_login", canister_args)
    if result is None:
        return jsonify({"error": "Canister call failed"}), 500

    return jsonify({
        "status": "ok",
        "principal": result.strip() if result else None,
        "email": email,
        "name": name,
        "roles": oidc_roles,
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "providers": list(JWKS_URIS.keys()),
        "registry": REGISTRY_CANISTER,
    })

if __name__ == "__main__":
    print(f"OIDC Relayer starting on port {PORT}")
    print(f"Registry canister: {REGISTRY_CANISTER}")
    print(f"Providers configured: {[k for k, v in JWKS_URIS.items() if v()]}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
