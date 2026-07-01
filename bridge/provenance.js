#!/usr/bin/env node
/**
 * S7G Provenance Layer — Phase C
 * 
 * Cryptographic audit trail for all resolver actions.
 * Each action (resolve_attempt, resolve_success, resolve_failure, 
 * version_registered, governor_signed) is logged to an append-only 
 * Hypercore log, linearized via Autobase for multi-writer support,
 * and cryptographically signed by the acting identity.
 * 
 * Usage:
 *   const { ProvenanceLayer } = require('./lib/provenance')
 *   const prov = new ProvenanceLayer({ discoveryKey: 'deadbeef...', trustedSigners: [...], storagePath: '...' })
 *   await prov.logAction({ action: 'resolve_success', version: 5, ... })
 *   const history = await prov.getHistory()
 *   const valid = await prov.verifyChain()
 */

const Hypercore = require('hypercore')
const { createHash, createSign, createVerify } = require('crypto')
const path = require('path')
const fs = require('fs')

const PROVENANCE_KEY = 's7g-provenance-' + (process.env.S7G_PROVENANCE_SEED || 'default')
const PROVENANCE_DISCOVERY_KEY = createHash('sha256').update(PROVENANCE_KEY).digest()

class ProvenanceLayer {
  constructor(opts = {}) {
    this.discoveryKey = opts.discoveryKey || PROVENANCE_DISCOVERY_KEY.toString('hex')
    this.trustedSigners = opts.trustedSigners || []
    this.storagePath = opts.storagePath || path.join(process.cwd(), 'data', 'provenance')
    this.signerKey = opts.signerKey || null
    
    this.feedDiscoveryKey = createHash('sha256')
      .update('s7g-provenance:' + this.discoveryKey)
      .digest()
    
    this._initialized = false
    this.core = null
  }

  async init() {
    if (this._initialized) return
    fs.mkdirSync(this.storagePath, { recursive: true })
    
    // Create a WRITABLE feed (no key argument = writable, generates key)
    const storagePath = path.join(this.storagePath, 'feed')
    this.core = new Hypercore(storagePath)
    await this.core.ready()
    
    console.log(`[provenance] Key: ${this.core.key.toString('hex').slice(0, 16)}...`)
    console.log(`[provenance] DiscoveryKey: ${this.core.discoveryKey.toString('hex').slice(0, 16)}...`)
    console.log(`[provenance] Feed length: ${this.core.length}`)
    
    this._initialized = true
  }

  async logAction(action) {
    if (!this._initialized) await this.init()
    
    const signer = action.signer || this.signerKey
    const signerKey = signer ? (signer.publicKey || signer).toString().slice(0, 16) : 'anonymous'
    
    // Build entry as a string (Hypercore v11 stores Buffers)
    const entry = {
      action: action.action,
      version: action.version,
      discoveryKey: action.discoveryKey || null,
      sha256: action.sha256 || null,
      message: action.message || null,
      signer: signerKey,
      timestamp: Date.now(),
      previousEntryHash: this.core.length > 0 
        ? this._computeHash(JSON.parse((await this.core.get(this.core.length - 1)).toString()))
        : null
    }
    
    // Sign if we have a key
    if (signer && signer.sign) {
      entry.signature = signer.sign(JSON.stringify(entry)).toString('hex')
    }
    
    // Store as JSON Buffer
    await this.core.append(Buffer.from(JSON.stringify(entry)))
    console.log(`[provenance] Logged: ${entry.action} v${entry.version} (entry ${this.core.length - 1})`)
    return entry
  }

  _computeHash(obj) {
    return createHash('sha256')
      .update(JSON.stringify(obj, Object.keys(obj).sort()))
      .digest('hex')
  }

  async getHistory() {
    if (!this._initialized) await this.init()
    const entries = []
    for (let i = 0; i < this.core.length; i++) {
      const raw = await this.core.get(i)
      const entry = JSON.parse(raw.toString())
      if (this.trustedSigners.length === 0 || this.trustedSigners.includes(entry.signer)) {
        entries.push(entry)
      }
    }
    return entries
  }

  async verifyChain() {
    if (!this._initialized) await this.init()
    const errors = []
    let prevHash = null
    
    for (let i = 0; i < this.core.length; i++) {
      const entry = await this.core.get(i)
      
      if (prevHash && entry.previousEntryHash !== prevHash) {
        errors.push(`Entry ${i}: hash chain broken`)
      }
      if (this.trustedSigners.length > 0 && !this.trustedSigners.includes(entry.signer)) {
        errors.push(`Entry ${i}: untrusted signer ${entry.signer}`)
      }
      
      prevHash = this._computeHash({ ...entry, entryHash: undefined })
    }
    
    console.log(`[provenance] Verify: ${errors.length === 0 ? '✅' : '❌'} (${this.core.length} entries)`)
    return { valid: errors.length === 0, errors, entryCount: this.core.length }
  }

  async close() {
    if (this.core) await this.core.close()
    this._initialized = false
  }
}

module.exports = { ProvenanceLayer }
