#!/usr/bin/env python3
"""
triad_dashboard.py — Live monitoring dashboard for the Sovereign OS Triad.

Serves dark-themed web UI on port 8080 showing real-time state of
Antigravity, Hermes, Odysseus, and the OKF bundle. Polls metrics
every 5 seconds via the TriadMetrics collector.

Usage:
    python3 triad_dashboard.py [port]
"""

import json
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Import metrics collector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from triad_metrics import TriadMetrics
from era2_phase2 import graph_data, OKFKnowledgeGraph, OKFRecommender

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
metrics = TriadMetrics()

# Cache for collected data
CACHE = {"status": {}, "events": [], "cache_time": 0}
CACHE_TTL = 3  # seconds
LOCK = threading.Lock()


def refresh_cache():
    """Periodically refresh cached metrics."""
    global CACHE
    while True:
        with LOCK:
            CACHE["status"] = metrics.collect()
            CACHE["events"] = metrics.events[-50:]
            CACHE["cache_time"] = time.time()
        time.sleep(CACHE_TTL)


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Triad Dashboard — Sovereign OS</title>
<style>
  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --dim: #8b949e; --green: #3fb950;
    --red: #f85149; --yellow: #d29922; --blue: #58a6ff;
    --purple: #bc8cff;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; padding: 20px; }
  h1 { font-size: 1.4rem; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
  h1 .sub { font-size: 0.8rem; color: var(--dim); font-weight: normal; margin-left: auto; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 16px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }
  .card h3 { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--dim); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
  .card .row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 0.85rem; }
  .card .row .label { color: var(--dim); }
  .card .row .value { font-weight: 500; }
  .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
  .dot.green { background: var(--green); }
  .dot.red { background: var(--red); }
  .dot.yellow { background: var(--yellow); }
  .big-num { font-size: 2rem; font-weight: 700; line-height: 1; }
  .metric-row { display: flex; gap: 24px; flex-wrap: wrap; }
  .metric-item { text-align: center; flex: 1; min-width: 80px; }
  .metric-item .num { font-size: 1.8rem; font-weight: 700; }
  .metric-item .lbl { font-size: 0.7rem; color: var(--dim); text-transform: uppercase; }
  .card.events { grid-column: span 4; }
  .event-log { max-height: 200px; overflow-y: auto; font-size: 0.8rem; }
  .event-log .entry { padding: 4px 0; border-bottom: 1px solid var(--border); display: flex; gap: 8px; }
  .event-log .entry:last-child { border: none; }
  .event-log .entry .time { color: var(--dim); white-space: nowrap; }
  .event-log .entry .sys { font-weight: 600; min-width: 80px; }
  .event-log .entry .msg { color: var(--text); }
  .sys-antigravity { color: var(--purple); }
  .sys-hermes { color: var(--blue); }
  .sys-odysseus { color: var(--green); }
  .sys-okf { color: var(--yellow); }
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
</head>
<body>
<h1>
  🪐 Triad Dashboard
  <span class="sub" id="uptime">Loading...</span>
</h1>

<div class="grid" id="systems"></div>

<div class="card" style="margin-bottom:16px">
  <h3>📊 Live Metrics</h3>
  <div class="metric-row" id="metrics"></div>
</div>

<div class="card events" style="margin-bottom:16px">
  <h3>📋 Event Log</h3>
  <div class="event-log" id="events"></div>
</div>

<script>
async function fetchJSON(url) {
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.status);
    return await r.json();
  } catch(e) { return null; }
}

