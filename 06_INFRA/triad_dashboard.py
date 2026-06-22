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
  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
  @media (max-width: 900px) { .grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }
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
      {label:'MCP Port 9000', val: v => v.mcp_port_9000 ? '✅ Up' : '❌ Down', cls: v => v.mcp_port_9000 ? 'green' : 'red'},
      {label:'REST Port 9001', val: v => v.rest_port_9001 ? '✅ Up' : '❌ Down', cls: v => v.rest_port_9001 ? 'green' : 'red'},
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
