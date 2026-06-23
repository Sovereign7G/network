#!/usr/bin/env python3
"""Sovereign 7G Python SDK v2 — unified client for the S7G network.
Covers: voice, messaging, nodes, beamforming, analytics, identity,
        LoRA IoT, ICP mesh, cross-chain, AI spec KB, and Virtual DSA.
"""
import json, os, time, hmac, hashlib
from decimal import Decimal
from http.client import HTTPSConnection
from typing import Dict, List, Optional, Callable, Any

API_BASE = os.getenv("S7G_API", "https://api.7g.sol")
# Fallback: read from .env or SERVEO_URL env var (updated on serveo restart)
def _resolve_serveo() -> str:
    url = os.getenv("SERVEO_URL") or os.getenv("SERVEO_FALLBACK")
    if url: return url
    try:
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("SERVEO_FALLBACK="):
                        return line.strip().split("=", 1)[1]
    except Exception:
        pass
    return "http://localhost:8080"
SERVEO_FALLBACK = _resolve_serveo()
S7G_TREASURY = os.getenv("S7G_TREASURY", "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611")
ICP_API = "https://ic0.app"
AETHERDB = os.getenv("AETHERDB_CANISTER", "h54dw-qyaaa-aaaaa-qhjtq-cai")
MOVE_VM = os.getenv("MOVE_VM_CANISTER", "gqshy-7qaaa-aaaaa-qhjua-cai")

# ── Helpers ─────────────────────────────────────────────────────

def _ic_call(canister: str, method: str, args: list) -> Optional[dict]:
    try:
        c = HTTPSConnection("ic0.app")
        body = json.dumps({"jsonrpc":"2.0","method":"canister_call",
            "params":[canister, method, args],"id":1}).encode()
        c.request("POST",f"/api/v2/canister/{canister}/call",body,
                  {"Content-Type":"application/json"})
        return json.loads(c.getresponse().read())
    except Exception:
        return None

def _sip_message(to: str, msg: str, host: str = "127.0.0.1", port: int = 5060):
    try:
        body = (f"MESSAGE sip:{to}@{host} SIP/2.0\r\n"
                f"From: <sip:sdk@{host}>;tag={hashlib.md5(msg.encode()).hexdigest()[:8]}\r\n"
                f"To: <sip:{to}@{host}>\r\nCall-ID: sdk-{int(time.time())}\r\n"
                f"CSeq: 1 MESSAGE\r\nContent-Type: text/plain\r\n"
                f"Content-Length: {len(msg)}\r\n\r\n{msg}")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(body.encode(), (host, port)); s.close()
        return True
    except Exception:
        return False



# ── S7G Types ───────────────────────────────────────────────────

class S7GCall:
    def __init__(self, session_id: str, client: 'S7GClient'):
        self.session_id = session_id; self.client = client
        self._handlers: Dict[str, list] = {}; self.status = "initiating"
        self.duration = 0.0; self.quality = {"mos":0,"packet_loss":0,"latency":0,"jitter":0}
    def on(self, event: str, handler: Callable): self._handlers.setdefault(event,[]).append(handler); return self
    def hangup(self):
        self.client._request("POST","/api/call/hangup",{"session_id":self.session_id})
        self.status = "ended"; self._emit("ended",self.duration)
    def _emit(self, event: str, *args):
        for h in self._handlers.get(event,[]): h(*args)

# ── S7G Client v2 ────────────────────────────────────────────────

