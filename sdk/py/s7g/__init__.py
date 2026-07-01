#!/usr/bin/env python3
"""Sovereign 7G Python SDK v2 — unified client for the S7G network.
Covers: voice, messaging, nodes, beamforming, analytics, identity,
        LoRA IoT, ICP mesh, cross-chain, AI spec KB, and Virtual DSA.
"""
__version__ = "2.4.0"
import json, os, time, hmac, hashlib
from decimal import Decimal
from http.client import HTTPSConnection
from typing import Dict, List, Optional, Callable, Any

API_BASE = os.getenv("S7G_API", "https://api.7g.sol")

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
        import socket
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
        self.network = network; self.base = self._resolve_api_endpoint() or API_BASE

    def _resolve_api_endpoint(self) -> Optional[str]:
        try:
            from identity.ssi_mesh import SSIMesh
            url = SSIMesh().resolve_url("api.7g.sol")
            if url: return url
        except Exception:
            pass
        url = os.getenv("S7G_API_URL")
        if url: return url
        url = os.getenv("SERVEO_URL") or os.getenv("SERVEO_FALLBACK")
        if url: return url
        return None

    def _sign(self, path: str, data: str = "") -> str:
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
        return _ic_call(AETHERDB, "aetherdb_put", [key, list(value.encode("utf-8"))])

    def icp_read(self, key: str) -> Optional[str]:
        r = _ic_call(AETHERDB, "aetherdb_get", [key])
        if r and isinstance(r, dict) and "Ok" in r:
            return bytes(r["Ok"]).decode("utf-8", errors="replace")
        return None

    # ═══════════════════════════════════════════════════════════════
    # CROSS-CHAIN SETTLEMENTS (via SHROUD Orchestrator)
    # ═══════════════════════════════════════════════════════════════
    #
    # These methods submit settlement requests to the SHROUD orchestrator
    # canister (txdkz-xqaaa-aaaaa-qhkea-cai). Each settlement is:
    #   - Attested by a 3-of-5 committee (hardware-backed, location-anchored)
    #   - Terms hidden via FE (only final result visible)
    #   - Finalized via 2-of-4 multi-ledger verification

    SHROUD_CANISTER = "txdkz-xqaaa-aaaaa-qhkea-cai"

    def _shroud_call(self, method: str, args: list) -> Optional[dict]:
        """Call the SHROUD orchestrator canister via IC HTTP API."""
        return _ic_call(self.SHROUD_CANISTER, method, args)

    def settlement_bitcoin(self, to_address: str, amount_sats: int) -> dict:
        """Settle on Bitcoin via SHROUD committee.
        
        The committee verifies the BTC transaction and finalizes via 2-of-4.
        Settlement terms are hidden — only the final result is visible.
        """
        return self._request("POST", "/api/settlement/bitcoin", {
            "to": to_address, "amount_sats": amount_sats, "identity": self.identity,
        })

    def settlement_evm(self, chain: str, to_address: str, amount_wei: int) -> dict:
        """Settle on an EVM chain via SHROUD committee.
        
        Supports Ethereum, Polygon, Arbitrum, Optimism, Base.
        """
        return self._request("POST", "/api/settlement/evm", {
            "chain": chain, "to": to_address, "amount_wei": amount_wei,
            "identity": self.identity,
        })

    def settlement_solana(self, to_address: str, amount_lamports: int) -> dict:
        """Settle on Solana via SHROUD committee.
        
        Solana's 400ms finality enables fast committee verification.
        """
        return self._request("POST", "/api/settlement/solana", {
            "to": to_address, "amount_lamports": amount_lamports,
            "identity": self.identity,
        })

    def settlement_elastos(self, carrier_id: str, service_type: str, units: int) -> dict:
        """Settle ELASTOS carrier services via SHROUD committee.
        
        Carrier location is attested via vAOM/DTC. Routing is computed
        via FHE (hidden from committee). Terms are hidden via FE.
        """
        return self._request("POST", "/api/settlement/elastos", {
            "carrier_id": carrier_id, "service_type": service_type, "units": units,
            "identity": self.identity,
        })

    def settlement_icp(self, to_principal: str, amount_e8s: int) -> dict:
        """Settle on ICP ledger via SHROUD committee.
        
        Native ICP settlement — uses the orchestrator canister directly.
        """
        return self._request("POST", "/api/settlement/icp", {
            "to": to_principal, "amount_e8s": amount_e8s,
            "identity": self.identity,
        })

    def settlement_status(self, ledger_id: str) -> dict:
        """Check the status of a cross-chain settlement."""
        return self._request("GET", f"/api/settlement/status?ledger_id={ledger_id}")

    def icp_list_type(self, prefix: str) -> list:
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
        return {"primary": self.icp_read("relayer:primary")}

    # ═══════════════════════════════════════════════════════════════
    # LoRA IOT
    # ═══════════════════════════════════════════════════════════════

    def lora_register_device(self, dev_eui: str, location: str = "") -> Optional[dict]:
        return _ic_call(AETHERDB, "aetherdb_put",
            [f"lora:device:{dev_eui}", json.dumps({"devEUI":dev_eui,"location":location,"ts":time.time()})])

    def lora_get_device(self, dev_eui: str) -> Optional[str]:
        return self.icp_read(f"lora:device:{dev_eui}")

    def lora_get_telemetry(self, dev_eui: str) -> list:
        return self.icp_list_type(f"lora:{dev_eui}")

    def lora_alert(self, dev_eui: str, alert_type: str, location: str,
                   contact: str = "+155****1234") -> bool:
        msg = f"[LoRA] {alert_type.upper()} at {dev_eui} ({location})"
        return _sip_message(contact, msg)

    # ═══════════════════════════════════════════════════════════════
    # VIRTUAL DSA / SCIENCE
    # ═══════════════════════════════════════════════════════════════

    def dsa_observe(self, target: str, freq_hz: float, bandwidth: float,
                    nodes: Optional[List[str]] = None, duration_s: int = 30) -> Dict:
        return self._request("POST","/api/dsa/observe",{
            "target":target,"freq_hz":freq_hz,"bandwidth":bandwidth,
            "nodes":nodes or [],"duration_s":duration_s})

    def dsa_frb_recent(self, minutes: int = 60) -> Dict:
        return self._request("GET",f"/api/dsa/frb?minutes={minutes}")

    def dsa_pulsar(self, name: str) -> Dict:
        return self._request("GET",f"/api/dsa/pulsar?name={name}")

    def dsa_rfi_report(self, node_id: Optional[str] = None) -> Dict:
        path = f"/api/dsa/rfi?node_id={node_id}" if node_id else "/api/dsa/rfi"
        return self._request("GET", path)

    def dsa_rfi_alert(self, band: str, power_dbm: float, node_id: str,
                      contact: str = "astronomer@7g.network") -> bool:
        return _sip_message(contact, f"[DSA RFI] {band}: {power_dbm:.1f} dBm at {node_id}")

    # ═══════════════════════════════════════════════════════════════
    # AI / 3GPP SPEC KNOWLEDGE
    # ═══════════════════════════════════════════════════════════════

    def spec_get_context(self, spec_id: str, clause: Optional[str] = None) -> Dict:
        return self._request("GET",f"/api/spec/context?spec={spec_id}&clause={clause or ''}")

    def spec_search(self, query: str) -> Dict:
        return self._request("GET",f"/api/spec/search?q={query}")

    def spec_for_component(self, component: str) -> Dict:
        return self._request("GET",f"/api/spec/component?name={component}")

    # ═══════════════════════════════════════════════════════════════
    # TEST INFRASTRUCTURE
    # ═══════════════════════════════════════════════════════════════

    def test_health(self) -> Dict:
        return self._request("GET","/api/test/health")

    def test_soak(self, hours: int = 1) -> Dict:
        return self._request("POST","/api/test/soak",{"hours":hours})

    def test_stress(self, requests: int = 100, workers: int = 10) -> Dict:
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

    # ── Emergency Response ───────────────────────────────────────
    def emergency_dispatch(self, inc_id: str) -> Dict:
        return self._request("POST","/api/emergency/dispatch",{"incident_id": inc_id})

    def emergency_fund(self, inc_id: str, amount: int) -> Dict:
        return self._request("POST","/api/emergency/fund",
                             {"incident_id": inc_id, "amount": amount})

    # ── AIOps & Federated Learning ───────────────────────────────
    def aiops_anomalies(self, hours: int = 24) -> Dict:
        return self._request("GET",f"/api/aiops/anomalies?hours={hours}")

    def aiops_patches(self, status: str = "open") -> Dict:
        return self._request("GET",f"/api/aiops/patches?status={status}")

    def federated_round(self) -> Dict:
        return self._request("GET","/api/federated/round")

    # ── Global Mesh ──────────────────────────────────────────────
    def mesh_routes(self) -> Dict:
        return self._request("GET","/api/mesh/routes")

    # ── GTME: Market & Adoption ──────────────────────────────────
    def adoption_metrics(self) -> Dict:
        return self._request("GET","/api/gtme/adoption")

    def competitive_intel(self, competitor: str = "") -> Dict:
        return self._request("GET",f"/api/gtme/intel?competitor={competitor}")


