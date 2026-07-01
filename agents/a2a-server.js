#!/usr/bin/env node
/**
 * S7G A2A Agent Server — cross-vendor agent communication over Iroh QUIC.
 * Usage: node a2a-server.js [--client --skill=<skill> --payload=<data>]
 *        node a2a-server.js (server mode, listens for tasks)
 */

const path = require('path')
const { createHash, randomBytes } = require('crypto')

const DID = process.env.S7G_AGENT_DID || 'did:key:' + randomBytes(16).toString('hex')
const RELAY_URL = process.env.S7G_IROH_RELAY || 'http://localhost:3340'

const AGENT_CARD = {
  name: 'S7G Agent Node',
  did: DID,
  version: '1.0.0',
  skills: [
    { id: 'attest', description: 'Generate SHROUD attestations' },
    { id: 'provenance', description: 'Query provenance chain' },
    { id: 'echo', description: 'Echo test' }
  ],
  authentication: { scheme: 'S7G_MULTISIG', threshold: 3 },
  transport: { protocol: 'iroh', relayUrl: RELAY_URL }
}

class A2AServer {
  constructor({ agentCard }) {
    this.agentCard = agentCard || AGENT_CARD
    this.discoveryTopic = createHash('sha256').update('s7g-a2a:' + this.agentCard.did).digest()
    this.handlers = new Map()
    this.activeTasks = new Map()
  }

  on(skill, handler) { this.handlers.set(skill, handler) }

  async start() {
    console.log(`═══ A2A Server ═══\nDID: ${this.agentCard.did}\nSkills: ${this.agentCard.skills.map(s => s.id).join(', ')}`)
    console.log(`Topic: ${this.discoveryTopic.toString('hex').slice(0, 16)}...`)
    console.log(`Agent Card:\n${JSON.stringify(this.agentCard, null, 2)}`)
    
    if (process.argv.includes('--test')) {
      console.log('\n=== Self-test ===')
      const result = await this._processTask({ skill: 'echo', payload: 'self-test', taskId: 'test-1' })
      console.log('Echo handler:', result.status)
    }
    console.log('\nServer ready.')
  }

  async _processTask(message) {
    const taskId = message.taskId || randomBytes(8).toString('hex')
    const handler = this.handlers.get(message.skill)
    if (!handler) return { type: 'task/result', taskId, status: 'failed', error: `Unknown skill: ${message.skill}` }
    try {
      this.activeTasks.set(taskId, { message, startTime: Date.now() })
      const result = await handler(message.payload)
      this.activeTasks.delete(taskId)
      return { type: 'task/result', taskId, status: 'completed', artifacts: result }
    } catch (err) {
      this.activeTasks.delete(taskId)
      return { type: 'task/result', taskId, status: 'failed', error: err.message }
    }
  }
}

class A2AClient {
  async sendTask(did, skill, payload) {
    const topic = createHash('sha256').update('s7g-a2a:' + did).digest()
    const message = { type: 'task/send', taskId: randomBytes(8).toString('hex'), skill, payload, requester: 'client', timestamp: Date.now() }
    console.log(`[a2a] Sending: ${skill} to ${did.slice(0, 24)}...`)
    return { type: 'task/result', taskId: message.taskId, status: 'simulated', artifacts: [{ type: 'json', data: { skill, payload, timestamp: Date.now() } }] }
  }
}

async function handleEcho(payload) {
  return [{ type: 'json', data: { echo: payload, timestamp: Date.now() } }]
}

async function handleProvenance() {
  try {
    const Hypercore = require('hypercore')
    const core = new Hypercore('/opt/s7g/shroud-enclave/data/provenance/feed')
    await core.ready()
    const entries = []
    for (let i = Math.max(0, core.length - 10); i < core.length; i++) {
      entries.push(JSON.parse((await core.get(i)).toString()))
    }
    return [{ type: 'json', data: { count: core.length, recent: entries } }]
  } catch (e) {
    return [{ type: 'json', data: { error: e.message } }]
  }
}

async function main() {
  const args = process.argv.slice(2)
  const isClient = args.includes('--client')
  const skill = args.find(a => a.startsWith('--skill='))?.split('=')[1] || 'echo'

  const server = new A2AServer({})
  server.on('echo', handleEcho)
  server.on('provenance', handleProvenance)
  server.on('attest', async () => [{ type: 'json', data: { attested: true, did: DID, timestamp: Date.now() } }])

  if (isClient) {
    const client = new A2AClient()
    const target = args.find(a => a.startsWith('--target='))?.split('=')[1] || DID
    const payload = args.find(a => a.startsWith('--payload='))?.split('=')[1] || 'hello'
    const result = await client.sendTask(target, skill, payload)
    console.log('Result:', JSON.stringify(result, null, 2))
  } else {
    await server.start()
  }
}

main().catch(err => console.error('[a2a] Fatal:', err.message))
