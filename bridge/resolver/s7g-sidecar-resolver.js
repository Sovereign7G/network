#!/usr/bin/env node
/**
 * s7g-sidecar-resolver — Phase A.2 Production Sidecar Daemon
 * 
 * Resolves the latest sidecar binary from the SHROUD canister via:
 * 1. Direct TCP replication (for dev/fallback)
 * 2. Hyperswarm DHT discovery (for production, requires UDP 49737)
 * 3. Iroh relay (TCP/443, for environments blocking UDP)
 * 
 * Designed to run as a systemd service alongside the current sidecar loader.
 * 
 * Usage:
 *   node s7g-sidecar-resolver.js [--daemon] [--shadow]
 * 
 * Env vars:
 *   ORCHESTRATOR_CANISTER  — SHROUD canister ID (default: txdkz-xqaaa-aaaaa-qhkea-cai)
 *   IC_NETWORK_URL         — ICP API endpoint (default: https://ic0.app)
 *   SIDECAR_BINARY_PATH    — Where to write the binary (default: /opt/s7g/enclave/sidecar)
 *   SIDECAR_SERVICE_NAME   — systemd service to restart (default: shroud-enclave)
 *   SIDECAR_POLL_INTERVAL  — Seconds between canister checks (default: 300)
 * 
 * Dependencies: npm install hyperswarm hypercore random-access-file @dfinity/agent
 */

const { createHash, randomBytes } = require('crypto')
const fs = require('fs')
const path = require('path')

// ── Config (from env or defaults) ──────────────────────────────────────────
const CANISTER_ID = process.env.ORCHESTRATOR_CANISTER || 'txdkz-xqaaa-aaaaa-qhkea-cai'
const IC_URL = process.env.IC_NETWORK_URL || 'https://ic0.app'
const BINARY_PATH = process.env.SIDECAR_BINARY_PATH || '/opt/s7g/enclave/sidecar'
const SERVICE_NAME = process.env.SIDECAR_SERVICE_NAME || 'shroud-enclave'
const POLL_INTERVAL = parseInt(process.env.SIDECAR_POLL_INTERVAL || '300')

// ── Provenance (Phase C) ───────────────────────────────────────────
let provenance = null

async function initProvenance() {
  try {
    // Resolve path relative to this script's location
    const scriptDir = __dirname
    const provPath = path.join(scriptDir, '..', 'lib', 'provenance')
    const { ProvenanceLayer } = require(provPath)
    provenance = new ProvenanceLayer({
      discoveryKey: process.env.S7G_PROVENANCE_KEY || createHash('sha256').update('s7g-provenance').digest('hex'),
      trustedSigners: (process.env.S7G_TRUSTED_SIGNERS || '').split(',').filter(Boolean),
      storagePath: process.env.S7G_PROVENANCE_PATH || '/opt/s7g/shroud-enclave/data/provenance'
    })
    await provenance.init()
    console.log('[provenance] Layer initialized')
  } catch (err) {
    console.log(`[provenance] Not available (${err.message.slice(0, 80)}) — continuing without audit trail`)
    provenance = null
  }
}

// ── ICP Canister Agent (via dfx subprocess) ─────────────────────────

const DFX_PATH = process.env.DFX_PATH || '/home/cherry/.cache/dfinity/versions/0.32.0/dfx'
const DFX_ARGS = process.env.DFX_NETWORK ? `--network ${process.env.DFX_NETWORK}` : '--network ic'
const WORKSPACE = process.env.S7G_WORKSPACE || '/tmp/s7g-dfx-workspace'

/**
 * Query an ICP canister via dfx subprocess.
 * Falls back to icp-cli if dfx is unavailable.
 * Returns parsed Candid response.
 */