# ═══════════════════════════════════════════════════════════════════
# Domain method injection — extracted into sdk/py/s7g/domains/
# ═══════════════════════════════════════════════════════════════════

from .domains.bridge import (
    pos_settle, pos_verify, pos_status, POS_PLATFORMS, POS_CORRIDORS,
    court_executive_pause, court_executive_freeze,
    court_arbitration_file, court_arbitration_status,
    court_governance_params, court_governance_propose,
    cctp_bridge_status, cctp_transfer, stablecoin_routes,
    global_rate_card, solana_cctp_settle,
)
from .domains.yield_router import multi_yield_vault
from .domains.solana import (
    solana_validator_info, solana_validator_stake, solana_validator_unstake,
    solana_validator_rewards, solana_swap, solana_balance, solana_transfer,
    solana_moneygram_track, solana_network_stats, solana_depin_projects,
)
from .domains.agents import (
    swarm_status, swarm_agent_info, swarm_logs,
    AGENTS, COURTS, STABLECOINS, CHAINS,
)

for _name, _val in list(locals().items()):
    if _name.startswith(('pos_', 'court_', 'cctp_', 'stablecoin_', 'global_rate_',
                         'solana_', 'multi_yield_vault', 'swarm_',
                         'POS_', 'AGENTS', 'COURTS', 'STABLECOINS', 'CHAINS')):
        setattr(S7GClient, _name, _val)
