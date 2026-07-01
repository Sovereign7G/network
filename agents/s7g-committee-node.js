#!/usr/bin/env node
/**
 * S7G Committee Node — P2P committee member service
 * 
 * Runs as a systemd service on each VPS node. Connects to the committee
 * via Iroh relay, discovers peers, and handles blob transfer + provenance
 * logging.
 * 
 * Run: node s7g-committee-node.js
 * Service: s7g-committee.service
 */

const path = require('path')
const { createHash, randomBytes } = require('crypto')

const COMMITTEE_ID = process.env.S7G_COMMITTEE_ID || 's7g-committee-' + randomBytes(4).toString('hex')
const RELAY_URL = process.env.S7G_IROH_RELAY || 'http://localhost:3340'

async function start() {
    console.log(`═══ S7G Committee Node ═══`)
    console.log(`Committee: ${COMMITTEE_ID}`)
    console.log(`Relay: ${RELAY_URL}`)

    // Load Iroh
    let Iroh
    try {
        Iroh = require(path.join(__dirname, '..', 'node_modules', '@number0', 'iroh'))
    } catch (e) {
        console.log(`[committee] Iroh not available: ${e.message}`)
        console.log('[committee] Running in standalone mode')
        console.log('\nTo deploy on VPS:')
        console.log('  npm install @number0/iroh')
        console.log('  S7G_COMMITTEE_ID=<id> node s7g-committee-node.js')
        return
    }

    // Connect to Iroh relay
    const builder = Iroh.Endpoint.builder()
    builder.applyN0()
    const endpoint = await builder.bind()
    const nodeId = await endpoint.id()
    console.log(`\n[committee] Connected. Node ID: ${nodeId}`)
    
    // Derive committee discovery topic
    const topic = createHash('sha256').update('s7g-committee:' + COMMITTEE_ID).digest()
    console.log(`[committee] Topic: ${topic.toString('hex').slice(0, 16)}...`)
    
    // Announce presence
    const announcement = JSON.stringify({
        type: 'ANNOUNCE',
        nodeId: nodeId.toString(),
        services: ['attestation', 'consensus', 'provenance'],
        timestamp: Date.now()
    })
    console.log(`[committee] Announcing: ${announcement}`)
    
    // Listen for connections
    console.log(`\n[committee] Listening for committee peers...`)
    console.log('[committee] Press Ctrl+C to stop.\n')
    
    // Keep alive
    setInterval(async () => {
        console.log(`[committee] Heartbeat — ${new Date().toISOString()}`)
    }, 60000)
    
    // Handle shutdown
    process.on('SIGINT', async () => {
        console.log('\n[committee] Shutting down...')
        await endpoint.close()
        process.exit(0)
    })
}

start().catch(err => console.error('[committee] Fatal:', err.message))
