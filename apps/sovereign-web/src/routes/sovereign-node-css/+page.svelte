<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import '$lib/styles/css-state-machine.css';
  import { IntelligenceEngine } from '$lib/local-first/intelligence-engine';
  
  // JS only does heavy lifting - CSS handles the visuals
  let syncState = $state(0); // 0: idle, 1: syncing, 2: synced, 3: error
  let networkHealth = $state(87);
  let peerCount = $state(3);
  let zkVerified = $state(0);
  
  let newMemory = $state('');
  
  // CSS custom properties update - triggers visual changes without VDOM diffing overhead
  $effect(() => {
    if (!browser) return;
    
    document.documentElement.style.setProperty('--sync-state', syncState.toString());
    document.documentElement.style.setProperty('--network-health', networkHealth.toString());
    document.documentElement.style.setProperty('--peer-count', peerCount.toString());
    document.documentElement.style.setProperty('--zk-verification', zkVerified.toString());
    
    // For String content pseudo-elements, valid CSS uses quotes
    document.documentElement.style.setProperty('--zk-content', zkVerified === 1 ? '"✓ PROOF VERIFIED"' : '"○ PROOF PENDING"');
    // Animation play state
    document.documentElement.style.setProperty('--sync-animation-play', syncState === 1 ? 'running' : 'paused');
  });
  
  async function generateZKProof() {
    syncState = 1; // CSS shows pulsing indicator running
    
    // Simulate WASM proof generation heavy compute
    await new Promise(r => setTimeout(r, 2000));
    
    syncState = 2; // Success
    zkVerified = 1; // Verified state
  }

  async function commitMemory() {
      if (!newMemory.trim()) return;
      
      syncState = 1;

      try {
          const brain = await IntelligenceEngine.getInstance();
          await brain.storeEngram(newMemory);
          newMemory = '';
          syncState = 2; // Back to synced
          networkHealth = Math.min(100, networkHealth + 2); // Boost glow
      } catch (e) {
          syncState = 3; // Error
      }
  }
</script>

<div class="sovereign-node-css">
  <div class="global-network-glow" style="display: none;"></div>
  
  <header>
    <div class="header-titles">
        <h1>🌀 THE SOVEREIGN NODE</h1>
        <p class="subtitle">Avenue 3 Synthesis / CSS-Accelerated Computation</p>
    </div>
    
    <div class="status-bar">
      <!-- Pure CSS status indicators - no JS animations -->
      <div class="indicator-group pt-sync">
          <span>SYNC:</span>
          <div class="sync-indicator" title="Sync Status"></div>
      </div>
      
      <div class="peer-indicator" title="Mesh Nodes Connected">
        <svg viewBox="0 0 40 40" width="40" height="40">
          <circle class="peer-ring-bg" cx="20" cy="20" r="15" />
          <circle class="peer-ring" cx="20" cy="20" r="15" />
        </svg>
        <span>{peerCount} PEERS</span>
      </div>
      
      <div class="zk-badge">ZK: {zkVerified ? '✓' : '○'}</div>
    </div>
  </header>
  
  <div class="panels">
    <div class="panel brain-panel">
      <h2>🧠 Local Cognition (JS/WASM Compute)</h2>
      <div class="network-glow"></div> <!-- CSS computes opacity -->
      
      <div class="interaction">
          <textarea 
            placeholder="Imprint a private thought into local vector memory..."
            bind:value={newMemory}
          ></textarea>
          <button onclick={commitMemory} disabled={syncState === 1 || !newMemory}>
            COMMIT ENGRAM (JS Computes Embedding)
          </button>
      </div>
      
      <div class="metrics">
        <div class="metric">
          <span>Cloud API Calls</span>
          <span class="value" style:color="hsl(160, 80%, 60%)">0</span>
        </div>
      </div>
      <p class="caption">WASM vector embeddings process locally, visual feedback bypasses the JS main thread via CSS transitions.</p>
    </div>
    
    <div class="panel evidence-panel">
      <h2>🔐 Mesh Evidence (CSS Visualized)</h2>
      
      <div class="zk-container">
        <!-- CSS shows verification status pseudo-element dynamically driven by var() -->
        <div class="zk-proof"></div> 
        <button onclick={generateZKProof} class="proof-btn" disabled={syncState === 1}>
            GENERATE ZK PROOF (JS Computes)
        </button>
      </div>
      
      <div class="peer-mesh">
        <h3>🌐 GOSSIP MESH</h3>
        <!-- CSS computes ring visualization via arithmetic interpolation -->
        <div class="mesh-visualization">
          {#each Array(peerCount) as _, i}
            <div class="peer-node" style:--index={i} style:--total={peerCount}>
              P{i + 1}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .sovereign-node-css {
    min-height: 100vh;
    background-color: #020617;
    color: #f8fafc;
    font-family: 'Inter', 'Space Grotesk', sans-serif;
    padding: 2.5rem;
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
    font-size: 2.2rem;
    margin-top: 0;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #64ffda, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
  }
  
  .subtitle {
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    text-transform: uppercase;
    margin: 0;
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
    /* Computes hue strictly using CSS variable derived math */
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
    /* Uses geometric math driven by variable */
    stroke: hsl(calc(var(--peer-count) * 36deg), 80%, 60%);
    stroke-width: 4;
    fill: none;
    /* Circumference is approx 94.2 for r=15 */
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
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }

  .panel {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
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

  textarea {
    width: 100%;
    height: 120px;
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
      border-color: #64ffda;
  }

  button {
    background: rgba(100, 255, 218, 0.1);
    border: 1px solid #64ffda;
    color: #64ffda;
    padding: 0.85rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
    width: 100%;
  }

  button:hover:not(:disabled) {
    background: rgba(100, 255, 218, 0.2);
    box-shadow: 0 0 15px rgba(100, 255, 218, 0.2);
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

  .metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed rgba(255,255,255,0.1);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
  }
  
  .metric .value {
     font-size: 1.5rem;
     font-weight: bold;
  }
  
  .caption {
      font-size: 0.8rem;
      color: #64748b;
      margin-top: 1.5rem;
      font-style: italic;
  }
  
  .network-glow {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(0, 255, 0, calc(var(--network-health) / 100)),
      transparent
    );
    filter: blur(4px);
    transition: background 0.5s ease;
  }
  
  .zk-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
  }

  .zk-proof {
    padding: 2rem;
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
  }
  
  .peer-node {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    /* Hue circles through spectrum based on index/total ratio logic entirely native to CSS */
    border: 2px solid hsl(calc(var(--index) * 360deg / var(--total)), 80%, 60%);
    animation: breathe 2s ease infinite;
    animation-delay: calc(var(--index) * 0.2s);
  }
  
  @keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.6; box-shadow: none; }
    50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 15px hsl(calc(var(--index) * 360deg / var(--total)), 80%, 60%, 0.5); }
  }
</style>
