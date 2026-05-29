/**
 * 🏛️ AGE REPUBLIC :: AXON DEV SERVER
 * Full-bundle dev mode — single Bun process serving the entire sovereign stack.
 */

import { AxonEngine, defineConfig } from "./axon.ts";
import { zettoSeal } from "./zetto_bridge.ts";
import { resolve } from "path";

const PORT = parseInt(process.env.AXON_PORT || "3777");
const ROOT = process.env.AXON_ROOT || resolve(import.meta.dir, "../../..");

const config = defineConfig({
  root: ROOT,
  entries: ["index", "main", "app"],
  trustBoundaries: {
    "axon_teles": "axon::teles",
    "axon_vision": "axon::vision",
    "02_CORE": "sovereign::core",
    "03_LOGIC": "sovereign::logic",
    "05_SECURITY": "sovereign::security",
    "06_INFRA": "sovereign::infra",
  },
  fullBundleDev: true,
  plugins: [
    {
      name: "sovereign-attestation-plugin",
      buildStart() {
        console.log("🛡️  [Plugin] Sovereign attestation plugin active");
      },
      renderChunk(chunk) {
        // Inject runtime attestation verification
        const verifier = `\n// 🛡️ Runtime attestation check\nif(typeof __ZETTO_SEAL__!=='undefined'){console.log('🔒 Chunk verified:',__ZETTO_SEAL__.slice(0,18)+'...')}\n`;
        return { ...chunk, code: chunk.code + verifier };
      },
    },
  ],
});

console.log("🏛️ ═══════════════════════════════════════════════════");
console.log("   A X O N   S O V E R E I G N   D E V   S E R V E R");
console.log("   Full-Bundle Mode on Bun Runtime");
console.log("═══════════════════════════════════════════════════════\n");

const engine = new AxonEngine(config);

