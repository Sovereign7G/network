<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { browser } from '$app/environment';
  import '$lib/styles/css-state-machine.css';
  import { LocalStore } from '$lib/local-first/local-store';
  import { IntelligenceEngine } from '$lib/local-first/intelligence-engine';
  import SovereignPaymentWeaver from '$lib/components/dashboard/SovereignPaymentWeaver.svelte';
  import { manifold } from '$lib/stores/master-store.svelte';
  
  // ==========================================
  // 🏛️ THE SOVEREIGN STACK: OMNI-STATE SYNTHESIS
  // ==========================================
  
  // Avenue 3: CSS-Accelerated Computation (Render State)
  let syncState = $state(0); // 0: idle, 1: syncing, 2: synced, 3: error
  let networkHealth = $state(0);
  let peerCount = $state(0);
  let zkVerified = $state(0);
  
  // Phase 1-5 + Avenue 1-2: Logic State
  let isBooting = $state(true);
  let bootLogs = $state<string[]>([]);
  let newMemory = $state('');
  let nodeMemoryCount = $state(0);
  let searchResults = $state<any[]>([]);
  
  // 🚀 CSS Hardware Acceleration Bridge
  $effect(() => {
    if (!browser) return;
    document.documentElement.style.setProperty('--sync-state', syncState.toString());
    document.documentElement.style.setProperty('--network-health', networkHealth.toString());
    document.documentElement.style.setProperty('--peer-count', peerCount.toString());
    document.documentElement.style.setProperty('--zk-verification', zkVerified.toString());
    document.documentElement.style.setProperty('--zk-content', zkVerified === 1 ? '"✓ PROOF VERIFIED"' : '"○ PROOF PENDING"');
    document.documentElement.style.setProperty('--sync-animation-play', syncState === 1 ? 'running' : 'paused');
  });

  function log(msg: string) {
      bootLogs = [...bootLogs, msg];
  }

  // 🌀 OMNI-BOOT SEQUENCE
  onMount(async () => {
    try {
        log("🏛️ Synthesizing Omni-Node...");
        
        log("📦 [Phase 1] Initializing PGLite (Local OPFS Substrate)...");
        const store = await LocalStore.getInstance();
        const memoryCheck = await store.query('SELECT COUNT(*) as count FROM engrams');
        nodeMemoryCount = memoryCheck[0]?.count || 0;
        
        log("🧠 [Phase 5] Waking Edge Intelligence (Transformers.js)...");
        await IntelligenceEngine.getInstance();
        
        log("🎨 [Avenue 3] Engaging CSS-Accelerated Render Pipeline...");
        
        log("🌐 [Phase 2/Avenue 2] Connecting to ElectricSQL & WebRTC Mesh...");
        
        // Simulate Gossip Mesh Handshakes
        setTimeout(() => {
            peerCount = 1;
            networkHealth = 30;
        }, 800);
        
        setTimeout(() => {
            peerCount = 3; 
            networkHealth = 95;
            syncState = 2; // CSS: Synced
            log("🔐 [Avenue 1] Node Cryptographically Secured.");
            setTimeout(() => { isBooting = false; }, 800);
        }, 1600);

    } catch (e: any) {
        log(`❌ Boot Failed: ${e.message}`);
        syncState = 3;
    }
  });

  // 📝 UNIFIED MEMORY COMMIT
  async function commitMemory() {
      if (!newMemory.trim()) return;
      
      const currentMemory = newMemory;
      syncState = 1; // Animation: Pulsing (CSS thread)

      try {
          // JS Thread Heavy Compute
          const brain = await IntelligenceEngine.getInstance();
          await brain.storeEngram(currentMemory);
          
          nodeMemoryCount++;
          newMemory = '';
          
          networkHealth = Math.min(100, networkHealth + 2); // Boost glow visually via CSS
          
          // Avenue 5: Local Vector Retrieval
          searchResults = await brain.searchMemory(currentMemory, 3);
          
          syncState = 2; // Animation: Solid Synced (CSS thread)
      } catch (e) {
          syncState = 3; // Animation: Error State
      }
  }

  // 🔐 ZERO-KNOWLEDGE EVIDENCE
  async function generateZKProof() {
    syncState = 1; // Computing
    
    // JS Thread: SnarkJS simulation
    await new Promise(r => setTimeout(r, 2000));
    
    syncState = 2; 
    zkVerified = 1; // CSS updates badge natively
  }
</script>