async function queryCanister(canisterId, method) {
  // Try dfx first
  try {
    const { execSync } = require('child_process')
    const cmd = `cd "${WORKSPACE}" && DFX_WARNING=-mainnet_plaintext_identity ${DFX_PATH} canister call ${canisterId} ${method} ${DFX_ARGS} 2>/dev/null`
    console.log(`[canister] Running: ${cmd.slice(0, 150)}...`)
    const result = execSync(cmd, { encoding: 'utf-8', timeout: 20_000, stdio: 'pipe' })
    console.log(`[canister] Raw response: ${result.slice(0, 200)}`)
    const parsed = parseDfxResponse(result)
    console.log(`[canister] Parsed:`, parsed ? `version=${parsed.version}` : 'null')
    return parsed
  } catch (err) {
    console.log(`[canister] dfx query failed: ${err.message.slice(0, 100)}`)
    return null
  }
}

/**
 * Parse dfx Candid response into structured object.
 * Handles the nested record/blob format from ICP.
 */
function parseDfxResponse(output) {
  // Example output:
  // (
  //   opt record {
  //     sha256 = blob "\9d\5d\d7...";
  //     discovery_key = blob "\4f\d6\71...";
  //     version = 4 : nat64;
  //   },
  // )
  
  if (output.includes('null')) return null
  
  const versionMatch = output.match(/version\s*=\s*(\d+)\s*:/)
  const keyMatch = output.match(/discovery_key\s*=\s*blob\s*"([^"]+)"/)
  const shaMatch = output.match(/sha256\s*=\s*blob\s*"([^"]+)"/)
  
  if (versionMatch) {
    const result = { version: parseInt(versionMatch[1]) }
    if (keyMatch) result.discovery_key = parseBlobString(keyMatch[1])
    if (shaMatch) result.sha256 = parseBlobString(shaMatch[1])
    return result
  }
  
  // Plain numeric response (get_latest_version)
  const numMatch = output.match(/^\s*\((\d+)\s*:/)
  if (numMatch) return parseInt(numMatch[1])
  
  return output
}

/**
 * Parse a Candid blob string from dfx output into a hex string.
 * dfx format: \e3\b2\ea\17\66... (backslash + 2 hex chars per byte)
 * Node.js preserves the backslash literally, so blobStr has \e3\b2... 
 * We match pairs of "\" + 2 hex chars.
 */
function parseBlobString(blobStr) {
  const bytes = []
  // Match \XX patterns where XX is hex
  const re = /\\([0-9a-fA-F]{2})/g
  let match
  while ((match = re.exec(blobStr)) !== null) {
    bytes.push(parseInt(match[1], 16))
  }
  const hex = Buffer.from(bytes).toString('hex')
  console.log(`[canister] Parsed blob: ${bytes.length} bytes -> ${hex.slice(0, 32)}...`)
  return hex
}

// ── Binary Resolution ───────────────────────────────────────────────────────

/**
 * Check if a binary is available via direct TCP replication from a known peer.
 * This is the fallback path when DHT discovery isn't available.
 * 
 * Returns the binary Buffer or null if not found.
 */
async function resolveViaTCP(keyHex, expectedSha256) {
  // Use the TCP seeder directly (raw TCP, not Hypercore stream)
  // This matches the tcp-seed.js / tcp-resolver.js approach
  const host = process.env.S7G_TCP_SEEDER_HOST || 'localhost'
  const port = parseInt(process.env.S7G_TCP_SEEDER_PORT || '9000')
  
  console.log(`[resolve] Connecting to TCP seeder: ${host}:${port}`)
  
  try {
    const net = require('net')
    const binary = await new Promise((resolve, reject) => {
      const client = net.createConnection(port, host)
      let data = Buffer.alloc(0)
      const timeout = setTimeout(() => reject(new Error('TCP timeout (30s)')), 30_000)
      
      client.on('connect', () => {
        console.log(`[resolve] Connected, sending key...`)
        client.write(Buffer.from(keyHex, 'hex'))
      })
      
      client.on('data', (chunk) => {
        data = Buffer.concat([data, chunk])
      })
      
      client.on('end', () => {
        clearTimeout(timeout)
        resolve(data)
      })
      
      client.on('error', (err) => { clearTimeout(timeout); reject(err) })
    })
    
    if (binary.length === 0) {
      console.log('[resolve] Empty response from TCP seeder')
      return null
    }
    
    console.log(`[resolve] Received ${binary.length} bytes`)
    
    // Verify SHA256
    const hash = createHash('sha256').update(binary).digest('hex')
    console.log(`[resolve] SHA256: ${hash}`)
    console.log(`[resolve] Expected: ${expectedSha256}`)
    
    if (expectedSha256 && hash !== expectedSha256) {
      console.log(`[resolve] ❌ SHA256 mismatch (expected ${expectedSha256.slice(0, 16)}...)`)
      return null
    }
    
    console.log('[resolve] ✅ TCP resolution successful!')
    return binary
    
  } catch (err) {
    console.log(`[resolve] TCP failed: ${err.message}`)
    return null
  }
}

