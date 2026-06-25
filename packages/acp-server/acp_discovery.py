#!/usr/bin/env python3
"""ACP Discovery Endpoint — authenticated, rate-limited, monitoring."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time, subprocess, hmac
from collections import defaultdict

# Load .env.acp if present
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.acp")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

AETHERDB = os.getenv("AETHERDB_CANISTER", "h54dw-qyaaa-aaaaa-qhjtq-cai")
LOG_FILE = "logs/acp_discovery.log"

# C-1: API key auth
API_KEY = os.getenv("ACP_API_KEY", "")
if not API_KEY:
    print("⚠️  WARNING: ACP_API_KEY not set — endpoint has NO authentication")
    print("   Set: export ACP_API_KEY=your-secret-key")

# C-2: Rate limiting
RATE_LIMIT = int(os.getenv("ACP_RATE_LIMIT", "100"))  # requests per minute per IP
_rate_store = defaultdict(list)

def _check_rate_limit(ip: str) -> bool:
    now = time.time()
    window = [t for t in _rate_store[ip] if t > now - 60]
    if len(window) >= RATE_LIMIT:
        return False  # rate limited
    _rate_store[ip].append(now)
    return True

def _log_to_aetherdb(entry):
    try:
        v = json.dumps(entry).encode("utf-8")
        blob = "vec{" + ";".join(str(b) for b in v) + "}"
        subprocess.run(["dfx","canister","--network","ic","call",AETHERDB,"aetherdb_put",
            f'({json.dumps(entry.get("type","acp:log"))}, {blob})'],
            capture_output=True, timeout=10)
    except: pass

def _log_local(entry):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

AGENT_METADATA = {
    "name": "Sovereign 7G Agent Swarm",
    "description": "30 autonomous agents managing the Sovereign 7G Network",
    "version": "1.0.0",
    "capabilities": [
        "liquidity_management", "arbitrage_detection", "yield_harvesting",
        "troves_liquidation", "cross_chain_bridging", "fx_hedging",
        "risk_assessment", "governance_voting", "reputation_scoring",
        "knowledge_curation", "action_planning", "synthesis",
        "memory_consolidation", "contextual_reasoning",
        "developer_onboarding", "adoption_funnel", "revenue_optimization",
        "competitive_intelligence",
    ],
    "agents": 30,
    "endpoints": {"discovery": "/.well-known/agent.json", "execute": "/api/agent/execute",
                  "status": "/api/agent/status", "health": "/api/agent/health"},
    "layers": ["ka_sem", "execution", "security", "governance", "gtme"],
}

class ACPHandler(BaseHTTPRequestHandler):
    def _auth(self) -> bool:
        if not API_KEY:
            return True  # no auth configured — allow
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return False
        token = auth.split(" ", 1)[1]
        return hmac.compare_digest(token, API_KEY)

    def _json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        ip = self.client_address[0]
        if not _check_rate_limit(ip):
            self._json(429, {"error": "rate limit exceeded"})
            return
        if not self._auth():
            self._json(401, {"error": "unauthorized"})
            return
        entry = {"type": "acp:discovery", "path": self.path, "ip": ip,
                 "ua": self.headers.get("User-Agent", "")[:60], "ts": time.time()}
        _log_local(entry)
        _log_to_aetherdb(entry)
        if self.path == "/.well-known/agent.json":
            self._json(200, AGENT_METADATA)
        elif self.path == "/api/agent/health":
            self._json(200, {"status": "healthy", "agents": 30, "uptime_s": int(time.time())})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        ip = self.client_address[0]
        if not _check_rate_limit(ip):
            self._json(429, {"error": "rate limit exceeded"})
            return
        if not self._auth():
            self._json(401, {"error": "unauthorized"})
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        entry = {"type": "acp:execute", "path": self.path, "ip": ip,
                 "task": body.get("task",""), "agent": body.get("agent","auto"), "ts": time.time()}
        _log_local(entry)
        _log_to_aetherdb(entry)
        if self.path == "/api/agent/execute":
            self._json(200, {"status": "queued", "task": body.get("task",""), "agent": body.get("agent","auto")})
        else:
            self._json(404, {"error": "not found"})

HTTPServer(("0.0.0.0", 8080), ACPHandler).serve_forever()