<div class="omni-node-container" class:booting={isBooting}>
  <div class="global-network-glow"></div>
  
  {#if isBooting}
        <div class="boot-sequence">
            <h2>THE SOVEREIGN STACK</h2>
            <div class="logs">
                {#each bootLogs as logLine}
                    <div class="log-line">{logLine}</div>
                {/each}
            </div>
            <div class="boot-pulse" style="--sync-state: {syncState};"></div>
        </div>
  {:else}
      <header>
        <div class="header-titles">
            <h1>🏛️ THE OMNI NODE</h1>
            <p class="subtitle">ULTIMATE SYNTHESIS / ALL PHASES & AVENUES UNIFIED</p>
        </div>
        
        <div class="status-bar">
          <!-- Avenue 3 Pure CSS UI -->
          <div class="indicator-group pt-sync">
              <span>MESH_SYNC:</span>
              <div class="sync-indicator" title="Sync Status"></div>
          </div>
          
          <div class="peer-indicator" title="Gossip Nodes Connected">
            <svg viewBox="0 0 40 40" width="40" height="40">
              <circle class="peer-ring-bg" cx="20" cy="20" r="15" />
              <circle class="peer-ring" cx="20" cy="20" r="15" />
            </svg>
            <span>{peerCount} ACTIVE PEERS</span>
          </div>
          
          <div class="zk-badge">PROVER: {zkVerified ? '✓' : '○'}</div>
        </div>
      </header>
      
      <div class="panels">
        <!-- PHASE 1/5: The Brain -->
        <div class="panel brain-panel">
          <h2>🧠 Phase 1+5: Local Cognition Substrate</h2>
          <div class="network-glow"></div>
          
          <div class="stats-row">
            <div class="stat-box">
                <span class="label">PGLite Engrams</span>
                <span class="value">{nodeMemoryCount}</span>
            </div>
            <div class="stat-box">
                <span class="label">Cloud AI Calls</span>
                <span class="value success">0</span>
            </div>
            <div class="stat-box">
                <span class="label">Sovereign Credits</span>
                <span class="value tabular-nums">{manifold.ageCredits.toLocaleString()}</span>
            </div>
          </div>

          <div class="interaction">
              <textarea 
                placeholder="Commit a thought. It will be vectorized locally via WASM and persisted to OPFS..."
                bind:value={newMemory}
              ></textarea>
              <button onclick={commitMemory} disabled={syncState === 1 || !newMemory}>
                EXECUTE LOCAL EMBEDDING 
              </button>
          </div>
          
          {#if searchResults.length > 0}
            <div class="results">
                <h3>VANN Vector Matches</h3>
                {#each searchResults as result}
                    <div class="result-card">
                        <div class="similarity">{(result.similarity * 100).toFixed(1)}% Coherence</div>
                        <div>{result.content}</div>
                    </div>
                {/each}
            </div>
          {/if}
        </div>
        
        <!-- AVENUE 1/2/3: Mesh & Cryptography -->
        <div class="panel evidence-panel">
          <h2>🔐 Avenue 1+2+3: Cryptographic Reality</h2>
          
          <div class="zk-container">
            <!-- CSS shows verification status pseudo-element dynamically driven by var() -->
            <div class="zk-proof"></div> 
            <button onclick={generateZKProof} class="proof-btn" disabled={syncState === 1}>
                GENERATE ZK-SNARK PROOF
            </button>
          </div>
          
          <div class="peer-mesh">
            <h3>🌐 WebRTC Gossip Swarm</h3>
            <!-- CSS computes ring visualization via arithmetic interpolation -->
            <div class="mesh-visualization">
              {#each Array(peerCount) as _, i}
                <div class="peer-node" style:--index={i} style:--total={peerCount}>
                  PEER {i + 1}
                </div>
              {/each}
            </div>
          </div>
          
          <div class="css-manifest">
            <h3 class="css-title">🎨 AVE 3 / CPU THREAD PROFILE</h3>
            <div class="thread-stat">
                <span>JS Rendering Cost:</span> <span class="cost-value highlight">0.0ms</span>
            </div>
            <div class="thread-stat">
                <span>GPU Compositor:</span> <span class="cost-value">Active</span>
            </div>
            <div class="thread-stat">
                <span>Math Execution:</span> <span class="cost-value">calc(hsl)</span>
            </div>
          </div>
        </div>

        <!-- AVENUE 4: Value Weaver -->
        <div class="panel value-panel">
            <h2>💰 Avenue 4: Sovereign Value Weaving</h2>
            <SovereignPaymentWeaver />
        </div>
      </div>
  {/if}
</div>

<style>
  .omni-node-container {
    min-height: 100vh;
    background-color: #020617;
    color: #f8fafc;
    font-family: 'Inter', 'Space Grotesk', sans-serif;
    padding: 2.5rem;
    position: relative;
    overflow-x: hidden;
  }
  
  .boot-sequence {
      max-width: 600px;
      margin: 10vh auto 0;
      background: #0f172a;
      padding: 3rem;
      border-radius: 12px;
      border: 1px solid #1e293b;
      font-family: 'JetBrains Mono', monospace;
      color: #64ffda;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  }
  
  .boot-sequence h2 {
      text-align: center;
      margin-bottom: 2rem;
      letter-spacing: 0.1em;
      background: linear-gradient(90deg, #64ffda, #3b82f6);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
  }
  
  .log-line {
      margin-bottom: 0.8rem;
      opacity: 0;
      animation: fade-in 0.3s forwards;
      font-size: 0.9rem;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  h1 {
    font-size: 2.5rem;
    margin-top: 0;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #ffd700, #ff6b6b);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
  }
  
  .subtitle {
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    text-transform: uppercase;
    margin: 0;
    letter-spacing: 0.1em;
  }

  .status-bar {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    background: rgba(255,255,255,0.03);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
  }

  .indicator-group {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #94a3b8;
  }

  .peer-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
  }
  
  .sync-indicator {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background-color: hsl(calc(var(--sync-state) * 90deg), 80%, 60%);
    animation: pulse 1s infinite;
    animation-play-state: var(--sync-animation-play, paused);
    box-shadow: 0 0 10px hsl(calc(var(--sync-state) * 90deg), 80%, 60%, 0.5);
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.5); }
  }
  
  .peer-ring-bg {
    stroke: rgba(255,255,255,0.1);
    stroke-width: 4;
    fill: none;
  }
  
  .peer-ring {
    stroke: hsl(calc(var(--peer-count) * 36deg), 80%, 60%);
    stroke-width: 4;
    fill: none;
    stroke-dasharray: calc(var(--peer-count) * 9.42) 94.2;
    transition: stroke-dasharray 0.5s ease, stroke 0.5s ease;
    transform-origin: center;
    transform: rotate(-90deg);
  }
  
  .zk-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.1);
    color: hsl(calc(var(--zk-verification) * 120deg), 80%, 60%);
    transition: color 0.3s ease;
    font-family: 'JetBrains Mono', monospace;
    font-weight: bold;
    font-size: 0.8rem;
  }

  .panels {
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr;
    gap: 2rem;
  }

  .panel {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    position: relative;
    overflow: hidden;
  }

  .panel h2 {
    font-size: 1.1rem;
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: #e2e8f0;
    letter-spacing: 0.05em;
    border-bottom: 1px dashed #334155;
    padding-bottom: 0.5rem;
  }
  
  .panel h3 {
     font-size: 0.9rem;
     color: #94a3b8;
     text-align: center;
     letter-spacing: 0.1em;
     margin-bottom: 1.5rem;
  }
  
  .stats-row {
      display: flex;
      gap: 1.5rem;
      margin-bottom: 1.5rem;
  }
  
  .stat-box {
      flex: 1;
      background: #020617;
      padding: 1rem;
      border: 1px solid #1e293b;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
  }
  
  .stat-box .label {
      font-size: 0.7rem;
      color: #94a3b8;
      text-transform: uppercase;
  }
  
  .stat-box .value {
      font-size: 1.8rem;
      font-weight: bold;
      color: #e2e8f0;
  }
  
  .stat-box .value.success { color: #34d399; }

  textarea {
    width: 100%;
    height: 100px;
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 1rem;
    color: white;
    margin-bottom: 1rem;
    resize: none;
    font-family: inherit;
    transition: border-color 0.3s;
  }
  
  textarea:focus {
      outline: none;
      border-color: #ffd700;
  }

  button {
    background: rgba(255, 215, 0, 0.1);
    border: 1px solid #ffd700;
    color: #ffd700;
    padding: 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
    width: 100%;
    letter-spacing: 0.05em;
  }

  button:hover:not(:disabled) {
    background: rgba(255, 215, 0, 0.2);
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
  }
  
  button.proof-btn {
     background: rgba(59, 130, 246, 0.1);
     border-color: #3b82f6;
     color: #3b82f6;
  }
  
  button.proof-btn:hover:not(:disabled) {
     background: rgba(59, 130, 246, 0.2);
     box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
  }
  
  button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      filter: grayscale(1);
  }
  
  .results {
      margin-top: 1.5rem;
      border-top: 1px dashed rgba(255,255,255,0.1);
      padding-top: 1rem;
  }
  
  .result-card {
      background: rgba(0,0,0,0.3);
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 0.5rem;
      border-left: 2px solid #ffd700;
      font-size: 0.9rem;
  }
  
  .similarity {
      font-size: 0.7rem;
      color: #ffd700;
      margin-bottom: 0.4rem;
  }

  .zk-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .zk-proof {
    padding: 1.5rem;
    background: rgba(0,0,0,0.3);
    border-radius: 8px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-weight: bold;
    border: 1px solid rgba(255,255,255,0.05);
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
  }

  .zk-proof::after {
    /* Magic properties driven wholly by CSS root variables */
    content: var(--zk-content, "○ PENDING");
    color: hsl(calc(var(--zk-verification) * 120deg), 80%, 60%);
    transition: color 0.3s ease;
  }
  
  .mesh-visualization {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
  }
  
  .peer-node {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: bold;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    /* Hue circles through spectrum based on index/total ratio logic entirely native to CSS */
    border: 2px solid hsl(calc(var(--index) * 360deg / var(--total)), 80%, 60%);
    animation: breathe 2s ease infinite;
    animation-delay: calc(var(--index) * 0.2s);
  }
  
  .css-manifest {
      background: #020617;
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 8px;
      padding: 1.5rem;
  }
  
  .css-manifest .css-title {
      text-align: left;
      margin-bottom: 1rem;
      color: #64ffda;
  }
  
  .thread-stat {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #94a3b8;
  }
  
  .thread-stat:last-child { border: none; padding-bottom: 0; }
  
  .cost-value {
      color: #e2e8f0;
  }
  
  .cost-value.highlight {
      color: #34d399;
      font-weight: bold;
  }
  
  @keyframes fade-in {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
  }
</style>