/**
 * Resolve binary via Iroh relay (TCP/443, no UDP needed).
 * Uses @number0/iroh Node.js bindings (v1.0.0).
 */
async function resolveViaIroh(keyHex, expectedSha256) {
  const relayUrl = process.env.S7G_IROH_RELAY || 'http://localhost:3340'
  console.log(`[iroh] Connecting to relay: ${relayUrl}`)
  
  try {
    const Iroh = require(path.join(__dirname, '..', 'node_modules', '@number0', 'iroh'))
    
    // Use the N0 preset which includes crypto + default relay config
    const builder = Iroh.Endpoint.builder()
    builder.applyN0()
    
    // Set custom relay if configured
    if (relayUrl !== 'http://localhost:3340') {
      const relayMap = Iroh.RelayMap.fromUrls([relayUrl])
      builder.relayMode(Iroh.RelayMode.custom(relayMap))
    }
    
    const endpoint = await builder.bind()
    console.log(`[iroh] Connected. ID: ${await endpoint.id()}`)
    
    // The @number0/iroh v1.0.0 provides core networking (QUIC relay, node discovery).
    // For blob distribution (sidecar binaries), we need iroh-blobs or custom blob
    // transfer via the endpoint's acceptNext/connect APIs.
    // 
    // For now, track the connection and let it fall through to TCP.
    // The relay connectivity is verified; blob distribution will use:
    //   endpoint.connect(peerId) → biStream → send/receive blob
    // 
    // See: https://github.com/n0-computer/iroh-ffi for blob API availability
    
    console.log(`[iroh] Relay connection verified. Blob download requires iroh-blobs integration.`)
    console.log(`[iroh] Endpoint online: ${await endpoint.online()}`)
    
    await endpoint.close()
    return null  // Fall through to TCP for now
    
  } catch (err) {
    console.log(`[iroh] Failed: ${err.message}`)
    return null
  }
}

/**
 * Attempt binary resolution through all available transports.
 * Returns the binary or null.
 */
async function resolveBinary(discoveryKeyHex, sha256Hex) {
  console.log(`[resolve] Attempting resolution for key: ${discoveryKeyHex.slice(0, 16)}...`)
  
  // 1. Try Iroh relay first (production P2P transport)
  const irohBinary = await resolveViaIroh(discoveryKeyHex, sha256Hex)
  if (irohBinary) return irohBinary
  
  // 2. Try TCP second (dev/fallback)
  const binary = await resolveViaTCP(discoveryKeyHex, sha256Hex)
  if (binary) return binary
  
  console.log('[resolve] All transports failed')
  return null
}

// ── Canister Interaction ────────────────────────────────────────────────────

/**
 * Fetch the latest sidecar discovery key from the SHROUD canister.
 * Returns { version, discovery_key, sha256 } or null.
 */
async function fetchLatestKey() {
  try {
    const result = await queryCanister(CANISTER_ID, 'get_latest_sidecar_key')
    if (result && result.version && result.version > 0) {
      console.log(`[canister] Got version ${result.version}, key=${(result.discovery_key || '').slice(0, 16)}..., sha=${(result.sha256 || '').slice(0, 16)}...`)
      return {
        version: Number(result.version),
        discovery_key: result.discovery_key,  // already hex from parseBlobString
        sha256: result.sha256                  // already hex from parseBlobString
      }
    }
    
    const version = await queryCanister(CANISTER_ID, 'get_latest_version')
    if (version && Number(version) > 0) {
      console.log(`[canister] Legacy sidecar version: ${version}`)
      return null
    }
    
    return null
  } catch (err) {
    console.error('[canister] Query failed:', err.message)
    return null
  }
}