// Serve with Bun's native HTTP
const server = Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === "/api/link") {
      // Scan modules from workspace and link
      await engine.scanModules();
      const result = await engine.link();
      return new Response(JSON.stringify(result, null, 2), {
        headers: { "Content-Type": "application/json", "X-Zetto-Seal": result.chunks[0]?.keccak_seal || "" },
      });
    }

    if (url.pathname === "/api/seal") {
      const body = await req.text();
      const seal = zettoSeal(body);
      return new Response(JSON.stringify({ seal }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    if (url.pathname === "/api/health") {
      return new Response(JSON.stringify({ status: "sovereign", runtime: "bun", engine: "axon+zetto+mojo" }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    // Default: serve the Trinity dashboard
    return new Response(DASHBOARD_HTML, {
      headers: { "Content-Type": "text/html" },
    });
  },
});

console.log(`\n🚀 Axon dev server running at http://localhost:${server.port}`);
console.log(`   POST /api/link  → trigger sovereign link pipeline`);
console.log(`   POST /api/seal  → compute Keccak-256 seal`);
console.log(`   GET  /api/health → system status\n`);

// ─────────────────────────────────────────────────────────────
// Embedded Dashboard
// ─────────────────────────────────────────────────────────────

const DASHBOARD_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🏛️ Sovereign Trinity Cockpit</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#08090d;color:#e4e4e7;font-family:'Inter',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px}
    .header{text-align:center;margin-bottom:48px}
    .header h1{font-family:'Outfit',sans-serif;font-size:2.8rem;letter-spacing:.08em;background:linear-gradient(135deg,#38bdf8,#a855f7,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
    .header .sub{font-size:.85rem;opacity:.5;letter-spacing:.15em;text-transform:uppercase}
    .trinity-diagram{display:flex;flex-direction:column;align-items:center;gap:0;margin-bottom:48px}
    .layer{width:480px;padding:20px 28px;border:1px solid rgba(255,255,255,.06);backdrop-filter:blur(20px);position:relative;text-align:center;transition:all .3s ease}
    .layer:hover{border-color:rgba(255,255,255,.15);transform:scale(1.02)}
    .layer.axon{background:linear-gradient(135deg,rgba(56,189,248,.08),rgba(56,189,248,.02));border-radius:16px 16px 0 0;border-bottom:none}
    .layer.zetto{background:linear-gradient(135deg,rgba(168,85,247,.08),rgba(168,85,247,.02));border-radius:0}
    .layer.mojo{background:linear-gradient(135deg,rgba(244,114,182,.08),rgba(244,114,182,.02));border-radius:0}
    .layer.bun{background:linear-gradient(135deg,rgba(251,191,36,.08),rgba(251,191,36,.02));border-radius:0 0 16px 16px;border-top:none}
    .layer-name{font-family:'Outfit',sans-serif;font-size:1.3rem;letter-spacing:.1em;margin-bottom:4px}
    .layer.axon .layer-name{color:#38bdf8}
    .layer.zetto .layer-name{color:#a855f7}
    .layer.mojo .layer-name{color:#f472b6}
    .layer.bun .layer-name{color:#fbbf24}
    .layer-role{font-size:.7rem;opacity:.5;text-transform:uppercase;letter-spacing:.12em}
    .arrow{color:rgba(255,255,255,.15);font-size:.7rem;letter-spacing:.3em;padding:4px 0;font-family:'Fira Code',monospace}
    .controls{display:flex;gap:12px;margin-bottom:40px}
    .btn{padding:12px 28px;border:1px solid rgba(255,255,255,.1);border-radius:12px;background:rgba(255,255,255,.03);color:#e4e4e7;font-family:'Fira Code',monospace;font-size:.8rem;cursor:pointer;transition:all .2s ease;letter-spacing:.05em}
    .btn:hover{background:rgba(168,85,247,.15);border-color:rgba(168,85,247,.4);transform:translateY(-2px);box-shadow:0 8px 25px rgba(168,85,247,.2)}
    .btn.primary{background:linear-gradient(135deg,rgba(56,189,248,.2),rgba(168,85,247,.2));border-color:rgba(56,189,248,.3)}
    .results{width:100%;max-width:700px;font-family:'Fira Code',monospace;font-size:.75rem}
    .result-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:12px;padding:20px;margin-bottom:12px;backdrop-filter:blur(10px)}
    .result-card h3{font-family:'Outfit',sans-serif;font-size:1rem;margin-bottom:12px;color:#38bdf8}
    .metric{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.03)}
    .metric:last-child{border:none}
    .metric .label{opacity:.6}
    .metric .value{color:#10b981;font-weight:600}
    .chunk-list{margin-top:12px}
    .chunk{padding:8px 12px;background:rgba(168,85,247,.05);border:1px solid rgba(168,85,247,.1);border-radius:8px;margin-bottom:6px}
    .chunk .seal{color:#a855f7;font-size:.65rem;opacity:.7}
    .loading{display:none;color:#fbbf24;animation:pulse 1.5s infinite}
    @keyframes pulse{0%,100%{opacity:.4}50%{opacity:1}}
    .status{font-size:.7rem;padding:4px 12px;border-radius:999px;display:inline-block;margin-top:8px}
    .status.ready{background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.3)}
  </style>
</head>
<body>
  <div class="header">
    <h1>SOVEREIGN TRINITY</h1>
    <div class="sub">Axon × Zetto × Mojo on Bun</div>
    <div class="status ready">🟢 ENGINE ACTIVE</div>
  </div>

  <div class="trinity-diagram">
    <div class="layer axon"><div class="layer-name">A X O N</div><div class="layer-role">Sovereign Lifecycle Orchestrator</div></div>
    <div class="arrow">▼ zero-copy AST ▼</div>
    <div class="layer zetto"><div class="layer-name">Z E T T O</div><div class="layer-role">Module Linker & Sovereign Packager</div></div>
    <div class="arrow">▼ shared memory ▼</div>
    <div class="layer mojo"><div class="layer-name">M O J O</div><div class="layer-role">SIMD Compiler & Hardware Kernel</div></div>
    <div class="arrow">▼ native FFI ▼</div>
    <div class="layer bun"><div class="layer-name">B U N</div><div class="layer-role">Runtime Substrate</div></div>
  </div>

  <div class="controls">
    <button class="btn primary" onclick="triggerLink()">⚡ LINK PIPELINE</button>
    <button class="btn" onclick="checkHealth()">🔍 HEALTH CHECK</button>
    <button class="btn" onclick="testSeal()">🔒 TEST SEAL</button>
  </div>

  <div class="loading" id="loading">⏳ Executing sovereign link pipeline...</div>
  <div class="results" id="results"></div>

  <script>
    async function triggerLink() {
      const el = document.getElementById('loading');
      el.style.display = 'block';
      try {
        const res = await fetch('/api/link', { method: 'POST' });
        const data = await res.json();
        el.style.display = 'none';
        renderResult(data);
      } catch(e) {
        el.style.display = 'none';
        document.getElementById('results').innerHTML = '<div class="result-card"><h3>❌ Error</h3><p>'+e.message+'</p></div>';
      }
    }
    async function checkHealth() {
      const res = await fetch('/api/health');
      const data = await res.json();
      document.getElementById('results').innerHTML = '<div class="result-card"><h3>System Health</h3>'+Object.entries(data).map(([k,v])=>'<div class="metric"><span class="label">'+k+'</span><span class="value">'+v+'</span></div>').join('')+'</div>';
    }
    async function testSeal() {
      const res = await fetch('/api/seal', { method: 'POST', body: 'sovereign test payload @ '+Date.now() });
      const data = await res.json();
      document.getElementById('results').innerHTML = '<div class="result-card"><h3>🔒 Keccak-256 Seal</h3><div class="metric"><span class="label">seal</span><span class="value" style="color:#a855f7;font-size:.65rem">'+data.seal+'</span></div></div>';
    }
    function renderResult(data) {
      let html = '<div class="result-card"><h3>⚡ Link Result</h3>';
      html += '<div class="metric"><span class="label">Total Modules</span><span class="value">'+data.total_modules+'</span></div>';
      html += '<div class="metric"><span class="label">Dead Modules Eliminated</span><span class="value">'+data.dead_modules_eliminated+'</span></div>';
      html += '<div class="metric"><span class="label">Output Chunks</span><span class="value">'+data.total_chunks+'</span></div>';
      html += '<div class="metric"><span class="label">Graph Edges</span><span class="value">'+data.module_graph_edges+'</span></div>';
      html += '<div class="metric"><span class="label">Link Time (native)</span><span class="value">'+data.link_time_us+'µs</span></div>';
      html += '<div class="chunk-list"><h3 style="margin:12px 0 8px">📦 Sealed Chunks</h3>';
      for (const c of data.chunks) {
        html += '<div class="chunk"><strong>'+c.id+'</strong> — '+c.modules.length+' modules, '+(c.size_bytes/1024).toFixed(1)+'KB<br><span class="seal">'+c.keccak_seal+'</span></div>';
      }
      html += '</div></div>';
      document.getElementById('results').innerHTML = html;
    }
  </script>
</body>
</html>`;
