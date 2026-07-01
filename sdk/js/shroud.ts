/**
 * shroud.ts — SHROUD TypeScript SDK
 * Cross-chain trust coordination engine client for browser/Node.js apps.
 * 
 * Usage:
 *   import { SHROUDClient } from './shroud.js';
 *   const client = new SHROUDClient();
 *   await client.getCommittee('UsEast');
 */

const CANISTER_ID = 'txdkz-xqaaa-aaaaa-qhkea-cai';
const DFX_BIN = process.env.DFX_PATH || `${process.env.HOME}/.cache/dfinity/versions/0.32.0/dfx`;

export interface AttestedNode {
  node_id: string;
  mr_enclave: string;
  zone: string;
  dtc_rtt: number;
  last_attestation: number;
  is_active: boolean;
}

export interface Committee {
  zone: string;
  members: string[];
  epoch: number;
  threshold: number;
  valid_until: number;
}

export interface LatencyProfile {
  zone: string;
  min_rtt: number;
  max_rtt: number;
  mean: number;
  stddev: number;
  sample_count: number;
}

export class SHROUDClient {
  private canisterId: string;
  private dfxPath: string;
  
  constructor(canisterId: string = CANISTER_ID, dfxPath: string = DFX_BIN) {
    this.canisterId = canisterId;
    this.dfxPath = dfxPath;
  }
  
  private async dfxCall(method: string, args: string): Promise<string> {
    const { exec } = await import('child_process');
    
    return new Promise((resolve, reject) => {
      exec(
        `DFX_WARNING=-mainnet_plaintext_identity ${this.dfxPath} canister call ${this.canisterId} ${method} '${args}' --network ic`,
        { maxBuffer: 1024 * 1024 },
        (err, stdout, stderr) => {
          if (err) {
            reject(new Error(stderr));
            return;
          }
          // Strip deprecation warning
          const lines = stdout.split('\n').filter(l => !l.includes('dfx is deprecated'));
          resolve(lines.join('\n').trim());
        }
      );
    });
  }
  
  private formatZone(zone: string): string {
    return zone.charAt(0).toUpperCase() + zone.slice(1).toLowerCase();
  }
  
  // ── Node operations ──
  
  async getAttestedNodes(zone?: string): Promise<string> {
    const args = zone
      ? `(opt variant { ${this.formatZone(zone)} })`
      : '(null)';
    return this.dfxCall('get_attested_nodes', args);
  }
  
  async registerAttestation(
    nodeId: string,
    mrEnclave: string,
    zone: string,
    dtcRtt: number = 60,
    timestamp?: number
  ): Promise<boolean> {
    const ts = timestamp ?? Math.floor(Date.now() / 1000);
    const args =
      `(record { node_id = principal "${nodeId}"; ` +
      `mr_enclave = "${mrEnclave}"; ` +
      `zone = variant { ${this.formatZone(zone)} }; ` +
      `dtc_rtt = ${dtcRtt}; ` +
      `signature = vec {}; ` +
      `timestamp = ${ts}; })`;
    const result = await this.dfxCall('register_attestation', args);
    return result.includes('Ok');
  }
  
  // ── Committee operations ──
  
  async getCommittee(zone: string): Promise<string> {
    return this.dfxCall('get_committee', `(variant { ${this.formatZone(zone)} })`);
  }
  
  async rotateCommittee(zone: string): Promise<string> {
    return this.dfxCall('rotate_committee', `(variant { ${this.formatZone(zone)} })`);
  }
  
  async getCommitteeHealth(): Promise<string> {
    return this.dfxCall('get_committee_health', '()');
  }
  
  async recoverZone(zone: string): Promise<boolean> {
    const result = await this.dfxCall('recover_zone', `(variant { ${this.formatZone(zone)} })`);
    return result.includes('Ok');
  }
  
  async recoverSettlement(ledgerId: string): Promise<boolean> {
    const result = await this.dfxCall('recover_settlement', `("${ledgerId}")`);
    return result.includes('Ok');
  }
  
  async enterDegradedMode(zone: string): Promise<boolean> {
    const result = await this.dfxCall('enter_degraded_mode', `(variant { ${this.formatZone(zone)} })`);
    return result.includes('Ok');
  }
  
  async exitDegradedMode(zone: string): Promise<boolean> {
    const result = await this.dfxCall('exit_degraded_mode', `(variant { ${this.formatZone(zone)} })`);
    return result.includes('Ok');
  }
  
  async isZoneDegraded(zone: string): Promise<boolean> {
    const result = await this.dfxCall('is_zone_degraded', `(variant { ${this.formatZone(zone)} })`);
    return result.includes('true');
  }
  
  async getDegradedZones(): Promise<string> {
    return this.dfxCall('get_degraded_zones', '()');
  }
  
  // ── Settlement operations ──
  
  async getPendingSettlements(): Promise<string> {
    return this.dfxCall('get_pending_settlements', '()');
  }
  