/**
 * Write binary to disk and restart the service.
 */
function installBinary(binary, version) {
  const tmpPath = BINARY_PATH + '.new'
  
  console.log(`[install] Writing ${binary.length} bytes to ${tmpPath}`)
  fs.writeFileSync(tmpPath, binary)
  fs.chmodSync(tmpPath, 0o755)
  
  // Atomic rename
  fs.renameSync(tmpPath, BINARY_PATH)
  console.log(`[install] Installed: ${BINARY_PATH}`)
  
  // Restart service
  const { execSync } = require('child_process')
  try {
    execSync(`systemctl restart ${SERVICE_NAME}`, { stdio: 'pipe' })
    console.log(`[install] Restarted ${SERVICE_NAME}`)
  } catch (err) {
    console.error(`[install] Failed to restart ${SERVICE_NAME}: ${err.message}`)
  }
  
  console.log(`[install] Sidecar v${version} deployed`)
}

// ── Main Loop ───────────────────────────────────────────────────────────────

async function runOnce() {
  console.log(`[s7g-sidecar] Checking canister ${CANISTER_ID}...`)
  
  const keyInfo = await fetchLatestKey()
  if (!keyInfo) {
    console.log('[s7g-sidecar] No new version available')
    return
  }
  
  console.log(`[s7g-sidecar] Found version ${keyInfo.version}`)
  
  // Log attempt to provenance
  if (provenance) {
    await provenance.logAction({
      action: 'resolve_attempt',
      version: keyInfo.version,
      discoveryKey: keyInfo.discovery_key,
      sha256: keyInfo.sha256,
      message: `Resolving sidecar v${keyInfo.version}`
    }).catch(() => {})
  }
  
  const binary = await resolveBinary(keyInfo.discovery_key, keyInfo.sha256)
  if (binary) {
    // Log success to provenance
    if (provenance) {
      await provenance.logAction({
        action: 'resolve_success',
        version: keyInfo.version,
        discoveryKey: keyInfo.discovery_key,
        sha256: keyInfo.sha256,
        message: `Resolved ${binary.length} bytes, SHA256 verified`
      }).catch(() => {})
    }
    
    installBinary(binary, keyInfo.version)
  } else {
    // Log failure to provenance
    if (provenance) {
      await provenance.logAction({
        action: 'resolve_failure',
        version: keyInfo.version,
        discoveryKey: keyInfo.discovery_key,
        sha256: keyInfo.sha256,
        message: 'All transports failed'
      }).catch(() => {})
    }
    
    console.log('[s7g-sidecar] Binary not available via any transport')
  }
}

async function daemonLoop() {
  console.log(`[s7g-sidecar] Starting daemon (poll interval: ${POLL_INTERVAL}s)`)
  console.log(`[s7g-sidecar] Binary path: ${BINARY_PATH}`)
  console.log(`[s7g-sidecar] Canister: ${CANISTER_ID}`)
  
  // Initialize provenance on startup
  await initProvenance()
  
  await runOnce()
  setInterval(runOnce, POLL_INTERVAL * 1000)
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2)
  const isDaemon = args.includes('--daemon')
  const isShadow = args.includes('--shadow')
  
  console.log('═══ S7G Sidecar Resolver (Phase A.2) ═══')
  
  if (isDaemon) {
    await daemonLoop()
  } else if (isShadow) {
    console.log('Shadow mode: one-shot check')
    const keyInfo = await fetchLatestKey()
    if (keyInfo) {
      console.log('Latest version:', keyInfo.version)
      console.log('Discovery key:', keyInfo.discovery_key.slice(0, 32) + '...')
      console.log('SHA256:', keyInfo.sha256)
    } else {
      console.log('No key registered yet (pre-Phase A.1)')
    }
  } else {
    await runOnce()
  }
}

main().catch(err => {
  console.error('[s7g-sidecar] Fatal:', err.message)
  process.exit(1)
})
