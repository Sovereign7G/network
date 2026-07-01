#!/usr/bin/env node
/**
 * S7G Committee Discovery — P2P node discovery over Iroh
 * 
 * Committee members discover each other via Iroh relay by joining
 * a topic derived from the committee ID. Each node announces its
 * presence and the services it provides.
 * 
 * Usage:
 *   const discovery = new CommitteeDiscovery({ committeeId, relayUrl })
 *   const members = await discovery.start()
 *   console.log(members.size, 'committee members found')
 */

const { createHash } = require('crypto')

function sha256(data) {
    return createHash('sha256').update(Buffer.from(data)).digest()
}

class CommitteeDiscovery {
    constructor({ committeeId, relayUrl }) {
        this.committeeId = committeeId
        this.discoveryKey = sha256('s7g-committee:' + committeeId).toString('hex')
        this.relayUrl = relayUrl || 'http://localhost:3340'
        this.members = new Map()
        this._nodeId = null
    }

    async start() {
        console.log(`[discovery] Committee: ${this.committeeId}`)
        console.log(`[discovery] Discovery key: ${this.discoveryKey.slice(0, 16)}...`)
        
        // In production, use Iroh to join the committee topic.
        // For local testing, simulate by tracking this node's identity.
        this._nodeId = sha256('s7g-node:' + this.committeeId + Date.now()).toString('hex').slice(0, 24)
        
        this.members.set(this._nodeId, {
            nodeId: this._nodeId,
            services: ['attestation', 'consensus', 'provenance'],
            lastSeen: Date.now(),
            connected: true
        })
        
        console.log(`[discovery] Node ID: ${this._nodeId}`)
        console.log(`[discovery] Members: ${this.members.size}`)
        
        return this.members
    }

    async getCommitteeMembers() {
        return Array.from(this.members.values())
    }

    async getNodeId() {
        return this._nodeId
    }
}

module.exports = { CommitteeDiscovery }
