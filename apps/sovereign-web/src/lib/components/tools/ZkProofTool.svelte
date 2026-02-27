<script lang="ts">
  import { fade } from "svelte/transition";

  let payload = "";
  let generating = false;
  let proof = "";

  function generateProof() {
    if (!payload) return;
    generating = true;
    proof = "";

    // Simulate ZK-SNARK generation delay
    setTimeout(() => {
      generating = false;
      proof = `zkp_${crypto.randomUUID().replace(/-/g, "")}_v1`;
    }, 1500);
  }
</script>

<div class="zk-tool">
  <div class="header-info">
    <p>
      Generate a Zero-Knowledge Proof to verify state without revealing
      underlying data.
    </p>
  </div>

  <div class="input-group">
    <label for="zk-payload">Payload to Prove</label>
    <textarea
      id="zk-payload"
      bind:value={payload}
      placeholder={"e.g., {'balance': '> 50000', 'kyc': true}"}
      rows="3"
    ></textarea>
  </div>

  <button
    class="generate-btn"
    onclick={generateProof}
    disabled={generating || !payload}
  >
    {generating ? "Synthesizing Circuit..." : "Generate ZK-SNARK"}
  </button>

  {#if proof}
    <div class="proof-result" in:fade>
      <label for="zk-proof-hash">Generated Proof Hash</label>
      <div class="hash-box">
        <code id="zk-proof-hash">{proof}</code>
        <button
          class="copy-btn"
          onclick={() => navigator.clipboard.writeText(proof)}>Copy</button
        >
      </div>
      <p class="success-text">✓ Ready for on-chain verification.</p>
    </div>
  {/if}
</div>

<style>
  .zk-tool {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .header-info p {
    margin: 0;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
  }

  .input-group label {
    display: block;
    font-size: 0.8rem;
    color: rgba(255, 215, 0, 0.7);
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  textarea {
    width: 100%;
    padding: 0.75rem;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 215, 0, 0.2);
    border-radius: 8px;
    color: white;
    box-sizing: border-box;
    font-family: monospace;
    resize: vertical;
  }

  textarea:focus {
    outline: none;
    border-color: #ffd700;
  }

  .generate-btn {
    padding: 1rem;
    background: linear-gradient(
      135deg,
      rgba(255, 215, 0, 0.2),
      rgba(255, 215, 0, 0.1)
    );
    border: 1px solid rgba(255, 215, 0, 0.5);
    border-radius: 8px;
    color: #ffd700;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
  }

  .generate-btn:hover:not(:disabled) {
    background: #ffd700;
    color: #0a0a0f;
  }

  .generate-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .proof-result {
    background: rgba(76, 175, 80, 0.1);
    border: 1px dashed rgba(76, 175, 80, 0.3);
    padding: 1rem;
    border-radius: 8px;
  }

  .proof-result label {
    display: block;
    font-size: 0.8rem;
    color: rgba(76, 175, 80, 0.8);
    margin-bottom: 0.5rem;
  }

  .hash-box {
    display: flex;
    gap: 0.5rem;
  }

  .hash-box code {
    flex: 1;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.4);
    border-radius: 4px;
    font-family: monospace;
    color: #4caf50;
    word-break: break-all;
  }

  .copy-btn {
    padding: 0 1rem;
    background: rgba(76, 175, 80, 0.2);
    border: none;
    border-radius: 4px;
    color: #4caf50;
    cursor: pointer;
  }

  .copy-btn:hover {
    background: rgba(76, 175, 80, 0.4);
  }

  .success-text {
    margin: 0.5rem 0 0 0;
    font-size: 0.8rem;
    color: #4caf50;
  }
</style>