  async submitSettlement(ledgerId: string, termsHash: string, threshold: number = 2): Promise<boolean> {
    const hashBytes = termsHash.match(/.{1,2}/g)?.map(b => '0x' + b).join('; ') || '';
    const args = `(record { ledger_id = "${ledgerId}"; terms_hash = vec { ${hashBytes} }; signatures = vec {}; threshold = ${threshold}; finalized = false; })`;
    const result = await this.dfxCall('submit_settlement', args);
    return result.includes('Ok');
  }
  
  async finalizeSettlement(ledgerId: string, signatures: string[]): Promise<boolean> {
    const sigs = signatures.map(s => `vec { ${s} }`).join('; ');
    const result = await this.dfxCall('finalize_settlement', `("${ledgerId}", vec { ${sigs} })`);
    return result.includes('Ok');
  }
  
  // ── Cross-Chain Settlement Operations ──
  
  /** Submit a Bitcoin settlement through the SHROUD committee. */
  async settleBitcoin(toAddress: string, amountSats: number): Promise<boolean> {
    const ledgerId = `bitcoin:${toAddress}`;
    // Simple commitment hash (would use FE in production)
    const hash = this.simpleHash(`${toAddress}:${amountSats}`);
    return this.submitSettlement(ledgerId, hash);
  }
  
  /** Submit an EVM chain settlement. */
  async settleEVM(chain: string, toAddress: string, amountWei: number): Promise<boolean> {
    const ledgerId = `evm:${chain}:${toAddress}`;
    const hash = this.simpleHash(`${chain}:${toAddress}:${amountWei}`);
    return this.submitSettlement(ledgerId, hash);
  }
  
  /** Submit a Solana settlement. */
  async settleSolana(toAddress: string, amountLamports: number): Promise<boolean> {
    const ledgerId = `solana:${toAddress}`;
    const hash = this.simpleHash(`solana:${toAddress}:${amountLamports}`);
    return this.submitSettlement(ledgerId, hash);
  }
  
  /** Submit an ELASTOS carrier settlement. */
  async settleElastos(carrierId: string, serviceType: string, units: number): Promise<boolean> {
    const ledgerId = `elastos:${carrierId}:${serviceType}`;
    const hash = this.simpleHash(`elastos:${carrierId}:${serviceType}:${units}`);
    return this.submitSettlement(ledgerId, hash);
  }
  
  /** Submit an ICP ledger settlement. */
  async settleICP(toPrincipal: string, amountE8s: number, memo: string = ''): Promise<boolean> {
    const ledgerId = `icp:${toPrincipal}`;
    const hash = this.simpleHash(`icp:${toPrincipal}:${amountE8s}:${memo}`);
    return this.submitSettlement(ledgerId, hash);
  }
  
  private simpleHash(input: string): string {
    // Simple hex hash for commitment (would be SHA256 in production)
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    // Pad to 64 hex chars
    return Math.abs(hash).toString(16).padStart(64, '0');
  }
  
  // ── Mesh operations ──
  
  async getMeshTopology(): Promise<string> {
    return this.dfxCall('get_mesh_topology', '()');
  }
  
  async formCrossZoneCommittee(zones: string[]): Promise<string> {
    const zoneArgs = zones.map(z => `variant { ${this.formatZone(z)} }`).join('; ');
    return this.dfxCall('form_cross_zone_committee', `(vec { ${zoneArgs} })`);
  }
  
  async getCrossZoneCommittee(zones: string[]): Promise<string> {
    const zoneArgs = zones.map(z => `variant { ${this.formatZone(z)} }`).join('; ');
    return this.dfxCall('get_cross_zone_committee', `(vec { ${zoneArgs} })`);
  }
  
  async getAllCrossZoneCommittees(): Promise<string> {
    return this.dfxCall('get_all_cross_zone_committees', '()');
  }
  
  async updateMeshTopology(connections: [string, string, number][]): Promise<boolean> {
    const connArgs = connections.map(([z1, z2, lat]) =>
      `variant { ${this.formatZone(z1)} }, variant { ${this.formatZone(z2)} }, ${lat}`
    ).join('; ');
    const result = await this.dfxCall('update_mesh_topology', `(vec { record { ${connArgs} } })`);
    return result.includes('Ok');
  }
  
  async getLatencyProfile(zone: string): Promise<string> {
    return this.dfxCall('get_latency_profile', `(variant { ${this.formatZone(zone)} })`);
  }
  
  async getAllLatencyProfiles(): Promise<string> {
    return this.dfxCall('get_all_latency_profiles', '()');
  }
  
  async getRecommendedBounds(zone: string): Promise<string> {
    return this.dfxCall('get_recommended_bounds', `(variant { ${this.formatZone(zone)} })`);
  }
  
  async resetCalibration(zone: string): Promise<boolean> {
    const result = await this.dfxCall('reset_calibration', `(variant { ${this.formatZone(zone)} })`);
    return result.includes('Ok');
  }
  
  async reportLatencySample(nodeId: string, zone: string, rtt: number): Promise<boolean> {
    const ts = Math.floor(Date.now() / 1000);
    const args =
      `(record { zone = variant { ${this.formatZone(zone)} }; ` +
      `node_id = principal "${nodeId}"; ` +
      `rtt = ${rtt}; ` +
      `timestamp = ${ts}; })`;
    const result = await this.dfxCall('report_latency_sample', args);
    return result.includes('Ok');
  }
}