class S7GClient:
    """Sovereign 7G SDK v2 — covers all S7G network capabilities."""

    def __init__(self, identity: str = "", secret: str = "", network: str = "base"):
        self.identity = identity; self.secret = secret or os.getenv("S7G_SECRET","")
        self.network = network
        self.base = self._resolve_api_endpoint() or API_BASE

    def _resolve_api_endpoint(self) -> Optional[str]:
        # Priority 1: SNS resolution (api.7g.sol via SSIMesh)
        try:
            from identity.ssi_mesh import SSIMesh
            ssi = SSIMesh()
            url = ssi.resolve_url("api.7g.sol")
            if url: return url
        except Exception:
            pass
        # Priority 2: Environment variable
        url = os.getenv("S7G_API_URL")
        if url: return url
        # Priority 3: SERVEO_FALLBACK (from .env or env var)
        url = os.getenv("SERVEO_URL") or os.getenv("SERVEO_FALLBACK")
        if url: return url
        return None  # let caller use API_BASE default

    def _sign(self, path: str, data: str = "") -> str:
        """HMAC sign a request — raises only when actually signing."""
        secret = self.secret or os.getenv("S7G_SECRET")
        if not secret:
            raise RuntimeError("S7G_SECRET required for signing requests")
        return hmac.new(secret.encode(), f"{path}:{data}".encode(), hashlib.sha256).hexdigest()[:16]

    def _request(self, method: str, path: str, body: Optional[Dict]=None) -> Dict:
        c = HTTPSConnection(self.base.replace("https://",""))
        c.request(method,path,body=json.dumps(body).encode() if body else None,
                  headers={"Content-Type":"application/json","X-Identity":self.identity,
                           "X-Signature":self._sign(path,json.dumps(body or {}))})
        return json.loads(c.getresponse().read().decode())

    # ═══════════════════════════════════════════════════════════════
    # CORE SERVICES
    # ═══════════════════════════════════════════════════════════════

    # ── Voice Calls ──────────────────────────────────────────────
    def call(self, to: str, call_type: str = "voice", quality: str = "hd",
             payment: Optional[Dict] = None) -> S7GCall:
        r = self._request("POST","/api/call/initiate",{
            "caller":self.identity,"callee":to,"type":call_type,"quality":quality,
            "payment":payment or {"method":"x402","currency":"USD"}})
        return S7GCall(r.get("session_id",""),self)

    def call_status(self, session_id: str) -> Dict:
        return self._request("GET",f"/api/call/status?session_id={session_id}")

    # ── Messaging ────────────────────────────────────────────────
    def message(self, to: str, text: str, priority: str = "normal") -> Dict:
        return self._request("POST","/api/message/send",
            {"from":self.identity,"to":to,"text":text,"priority":priority})

    # ── Node Management ──────────────────────────────────────────
    def node_register(self, lat: float, lon: float, stake: int = 1000) -> Dict:
        return self._request("POST","/api/node/register",
            {"identity":self.identity,"lat":lat,"lon":lon,"stake":stake})

    def node_status(self, node_id: str) -> Dict:
        return self._request("GET",f"/api/node/status?node_id={node_id}")

    def node_list(self) -> Dict:
        return self._request("GET","/api/node/list")

    # ── Beamforming ──────────────────────────────────────────────
    def beam_compute(self, src_lat: float, src_lon: float,
                     dst_lat: float, dst_lon: float) -> Dict:
        return self._request("POST","/api/beam/calculate",
            {"source":{"lat":src_lat,"lon":src_lon},
             "target":{"lat":dst_lat,"lon":dst_lon}})

    def beam_status(self, beam_id: str) -> Dict:
        return self._request("GET",f"/api/beam/status?beam_id={beam_id}")

    # ── Analytics ────────────────────────────────────────────────
    def analytics_health(self, metric: str = "avg_mos", region: str = "global") -> Dict:
        return self._request("GET",f"/api/analytics/health?metric={metric}&region={region}")

    def analytics_risk(self) -> Dict:
        return self._request("GET","/api/analytics/risk")

    # ── Identity ─────────────────────────────────────────────────
    def identity_resolve(self, name: str) -> Dict:
        return self._request("GET",f"/api/identity/resolve?name={name}")

    def identity_bind(self, name: str, bind_type: str = "ens") -> Dict:
        return self._request("POST","/api/identity/bind",
            {"name":name,"type":bind_type,"owner":self.identity})

    # ═══════════════════════════════════════════════════════════════
    # ICP MESH
    # ═══════════════════════════════════════════════════════════════

    def icp_store(self, key: str, value: str) -> Optional[dict]:
        """Store a value in aetherdb_bridge."""
        return _ic_call(AETHERDB, "aetherdb_put", [key, list(value.encode("utf-8"))])

    def icp_get(self, key: str) -> Optional[str]:
        """Get a value from aetherdb_bridge."""
        r = _ic_call(AETHERDB, "aetherdb_get", [key])
        if not r: return None
        data = r.get("result") or r.get("Ok")
        if isinstance(data, list): return bytes(data).decode("utf-8", errors="replace")
        return data

    def icp_list_type(self, prefix: str) -> list:
        """List keys by type prefix."""
        r = _ic_call(AETHERDB, "list_by_type", [prefix])
        if not r: return []
        return r.get("result") or r.get("Ok") or []

    def icp_estimate_storage(self) -> Optional[dict]:
        return _ic_call(AETHERDB, "estimate_storage", [])

    # ── Cross-Chain Proposals ─────────────────────────────────────
    def proposal_queue(self, target: str, data: str) -> Optional[dict]:
        return _ic_call(MOVE_VM, "queue_proposal", [target, list(data.encode("utf-8"))])

    def proposal_list(self) -> Optional[dict]:
        return _ic_call(MOVE_VM, "list_proposals", [])

    # ── Relayer Status ────────────────────────────────────────────
    def relayer_status(self) -> Optional[dict]:
        primary = self.icp_get("relayer:primary")
        return {"primary": primary}

    # ═══════════════════════════════════════════════════════════════
    # LoRA IOT
    # ═══════════════════════════════════════════════════════════════

    def lora_register_device(self, dev_eui: str, location: str = "") -> Optional[dict]:
        """Register a LoRA device by DevEUI."""
        return _ic_call(AETHERDB, "aetherdb_put",
            [f"lora:device:{dev_eui}", json.dumps({"devEUI":dev_eui,"location":location,"ts":time.time()})])

    def lora_get_device(self, dev_eui: str) -> Optional[str]:
        return self.icp_get(f"lora:device:{dev_eui}")

    def lora_get_telemetry(self, dev_eui: str) -> list:
        """Get recent telemetry for a LoRA device."""
        return self.icp_list_type(f"lora:{dev_eui}")

    def lora_alert(self, dev_eui: str, alert_type: str, location: str, contact: str = "+15551234") -> bool:
        """Send a LoRA alert via SIP."""
        msg = f"[LoRA] {alert_type.upper()} at {dev_eui} ({location})"
        return _sip_message(contact, msg)

    # ═══════════════════════════════════════════════════════════════
    # VIRTUAL DSA / SCIENCE
    # ═══════════════════════════════════════════════════════════════

    def dsa_observe(self, target: str, freq_hz: float, bandwidth: float,
                    nodes: Optional[List[str]] = None, duration_s: int = 30) -> Dict:
        """Schedule a radio observation across mesh nodes."""
        return self._request("POST","/api/dsa/observe",{
            "target":target,"freq_hz":freq_hz,"bandwidth":bandwidth,
            "nodes":nodes or [],"duration_s":duration_s})

    def dsa_frb_recent(self, minutes: int = 60) -> Dict:
        """Get recent Fast Radio Burst detections."""
        return self._request("GET",f"/api/dsa/frb?minutes={minutes}")

    def dsa_pulsar(self, name: str) -> Dict:
        """Get pulsar timing data."""
        return self._request("GET",f"/api/dsa/pulsar?name={name}")

    def dsa_rfi_report(self, node_id: Optional[str] = None) -> Dict:
        """Get RFI monitoring report."""
        path = f"/api/dsa/rfi?node_id={node_id}" if node_id else "/api/dsa/rfi"
        return self._request("GET", path)

    def dsa_rfi_alert(self, band: str, power_dbm: float, node_id: str,
                      contact: str = "astronomer@7g.network") -> bool:
        """Send RFI alert via SIP."""
        msg = f"[DSA RFI] {band}: {power_dbm:.1f} dBm at {node_id}"
        return _sip_message(contact, msg)

    # ═══════════════════════════════════════════════════════════════
    # AI / 3GPP SPEC KNOWLEDGE
    # ═══════════════════════════════════════════════════════════════

    def spec_get_context(self, spec_id: str, clause: Optional[str] = None) -> Dict:
        """Get 3GPP spec context for AI agent debugging."""
        return self._request("GET",f"/api/spec/context?spec={spec_id}&clause={clause or ''}")

    def spec_search(self, query: str) -> Dict:
        """Search 3GPP specs."""
        return self._request("GET",f"/api/spec/search?q={query}")

    def spec_for_component(self, component: str) -> Dict:
        """Get spec context for a specific S7G component."""
        return self._request("GET",f"/api/spec/component?name={component}")

    # ═══════════════════════════════════════════════════════════════
    # TEST INFRASTRUCTURE
    # ═══════════════════════════════════════════════════════════════

    def test_health(self) -> Dict:
        """Run health check — 7 contracts on Base Mainnet."""
        return self._request("GET","/api/test/health")

    def test_soak(self, hours: int = 1) -> Dict:
        """Trigger soak test."""
        return self._request("POST","/api/test/soak",{"hours":hours})

    def test_stress(self, requests: int = 100, workers: int = 10) -> Dict:
        """Trigger stress test."""
        return self._request("POST","/api/test/stress",{"requests":requests,"workers":workers})

    # ═══════════════════════════════════════════════════════════════
    # CONSTANTS
    # ═══════════════════════════════════════════════════════════════

    @property
    def CONTRACTS(self):
        return {
            "s7g": "0x54951D5021a2774567412fB8DB6FDF4A1EaE2611",
            "license": "0x45bD704f371bc593f38Bd76D43D356A14Febe477",
            "staking": "0xEfc2803E088e287b4013abB37358e3cf760A4747",
            "session": "0x6afd8D26dF226980a932439948DEefBd33301bf6",
            "registry": "0x2606fEbB30deE751DfFbCa538df20Eed5E379410",
            "roaming": "0x367d9481CfF6e7E18fAE5b11aA524dbbE139f443",
            "dao": "0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588",
        }

    @property
    def CANISTERS(self):
        return {
            "move_vm": MOVE_VM,
            "aetherdb": AETHERDB,
            "swarm": "oyipx-nyaaa-aaaab-qhbja-cai",
        }

    @property
    def BANDS(self):
        return {
            "l_band": (1.2e9, 1.7e9), "s_band": (2.3e9, 3.0e9),
            "c_band": (4.8e9, 5.5e9), "x_band": (8.0e9, 8.8e9),
            "ku_band": (12.0e9, 12.75e9),
        }

    # ═══════════════════════════════════════════════════════════════
    # POS DONGLE
    # ═══════════════════════════════════════════════════════════════

    def pos_settle(self, agent_did: str, merchant_id: str, amount: int,
                   corridor: str = "base_usdc", credential: str = "0x") -> Dict:
        """Settle a POS transaction through the S7G network."""
        return self._request("POST", "/api/pos/settle", {
            "agent_did": agent_did, "merchant_id": merchant_id,
            "amount": amount, "corridor": corridor, "credential": credential,
        })

    def pos_verify(self, agent_did: str, amount: int, corridor: str,
                   proof_hash: str) -> Dict:
        """Verify a POS settlement proof."""
        return self._request("POST", "/api/pos/verify", {
            "agent_did": agent_did, "amount": amount,
            "corridor": corridor, "proof_hash": proof_hash,
        })

    def pos_status(self) -> Dict:
        """Get POS integration status."""
        return self._request("GET", "/api/pos/status")

    @property
    def POS_PLATFORMS(self):
        return ["zavo", "razorpay", "airwallex"]

    @property
    def POS_CORRIDORS(self):
        return ["base_usdc", "base_eurc", "esc_ela", "icp_cycles"]

    # ── Court Operations (S7G v2.2) ──────────────────────────────

    def court_executive_pause(self, agent_name: str) -> Dict:
        """ExecutiveCourt: pause an agent (3-of-5 judges)."""
        return self._request("POST", "/api/court/executive/pause", {"agent": agent_name})

    def court_executive_freeze(self, corridor: str) -> Dict:
        """ExecutiveCourt: freeze a stablecoin corridor."""
        return self._request("POST", "/api/court/executive/freeze", {"corridor": corridor})

    def court_arbitration_file(self, defendant: str, evidence: str) -> Dict:
        """ArbitrationCourt: file a dispute (requires 1,000 S7G bond)."""
        return self._request("POST", "/api/court/arbitration/file",
                             {"defendant": defendant, "evidence": evidence})

    def court_arbitration_status(self, case_id: int) -> Dict:
        """ArbitrationCourt: check case status."""
        return self._request("GET", f"/api/court/arbitration/{case_id}")

    def court_governance_params(self, agent: str = "", param: str = "") -> Dict:
        """AgentGovernance: get or set agent parameters."""
        return self._request("GET", f"/api/court/governance/params?agent={agent}&param={param}")

    def court_governance_propose(self, agent: str, param: str, value: int) -> Dict:
        """AgentGovernance: propose a parameter change (7-day optimistic)."""
        return self._request("POST", "/api/court/governance/propose",
                             {"agent": agent, "param": param, "value": value})

    # ── Agent Swarm ──────────────────────────────────────────────

    def swarm_status(self) -> Dict:
        """Get status of all 26 agents."""
        return self._request("GET", "/api/swarm/status")

    def swarm_agent_info(self, name: str) -> Dict:
        """Get detailed info for a specific agent."""
        return self._request("GET", f"/api/swarm/agent/{name}")

    def swarm_logs(self, agent: str = "", hours: int = 1) -> Dict:
        """Read agent logs from aetherdb_bridge."""
        return self._request("GET", f"/api/swarm/logs?agent={agent}&hours={hours}")

    # ── Stablecoin Engine ────────────────────────────────────────

    def cctp_bridge_status(self, chain: str = "base") -> Dict:
        """CCTP Bridge: check cross-chain USDC bridge status."""
        return self._request("GET", f"/api/stablecoin/cctp?chain={chain}")

    def cctp_transfer(self, amount: int, source: str, dest: str) -> Dict:
        """CCTP Bridge: transfer USDC cross-chain with CCTP."""
        return self._request("POST", "/api/stablecoin/cctp/transfer",
                             {"amount": amount, "source": source, "dest": dest})

    def multi_yield_vault(self, action: str = "stats", asset: str = "USDC") -> Dict:
        """MultiYieldVault: deposit, withdraw, or check yields."""
        return self._request("POST", f"/api/stablecoin/vault/{action}", {"asset": asset})

    def stablecoin_routes(self) -> Dict:
        """Get current stablecoin routing table (all corridors)."""
        return self._request("GET", "/api/stablecoin/routes")

    def global_rate_card(self, currency: str = "USD") -> Dict:
        """GlobalRateCard: get per-minute rate for any currency."""
        return self._request("GET", f"/api/stablecoin/rates?currency={currency}")

    # ── Emergency Response ───────────────────────────────────────

    def emergency_dispatch(self, inc_id: str) -> Dict:
        """Dispatch responders to an incident."""
        return self._request("POST", "/api/emergency/dispatch", {"incident_id": inc_id})

    def emergency_fund(self, inc_id: str, amount: int) -> Dict:
        """Fund an emergency response from the S7G pool."""
        return self._request("POST", "/api/emergency/fund",
                             {"incident_id": inc_id, "amount": amount})

    # ── AIOps & Federated Learning ───────────────────────────────

    def aiops_anomalies(self, hours: int = 24) -> Dict:
        """Get recent AIOps anomaly detections."""
        return self._request("GET", f"/api/aiops/anomalies?hours={hours}")

    def aiops_patches(self, status: str = "open") -> Dict:
        """Get AI-generated patches from AIOps."""
        return self._request("GET", f"/api/aiops/patches?status={status}")

    def federated_round(self) -> Dict:
        """Get current federated learning round state."""
        return self._request("GET", "/api/federated/round")

    # ── Global Mesh ──────────────────────────────────────────────

    def mesh_routes(self) -> Dict:
        """Get current global mesh routes and fallback status."""
        return self._request("GET", "/api/mesh/routes")

    # ── GTME: Market & Adoption ──────────────────────────────────

    def adoption_metrics(self) -> Dict:
        """Get developer adoption funnel metrics."""
        return self._request("GET", "/api/gtme/adoption")

    def competitive_intel(self, competitor: str = "") -> Dict:
        """Get competitive intelligence report."""
        return self._request("GET", f"/api/gtme/intel?competitor={competitor}")

    # ── Constants v2.2 ───────────────────────────────────────────

    @property
    def AGENTS(self):
        return {"total": 26, "ka_sem": 5, "execution": 12, "security": 3,
                "governance": 2, "gtme": 4}

    @property
    def COURTS(self):
        return {"executive": "ExecutiveCourt.sol", "arbitration": "ArbitrationCourt.sol",
                "governance": "AgentGovernance.sol"}

    @property
    def STABLECOINS(self):
        return ["USDC", "EURC", "USDT", "DAI", "LUSD", "BOLD", "PYUSD"]

    @property
    def CHAINS(self):
        return ["base", "arbitrum", "solana", "ethereum", "polygon", "tron"]