function renderSystems(data) {
  const sys = data?.systems || {};
  const grid = document.getElementById('systems');
  grid.innerHTML = '';

  const cards = [
    {name:'🤖 Antigravity', key:'antigravity', color:'var(--purple)', fields:[
      {label:'Connected', val: v => v.connected ? '✅ Online' : '❌ Offline', cls: v => v.connected ? 'green' : 'red'},
      {label:'Artifacts', val: v => v.artifacts_total},
      {label:'MD Files', val: v => v.md_artifacts},
    ]},
    {name:'⚡ Hermes', key:'hermes', color:'var(--blue)', fields:[
      {label:'MCP Port 9002', val: v => v.mcp_port_9002 ? '✅ Up' : '❌ Down', cls: v => v.mcp_port_9002 ? 'green' : 'red'},
      {label:'REST Port 9002', val: v => v.rest_port_9002 ? '✅ Up' : '❌ Down', cls: v => v.rest_port_9002 ? 'green' : 'red'},
      {label:'Skills', val: v => v.skills},
      {label:'MCP Tools', val: v => v.mcp_total_tools},
    ]},
    {name:'🗄️ Odysseus', key:'odysseus', color:'var(--green)', fields:[
      {label:'API Port 9010', val: v => v.api_port_9010 ? '✅ Up' : '❌ Down', cls: v => v.api_port_9010 ? 'green' : 'red'},
      {label:'Bridge File', val: v => v.bridge_file ? '✅ Present' : '❌ Missing', cls: v => v.bridge_file ? 'green' : 'red'},
      {label:'Endpoints', val: v => v.endpoints},
    ]},
    {name:'📚 OKF Bundle', key:'okf', color:'var(--yellow)', fields:[
      {label:'Concepts', val: v => v.total_concepts},
      {label:'Types', val: v => v.registered_types},
      {label:'Git Commits', val: v => v.git_commits},
      {label:'Size', val: v => v.bundle_size_kb + ' KB'},
      {label:'Schema Validation', val: v => v.schema_validation ? '✅ Active' : '❌ Inactive', cls: v => v.schema_validation ? 'green' : 'red'},
    ]},
    {name:'🧬 S2L Adapters', key:'s2l', color:'var(--blue)', fields:[
      {label:'Active Adapter', val: v => v.active_adapter ? '🟢 ' + v.active_adapter : '⚪ None'},
      {label:'Parameters', val: v => v.active_parameters ? (v.active_parameters / 1000000).toFixed(2) + 'M' : '0M'},
      {label:'Trained Skills', val: v => v.trained_adapters ? v.trained_adapters.join(', ') : 'None'},
      {label:'Base Model', val: v => v.base_model || 'Unknown'},
      {label:'Avg Token Saving', val: v => v.token_saving_average ? v.token_saving_average + '%' : '0%'},
    ]},
    {name:'🔒 Privacy Gateway', key:'gateway', color:'var(--purple)', fields:[
      {label:'Active Policy', val: v => v.active_policy || 'default'},
      {label:'EU Data Residency', val: v => v.eu_data_residency ? '✅ Enabled' : '❌ Disabled', cls: v => v.eu_data_residency ? 'green' : 'dim'},
      {label:'Budget Cap', val: v => '$' + (v.budget_cap_usd || 50.0).toFixed(2)},
      {label:'Budget Spent', val: v => '$' + (v.budget_spent_usd || 0.0).toFixed(4), cls: v => (v.budget_spent_usd >= v.budget_cap_usd) ? 'red' : 'green'},
      {label:'PII Redaction', val: v => v.pii_redaction ? '✅ Active' : '❌ Inactive', cls: v => v.pii_redaction ? 'green' : 'dim'},
      {label:'Calls / Redacts', val: v => (v.total_calls || 0) + ' / ' + (v.total_redactions || 0)},
      {label:'Cache Hits / Rate', val: v => (v.cache_hits || 0) + ' (' + (v.cache_hit_rate_pct || 0.0) + '%)'},
      {label:'Avg Latency', val: v => (v.average_latency_ms || 0.0) + ' ms'}
    ]},
  ];

  for (const card of cards) {
    const state = sys[card.key] || {};
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<h3 style="color:${card.color}">${card.name}</h3>` +
      card.fields.map(f => {
        const val = f.val(state);
        const cls = f.cls ? f.cls(state) : '';
        return `<div class="row"><span class="label">${f.label}</span>` +
          `<span class="value"><span class="dot ${cls}"></span> ${val}</span></div>`;
      }).join('');
    grid.appendChild(div);
  }
}

function renderMetrics(data) {
  const req = data?.requests || {mcp:0, rest:0};
  const err = data?.errors || {mcp:0, rest:0};
  const el = document.getElementById('metrics');
  el.innerHTML = `
    <div class="metric-item"><div class="num">${req.mcp}</div><div class="lbl">MCP Calls</div></div>
    <div class="metric-item"><div class="num">${req.rest}</div><div class="lbl">REST Calls</div></div>
    <div class="metric-item"><div class="num">${err.mcp + err.rest}</div><div class="lbl">Errors</div></div>
    <div class="metric-item"><div class="num">${data?.systems?.okf?.total_concepts || 0}</div><div class="lbl">Concepts</div></div>
    <div class="metric-item"><div class="num">${data?.systems?.okf?.git_commits || 0}</div><div class="lbl">Git Commits</div></div>
    <div class="metric-item"><div class="num">${Math.floor((data?.uptime_seconds || 0) / 60)}m</div><div class="lbl">Uptime</div></div>
  `;
}

function renderEvents(data) {
  const el = document.getElementById('events');
  el.innerHTML = (data || []).slice(-30).reverse().map(e =>
    `<div class="entry">
      <span class="time">${e.time}</span>
      <span class="sys sys-${e.system?.toLowerCase()}">${e.system}</span>
      <span class="msg">${e.message}</span>
    </div>`
  ).join('');
}

function updateUptime(data) {
  const u = data?.uptime_seconds || 0;
  const h = Math.floor(u / 3600);
  const m = Math.floor((u % 3600) / 60);
  const s = u % 60;
  document.getElementById('uptime').textContent = `Uptime: ${h}h ${m}m ${s}s`;
}

async function refresh() {
  const data = await fetchJSON('/api/status');
  if (data) {
    renderSystems(data);
    renderMetrics(data);
    updateUptime(data);
  }
  const events = await fetchJSON('/api/events');
  if (events) renderEvents(events);
}

setInterval(refresh, 3000);
refresh();
</script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with LOCK:
            status = CACHE["status"]
            events = CACHE["events"]

        if self.path == "/api/status":
            self._json(status)
        elif self.path == "/api/events":
            self._json(events)
        elif self.path == "/api/metrics":
            self._json({"mcp_latency": metrics.avg_latency("mcp"),
                        "rest_latency": metrics.avg_latency("rest"),
                        "mcp_calls": metrics.request_counts["mcp"],
                        "rest_calls": metrics.request_counts["rest"],
                        "mcp_errors": metrics.errors["mcp"],
                        "rest_errors": metrics.errors["rest"]})
        elif self.path == "/api/graph":
            self._json(graph_data({}))
        elif self.path == "/api/semantic":
            self._html(SEMANTIC_HTML)
        else:
            self._html(HTML)

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _html(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def log_message(self, fmt, *args):
        pass  # Quiet

    # CORS for browsers
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def seed_events():
    """Add initial events to the log."""
    metrics.add_event("Antigravity", "MCP bridge ready — artifact capture active")
    metrics.add_event("Hermes", f"{46} MCP tools registered on port 9000")
    metrics.add_event("Odysseus", "REST endpoints ready on port 9010")
    metrics.add_event("OKF", "Knowledge bundle initialized — 11 types, schema validation active")
    metrics.add_event("Antigravity", "MCP bridge connected to port 9000")


# ── Semantic Dashboard (Era II) ─────────────────────────────────

SEMANTIC_HTML = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OKF Knowledge Graph — Semantic View</title>
<style>
  body{background:#0d1117;color:#e6edf3;font-family:system-ui,monospace;margin:0;padding:20px}
  h1{font-size:1.2rem;margin-bottom:20px}
  .layout{display:flex;gap:20px;height:calc(100vh-80px)}
  .graph-panel{flex:1;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;overflow:hidden;position:relative}
  .side-panel{width:320px;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;overflow-y:auto}
  .stat{margin:8px 0;padding:8px;background:#0d1117;border-radius:6px;display:flex;justify-content:space-between}
  .stat .label{color:#8b949e;font-size:0.8rem}
  .stat .value{font-weight:600}
  canvas{width:100%;height:calc(100% - 40px)}
  .recos{margin-top:16px}
  .reco-item{padding:6px 8px;margin:4px 0;border-radius:6px;cursor:pointer;font-size:0.85rem}
  .reco-item:hover{background:rgba(88,166,255,0.15)}
  .reco-item .sim{color:#8b949e;font-size:0.75rem}
  .tag{display:inline-block;padding:1px 6px;border-radius:4px;font-size:0.7rem;margin-right:4px;background:#30363d;color:#8b949e}
</style></head><body>
<h1>🧠 OKF Knowledge Graph <span style="color:#8b949e;font-size:0.8rem;font-weight:normal;margin-left:10px" id="stats"></span></h1>
<div class="layout">
<div class="graph-panel">
  <canvas id="graph"></canvas>
</div>
<div class="side-panel">
  <h3 style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;color:#8b949e">Recommendations</h3>
  <div id="recos" class="recos"><p style="color:#8b949e;font-size:0.85rem">Loading...</p></div>
</div>
</div>
<script>
async function init(){const r=await fetch('/api/graph');const d=await r.json();renderGraph(d);renderRecos(d)}
function renderGraph(d){document.getElementById('stats').textContent=`${d.nodes.length} concepts, ${d.edges.length} connections`;const c=document.getElementById('graph');const ctx=c.getContext('2d');c.width=c.parentElement.clientWidth-32;c.height=c.parentElement.clientHeight-80;const cx=c.width/2;const cy=c.height/2;const r=Math.min(cx,cy)*0.75;const pos={};d.nodes.forEach((n,i)=>{const a=(i/d.nodes.length)*2*Math.PI-Math.PI/2;pos[n.id]={x:cx+r*Math.cos(a),y:cy+r*Math.sin(a)}});ctx.clearRect(0,0,c.width,c.height);d.edges.forEach(e=>{ctx.strokeStyle='rgba(48,54,61,0.5)';ctx.lineWidth=e.weight*3;ctx.beginPath();ctx.moveTo(pos[e.source].x,pos[e.source].y);ctx.lineTo(pos[e.target].x,pos[e.target].y);ctx.stroke()});const colors={'ResearchFinding':'#bc8cff','EmailThread':'#58a6ff','EmailDraft':'#58a6ff','Document':'#3fb950','ModelComparison':'#d29922','Note':'#8b949e','CalendarEvent':'#f85149','SystemConfig':'#f0883e','KnowledgeBundle':'#e6edf3','KnowledgeIndex':'#6e7681'};d.nodes.forEach(n=>{ctx.beginPath();ctx.arc(pos[n.id].x,pos[n.id].y,8,0,2*Math.PI);ctx.fillStyle=colors[n.type]||'#8b949e';ctx.fill();ctx.strokeStyle='#0d1117';ctx.lineWidth=2;ctx.stroke();ctx.fillStyle='#e6edf3';ctx.font='11px system-ui';ctx.textAlign='center';const label=n.title.length>20?n.title.slice(0,20)+'...':n.title;ctx.fillText(label,pos[n.id].x,pos[n.id].y-14)})}
function renderRecos(d){if(!d.nodes.length)return;const seen=new Set();const el=document.getElementById('recos');el.innerHTML='';const sample=d.nodes.slice(0,10);sample.forEach(n=>{const div=document.createElement('div');div.className='reco-item';div.innerHTML=`<span>${n.title}</span> <span class="tag">${n.type}</span><br><span class="sim">${n.path}</span>`;div.onclick=()=>{fetch('/api/status').then(r=>r.json()).then(data=>{document.getElementById('stats').textContent=`Selected: ${n.path} | ${data.systems.okf.total_concepts} total concepts`})};el.appendChild(div)})}
init();setInterval(()=>fetch('/api/graph').then(r=>r.json()).then(d=>{renderGraph(d);renderRecos(d)}),10000);
</script></body></html>"""


if __name__ == "__main__":
    seed_events()

    # Start background cache refresher
    threading.Thread(target=refresh_cache, daemon=True).start()

    server = HTTPServer(("0.0.0.0", PORT), DashboardHandler)
    print(f"🪐 Triad Dashboard → http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
