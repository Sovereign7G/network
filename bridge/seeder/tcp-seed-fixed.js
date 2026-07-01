#!/usr/bin/env node
const fs = require('fs')
const crypto = require('crypto')
const net = require('net')

const BINARY_PATH = process.env.S7G_BINARY_PATH || '/opt/s7g/shroud-enclave/current/sidecar'
const DISCOVERY_KEY_FILE = process.env.S7G_DISCOVERY_KEY_FILE || '/opt/s7g/shroud-enclave/.discovery-key'
const TCP_PORT = parseInt(process.env.S7G_TCP_PORT || '9090')

function getDiscoveryKey() {
    if (fs.existsSync(DISCOVERY_KEY_FILE)) {
        const key = fs.readFileSync(DISCOVERY_KEY_FILE, 'utf8').trim()
        if (key.length === 64) return key
    }
    const key = crypto.randomBytes(32).toString('hex')
    fs.writeFileSync(DISCOVERY_KEY_FILE, key)
    console.log(`[seeder] Generated new key: ${key.slice(0, 16)}...`)
    return key
}

function startTCPServer(discoveryKey) {
    const server = net.createServer((socket) => {
        let received = Buffer.alloc(0)
        socket.on('data', (chunk) => {
            received = Buffer.concat([received, chunk])
            if (received.length >= 32) {
                const receivedHex = received.slice(0, 32).toString('hex')
                if (receivedHex !== discoveryKey) {
                    console.log(`[seeder] Key mismatch (got ${receivedHex.slice(0, 16)}...)`)
                    socket.write(Buffer.from('KEY_MISMATCH'))
                    socket.end()
                    return
                }
                try {
                    const binary = fs.readFileSync(BINARY_PATH)
                    socket.write(binary)
                    console.log(`[seeder] Sent ${binary.length} bytes`)
                } catch(e) { console.log(`[seeder] Error: ${e.message}`) }
                socket.end()
            }
        })
        socket.on('error', () => {})
    })
    server.listen(TCP_PORT, '0.0.0.0', () => console.log(`[seeder] Port ${TCP_PORT}`))
    return server
}

const dk = getDiscoveryKey()
startTCPServer(dk)
console.log(`Key: ${dk.slice(0, 16)}...`)
